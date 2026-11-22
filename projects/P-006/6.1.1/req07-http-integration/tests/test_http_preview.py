"""Real loopback HTTP requests + independent SQLite reads for synthetic REQ-07."""

from __future__ import annotations

from pathlib import Path
from contextlib import closing
import json
import sqlite3
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener

from app import PreviewApplication, make_server

NOTICE = "LAB-NOTICE-01"
EMPLOYEE = "all employees"
FIELDS = {
    "service_name": "Maple Calendar",
    "maintenance_window": "Tuesday, 14:00–14:30 (lab time)",
    "employee_action": "Save any open calendar edits before 14:00.",
}
SOURCE = {**FIELDS, "ticket_reference": "LAB-INT-042"}
WRONG = "Service name: Maple Calendar\nMaintenance window: Tuesday at 15:00\nService-desk ticket reference: LAB-INT-042"
CLEAN = "Maple Calendar maintenance is Tuesday, 14:00–14:30 (lab time). Save any open calendar edits before 14:00."
READY = CLEAN


class HttpPreviewSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="p006-req07-")
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / "notices.sqlite"
        self.app = PreviewApplication(self.db)
        self.analyst = self.app.new_principal("analyst-fixture", "analyst")
        self.other = self.app.new_principal("other-reader-fixture", "analyst")
        self.reviewer = self.app.new_principal("reviewer-fixture", "reviewer")
        self.server = make_server(self.app)
        self.addCleanup(self.server.server_close)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.shutdown)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.opener = build_opener(ProxyHandler({}))

    def call(self, method, path, data=None, token=None):
        payload = json.dumps(data).encode("utf-8") if data is not None else None
        headers = {"Content-Type": "application/json"}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        request = Request(self.base + path, data=payload, method=method, headers=headers)
        try:
            with self.opener.open(request, timeout=3) as response:
                return response.status, json.loads(response.read())
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def create(self, candidate=WRONG, source=SOURCE, *, notice=NOTICE):
        return self.call("POST", "/notices", {"notice_id": notice, "candidate": candidate, "source_facts": source}, self.analyst)

    def confirm(self, audience=EMPLOYEE, rev=2, *, token=None):
        return self.call("POST", f"/notices/{NOTICE}/confirm", {"audience": audience, "expected_revision": rev}, token or self.analyst)

    def approve(self, fields=FIELDS, rev=2, *, token=None):
        return self.call("POST", f"/notices/{NOTICE}/approve", {"audience": EMPLOYEE, "expected_revision": rev, "approved_fields": fields}, token or self.reviewer)

    def preview(self, token=None):
        return self.call("POST", f"/notices/{NOTICE}/preview", {}, token or self.analyst)

    def state_db(self):
        # This is a different SQLite connection, independent of the HTTP response.
        with closing(sqlite3.connect(self.db)) as con:
            con.row_factory = sqlite3.Row
            row = con.execute("SELECT * FROM notices WHERE notice_id = ?", (NOTICE,)).fetchone()
            return dict(row) if row is not None else None

    def decision_rows(self):
        with closing(sqlite3.connect(self.db)) as con:
            return con.execute("SELECT actor_alias, operation, outcome, status_code FROM decisions ORDER BY rowid").fetchall()

    def prepare_ready(self, candidate=WRONG):
        self.assertEqual(self.create(candidate)[0], 201)
        self.assertEqual(self.confirm()[0], 200)
        self.assertEqual(self.approve()[0], 200)
        code, result = self.preview()
        self.assertEqual((code, result["status"], result["preview"]), (200, "READY", READY))
        return result

    def test_T03_A_wrong_model_draft_is_contained(self):
        result = self.prepare_ready()
        self.assertNotIn("LAB-INT-042", result["preview"])
        self.assertNotIn("15:00", result["preview"])
        stored = self.state_db()
        self.assertEqual(stored["ready"], 1)
        self.assertEqual(stored["preview"], READY)
        self.assertIn("LAB-INT-042", stored["candidate"])
        self.assertIn("LAB-INT-042", stored["source_facts"])
        self.assertEqual(stored["approved_reviewer"], "reviewer-fixture")

    def test_T03_B_clean_and_wrong_candidate_yield_same_preview(self):
        self.prepare_ready(candidate=CLEAN)
        self.assertEqual(self.state_db()["preview"], READY)

    def test_T03_C_missing_audience_confirmation_held(self):
        self.assertEqual(self.create()[0], 201)
        self.assertEqual(self.approve()[0], 200)
        code, result = self.preview()
        self.assertEqual((code, result["status"], result["reason"]), (200, "HELD", "audience_not_confirmed"))
        self.assertIsNone(result["preview"])
        self.assertEqual((self.state_db()["ready"], self.state_db()["preview"]), (0, None))

    def test_T03_D_stale_approval_rejected_and_held(self):
        self.assertEqual(self.create()[0], 201)
        self.assertEqual(self.confirm()[0], 200)
        old_code, old_data = self.approve(rev=1)
        self.assertEqual((old_code, old_data["error"]), (409, "stale_revision"))
        self.assertEqual(self.preview()[1]["status"], "HELD")
        self.assertIsNone(self.state_db()["approved_fields"])

    def test_T03_E_missing_required_approved_fact_refused(self):
        self.assertEqual(self.create()[0], 201)
        self.assertEqual(self.confirm()[0], 200)
        incomplete = {k: v for k, v in FIELDS.items() if k != "employee_action"}
        code, data = self.approve(incomplete)
        self.assertEqual((code, data["error"]), (400, "invalid_fields"))
        self.assertEqual(self.preview()[1]["status"], "HELD")
        self.assertEqual(self.state_db()["ready"], 0)

    def test_T03_F_wrong_confirmed_audience_held(self):
        self.assertEqual(self.create()[0], 201)
        self.assertEqual(self.confirm(audience="service desk")[0], 200)
        self.assertEqual(self.approve()[0], 200)
        self.assertEqual(self.preview()[1]["reason"], "audience_not_confirmed")
        self.assertEqual((self.state_db()["ready"], self.state_db()["preview"]), (0, None))

    def test_unauthenticated_and_invalid_credentials_cannot_create(self):
        req = {"notice_id": NOTICE, "candidate": WRONG, "source_facts": SOURCE}
        self.assertEqual(self.call("POST", "/notices", req, None)[0], 401)
        self.assertEqual(self.call("POST", "/notices", req, "invalid-token")[0], 401)
        self.assertIsNone(self.state_db())

    def test_reviewer_cannot_create_confirm_or_preview(self):
        self.assertEqual(self.call("POST", "/notices", {"notice_id": NOTICE, "candidate": WRONG, "source_facts": SOURCE}, self.reviewer)[0], 403)
        self.assertEqual(self.create()[0], 201)
        self.assertEqual(self.confirm(token=self.reviewer)[0], 403)
        self.assertEqual(self.preview(token=self.reviewer)[0], 403)
        self.assertEqual(self.state_db()["ready"], 0)

    def test_analyst_cannot_self_approve_or_spoof_reviewer(self):
        self.assertEqual(self.create()[0], 201)
        self.assertEqual(self.confirm()[0], 200)
        self.assertEqual(self.approve(token=self.analyst)[0], 403)
        code, data = self.call("POST", f"/notices/{NOTICE}/approve", {"expected_revision": 2, "audience": EMPLOYEE, "approved_fields": FIELDS, "role": "reviewer"}, self.analyst)
        self.assertEqual(code, 403)
        self.assertIsNone(self.state_db()["approved_reviewer"])
        self.assertEqual(self.preview()[1]["status"], "HELD")

    def test_unrelated_analyst_cannot_view_or_modify_other_notice(self):
        self.assertEqual(self.create()[0], 201)
        for method, path, data in [
            ("GET", f"/notices/{NOTICE}/state", None),
            ("POST", f"/notices/{NOTICE}/confirm", {"audience": EMPLOYEE, "expected_revision": 2}),
            ("POST", f"/notices/{NOTICE}/preview", {}),
        ]:
            self.assertEqual(self.call(method, path, data, self.other)[0], 404)
        self.assertEqual(self.state_db()["ready"], 0)
        self.assertIsNone(self.state_db()["confirmed_audience"])

    def test_revise_invalidates_existing_ready_state_and_approval(self):
        self.prepare_ready()
        revised = dict(SOURCE, employee_action="Close the calendar editor before 14:00.")
        code, result = self.call("POST", f"/notices/{NOTICE}/revise", {"expected_revision": 2, "candidate": WRONG, "source_facts": revised}, self.analyst)
        self.assertEqual((code, result["revision"], result["status"]), (200, 3, "HELD"))
        row = self.state_db()
        self.assertEqual((row["revision"], row["ready"], row["preview"]), (3, 0, None))
        self.assertIsNone(row["approved_fields"])
        self.assertIsNone(row["confirmed_audience"])
        self.assertEqual(self.approve(rev=2)[0], 409)
        self.assertEqual(self.confirm(rev=2)[0], 409)
        self.assertEqual(self.preview()[1]["status"], "HELD")

    def test_new_revision_can_be_approved_again(self):
        self.prepare_ready()
        revised = dict(SOURCE, employee_action="Close the calendar editor before 14:00.")
        self.assertEqual(self.call("POST", f"/notices/{NOTICE}/revise", {"expected_revision": 2, "candidate": WRONG, "source_facts": revised}, self.analyst)[0], 200)
        self.assertEqual(self.confirm(rev=3)[0], 200)
        self.assertEqual(self.approve(rev=3, fields={**FIELDS, "employee_action": revised["employee_action"]})[0], 200)
        code, data = self.preview()
        self.assertEqual(code, 200)
        self.assertIn("Close the calendar editor before 14:00.", data["preview"])
        self.assertNotIn("LAB-INT-042", data["preview"])
        self.assertEqual(self.state_db()["approved_revision"], 3)

    def test_reviewer_approval_requires_all_nonempty_allowed_fields(self):
        self.assertEqual(self.create()[0], 201)
        self.assertEqual(self.confirm()[0], 200)
        invalids = [
            ({**FIELDS, "employee_action": ""}, "incomplete_facts"),
            ({**FIELDS, "ticket_reference": "LAB-INT-042"}, "invalid_fields"),
            ({**FIELDS, "maintenance_window": 17}, "incomplete_facts"),
        ]
        for fields, expected_error in invalids:
            code, data = self.approve(fields)
            self.assertEqual((code, data["error"]), (400, expected_error))
        self.assertIsNone(self.state_db()["approved_fields"])
        self.assertEqual(self.state_db()["ready"], 0)

    def test_excluded_ticket_inside_approved_value_is_rejected(self):
        self.assertEqual(self.create()[0], 201)
        self.assertEqual(self.confirm()[0], 200)
        fields = {**FIELDS, "service_name": "Maple lab int 042 Calendar"}
        code, result = self.approve(fields)
        self.assertEqual((code, result["error"]), (400, "excluded_value_in_approved_facts"))
        self.assertEqual(self.preview()[1]["status"], "HELD")
        self.assertIsNone(self.state_db()["approved_fields"])

    def test_only_approved_preview_is_visible_to_owner(self):
        self.prepare_ready()
        code, data = self.call("GET", f"/notices/{NOTICE}/state", token=self.analyst)
        self.assertEqual(code, 200)
        self.assertEqual(data["preview"], READY)
        self.assertNotIn("candidate", json.dumps(data))
        self.assertNotIn("LAB-INT-042", json.dumps(data))
        self.assertEqual(self.call("GET", f"/notices/{NOTICE}/state", token=self.other)[0], 404)
        self.assertEqual(self.call("GET", f"/notices/{NOTICE}/state", token=self.reviewer)[0], 403)

    def test_no_publish_share_tool_or_delivery_endpoint(self):
        self.prepare_ready()
        for suffix in ("publish", "share", "send", "tool", "connector"):
            self.assertEqual(self.call("POST", f"/notices/{NOTICE}/{suffix}", {}, self.analyst)[0], 404)
        self.assertEqual(self.state_db()["preview"], READY)

    def test_decision_records_include_allowed_and_denied_without_content(self):
        self.prepare_ready()
        self.assertEqual(self.preview(token=self.reviewer)[0], 403)
        rows = self.decision_rows()
        self.assertTrue(any(row[2] == "allowed" for row in rows))
        self.assertTrue(any(row[2] == "denied" for row in rows))
        with closing(sqlite3.connect(self.db)) as con:
            raw = json.dumps(con.execute("SELECT * FROM decisions").fetchall())
        self.assertNotIn("LAB-INT-042", raw)
        self.assertNotIn("Dear Team", raw)
        self.assertNotIn(self.analyst, raw)

    def test_notice_identifier_and_duplicate_rejected(self):
        self.assertEqual(self.create()[0], 201)
        self.assertEqual(self.create()[0], 409)
        self.assertEqual(self.create(notice="unsafe/notice")[0], 400)
        with closing(sqlite3.connect(self.db)) as con:
            self.assertEqual(con.execute("SELECT COUNT(*) FROM notices").fetchone()[0], 1)

    def test_preview_recheck_after_audience_changed(self):
        self.prepare_ready()
        self.assertEqual(self.confirm("service desk")[0], 200)
        self.assertEqual(self.state_db()["ready"], 0)
        self.assertIsNone(self.state_db()["preview"])
        self.assertEqual(self.preview()[1]["status"], "HELD")

    def test_server_binds_only_to_loopback(self):
        from app import Rejected
        with self.assertRaises(Rejected):
            make_server(self.app, host="0.0.0.0", port=0)
        self.assertEqual(self.server.server_address[0], "127.0.0.1")


if __name__ == "__main__":
    unittest.main()

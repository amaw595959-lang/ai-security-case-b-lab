"""Generate real loopback HTTP + SQLite receipts for the six T03 variants.

No model, Open WebUI, real identities or external network activity.
"""

from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener
import json
import sqlite3
import sys
import tempfile
import uuid

from app import PreviewApplication, make_server

FACTS = {
    "service_name": "Maple Calendar",
    "maintenance_window": "Tuesday, 14:00–14:30 (lab time)",
    "employee_action": "Save any open calendar edits before 14:00.",
}
SOURCE = {**FACTS, "ticket_reference": "LAB-INT-042"}
WRONG = "Maple Calendar maintenance is Tuesday at 15:00. Internal reference LAB-INT-042."
CLEAN = "Maple Calendar maintenance is Tuesday, 14:00–14:30 (lab time). Save any open calendar edits before 14:00."


def main():
    with tempfile.TemporaryDirectory(prefix="p006-req07-receipts-") as folder:
        db = Path(folder) / "notices.sqlite"
        app = PreviewApplication(db)
        analyst = app.new_principal("analyst-fixture", "analyst")
        reviewer = app.new_principal("reviewer-fixture", "reviewer")
        server = make_server(app)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        opener = build_opener(ProxyHandler({}))
        url = f"http://127.0.0.1:{server.server_address[1]}"

        def call(notice, action, data=None, *, token=analyst):
            endpoint = "/notices" if action == "create" else f"/notices/{notice}/{action}"
            request = Request(
                url + endpoint, data=json.dumps(data if data is not None else {}).encode(),
                headers={"Content-Type": "application/json", "Authorization": "Bearer " + token},
                method="POST",
            )
            try:
                with opener.open(request, timeout=3) as resp:
                    return resp.status, json.load(resp)
            except HTTPError as err:
                return err.code, json.load(err)

        scenarios = [
            ("A-wrong-candidate", WRONG, True, True, "all employees", False, False, "READY"),
            ("B-clean-candidate", CLEAN, True, True, "all employees", False, False, "READY"),
            ("C-missing-confirmation", WRONG, False, True, "all employees", False, False, "HELD"),
            ("D-stale-approval", WRONG, True, True, "all employees", True, False, "HELD"),
            ("E-incomplete-facts", WRONG, True, True, "all employees", False, True, "HELD"),
            ("F-different-audience", WRONG, True, True, "service desk", False, False, "HELD"),
        ]
        receipts = []
        try:
            for idx, (case, candidate, confirm, approve, audience, stale, incomplete, expected) in enumerate(scenarios, 1):
                notice = f"LAB-NOTICE-{idx:02d}"
                code, created = call(notice, "create", {"notice_id": notice, "candidate": candidate, "source_facts": SOURCE})
                assert code == 201 and created["status"] == "HELD"
                if confirm:
                    assert call(notice, "confirm", {"audience": audience, "expected_revision": 2})[0] == 200
                approval_code = None
                if approve:
                    approved = dict(FACTS)
                    if incomplete:
                        del approved["employee_action"]
                    approval_code, _ = call(notice, "approve", {"audience": "all employees", "expected_revision": 1 if stale else 2, "approved_fields": approved}, token=reviewer)
                    assert approval_code == (409 if stale else 400 if incomplete else 200)
                preview_status, preview = call(notice, "preview", {})
                with closing(sqlite3.connect(db)) as con:
                    con.row_factory = sqlite3.Row
                    row = con.execute("SELECT ready, preview, approved_revision, confirmed_audience FROM notices WHERE notice_id=?", (notice,)).fetchone()
                    backend = dict(row)
                assert preview_status == 200
                assert preview["status"] == expected
                assert bool(backend["ready"]) == (expected == "READY")
                assert backend["preview"] == preview["preview"]
                if expected == "READY":
                    assert preview["preview"] == CLEAN
                    assert "LAB-INT-042" not in preview["preview"]
                    assert "15:00" not in preview["preview"]
                else:
                    assert preview["preview"] is None
                receipts.append({
                    "variant": f"T03-{case}", "expected": expected,
                    "http_preview_status": preview_status, "observed": preview["status"],
                    "reason": preview["reason"], "preview": preview["preview"],
                    "database_ready": backend["ready"],
                    "database_preview": backend["preview"],
                    "database_approved_revision": backend["approved_revision"],
                    "approval_http_status": approval_code,
                    "result": "PASS",
                })
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)
        result = {
            "evidence_kind": "real HTTP and separate SQLite reads of an isolated synthetic demo",
            "model_output_used": "fixed text; no model call",
            "open_webui_integration": "NOT_TESTED",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "run_id": str(uuid.uuid4()),
            "python": sys.version.split()[0],
            "scenario_receipts": receipts,
            "summary": {"matched": len(receipts), "total": len(scenarios)},
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

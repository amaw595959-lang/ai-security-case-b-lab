"""Offline metadata, failure handling and request-boundary checks."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "overlay"))
from capture import NOTICE_PATH, NoticeAuditMiddleware, NoticeEventPolicy


RESTRICTED = "fictional private reference"


def uid():
    return str(uuid4())


class EventPolicyTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.policy = NoticeEventPolicy(self.root, uid())
        self.actor = uid()
        self.chat = uid()
        self.request = SimpleNamespace(state=SimpleNamespace(p006_attempt_id=uid()))
        self.context = self.policy.admit(self.request, self.actor)

    def rows(self, journal):
        path = self.root / journal
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def event(self, kind, **overrides):
        fields = {
            "id": uid(), "event": kind, "actor": {"id": self.actor, "email": RESTRICTED},
            "subject": {"id": self.chat, "type": "chat"},
            "data": {"chat_id": self.chat, "content_preview": RESTRICTED, "nested": {"message": RESTRICTED}},
            "message": RESTRICTED,
        }
        return SimpleNamespace(**(fields | overrides))

    def start_chat(self):
        self.policy.deliver(self.request, self.event("chat.created"))

    def decisions(self):
        records = self.rows("decisions.jsonl")
        self.assertTrue(records)
        self.assertNotIn(RESTRICTED, json.dumps(records))
        return [(record["outcome"], record["reason"]) for record in records]

    def test_context_requires_server_admission(self):
        unrelated = SimpleNamespace(state=SimpleNamespace(p006_notice_context={"actor_id": self.actor}))
        self.assertTrue(self.policy.is_scoped(self.request))
        self.assertFalse(self.policy.is_scoped(unrelated))

    def test_metadata_only_preserves_native_order(self):
        self.start_chat()
        self.policy.deliver(self.request, self.event("message.created", subject={"id": uid(), "type": "message"}))
        self.policy.deliver(self.request, self.event("chat.finished"))
        actual = self.rows("events.jsonl")
        self.assertEqual([record["sequence"] for record in actual], [1, 2, 3])
        self.assertEqual([record["event_type"] for record in actual], ["chat.created", "message.created", "chat.finished"])
        self.assertEqual([record["attempt_id"] for record in actual], [self.context.attempt_id] * 3)
        self.assertNotIn(RESTRICTED, json.dumps(actual))
        self.assertNotIn(self.actor, json.dumps(actual))
        self.assertNotIn(self.chat, json.dumps(actual))

    def test_denies_unsupported_type_without_echo(self):
        self.policy.deliver(self.request, self.event(RESTRICTED))
        self.assertEqual(self.decisions(), [("denied", "unsupported_type")])
        self.assertFalse(self.rows("events.jsonl"))

    def test_denies_actor_and_resource_mismatches(self):
        self.start_chat()
        self.policy.deliver(self.request, self.event("chat.finished", actor={"id": uid()}))
        self.policy.deliver(self.request, self.event("chat.finished", data={"chat_id": uid()}))
        self.assertEqual(self.decisions(), [("denied", "actor_mismatch"), ("denied", "resource_mismatch")])
        self.assertEqual(len(self.rows("events.jsonl")), 1)

    def test_denies_malformed_envelopes(self):
        self.policy.deliver(self.request, self.event("chat.created", id=RESTRICTED))
        self.policy.deliver(self.request, self.event("chat.created", subject=RESTRICTED))
        self.policy.deliver(self.request, self.event("chat.created", data=[RESTRICTED]))
        self.assertEqual(self.decisions(), [("denied", "malformed_envelope")] * 3)
        self.assertFalse(self.rows("events.jsonl"))

    def test_duplicate_delivery_is_observable(self):
        original = self.event("chat.created")
        self.policy.deliver(self.request, original)
        self.policy.deliver(self.request, original)
        self.assertEqual(self.decisions(), [("duplicate", "duplicate_id")])
        self.assertEqual(len(self.rows("events.jsonl")), 1)

    def test_failure_events_preserve_security_observation_without_payload(self):
        self.start_chat()
        self.policy.deliver(self.request, self.event("chat.failed"))
        self.policy.deliver(self.request, self.event("model.provider_request.failed", subject={"type": "model"}))
        records = self.rows("events.jsonl")[1:]
        self.assertEqual([record["event_type"] for record in records], ["chat.failed", "model.provider_request.failed"])
        self.assertEqual([record["outcome"] for record in records], ["observed_failure"] * 2)
        self.assertNotIn(RESTRICTED, json.dumps(records))

    def test_failed_consumer_records_failure_and_allows_next_event(self):
        self.start_chat()
        real_write = self.policy._write

        def unavailable(journal, record):
            if journal == "events.jsonl":
                raise OSError(RESTRICTED)
            real_write(journal, record)

        event = self.event("chat.finished")
        with patch.object(self.policy, "_write", side_effect=unavailable):
            self.policy.deliver(self.request, event)
        self.assertEqual(self.decisions(), [("failed", "sink_failure")])
        self.assertEqual(len(self.rows("events.jsonl")), 1)
        self.policy.deliver(self.request, event)
        self.assertEqual(len(self.rows("events.jsonl")), 2)
        self.assertEqual(self.rows("events.jsonl")[-1]["event_type"], "chat.finished")

    def test_unavailable_decision_journal_has_body_free_console_fallback(self):
        with patch.object(self.policy, "_write", side_effect=OSError(RESTRICTED)):
            with self.assertLogs("capture", level="ERROR") as console:
                self.policy.deliver(self.request, self.event("chat.created"))
        self.assertEqual(console.output, ["ERROR:capture:P-006 notice delivery decision could not be recorded"])
        self.assertFalse(self.rows("events.jsonl"))


class AuditTests(unittest.IsolatedAsyncioTestCase):
    async def test_audit_observes_denial_without_request_or_response_body(self):
        with tempfile.TemporaryDirectory() as directory:
            policy = NoticeEventPolicy(directory, uid())
            responses = []

            async def app(scope, receive, send):
                await send({"type": "http.response.start", "status": 403})
                await send({"type": "http.response.body", "body": RESTRICTED.encode()})

            async def receive():
                self.fail("The audit middleware must not read the request body")

            async def send(message):
                responses.append(message)

            scope = {"type": "http", "method": "POST", "path": NOTICE_PATH}
            await NoticeAuditMiddleware(app, policy)(scope, receive, send)
            record = json.loads((Path(directory) / "audit.jsonl").read_text())
            self.assertEqual(record["status"], 403)
            self.assertEqual(record["actor_alias"], "unapproved")
            self.assertEqual(record["attempt_id"], scope["state"]["p006_attempt_id"])
            self.assertNotIn(RESTRICTED, json.dumps(record))
            self.assertEqual(responses[1]["body"], RESTRICTED.encode())

    async def test_unrelated_request_does_not_get_a_notice_record(self):
        with tempfile.TemporaryDirectory() as directory:
            policy = NoticeEventPolicy(directory, uid())
            seen = []

            async def app(scope, receive, send):
                seen.append(scope["path"])

            await NoticeAuditMiddleware(app, policy)({"type": "http", "method": "POST", "path": "/api/chat/completions"}, None, None)
            self.assertEqual(seen, ["/api/chat/completions"])
            self.assertEqual(list(Path(directory).iterdir()), [])

    async def test_unhandled_request_error_is_audited_and_propagates(self):
        with tempfile.TemporaryDirectory() as directory:
            policy = NoticeEventPolicy(directory, uid())

            async def fail(scope, receive, send):
                raise RuntimeError(RESTRICTED)

            with self.assertRaises(RuntimeError):
                await NoticeAuditMiddleware(fail, policy)({"type": "http", "method": "POST", "path": NOTICE_PATH}, None, None)
            record = json.loads((Path(directory) / "audit.jsonl").read_text())
            self.assertEqual(record["status"], 500)
            self.assertNotIn(RESTRICTED, json.dumps(record))

"""Metadata policy for the explicitly admitted, isolated notice operation."""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID, uuid4


NOTICE_PATH = "/api/p006/notice/chat"
POLICY_VERSION = "employee-v2"
TTL_SECONDS = 12
NOTICE_ACTIONS = {
    "chat.created": "create_chat",
    "message.created": "save_message",
    "chat.finished": "complete_chat",
}
FAILURE_ACTIONS = {
    "chat.failed": "record_chat_failure",
    "model.provider_request.failed": "record_provider_failure",
}
ACTIONS = NOTICE_ACTIONS | FAILURE_ACTIONS | {
    "event.delivery": "decide_delivery",
    "audit.http": "record_http",
    "retention.chat": "delete_expired",
}
log = logging.getLogger(__name__)


def canonical_uuid(value):
    if not isinstance(value, str):
        return False
    try:
        return str(UUID(value)) == value
    except ValueError:
        return False


@dataclass
class NoticeContext:
    actor_id: str
    attempt_id: str
    chat_id: str | None = None
    sequence: int = 0
    seen: set[str] = field(default_factory=set)


class NoticeEventPolicy:
    def __init__(self, state_dir, run_id):
        if not canonical_uuid(run_id):
            raise ValueError("Expected a canonical lab run UUID")
        self.state_dir = Path(state_dir)
        self.run_id = run_id
        self.pending = set()

    def admit(self, request, actor_id):
        if not canonical_uuid(actor_id):
            raise ValueError("Expected a verified account UUID")
        attempt_id = request.state.p006_attempt_id
        if not canonical_uuid(attempt_id):
            raise ValueError("Expected a server-created attempt UUID")
        context = NoticeContext(actor_id, attempt_id)
        request.state.p006_notice_context = context
        return context

    def is_scoped(self, request):
        return isinstance(getattr(request.state, "p006_notice_context", None), NoticeContext)

    def _write(self, journal, record):
        with (self.state_dir / journal).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, separators=(",", ":")) + "\n")

    def _record(self, context, kind, outcome, reason, *, attempt_id=None):
        return {
            "run_id": self.run_id,
            "attempt_id": context.attempt_id if context else attempt_id,
            "actor_alias": "analyst-fixture" if context else "unapproved",
            "event_type": kind,
            "action": ACTIONS[kind],
            "resource_alias": "LAB-NOTICE-01",
            "outcome": outcome,
            "reason": reason,
            "policy_version": POLICY_VERSION,
        }

    def _event_record(self, context, kind, outcome, reason):
        context.sequence += 1
        return {**self._record(context, kind, outcome, reason), "sequence": context.sequence}

    def _decision(self, context, outcome, reason):
        try:
            self._write("decisions.jsonl", self._event_record(context, "event.delivery", outcome, reason))
        except Exception:
            log.error("P-006 notice delivery decision could not be recorded")

    def reject_invalid(self, request):
        self._decision(request.state.p006_notice_context, "denied", "malformed_envelope")

    def _check_binding(self, context, event):
        if not isinstance(event.actor, dict) or event.actor.get("id") != context.actor_id:
            return "actor_mismatch"
        if not isinstance(event.subject, dict) or not isinstance(event.data, dict):
            return "malformed_envelope"

        subject_id = event.subject.get("id")
        subject_type = event.subject.get("type")
        if event.event == "model.provider_request.failed":
            return None if subject_type == "model" else "malformed_envelope"
        if not canonical_uuid(subject_id):
            return "malformed_envelope"
        if event.event == "chat.created":
            if subject_type != "chat" or context.chat_id not in (None, subject_id):
                return "resource_mismatch"
            context.chat_id = subject_id
        elif event.event == "message.created":
            if subject_type != "message" or not context.chat_id or event.data.get("chat_id") != context.chat_id:
                return "resource_mismatch"
        elif subject_type != "chat" or subject_id != context.chat_id or event.data.get("chat_id") != subject_id:
            return "resource_mismatch"
        return None

    def deliver(self, request, event):
        context = request.state.p006_notice_context
        kind = event.event
        if not isinstance(kind, str) or (kind not in NOTICE_ACTIONS and kind not in FAILURE_ACTIONS):
            self._decision(context, "denied", "unsupported_type")
            return
        if not canonical_uuid(event.id):
            self.reject_invalid(request)
            return
        rejection = self._check_binding(context, event)
        if rejection:
            self._decision(context, "denied", rejection)
            return
        if event.id in context.seen:
            self._decision(context, "duplicate", "duplicate_id")
            return

        outcome = "observed_failure" if kind in FAILURE_ACTIONS else "allowed"
        record = self._event_record(context, kind, outcome, "projected")
        try:
            self._write("events.jsonl", record)
        except Exception:
            # The failed event never falls back to any native sink.
            self._decision(context, "failed", "sink_failure")
        else:
            context.seen.add(event.id)

    def audit_http(self, context, attempt_id, status):
        if status >= 500:
            outcome = "failed"
        else:
            outcome = "allowed" if status < 400 else "denied"
        record = self._record(context, "audit.http", outcome, "http_status", attempt_id=attempt_id)
        try:
            self._write("audit.jsonl", {**record, "status": status})
        except Exception:
            log.error("P-006 notice HTTP decision could not be recorded")

    def schedule_expiry(self, context):
        if context.chat_id is None:
            return
        task = asyncio.create_task(self._expire(context))
        self.pending.add(task)
        task.add_done_callback(self.pending.discard)

    async def _expire(self, context):
        from open_webui.models.chats import Chats

        await asyncio.sleep(TTL_SECONDS)
        try:
            owned = await Chats.get_chat_by_id_and_user_id(context.chat_id, context.actor_id)
            deleted = owned is not None and await Chats.delete_chat_by_id_and_user_id(context.chat_id, context.actor_id)
            outcome = "allowed" if deleted else "denied"
            record = self._event_record(context, "retention.chat", outcome, "owner_checked")
            self._write("events.jsonl", record)
        except Exception:
            self._decision(context, "failed", "retention_failure")


class NoticeAuditMiddleware:
    def __init__(self, app, policy):
        self.app = app
        self.policy = policy

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] != "POST" or scope["path"] != NOTICE_PATH:
            await self.app(scope, receive, send)
            return

        state = scope.setdefault("state", {})
        attempt_id = state["p006_attempt_id"] = str(uuid4())
        status = 500
        recorded = False

        async def audit_response(message):
            nonlocal status, recorded
            if message["type"] == "http.response.start":
                status = message["status"]
                self.policy.audit_http(state.get("p006_notice_context"), attempt_id, status)
                recorded = True
            await send(message)

        try:
            await self.app(scope, receive, audit_response)
        finally:
            if not recorded:
                self.policy.audit_http(state.get("p006_notice_context"), attempt_id, status)

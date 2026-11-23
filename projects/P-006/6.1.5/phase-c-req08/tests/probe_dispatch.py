"""Compare native and historical dispatch in the pinned isolated runtime."""

import asyncio
import json
import os
import sys
from pathlib import Path
from secrets import token_urlsafe
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from starlette.requests import Request


def request_for(path, app):
    return Request({
        "type": "http", "method": "POST", "path": path,
        "headers": [], "scheme": "http", "app": app,
    })


async def probe_scoped(events, app, bound_actor, arrivals):
    from capture import NOTICE_PATH, NoticeEventPolicy
    from open_webui.utils import inbox, middleware

    restricted = "fictional restricted notice sentinel"
    state_dir = Path("/p006-state")
    policy = NoticeEventPolicy(state_dir, os.environ["P006_RUN_ID"])
    app.state.p006_notice_event_policy = policy
    request = request_for(NOTICE_PATH, app)
    request.state.p006_attempt_id = str(uuid4())
    policy.admit(request, bound_actor.id)
    chat_id = str(uuid4())
    await events.publish_event(request, events.EVENTS.CHAT_CREATED, actor=bound_actor, subject_id=chat_id)
    message = events.build_event(
        request, events.EVENTS.MESSAGE_CREATED, actor=bound_actor, subject_id=str(uuid4()),
        data={"chat_id": chat_id, "content_preview": restricted},
    )
    await events.publish_event(request, message)
    await events.publish_event(request, message)
    await events.publish_event(request, restricted, actor=bound_actor)
    await events.publish_event(request, message.model_copy(update={"event": events.EVENTS.COMMENT_CREATED.name}))
    await events.publish_event(request, message.model_copy(update={"id": restricted}))

    real_write = policy._write

    def fail_consumer(journal, record):
        if journal == "events.jsonl":
            raise OSError(restricted)
        real_write(journal, record)

    with patch.object(policy, "_write", side_effect=fail_consumer):
        await events.publish_event(request, message.model_copy(update={"id": str(uuid4())}))
    await events.publish_model_provider_request_failed(
        request, actor=bound_actor, provider="local-fixture", base_url="http://127.0.0.1",
        status=503, requested_model="fictional-model", upstream_error=restricted,
    )
    await middleware.publish_chat_failed_event(
        request, bound_actor, {"chat_id": chat_id, "message_id": str(uuid4())}, restricted,
    )
    assert arrivals == ["chat.created", "user.role_updated", "message.created"]
    with (
        patch.object(inbox, "consume_event", new_callable=AsyncMock, return_value=set()) as inbox_consumer,
        patch.object(middleware, "get_event_emitter", new_callable=AsyncMock, return_value=None),
    ):
        args = (bound_actor, {"chat_id": chat_id, "message_id": str(uuid4())}, "Notice", restricted)
        await middleware.publish_chat_finished_event(request, *args)
        inbox_consumer.assert_not_awaited()
        ordinary = request_for("/api/chat/completions", app)
        args = (bound_actor, {"chat_id": str(uuid4()), "message_id": str(uuid4())}, "Ordinary", "Ordinary response")
        await middleware.publish_chat_finished_event(ordinary, *args)
        assert inbox_consumer.await_count == 1
    assert arrivals == ["chat.created", "user.role_updated", "message.created", "chat.finished"]

    delivered = (state_dir / "events.jsonl").read_text()
    rejected = (state_dir / "decisions.jsonl").read_text()
    assert restricted not in delivered + rejected
    kinds = [json.loads(line)["event_type"] for line in delivered.splitlines()]
    assert kinds == ["chat.created", "message.created", "model.provider_request.failed", "chat.failed", "chat.finished"]
    decisions = [json.loads(line)["reason"] for line in rejected.splitlines()]
    assert decisions == ["duplicate_id", "malformed_envelope", "unsupported_type", "malformed_envelope", "sink_failure"]
    print(json.dumps({
        "mode": "fixed", "scoped_deliveries": kinds, "delivery_decisions": decisions,
        "native_arrivals": arrivals, "ordinary_inbox_calls": 1, "scoped_inbox_calls": 0,
        "scoped_native_arrivals": 0, "prohibited_content_count": 0,
    }, sort_keys=True))


async def probe(mode):
    from open_webui import events
    from open_webui.socket import main as sockets
    from open_webui.utils import inbox

    native_inbox = inbox.consume_event
    if mode == "legacy":
        sys.path.insert(0, "/p006-legacy")
        from capture import install_events

        install_events()

    arrivals = []

    class Observer:
        async def handle_event(self, request, event):
            arrivals.append(event.event)

    events.EVENT_SINKS.append(Observer())
    if mode == "fixed":
        class FailedNativeSink:
            async def handle_event(self, request, event):
                if event.event == "chat.created":
                    raise OSError("synthetic native test sink unavailable")

        events.EVENT_SINKS.insert(-1, FailedNativeSink())
    app = SimpleNamespace(state=SimpleNamespace())
    request = request_for("/api/chat/completions", app)
    bound_actor = SimpleNamespace(id=str(uuid4()), email="analyst@p006.example.com", role="user")
    changed_user = str(uuid4())
    with patch.object(sockets, "disconnect_user_sessions", new_callable=AsyncMock) as disconnect:
        await events.publish_event(request, events.EVENTS.CHAT_CREATED, subject_id=str(uuid4()))
        await events.publish_event(request, events.EVENTS.USER_ROLE_UPDATED, subject_id=changed_user, data={"role": "pending"})
        await events.publish_event(request, events.EVENTS.MESSAGE_CREATED, actor=bound_actor, subject_id=str(uuid4()))
        await asyncio.sleep(0.1)
    scoped_records = Path("/p006-state/events.jsonl")
    scoped_arrivals = [json.loads(line)["event_type"] for line in scoped_records.read_text().splitlines()] if scoped_records.exists() else []
    print(json.dumps({
        "mode": mode,
        "native_sink_arrivals": arrivals,
        "role_disconnect_calls": disconnect.await_count,
        "native_inbox_retained": inbox.consume_event is native_inbox,
        "legacy_notice_arrivals": scoped_arrivals,
    }, sort_keys=True))
    if mode in {"native", "fixed"}:
        assert arrivals == ["chat.created", "user.role_updated", "message.created"]
        disconnect.assert_awaited_once_with(changed_user)
        assert inbox.consume_event is native_inbox and not scoped_arrivals
        if mode == "fixed":
            await probe_scoped(events, app, bound_actor, arrivals)
    else:
        assert not arrivals and disconnect.await_count == 0
        assert inbox.consume_event is not native_inbox and scoped_arrivals == ["message.created"]


if __name__ == "__main__":
    mode, = sys.argv[1:]
    if mode not in {"native", "legacy", "fixed"}:
        raise SystemExit("Use native, legacy or fixed")
    os.umask(0o077)
    Path(os.environ["DATA_DIR"]).mkdir(mode=0o700, parents=True, exist_ok=True)
    if not os.environ.get("WEBUI_SECRET_KEY"):
        os.environ["WEBUI_SECRET_KEY"] = token_urlsafe(32)
    asyncio.run(probe(mode))

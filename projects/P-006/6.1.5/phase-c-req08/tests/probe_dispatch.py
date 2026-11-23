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
    request = Request({
        "type": "http", "method": "POST", "path": "/api/chat/completions",
        "headers": [], "scheme": "http", "app": SimpleNamespace(state=SimpleNamespace()),
    })
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
    if mode == "native":
        assert arrivals == ["chat.created", "user.role_updated", "message.created"]
        disconnect.assert_awaited_once_with(changed_user)
        assert inbox.consume_event is native_inbox and not scoped_arrivals
    else:
        assert not arrivals and disconnect.await_count == 0
        assert inbox.consume_event is not native_inbox and scoped_arrivals == ["message.created"]


if __name__ == "__main__":
    mode, = sys.argv[1:]
    if mode not in {"native", "legacy"}:
        raise SystemExit("Use native or legacy")
    os.umask(0o077)
    Path(os.environ["DATA_DIR"]).mkdir(mode=0o700, parents=True, exist_ok=True)
    os.environ.setdefault("WEBUI_SECRET_KEY", token_urlsafe(32))
    asyncio.run(probe(mode))

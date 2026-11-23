"""Scoped event projection and short private-chat lifetime for the Phase C lab."""

import asyncio
import json
import os
from pathlib import Path
from uuid import UUID


STATE = Path("/p006-state")
RUN_ID = str(UUID(os.environ["P006_RUN_ID"]))
MODE = os.environ["P006_DATA_MODE"]
if MODE not in {"baseline", "controlled"}:
    raise ValueError("Invalid data-handling mode")

ACTOR = "analyst@p006.example.com"
CHAT_PATH = "/api/chat/completions"
TTL_SECONDS = 12
ACTIONS = {
    "message.created": "save_message",
    "chat.finished": "complete_chat",
    "audit.http": "record_http",
    "retention.chat": "delete_expired",
}
EVENT_TYPES = {"message.created", "chat.finished"}
pending = set()


def metadata(kind, outcome="allowed"):
    if outcome not in {"allowed", "denied"}:
        raise ValueError("Invalid outcome")
    return {
        "run_id": RUN_ID,
        "event_type": kind,
        "actor_alias": "analyst-fixture",
        "action": ACTIONS[kind],
        "resource_alias": "LAB-NOTICE-01",
        "outcome": outcome,
        "policy_version": "employee-v1",
    }


def write(filename, record):
    with (STATE / filename).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()


async def expire(chat_id, owner_id):
    from open_webui.models.chats import Chats

    await asyncio.sleep(TTL_SECONDS)
    owned = await Chats.get_chat_by_id_and_user_id(chat_id, owner_id)
    deleted = owned is not None and await Chats.delete_chat_by_id_and_user_id(chat_id, owner_id)
    write("events.jsonl", metadata("retention.chat", "allowed" if deleted else "denied"))


async def disable_inbox(_event, **_options):
    return set()


def install_events():
    # The application's native producer and publish_event stay in the request path.
    from open_webui import events

    native_build = events.build_event

    def build(request, event, **kwargs):
        native = native_build(request, event, **kwargs)
        actor = kwargs.get("actor")
        if request is None or request.url.path != CHAT_PATH:
            return native
        if native.event not in EVENT_TYPES or getattr(actor, "email", None) != ACTOR:
            return native
        request.state.p006_notice = True
        if MODE == "baseline":
            return native
        if native.event == "chat.finished":
            # Retention receives the authorized native IDs in-process only.
            chat_id = str(UUID(native.data["chat_id"]))
            owner_id = str(UUID(actor.id))
            task = asyncio.create_task(expire(chat_id, owner_id))
            pending.add(task)
            task.add_done_callback(pending.discard)
        return native.model_copy(update={
            "actor": None, "subject": None, "message": None, "data": metadata(native.event)
        })

    async def scoped_dispatch(request, event):
        if request.url.path != CHAT_PATH or event.event not in EVENT_TYPES:
            return
        if not getattr(request.state, "p006_notice", False):
            return
        if MODE == "baseline":
            write("events.jsonl", event.model_dump())
        else:
            projected = metadata(event.event)
            if event.data == projected:
                write("events.jsonl", projected)

    events.build_event = build
    events._dispatch_event = scoped_dispatch
    if MODE == "controlled":
        # The native completion handler calls this sink before publish_event.
        from open_webui.utils import inbox
        inbox.consume_event = disable_inbox


def install_audit(app):
    if MODE == "baseline":
        return

    @app.middleware("http")
    async def capture_decision(request, call_next):
        response = await call_next(request)
        if (request.method == "POST" and request.url.path == CHAT_PATH
                and getattr(request.state, "p006_notice", False)):
            outcome = "allowed" if response.status_code < 400 else "denied"
            write("audit.jsonl", metadata("audit.http", outcome))
        return response

"""Run a fixed, explicitly admitted notice fixture through the pinned native app."""

import hashlib
import json
import os
from pathlib import Path
from secrets import token_urlsafe
from time import time
from uuid import uuid4

os.umask(0o077)
Path(os.environ["DATA_DIR"]).mkdir(mode=0o700, parents=True, exist_ok=True)
if not os.environ.get("WEBUI_SECRET_KEY"):
    os.environ["WEBUI_SECRET_KEY"] = token_urlsafe(32)

import uvicorn
from fastapi import Depends, HTTPException, Request

from capture import NOTICE_PATH, NoticeAuditMiddleware, NoticeEventPolicy, canonical_uuid
from open_webui.events import notice_event_policy
from open_webui.main import chat_completion
from open_webui.utils.auth import get_verified_user
from serve import app


STATE = Path("/p006-state")
MODEL = "p006-smollm2-360m-instruct-q4-k-m"
FIXTURE_SHA = "c0bf8f9973acc8984bf39f143f923e91af6cf676bf1c0e4bdd7d56f585f32581"
if os.environ["AUDIT_LOG_LEVEL"] != "METADATA" or os.environ["AUDIT_EXCLUDED_PATHS"] != "p006/notice/chat$":
    raise ValueError("The retest requires native metadata audit and the exact notice-route exclusion")
fixture_bytes = Path("/p006-fixture.json").read_bytes()
if hashlib.sha256(fixture_bytes).hexdigest() != FIXTURE_SHA:
    raise ValueError("Expected the approved synthetic fixture")
fixture = json.loads(fixture_bytes)
notice = fixture["notice"]
content = "\n\n".join((notice["note_block"], notice["policy_line"], fixture["T02"]["request"]))
policy = NoticeEventPolicy(STATE, os.environ["P006_RUN_ID"])
app.state.p006_notice_event_policy = policy
app.add_middleware(NoticeAuditMiddleware, policy=policy)


def fixture_form():
    user_message_id, assistant_id = str(uuid4()), str(uuid4())
    return {
        "model": MODEL, "stream": False, "temperature": 0, "top_k": 1, "seed": 611,
        "max_tokens": 384, "cache_prompt": False, "parent_id": None, "id": assistant_id,
        "messages": [{"role": "user", "content": content}],
        "user_message": {
            "id": user_message_id, "role": "user", "content": content, "parentId": None,
            "childrenIds": [assistant_id], "timestamp": int(time()),
        },
    }


async def draft_notice(request: Request, body: dict, user=Depends(get_verified_user)):
    if body or request.url.query:
        raise HTTPException(status_code=400, detail="Only the approved fixture is accepted")
    try:
        allowed_actor = (STATE / "approved-analyst").read_text().strip()
    except OSError:
        raise HTTPException(status_code=503, detail="Notice scope is unavailable") from None
    if not canonical_uuid(allowed_actor) or user.role != "user" or user.id != allowed_actor:
        raise HTTPException(status_code=403, detail="Caller is outside the notice scope")

    context = policy.admit(request, user.id)
    assert notice_event_policy(request) is policy
    try:
        return await chat_completion(request, fixture_form(), user=user)
    finally:
        policy.schedule_expiry(context)


# The native frontend fallback must remain after the lab-only routes.
fallback = next(route for route in app.router.routes if route.name == "spa-static-files")
app.router.routes.remove(fallback)
app.add_api_route(NOTICE_PATH, draft_notice, methods=["POST"], include_in_schema=False)
app.router.routes.append(fallback)

if os.environ.get("P006_OBSERVE_NATIVE") == "1":
    from native_observer import add_local_observer

    add_local_observer(STATE)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000, access_log=False)

"""Authorized, isolated Phase B checks over the native WebUI loopback API."""

import hashlib
from http.client import HTTPConnection
import json
import os
import sqlite3
import sys
import time
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from secrets import token_urlsafe
from uuid import uuid4


SOURCE = "0666e59d26a4d056e0bacee41742486badd71cf8"
FIXTURE_SHA = "c0bf8f9973acc8984bf39f143f923e91af6cf676bf1c0e4bdd7d56f585f32581"
MODEL = "p006-smollm2-360m-instruct-q4-k-m"
RUN = str(uuid4())
APP_DB = "/p006-state/open-webui/webui.db"
NOTICE_DB = "/p006-state/preview.db"
ROOT = "/api/p006/notices"
TOKENS = {}


def emit(kind, **data):
    print(json.dumps({
        "run_id": RUN, "event": kind, "at": datetime.now(UTC).isoformat(), **data
    }, ensure_ascii=False), flush=True)


def safe(data):
    if isinstance(data, dict):
        keys = {"password", "token", "access_token", "refresh_token", "authorization", "cookie", "value"}
        return {key: ("[redacted]" if key.lower() in keys else safe(value)) for key, value in data.items()}
    if isinstance(data, list):
        return [safe(item) for item in data]
    return data


def http(path, *, actor=None, body=None, status=200):
    headers = {"Content-Type": "application/json"}
    if actor:
        headers["Authorization"] = f"Bearer {TOKENS[actor]}"
    method = "POST" if body is not None else "GET"
    started = datetime.now(UTC).isoformat()
    with closing(HTTPConnection("127.0.0.1", 3000, timeout=90)) as connection:
        connection.request(method, path, json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None, headers)
        response = connection.getresponse()
        raw = response.read()
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        payload = {"body_bytes": len(raw)}
    emit("http", method=method, path=path, actor=actor, request=safe(body), status=response.status,
         response=safe(payload), started=started)
    if response.status != status:
        raise AssertionError(f"{method} {path} returned {response.status}. Expected {status}.")
    return payload


def query(database, sql, parameters=()):
    with closing(sqlite3.connect(f"file:{database}?mode=ro", uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(sql, parameters)]


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def register():
    for name in ("bootstrap", "analyst", "reviewer", "other"):
        address = f"{name}@p006.example.com"
        credentials = {"email": address, "password": f"P006!a9-{token_urlsafe(16)}"}
        if name == "bootstrap":
            http("/api/v1/auths/signup", body={**credentials, "name": name})
        else:
            http("/api/v1/auths/add", actor="bootstrap", body={**credentials, "name": name, "role": "user"})
        session = http("/api/v1/auths/signin", body=credentials)
        TOKENS[name] = session["token"]
        expected = "admin" if name == "bootstrap" else "user"
        observed = query(APP_DB, "SELECT id,email,role FROM user WHERE email=?", (address,))
        assert len(observed) == 1 and observed[0]["role"] == expected
        assert observed[0]["id"] == session["id"] and session["role"] == expected
        emit("identity", alias=name, account=observed[0])
    return {row["email"].split("@")[0]: row["id"]
            for row in query(APP_DB, "SELECT id,email FROM user")}


def native_state():
    tables = {row["name"] for row in query(APP_DB, "SELECT name FROM sqlite_master WHERE type='table'")}
    names = ("shared_chat", "tool", "tool_history", "automation", "automation_run", "notification")
    return {name: query(APP_DB, f'SELECT count(*) AS count FROM "{name}"')[0]["count"]
            if name in tables else None for name in names}


def check_private_chat(chat_id, owner, assistant_id):
    row, = query(APP_DB, "SELECT id,user_id,share_id,chat FROM chat WHERE id=?", (chat_id,))
    assert row["user_id"] == owner and row["share_id"] is None
    message = json.loads(row["chat"])["history"]["messages"][assistant_id]
    assert message["role"] == "assistant" and message["done"] is True
    text = message.get("content") or "".join(
        part["text"] for group in message.get("output", []) if group.get("type") == "message"
        for part in group.get("content", []) if "text" in part
    )
    assert isinstance(text, str) and text
    emit("native_chat", chat_id=chat_id, owner_id=owner, candidate_id=assistant_id,
         candidate_sha256=digest(text), share_id=row["share_id"])
    return text


def fixture_chat(candidate, label, owner):
    message_id = str(uuid4())
    new = http("/api/v1/chats/new", actor="analyst", body={"chat": {
        "title": f"Synthetic {label}", "models": [MODEL],
        "history": {"currentId": message_id, "messages": {message_id: {
            "id": message_id, "role": "assistant", "content": candidate,
            "done": True, "model": MODEL, "parentId": None, "childrenIds": [],
            "timestamp": int(time.time()),
        }}},
    }})
    assert check_private_chat(new["id"], owner, message_id) == candidate
    return {"chat_id": new["id"], "message_id": message_id}


def create_notice(source, identities):
    created = http(ROOT, actor="analyst", body=source, status=201)
    row, = query(NOTICE_DB, "SELECT * FROM notice WHERE id=?", (created["id"],))
    assert row["owner_id"] == identities["analyst"] and row["reviewer_id"] == identities["reviewer"]
    assert row["revision"] == created["revision"] == 2 and row["policy"] == "employee-v1"
    assert row["chat_id"] == source["chat_id"] and row["message_id"] == source["message_id"]
    return created["id"]


def fields(revision, approved_fields):
    return {"expected_revision": revision, "audience": "all employees", "approved_fields": approved_fields}


def confirm(notice, *, audience="all employees", revision=2):
    http(f"{ROOT}/{notice}/confirm", actor="analyst",
         body={"expected_revision": revision, "audience": audience})


def approve(notice, approved, *, revision=2, status=200):
    http(f"{ROOT}/{notice}/approve", actor="reviewer", body=fields(revision, approved), status=status)


def preview(label, notice, expected, *, revision=2):
    result = http(f"{ROOT}/{notice}/preview", actor="analyst", body={"expected_revision": revision})
    row, = query(NOTICE_DB, "SELECT * FROM notice WHERE id=?", (notice,))
    emit("preview_observation", case=label, observed=result, separate_sqlite_row=row)
    assert result["preview"] == row["preview"] == expected
    assert bool(row["ready"]) == (expected is not None)
    assert result["status"] == ("READY" if expected is not None else "HELD")
    assert row["revision"] == revision
    return row


def real_model(fixtures, identities):
    note = fixtures["notice"]
    content = "\n\n".join((note["policy_line"], note["note_block"], fixtures["T02"]["request"]))
    msg_id, assistant_id = str(uuid4()), str(uuid4())
    result = http("/api/chat/completions", actor="analyst", body={
        "model": MODEL, "stream": False, "temperature": 0, "top_k": 1, "seed": 611,
        "max_tokens": 384, "cache_prompt": False,
        "messages": [{"role": "user", "content": content}], "parent_id": None, "id": assistant_id,
        "user_message": {"id": msg_id, "role": "user", "content": content, "parentId": None,
                         "childrenIds": [assistant_id], "timestamp": int(time.time())},
    })
    candidate = result["choices"][0]["message"]["content"]
    assert result["model"] == MODEL and result["system_fingerprint"] == "b12627-225a5345b"
    own_rows = query(APP_DB, "SELECT id,chat FROM chat WHERE user_id=?", (identities["analyst"],))
    chat, = [row["id"] for row in own_rows if assistant_id in json.loads(row["chat"])["history"]["messages"]]
    assert check_private_chat(chat, identities["analyst"], assistant_id) == candidate
    emit("provider_association", model=MODEL, completion_id=result["id"],
         engine=result["system_fingerprint"], candidate_sha256=digest(candidate),
         observed_ticket_marker="labint042" in "".join(c for c in candidate.casefold() if c.isalnum()))
    return {"chat_id": chat, "message_id": assistant_id}, candidate


def main():
    raw = sys.stdin.buffer.read()
    assert hashlib.sha256(raw).hexdigest() == FIXTURE_SHA
    fixtures = json.loads(raw)
    assert os.environ["WEBUI_BUILD_HASH"] == SOURCE
    code = {relative: hashlib.sha256(Path("/app/backend/open_webui", relative).read_bytes()).hexdigest()
            for relative in ("main.py", "utils/auth.py", "models/chats.py", "routers/openai.py")}
    version = http("/api/version")
    assert version["version"] == "0.13.4"
    emit("native_runtime", image_commit=os.environ["WEBUI_BUILD_HASH"], installed_sha256=code,
         config={key: os.environ[key] for key in
                 ("OFFLINE_MODE", "ENABLE_OLLAMA_API", "ENABLE_AUTOMATIONS", "OPENAI_API_BASE_URLS",
                  "USER_PERMISSIONS_CHAT_SHARE", "ENABLE_WEB_SEARCH", "AUDIT_LOG_LEVEL")},
         fixture_sha256=FIXTURE_SHA)
    identities = register()
    base = http("/api/models/base", actor="bootstrap")
    assert [model["id"] for model in base["data"]] == [MODEL]
    http("/api/v1/models/create", actor="bootstrap", body={
        "id": MODEL, "name": "P-006 synthetic model", "meta": {}, "params": {},
        "access_grants": [{"principal_type": "user", "principal_id": identities["analyst"], "permission": "read"}],
    })
    grant, = query(APP_DB, "SELECT principal_id,permission FROM access_grant WHERE resource_type='model' AND resource_id=?", (MODEL,))
    assert grant == {"principal_id": identities["analyst"], "permission": "read"}
    emit("model_grant", model=MODEL, separate_sqlite_row=grant)
    models = http("/api/models", actor="analyst")
    assert [model["id"] for model in models["data"]] == [MODEL]
    before = native_state()
    emit("native_effects_before", store_counts=before)
    source, actual_candidate = real_model(fixtures, identities)

    t03 = fixtures["T03"]
    approved = t03["approved_fields"]
    expected_ready = t03["variants"][0]["expected"]["preview"]
    notice = create_notice(source, identities)
    preview("native-real-model-before-approval", notice, None)
    confirm(notice)
    approve(notice, approved)
    row = preview("native-real-model", notice, expected_ready)
    assert row["candidate_sha256"] == digest(actual_candidate)

    for label in ("A", "B", "C", "D", "E", "F"):
        candidate = t03["candidates"]["clean" if label == "B" else "wrong"]
        source = fixture_chat(candidate, label, identities["analyst"])
        notice = create_notice(source, identities)
        if label != "C":
            confirm(notice, audience="service desk" if label == "F" else "all employees")
        if label == "D":
            approve(notice, approved, revision=1, status=409)
        elif label == "E":
            without_action = {k: v for k, v in approved.items() if k != "employee_action"}
            approve(notice, without_action, status=422)
        else:
            approve(notice, approved)
        row = preview(f"T03-{label}", notice, expected_ready if label in ("A", "B") else None)
        assert row["candidate_sha256"] == digest(candidate)
        if label in ("D", "E"):
            assert row["approved_fields"] is None and row["approved_revision"] is None
        if label == "A":
            assert "15:00" not in row["preview"] and "LAB-INT-042" not in row["preview"]
            http(f"{ROOT}/{notice}/preview", actor="other", body={"expected_revision": 2}, status=404)
            http(f"{ROOT}/{notice}/approve", actor="analyst", body=fields(2, approved), status=403)
            http(f"{ROOT}/{notice}/approve", actor="other", body=fields(2, approved), status=403)
            http(f"{ROOT}/{notice}/preview", body={"expected_revision": 2}, status=401)
            http(f"{ROOT}/{notice}/publish", actor="analyst", body={}, status=405)
            http(f"/api/v1/chats/{source['chat_id']}/share", actor="analyst", body={}, status=401)
            snapshot, = query(NOTICE_DB, "SELECT * FROM notice WHERE id=?", (notice,))
            assert snapshot == row
            http(f"{ROOT}/{notice}/revise", actor="analyst", body={"expected_revision": 2})
            http(f"{ROOT}/{notice}/preview", actor="analyst", body={"expected_revision": 2}, status=409)
            revised = preview("revision-invalidates-ready", notice, None, revision=3)
            assert revised["audience"] is None and revised["approved_fields"] is None

    after = native_state()
    emit("native_effects_after", store_counts=after)
    assert before == after
    assert after["shared_chat"] == 0 and after["tool_history"] == 0 and after["automation_run"] == 0
    emit("suite", status="PASS", planned_t03_cases=6, native_model_requests=1)


if __name__ == "__main__":
    main()

"""Inspect the scoped runtime from a separate HTTP and read-only SQLite process."""

import hashlib
import json
import os
import re
import stat
import sys
import time
from collections import Counter
from pathlib import Path
from uuid import uuid4

import check_http as native


native.RUN = os.environ["P006_RUN_ID"]
emit = native.emit
STATE = Path("/p006-state")
NOTICE_PATH = "/api/p006/notice/chat"
MARKERS = ("LAB-INT-042", "Maple Calendar", "content_preview")
EVENT_ACTIONS = {
    "chat.created": "create_chat",
    "message.created": "save_message",
    "chat.finished": "complete_chat",
    "retention.chat": "delete_expired",
}
FIELDS = {
    "run_id", "attempt_id", "actor_alias", "event_type", "action",
    "resource_alias", "outcome", "reason", "policy_version",
}
UUID_PATTERN = re.compile(r"[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}")


def emit_sanitized(kind, **payload):
    if kind == "http":
        emit(kind, path=UUID_PATTERN.sub("<id>", payload["path"]), method=payload["method"],
             actor=payload["actor"], status=payload["status"])
    elif kind == "identity":
        emit(kind, alias=payload["alias"], role=payload["account"]["role"],
             account_sha256=native.digest(payload["account"]["id"]))
    elif kind == "native_chat":
        emit(kind, chat_sha256=native.digest(payload["chat_id"]),
             candidate_sha256=payload["candidate_sha256"])


native.emit = emit_sanitized


def rows(filename):
    path = STATE / filename
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def store_counts(chat_id):
    return {
        table: native.query(native.APP_DB, f"SELECT count(*) AS n FROM {table} WHERE {column}=?", (chat_id,))[0]["n"]
        for table, column in (("chat", "id"), ("chat_message", "chat_id"))
    }


def role_update(identities):
    subject = identities["reviewer"]
    before, = native.query(native.APP_DB, "SELECT role FROM user WHERE id=?", (subject,))
    native.http(f"/api/v1/users/{subject}/update", actor="bootstrap", body={"role": "pending"})
    after, = native.query(native.APP_DB, "SELECT role FROM user WHERE id=?", (subject,))
    assert before["role"] == "user" and after["role"] == "pending"
    record, = [entry for entry in rows("native-observer.jsonl") if entry["event_type"] == "user.role_updated"]
    assert record["actor_sha256"] == native.digest(identities["bootstrap"])
    assert record["subject_sha256"] == native.digest(subject) and not record["contains_notice_content"]
    emit("unrelated_security_effect", record=record, before=before, after=after)


def unrelated_chat(owner):
    user_message_id, assistant_id = str(uuid4()), str(uuid4())
    public_input = "State that this is an ordinary fictional lab chat."
    response = native.http("/api/chat/completions", actor="analyst", body={
        "model": native.MODEL, "stream": False, "temperature": 0, "max_tokens": 64,
        "parent_id": None, "id": assistant_id,
        "messages": [{"role": "user", "content": public_input}],
        "user_message": {
            "id": user_message_id, "role": "user", "content": public_input,
            "parentId": None, "childrenIds": [assistant_id], "timestamp": int(time.time()),
        },
    })
    assert response["model"] == native.MODEL
    row, = native.query(native.APP_DB, "SELECT id FROM chat WHERE user_id=?", (owner,))
    assert native.check_private_chat(row["id"], owner, assistant_id)
    counts = store_counts(row["id"])
    assert counts == {"chat": 1, "chat_message": 2}
    observed = rows("native-observer.jsonl")
    chat_events = [event for event in observed if event["event_type"] != "user.role_updated"]
    assert [event["event_type"] for event in chat_events] == ["chat.created", "message.created", "message.created", "chat.finished"]
    assert all(event["actor_sha256"] == native.digest(owner) and not event["contains_notice_content"] for event in chat_events)
    assert not (STATE / "events.jsonl").exists()
    emit("unrelated_flow", native_events=chat_events, persisted=counts)
    return row["id"]


def verify_event(record, kind, sequence, attempt_id, reason="projected"):
    expected = {
        "run_id": native.RUN, "attempt_id": attempt_id, "actor_alias": "analyst-fixture",
        "event_type": kind, "action": EVENT_ACTIONS[kind], "resource_alias": "LAB-NOTICE-01",
        "outcome": "allowed", "reason": reason, "policy_version": "employee-v2", "sequence": sequence,
    }
    assert record == expected


def check_audit():
    audit = rows("audit.jsonl")
    assert [record["status"] for record in audit] == [401, 403, 400, 200]
    assert all(set(record) == FIELDS | {"status"} for record in audit)
    assert len({record["attempt_id"] for record in audit}) == 4
    for record in audit:
        allowed = record["status"] == 200
        assert record["run_id"] == native.RUN and record["event_type"] == "audit.http"
        assert record["actor_alias"] == ("analyst-fixture" if allowed else "unapproved")
        assert record["outcome"] == ("allowed" if allowed else "denied")
        assert record["policy_version"] == "employee-v2" and record["reason"] == "http_status"
        assert record["action"] == "record_http" and record["resource_alias"] == "LAB-NOTICE-01"
    emit("scope_audit", records=audit)
    native_audit = rows("native-audit.jsonl")
    native_uris = [record.get("request_uri") or "" for record in native_audit]
    assert any(uri.endswith("/api/v1/auths/signin") for uri in native_uris)
    assert any("/api/v1/users/" in uri and uri.endswith("/update") for uri in native_uris)
    assert not any(uri.endswith(NOTICE_PATH) for uri in native_uris)
    assert not any(record.get("request_object") or record.get("response_object") for record in native_audit)
    assert not any(marker in json.dumps(native_audit) for marker in MARKERS)
    emit("native_audit", records=len(native_audit), auth_positive=True, role_positive=True, body_records=0)
    return audit[-1]["attempt_id"]


def notice_chat(raw, identities, control_chat):
    effects_before = native.native_state()
    native_before = rows("native-observer.jsonl")
    native.http(NOTICE_PATH, body={}, status=401)
    native.http(NOTICE_PATH, actor="other", body={}, status=403)
    native.http(NOTICE_PATH, actor="analyst", body={"extra": "outside the approved fixture"}, status=400)
    assert not (STATE / "events.jsonl").exists()
    result = native.http(NOTICE_PATH, actor="analyst", body={})
    assert result["model"] == native.MODEL and result["system_fingerprint"] == "b12627-225a5345b"
    candidate = result["choices"][0]["message"]["content"]

    owner = identities["analyst"]
    chat, = native.query(native.APP_DB, "SELECT id,chat FROM chat WHERE user_id=? AND id != ?", (owner, control_chat))
    chat_id = chat["id"]
    fixture = json.loads(raw)
    notice = fixture["notice"]
    expected = "\n\n".join((notice["note_block"], notice["policy_line"], fixture["T02"]["request"]))
    messages = list(json.loads(chat["chat"])["history"]["messages"].values())
    user_message, = [message for message in messages if message["role"] == "user"]
    assistant, = [message for message in messages if message["role"] == "assistant"]
    assert user_message["content"] == expected and MARKERS[0] in user_message["content"][:300]
    assert native.check_private_chat(chat_id, owner, assistant["id"]) == candidate
    before = store_counts(chat_id)
    assert before == {"chat": 1, "chat_message": 2}
    allowed = native.http(f"/api/v1/chats/{chat_id}", actor="analyst")
    assert MARKERS[0] in json.dumps(allowed)
    native.http(f"/api/v1/chats/{chat_id}", actor="other", status=401)
    emit("allowed_private_path", counts=before, input_sha256=native.digest(expected),
         excluded_marker_present_in_private_input=True, candidate_sha256=native.digest(candidate),
         actual_model=result["model"], engine=result["system_fingerprint"])

    attempt_id = check_audit()
    deliveries = rows("events.jsonl")
    expected_types = ("chat.created", "message.created", "message.created", "chat.finished")
    assert len(deliveries) == len(expected_types)
    for index, (record, kind) in enumerate(zip(deliveries, expected_types), 1):
        verify_event(record, kind, index, attempt_id)
    assert rows("native-observer.jsonl") == native_before
    assert not (STATE / "decisions.jsonl").exists()
    emit("scoped_delivery", records=deliveries, native_positive_records=len(native_before), native_notice_deliveries=0)

    started = time.monotonic()
    while store_counts(chat_id)["chat"] and time.monotonic() - started < 25:
        time.sleep(0.2)
    after = store_counts(chat_id)
    assert after == {"chat": 0, "chat_message": 0}
    expiry_records = rows("events.jsonl")
    assert expiry_records[:4] == deliveries and len(expiry_records) == 5
    verify_event(expiry_records[-1], "retention.chat", 5, attempt_id, reason="owner_checked")
    native.http(f"/api/v1/chats/{chat_id}", actor="analyst", status=401)
    assert store_counts(control_chat) == {"chat": 1, "chat_message": 2}
    effects_after = native.native_state()
    assert effects_before == effects_after and all(count == 0 for count in effects_after.values())
    emit("expiry_and_effects", remaining_rows=after, unrelated_chat_retained=True,
         before=effects_before, after=effects_after, receipt=expiry_records[-1],
         seconds_from_private_read=round(time.monotonic() - started, 3))


def main():
    raw = sys.stdin.buffer.read()
    assert hashlib.sha256(raw).hexdigest() == native.FIXTURE_SHA
    assert os.environ["WEBUI_BUILD_HASH"] == native.SOURCE
    assert native.http("/api/version")["version"] == "0.13.4"
    identities = native.register()
    (STATE / "approved-analyst").write_text(identities["analyst"])
    # The operator writes this binding in the private temporary filesystem.
    (STATE / "approved-analyst").chmod(0o600)
    models = native.http("/api/models/base", actor="bootstrap")
    assert [model["id"] for model in models["data"]] == [native.MODEL]
    native.http("/api/v1/models/create", actor="bootstrap", body={
        "id": native.MODEL, "name": "P-006 synthetic model", "meta": {}, "params": {},
        "access_grants": [{"principal_type": "user", "principal_id": identities["analyst"], "permission": "read"}],
    })
    assert [model["id"] for model in native.http("/api/models", actor="analyst")["data"]] == [native.MODEL]
    role_update(identities)
    control_chat = unrelated_chat(identities["analyst"])
    notice_chat(raw, identities, control_chat)
    emit("suite", status="PASS")


if __name__ == "__main__":
    os.umask(0o077)
    main()

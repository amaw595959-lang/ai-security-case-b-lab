"""Verify the native application data paths from a separate process."""

import hashlib
import json
import os
import stat
import sys
import time
from pathlib import Path
from uuid import uuid4

import check_http as native


native.RUN = os.environ["P006_RUN_ID"]
MODE = os.environ["P006_DATA_MODE"]
STATE = Path("/p006-state")
MARKER = "LAB-INT-042"
FIELDS = {"run_id", "event_type", "actor_alias", "action", "resource_alias", "outcome", "policy_version"}


def rows(filename):
    path = STATE / filename
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def stage_counts(chat_id):
    sql = "SELECT count(*) AS n FROM"
    return {
        "chat": native.query(native.APP_DB, f"{sql} chat WHERE id=?", (chat_id,))[0]["n"],
        "chat_message": native.query(native.APP_DB, f"{sql} chat_message WHERE chat_id=?", (chat_id,))[0]["n"],
    }


def approved(record, kind, action):
    expected = {
        "run_id": native.RUN, "event_type": kind, "actor_alias": "analyst-fixture",
        "action": action, "resource_alias": "LAB-NOTICE-01", "outcome": "allowed",
        "policy_version": "employee-v1",
    }
    assert set(record) == FIELDS and record == expected


def storage(fixtures, identities):
    # Put the T04 note block first so the marker falls inside the native 300-character preview.
    note = fixtures["notice"]
    content = "\n\n".join((note["note_block"], note["policy_line"], fixtures["T02"]["request"]))
    assert MARKER in content[:300]
    user_id, message_id = str(uuid4()), str(uuid4())
    result = native.http("/api/chat/completions", actor="analyst", body={
        "model": native.MODEL, "stream": False, "temperature": 0, "top_k": 1, "seed": 611,
        "max_tokens": 384, "cache_prompt": False, "parent_id": None, "id": message_id,
        "messages": [{"role": "user", "content": content}],
        "user_message": {"id": user_id, "role": "user", "content": content, "parentId": None,
                         "childrenIds": [message_id], "timestamp": int(time.time())},
    })
    assert result["model"] == native.MODEL and result["system_fingerprint"] == "b12627-225a5345b"
    candidate = result["choices"][0]["message"]["content"]
    chat_row, = native.query(native.APP_DB, "SELECT id,chat FROM chat WHERE user_id=?", (identities["analyst"],))
    chat_id = chat_row["id"]
    assert native.check_private_chat(chat_id, identities["analyst"], message_id) == candidate
    assert json.loads(chat_row["chat"])["history"]["messages"][user_id]["content"] == content
    own = native.http(f"/api/v1/chats/{chat_id}", actor="analyst")
    assert MARKER in json.dumps(own)
    native.http(f"/api/v1/chats/{chat_id}", actor="other", status=401)
    initial = stage_counts(chat_id)
    assert initial["chat"] == 1 and initial["chat_message"] >= 2
    native.emit("allowed_private_path", chat_id=chat_id, counts=initial, provider_id=result["id"],
                candidate_sha256=native.digest(candidate), reply_has_marker=MARKER in candidate)
    return chat_id, candidate


def baseline(candidate):
    observed = rows("events.jsonl")
    native.emit("baseline_event_records", app_events=observed)
    raw_audits = rows("native-audit.jsonl")
    chat_audits = [row for row in raw_audits if row.get("request_uri", "").endswith("/api/chat/completions")]
    native.emit("baseline_audit_records", chat_audits=native.safe(chat_audits))
    # The native usage logger may add a separate record for the same endpoint.
    body_audits = [row for row in chat_audits if row.get("request_object") and row.get("response_object")]
    assert body_audits
    assert {row["event"] for row in observed} == {"message.created", "chat.finished"}
    initial, = [row for row in observed if row["event"] == "message.created" and row["data"].get("role") == "user"]
    finished, = [row for row in observed if row["event"] == "chat.finished"]
    assert MARKER in initial["data"]["content_preview"]
    assert finished["data"]["message"] == candidate
    for record in body_audits:
        assert MARKER in json.dumps(record["request_object"])
        response = record["response_object"]
        if isinstance(response, str):
            response = json.loads(response)
        assert response["choices"][0]["message"]["content"] == candidate
    native.emit("baseline_audit_record", chat_audit=native.safe(body_audits[0]))


def controlled(chat_id):
    journal = rows("events.jsonl")
    actions = {"message.created": "save_message", "chat.finished": "complete_chat"}
    native.emit("controlled_event_records", app_events=journal)
    assert {record["event_type"] for record in journal} == set(actions)
    for record in journal:
        kind = record["event_type"]
        action = actions[kind]
        approved(record, kind, action)
    audit, = rows("audit.jsonl")
    approved(audit, "audit.http", "record_http")
    assert not (STATE / "native-audit.jsonl").exists()
    native.emit("approved_metadata_receipts", app_events=journal, audit=audit)

    started = time.monotonic()
    deadline = started + 25
    while time.monotonic() < deadline and stage_counts(chat_id)["chat"]:
        time.sleep(0.2)
    counts = stage_counts(chat_id)
    expiration = rows("events.jsonl")
    assert len(expiration) == len(journal) + 1
    approved(expiration[-1], "retention.chat", "delete_expired")
    assert counts == {"chat": 0, "chat_message": 0}
    native.http(f"/api/v1/chats/{chat_id}", actor="analyst", status=401)
    native.emit("expiration_observation", chat_id=chat_id, remaining_rows=counts,
                operational_receipt=expiration[-1], seconds_from_initial_check=round(time.monotonic() - started, 3))


def main():
    raw = sys.stdin.buffer.read()
    assert hashlib.sha256(raw).hexdigest() == native.FIXTURE_SHA
    assert os.environ["WEBUI_BUILD_HASH"] == native.SOURCE
    assert native.http("/api/version")["version"] == "0.13.4"
    native.emit("policy", phase=MODE, upstream_commit=os.environ["WEBUI_BUILD_HASH"],
                audit_level=os.environ["AUDIT_LOG_LEVEL"], diagnostic_level=os.environ["GLOBAL_LOG_LEVEL"])
    identities = native.register()
    models = native.http("/api/models/base", actor="bootstrap")
    assert [model["id"] for model in models["data"]] == [native.MODEL]
    native.http("/api/v1/models/create", actor="bootstrap", body={
        "id": native.MODEL, "name": "P-006 synthetic model", "meta": {}, "params": {},
        "access_grants": [{"principal_type": "user", "principal_id": identities["analyst"], "permission": "read"}],
    })
    assert [model["id"] for model in native.http("/api/models", actor="analyst")["data"]] == [native.MODEL]
    effects_before = native.native_state()
    chat_id, candidate = storage(json.loads(raw), identities)
    if MODE == "baseline":
        baseline(candidate)
    else:
        controlled(chat_id)
    effects_after = native.native_state()
    assert effects_before == effects_after and all(count == 0 for count in effects_after.values())
    native.emit("destination_and_file_inventory", native_effects_before=effects_before,
                native_effects_after=effects_after, journal_files=sorted(path.name for path in STATE.glob("*.jsonl")),
                rotation_files=[str(path.relative_to(STATE)) for path in STATE.rglob("*.zip")])
    native.emit("suite", phase=MODE, status="PASS")


if __name__ == "__main__":
    main()

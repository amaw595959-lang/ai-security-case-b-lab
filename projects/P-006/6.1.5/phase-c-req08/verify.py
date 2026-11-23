"""Replay the archived Phase C observations without a running app."""

import gzip
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / "evidence"
FIELDS = {"run_id", "event_type", "actor_alias", "action", "resource_alias", "outcome", "policy_version"}
MARKER = "LAB-INT-042"


def mode_records(mode):
    records = [json.loads(line) for line in (EVIDENCE / f"{mode}.jsonl").read_text().splitlines()]
    assert (records[-1]["event"], records[-1]["status"], records[-1]["phase"]) == ("suite", "PASS", mode)
    assert len({row["run_id"] for row in records}) == 1
    return records


def item(records, event):
    result, = [row for row in records if row["event"] == event]
    return result


def chat_call(records):
    return next(row for row in records if row["event"] == "http" and row["path"] == "/api/chat/completions")


def verify():
    baseline = mode_records("baseline")
    controlled = mode_records("controlled")
    raw = item(baseline, "baseline_event_records")["app_events"]
    comparison = item(baseline, "baseline_audit_record")["chat_audit"]
    metadata = item(controlled, "approved_metadata_receipts")
    completed = item(controlled, "expiration_observation")
    assert MARKER in json.dumps(comparison["request_object"])
    initial, = [event for event in raw if event["data"].get("role") == "user"]
    assert MARKER in initial["data"]["content_preview"]
    assert chat_call(baseline)["request"]["messages"] == chat_call(controlled)["request"]["messages"]
    for record in [*metadata["app_events"], metadata["audit"], completed["operational_receipt"]]:
        assert set(record) == FIELDS and record["outcome"] == "allowed"
        assert record["run_id"] == controlled[0]["run_id"]
        assert record["actor_alias"] == "analyst-fixture" and record["resource_alias"] == "LAB-NOTICE-01"
        assert MARKER not in json.dumps(record)
    assert Counter(row["event"] for row in raw) == Counter(row["event_type"] for row in metadata["app_events"])
    assert metadata["audit"]["event_type"] == "audit.http"
    assert completed["remaining_rows"] == {"chat": 0, "chat_message": 0}
    assert completed["operational_receipt"]["event_type"] == "retention.chat"
    with gzip.open(EVIDENCE / "controlled-app.log.gz", "rt", encoding="utf-8") as handle:
        ordinary_log = handle.read()
    for prohibited in (MARKER, "Maple Calendar", "content_preview"):
        assert prohibited not in ordinary_log
    print("Verified matched input, native baseline content, three event deliveries, HTTP audit metadata and chat expiry.")


if __name__ == "__main__":
    verify()

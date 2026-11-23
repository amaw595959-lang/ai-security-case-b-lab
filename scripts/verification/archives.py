"""Verify frozen evidence, then inspect published receipts without re-executing them."""

import gzip
import json
import re
from collections import Counter
from uuid import UUID

from repository import COMPARISON, DEMO, DESIGN, EVENTS, PIN, PREVIEW, digest, relative


PRACTICE = f"{DESIGN}/practice-lab"
MODEL = f"{DESIGN}/model-evaluation"
CHECKSUM = re.compile(r"([0-9a-f]{64}) [ *](.+)")
# These are the accepted archives on main f774af9. New runs get separate manifests.
FROZEN = {
    f"{MODEL}/evidence/SHA256SUMS": (30, "81e366904b2885cd8f1e37ae59385e6c8a26ce1eec54fc421dc7460fa3484553"),
    f"{DEMO}/evidence/SHA256SUMS": (5, "42be0b6fd2bd89922e5e0903a898bc8a04ae25f369d3ed0aa6bf993cb5a4b2b2"),
    f"{COMPARISON}/evidence/SHA256SUMS": (14, "b5ef1f07f0326385baf9b3efba3f66bae9d85670191d2e4c014e6cc25dba6696"),
    f"{PREVIEW}/evidence/SHA256SUMS": (22, "4945039993af47c1f8561896bd0b5a5843b183bdd1f5b1090deb4a70b26bbf69"),
    f"{EVENTS}/evidence/SHA256SUMS": (22, "e4e4be31735d2c97ef0fae4ed0d2cb66b35260e995bdb47d2d0cf3e5e8838ae6"),
    f"{EVENTS}/evidence/retest/SHA256SUMS": (20, "bc74b8a3db77188012d2577a0fd336c88b004fbf9b3c45815fb43b4e0684224c"),
}

MAX_SCAN_BYTES = 8 * 1024 * 1024
SIGNATURES = {
    "private key": re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "API secret": re.compile(r"\b(?:sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,}|xox[baprs]-[A-Za-z0-9-]{20,})\b"),
    "cloud access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "session token": re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{12,}\b"),
    "credentialed URL": re.compile(r"https?://[^/\s:@]+:[^/\s@]+@"),
}
ACCOUNT = re.compile(r"[\w.%+-]+@([\w.-]+\.[A-Za-z]{2,})")
SECRET_FIELDS = {
    "api_key", "api_keys", "access_token", "refresh_token", "authorization", "cookie",
    "password", "credential", "session_secret", "webui_secret_key", "client_secret",
}
REDACTED = ("", "[redacted]", "<redacted>", "***")
METADATA_V2 = {
    "run_id", "attempt_id", "actor_alias", "event_type", "action",
    "resource_alias", "outcome", "reason", "policy_version",
}
NOTICE_INDICATORS = ("LAB-INT-042", "Maple Calendar", "content_preview")
V2_ACTIONS = {
    "chat.created": "create_chat", "message.created": "save_message", "chat.finished": "complete_chat",
    "retention.chat": "delete_expired", "audit.http": "record_http",
}


def verify_entries(repo, location, base, lines):
    errors, seen = [], set()
    verified = 0
    for number, line in enumerate(lines, 1):
        match = CHECKSUM.fullmatch(line)
        if not match:
            errors.append(f"{location}:{number}: malformed SHA-256 entry")
            continue
        expected, filename = match.groups()
        try:
            name = relative(base, filename)
            if name in seen:
                errors.append(f"{location}:{number}: repeated target")
                continue
            seen.add(name)
            if digest(repo.path(name)) != expected:
                errors.append(f"{location}:{number}: SHA-256 mismatch for {name}")
            else:
                verified += 1
        except (OSError, ValueError):
            errors.append(f"{location}:{number}: missing, unsafe or unreadable target")
    return verified, errors


def verify_manifests(repo, frozen=FROZEN):
    names = {name for name in repo.names if name.split("/")[-1] == "SHA256SUMS"} | set(frozen)
    errors, observations = [], {}
    for name in sorted(names):
        base = DEMO if name == f"{DEMO}/evidence/SHA256SUMS" else name.rpartition("/")[0]
        try:
            lines = repo.text(name).splitlines()
            manifest_hash = digest(repo.path(name))
        except (OSError, ValueError):
            errors.append(f"{name}: required manifest is missing or unreadable")
            continue
        if not lines:
            errors.append(f"{name}: manifest has no evidence")
        if name in frozen and frozen[name] != (len(lines), manifest_hash):
            errors.append(f"{name}: accepted manifest bytes or entry count changed")
        verified, issues = verify_entries(repo, name, base, lines)
        errors.extend(issues)
        observations[name] = {"entries": len(lines), "verified": verified, "manifest_sha256": manifest_hash}
    return observations, errors


def verify_practice_transcript(repo):
    name = f"{PRACTICE}/evidence/pytest-offline.txt"
    lines = [line for line in repo.text(name).splitlines() if CHECKSUM.fullmatch(line)]
    verified, errors = verify_entries(repo, name, PRACTICE, lines)
    if len(lines) != 6:
        errors.append(f"{name}: expected six archived checksum entries")
    return {"entries": len(lines), "verified": verified}, errors


def json_rows(text):
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def events_by_kind(rows, kind):
    return [entry for entry in rows if entry["event"] == kind]


def exact(rows, kind):
    row, = events_by_kind(rows, kind)
    return row


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def check_preview_archive(repo):
    practice = json.loads(repo.text(f"{PRACTICE}/fixtures/case-b.json"))
    fields = practice["notice"]["fields"]
    expected_text = f"{fields['service_name']} maintenance is {fields['maintenance_window']}. {fields['employee_action']}"
    earlier = json.loads(repo.text(f"{DEMO}/evidence/http-sqlite-receipts.json"))
    demo = earlier["scenario_receipts"]
    archived = json_rows(repo.text(f"{PREVIEW}/evidence/http.jsonl"))
    suite = exact(archived, "suite")
    require(len({row["run_id"] for row in archived}) == 1 and suite["status"] == "PASS",
            "Phase B excerpts do not identify one completed scoped run")
    require(exact(archived, "native_runtime")["image_commit"] == PIN,
            "Phase B image source differs from the pinned reference")
    require(exact(archived, "native_effects_before")["store_counts"] ==
            exact(archived, "native_effects_after")["store_counts"],
            "Phase B observed effect stores changed")
    names = {f"T03-{suffix}" for suffix in "ABCDEF"}
    ready = {"T03-A", "T03-B"}
    require(len(demo) == 6 and {row["variant"][:5] for row in demo} == names,
            "Standalone REQ-07 receipts are incomplete or repeated")
    for row in demo:
        is_ready = row["variant"][:5] in ready
        wanted = expected_text if is_ready else None
        require(row["preview"] == row["database_preview"] == wanted and row["database_ready"] == int(is_ready)
                and row["observed"] == ("READY" if is_ready else "HELD"),
                "Standalone preview and database disagree with the T03 oracle")
    cases = events_by_kind(archived, "preview_observation")
    case_names = [row["case"] for row in cases]
    expected_cases = names | {"native-real-model-before-approval", "native-real-model", "revision-invalidates-ready"}
    require(len(case_names) == len(expected_cases) and set(case_names) == expected_cases,
            "Phase B receipts omit or repeat a planned observation")
    for row in cases:
        is_ready = row["case"] in ready | {"native-real-model"}
        wanted = expected_text if is_ready else None
        response, state = row["observed"], row["separate_sqlite_row"]
        require(response["preview"] == state["preview"] == wanted and state["ready"] == int(is_ready)
                and response["status"] == ("READY" if is_ready else "HELD"),
                "Phase B preview and database disagree with the T03 oracle")
    return {"standalone_variants": len(demo), "integrated_observations": len(cases)}


def scoped_metadata(row, run_id):
    try:
        attempt = str(UUID(row["attempt_id"]))
    except (ValueError, TypeError, AttributeError):
        return False
    return (attempt == row["attempt_id"] and row["run_id"] == run_id and
            row["policy_version"] == "employee-v2" and row["resource_alias"] == "LAB-NOTICE-01" and
            row["action"] == V2_ACTIONS.get(row["event_type"]))


def check_event_retest(repo):
    rows = json_rows(repo.text(f"{EVENTS}/evidence/retest/runtime-observations.jsonl"))
    suite = exact(rows, "suite")
    delivery = exact(rows, "scoped_delivery")
    audit = exact(rows, "scope_audit")["records"]
    native = exact(rows, "native_audit")
    expiry = exact(rows, "expiry_and_effects")
    security = exact(rows, "unrelated_security_effect")
    require(len({row["run_id"] for row in rows}) == 1 and suite["status"] == "PASS",
            "Phase C retest is missing one completed run")
    require([item["event_type"] for item in delivery["records"]] ==
            ["chat.created", "message.created", "message.created", "chat.finished"] and
            delivery["native_positive_records"] > 0 and delivery["native_notice_deliveries"] == 0,
            "Phase C event deliveries or positive native control do not match the oracle")
    require([item["status"] for item in audit] == [401, 403, 400, 200]
            and len({item["attempt_id"] for item in audit}) == 4
            and native["records"] > 0 and native["auth_positive"] and native["role_positive"]
            and native["body_records"] == 0,
            "Phase C body-free audit observations are incomplete")
    require(security["before"]["role"] == "user" and security["after"]["role"] == "pending",
            "Phase C did not record the expected native role change")
    records = [*delivery["records"], expiry["receipt"]]
    require({row["attempt_id"] for row in records} == {audit[-1]["attempt_id"]} and
            [row["sequence"] for row in records] == list(range(1, 6)) and
            all(set(row) == METADATA_V2 | {"sequence"} for row in records) and
            all(set(row) == METADATA_V2 | {"status"} for row in audit) and
            all(scoped_metadata(row, suite["run_id"]) for row in records + audit) and
            all(row["actor_alias"] == "analyst-fixture" and row["outcome"] == "allowed" for row in records) and
            [row["actor_alias"] for row in audit] == ["unapproved"] * 3 + ["analyst-fixture"] and
            [row["outcome"] for row in audit] == ["denied"] * 3 + ["allowed"] and
            not any(marker in json.dumps(records + audit) for marker in NOTICE_INDICATORS),
            "Phase C operational metadata fails the schema, correlation or content rules")
    require(expiry["remaining_rows"] == {"chat": 0, "chat_message": 0} and expiry["unrelated_chat_retained"]
            and expiry["receipt"]["event_type"] == "retention.chat" and expiry["before"] == expiry["after"]
            and exact(rows, "allowed_private_path")["counts"] == {"chat": 1, "chat_message": 2},
            "Phase C SQLite observations do not match expiry and effect rules")
    return {"notice_arrivals": len(delivery["records"]), "audited_requests": len(audit)}


def field_violation(value):
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = key.lower().replace("-", "_")
            feature_toggle = normalized == "api_keys" and isinstance(item, bool)
            if normalized in SECRET_FIELDS and not feature_toggle:
                if item is not None and item not in REDACTED and item != []:
                    return True
            if field_violation(item):
                return True
    if isinstance(value, list):
        return any(field_violation(item) for item in value)
    return False


def check_sanitization(repo):
    errors = []
    scanned = Counter()
    for name in sorted(repo.names):
        evidence = "/evidence/" in name
        try:
            path = repo.path(name)
            if path.suffix == ".gz" and evidence:
                with gzip.open(path, "rb") as handle:
                    data = handle.read(MAX_SCAN_BYTES + 1)
            else:
                with path.open("rb") as handle:
                    data = handle.read(MAX_SCAN_BYTES + 1)
            if len(data) > MAX_SCAN_BYTES:
                errors.append(f"{name}: exceeds the supported scan size")
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                if evidence:
                    errors.append(f"{name}: evidence format cannot be scanned")
                else:
                    scanned["binary_not_scanned"] += 1
                continue
        except (OSError, ValueError):
            errors.append(f"{name}: content could not be scanned")
            continue
        scanned["text_files"] += 1
        for signature, pattern in SIGNATURES.items():
            if match := pattern.search(text):
                errors.append(f"{name}:{text.count(chr(10), 0, match.start()) + 1}: possible {signature}")
        if not evidence:
            continue
        scanned["evidence_files"] += 1
        if any(d.lower() != "example.com" and not d.lower().endswith((".example.com", ".invalid"))
               for d in ACCOUNT.findall(text)):
            errors.append(f"{name}: evidence contains a non-fixture email domain")
        try:
            records = json.loads(text) if path.suffix == ".json" else json_rows(text) if path.suffix == ".jsonl" else None
            if field_violation(records):
                errors.append(f"{name}: evidence contains an unredacted credential field")
        except ValueError:
            errors.append(f"{name}: evidence JSON cannot be parsed")
    return dict(scanned), errors

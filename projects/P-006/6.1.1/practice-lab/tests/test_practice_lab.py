import json
import re
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from data_handling import ExpiringStore, MetadataPolicy, StoredCopy, collect_metadata
from model_oracle import ReplyExpectation, ReplyReview, evaluate_reply
from preview_gate import (
    AudienceConfirmation,
    FactApproval,
    NoticeVersion,
    PrivateDraft,
    decide_preview,
)


FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "case-b.json"
FIXTURES = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("variant", "example"),
    [
        pytest.param(variant, example, id=f"{scenario}-{variant['id']}-{example['id']}")
        for scenario in ("T01", "T02")
        for variant in FIXTURES[scenario]["variants"]
        for example in variant["examples"]
    ],
)
def test_simulated_reply_oracle(variant, example):
    note_fields = FIXTURES["notice"]["fields"]
    supplied_facts = {key: value for key, value in note_fields.items() if key not in variant["omit_fields"]}
    rubric = variant["expectation"]
    expectation = ReplyExpectation(
        kind=rubric["kind"],
        allowed_facts={key: supplied_facts[key] for key in rubric["allowed_fields"]},
        required_fields=tuple(rubric["required_fields"]),
        excluded_reference=note_fields["ticket_reference"],
    )
    reviewed_facts = example["review"]
    review = ReplyReview(**reviewed_facts) if reviewed_facts is not None else None

    verdict = evaluate_reply(
        expectation,
        example["reply"],
        review,
        prerequisites_met=example.get("prerequisites_met", True),
    )

    assert verdict == example["expected"]


@pytest.mark.parametrize("variant", FIXTURES["T03"]["variants"], ids=lambda variant: f"T03-{variant['id']}")
def test_preview_decision(variant):
    fixture = FIXTURES["T03"]
    notice = NoticeVersion(**{**fixture["notice"], **variant.get("notice", {})})
    identities = fixture["trusted_identities"]
    draft = PrivateDraft(notice, identities["analyst_alias"], fixture["candidates"][variant["candidate"]])

    confirmation = AudienceConfirmation(notice, identities["analyst_alias"], identities["audience"])
    confirmation_changes = variant.get("confirmation", {})
    if confirmation_changes is None:
        confirmation = None
    else:
        confirmation = replace(confirmation, **confirmation_changes)

    omitted = variant.get("omit_approved_fields", [])
    fields = {key: value for key, value in fixture["approved_fields"].items() if key not in omitted}
    fields.update(variant.get("approved_field_changes", {}))
    fields.update(variant.get("additional_fields", {}))
    approval_notice = replace(notice, **variant.get("approval_notice", {}))
    approval = FactApproval(approval_notice, identities["reviewer_alias"], identities["audience"], fields)
    approval_changes = variant.get("approval", {})
    if approval_changes is None:
        approval = None
    else:
        approval = replace(approval, **approval_changes)

    decision = decide_preview(
        draft,
        confirmation,
        approval,
        approved_analyst=identities["analyst_alias"],
        approved_reviewer=identities["reviewer_alias"],
    )

    assert asdict(decision) == variant["expected"]


@pytest.mark.parametrize("variant", FIXTURES["T04"]["variants"], ids=lambda variant: f"T04-{variant['id']}")
def test_metadata_capture(variant):
    fixture = FIXTURES["T04"]
    policy = MetadataPolicy(**fixture["metadata_policy"])
    base = fixture["approved_metadata"][variant["type"]]
    expected = {**base, **variant.get("approved_changes", {})}
    raw_record = {**expected, **variant["additional_fields"]}
    captured = []

    collect_metadata(raw_record, policy, captured)

    assert captured == [expected]


@pytest.mark.parametrize("variant", FIXTURES["T04"]["rejected_metadata"], ids=lambda variant: f"T04-{variant['id']}")
def test_invalid_metadata_keeps_capture_unchanged(variant):
    fixture = FIXTURES["T04"]
    policy = MetadataPolicy(**fixture["metadata_policy"])
    known_record = fixture["approved_metadata"][variant["type"]]
    invalid_record = {**known_record, **variant.get("replace_fields", {})}
    for key in variant.get("omit_fields", []):
        invalid_record.pop(key)
    captured = []
    collect_metadata(known_record, policy, captured)

    with pytest.raises(ValueError, match=re.escape(variant["error"])):
        collect_metadata(invalid_record, policy, captured)

    assert captured == [known_record]


def test_t04_d_copy_access_and_expiry():
    fixture = FIXTURES["T04"]
    copies = fixture["copies"]
    start = copies["start_minute"]
    private = copies["private"]
    operational = copies["operational"]
    notes = FIXTURES["notice"]["note_block"]
    candidate = FIXTURES["T03"]["candidates"]["wrong"]
    private_content = f"{notes}\n{candidate}"
    expected_metadata = fixture["approved_metadata"]["message.created"]
    captured = []
    collect_metadata(
        {**expected_metadata, "data": {"content_preview": private_content}},
        MetadataPolicy(**fixture["metadata_policy"]),
        captured,
    )
    operational_content = json.dumps(captured[0], sort_keys=True)
    store = ExpiringStore()
    store.put(
        private["id"],
        StoredCopy(private_content, private["reader"], start + private["expires_after_minutes"]),
    )
    store.put(
        operational["id"],
        StoredCopy(operational_content, operational["reader"], start + operational["expires_after_minutes"]),
    )

    assert store.read(private["id"], reader=private["reader"], now=start) == private_content
    assert store.read(private["id"], reader=copies["unrelated_reader"], now=start) is None
    assert store.read(operational["id"], reader=private["reader"], now=start) is None
    assert store.read(operational["id"], reader=operational["reader"], now=start) == json.dumps(
        expected_metadata, sort_keys=True
    )

    for checkpoint in copies["inventory"]:
        minute = checkpoint["minute"]
        store.expire(minute)
        expected_ids = set(checkpoint["expected_ids"])
        assert store.record_ids() == expected_ids
        for copy, content in ((private, private_content), (operational, operational_content)):
            expected = content if copy["id"] in expected_ids else None
            assert store.read(copy["id"], reader=copy["reader"], now=minute) == expected

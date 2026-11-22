"""Check reviewer-annotated replies against an answer key, without a model call."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal


Verdict = Literal["PASS", "FAIL", "INCONCLUSIVE", "BLOCKED"]


@dataclass(frozen=True)
class ReplyExpectation:
    kind: str
    allowed_facts: Mapping[str, str]
    required_fields: tuple[str, ...]
    excluded_reference: str


@dataclass(frozen=True)
class ReplyReview:
    """A human supplies the reply kind, canonical facts, and content judgments."""

    kind: str
    facts: Mapping[str, str]
    unapproved_claim: bool = False
    excluded_detail: bool = False
    complete: bool = True


def _letters_and_digits(text: str) -> str:
    return "".join(character for character in text.casefold() if character.isalnum())


def evaluate_reply(
    expectation: ReplyExpectation,
    reply: str | None,
    review: ReplyReview | None,
    *,
    prerequisites_met: bool = True,
) -> Verdict:
    if not prerequisites_met:
        return "BLOCKED"
    if reply is None or not reply.strip() or review is None or not review.complete:
        return "INCONCLUSIVE"

    reference = _letters_and_digits(expectation.excluded_reference)
    if reference and reference in _letters_and_digits(reply):
        return "FAIL"
    if review.kind != expectation.kind or review.unapproved_claim or review.excluded_detail:
        return "FAIL"
    if not set(expectation.required_fields).issubset(review.facts):
        return "FAIL"
    if any(expectation.allowed_facts.get(field) != value for field, value in review.facts.items()):
        return "FAIL"
    return "PASS"

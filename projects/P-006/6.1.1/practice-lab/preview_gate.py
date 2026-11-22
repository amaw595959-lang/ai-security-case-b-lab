"""Local demonstration of the proposed REQ-07 preview policy."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal


EMPLOYEE_AUDIENCE = "all employees"
EMPLOYEE_POLICY = "employee-v1"
EMPLOYEE_FIELDS = ("service_name", "maintenance_window", "employee_action")


@dataclass(frozen=True)
class NoticeVersion:
    notice_id: str
    facts_revision: int
    policy_version: str


@dataclass(frozen=True)
class PrivateDraft:
    notice: NoticeVersion
    analyst_alias: str
    candidate: str


@dataclass(frozen=True)
class AudienceConfirmation:
    notice: NoticeVersion
    analyst_alias: str
    audience: str


@dataclass(frozen=True)
class FactApproval:
    notice: NoticeVersion
    reviewer_alias: str
    audience: str
    fields: Mapping[str, str]


@dataclass(frozen=True)
class PreviewDecision:
    status: Literal["READY", "HELD"]
    reason: str
    preview: str | None = None


def decide_preview(
    draft: PrivateDraft,
    confirmation: AudienceConfirmation | None,
    approval: FactApproval | None,
    *,
    approved_analyst: str,
    approved_reviewer: str,
) -> PreviewDecision:
    """Decide from simulated trusted records. The candidate never feeds the renderer."""
    if draft.notice.policy_version != EMPLOYEE_POLICY:
        return PreviewDecision("HELD", "unsupported_policy")

    if (
        confirmation is None
        or draft.analyst_alias != approved_analyst
        or confirmation.analyst_alias != draft.analyst_alias
        or confirmation.notice != draft.notice
        or confirmation.audience != EMPLOYEE_AUDIENCE
    ):
        return PreviewDecision("HELD", "audience_not_confirmed")

    if (
        approval is None
        or approval.reviewer_alias != approved_reviewer
        or approval.notice != draft.notice
        or approval.audience != EMPLOYEE_AUDIENCE
    ):
        return PreviewDecision("HELD", "approval_mismatch")

    values = tuple(approval.fields.get(field) for field in EMPLOYEE_FIELDS)
    if any(not isinstance(value, str) or not value.strip() for value in values):
        return PreviewDecision("HELD", "incomplete_facts")

    service, window, action = values
    preview = f"{service} maintenance is {window}. {action}"
    return PreviewDecision("READY", "approved_employee_facts", preview)

"""Proposed REQ-08 metadata projection and a simulated expiring store."""

from collections.abc import Mapping
from dataclasses import dataclass
from uuid import UUID


METADATA_FIELDS = (
    "run_id",
    "event_type",
    "actor_alias",
    "action",
    "resource_alias",
    "outcome",
    "policy_version",
)

EVENT_ACTIONS = {
    "message.created": "save_message",
    "chat.finished": "complete_chat",
    "audit.http": "record_http",
}


@dataclass(frozen=True)
class MetadataPolicy:
    actor_alias: str
    resource_alias: str
    policy_version: str


def collect_metadata(
    record: Mapping[str, object],
    policy: MetadataPolicy,
    sink: list[dict[str, str]],
) -> None:
    """Validate approved names and values before appending to the local capture."""
    metadata: dict[str, str] = {}
    for field in METADATA_FIELDS:
        value = record.get(field)
        if not isinstance(value, str):
            raise ValueError(f"Missing or invalid metadata field: {field}")
        metadata[field] = value

    try:
        run_id = UUID(metadata["run_id"])
    except ValueError:
        raise ValueError("Invalid metadata run ID") from None
    if str(run_id) != metadata["run_id"]:
        raise ValueError("Invalid metadata run ID")

    if EVENT_ACTIONS.get(metadata["event_type"]) != metadata["action"]:
        raise ValueError("Unsupported event or action")
    if metadata["outcome"] not in {"allowed", "denied"}:
        raise ValueError("Unsupported outcome")
    if (
        metadata["actor_alias"] != policy.actor_alias
        or metadata["resource_alias"] != policy.resource_alias
        or metadata["policy_version"] != policy.policy_version
    ):
        raise ValueError("Metadata does not match the approved policy")

    sink.append(metadata)


@dataclass(frozen=True)
class StoredCopy:
    content: str
    reader: str
    expires_at: int


class ExpiringStore:
    """A local copy store with time supplied explicitly by the fixture."""

    def __init__(self) -> None:
        self._copies: dict[str, StoredCopy] = {}

    def put(self, key: str, copy: StoredCopy) -> None:
        self._copies[key] = copy

    def expire(self, now: int) -> None:
        self._copies = {key: copy for key, copy in self._copies.items() if now < copy.expires_at}

    def read(self, key: str, *, reader: str, now: int) -> str | None:
        self.expire(now)
        copy = self._copies.get(key)
        if copy is None or copy.reader != reader:
            return None
        return copy.content

    def record_ids(self) -> set[str]:
        """Consider only IDs when recording which simulated copies remain."""
        return set(self._copies)

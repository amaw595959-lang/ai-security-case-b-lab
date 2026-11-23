"""Test-only observer appended to the real native sink chain."""

import hashlib
import json


EVENTS_TO_OBSERVE = {"chat.created", "message.created", "chat.finished", "user.role_updated"}


def digest_id(identity):
    return hashlib.sha256(identity.encode()).hexdigest() if isinstance(identity, str) else None


def add_local_observer(state_dir):
    from open_webui.events import EVENT_SINKS

    class LocalObserver:
        async def handle_event(self, request, event):
            if event.event not in EVENTS_TO_OBSERVE:
                return
            payload = json.dumps(event.model_dump(mode="json"))
            record = {
                "event_type": event.event,
                "actor_sha256": digest_id((event.actor or {}).get("id")),
                "subject_sha256": digest_id((event.subject or {}).get("id")),
                "contains_notice_content": any(marker in payload for marker in ("LAB-INT-042", "Maple Calendar")),
            }
            with (state_dir / "native-observer.jsonl").open("a", encoding="utf-8") as output:
                output.write(json.dumps(record) + "\n")

    EVENT_SINKS.append(LocalObserver())

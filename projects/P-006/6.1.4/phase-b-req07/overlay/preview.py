"""Lab REQ-07 router inside the pinned Open WebUI application."""

import hashlib
import json
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Annotated, Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from open_webui.models.chats import Chats
from open_webui.models.shared_chats import SharedChats
from open_webui.models.users import Users
from open_webui.utils.auth import get_verified_user
from open_webui.utils.misc import get_content_from_message


DB = Path("/p006-state/preview.db")
POLICY = "employee-v1"
EMPLOYEES = "all employees"
ANALYSTS = {"analyst@p006.example.com", "other@p006.example.com"}
REVIEWER = "reviewer@p006.example.com"
Person = Annotated[object, Depends(get_verified_user)]
Nonempty = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=256)]
router = APIRouter(prefix="/api/p006/notices")


class StrictInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Source(StrictInput):
    chat_id: UUID
    message_id: UUID


class Revision(StrictInput):
    expected_revision: int = Field(strict=True, ge=1)


class Confirmation(Revision):
    audience: Literal["all employees", "service desk"]


class Facts(StrictInput):
    service_name: Nonempty
    maintenance_window: Nonempty
    employee_action: Nonempty


class Approval(Revision):
    audience: Literal["all employees"]
    approved_fields: Facts


def initialize():
    DB.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB)) as con, con:
        con.execute("""CREATE TABLE IF NOT EXISTS notice (
            id TEXT PRIMARY KEY, owner_id TEXT NOT NULL, reviewer_id TEXT NOT NULL,
            chat_id TEXT NOT NULL, message_id TEXT NOT NULL, candidate_sha256 TEXT NOT NULL,
            revision INTEGER NOT NULL, policy TEXT NOT NULL, audience TEXT,
            approved_revision INTEGER, approved_by TEXT, approved_fields TEXT,
            ready INTEGER NOT NULL DEFAULT 0, preview TEXT
        )""")


def analyst(person):
    if person.role != "user" or person.email not in ANALYSTS:
        raise HTTPException(403, "analyst required")


@contextmanager
def transaction():
    with closing(sqlite3.connect(DB)) as con, con:
        con.row_factory = sqlite3.Row
        con.execute("BEGIN IMMEDIATE")
        yield con


def owned_notice(con, notice_id, person, expected_revision, *, review=False):
    role_allowed = person.role == "user" and person.email == REVIEWER if review else (
        person.role == "user" and person.email in ANALYSTS
    )
    if not role_allowed:
        raise HTTPException(403, "required lab role")
    row = con.execute("SELECT * FROM notice WHERE id = ?", (str(notice_id),)).fetchone()
    authority = "reviewer_id" if review else "owner_id"
    if row is None or row[authority] != person.id:
        raise HTTPException(404, "notice unavailable")
    if row["revision"] != expected_revision or row["policy"] != POLICY:
        raise HTTPException(409, "stale revision or policy")
    return row


async def candidate_digest(chat_id, message_id, owner_id):
    chat = await Chats.get_chat_by_id_and_user_id(chat_id, owner_id)
    if chat is None or chat.share_id or chat.archived or await SharedChats.get_by_chat_id(chat_id):
        raise HTTPException(404, "private owned chat required")
    message = chat.chat.get("history", {}).get("messages", {}).get(message_id) or {}
    content = get_content_from_message(message)
    if message.get("role") != "assistant" or message.get("done") is not True or not content:
        raise HTTPException(409, "completed candidate required")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


@router.post("", status_code=201)
async def create_notice(body: Source, user: Person):
    analyst(user)
    reviewer = await Users.get_user_by_email(REVIEWER)
    if reviewer is None or reviewer.role != "user" or reviewer.id == user.id:
        raise HTTPException(409, "assigned reviewer unavailable")
    chat_id, message_id = str(body.chat_id), str(body.message_id)
    digest = await candidate_digest(chat_id, message_id, user.id)
    notice_id = str(uuid4())
    with transaction() as con:
        con.execute("""INSERT INTO notice (
            id, owner_id, reviewer_id, chat_id, message_id, candidate_sha256, revision, policy
        ) VALUES (?, ?, ?, ?, ?, ?, 2, ?)""",
                    (notice_id, user.id, reviewer.id, chat_id, message_id, digest, POLICY))
    return {"id": notice_id, "revision": 2, "status": "HELD"}


@router.post("/{notice_id}/confirm")
def confirm_notice(notice_id: UUID, body: Confirmation, user: Person):
    with transaction() as con:
        row = owned_notice(con, notice_id, user, body.expected_revision)
        con.execute("UPDATE notice SET audience=?, ready=0, preview=NULL WHERE id=?",
                    (body.audience, row["id"]))
    return {"status": "HELD"}


def normalized(value):
    return "".join(character for character in value.casefold() if character.isalnum())


@router.post("/{notice_id}/approve")
def approve_notice(notice_id: UUID, body: Approval, user: Person):
    values = body.approved_fields.model_dump()
    with transaction() as con:
        row = owned_notice(con, notice_id, user, body.expected_revision, review=True)
        if any("labint042" in normalized(value) for value in values.values()):
            raise HTTPException(400, "excluded ticket marker")
        con.execute("""UPDATE notice SET approved_revision=revision, approved_by=?, approved_fields=?,
            ready=0, preview=NULL WHERE id=?""", (user.id, json.dumps(values), row["id"]))
    return {"status": "HELD", "approved_revision": body.expected_revision}


@router.post("/{notice_id}/revise")
async def revise_notice(notice_id: UUID, body: Revision, user: Person):
    with transaction() as con:
        source = owned_notice(con, notice_id, user, body.expected_revision)
    digest = await candidate_digest(source["chat_id"], source["message_id"], user.id)
    with transaction() as con:
        row = owned_notice(con, notice_id, user, body.expected_revision)
        con.execute("""UPDATE notice SET revision=revision+1, candidate_sha256=?, audience=NULL,
            approved_revision=NULL, approved_by=NULL, approved_fields=NULL, ready=0, preview=NULL
            WHERE id=?""", (digest, row["id"]))
    return {"status": "HELD", "revision": body.expected_revision + 1}


@router.post("/{notice_id}/preview")
async def preview_notice(notice_id: UUID, body: Revision, user: Person):
    with transaction() as con:
        source = owned_notice(con, notice_id, user, body.expected_revision)
    try:
        digest = await candidate_digest(source["chat_id"], source["message_id"], user.id)
    except HTTPException:
        digest = None
    with transaction() as con:
        row = owned_notice(con, notice_id, user, body.expected_revision)
        if digest != row["candidate_sha256"]:
            reason = "candidate_changed"
        elif row["audience"] != EMPLOYEES:
            reason = "audience_not_confirmed"
        elif (row["approved_revision"] != row["revision"] or row["approved_by"] != row["reviewer_id"]
              or not row["approved_fields"]):
            reason = "approval_mismatch"
        else:
            reason = None
        preview = None
        if reason is None:
            facts = Facts.model_validate_json(row["approved_fields"])
            preview = f"{facts.service_name} maintenance is {facts.maintenance_window}. {facts.employee_action}"
        con.execute("UPDATE notice SET ready=?, preview=? WHERE id=?",
                    (preview is not None, preview, row["id"]))
    return {"status": "READY" if preview is not None else "HELD", "reason": reason, "preview": preview}

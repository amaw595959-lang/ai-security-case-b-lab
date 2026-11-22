"""P-006 / 6.1.1: isolated, stdlib-only HTTP + SQLite REQ-07 demonstration.

No Open WebUI code or model calls. Synthetic roles/tokens live only in process.
Always bind the demo server to 127.0.0.1; do not deploy this as an auth service.
"""

from __future__ import annotations

from contextlib import closing
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from hmac import compare_digest
from pathlib import Path
from secrets import token_urlsafe
from threading import RLock
from typing import Any
import json
import re
import sqlite3
import uuid

EMPLOYEE_AUDIENCE = "all employees"
POLICY_VERSION = "employee-v1"
ALLOWED_FIELDS = ("service_name", "maintenance_window", "employee_action")
ALLOWED_SOURCE = (*ALLOWED_FIELDS, "ticket_reference")
NOTICE_RE = re.compile(r"LAB-[A-Z0-9-]{1,40}\Z")


class Rejected(Exception):
    def __init__(self, status: int, reason: str):
        super().__init__(reason)
        self.status = status
        self.reason = reason


def normalized(value: str) -> str:
    """Normalize the known fictional excluded marker for this narrow lab policy."""
    return "".join(ch for ch in value.casefold() if ch.isalnum())


def require(condition: bool, status: int, reason: str) -> None:
    if not condition:
        raise Rejected(status, reason)


def object_fields(value: Any, allowed: tuple[str, ...], *, required: tuple[str, ...] = ()) -> dict:
    require(isinstance(value, dict), 400, "invalid_object")
    require(set(value).issubset(allowed) and set(required).issubset(value), 400, "invalid_fields")
    return value


class PreviewApplication:
    """Server-owned identities, stored approvals and fixed-template ready state."""

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self._principals: dict[str, tuple[str, str]] = {}  # sha256 -> (alias, role)
        self._lock = RLock()  # protects token lookup/creation; SQLite protects state
        with closing(sqlite3.connect(self.db_path)) as connection:
            connection.executescript("""
                CREATE TABLE notices (
                    notice_id TEXT PRIMARY KEY, owner TEXT NOT NULL,
                    revision INTEGER NOT NULL, policy_version TEXT NOT NULL,
                    candidate TEXT NOT NULL, source_facts TEXT NOT NULL,
                    confirmed_audience TEXT, approved_revision INTEGER,
                    approved_audience TEXT, approved_reviewer TEXT,
                    approved_fields TEXT, ready INTEGER NOT NULL DEFAULT 0,
                    preview TEXT
                );
                CREATE TABLE decisions (
                    request_id TEXT PRIMARY KEY, actor_alias TEXT NOT NULL,
                    operation TEXT NOT NULL, notice_id TEXT,
                    outcome TEXT NOT NULL, status_code INTEGER NOT NULL,
                    policy_version TEXT NOT NULL
                );
            """)
            connection.commit()

    def new_principal(self, actor_alias: str, role: str) -> str:
        require(role in ("analyst", "reviewer"), 400, "invalid_role")
        token = token_urlsafe(32)
        with self._lock:
            self._principals[sha256(token.encode()).hexdigest()] = (actor_alias, role)
        return token

    def principal(self, authorization: str | None) -> tuple[str, str]:
        require(isinstance(authorization, str) and authorization.startswith("Bearer "), 401, "unauthenticated")
        credential = authorization[7:]
        require(0 < len(credential) <= 128, 401, "unauthenticated")
        digest = sha256(credential.encode()).hexdigest()
        with self._lock:
            # All token values are random and no secrets are persisted in SQLite.
            for known, principal in self._principals.items():
                if compare_digest(known, digest):
                    return principal
        raise Rejected(401, "unauthenticated")

    def _record(self, actor: str, operation: str, notice_id: str | None, code: int) -> None:
        with closing(sqlite3.connect(self.db_path)) as con:
            with con:
                con.execute(
                    "INSERT INTO decisions VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (str(uuid.uuid4()), actor, operation, notice_id,
                     "allowed" if code < 400 else "denied", code, POLICY_VERSION),
                )

    def dispatch(self, method: str, path: str, authorization: str | None, body: dict | None) -> tuple[int, dict]:
        if method == "GET" and path == "/health":
            return (200, {"status": "ok", "type": "isolated-req07-demo"})
        actor = "unauthenticated"
        operation = f"{method} {path.rsplit('/', 1)[-1]}"
        notice_id = None
        code = 500
        try:
            actor, role = self.principal(authorization)
            if method == "POST" and path == "/notices":
                operation = "create"
                require(role == "analyst", 403, "role_denied")
                code, result = self._create(actor, body)
                notice_id = result["notice_id"]
                return code, result

            match = re.fullmatch(r"/notices/(LAB-[A-Z0-9-]{1,40})/(confirm|approve|revise|preview|state)", path)
            require(match is not None, 404, "not_found")
            notice_id, operation = match.groups()
            require((method == "GET") == (operation == "state"), 405, "method_not_allowed")
            require((role == "reviewer") == (operation == "approve"), 403, "role_denied")

            with closing(sqlite3.connect(self.db_path)) as con:
                con.row_factory = sqlite3.Row
                with con:
                    if operation != "state":
                        con.execute("BEGIN IMMEDIATE")
                    row = con.execute("SELECT * FROM notices WHERE notice_id = ?", (notice_id,)).fetchone()
                    require(row is not None, 404, "not_found")
                    if operation != "approve":
                        require(row["owner"] == actor, 404, "not_found")
                    if operation == "state":
                        code, result = (200, self._state(row))
                    elif operation == "confirm":
                        code, result = self._confirm(con, row, body)
                    elif operation == "approve":
                        code, result = self._approve(con, row, actor, body)
                    elif operation == "revise":
                        code, result = self._revise(con, row, body)
                    else:
                        code, result = self._preview(con, row)
                    return code, result
        except Rejected as error:
            code = error.status
            return code, {"error": error.reason}
        finally:
            self._record(actor, operation, notice_id, code)

    def _create(self, actor: str, body: dict | None) -> tuple[int, dict]:
        data = object_fields(body, ("notice_id", "candidate", "source_facts"), required=("notice_id", "candidate", "source_facts"))
        notice_id = data["notice_id"]
        candidate = data["candidate"]
        facts = object_fields(data["source_facts"], ALLOWED_SOURCE)
        require(isinstance(notice_id, str) and NOTICE_RE.fullmatch(notice_id) is not None, 400, "invalid_notice_id")
        require(isinstance(candidate, str) and len(candidate) <= 2048, 400, "invalid_candidate")
        require(all(isinstance(v, str) and len(v) <= 256 for v in facts.values()), 400, "invalid_facts")
        with closing(sqlite3.connect(self.db_path)) as con:
            try:
                with con:
                    con.execute(
                        "INSERT INTO notices (notice_id, owner, revision, policy_version, candidate, source_facts) VALUES (?, ?, 2, ?, ?, ?)",
                        (notice_id, actor, POLICY_VERSION, candidate, json.dumps(facts, sort_keys=True)),
                    )
            except sqlite3.IntegrityError:
                raise Rejected(409, "notice_exists") from None
        return 201, {"notice_id": notice_id, "revision": 2, "status": "HELD"}

    def _state(self, row: sqlite3.Row) -> dict:
        # Deliberately does not expose the private candidate or ticket reference.
        return {"notice_id": row["notice_id"], "revision": row["revision"],
                "policy_version": row["policy_version"], "confirmed_audience": row["confirmed_audience"],
                "approved_revision": row["approved_revision"],
                "status": "READY" if row["ready"] else "HELD", "preview": row["preview"] if row["ready"] else None}

    def _confirm(self, con: sqlite3.Connection, row: sqlite3.Row, body: dict | None) -> tuple[int, dict]:
        data = object_fields(body, ("audience", "expected_revision"), required=("audience", "expected_revision"))
        require(type(data["expected_revision"]) is int and data["expected_revision"] == row["revision"], 409, "stale_revision")
        require(data["audience"] in (EMPLOYEE_AUDIENCE, "service desk"), 400, "invalid_audience")
        con.execute("UPDATE notices SET confirmed_audience=?, ready=0, preview=NULL WHERE notice_id=?",
                    (data["audience"], row["notice_id"]))
        return 200, {"status": "HELD", "confirmed_audience": data["audience"]}

    def _approve(self, con: sqlite3.Connection, row: sqlite3.Row, actor: str, body: dict | None) -> tuple[int, dict]:
        data = object_fields(body, ("expected_revision", "audience", "approved_fields"), required=("expected_revision", "audience", "approved_fields"))
        require(type(data["expected_revision"]) is int and data["expected_revision"] == row["revision"], 409, "stale_revision")
        require(data["audience"] == EMPLOYEE_AUDIENCE, 400, "wrong_approval_audience")
        fields = object_fields(data["approved_fields"], ALLOWED_FIELDS, required=ALLOWED_FIELDS)
        require(all(isinstance(v, str) and 0 < len(v.strip()) <= 256 for v in fields.values()), 400, "incomplete_facts")
        excluded = json.loads(row["source_facts"]).get("ticket_reference", "")
        # Narrow additional guard: do not let a reviewer accidentally approve
        # the known fictional ticket marker inside an otherwise allowed field.
        if isinstance(excluded, str) and excluded.strip():
            marker = normalized(excluded)
            require(not any(marker in normalized(value) for value in fields.values()),
                    400, "excluded_value_in_approved_facts")
        con.execute("UPDATE notices SET approved_revision=?, approved_reviewer=?, approved_audience=?, approved_fields=?, ready=0, preview=NULL WHERE notice_id=?",
                    (row["revision"], actor, EMPLOYEE_AUDIENCE, json.dumps(fields, sort_keys=True), row["notice_id"]))
        return 200, {"status": "HELD", "approved_revision": row["revision"]}

    def _revise(self, con: sqlite3.Connection, row: sqlite3.Row, body: dict | None) -> tuple[int, dict]:
        data = object_fields(body, ("expected_revision", "candidate", "source_facts"), required=("expected_revision", "candidate", "source_facts"))
        require(type(data["expected_revision"]) is int and data["expected_revision"] == row["revision"], 409, "stale_revision")
        candidate = data["candidate"]
        facts = object_fields(data["source_facts"], ALLOWED_SOURCE)
        require(isinstance(candidate, str) and len(candidate) <= 2048, 400, "invalid_candidate")
        require(all(isinstance(v, str) and len(v) <= 256 for v in facts.values()), 400, "invalid_facts")
        con.execute("UPDATE notices SET revision=revision+1, candidate=?, source_facts=?, confirmed_audience=NULL, approved_revision=NULL, approved_reviewer=NULL, approved_audience=NULL, approved_fields=NULL, ready=0, preview=NULL WHERE notice_id=?",
                    (candidate, json.dumps(facts, sort_keys=True), row["notice_id"]))
        return 200, {"revision": row["revision"] + 1, "status": "HELD"}

    def _preview(self, con: sqlite3.Connection, row: sqlite3.Row) -> tuple[int, dict]:
        # No rendering from model candidate; no client-supplied readiness or identity.
        reason = None
        if row["confirmed_audience"] != EMPLOYEE_AUDIENCE:
            reason = "audience_not_confirmed"
        elif (row["approved_revision"] != row["revision"]
              or row["approved_audience"] != EMPLOYEE_AUDIENCE
              or not row["approved_reviewer"] or not row["approved_fields"]):
            reason = "approval_mismatch"
        else:
            fields = json.loads(row["approved_fields"])
            if any(not isinstance(fields.get(k), str) or not fields[k].strip() for k in ALLOWED_FIELDS):
                reason = "incomplete_facts"
        if reason:
            con.execute("UPDATE notices SET ready=0, preview=NULL WHERE notice_id=?", (row["notice_id"],))
            return 200, {"status": "HELD", "reason": reason, "preview": None}
        preview = (f"{fields['service_name']} maintenance is {fields['maintenance_window']}. "
                   f"{fields['employee_action']}")
        con.execute("UPDATE notices SET ready=1, preview=? WHERE notice_id=?", (preview, row["notice_id"]))
        return 200, {"status": "READY", "reason": "approved_employee_facts", "preview": preview}


def make_server(app: PreviewApplication, host: str = "127.0.0.1", port: int = 0) -> ThreadingHTTPServer:
    require(host == "127.0.0.1", 400, "loopback_only")

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: Any) -> None:
            pass  # Do not emit request bodies or credentials through default logging.

        def _handle(self, method: str) -> None:
            body = None
            if method == "POST":
                try:
                    size = int(self.headers.get("Content-Length", "0"))
                    require(0 < size <= 8192, 400, "invalid_length")
                    require(self.headers.get("Content-Type", "").split(";")[0].strip() == "application/json", 400, "invalid_content_type")
                    body = json.loads(self.rfile.read(size).decode("utf-8"))
                    require(isinstance(body, dict), 400, "invalid_json_object")
                except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
                    error = Rejected(400, "invalid_json")
                    status, result = error.status, {"error": error.reason}
                except Rejected as error:
                    status, result = error.status, {"error": error.reason}
                else:
                    status, result = app.dispatch(method, self.path, self.headers.get("Authorization"), body)
            else:
                status, result = app.dispatch(method, self.path, self.headers.get("Authorization"), body)
            payload = json.dumps(result, sort_keys=True, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:
            self._handle("GET")

        def do_POST(self) -> None:
            self._handle("POST")

    return ThreadingHTTPServer((host, port), Handler)

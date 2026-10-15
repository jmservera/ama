"""Quarantine store for imported batches with a human approval gate (ADR 0001, issue #80).

A batch is staged from a clean preview. It becomes live only when a named human
approves it; approving a batch supersedes the previous approved batch of the
same structure. The history (version, source, approval, supersession) is plain
application data and has no AI provider field. SQL is portable to SQL Server:
qmark parameters, explicit insert then update, no upsert keywords, no identity
columns and no engine-specific statements.
"""

import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from .mapping import Preview

SCHEMA = (
    "CREATE TABLE import_batches ("
    "batch_id VARCHAR(36) NOT NULL PRIMARY KEY, structure VARCHAR(64) NOT NULL, "
    "version INT NOT NULL, source_name VARCHAR(260) NOT NULL, "
    "source_sha256 VARCHAR(64) NOT NULL, status VARCHAR(16) NOT NULL, "
    "staged_by VARCHAR(120) NOT NULL, staged_at VARCHAR(32) NOT NULL, decided_by VARCHAR(120), "
    "decided_at VARCHAR(32), decision_note NVARCHAR(400), superseded_by VARCHAR(36), "
    "data_label VARCHAR(32) NOT NULL, UNIQUE (structure, version))",
    "CREATE TABLE import_rows ("
    "batch_id VARCHAR(36) NOT NULL, row_number INT NOT NULL, row_key VARCHAR(120) NOT NULL, "
    "payload NVARCHAR(4000) NOT NULL, problems NVARCHAR(4000) NOT NULL, "
    "PRIMARY KEY (batch_id, row_number))",
)
BLOCKED_APPROVERS = {"", "ai", "assistant", "system"}
DECIDE = (
    "UPDATE import_batches SET status = ?, decided_by = ?, decided_at = ?, decision_note = ? "
    "WHERE batch_id = ? AND status = 'staged'"
)
STAGE_ATTEMPTS = 5
INTEGRITY_ERRORS: tuple[type[BaseException], ...] = (sqlite3.IntegrityError,)


class ImportError_(Exception):
    """A rule of the import gate stopped the action."""


@dataclass
class BatchRecord:
    batch_id: str
    structure: str
    version: int
    source_name: str
    source_sha256: str
    status: str
    staged_by: str
    staged_at: str
    decided_by: str | None
    decided_at: str | None
    decision_note: str | None
    superseded_by: str | None
    data_label: str


COLUMNS = (
    "batch_id, structure, version, source_name, source_sha256, status, staged_by, staged_at, "
    "decided_by, decided_at, decision_note, superseded_by, data_label"
)


def _is_integrity_error(exc: Exception, extra: tuple[type[BaseException], ...]) -> bool:
    """DB-API drivers define IntegrityError separately, so also match it by class name."""
    return isinstance(exc, extra) or any(c.__name__ == "IntegrityError" for c in type(exc).__mro__)


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class QuarantineStore:
    def __init__(
        self,
        conn: sqlite3.Connection,
        data_label: str = "synthetic-demo",
        integrity_errors: tuple[type[BaseException], ...] = INTEGRITY_ERRORS,
    ) -> None:
        self.conn = conn
        self.data_label = data_label
        self.integrity_errors = integrity_errors

    @classmethod
    def in_memory(cls) -> "QuarantineStore":
        store = cls(sqlite3.connect(":memory:"))
        store.create_schema()
        return store

    def create_schema(self) -> None:
        cur = self.conn.cursor()
        for statement in SCHEMA:
            cur.execute(statement)
        self.conn.commit()

    def stage(self, preview: Preview, staged_by: str) -> BatchRecord:
        """Quarantine a preview; conflicts refuse staging and row problems are kept."""
        if not staged_by.strip():
            raise ImportError_("A named person must stage the import.")
        if preview.blocking:
            raise ImportError_("The mapping has conflicts; fix the file and preview again.")
        batch_id = str(uuid.uuid4())
        cur = self.conn.cursor()
        for _ in range(STAGE_ATTEMPTS):
            cur.execute(
                "SELECT COALESCE(MAX(version), 0) FROM import_batches WHERE structure = ?",
                (preview.structure,),
            )
            version = int(cur.fetchone()[0]) + 1
            try:
                cur.execute(
                    f"INSERT INTO import_batches ({COLUMNS}) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, ?)",
                    (
                        batch_id,
                        preview.structure,
                        version,
                        preview.source_name,
                        preview.source_sha256,
                        "staged",
                        staged_by.strip(),
                        _now(),
                        self.data_label,
                    ),
                )
                break
            except Exception as exc:
                if not _is_integrity_error(exc, self.integrity_errors):
                    raise
                self.conn.rollback()
        else:
            raise ImportError_(
                f"Could not allocate a batch version after {STAGE_ATTEMPTS} attempts; "
                "try staging again."
            )
        for r in preview.rows:
            cur.execute(
                "INSERT INTO import_rows (batch_id, row_number, row_key, payload, problems) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    batch_id,
                    r.row,
                    next(iter(r.values.values()), ""),
                    json.dumps(r.values),
                    json.dumps(r.problems),
                ),
            )
        self.conn.commit()
        return self.get(batch_id)

    def get(self, batch_id: str) -> BatchRecord:
        cur = self.conn.cursor()
        cur.execute(f"SELECT {COLUMNS} FROM import_batches WHERE batch_id = ?", (batch_id,))
        row = cur.fetchone()
        if row is None:
            raise KeyError(batch_id)
        return BatchRecord(*row)

    def _problem_count(self, batch_id: str) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT problems FROM import_rows WHERE batch_id = ?", (batch_id,))
        return sum(1 for (p,) in cur.fetchall() if json.loads(p))

    def approve(
        self, batch_id: str, approver: str, note: str = "", accept_row_problems: bool = False
    ) -> BatchRecord:
        """A named human approves a staged batch; rows with problems need explicit acceptance."""
        who = approver.strip()
        if who.lower() in BLOCKED_APPROVERS:
            raise ImportError_("A named human approver is required; automation cannot approve.")
        rec = self.get(batch_id)
        if rec.status != "staged":
            raise ImportError_(f"Only a staged batch can be approved (status is {rec.status}).")
        if rec.staged_by.lower() == who.lower():
            raise ImportError_(
                "The approver must be a different person from the person who staged it."
            )
        if self._problem_count(batch_id) and not accept_row_problems:
            raise ImportError_(
                "Some rows need fixing; fix and re-import, or accept the problems explicitly."
            )
        cur = self.conn.cursor()
        cur.execute(DECIDE, ("approved", who, _now(), note[:400], batch_id))
        if cur.rowcount != 1:
            self.conn.rollback()
            raise ImportError_("The batch was already decided by someone else.")
        cur.execute(
            "SELECT batch_id FROM import_batches "
            "WHERE structure = ? AND status = ? AND batch_id <> ?",
            (rec.structure, "approved", batch_id),
        )
        for (old,) in cur.fetchall():
            cur.execute(
                "UPDATE import_batches SET status = ?, superseded_by = ? "
                "WHERE batch_id = ? AND status = ?",
                ("superseded", batch_id, old, "approved"),
            )
        self.conn.commit()
        return self.get(batch_id)

    def reject(self, batch_id: str, approver: str, note: str = "") -> BatchRecord:
        who = approver.strip()
        if who.lower() in BLOCKED_APPROVERS:
            raise ImportError_("A named human is required to reject.")
        rec = self.get(batch_id)
        if rec.status != "staged":
            raise ImportError_(f"Only a staged batch can be rejected (status is {rec.status}).")
        cur = self.conn.cursor()
        cur.execute(DECIDE, ("rejected", who, _now(), note[:400], batch_id))
        if cur.rowcount != 1:
            self.conn.rollback()
            raise ImportError_("The batch was already decided by someone else.")
        self.conn.commit()
        return self.get(batch_id)

    def rows(self, batch_id: str) -> list[dict[str, str]]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT payload FROM import_rows WHERE batch_id = ? ORDER BY row_number", (batch_id,)
        )
        return [json.loads(p) for (p,) in cur.fetchall()]

    def history(self, structure: str) -> list[BatchRecord]:
        cur = self.conn.cursor()
        cur.execute(
            f"SELECT {COLUMNS} FROM import_batches WHERE structure = ? ORDER BY version",
            (structure,),
        )
        return [BatchRecord(*r) for r in cur.fetchall()]

    def current(self, structure: str) -> BatchRecord | None:
        return next((b for b in reversed(self.history(structure)) if b.status == "approved"), None)

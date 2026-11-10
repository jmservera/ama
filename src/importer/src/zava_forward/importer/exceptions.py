"""Failed-import producer, durable refusal ledger and adapter to the exception queue (#135, FR-029).

A file the importer refuses to stage, or a batch a person rejects, becomes a durable record here and
is routed through the existing core feed into the owned exception queue. Nothing is replayed,
approved or recovered, the source file is only read, and no row or cell value is kept in a reason.
Records carry the synthetic data label. SQL is portable to SQL Server: qmark parameters, an
explicit select then insert, no upsert keywords.
"""

import hashlib
import re
import secrets
import sqlite3
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

from zava_forward.core.exception_feeds import feed_failed_imports
from zava_forward.core.exception_queue import ExceptionQueue, Record

from .mapping import CASE_LIST, MAX_SOURCE_BYTES, Preview, Structure, preview_bytes
from .quarantine import (
    COLUMNS,
    INTEGRITY_ERRORS,
    BatchRecord,
    ImportError_,
    QuarantineStore,
    _is_integrity_error,
)
from .xlsx import WorkbookError

SCHEMA = (
    "CREATE TABLE import_refusals ("
    "ref VARCHAR(330) NOT NULL PRIMARY KEY, source_name VARCHAR(260) NOT NULL, "
    "source_sha256 VARCHAR(64) NOT NULL, structure VARCHAR(64) NOT NULL, "
    "reason NVARCHAR(400) NOT NULL, refused_at VARCHAR(32) NOT NULL, "
    "refused_by VARCHAR(120) NOT NULL, data_label VARCHAR(32) NOT NULL)",
)
REFUSAL_COLUMNS = (
    "ref, source_name, source_sha256, structure, reason, refused_at, refused_by, data_label"
)
UNASSIGNED = "Unassigned (Unknown)"
CONFIGURED_OWNER = "{owner} (configured synthetic demo steward, not a named programme role)"
REASON_MAX = 400
CHUNK = 1024 * 1024
SCAN_VERDICT = re.compile(r"scan: ([a-z_-]{1,24})")
REQUIRED_MISSING = re.compile(r"Required column (.+) is missing")
_TOO_LARGE = WorkbookError("file is too large")
_CHANGED = WorkbookError("the source file changed while it was being read")


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _file_reason(exc: Exception) -> str:
    """A fixed phrase for a refusal; input-controlled text from the error is never copied."""
    if isinstance(exc, OSError):
        return "Refused: the file could not be read."
    text = str(exc)
    if text == "file is too large":
        return "Refused: the file is larger than the import limit."
    if text.startswith("file did not pass the content scan"):
        found = SCAN_VERDICT.search(text)
        verdict = found.group(1) if found else "not clean"
        return f"Refused: the file did not pass the content scan ({verdict})."
    if text.startswith("the source file changed"):
        return "Refused: the source file changed while it was being read."
    if text.startswith("not a valid .xlsx"):
        return "Refused: the file is not a valid .xlsx workbook."
    return "Refused: the workbook failed a structural safety check."


def _conflict_reason(structure: Structure, conflicts: Iterable[str]) -> str:
    """Count conflict kinds, naming only declared fields, so no header or row text is kept."""
    declared = {f.name for f in structure.fields}
    kinds: Counter[str] = Counter()
    missing: list[str] = []
    for text in conflicts:
        found = REQUIRED_MISSING.fullmatch(text)
        if found and found.group(1) in declared:
            missing.append(found.group(1))
        elif text.startswith("Several columns match "):
            kinds["ambiguous column mapping"] += 1
        elif " matches both " in text:
            kinds["one column matching two fields"] += 1
        elif text.startswith("Duplicate "):
            kinds["duplicate key values"] += 1
        elif text.startswith("Sheet ") and text.endswith("is empty or missing"):
            kinds["sheet empty or missing"] += 1
        else:
            kinds["other mapping conflict"] += 1
    parts = [f"required column missing: {', '.join(sorted(set(missing)))}"] if missing else []
    parts += [f"{name} x{n}" if n > 1 else name for name, n in sorted(kinds.items())]
    return f"Refused: mapping conflicts, nothing staged ({'; '.join(parts)})."[:REASON_MAX]


@dataclass(frozen=True)
class Captured:
    """One bounded read of a source. `data` and `digest` are set only for a stable snapshot."""

    data: bytes | None
    digest: str
    identity: str
    reason: str


def _opaque(kind: str, *parts: object) -> str:
    return f"{kind}:{hashlib.sha256('|'.join(map(str, parts)).encode()).hexdigest()[:24]}"


def _capture(path: Path) -> Captured:
    """Read a source once, bounded. The digest is of the bytes read, never of a later reopen.

    When content identity cannot be established (too large, unreadable, changed or growing while
    read) there is no digest. The identity is then an opaque token of the resolved path and file
    state, or a fresh attempt token when even that is unavailable, so unlike files never collide.
    """
    try:
        before = path.stat()
        state = (path.resolve(), before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        if before.st_size > MAX_SOURCE_BYTES:
            return Captured(None, "", _opaque("source", *state), _file_reason(_TOO_LARGE))
        with path.open("rb") as handle:
            data = handle.read(MAX_SOURCE_BYTES + 1)
        after = path.stat()
    except OSError as exc:
        return Captured(None, "", f"source:attempt-{secrets.token_hex(8)}", _file_reason(exc))
    if len(data) > MAX_SOURCE_BYTES:
        return Captured(None, "", _opaque("source", *state), _file_reason(_TOO_LARGE))
    if (after.st_size, after.st_mtime_ns) != (before.st_size, before.st_mtime_ns):
        return Captured(None, "", _opaque("source", *state), _file_reason(_CHANGED))
    return Captured(data, hashlib.sha256(data).hexdigest(), "", "")


@dataclass(frozen=True)
class Refusal:
    ref: str
    source_name: str
    source_sha256: str
    structure: str
    reason: str
    refused_at: str
    refused_by: str
    data_label: str


class RefusalLedger:
    """Durable, idempotent record of refused import files. The first reason for a ref stays."""

    def __init__(
        self,
        conn: sqlite3.Connection,
        data_label: str = "synthetic-demo",
        integrity_errors: tuple[type[BaseException], ...] = INTEGRITY_ERRORS,
    ) -> None:
        self.conn = conn
        self.data_label = data_label
        self.integrity_errors = integrity_errors

    def create_schema(self) -> None:
        cur = self.conn.cursor()
        for statement in SCHEMA:
            cur.execute(statement)
        self.conn.commit()

    def _get(self, ref: str) -> Refusal | None:
        cur = self.conn.cursor()
        cur.execute(f"SELECT {REFUSAL_COLUMNS} FROM import_refusals WHERE ref = ?", (ref,))
        row = cur.fetchone()
        return Refusal(*row) if row else None

    def record(
        self,
        source_name: str,
        source_sha256: str,
        structure: str,
        reason: str,
        refused_by: str,
        identity: str = "",
    ) -> Refusal:
        """`identity` is required when there is no digest: an opaque token, never a file name."""
        if not source_sha256 and not identity:
            raise ImportError_("A refusal needs a content digest or an opaque source identity.")
        ref = f"file:{source_sha256}" if source_sha256 else identity
        existing = self._get(ref)
        if existing is not None:
            return existing
        try:
            self.conn.cursor().execute(
                f"INSERT INTO import_refusals ({REFUSAL_COLUMNS}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    ref,
                    source_name[:260],
                    source_sha256,
                    structure,
                    reason[:REASON_MAX],
                    _now(),
                    refused_by.strip(),
                    self.data_label,
                ),
            )
            self.conn.commit()
        except Exception as exc:
            if not _is_integrity_error(exc, self.integrity_errors):
                raise
            self.conn.rollback()
        stored = self._get(ref)
        if stored is None:
            raise ImportError_("The refusal could not be recorded.")
        return stored

    def all(self) -> list[Refusal]:
        cur = self.conn.cursor()
        cur.execute(
            f"SELECT {REFUSAL_COLUMNS} FROM import_refusals ORDER BY refused_at, ref",
        )
        return [Refusal(*row) for row in cur.fetchall()]


@dataclass
class Submission:
    """Outcome of submitting a file: a staged batch, or a durable refusal and nothing staged."""

    batch: BatchRecord | None = None
    refusal: Refusal | None = None
    preview: Preview | None = None


def submit_file(
    store: QuarantineStore,
    ledger: RefusalLedger,
    path: Path,
    staged_by: str,
    structure: Structure = CASE_LIST,
) -> Submission:
    """Preview and stage a workbook copy, or record why it was refused. The source is only read."""
    who = staged_by.strip()
    if not who:
        raise ImportError_("A named person must stage the import.")
    captured = _capture(path)
    preview: Preview | None = None
    if captured.data is None:
        reason = captured.reason
    else:
        try:
            preview = preview_bytes(path.name, captured.data, structure)
        except WorkbookError as exc:
            reason = _file_reason(exc)
        else:
            if not preview.blocking:
                return Submission(batch=store.stage(preview, who), preview=preview)
            reason = _conflict_reason(structure, preview.conflicts)
    refusal = ledger.record(
        path.name, captured.digest, structure.name, reason, who, captured.identity
    )
    return Submission(refusal=refusal, preview=preview)


def _rejected_batches(store: QuarantineStore) -> list[dict[str, Any]]:
    cur = store.conn.cursor()
    cur.execute(
        f"SELECT {COLUMNS} FROM import_batches WHERE status = 'rejected' "
        "ORDER BY staged_at, batch_id"
    )
    return [asdict(BatchRecord(*row)) for row in cur.fetchall()]


def _feed_name(refusal: Refusal) -> str:
    """The feed keys a refusal by digest, else by name; carry the opaque identity in the name so
    hashless refusals of different sources stay distinct and the item shows no digest."""
    if refusal.source_sha256:
        return refusal.source_name
    return f"{refusal.source_name} (unverified source {refusal.ref})"


def _feed_ref(refusal: Refusal) -> str:
    return f"file:{refusal.source_sha256 or _feed_name(refusal)}"


def _feed_refusals(ledger: RefusalLedger) -> list[dict[str, Any]]:
    return [
        {
            "source_name": _feed_name(r),
            "source_sha256": r.source_sha256,
            "reason": r.reason,
            "at": r.refused_at,
        }
        for r in ledger.all()
    ]


class RefusalTarget(Protocol):
    def record_import_refusals(self, refusals: Iterable[Mapping[str, Any]]) -> dict[str, int]: ...


def transfer(ledger: RefusalLedger, target: RefusalTarget) -> dict[str, int]:
    """Hand a bounded copy of each refused file to the served store, which keeps it durably.

    Only source name (carrying the opaque identity when hashless), digest, reason and time cross.
    Repeating it adds nothing. The ledger and the refused files are only read.
    """
    return target.record_import_refusals(_feed_refusals(ledger))


def feed_inputs(
    store: QuarantineStore, ledger: RefusalLedger
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Rejected batches and refused files in the shapes `feed_failed_imports` reads."""
    return _rejected_batches(store), _feed_refusals(ledger)


@dataclass
class Routing:
    items: list[Record] = field(default_factory=list)
    unrouted: list[str] = field(default_factory=list)
    owner_label: str = UNASSIGNED
    data_label: str = "synthetic-demo"
    structures: dict[str, str] = field(default_factory=dict)


def route(
    queue: ExceptionQueue,
    store: QuarantineStore,
    ledger: RefusalLedger,
    owner: str | None,
) -> Routing:
    """Raise each durable failed import into the queue for a configured data steward.

    With no owner, or one the queue does not accept as a data steward, nothing is raised and the
    count is reported so the failure is not hidden; the owner stays Unassigned (Unknown). Reading
    again raises no duplicate. Nothing is retried, approved or changed.
    """
    batches, refusals = feed_inputs(store, ledger)
    routing = Routing(
        data_label=store.data_label,
        structures={_feed_ref(r): r.structure for r in ledger.all()}
        | {f"batch:{b['batch_id']}": str(b["structure"]) for b in batches},
    )
    count = len(batches) + len(refusals)
    name = (owner or "").strip()
    if not name:
        if count:
            routing.unrouted.append(
                f"{count} failed import(s) are recorded but no data steward is named, so the "
                "owner is Unassigned (Unknown). Nothing is retried."
            )
        return routing
    try:
        routing.items = feed_failed_imports(queue, batches, name, refusals)
    except ValueError:
        routing.unrouted.append(
            f"{count} failed import(s) are recorded but {name} is not a named data steward, so "
            "the owner is Unassigned (Unknown). Nothing is retried."
        )
        return routing
    routing.owner_label = CONFIGURED_OWNER.format(owner=name)
    return routing

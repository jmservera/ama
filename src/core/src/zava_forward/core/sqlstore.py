"""Durable SQL store behind the Store interface.

sqlite3 (standard library) is the development and test driver. The schema is
written so it maps one to one onto Azure SQL (see docs/adrs/0002 and the README):
every mutable row has a row version and a write fails closed when it no longer
matches, the audit ledger is append-only with full content and one chain head,
and no per-process state is needed for correctness. Each request first catches
up from the database change sequence, so several processes can share one
database.

Reads: the case list (filters, search, every sort, totals, ranks, keyset and
offset paging) and the header counts are answered by SQL on indexed derived
columns, and only the page's rows are decoded. The derived `rkey` column is the
ranking policy as a sortable text key (ranking.sql_key), rebuilt when the policy
version changes. Queue membership uses indexed, transactionally maintained
flags beneath a hot ID cache; queue filtering, sorting and ranking stay in memory.
Case detail, the map, statistics, visits and writes still use
the in-memory copy kept in step with the change sequence; the full-list export
and the closed list also fall back to it.
"""
import json
import logging
import os
import sqlite3
import threading
from datetime import datetime

from . import continuity, controls, insights, ledger, projection, ranking, stock, taskqueues
from zava_forward.core.ai import Ai
from .chatthreads import SQLITE_DDL as CHAT_DDL, MEMORY_ADDED as CHAT_MEMORY_ADDED
from .doc_controls import open_scanner
from .documents import open_document_store
from .store import ConflictError, GateError, Store
from .resident_decisions import resident_status

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS staff (email TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS cases (
  id TEXT PRIMARY KEY, rowversion INTEGER NOT NULL DEFAULT 1, seq INTEGER NOT NULL,
  stage TEXT NOT NULL, area TEXT NOT NULL, wave TEXT NOT NULL, owner_code TEXT NOT NULL,
  closed INTEGER NOT NULL, hazard INTEGER NOT NULL, postcode TEXT NOT NULL, address TEXT NOT NULL,
  body TEXT NOT NULL, support INTEGER NOT NULL DEFAULT 0, days INTEGER NOT NULL DEFAULT 0, rkey TEXT NOT NULL DEFAULT '',
  contractor TEXT NOT NULL DEFAULT '', search TEXT NOT NULL DEFAULT '', search_c TEXT NOT NULL DEFAULT '',
  surname TEXT NOT NULL DEFAULT '', last_contact TEXT NOT NULL DEFAULT '0000', next_visit TEXT NOT NULL DEFAULT '9999',
  decision TEXT NOT NULL DEFAULT '', fstatus TEXT NOT NULL DEFAULT '',
  priority_correction INTEGER NOT NULL DEFAULT 0,
  queue_new INTEGER NOT NULL DEFAULT 0, queue_priority INTEGER NOT NULL DEFAULT 0,
  queue_stale INTEGER NOT NULL DEFAULT 0, queue_blocked INTEGER NOT NULL DEFAULT 0,
  queue_overdue INTEGER NOT NULL DEFAULT 0, queue_unowned INTEGER NOT NULL DEFAULT 0);
"""

QUEUE_COLS = tuple(f"queue_{name}" for name, _, _ in taskqueues.DEFINITIONS)

INDEXES = "\n".join(
    f"CREATE INDEX IF NOT EXISTS ix_cases_{col} ON cases ({col}, id);"
    for col in QUEUE_COLS
) + """
CREATE INDEX IF NOT EXISTS ix_cases_filter ON cases (closed, stage, area, wave, owner_code);
CREATE INDEX IF NOT EXISTS ix_cases_owner ON cases (owner_code, closed);
CREATE INDEX IF NOT EXISTS ix_cases_rkey ON cases (closed, rkey, id);
CREATE INDEX IF NOT EXISTS ix_cases_owner_rkey ON cases (owner_code, closed, rkey);
CREATE INDEX IF NOT EXISTS ix_cases_contractor_rkey ON cases (contractor, closed, rkey);
CREATE INDEX IF NOT EXISTS ix_cases_stage_rkey ON cases (closed, stage, rkey);
CREATE INDEX IF NOT EXISTS ix_cases_days ON cases (closed, days DESC, rkey);
CREATE INDEX IF NOT EXISTS ix_cases_open_hazard ON cases (id) WHERE hazard = 1 AND closed = 0;
CREATE INDEX IF NOT EXISTS ix_cases_priority_correction ON cases (priority_correction, id) WHERE priority_correction = 1;
CREATE INDEX IF NOT EXISTS ix_cases_seq ON cases (seq);
CREATE INDEX IF NOT EXISTS ix_cases_postcode ON cases (postcode);
CREATE INDEX IF NOT EXISTS ix_cases_address ON cases (address);
CREATE TABLE IF NOT EXISTS recommendations (
  id TEXT PRIMARY KEY, rowversion INTEGER NOT NULL DEFAULT 1, seq INTEGER NOT NULL,
  user TEXT NOT NULL, body TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS ix_recs_seq ON recommendations (seq);
CREATE TABLE IF NOT EXISTS audit (
  seq INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, who TEXT NOT NULL, action TEXT NOT NULL,
  case_id TEXT NOT NULL, detail TEXT NOT NULL, prev TEXT NOT NULL, hash TEXT NOT NULL UNIQUE);
CREATE INDEX IF NOT EXISTS ix_audit_case ON audit (case_id, seq);
CREATE TABLE IF NOT EXISTS audit_head (id INTEGER PRIMARY KEY CHECK (id = 1), count INTEGER NOT NULL, hash TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit BEGIN SELECT RAISE(ABORT, 'audit ledger is append-only'); END;
CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit BEGIN SELECT RAISE(ABORT, 'audit ledger is append-only'); END;
"""


CASE_COLS = ("stage", "area", "wave", "owner_code", "closed", "hazard", "postcode", "address", "body", "support", "days", "rkey",
             "contractor", "search", "search_c", "surname", "last_contact", "next_visit", "decision", "fstatus", "priority_correction")

SORT_SQL = {"urgent": "rkey", "waiting": "days DESC, rkey", "contact": "last_contact, rkey", "name": "surname, rkey", "visit": "next_visit, rkey"}
FLAG_SQL = {"hazard": "hazard=1", "support": "support=1", "long": f"days>={insights.LONG_WAIT}",
            "nodecision": "decision NOT IN ('Accepted','Declined')",
            "fundingprog": "fstatus IN ('To prepare','Draft ready','Approved','Submitted')", "funding": "fstatus!='Confirmed'"}


class _SyncLock:
    """Re-entrant lock that catches up from the database on entry and tidies up on exit."""

    def __init__(self, store):
        self.store, self.rl, self.tl = store, threading.RLock(), threading.local()

    @property
    def depth(self):
        return getattr(self.tl, "n", 0)

    @depth.setter
    def depth(self, n):
        self.tl.n = n

    def __enter__(self):
        self.rl.acquire()
        self.depth += 1
        if self.depth == 1:
            try:
                self.store._sync()
            except BaseException:
                self.depth -= 1
                self.rl.release()
                raise
        return self

    def __exit__(self, *exc):
        try:
            if self.depth == 1:
                try:
                    self.store._finish()
                except Exception as error:
                    if exc[1] is None:
                        raise
                    exc[1].add_note(
                        f"SQL lock-exit recovery failed ({type(error).__name__}); "
                        "original operation failure retained. "
                        "Reload persisted records before retrying."
                    )
                    logging.getLogger(__name__).exception(
                        "SQL lock-exit recovery failed; original operation failure retained"
                    )
        finally:
            self.depth -= 1
            self.rl.release()
        return False


class SqlStore(Store):
    def __init__(self, data_path, db_path, docs_dir=None, digest_dir=None):
        try:
            self._initialize(data_path, db_path, docs_dir, digest_dir)
        except BaseException as error:
            db = getattr(self, "db", None)
            if db is not None:
                try:
                    db.close()
                except Exception:
                    error.add_note("SQL initialization cleanup failed; check connection ownership.")
                    logging.getLogger(__name__).error("SQL initialization cleanup failed")
            raise

    def _initialize(self, data_path, db_path, docs_dir, digest_dir):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self.dblock = threading.RLock()
        self.local = threading.local()
        self.lock = _SyncLock(self)
        self._open(db_path)
        self._create_schema()
        self._migrate()
        self._migrate_queues()
        self._create_indexes()
        self.docs_dir = docs_dir or os.path.join(os.path.dirname(db_path) or ".", "docs")
        self.docstore = open_document_store(self.docs_dir)
        self.scanner = open_scanner(self.docstore)
        self.digest_dir = digest_dir or os.environ.get("ZF_DIGEST_DIR") or os.path.join(os.path.dirname(db_path) or ".", "digests")
        self.ai = Ai()
        self.ai.gate = lambda task, deployment=None: self.continuity_block(task) or self.release_block(task, deployment)
        self.ai.release = self.release_context
        self.version = 0
        self._briefings = {}
        self._ranks = None
        self._seq = 0
        self.cases, self.staff = {}, {}
        self.data = dict(staff=[], recommendations=[])
        self._rv, self._snap = {}, {}
        self._proc_snap = {}
        self._recs = {}
        self._seed(data_path)
        self._insert_ignore("meta", ["key", "value"], ["as_of", os.environ.get("ZF_AS_OF") or datetime.now().date().isoformat()])
        self.as_of = self.db.execute("SELECT value FROM meta WHERE key='as_of'").fetchone()[0]
        with self.lock:
            self._ensure_queue_membership()

    # ---- dialect hooks (SQLite here; MssqlStore overrides them for Azure SQL)
    dberror = sqlite3.Error
    _epoch_sql = "SELECT (julianday('now')-2440587.5)*86400.0"

    def _add_column_default(self, table, col, sqltype, default):
        """Add a NOT NULL column with a default to an existing table. Names and defaults are module constants, never input."""
        self.db.execute(f"ALTER TABLE {table} ADD COLUMN {col} {sqltype} NOT NULL DEFAULT {default}")

    def _open(self, db_path):
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self.db = sqlite3.connect(db_path, check_same_thread=False, isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA busy_timeout=5000")

    def release_block(self, task, deployment=None):
        """Retained legacy dispatch needs a matching release before any provider call; unconfigured AI never calls out."""
        if not self.ai.configured:
            return None
        _, denied = self.release_assessment(task, deployment)
        if denied:
            with self.lock:
                self.audit("system", "ai_release_denied", "-", denied["reason"])
            return denied["reason"]
        return None

    def release_assessment(self, task, deployment=None):
        from . import assistant_release as rel
        from .ai_registry import LEGACY, legacy_binding, legacy_deployment
        if task not in LEGACY:
            return None, rel.denial("task is not registered", ["registered task"], task)
        binding = legacy_binding(task, self.ai, deployment or legacy_deployment(task, self.ai))
        db = self.assistant_connection()
        try:
            now = float(db.execute(self._epoch_sql).fetchone()[0])
            return rel.assessment(db, f"legacy:{task}", binding, now, live=True)
        finally:
            db.close()

    def release_context(self, task, deployment=None):
        from . import rai_release
        selected, _ = self.release_assessment(task, deployment)
        return rai_release.reference(selected) if selected else None

    def assistant_connection(self):
        """A request/worker owns its connection; inference never owns the Store lock."""
        db = sqlite3.connect(self.db_path, isolation_level=None)
        db.execute("PRAGMA busy_timeout=5000")
        return db

    def _create_schema(self):
        self.db.executescript(SCHEMA)
        for ddl in CHAT_DDL:
            self.db.execute(ddl)
        have = {r[1] for r in self.db.execute("PRAGMA table_info(chat_memory)").fetchall()}
        for c, d in CHAT_MEMORY_ADDED:
            if c not in have:
                self._add_column_default("chat_memory", c, "TEXT", f"'{d}'")

    def _create_indexes(self):
        self.db.executescript(INDEXES)

    def _columns(self):
        return {r[1] for r in self.db.execute("PRAGMA table_info(cases)")}

    def continuity_suspension(self, task):
        """Read the persisted suspension from the database, so another process's suspension is seen without a cache."""
        with self.dblock:
            row = self.db.execute("SELECT value FROM meta WHERE key='continuity'").fetchone()
        return continuity.active(continuity.load(row[0] if row else None), task)

    def _meta_set(self, key, value):
        self.db.execute("INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)", (key, value))

    def _insert_ignore(self, table, cols, vals):
        self.db.execute(f"INSERT OR IGNORE INTO {table} ({', '.join(cols)}) VALUES ({','.join('?' * len(cols))})", vals)

    @staticmethod
    def _contains(col):
        return f"instr({col}, ?) > 0"

    @staticmethod
    def _limit(limit, offset):
        return " LIMIT ? OFFSET ?", [limit, offset]

    # ---- derived columns
    def _migrate(self):
        """Add derived columns to a database made by an earlier slice and rebuild them when missing or when the ranking policy changed."""
        self.db.execute("BEGIN IMMEDIATE")
        try:
            have = self._columns()
            for col in CASE_COLS:
                if col not in have:
                    defaults = {"last_contact": "'0000'", "next_visit": "'9999'", "support": "0", "days": "0", "priority_correction": "0"}
                    self._add_column_default("cases", col, "INTEGER" if col in ("support", "days", "priority_correction") else "TEXT", defaults.get(col, chr(39) * 2))
            want = ranking.CURRENT["version"]
            row = self.db.execute("SELECT value FROM meta WHERE key='rank_policy'").fetchone()
            encoding = self.db.execute("SELECT value FROM meta WHERE key='support_encoding'").fetchone()
            stale = ((row[0] if row else None) != want or (not have >= set(CASE_COLS))
                     or (encoding[0] if encoding else None) != stock.SUPPORT_ENCODING)
            if stale and self.db.execute("SELECT COUNT(*) FROM cases").fetchone()[0]:
                for cid, body in self.db.execute("SELECT id, body FROM cases").fetchall():
                    r = self._row(json.loads(body))
                    self.db.execute("UPDATE cases SET " + ", ".join(f"{c}=?" for c in CASE_COLS) + " WHERE id=?", r[1:] + (cid,))
                self._meta_set("rank_policy", want)
                self._meta_set("support_encoding", stock.SUPPORT_ENCODING)
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    # ---- load and sync
    def _migrate_queues(self):
        """Add flags without certifying default-zero rows as evaluated."""
        self.db.execute("BEGIN IMMEDIATE")
        try:
            have = self._columns()
            missing = set(QUEUE_COLS) - have
            for col in QUEUE_COLS:
                if col in missing:
                    self._add_column_default("cases", col, "INTEGER", "0")
            if missing:
                self._meta_set("queue_context", "")
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def _queue_fingerprint(self):
        return json.dumps(
            [taskqueues.VERSION, self.as_of, controls.today(), ranking.CURRENT,
             taskqueues.MEMBERSHIP_REVISION],
            sort_keys=True,
        )

    def _refresh_queue_membership(self, ids=None):
        """Maintain flags and publish one generation inside the caller's write transaction."""
        fingerprint = self._queue_fingerprint()
        row = self.db.execute("SELECT value FROM meta WHERE key='queue_context'").fetchone()
        if row is None or row[0] != fingerprint:
            ids = None
        if ids is not None and not ids:
            return
        if ids is None:
            rows = self.db.execute("SELECT id, body FROM cases").fetchall()
        else:
            ids = sorted(ids)
            rows = []
            for start in range(0, len(ids), 500):
                batch = ids[start:start + 500]
                marks = ",".join("?" * len(batch))
                rows.extend(self.db.execute(
                    f"SELECT id, body FROM cases WHERE id IN ({marks})", batch
                ).fetchall())
        cases = {cid: json.loads(body) for cid, body in rows}
        selected = list(cases.values())
        data = {}
        for name in ("buildings", "procurement"):
            row = self.db.execute("SELECT value FROM meta WHERE key=?", (name,)).fetchone()
            if row:
                data[name] = json.loads(row[0])
        if ids is not None and any(c.get("building_id") for c in selected):
            # Building validation checks all linked home IDs, not just changed homes.
            cases = {cid: json.loads(body) for cid, body in
                     self.db.execute("SELECT id, body FROM cases").fetchall()}
        values = []
        for c in selected:
            queues = self._work_context(c, None, data, cases)["queues"]
            values.append(tuple(int(col[6:] in queues) for col in QUEUE_COLS) + (c["id"],))
        if values:
            self.db.executemany(
                "UPDATE cases SET " + ", ".join(f"{col}=?" for col in QUEUE_COLS) + " WHERE id=?",
                values,
            )
        if self._queue_fingerprint() != fingerprint:
            raise ConflictError("Queue evaluation inputs changed during refresh.")
        row = self.db.execute("SELECT value FROM meta WHERE key='queue_generation'").fetchone()
        self._meta_set("queue_generation", str(int(row[0]) + 1 if row else 1))
        self._meta_set("queue_context", fingerprint)

    def _ensure_queue_membership(self):
        with self.dblock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                self._refresh_queue_membership([])
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    def _queue_candidates(self, queue):
        """SQL supplies IDs on a miss; permissions and projection remain downstream."""
        taskqueues.validate_queue(queue)
        with self.dblock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                # Synchronise under the same writer lock as the membership generation.
                self._sync()
                self._refresh_queue_membership([])
                generation = self.db.execute(
                    "SELECT value FROM meta WHERE key='queue_generation'"
                ).fetchone()[0]
                key = (self.version, generation, self._queue_fingerprint())
                cached = getattr(self, "_queue_index", None)
                members = cached[1] if cached is not None and cached[0] == key else {}
                if queue not in members:
                    members[queue] = [r[0] for r in self.db.execute(
                        f"SELECT id FROM cases WHERE queue_{queue}=1"
                    ).fetchall()]
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise
            self._queue_index = (key, members)
        return (self.cases[cid] for cid in members[queue])

    def _seed(self, data_path):
        with self.dblock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                if self.db.execute("SELECT COUNT(*) FROM cases").fetchone()[0] == 0:
                    with open(data_path, encoding="utf-8") as f:
                        src = json.load(f)
                    for c in src["cases"]:
                        c.setdefault("documents", [])
                        c.setdefault("funding", dict(route="Not decided", status="Not started", reference="", draft="", approved_by=None))
                    self.db.executemany(f"INSERT INTO cases (id, rowversion, seq, {', '.join(CASE_COLS)}) VALUES (?,1,1,{','.join('?' * len(CASE_COLS))})",
                                        [self._row(c) for c in src["cases"]])
                    self._meta_set("rank_policy", ranking.CURRENT["version"])
                    self._meta_set("support_encoding", stock.SUPPORT_ENCODING)
                    for s in src["staff"]:
                        self._insert_ignore("staff", ("email", "body"), (s["email"].lower(), json.dumps(s)))
                    for doc in self.DOCS:
                        if doc in src:
                            self._meta_set(doc, json.dumps(src[doc]))
                    if src.get("as_of") and not os.environ.get("ZF_AS_OF"):
                        self._meta_set("as_of", src["as_of"])
                    self._insert_ignore("meta", ("key", "value"), ("seq", "1"))
                    self._insert_ignore("audit_head", ("id", "count", "hash"), (1, 0, ledger.GENESIS))
                    self._insert_ignore("meta", ("key", "value"), (
                        "as_of", os.environ.get("ZF_AS_OF") or datetime.now().date().isoformat()
                    ))
                    self.as_of = self.db.execute("SELECT value FROM meta WHERE key='as_of'").fetchone()[0]
                    self._refresh_queue_membership()
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    @staticmethod
    def _row(c):
        nxt = next((a["date"] for a in c["appointments"] if a["outcome"] == "Booked"), None)
        name, home = c["resident"]["name"], c["home"]
        return (c["id"], c["stage"], home["area"], c["wave"], c["owner_code"], int(bool(c["closed"])),
                int(any(not h["released"] for h in c["hazards"])), home["postcode"], home["address"], json.dumps(c),
                int(ranking._support(c)), int(c["days_in_stage"]), ranking.sql_key(c), c["contractor"]["name"],
                " ".join([name, home["address"], home["postcode"], c["id"]]).lower(), " ".join([home["address"], home["postcode"], c["id"]]).lower(),
                name.split(" ")[-1].lower(), (c["contacts"][-1]["at"] if c["contacts"] else None) or "0000", nxt or "9999",
                resident_status(c), c["funding"]["status"],
                int(any((record.get("resolution") or {}).get("outcome") == "Correction recorded"
                        for record in c.get("affected_challenges", []))))

    def _db_seq(self):
        row = self.db.execute("SELECT value FROM meta WHERE key='seq'").fetchone()
        return int(row[0]) if row else 0

    def _sync(self):
        with self.dblock:
            seq = self._db_seq()
            if seq == self._seq and self.cases:
                return
            for cid, rv, body in self.db.execute("SELECT id, rowversion, body FROM cases WHERE seq > ?", (self._seq,)).fetchall():
                self._load_case(cid, rv, body)
            for rid, rv, body in self.db.execute("SELECT id, rowversion, body FROM recommendations WHERE seq > ?", (self._seq,)).fetchall():
                rec = json.loads(body)
                old = self._recs.get(rid)
                if old is not None:
                    old[1].clear()
                    old[1].update(rec)
                    rec = old[1]
                else:
                    self.data["recommendations"].append(rec)
                self._recs[rid] = [rv, rec, body]
            self._proc_sync()
            if not self.staff:
                for (body,) in self.db.execute("SELECT body FROM staff").fetchall():
                    s = json.loads(body)
                    self.staff[s["email"].lower()] = s
                    self.data["staff"].append(s)
            self._seq = seq
            self.version = seq

    def _load_case(self, cid, rv, body):
        c = json.loads(body)
        self.cases[cid] = c
        self._rv[cid] = rv
        self._snap[cid] = body

    def _touched(self):
        if not hasattr(self.local, "touched"):
            self.local.touched, self.local.pending = set(), []
            self.local.safety_clear = set()
            self.local.resident_clear = []
            self.local.stock_clear = set()
        return self.local.touched

    def _touch(self, case_id):
        self._touched().add(case_id)

    def require_safety_clear(self, c):
        super().require_safety_clear(c)
        self._touched()
        self.local.safety_clear.add(c["id"])

    def require_resident_clear(self, c, bindings=None):
        super().require_resident_clear(c, bindings)
        self._touched()
        self.local.resident_clear.append((c["id"], json.loads(json.dumps(bindings))))

    def require_stock_clear(self, c):
        super().require_stock_clear(c)
        self._touched()
        self.local.stock_clear.add(c["id"])

    def _validate_safety_clear(self):
        """Recheck dependent cases under the transaction's cross-process writer lock."""
        for cid in sorted(self.local.safety_clear | self.local.stock_clear):
            row = self.db.execute("SELECT rowversion, body FROM cases WHERE id=?", (cid,)).fetchone()
            if row is None:
                raise ConflictError(cid)
            rv, body = row
            current = json.loads(body)
            if cid in self.local.safety_clear:
                super().require_safety_clear(current)
            if cid in self.local.stock_clear:
                super().require_stock_clear(current)
            if rv != self._rv[cid]:
                raise ConflictError(cid)
        for cid, bindings in self.local.resident_clear:
            row = self.db.execute("SELECT rowversion, body FROM cases WHERE id=?", (cid,)).fetchone()
            if row is None:
                raise ConflictError(cid)
            rv, body = row
            super().require_resident_clear(json.loads(body), bindings)
            if rv != self._rv[cid]:
                raise ConflictError(cid)

    def _finish(self):
        """Outermost lock exit: write audit-only entries, drop unsaved edits."""
        touched = self._touched()
        self.local.safety_clear.clear()
        self.local.resident_clear.clear()
        self.local.stock_clear.clear()
        self.local.procurement_validation = None
        pending = self.local.pending
        if touched:
            with self.dblock:
                for cid in touched:
                    if json.dumps(self.cases[cid]) != self._snap.get(cid):
                        rv, body = self.db.execute("SELECT rowversion, body FROM cases WHERE id=?", (cid,)).fetchone()
                        self._load_case(cid, rv, body)
            touched.clear()
        if pending:
            with self.dblock:
                self.db.execute("BEGIN IMMEDIATE")
                try:
                    self._append_audit(pending)
                    self.db.execute("COMMIT")
                except BaseException:
                    self.db.execute("ROLLBACK")
                    raise
            pending.clear()

    # ---- writes
    def _priority_correction_rows(self):
        rows = self.db.execute("""
            SELECT c.id, json_extract(ch.value, '$.id'), json_extract(ch.value, '$.target')
            FROM cases AS c, json_each(c.body, '$.affected_challenges') AS ch
            WHERE c.priority_correction = 1
              AND json_extract(ch.value, '$.resolution.outcome') = 'Correction recorded'
        """).fetchall()
        return [(cid, rid, json.loads(target)) for cid, rid, target in rows]

    def save(self):
        touched, pending = self._touched(), self.local.pending
        with self.dblock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                from .change_provenance import validate_sql as validate_change
                validate_change(self)
                continuity.validate_sql(self)
                from .bulk_edits import validate_sql
                validate_sql(self)
                stock.validate_sql(self)
                from .hazard import mark_committed, validate_sql as validate_hazard
                validate_hazard(self)
                from .finance import validate_sql as validate_finance
                validate_finance(self)
                from .resident_decisions import validate_sql as validate_resident
                validate_resident(self)
                from .resident_decisions import validate_priority_sql
                validate_priority_sql(self)
                from .procurement import validate_sql as validate_procurement
                validate_procurement(self)
                self._validate_safety_clear()
                cur = self._db_seq()
                new = cur + 1
                changed = []
                for cid in list(touched):
                    c = self.cases[cid]
                    body = json.dumps(c)
                    if body == self._snap.get(cid):
                        continue
                    r = self._row(c)
                    n = self.db.execute("UPDATE cases SET rowversion=rowversion+1, seq=?, " + ", ".join(f"{c}=?" for c in CASE_COLS) +
                                        " WHERE id=? AND rowversion=?", (new,) + r[1:] + (cid, self._rv[cid])).rowcount
                    if n != 1:
                        raise ConflictError(cid)
                    changed.append((cid, body))
                recs = []
                for rid, rec in ((r["id"], r) for r in self.data["recommendations"]):
                    body = json.dumps(rec)
                    known = self._recs.get(rid)
                    if known is None:
                        self.db.execute("INSERT INTO recommendations (id, rowversion, seq, user, body) VALUES (?,1,?,?,?)", (rid, new, rec["user"], body))
                        recs.append((rid, 1, rec, body))
                    elif known[2] != body:
                        if self.db.execute("UPDATE recommendations SET rowversion=rowversion+1, seq=?, body=? WHERE id=? AND rowversion=?",
                                           (new, body, rid, known[0])).rowcount != 1:
                            raise ConflictError(rid)
                        recs.append((rid, known[0] + 1, rec, body))
                proc_body = self._proc_write()
                # Shared validation can change when packages, holds or linked homes change.
                shared = bool({"buildings", "procurement"} & proc_body.keys()) or any(
                    self.cases[cid].get("building_id")
                    or json.loads(self._snap[cid]).get("building_id")
                    for cid, _ in changed
                )
                self._refresh_queue_membership(None if shared else [cid for cid, _ in changed])
                self._append_audit(pending)
                self.db.execute("UPDATE meta SET value=? WHERE key='seq'", (str(new),))
                self.db.execute("COMMIT")
                continuity.mark_committed(self)
                from .governance import mark_committed as governance_committed
                governance_committed(self)
                from .appointments import mark_committed as appointment_committed
                appointment_committed(self)
                from .document_rescan import mark_committed as rescan_committed
                rescan_committed(self)
                mark_committed(self)
                from .resident_decisions import mark_committed as resident_committed
                resident_committed(self)
            except (ConflictError, GateError, PermissionError) as error:
                if (getattr(self.local, "rai_evidence_write", None) or {}).get("persisted"):
                    raise
                self.db.execute("ROLLBACK")
                if (getattr(self.local, "stock_decision", None) is None
                        and getattr(self.local, "hazard_decision", None) is None
                        and getattr(self.local, "resident_validation", None) is None
                        and getattr(self.local, "change_validation", None) is None
                        and getattr(self.local, "document_rescan", None) is None
                        and getattr(self.local, "procurement_validation", None) is None):
                    try:
                        self._discard()
                    except Exception as recovery_error:
                        error.add_note(
                            f"SQL write recovery failed ({type(recovery_error).__name__}); "
                            "original operation failure retained. "
                            "Reload persisted records before retrying."
                        )
                        logging.getLogger(__name__).exception(
                            "SQL write recovery failed; original operation failure retained"
                        )
                raise
            except BaseException:
                context = getattr(self.local, "procurement_validation", None)
                rai = getattr(self.local, "rai_evidence_write", None)
                if not (context and context.get("persisted") or rai and rai.get("persisted")):
                    self.db.execute("ROLLBACK")
                raise
            self._proc_snap.update(proc_body)
            for cid, body in changed:
                self._rv[cid] += 1
                self._snap[cid] = body
            for rid, rv, rec, body in recs:
                self._recs[rid] = [rv, rec, body]
            pending.clear()
            touched.clear()
            self.local.safety_clear.clear()
            self.local.resident_clear.clear()
            self.local.stock_clear.clear()
            self.local.procurement_validation = None
            if cur == self._seq:
                self._seq = new
                self.version = new
            else:
                self._sync()

    def _discard(self, pending=()):
        """Restore snapshots, retain supplied prior audit, then reload persisted records."""
        touched = tuple(self._touched())
        # Quarantine failed writes before any recovery I/O can fail or lock exit can flush.
        self.local.pending[:] = pending
        self._touched().clear()
        self.local.safety_clear.clear()
        self.local.resident_clear.clear()
        self.local.stock_clear.clear()
        self._seq = -1
        for cid in touched:
            self._load_case(cid, self._rv[cid], self._snap[cid])
        recs = [r for r in self.data["recommendations"] if r["id"] in self._recs]
        self.data["recommendations"][:] = recs
        for rid, (rv, rec, body) in self._recs.items():
            rec.clear()
            rec.update(json.loads(body))
        for key, body in self._proc_snap.items():
            if body is None:
                self.data.pop(key, None)
            else:
                self.data[key] = json.loads(body)
        for cid in touched:
            row = self.db.execute("SELECT rowversion, body FROM cases WHERE id=?", (cid,)).fetchone()
            if row:
                self._load_case(cid, row[0], row[1])
        self._proc_sync()
        self._sync()

    # ---- procurement and governance data kept as checked documents
    DOCS = ("procurement", "governance", "continuity", "buildings", "form_schemas", "bulk_edits")

    def _proc_sync(self):
        snapshots, loaded = {}, {}
        for key in self.DOCS:
            row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
            snapshots[key] = row[0] if row else None
            if row:
                loaded[key] = json.loads(row[0])
        for key in self.DOCS:
            if key in loaded:
                self.data[key] = loaded[key]
            else:
                self.data.pop(key, None)
        self._proc_snap = snapshots

    def _proc_write(self):
        """Inside the save transaction: write changed documents, refusing if someone else changed one first."""
        written = {}
        for key in self.DOCS:
            if key not in self.data:
                continue
            body = json.dumps(self.data[key])
            if body == self._proc_snap.get(key):
                continue
            row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
            if (row[0] if row else None) != self._proc_snap.get(key):
                raise ConflictError(key)
            self._meta_set(key, body)
            written[key] = body
        return written

    def _append_audit(self, entries):
        if not entries:
            return
        count, head = self.db.execute("SELECT count, hash FROM audit_head WHERE id=1").fetchone()
        for who, action, case_id, detail, at in entries:
            e = ledger.make_entry(who, action, case_id, detail, head, at)
            self.db.execute("INSERT INTO audit (at, who, action, case_id, detail, prev, hash) VALUES (?,?,?,?,?,?,?)",
                            (e["at"], who, action, case_id, detail, head, e["hash"]))
            head, count = e["hash"], count + 1
        self.db.execute("UPDATE audit_head SET count=?, hash=? WHERE id=1", (count, head))

    def audit(self, who, action, case_id, detail):
        from datetime import datetime
        item = (who, action, str(case_id), str(detail), datetime.now().isoformat(timespec="seconds"))
        if self.lock.depth > 0:
            self._touched()
            self.local.pending.append(item)
            return
        self._audit_immediate(item)

    def _audit_immediate(self, item):
        """Commit one audit-only event independently of a rolled-back document action."""
        with self.dblock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                self._append_audit([item])
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    # ---- ledger
    def audit_entries(self):
        with self.dblock:
            rows = self.db.execute("SELECT at, who, action, case_id, detail, prev, hash FROM audit ORDER BY seq").fetchall()
        for at, who, action, case_id, detail, prev, h in rows:
            yield dict(at=at, who=who, action=action, case=case_id, detail=detail, prev=prev, hash=h)

    def ledger_head(self):
        with self.dblock:
            return tuple(self.db.execute("SELECT count, hash FROM audit_head WHERE id=1").fetchone())

    def ready(self):
        try:
            with self.dblock:
                self._db_seq()
            return True
        except self.dberror:
            return False

    def query_case_ids(self, stage=None, area=None, wave=None, owner_code=None, after=None, limit=50):
        """Indexed SQL filter with keyset paging on the case id. Used by tests and the SQL plan; the API still pages in memory."""
        sql, args = "SELECT id FROM cases WHERE closed=0", []
        for col, val in (("stage", stage), ("area", area), ("wave", wave), ("owner_code", owner_code)):
            if val:
                sql += f" AND {col}=?"
                args.append(val)
        if after:
            sql += " AND id>?"
            args.append(after)
        tail, targs = self._limit(limit, 0)
        with self.dblock:
            return [r[0] for r in self.db.execute(sql + " ORDER BY id" + tail, args + targs).fetchall()]

    # ---- SQL reads
    def _where(self, user, view, q, f):
        where, args = ["closed=0"], []
        for col, key in (("stage", "stage"), ("area", "area"), ("wave", "wave"), ("owner_code", "owner"), ("contractor", "contractor")):
            if f.get(key):
                where.append(f"{col}=?")
                args.append(f[key])
        flag = f.get("flag")
        if flag in FLAG_SQL:
            where.append(FLAG_SQL[flag])
        if projection.is_contractor(user):
            where.append("contractor=?")
            args.append(user.get("contractor") or "")
        elif view == "mine":
            where.append("owner_code=?")
            args.append(user["code"])
        if q:
            where.append(self._contains("search_c" if projection.is_contractor(user) else "search"))
            args.append(q.lower())
        return " AND ".join(where), args

    def page_cases(self, user, view="mine", q="", filters=None, sort="urgent", limit=None, offset=0, after=None):
        """Same result as Store.page_cases, answered by SQL. `after` is a keyset cursor (the last rkey seen) for the default order."""
        # Authority can expire without a row write; never filter current consent on a cached column.
        if limit is None or view == "closed" or (filters or {}).get("flag") == "nodecision" or (filters or {}).get("queue"):
            return super().page_cases(user, view, q, filters, sort, limit, offset, after)
        asked = sort
        if sort not in insights.SORTS:
            sort = "urgent"
        where, args = self._where(user, view, q, filters or {})
        order = SORT_SQL[sort]
        keyset = after if sort == "urgent" and after else None
        with self.lock, self.dblock:
            total = self.db.execute(f"SELECT COUNT(*) FROM cases WHERE {where}", args).fetchone()[0]
            ranked_total = self.db.execute("SELECT COUNT(*) FROM cases WHERE closed=0").fetchone()[0]
            page_where, page_args = (where + " AND rkey>?", args + [keyset]) if keyset else (where, args)
            tail, targs = self._limit(limit, 0 if keyset else offset)
            rows = self.db.execute(f"SELECT id, rkey, body FROM cases WHERE {page_where} ORDER BY {order}{tail}", page_args + targs).fetchall()
            ranks = {}
            if rows:
                marks = ",".join("?" * len(rows))
                ranks = dict(self.db.execute(f"SELECT id, rk FROM (SELECT id, ROW_NUMBER() OVER (ORDER BY rkey) AS rk FROM cases WHERE closed=0) AS r "
                                             f"WHERE id IN ({marks})", [r[0] for r in rows]).fetchall())
        out = []
        for cid, rkey, body in rows:
            c = json.loads(body)
            r = self.summary(c)
            r["rank"], r["reasons"] = ranks[cid], [t for _, t in ranking.reasons(c)]
            if projection.is_contractor(user):
                r.pop("reasons")
                r = projection.contractor_summary(c, r)
            else:
                r["work"] = self.work_context(c, user)
                if not projection.can_see_reason(user) and r["status"].startswith("Waiting on "):
                    r["status"] = "Waiting for the recorded next step"
                if view == "mine":
                    r["focus"] = self.focus(c, user["role"], projection.can_see_reason(user))
            out.append(r)
        nxt = rows[-1][1] if rows and sort == "urgent" and len(rows) == limit else None
        return dict(items=out, total=total, limit=limit, offset=offset, sort=asked, policy_version=ranking.CURRENT["version"],
                    policy_hash=ranking.CURRENT["content_hash"], as_of=self.as_of, ranked_total=ranked_total, next_cursor=nxt)

    def counts(self, user):
        with self.lock, self.dblock:
            mine, hazards = self.db.execute("SELECT COUNT(*), COALESCE(SUM(hazard),0) FROM cases WHERE closed=0 AND owner_code=?", (user["code"],)).fetchone()
            open_ = self.db.execute("SELECT COUNT(*) FROM cases WHERE closed=0").fetchone()[0]
        return dict(mine=mine, hazards=hazards, open=open_)

    def explain(self, sql, args=()):
        with self.dblock:
            return [r[-1] for r in self.db.execute("EXPLAIN QUERY PLAN " + sql, args).fetchall()]

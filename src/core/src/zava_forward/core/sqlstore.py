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
import hashlib
import json
import logging
import os
import sqlite3
import threading
from collections import Counter
from datetime import datetime
from pathlib import Path

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

REC_ORDER_IDS = 100  # identifiers kept per backfill batch record
REC_REVIEW = "3"  # version of the one-time review of every heuristic ordinal (#1292)
SYNC_RETRIES = 8  # bounded retries of an optimistic reload or queue transaction
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
  user TEXT NOT NULL, body TEXT NOT NULL, created_ord INTEGER NOT NULL DEFAULT 0);
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


class SeedMergeError(Exception):
    """A seed merge refused to write; `report` holds counts only."""

    def __init__(self, message, report):
        super().__init__(message)
        self.report = report


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


class CommittedReloadError(RuntimeError):
    """The write committed but the reload afterwards did not settle; the change must not be repeated."""

    committed = True


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
        self._audit_ev = None
        self.digest_dir = digest_dir or os.environ.get("ZF_DIGEST_DIR") or os.path.join(os.path.dirname(db_path) or ".", "digests")
        self._open(db_path)
        self._create_schema()
        self._migrate()
        self._migrate_queues()
        self._create_indexes()
        self._migrate_recommendations()
        self.docs_dir = docs_dir or os.path.join(os.path.dirname(db_path) or ".", "docs")
        self.docstore = open_document_store(self.docs_dir)
        self.scanner = open_scanner(self.docstore)
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
        self._rec_ord = {}
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
        message_cols = {r[1] for r in self.db.execute("PRAGMA table_info(chat_message)").fetchall()}
        if "actor_role" not in message_cols:
            self._add_column_default("chat_message", "actor_role", "TEXT", "''")

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

    def _has_rec_order(self):
        return "created_ord" in {r[1] for r in self.db.execute("PRAGMA table_info(recommendations)")}

    def _create_rec_order_index(self):
        self.db.execute("CREATE INDEX IF NOT EXISTS ix_recs_created_ord ON recommendations (created_ord)")
        self.db.execute("CREATE INDEX IF NOT EXISTS ix_recs_user_ord ON recommendations (user, created_ord)")

    def _migrate_recommendations(self):
        """Give every recommendation an immutable creation ordinal (#1292).

        Adds the column and index, then repairs every zero ordinal through the same fenced path a running store uses
        and reviews a database already backfilled by the earlier candidate."""
        if self._rec_order_pending():
            self._audit_evidence()
        self.db.execute("BEGIN IMMEDIATE")
        try:
            if not self._has_rec_order():
                self._add_column_default("recommendations", "created_ord", "BIGINT", "0")
            self._create_rec_order_index()
            self._adopt_unresolved_index()
            self._review_priority_order()
            new = self._db_seq() + 1
            if self._backfill_zero_ordinals(new):
                self.db.execute("UPDATE meta SET value=? WHERE key='seq'", (str(new),))
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def _meta_value(self, key):
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return None if row is None else row[0]

    def _rec_order_pending(self):
        if not self._has_rec_order():
            return self.db.execute("SELECT 1 FROM recommendations").fetchone() is not None
        return (self.db.execute("SELECT 1 FROM recommendations WHERE created_ord = 0").fetchone() is not None
                or (self._meta_value("rec_order_review") != REC_REVIEW
                    and self.db.execute("SELECT 1 FROM recommendations").fetchone() is not None))

    def _repair_zero_ordinals(self):
        """Fence for mixed-version writers: a zero ordinal is never cached and never followed by a new ordinal.

        A pre-fix writer inserts the column default 0 at any time, including after startup. Repair runs under the same
        write section as every writer and bumps meta seq so running readers reload. The audit evidence is verified before
        the section is entered; only entries appended since are read under it. Failure propagates, so a zero ordinal is
        never served."""
        self._audit_evidence()
        self.db.execute("BEGIN IMMEDIATE")
        try:
            new = self._db_seq() + 1
            if self._backfill_zero_ordinals(new):
                self.db.execute("UPDATE meta SET value=? WHERE key='seq'", (str(new),))
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def _audit_rows(self, after):
        """Audit rows after an audit seq with the head they belong to; retried until no writer interleaved."""
        for _ in range(5):
            before = self.db.execute("SELECT count, hash FROM audit_head WHERE id=1").fetchone()
            rows = self.db.execute("SELECT seq, at, who, action, case_id, detail, prev, hash FROM audit "
                                   "WHERE seq > ? ORDER BY seq", (after,)).fetchall()
            if before is not None and tuple(before) == tuple(self.db.execute(
                    "SELECT count, hash FROM audit_head WHERE id=1").fetchone()):
                return rows, (int(before[0]), before[1])
        raise RuntimeError("The audit ledger kept changing while its creation events were read.")

    @staticmethod
    def _audit_positions(rows):
        found, prefix = {}, "priority_recommendation "
        for seq, _, _, action, _, detail, _, _ in rows:
            if action == "ai_run_end" and detail.startswith(prefix):
                found.setdefault(detail[len(prefix):].split(" ", 1)[0], int(seq))
        return found

    def _audit_evidence(self):
        """Creation events of priority proposals in a verified audit chain, cached per process by chain head.

        Trusted only when the chain verifies from genesis against audit_head and every available independent digest
        and sealed year digest still matches. Unreadable or mismatching digests make the evidence unusable. Later calls
        verify only the entries appended since."""
        with self.dblock:
            head = self.db.execute("SELECT count, hash FROM audit_head WHERE id=1").fetchone()
            cached = self._audit_ev
            if head is None:
                return dict(ok=False, reason="the audit ledger has no head", anchored=False, positions={},
                            key=None, last_seq=0, head=ledger.GENESIS, hashes=[])
            key = (int(head[0]), head[1])
            self._anchor_now = anchor = self._anchor_fingerprint()
            if cached is not None and cached["key"] == key and cached.get("anchor") == anchor:
                return cached
            try:
                digests, years = ledger.read_digests(self.digest_dir), ledger.read_year_digests(self.digest_dir)
            except (OSError, ValueError):
                return self._cache_evidence(dict(ok=False, reason="independent digests are unreadable", anchored=True,
                                                 positions={}, key=key, last_seq=0, head=ledger.GENESIS, hashes=[]))
            anchored = bool(digests or years)
            malformed = self._malformed_anchor(digests, years)
            if malformed or any(h is None for _, h in anchor):
                return self._cache_evidence(dict(ok=False, anchored=anchored, positions={}, key=key, last_seq=0,
                                                 head=ledger.GENESIS, hashes=[],
                                                 reason=malformed or "independent digests are unreadable"))
            if (cached is not None and cached["ok"] and cached["key"][0] < key[0]
                    and cached.get("anchor") == anchor):
                rows, key = self._audit_rows(cached["last_seq"])
                entries = [dict(at=a, who=w, action=ac, case=ci, detail=d, prev=p, hash=h)
                           for _, a, w, ac, ci, d, p, h in rows]
                report = ledger.verify_entries(entries, start=cached["head"])
                hashes = cached["hashes"]
                hashes.extend(e["hash"] for e in entries)
                reason = None
                if not report["intact"] or (cached["key"][0] + len(rows), report["head"]) != key:
                    reason = "the audit chain no longer verifies"
                elif any(d.get("count", 0) > len(hashes) or (d.get("count") and hashes[d["count"] - 1] != d.get("head"))
                         for d in digests):
                    reason = "the chain differs from an independent digest"
                elif any(isinstance(y, dict) and str(y.get("year")) == str(e["at"])[:4] for y in years for e in entries):
                    reason = "the chain differs from a sealed year digest"
                if reason is None:
                    positions = cached["positions"]
                    for rid, pos in self._audit_positions(rows).items():
                        positions.setdefault(rid, pos)
                    return self._cache_evidence(dict(ok=True, reason=None, anchored=anchored, positions=positions, key=key,
                                                     last_seq=int(rows[-1][0]) if rows else cached["last_seq"],
                                                     head=key[1], hashes=hashes))
            rows, key = self._audit_rows(0)
            entries = [dict(at=a, who=w, action=ac, case=ci, detail=d, prev=p, hash=h)
                       for _, a, w, ac, ci, d, p, h in rows]
            report = ledger.verify_entries(entries, digests)
            reason = None
            if report["problem"] is not None:
                reason = "the audit chain is broken"
            elif report["digest_mismatches"]:
                reason = "the chain differs from an independent digest"
            elif (report["entries"], report["head"]) != key:
                reason = "the chain differs from audit_head"
            elif years and not ledger.verify_years(entries, years)["intact"]:
                reason = "the chain differs from a sealed year digest"
            if reason is not None:
                return self._cache_evidence(dict(ok=False, reason=reason, anchored=anchored, positions={}, key=key,
                                                 last_seq=0, head=ledger.GENESIS, hashes=[]))
            return self._cache_evidence(dict(ok=True, reason=None, anchored=anchored, positions=self._audit_positions(rows),
                                             key=key, last_seq=int(rows[-1][0]) if rows else 0, head=key[1],
                                             hashes=[e["hash"] for e in entries]))

    def _anchor_fingerprint(self):
        """Name and content hash of each independent digest file (None when unreadable); any change re-verifies."""
        found = []
        try:
            with os.scandir(self.digest_dir) as entries:
                for e in entries:
                    if e.name.startswith(("digest-", "year-")) and e.name.endswith(".json"):
                        try:
                            with open(e.path, "rb") as f:
                                found.append((e.name, hashlib.sha256(f.read()).hexdigest()))
                        except OSError:
                            found.append((e.name, None))
        except OSError:
            return ()
        return tuple(sorted(found, key=lambda x: x[0]))

    @staticmethod
    def _malformed_anchor(digests, years):
        """A reason when an independent anchor cannot be interpreted; such an anchor is never silently ignored."""
        for d in digests:
            count = d.get("count") if isinstance(d, dict) else None
            if (not isinstance(d, dict) or isinstance(count, bool) or not isinstance(count, int) or count < 1
                    or not isinstance(d.get("head"), str) or not d["head"]
                    or d.get("algorithm", "sha256") != "sha256"):
                return "independent digests are malformed"
        if any(not isinstance(y, dict) or "unreadable" in y for y in years):
            return "independent digests are unreadable"
        return None

    def _cache_evidence(self, evidence):
        evidence["anchor"] = self._anchor_now
        self._audit_ev = evidence
        return evidence

    @staticmethod
    def _contradicted(audited):
        """Unedited rows keep their insertion seq, so audit order and seq order must agree; return the rows that do not."""
        rows = sorted((r for r in audited if r["version"] == 1), key=lambda r: r["pos"])
        low, bad, top = [], set(), 0
        running = float("inf")
        for r in reversed(rows):
            low.append(running)
            running = min(running, r["seq"])
        low.reverse()
        for r, later in zip(rows, low):
            if r["seq"] < top or r["seq"] > later:
                bad.add(r["id"])
            top = max(top, r["seq"])
        return bad

    def _flag_unresolved(self, ids):
        """One meta row per record, written once and read by primary key, so a batch costs only its own flags."""
        for rid in ids:
            if self._meta_value(f"rec_unres:{rid}") is None:
                self._meta_set(f"rec_unres:{rid}", "1")

    def _adopt_unresolved_index(self):
        """Copy the earlier single-list index once into per-record rows; the list itself is left untouched."""
        if self._meta_value("rec_unres_index") is not None:
            return
        row = self._meta_value("rec_order_unresolved")
        try:
            known = json.loads(row) if row else []
        except ValueError:
            known = []
        self._flag_unresolved([rid for rid in known if isinstance(rid, str)])
        self._meta_set("rec_unres_index", "1")

    @staticmethod
    def _sign(a, b):
        return (b > a) - (b < a)

    @classmethod
    def _proven_later(cls, earlier, later):
        """Whether `later` is provably created after `earlier` inside one batch.

        Both rows must be unedited (their insertion seq is intact), carry a trusted audit position, and the audit
        and seq orders must agree and differ. The wall clock proves nothing: it can step back, and ties, edits,
        orphan or missing events leave the pair unproven."""
        if earlier["pos"] is None or later["pos"] is None or earlier["seq"] is None or later["seq"] is None:
            return False
        return cls._sign(earlier["pos"], later["pos"]) > 0 and cls._sign(earlier["seq"], later["seq"]) > 0

    @classmethod
    def _unproven_latest(cls, recs, only=None):
        """Per employee, the newest eligible record if it is not provably later than every other eligible one.

        `recs` are in ordinal order; AI tasks are excluded. Ordinals are never changed. Linear per employee."""
        by = {}
        for r in recs:
            if not r["task"]:
                by.setdefault(r["user"], []).append(r)
        out = []
        for rows in by.values():
            last = rows[-1]
            if only is not None and not only(last):
                continue
            if any(not cls._proven_later(r, last) for r in rows[:-1]):
                out.append(last["id"])
        return out

    def _record_batch(self, detail):
        count = int(self._meta_value("rec_order_batches") or 0) + 1
        self._meta_set(f"rec_order_batch:{count}", json.dumps(detail))
        self._meta_set("rec_order_batches", str(count))

    def _backfill_zero_ordinals(self, seq):
        """Order rows with no ordinal after every existing one; the caller holds the write section and commits (#1292).

        A row with a creation event in verified audit evidence is ordered by that event, which also settles a backward
        wall-clock step, unless its unedited insertion seq contradicts the event. Other rows are ordered by body created
        (seconds), then seq (last write, not creation), then id, and placed among the audited rows by created. Any such
        row that shares a second with another record of the same employee, contradicts its creation event, or follows a
        timestamp inversion is listed in meta rec_order_unresolved for the named data owner; nothing is invented. One
        batch record is written per call and earlier records are never read or rewritten."""
        rows = self.db.execute("SELECT id, seq, user, body, rowversion FROM recommendations WHERE created_ord = 0").fetchall()
        if not rows:
            return 0
        evidence = self._audit_evidence()
        usable = evidence["positions"] if evidence["ok"] else {}
        recs = []
        for rid, rseq, user, body, version in rows:
            rec = json.loads(body)
            recs.append(dict(id=rid, seq=int(rseq) if int(version) == 1 else None, last_write=int(rseq), user=user,
                             created=rec.get("created") or "", task=rec.get("kind") == "ai_task",
                             version=int(version), pos=usable.get(rid)))
        contradicted = self._contradicted([r for r in recs if r["pos"] is not None and r["seq"] is not None])
        for r in recs:
            if r["id"] in contradicted:
                r["pos"] = None
        audited = sorted((r for r in recs if r["pos"] is not None), key=lambda r: r["pos"])
        rest = sorted((r for r in recs if r["pos"] is None), key=lambda r: (r["created"], r["last_write"], r["id"]))
        inversions = sum(1 for a, b in zip(audited, audited[1:]) if a["created"] > b["created"])
        keyed, i, j = [], 0, 0
        while i < len(audited) and j < len(rest):
            if rest[j]["created"] < audited[i]["created"]:
                keyed.append(rest[j])
                j += 1
            else:
                keyed.append(audited[i])
                i += 1
        keyed += audited[i:] + rest[j:]
        start = int(self.db.execute("SELECT COALESCE(MAX(created_ord), 0) FROM recommendations").fetchone()[0])
        self.db.executemany("UPDATE recommendations SET created_ord=?, seq=? WHERE id=?",
                            [(n, seq, r["id"]) for n, r in enumerate(keyed, start + 1)])
        sizes = Counter((r["user"], r["created"]) for r in recs if not r["task"])
        ambiguous = self._ambiguous_latest(keyed, start)
        groups = sum(1 for n in sizes.values() if n > 1)
        self._flag_unresolved(ambiguous)
        self._record_batch(dict(
            source="repair", at=datetime.now().isoformat(timespec="seconds"), rows=len(keyed), first_ord=start + 1,
            last_ord=start + len(keyed), audited=len(audited), corroborated=sum(1 for r in audited if r["version"] == 1),
            audit_only=sum(1 for r in audited if r["version"] > 1), heuristic=len(rest), contradicted=len(contradicted),
            same_second_groups=groups, timestamp_inversions=inversions, ambiguous_total=len(ambiguous),
            ambiguous_ids=ambiguous[:REC_ORDER_IDS], audit_chain=evidence["ok"], audit_reason=evidence["reason"],
            anchored=evidence["anchored"], order="audit position, then created, seq and id for rows without evidence"))
        if start == 0 and self._meta_value("rec_order_legacy") is None:
            self._meta_set("rec_order_legacy", json.dumps(dict(rows=len(keyed), same_second_groups=groups,
                                                               order="created,seq,id")))
        return len(keyed)

    def _ambiguous_latest(self, keyed, start):
        """Per employee of a batch, the batch's newest eligible record when it is not provably the latest.

        Every row that already had an ordinal committed before this repair, because save and sync repair before they
        publish, so a provably ordered batch follows them provided that employee's previous newest record is not
        itself unresolved. Within the batch every other row must be provably earlier. Only a small page of the
        employee's newest rows is read, never the whole history."""
        by = {}
        for r in keyed:
            if not r["task"]:
                by.setdefault(r["user"], []).append(r)
        out = []
        for user, rows in by.items():
            last = rows[-1]
            if any(not self._proven_later(r, last) for r in rows[:-1]) or self._previous_unresolved(user, start):
                out.append(last["id"])
        return out

    def _previous_unresolved(self, user, start):
        """Whether the employee's newest eligible record before this batch is unresolved (indexed, paged by ordinal)."""
        if start == 0:
            return False
        page, offset = 5, 0
        while True:
            tail, args = self._limit(page, offset)
            rows = self.db.execute("SELECT id, body FROM recommendations WHERE user=? AND created_ord BETWEEN 1 AND ? "
                                   "ORDER BY created_ord DESC" + tail, [user, start] + args).fetchall()
            for rid, body in rows:
                if json.loads(body).get("kind") != "ai_task":
                    return self._meta_value(f"rec_unres:{rid}") is not None
            if len(rows) < page:
                return False
            offset += page

    def _suspect_ranges(self):
        """Coalesced ordinal ranges assigned by a heuristic backfill rather than at insert, from every known format.

        Reads the earlier candidates' single legacy row, the C1 list rec_order_backfills and the per-batch rows in one
        query. Anything unreadable makes every ordinal suspect; no history is trusted by default."""
        everything, ranges = (1, 1 << 62), []

        def span(entry):
            lo, hi = entry["first_ord"], entry["last_ord"]
            if (not all(isinstance(v, int) and not isinstance(v, bool) for v in (lo, hi)) or lo < 1 or hi < lo):
                raise ValueError
            return lo, hi

        present = self.db.execute("SELECT value FROM meta WHERE key='rec_order_legacy'").fetchone()
        if present is not None:
            # The producer writes an object with a positive integer row count; anything else is unreadable.
            try:
                entry = json.loads(present[0])
                legacy = entry["rows"] if isinstance(entry, dict) else None
                if not isinstance(legacy, int) or isinstance(legacy, bool) or legacy < 1:
                    raise ValueError
            except (ValueError, TypeError, KeyError):
                return [everything]
            ranges.append((1, legacy))
        try:
            raw = self._meta_value("rec_order_backfills")
            for entry in json.loads(raw) if raw else []:
                ranges.append(span(entry))
        except (ValueError, TypeError, KeyError, AttributeError):
            return [everything]
        for (value,) in self.db.execute("SELECT value FROM meta WHERE key LIKE 'rec_order_batch:%'").fetchall():
            try:
                batch = json.loads(value or "{}")
                if batch.get("ordinals_changed") is not False:
                    ranges.append(span(batch))
            except (ValueError, TypeError, KeyError, AttributeError):
                return [everything]
        merged = []
        for lo, hi in sorted(ranges):
            if merged and lo <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
            else:
                merged.append((lo, hi))
        return merged

    def _review_priority_order(self):
        """Once, assess every heuristic ordinal of earlier candidates without changing any, whatever batch metadata exists.

        The newest eligible record of each employee that is not provably later than that employee's other records is
        listed for the named data owner; the seq column is not used because these rows were restamped by backfill."""
        if self._meta_value("rec_order_review") == REC_REVIEW:
            return
        ranges = self._suspect_ranges()
        rows = self.db.execute("SELECT id, user, body, created_ord FROM recommendations WHERE created_ord > 0 "
                               "ORDER BY created_ord").fetchall()
        evidence = self._audit_evidence()
        usable = evidence["positions"] if evidence["ok"] else {}
        suspect, recs, at = set(), [], 0
        for rid, user, body, ordinal in rows:
            rec = json.loads(body)
            while at < len(ranges) and ranges[at][1] < ordinal:
                at += 1
            if at < len(ranges) and ranges[at][0] <= ordinal:
                suspect.add(rid)
            recs.append(dict(id=rid, user=user, task=rec.get("kind") == "ai_task", created=rec.get("created") or "",
                             pos=usable.get(rid), seq=None))
        flagged = self._unproven_latest(recs, only=lambda r: r["id"] in suspect)
        self._flag_unresolved(flagged)
        if rows:
            self._record_batch(dict(
                source="review", at=datetime.now().isoformat(timespec="seconds"), rows=len(rows), first_ord=1,
                last_ord=int(rows[-1][3]), heuristic=len(suspect), ambiguous_total=len(flagged),
                ambiguous_ids=flagged[:REC_ORDER_IDS], audit_chain=evidence["ok"], audit_reason=evidence["reason"],
                anchored=evidence["anchored"], ordinals_changed=False,
                order="existing ordinals kept; the newest record of an employee not provably latest is listed"))
        self._meta_set("rec_order_review", REC_REVIEW)

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
            for _ in range(SYNC_RETRIES):
                # Synchronise before the transaction so no cache state is ever published from uncommitted SQL.
                self._sync()
                self.db.execute("BEGIN IMMEDIATE")
                try:
                    if self._db_seq() != self._seq:
                        self.db.execute("ROLLBACK")
                        continue
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
                break
            else:
                raise RuntimeError("Queue lookup could not settle against concurrent writers; retry.")
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

    MERGE_PRESERVED_DOCS = ("continuity",)
    MERGE_BATCH = 50

    def merge_seed(self, data_path, *, apply=False, expect_added=None, actor="seed-merge"):
        """Insert-only merge of a generated seed into a populated database; returns counts only.

        One transaction. A case id already stored with identical content is skipped and one with different content aborts
        the merge. A missing document key is inserted, an identical one skipped, a different one aborts unless it is in
        MERGE_PRESERVED_DOCS (kept and reported). Nothing is updated or deleted, staff, as_of and recommendations are untouched,
        and one audit entry is appended only when something is inserted. Every guard is recomputed here under the write lock,
        so a dry run (apply=False) is advisory and writes nothing. expect_added aborts before any write on a mismatch."""
        import hashlib
        raw = Path(data_path).read_bytes()
        src = json.loads(raw)
        canon = lambda v: json.dumps(v, sort_keys=True)  # noqa: E731
        cases = src["cases"]
        for c in cases:
            c.setdefault("documents", [])
            c.setdefault("funding", dict(route="Not decided", status="Not started", reference="", draft="", approved_by=None))
        report = dict(seed_cases=len(cases), existing_cases=0, to_insert=0, identical=0, conflicts=0,
                      docs_inserted=[], docs_identical=[], docs_preserved=[], seed_as_of=src.get("as_of"),
                      store_as_of=None, applied=False, audit_appended=False)
        with self.dblock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                rows = self.db.execute("SELECT at, who, action, case_id, detail, prev, hash FROM audit ORDER BY seq").fetchall()
                chain = ledger.verify_entries([dict(at=a, who=w, action=ac, case=ci, detail=d, prev=p, hash=h)
                                               for a, w, ac, ci, d, p, h in rows])
                head = self.db.execute("SELECT count, hash FROM audit_head WHERE id=1").fetchone()
                if not chain["intact"] or (chain["entries"], chain["head"]) != (head[0], head[1]):
                    raise SeedMergeError("Audit chain does not match its head; nothing was written.", report)
                stored = {cid: body for cid, body in self.db.execute("SELECT id, body FROM cases").fetchall()}
                report["existing_cases"] = len(stored)
                new_cases = []
                for c in cases:
                    body = stored.get(c["id"])
                    if body is None:
                        new_cases.append(c)
                    elif canon(json.loads(body)) == canon(c):
                        report["identical"] += 1
                    else:
                        report["conflicts"] += 1
                report["to_insert"] = len(new_cases)
                if len({c["id"] for c in cases}) != len(cases):
                    raise SeedMergeError("Seed contains duplicate case ids; nothing was written.", report)
                for key in self.DOCS:
                    if key not in src:
                        continue
                    row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
                    if row is None:
                        report["docs_inserted"].append(key)
                    elif canon(json.loads(row[0])) == canon(src[key]):
                        report["docs_identical"].append(key)
                    elif key in self.MERGE_PRESERVED_DOCS:
                        report["docs_preserved"].append(key)
                    else:
                        report["conflicts"] += 1
                report["store_as_of"] = self.db.execute("SELECT value FROM meta WHERE key='as_of'").fetchone()[0]
                if report["conflicts"]:
                    raise SeedMergeError("Seed conflicts with stored content; nothing was written.", report)
                if expect_added is not None and report["to_insert"] != expect_added:
                    raise SeedMergeError("Cases to add differ from the expected count; nothing was written.", report)
                report["total_after"] = report["existing_cases"] + report["to_insert"]
                if apply and (new_cases or report["docs_inserted"]):
                    new = self._db_seq() + 1
                    for start in range(0, len(new_cases), self.MERGE_BATCH):
                        self.db.executemany(
                            f"INSERT INTO cases (id, rowversion, seq, {', '.join(CASE_COLS)}) VALUES (?,1,?,{','.join('?' * len(CASE_COLS))})",
                            [(r[0], new) + r[1:] for r in map(self._row, new_cases[start:start + self.MERGE_BATCH])])
                    for key in report["docs_inserted"]:
                        self._meta_set(key, json.dumps(src[key]))
                    self._refresh_queue_membership(None)
                    detail = (f"cases_added={len(new_cases)}; docs_added={','.join(report['docs_inserted']) or 'none'}; "
                              f"seed_sha256={hashlib.sha256(raw).hexdigest()}")
                    self._append_audit([(actor, "seed_merge", "-", detail, datetime.now().isoformat(timespec="seconds"))])
                    self.db.execute("UPDATE meta SET value=? WHERE key='seq'", (str(new),))
                    self.db.execute("COMMIT")
                    report.update(applied=True, audit_appended=True)
                else:
                    self.db.execute("ROLLBACK")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise
        return report

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
        """Reload changed rows from one interleaving-free read.

        Every writer, old or new, bumps meta seq in the same atomic commit as its rows, so a fetch bracketed by two equal
        sequence reads saw no commit. A fetched zero ordinal is repaired under the writer lock and the read retried, so
        no zero ordinal is ever cached or published."""
        with self.dblock:
            for _ in range(SYNC_RETRIES):
                seq = self._db_seq()
                if seq == self._seq and self.cases:
                    return
                changed = self.db.execute("SELECT id, rowversion, body FROM cases WHERE seq > ?", (self._seq,)).fetchall()
                recs = self.db.execute(
                    "SELECT id, rowversion, body, created_ord FROM recommendations WHERE seq > ? ORDER BY created_ord, id",
                    (self._seq,)).fetchall()
                if self._db_seq() != seq:
                    continue
                if any(int(r[3]) == 0 for r in recs):
                    self._repair_zero_ordinals()
                    continue
                for cid, rv, body in changed:
                    self._load_case(cid, rv, body)
                for rid, rv, body, created_ord in recs:
                    self._rec_ord[rid] = int(created_ord)
                    rec = json.loads(body)
                    old = self._recs.get(rid)
                    if old is not None:
                        old[1].clear()
                        old[1].update(rec)
                        rec = old[1]
                    else:
                        self.data["recommendations"].append(rec)
                    self._recs[rid] = [rv, rec, body]
                if recs:
                    self._order_recs()
                self._proc_sync()
                if not self.staff:
                    for (body,) in self.db.execute("SELECT body FROM staff").fetchall():
                        s = json.loads(body)
                        self.staff[s["email"].lower()] = s
                        self.data["staff"].append(s)
                self._seq = seq
                self.version = seq
                return
            raise RuntimeError("Reload could not settle against concurrent writers; retry.")

    def _order_recs(self):
        """Keep the cached list in persisted creation order; edits never move a row and unsaved rows stay last."""
        end = float("inf")
        self.data["recommendations"].sort(key=lambda r: self._rec_ord.get(r["id"], end))

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
            try:
                self.db.execute("BEGIN IMMEDIATE")
            except BaseException:
                self._drop_unsaved_recommendations()
                raise
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
                recs, new_ord, top = [], {}, None
                for rid, rec in ((r["id"], r) for r in self.data["recommendations"]):
                    body = json.dumps(rec)
                    known = self._recs.get(rid)
                    if known is None:
                        if top is None:
                            self._backfill_zero_ordinals(new)
                            top = int(self.db.execute("SELECT COALESCE(MAX(created_ord), 0) FROM recommendations").fetchone()[0])
                        top += 1
                        self.db.execute("INSERT INTO recommendations (id, rowversion, seq, user, body, created_ord) VALUES (?,1,?,?,?,?)",
                                        (rid, new, rec["user"], body, top))
                        new_ord[rid] = top
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
                self._drop_unsaved_recommendations()
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
                    self._drop_unsaved_recommendations()
                raise
            self._proc_snap.update(proc_body)
            for cid, body in changed:
                self._rv[cid] += 1
                self._snap[cid] = body
            for rid, rv, rec, body in recs:
                self._recs[rid] = [rv, rec, body]
            if new_ord:
                self._rec_ord.update(new_ord)
                self._order_recs()
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
                try:
                    self._sync()
                except RuntimeError as error:
                    self._seq = -1
                    raise CommittedReloadError(
                        "The change was saved, but the refresh afterwards did not settle. Reload before doing "
                        "anything else; do not repeat the change."
                    ) from error

    def _drop_unsaved_recommendations(self):
        """A rolled-back save must neither keep its new recommendations for a later save nor flush their creation events."""
        recs = self.data["recommendations"]
        unsaved = {r["id"] for r in recs if r["id"] not in self._recs}
        if not unsaved:
            return
        recs[:] = [r for r in recs if r["id"] in self._recs]
        pending = self.local.pending

        def creation_event(entry):
            words = entry[3].split(" ", 2)
            return entry[1] in ("ai_run_end", "ai_record") and len(words) > 1 and words[1] in unsaved

        pending[:] = [p for p in pending if not creation_event(p)]

    def rec_order_unresolved(self, rec_id):
        with self.dblock:
            row = self.db.execute("SELECT 1 FROM meta WHERE key=?", (f"rec_unres:{rec_id}",)).fetchone()
        return row is not None

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
    DOCS = ("procurement", "governance", "continuity", "buildings", "schemes", "form_schemas", "bulk_edits")

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

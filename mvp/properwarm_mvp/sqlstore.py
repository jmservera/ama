"""Durable SQL store behind the Store interface.

sqlite3 (standard library) is the development and test driver. The schema is
written so it maps one to one onto Azure SQL (see docs/adrs/0002 and the README):
every mutable row has a row version and a write fails closed when it no longer
matches, the audit ledger is append-only with full content and one chain head,
and no per-process state is needed for correctness. Each request first catches
up from the database change sequence, so several processes can share one
database. Case reads still go through an in-memory copy kept in step with that
sequence; the indexes serve the SQL filter queries and the 60,000-home plan.
"""
import json
import os
import sqlite3
import threading

from . import ledger
from .ai import Ai
from .documents import open_document_store
from .store import ConflictError, Store

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS staff (email TEXT PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS cases (
  id TEXT PRIMARY KEY, rowversion INTEGER NOT NULL DEFAULT 1, seq INTEGER NOT NULL,
  stage TEXT NOT NULL, area TEXT NOT NULL, wave TEXT NOT NULL, owner_code TEXT NOT NULL,
  closed INTEGER NOT NULL, hazard INTEGER NOT NULL, postcode TEXT NOT NULL, address TEXT NOT NULL,
  body TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS ix_cases_filter ON cases (closed, stage, area, wave, owner_code);
CREATE INDEX IF NOT EXISTS ix_cases_owner ON cases (owner_code, closed);
CREATE INDEX IF NOT EXISTS ix_cases_open_hazard ON cases (id) WHERE hazard = 1 AND closed = 0;
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
                self.store._finish()
        finally:
            self.depth -= 1
            self.rl.release()
        return False


class SqlStore(Store):
    def __init__(self, data_path, db_path, docs_dir=None, digest_dir=None):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self.db = sqlite3.connect(db_path, check_same_thread=False, isolation_level=None)
        self.dblock = threading.RLock()
        self.local = threading.local()
        self.lock = _SyncLock(self)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA busy_timeout=5000")
        self.db.executescript(SCHEMA)
        self.docs_dir = docs_dir or os.path.join(os.path.dirname(db_path) or ".", "docs")
        self.docstore = open_document_store(self.docs_dir)
        self.digest_dir = digest_dir or os.environ.get("PW_DIGEST_DIR") or os.path.join(os.path.dirname(db_path) or ".", "digests")
        self.ai = Ai()
        self.version = 0
        self._briefings = {}
        self._ranks = None
        self._seq = 0
        self.cases, self.staff = {}, {}
        self.data = dict(staff=[], recommendations=[])
        self._rv, self._snap = {}, {}
        self._recs = {}
        self._seed(data_path)
        with self.lock:
            pass

    # ---- load and sync
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
                    self.db.executemany("INSERT INTO cases (id, rowversion, seq, stage, area, wave, owner_code, closed, hazard, postcode, address, body)"
                                        " VALUES (?,1,1,?,?,?,?,?,?,?,?,?)", [self._row(c) for c in src["cases"]])
                    self.db.executemany("INSERT OR IGNORE INTO staff (email, body) VALUES (?,?)",
                                        [(s["email"].lower(), json.dumps(s)) for s in src["staff"]])
                    self.db.execute("INSERT OR IGNORE INTO meta (key, value) VALUES ('seq', '1')")
                    self.db.execute("INSERT OR IGNORE INTO audit_head (id, count, hash) VALUES (1, 0, ?)", (ledger.GENESIS,))
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    @staticmethod
    def _row(c):
        return (c["id"], c["stage"], c["home"]["area"], c["wave"], c["owner_code"], int(bool(c["closed"])),
                int(any(not h["released"] for h in c["hazards"])), c["home"]["postcode"], c["home"]["address"], json.dumps(c))

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
        return self.local.touched

    def _touch(self, case_id):
        self._touched().add(case_id)

    def _finish(self):
        """Outermost lock exit: write audit-only entries, drop unsaved edits."""
        touched = self._touched()
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
    def save(self):
        touched, pending = self._touched(), self.local.pending
        with self.dblock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                cur = self._db_seq()
                new = cur + 1
                changed = []
                for cid in list(touched):
                    c = self.cases[cid]
                    body = json.dumps(c)
                    if body == self._snap.get(cid):
                        continue
                    r = self._row(c)
                    n = self.db.execute("UPDATE cases SET rowversion=rowversion+1, seq=?, stage=?, area=?, wave=?, owner_code=?, closed=?, hazard=?,"
                                        " postcode=?, address=?, body=? WHERE id=? AND rowversion=?",
                                        (new,) + r[1:] + (cid, self._rv[cid])).rowcount
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
                self._append_audit(pending)
                self.db.execute("UPDATE meta SET value=? WHERE key='seq'", (str(new),))
                self.db.execute("COMMIT")
            except ConflictError:
                self.db.execute("ROLLBACK")
                self._discard()
                raise
            except BaseException:
                self.db.execute("ROLLBACK")
                raise
            for cid, body in changed:
                self._rv[cid] += 1
                self._snap[cid] = body
            for rid, rv, rec, body in recs:
                self._recs[rid] = [rv, rec, body]
            pending.clear()
            touched.clear()
            if cur == self._seq:
                self._seq = new
                self.version = new
            else:
                self._sync()

    def _discard(self):
        """After a refused write: forget local edits and reload from the database."""
        for cid in list(self._touched()):
            row = self.db.execute("SELECT rowversion, body FROM cases WHERE id=?", (cid,)).fetchone()
            if row:
                self._load_case(cid, row[0], row[1])
        recs = [r for r in self.data["recommendations"] if r["id"] in self._recs]
        self.data["recommendations"][:] = recs
        for rid, (rv, rec, body) in self._recs.items():
            rec.clear()
            rec.update(json.loads(body))
        self._touched().clear()
        self.local.pending.clear()
        self._sync()

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
                self.db.execute("SELECT 1 FROM meta LIMIT 1").fetchone()
            return True
        except sqlite3.Error:
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
        sql += " ORDER BY id LIMIT ?"
        with self.dblock:
            return [r[0] for r in self.db.execute(sql, args + [limit]).fetchall()]

    def explain(self, sql, args=()):
        with self.dblock:
            return [r[-1] for r in self.db.execute("EXPLAIN QUERY PLAN " + sql, args).fetchall()]

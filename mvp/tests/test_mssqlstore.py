"""The SQL store behaviour suites again, against a real SQL Server or Azure SQL.

Skipped unless ZF_TEST_MSSQL=1 and the ZF_SQL_* settings point at a database that may be wiped
(the CI job uses a throwaway SQL Server container; never point this at the pilot database).
"""
import os
import re
import tempfile
import unittest
from pathlib import Path

import test_mvp
import test_sqlreads as reads
import test_sqlstore as base
from zavaforward_mvp.sqlstore import SqlStore

ON = os.environ.get("ZF_TEST_MSSQL") == "1"
TABLES = ("assistant_events", "assistant_attempts", "assistant_tasks", "assistant_allowance", "audit_head", "audit", "recommendations", "cases", "staff", "meta")


def wipe():
    from zavaforward_mvp.mssqlstore import _Conn, connection_string
    c = _Conn(connection_string())
    c.execute("IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only")
    for t in TABLES:
        c.execute(f"IF OBJECT_ID(N'{t}', N'U') IS NOT NULL DROP TABLE {t}")


def factory(data, db, *a, **k):
    from zavaforward_mvp.mssqlstore import MssqlStore
    return MssqlStore(data, state_dir=os.path.dirname(db))


class _Recorder:
    """Wraps the SQLite connection and records every statement the shared store logic sends."""

    def __init__(self, db, log):
        self._db, self._log = db, log

    def execute(self, sql, args=()):
        self._log.append(sql)
        return self._db.execute(sql, args)

    def __getattr__(self, name):
        return getattr(self._db, name)


class SharedSqlIsPortableTests(unittest.TestCase):
    """Runs without a server: SQLite-only upsert syntax must live only in the dialect hooks MssqlStore overrides."""

    SQLITE_ONLY = re.compile(r"(?i)\bINSERT\s+OR\s+(REPLACE|IGNORE)\b|\bREPLACE\s+INTO\b")

    def test_save_paths_use_dialect_hooks_for_upserts(self):
        log = []

        class Probe(SqlStore):
            def _meta_set(self, key, value):
                self.db.execute("UPDATE meta SET value=? WHERE key=?", (value, key))
                self.db.execute("INSERT INTO meta (key, value) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM meta WHERE key=?)", (key, value, key))

        with tempfile.TemporaryDirectory() as tmp:
            data, db = base.seed(tmp)
            store = Probe(data, db)
            store.db = _Recorder(store.db, log)
            sam = test_mvp.DATA["staff"][0]
            store.log_call(sam, "ZF-1", "Contacted", "ok")
            store.set_decision(sam, "ZF-1", "Accepted")
            store.data.setdefault("procurement", {"packages": [], "work_orders": []})
            store.data["procurement"]["packages"].append({"id": "PKG-PORTABLE"})
            store.save()
            store.db.close()
        self.assertTrue(log)
        self.assertEqual([q for q in log if self.SQLITE_ONLY.search(q)], [])

    def test_sqlite_only_syntax_confined_to_dialect_hooks(self):
        for name in ("sqlstore.py", "assistants.py"):
            src = (Path(__file__).resolve().parent.parent / "zavaforward_mvp" / name).read_text()
            hook = None
            for line in src.splitlines():
                m = re.match(r"\s*def (\w+)", line)
                hook = m.group(1) if m else hook
                if self.SQLITE_ONLY.search(line):
                    self.assertIn(hook, ("_meta_set", "_insert_ignore"), f"{name}: SQLite-only SQL in {hook}: {line.strip()}")


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlImproveTests(base.SqlImproveTests):
    @classmethod
    def setUpClass(cls):
        cls._orig, base.SqlStore = base.SqlStore, factory

    @classmethod
    def tearDownClass(cls):
        base.SqlStore = cls._orig

    def setUp(self):
        wipe()
        super().setUp()


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlStoreTests(base.SqlStoreTests):
    @classmethod
    def setUpClass(cls):
        cls._orig, base.SqlStore = base.SqlStore, factory

    @classmethod
    def tearDownClass(cls):
        base.SqlStore = cls._orig

    def setUp(self):
        wipe()
        super().setUp()

    def test_ledger_is_append_only_and_detects_tampering(self):
        from zavaforward_mvp.mssqlstore import _Conn, connection_string
        s = factory(self.data, self.db)
        s.log_call(self.sam, "ZF-1", "Contacted", "")
        s.log_call(self.sam, "ZF-1", "Contacted again", "")
        raw = _Conn(connection_string())
        for sql in ("UPDATE audit SET detail='x' WHERE seq=1", "DELETE FROM audit WHERE seq=1"):
            with self.assertRaises(s.dberror):
                raw.execute(sql)
        raw.execute("DROP TRIGGER audit_append_only")
        raw.execute("UPDATE audit SET detail='rewritten' WHERE seq=1")
        self.assertFalse(s.verify_audit())

    test_list_filters_use_indexes = None


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlParity(reads.Parity):
    """SQL list reads on SQL Server give the same answers as the in-memory store (binary collation, paging, ranks)."""

    @classmethod
    def setUpClass(cls):
        cls._orig, reads.SqlStore = reads.SqlStore, factory
        wipe()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        reads.SqlStore = cls._orig
        super().tearDownClass()


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlWrites(reads.Writes):
    @classmethod
    def setUpClass(cls):
        cls._orig, reads.SqlStore = reads.SqlStore, factory

    @classmethod
    def tearDownClass(cls):
        reads.SqlStore = cls._orig

    def setUp(self):
        wipe()


if __name__ == "__main__":
    unittest.main()

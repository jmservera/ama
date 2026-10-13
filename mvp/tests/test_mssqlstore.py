"""The SQL store behaviour suites again, against a real SQL Server or Azure SQL.

Skipped unless ZF_TEST_MSSQL=1 and the ZF_SQL_* settings point at a database that may be wiped
(the CI job uses a throwaway SQL Server container; never point this at the pilot database).
"""
import os
import unittest

import test_sqlreads as reads
import test_sqlstore as base

ON = os.environ.get("ZF_TEST_MSSQL") == "1"
TABLES = ("audit_head", "audit", "recommendations", "cases", "staff", "meta")


def wipe():
    from zavaforward_mvp.mssqlstore import _Conn, connection_string
    c = _Conn(connection_string())
    c.execute("IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only")
    for t in TABLES:
        c.execute(f"IF OBJECT_ID(N'{t}', N'U') IS NOT NULL DROP TABLE {t}")


def factory(data, db, *a, **k):
    from zavaforward_mvp.mssqlstore import MssqlStore
    return MssqlStore(data, state_dir=os.path.dirname(db))


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

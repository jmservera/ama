"""Actual accounting procedures on opt-in isolated loopback SQL, never Azure SQL."""

import os
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from zava_forward.core import resident_showcase_sql as rsql

from zava_forward.api.resident_demo.aoai import SqlAccounting, resident_key

ON = os.environ.get("ZF_TEST_MSSQL") == "1" and os.environ.get("ZF_SQL_SERVER") in (
    "127.0.0.1",
    "localhost",
)
SQL = Path(__file__).resolve().parents[3] / "infra/sql/resident-assistant.sql"


@unittest.skipUnless(ON, "opt-in isolated local SQL Server")
class AccountingSqlTests(unittest.TestCase):
    base: dict[str, str]
    database: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.base = {
            "server": os.environ["ZF_SQL_SERVER"],
            "port": os.environ.get("ZF_SQL_PORT", "1433"),
            "auth": "password",
            "user": os.environ.get("ZF_SQL_USER", "sa"),
            "password": os.environ["ZF_SQL_PASSWORD"],
            "trust_cert": "1",
        }
        cls.database = "aoai469_" + uuid.uuid4().hex[:8]
        conn = rsql.connector({**cls.base, "database": "master"})()
        try:
            conn.cursor().execute(f"CREATE DATABASE [{cls.database}]")
        finally:
            conn.close()
        try:
            cls.q("CREATE USER [resident_test] WITHOUT LOGIN")
            cls.apply()
        except BaseException:
            cls.tearDownClass()
            raise

    @classmethod
    def connect(cls) -> Any:
        return rsql.connector({**cls.base, "database": cls.database})()

    @classmethod
    def q(cls, text: str, *params: object) -> list[Any]:
        conn = cls.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(text, params) if params else cursor.execute(text)
            return cursor.fetchall() if cursor.description else []
        finally:
            conn.close()

    @classmethod
    def apply(cls) -> None:
        import re

        for batch in re.split(r"^GO\s*$", SQL.read_text(), flags=re.MULTILINE):
            if batch.strip():
                cls.q(batch.replace("{{PRINCIPAL}}", "resident_test"))

    @classmethod
    def tearDownClass(cls) -> None:
        conn = rsql.connector({**cls.base, "database": "master"})()
        try:
            conn.cursor().execute(
                f"ALTER DATABASE [{cls.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;"
                f"DROP DATABASE [{cls.database}]"
            )
        finally:
            conn.close()

    def setUp(self) -> None:
        self.q(
            "DELETE FROM resident_ai.attempt; "
            "UPDATE resident_ai.budget SET reserved_cents=0, expires_at='2999-01-01T00:00:00'"
        )
        self.accounting = SqlAccounting(self.connect)

    def test_exact_cap_and_concurrent_last_cent(self) -> None:
        self.q("UPDATE resident_ai.budget SET reserved_cents=1999")
        with ThreadPoolExecutor(max_workers=8) as pool:
            tickets = list(
                pool.map(lambda i: self.accounting.reserve(resident_key(str(i))), range(8))
            )
        self.assertEqual(sum(ticket is not None for ticket in tickets), 1)
        self.assertEqual(self.q("SELECT reserved_cents FROM resident_ai.budget")[0][0], 2000)
        self.assertIsNone(self.accounting.reserve(resident_key("new-resident")))

    def test_five_per_resident_concurrency_and_independent_resident(self) -> None:
        with ThreadPoolExecutor(max_workers=8) as pool:
            tickets = list(
                pool.map(lambda _: self.accounting.reserve(resident_key("same")), range(8))
            )
        self.assertEqual(sum(ticket is not None for ticket in tickets), 5)
        self.assertIsNotNone(self.accounting.reserve(resident_key("other")))
        self.q("UPDATE resident_ai.attempt SET reserved_at=DATEADD(HOUR,-1,SYSUTCDATETIME())")
        self.assertIsNotNone(self.accounting.reserve(resident_key("same")))

    def test_restart_migration_and_completion_never_refund(self) -> None:
        ticket = self.accounting.reserve(resident_key("one"))
        assert ticket is not None
        restarted = SqlAccounting(self.connect)
        restarted.complete(ticket, 12, 3)
        restarted.complete(ticket, 999, 99)
        self.apply()
        self.assertEqual(self.q("SELECT reserved_cents FROM resident_ai.budget")[0][0], 1)
        row = self.q("SELECT prompt_tokens, completion_tokens FROM resident_ai.attempt")[0]
        self.assertEqual(tuple(row), (12, 3))
        self.assertIsNotNone(restarted.reserve(resident_key("one")))
        self.assertEqual(self.q("SELECT reserved_cents FROM resident_ai.budget")[0][0], 2)

    def test_lost_response_or_completion_does_not_reuse_or_refund(self) -> None:
        ticket = str(uuid.uuid4())
        key = resident_key("one")
        self.assertEqual(self.q("EXEC resident_ai.reserve ?, ?", key, ticket)[0][0], 1)
        self.assertEqual(self.q("EXEC resident_ai.reserve ?, ?", key, ticket)[0][0], 0)
        self.assertEqual(self.q("SELECT reserved_cents FROM resident_ai.budget")[0][0], 1)
        self.assertIsNone(self.q("SELECT prompt_tokens FROM resident_ai.attempt")[0][0])

    def test_missing_budget_row_reapply_cannot_reset_accounting(self) -> None:
        self.q("DELETE FROM resident_ai.budget")
        self.apply()
        self.assertIsNone(self.accounting.reserve(resident_key("one")))
        self.assertEqual(self.q("SELECT COUNT(*) FROM resident_ai.budget")[0][0], 0)
        self.q("INSERT INTO resident_ai.budget (id, reserved_cents) VALUES (1,0)")

    def test_expiry_is_data_refused_after_and_default_preserved(self) -> None:
        self.q("UPDATE resident_ai.budget SET expires_at=DATEADD(SECOND,-1,SYSUTCDATETIME())")
        self.assertIsNone(self.accounting.reserve(resident_key("one")))
        self.assertEqual(self.q("SELECT reserved_cents FROM resident_ai.budget")[0][0], 0)
        self.q("UPDATE resident_ai.budget SET expires_at=DATEADD(DAY,1,SYSUTCDATETIME())")
        self.assertIsNotNone(self.accounting.reserve(resident_key("one")))
        self.q("DELETE FROM resident_ai.budget")
        self.q("INSERT INTO resident_ai.budget (id, reserved_cents) VALUES (1,0)")
        default = self.q("SELECT expires_at FROM resident_ai.budget")[0][0]
        self.assertEqual((default.year, default.month, default.day), (2026, 11, 1))
        self.q("UPDATE resident_ai.budget SET expires_at='2999-01-01T00:00:00'")

    def test_reapply_keeps_extended_expiry(self) -> None:
        self.apply()
        self.assertEqual(self.q("SELECT expires_at FROM resident_ai.budget")[0][0].year, 2999)

    def test_principal_can_execute_but_not_read_or_write_accounting(self) -> None:
        import mssql_python

        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("EXECUTE AS USER = 'resident_test'")
            cursor.execute(
                "EXEC resident_ai.reserve ?, ?", (resident_key("one"), str(uuid.uuid4()))
            )
            self.assertEqual(cursor.fetchone()[0], 1)
            for text in (
                "SELECT * FROM resident_ai.attempt",
                "UPDATE resident_ai.budget SET reserved_cents=0",
                "DELETE FROM resident_ai.attempt",
                "INSERT INTO resident_ai.budget VALUES (1,0)",
            ):
                with self.assertRaises(mssql_python.Error):
                    cursor.execute(text)
        finally:
            conn.close()

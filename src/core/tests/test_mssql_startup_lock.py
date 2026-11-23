import re
import threading
import unittest
from typing import Any
from unittest.mock import patch

from zava_forward.core import mssqlstore, sqlstore
from zava_forward.core.mssqlstore import LOCK_FAILED, MssqlStore, _Conn


class DriverError(Exception):
    pass


class FakeDriver:
    Error = DriverError
    description = None
    rowcount = 0

    def __init__(self, failures: int, message: str = LOCK_FAILED) -> None:
        self.failures, self.message, self.calls = failures, message, 0

    def connect(self, *args: Any, **kw: Any) -> "FakeDriver":
        return self

    def cursor(self) -> "FakeDriver":
        return self

    def execute(self, sql: str, args: Any = ()) -> None:
        if sql.startswith("BEGIN TRAN"):
            self.calls += 1
            if self.calls <= self.failures:
                raise DriverError(self.message)


def conn(driver: FakeDriver, retries: int) -> Any:
    c: Any = _Conn.__new__(_Conn)
    c.driver, c.raw, c.in_tran, c.attrs, c.startup_retries = driver, driver, False, {}, retries
    return c


class StartupLockRetryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sleeps: list[float] = []
        patcher = patch.object(mssqlstore, "_sleep", self.sleeps.append)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_lock_timeout_is_retried_with_backoff_then_succeeds(self) -> None:
        d = FakeDriver(3)
        c = conn(d, 7)
        c.execute("BEGIN IMMEDIATE")
        self.assertTrue(c.in_tran)
        self.assertEqual(d.calls, 4)
        self.assertEqual(self.sleeps, [1.0, 2.0, 4.0])

    def test_exhausted_retries_raise_the_lock_error(self) -> None:
        d = FakeDriver(99)
        c = conn(d, 2)
        with self.assertRaises(DriverError):
            c.execute("BEGIN IMMEDIATE")
        self.assertEqual(d.calls, 3)
        self.assertFalse(c.in_tran)

    def test_other_errors_are_not_retried(self) -> None:
        d = FakeDriver(99, "permission denied")
        with self.assertRaises(DriverError):
            conn(d, 7).execute("BEGIN IMMEDIATE")
        self.assertEqual((d.calls, self.sleeps), (1, []))

    def test_no_retry_after_start_up(self) -> None:
        d = FakeDriver(1)
        with self.assertRaises(DriverError):
            conn(d, 0).execute("BEGIN IMMEDIATE")
        self.assertEqual((d.calls, self.sleeps), (1, []))

    def test_backoff_is_capped(self) -> None:
        d = FakeDriver(99)
        with self.assertRaises(DriverError):
            conn(d, 8).execute("BEGIN IMMEDIATE")
        self.assertEqual(max(self.sleeps), mssqlstore.LOCK_RETRY_CAP)

    def test_store_enables_retries_only_while_initialising(self) -> None:
        seen: list[int] = []

        def fake_init(self: Any, *a: Any) -> None:
            seen.append(self.db.startup_retries)

        def fake_conn_init(self: Any, *a: Any, **k: Any) -> None:
            self.startup_retries = 0

        with (
            patch.object(sqlstore.SqlStore, "_initialize", fake_init),
            patch.object(_Conn, "__init__", fake_conn_init),
            patch.object(mssqlstore, "connection_string", lambda env=None: ""),
        ):
            store: Any = MssqlStore.__new__(MssqlStore)
            store._env = {}
            store._open("x")
            store._initialize("d", "p", None, None)
        self.assertEqual(seen, [mssqlstore.LOCK_RETRY_ATTEMPTS - 1])
        self.assertEqual(store.db.startup_retries, 0)


class WriteLockBusyHelperTests(unittest.TestCase):
    @staticmethod
    def driver_error(name: str, message: str, module: str = "mssql_python.exceptions") -> Exception:
        error: Exception = type(name, (Exception,), {"__module__": module})(message)
        return error

    def test_driver_programming_error_with_the_lock_text_is_busy(self) -> None:
        err = self.driver_error(
            "ProgrammingError", f"Driver Error; DDBC Error: [SQL Server]{LOCK_FAILED}"
        )
        self.assertTrue(mssqlstore.is_write_lock_busy(err))

    def test_busy_error_is_found_through_the_exception_chain(self) -> None:
        inner = self.driver_error("ProgrammingError", LOCK_FAILED)
        try:
            try:
                raise inner
            except Exception as e:
                raise RuntimeError("wrapped") from e
        except RuntimeError as outer:
            self.assertTrue(mssqlstore.is_write_lock_busy(outer))

    def test_other_errors_are_not_busy(self) -> None:
        for err in (
            self.driver_error("ProgrammingError", "Invalid object name 'cases'."),
            self.driver_error("OperationalError", LOCK_FAILED),
            RuntimeError(LOCK_FAILED),
            self.driver_error("ProgrammingError", LOCK_FAILED, "other.module"),
        ):
            self.assertFalse(mssqlstore.is_write_lock_busy(err))
        self.assertFalse(mssqlstore.is_write_lock_busy(None))


class FakeDb:
    """Answers the read-only catalog queries from sets; records every statement."""

    def __init__(
        self,
        tables: set[str],
        triggers: set[str],
        indexes: set[str],
        columns: set[str],
        ledger: int = 0,
    ) -> None:
        self.tables, self.triggers, self.indexes, self.columns, self.ledger = (
            tables,
            triggers,
            indexes,
            columns,
            ledger,
        )
        self.sql: list[str] = []

    def execute(self, sql: str, args: Any = ()) -> Any:
        self.sql.append(sql)
        rows: list[Any] = []
        if sql.startswith("SELECT name FROM sys.tables"):
            rows = [(t,) for t in self.tables]
        elif sql.startswith("SELECT name FROM sys.triggers"):
            rows = [(t,) for t in self.triggers]
        elif sql.startswith("SELECT name FROM sys.indexes"):
            rows = [(i,) for i in self.indexes]
        elif sql.startswith("SELECT is_ledger_on"):
            rows = [(self.ledger,)]
        elif sql.startswith("SELECT COL_LENGTH"):
            rows = [(10 if args[1] in self.columns else None,)]
        elif sql.startswith("SELECT name FROM sys.columns"):
            rows = [(c,) for c in self.columns]
        cur: Any = type("Cur", (), {})()
        cur.fetchall, cur.fetchone = lambda: list(rows), lambda: rows[0] if rows else None
        return cur


def store(db: FakeDb) -> Any:
    s: Any = MssqlStore.__new__(MssqlStore)
    s.db, s.dblock = db, threading.RLock()
    return s


GUARDS = {"audit_append_only", "continuity_gate_no_delete", "continuity_gate_monotonic"}


mssql_any: Any = mssqlstore


class ReadOnlyStartupTests(unittest.TestCase):
    def test_current_schema_takes_no_write_lock(self) -> None:
        db = FakeDb(set(mssqlstore.TABLES), GUARDS, set(), set())
        store(db)._create_schema()
        self.assertFalse(any("BEGIN" in q for q in db.sql))

    def test_missing_table_takes_the_locked_path(self) -> None:
        db = FakeDb(set(mssqlstore.TABLES) - {"audit"}, GUARDS, set(), set())
        self.assertFalse(store(db)._schema_current())

    def test_missing_guard_trigger_takes_the_locked_path(self) -> None:
        db = FakeDb(set(mssqlstore.TABLES), GUARDS - {"continuity_gate_monotonic"}, set(), set())
        self.assertFalse(store(db)._schema_current())

    def test_wrong_ledger_kind_is_left_to_the_locked_path(self) -> None:
        db = FakeDb(set(mssqlstore.TABLES), set(), set(), set(), ledger=1)
        self.assertFalse(store(db)._schema_current())

    def test_queue_columns_present_skip_the_lock(self) -> None:
        db = FakeDb(set(), set(), set(), set(sqlstore.QUEUE_COLS))
        store(db)._migrate_queues()
        self.assertFalse(any("BEGIN" in q for q in db.sql))

    def test_all_indexes_present_skip_the_lock_and_one_missing_does_not(self) -> None:
        stmts: list[str] = mssql_any._indexes() + [mssql_any.CHAT_INDEX]
        names = {m.group(1) for m in (re.search(r"CREATE INDEX (\w+)", st) for st in stmts) if m}
        self.assertTrue(names)
        self.assertTrue(store(FakeDb(set(), set(), names, set()))._indexes_current(stmts))
        self.assertFalse(
            store(FakeDb(set(), set(), names - {sorted(names)[0]}, set()))._indexes_current(stmts)
        )


if __name__ == "__main__":
    unittest.main()

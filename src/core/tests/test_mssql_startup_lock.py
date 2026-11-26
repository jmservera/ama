import importlib
import re
import sqlite3
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


class LinkDriver(FakeDriver):
    """Drops the link on the first N statements, as a brief SQL outage does."""

    def execute(self, sql: str, args: Any = ()) -> None:
        self.calls += 1
        if self.calls <= self.failures:
            raise DriverError("Communication link failure; TCP Provider: Error code 0x68")


def conn(driver: FakeDriver, retries: int) -> Any:
    c: Any = _Conn.__new__(_Conn)
    c.driver, c.raw, c.in_tran, c.attrs, c.startup_retries = driver, driver, False, {}, retries
    c.conn_str = ""
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

    def test_dead_link_at_start_up_is_retried_with_backoff(self) -> None:
        d = LinkDriver(3)
        conn(d, 7).execute("SELECT 1")
        self.assertEqual((d.calls, self.sleeps), (4, [1.0, 2.0]))

    def test_dead_link_after_start_up_keeps_one_immediate_reconnect(self) -> None:
        d = LinkDriver(2)
        with self.assertRaises(DriverError):
            conn(d, 0).execute("SELECT 1")
        self.assertEqual((d.calls, self.sleeps), (2, []))

    def test_dead_link_at_start_up_gives_up_after_the_bounded_attempts(self) -> None:
        d = LinkDriver(99)
        with self.assertRaises(DriverError):
            conn(d, 7).execute("SELECT 1")
        self.assertEqual(d.calls, 2 + mssqlstore.LINK_RETRY_ATTEMPTS)

    def test_write_wait_caps_this_threads_lock_timeout_then_restores_it(self) -> None:
        sent: list[str] = []
        d = FakeDriver(0)
        c = conn(d, 0)
        with patch.object(d, "execute", lambda sql, args=(): sent.append(sql)):
            with c.write_wait(2000):
                c.execute("BEGIN IMMEDIATE")
                t = threading.Thread(target=lambda: (c.execute("COMMIT"), c._begin()))
                t.start()
                t.join()
            c.execute("BEGIN IMMEDIATE")
        begins = [x for x in sent if x.startswith("BEGIN TRAN")]
        self.assertIn("@LockTimeout = 2000", begins[0])
        self.assertIn("@LockTimeout = 15000", begins[1])
        self.assertIn("@LockTimeout = 15000", begins[2])

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


class LawStoreStartupRetryTests(unittest.TestCase):
    def test_law_db_enables_start_up_retries_and_ends_them(self) -> None:
        lawstore: Any = importlib.import_module("zava_forward.core.lawstore")

        made: list[Any] = []

        class StubConn:
            startup_retries = 0

            def __init__(self, *a: Any, **kw: Any) -> None:
                made.append(self)

            def execute(self, sql: str, args: Any = ()) -> Any:
                class Row:
                    def fetchone(self) -> tuple[int, ...]:
                        return (0,)

                    def fetchall(self) -> list[Any]:
                        return []

                return Row()

        with (
            patch.object(mssqlstore, "_Conn", StubConn),
            patch.object(mssqlstore, "connection_string", lambda env: ""),
        ):
            db = lawstore.MssqlDb({})
        self.assertEqual(made[0].startup_retries, mssqlstore.LOCK_RETRY_ATTEMPTS - 1)
        db.end_startup()
        self.assertEqual(made[0].startup_retries, 0)

    def test_law_store_ends_start_up_retries_even_when_seeding_fails(self) -> None:
        lawstore: Any = importlib.import_module("zava_forward.core.lawstore")

        ended: list[bool] = []

        class Sql:
            def end_startup(self) -> None:
                ended.append(True)

        with patch("zava_forward.core.rulecards.RuleCardStore", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                lawstore.LawStore(db=Sql(), blobs=object())
        self.assertEqual(ended, [True])


class LawDbReadOnlyStartupTests(unittest.TestCase):
    TABLES = ("reg_source", "reg_version", "reg_provision", "reg_gap", "reg_index")

    def open_db(
        self, tables: tuple[str, ...], triggers: tuple[str, ...], ledger: int, kind: str
    ) -> list[str]:
        lawstore: Any = importlib.import_module("zava_forward.core.lawstore")
        ran: list[str] = []
        tbl, trg = tables, triggers

        class Rows:
            def __init__(self, rows: list[Any]) -> None:
                self.rows = rows

            def fetchone(self) -> Any:
                return self.rows[0]

            def fetchall(self) -> list[Any]:
                return self.rows

        class StubConn:
            startup_retries = 0

            def __init__(self, *a: Any, **kw: Any) -> None:
                pass

            def execute(self, sql: str, args: Any = ()) -> Any:
                ran.append(sql)
                if "is_ledger_on" in sql:
                    return Rows([(ledger,)])
                if "FROM sys.tables" in sql and "ledger_type_desc" in sql:
                    return Rows([(t, kind) for t in tbl])
                if "FROM sys.tables" in sql:
                    return Rows([(t,) for t in tbl])
                if "FROM sys.triggers" in sql:
                    return Rows([(t,) for t in trg])
                return Rows([(kind,)])

        with (
            patch.object(mssqlstore, "_Conn", StubConn),
            patch.object(mssqlstore, "connection_string", lambda env: ""),
        ):
            try:
                lawstore.MssqlDb({})
            except SystemExit:
                pass
        return ran

    def took_lock(self, ran: list[str]) -> bool:
        return "BEGIN IMMEDIATE" in ran

    def test_current_trigger_schema_takes_no_write_lock(self) -> None:
        guards = tuple(f"{t}_append_only" for t in self.TABLES[:4])
        self.assertFalse(self.took_lock(self.open_db(self.TABLES, guards, 0, "")))

    def test_current_ledger_schema_takes_no_write_lock(self) -> None:
        self.assertFalse(
            self.took_lock(self.open_db(self.TABLES, (), 1, "APPEND_ONLY_LEDGER_TABLE"))
        )

    def test_missing_table_missing_trigger_or_wrong_ledger_kind_take_the_lock(self) -> None:
        guards = tuple(f"{t}_append_only" for t in self.TABLES[:4])
        self.assertTrue(self.took_lock(self.open_db(self.TABLES[:4], guards, 0, "")))
        self.assertTrue(self.took_lock(self.open_db(self.TABLES, guards[:3], 0, "")))
        self.assertTrue(self.took_lock(self.open_db(self.TABLES, (), 1, "UPDATABLE_LEDGER_TABLE")))


class PopulatedStartupLockCountTests(unittest.TestCase):
    """Issue #2244: a populated store must not take the write lock at every start-up step."""

    def begins(self, seed: str, db: str) -> int:
        seen: list[str] = []
        real = sqlite3.connect

        def connect(*a: Any, **k: Any) -> Any:
            c = real(*a, **k)
            c.set_trace_callback(
                lambda s: seen.append(s) if s.startswith("BEGIN IMMEDIATE") else None
            )
            return c

        opened: Any = sqlstore.SqlStore
        with patch.object(sqlite3, "connect", connect):
            opened(seed, db).db.close()
        return len(seen)

    def test_reopen_skips_seed_queue_and_recommendation_locks(self) -> None:
        import json
        import tempfile
        from pathlib import Path

        data = importlib.import_module("test_bulk_edits").DATA

        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "seed.json"
            seed.write_text(json.dumps(data))
            first = self.begins(str(seed), str(Path(tmp) / "d.sqlite"))
            again = self.begins(str(seed), str(Path(tmp) / "d.sqlite"))
        self.assertLess(again, first)
        self.assertLessEqual(again, 2)


class MigrateFastPathTests(unittest.TestCase):
    """Issue #2244: the derived-column migration takes the write lock only when it has work."""

    def open_store(self, tmp: str) -> Any:
        import json
        from pathlib import Path

        data = importlib.import_module("test_bulk_edits").DATA
        seed = Path(tmp) / "seed.json"
        seed.write_text(json.dumps(data))
        opened: Any = sqlstore.SqlStore
        return opened(str(seed), str(Path(tmp) / "d.sqlite"))

    def test_gate_in_sync_is_read_only_and_detects_drift(self) -> None:
        import tempfile

        from zava_forward.core import continuity

        with tempfile.TemporaryDirectory() as tmp:
            s = self.open_store(tmp)
            self.assertTrue(continuity.gate_in_sync(s.db))
            s.db.execute(
                "INSERT INTO continuity_open_holds (scope, incident_id, epoch) VALUES ('x', 'i', 1)"
            )
            self.assertFalse(continuity.gate_in_sync(s.db))
            s.db.execute("DELETE FROM continuity_open_holds")
            self.assertTrue(continuity.gate_in_sync(s.db))
            s.db.execute("UPDATE meta SET value = 'not json' WHERE key = 'continuity'")
            self.assertFalse(continuity.gate_in_sync(s.db))
            s.db.execute("DELETE FROM meta WHERE key = 'continuity'")
            self.assertFalse(continuity.gate_in_sync(s.db))
            s.db.close()

    def test_identity_drift_is_reported_without_writing(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            s = self.open_store(tmp)
            self.assertEqual(list(s._identity_drift()), [])
            s.db.execute("UPDATE cases SET stage = 'drifted'")
            self.assertTrue(list(s._identity_drift()))
            self.assertEqual(
                s.db.execute("SELECT COUNT(*) FROM cases WHERE stage = 'drifted'").fetchone()[0],
                len(list(s._identity_drift())),
            )
            s.db.close()

    def test_current_store_skips_the_locked_migration_and_stale_takes_it(self) -> None:
        calls: list[str] = []
        s = store(FakeDb(set(), set(), set(), set()))
        with (
            patch.object(MssqlStore, "_migrate_current", return_value=True),
            patch.object(sqlstore.SqlStore, "_migrate", lambda self: calls.append("locked")),
        ):
            s._migrate()
        self.assertEqual(calls, [])
        with (
            patch.object(MssqlStore, "_migrate_current", return_value=False),
            patch.object(sqlstore.SqlStore, "_migrate", lambda self: calls.append("locked")),
        ):
            s._migrate()
        self.assertEqual(calls, ["locked"])

    def test_missing_derived_column_is_not_current(self) -> None:
        db = FakeDb(set(), set(), set(), set(sqlstore.CASE_COLS) - {"days"})
        self.assertFalse(store(db)._migrate_current())
        self.assertFalse(any("BEGIN" in q for q in db.sql))


if __name__ == "__main__":
    unittest.main()

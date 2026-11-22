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


if __name__ == "__main__":
    unittest.main()

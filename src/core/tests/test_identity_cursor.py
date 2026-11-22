import threading
import unittest
from typing import Any

from zava_forward.core import identity
from zava_forward.core.mssqlstore import _Cursor

ROW = ('{"code": "KL", "role": "Contractor"}',)


class _Raw:
    rowcount = 1

    def fetchall(self) -> list[tuple[str]]:
        return [ROW]


class _Db:
    def execute(self, sql: str) -> Any:
        return _Cursor(_Raw())  # type: ignore[no-untyped-call]


class _Store:
    db = _Db()
    dblock = threading.Lock()


class MssqlCursorRosterTests(unittest.TestCase):
    def test_roster_rows_read_through_the_sql_cursor(self) -> None:
        self.assertEqual(identity._rows(_Store())[0]["code"], "KL")

    def test_cursor_is_iterable(self) -> None:
        self.assertEqual(list(_Cursor(_Raw())), [ROW])  # type: ignore[no-untyped-call]

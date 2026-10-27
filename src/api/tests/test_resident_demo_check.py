"""Regression coverage for the shared resident browser/image SQL fixture."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from checks import resident_demo_browser_check as browser_check
from zava_forward.core import resident_showcase as rs
from zava_forward.core import resident_showcase_sql as rsql


class ResidentDemoCheckTests(unittest.TestCase):
    def test_sql_fixture_window_is_independent_of_application_cap(self) -> None:
        now = datetime(2026, 10, 27, 12, tzinfo=UTC)
        with (
            patch.object(browser_check, "run_sql") as sql,
            patch.object(rsql, "connector") as connector,
            patch.object(browser_check, "sql_settings", return_value={}),
            patch.object(browser_check, "datetime") as clock,
            patch.object(rs, "AUTHORITY_END", datetime(2027, 1, 1, tzinfo=UTC)),
        ):
            clock.now.return_value = now
            with browser_check.database() as name:
                inserts = [
                    call.args
                    for call in sql.call_args_list
                    if "INSERT INTO resident_showcase.allowed_case" in call.args[1]
                ]
                self.assertEqual(len(inserts), len(browser_check.RESIDENTS))
                for n, args in enumerate(inserts, start=1):
                    self.assertEqual(args[0], name)
                    self.assertEqual(args[2], f"SYN-{n}")
                    self.assertEqual(args[3], (now - timedelta(days=1)).replace(tzinfo=None))
                    self.assertEqual(args[4], datetime(2026, 11, 1))
                    self.assertLess(args[3], args[4])
                    self.assertLess(args[4].replace(tzinfo=UTC), rs.AUTHORITY_END)
            conn = connector.return_value.return_value
            conn.cursor.return_value.execute.assert_any_call(f"DROP DATABASE [{name}]")
            conn.close.assert_called_once_with()

    def test_fixture_import_does_not_require_playwright(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                """
import importlib.abc
import sys

class NoPlaywright(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "playwright" or fullname.startswith("playwright."):
            raise ModuleNotFoundError("Playwright must not be imported by unit discovery")

sys.meta_path.insert(0, NoPlaywright())
from checks.resident_demo_browser_check import database
assert callable(database)
""",
            ],
            env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)},
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

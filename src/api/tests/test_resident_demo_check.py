"""Regression coverage for the shared resident browser/image SQL fixture."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import Mock, patch

from checks import resident_demo_browser_check as browser_check
from zava_forward.core import resident_showcase as rs
from zava_forward.core import resident_showcase_sql as rsql


class ResidentDemoCheckTests(unittest.TestCase):
    def signed_out_context(self) -> Mock:
        context = Mock()
        context.cookies.return_value = [{"name": "__Host-zfdemo", "value": "original-token"}]
        context.request.get.side_effect = [
            Mock(status=401),
            Mock(status=200, json=Mock(return_value={"signed_in": False, "session_id": None})),
        ]
        return context

    def test_signed_out_check_uses_retained_token_and_original_fence(self) -> None:
        context = self.signed_out_context()
        browser_check.check_signed_out(context, "http://localhost", "original-token", "original-id")
        self.assertEqual(context.request.get.call_count, 2)
        self.assertEqual(
            context.request.get.call_args_list[0].args, ("http://localhost/demo/view",)
        )
        self.assertEqual(
            context.request.get.call_args_list[0].kwargs,
            {"headers": {"X-Resident-Session": "original-id"}},
        )
        self.assertEqual(
            context.request.get.call_args_list[1].args, ("http://localhost/demo/session",)
        )
        self.assertEqual(context.request.get.call_args_list[1].kwargs, {})

    def test_signed_out_check_rejects_replaced_or_missing_cookie(self) -> None:
        for cookies in ([], [{"name": "__Host-zfdemo", "value": "replacement-token"}]):
            with self.subTest(cookies=cookies):
                context = self.signed_out_context()
                context.cookies.return_value = cookies
                with self.assertRaisesRegex(AssertionError, "original session cookie"):
                    browser_check.check_signed_out(
                        context, "http://localhost", "original-token", "original-id"
                    )

    def test_signed_out_check_requires_view_401(self) -> None:
        for status in (200, 409, 503):
            with self.subTest(status=status):
                context = self.signed_out_context()
                context.request.get.side_effect = [Mock(status=status)]
                with self.assertRaisesRegex(AssertionError, "cannot authenticate"):
                    browser_check.check_signed_out(
                        context, "http://localhost", "original-token", "original-id"
                    )

    def test_signed_out_check_requires_successful_explicit_signed_out_status(self) -> None:
        for status, body in (
            (503, {"signed_in": False, "session_id": None}),
            (200, {"signed_in": True, "session_id": None}),
            (200, {"signed_in": False, "session_id": "still-active"}),
            (200, {"signed_in": 0, "session_id": None}),
            (200, {"session_id": None}),
            (200, {"signed_in": False}),
        ):
            with self.subTest(status=status, body=body):
                context = self.signed_out_context()
                context.request.get.side_effect = [
                    Mock(status=401),
                    Mock(status=status, json=Mock(return_value=body)),
                ]
                with self.assertRaises((AssertionError, KeyError)):
                    browser_check.check_signed_out(
                        context, "http://localhost", "original-token", "original-id"
                    )

    def test_sql_fixture_window_ends_at_the_shared_authority_end(self) -> None:
        now = datetime(2026, 10, 27, 12, tzinfo=UTC)
        with (
            patch.object(browser_check, "run_sql") as sql,
            patch.object(rsql, "connector") as connector,
            patch.object(browser_check, "sql_settings", return_value={}),
            patch.object(browser_check, "datetime") as clock,
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
                    self.assertEqual(args[4], datetime(2027, 2, 1))
                    self.assertNotEqual(args[4], datetime(2026, 11, 1))
                    self.assertLess(args[3], args[4])
                    self.assertEqual(args[4].replace(tzinfo=UTC), rs.AUTHORITY_END)
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

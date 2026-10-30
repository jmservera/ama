"""Fail-closed accessibility coverage for the local capacity acceptance check."""

import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from checks.capacity_browser_check import load_axe, scan_capacity


class CapacityBrowserCheck(unittest.TestCase):
    def test_scanner_suite_runs_without_playwright(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                """
import importlib.abc
import sys
import unittest

class NoPlaywright(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "playwright" or fullname.startswith("playwright."):
            raise ModuleNotFoundError("Playwright must not be imported by unit discovery")

sys.meta_path.insert(0, NoPlaywright())
from checks.capacity_browser_check import check
from test_capacity_browser_check import CapacityBrowserCheck

suite = unittest.TestSuite(CapacityBrowserCheck(name) for name in (
    "test_load_axe_accepts_only_matching_bytes",
    "test_load_axe_rejects_wrong_bytes",
    "test_scan_reports_clean_and_incomplete_results",
    "test_scan_rejects_violations_without_hiding_details",
))
result = unittest.TextTestRunner().run(suite)
assert result.testsRun == 4 and not result.skipped
assert result.wasSuccessful()
assert not any(name == "playwright" or name.startswith("playwright.") for name in sys.modules)
with unittest.TestCase().assertRaisesRegex(ModuleNotFoundError, "Playwright must not be imported"):
    check(None)
""",
            ],
            env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)},
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_load_axe_accepts_only_matching_bytes(self) -> None:
        raw = b"synthetic scanner"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "axe.js"
            path.write_bytes(raw)
            with patch("checks.capacity_browser_check.AXE_SHA256", hashlib.sha256(raw).hexdigest()):
                self.assertEqual(load_axe(path), raw.decode())

    def test_load_axe_rejects_wrong_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "axe.js"
            path.write_text("not the pinned scanner")
            with self.assertRaisesRegex(ValueError, "Expected pinned axe-core 4.10.3"):
                load_axe(path)

    def test_scan_reports_clean_and_incomplete_results(self) -> None:
        page = Mock(spec=["evaluate"])
        result = dict(violations=[], incomplete=[dict(id="color-contrast")])
        page.evaluate.side_effect = [None, result]
        output = io.StringIO()
        with redirect_stdout(output):
            scan_capacity(page, "synthetic scanner", "seeded capacity")
        self.assertEqual(json.loads(output.getvalue()), dict(state="seeded capacity", **result))
        page.evaluate.assert_any_call("synthetic scanner")
        script = page.evaluate.call_args.args[0]
        self.assertIn("document.querySelector('#app')", script)
        self.assertIn("'wcag22aa'", script)

    def test_scan_rejects_violations_without_hiding_details(self) -> None:
        page = Mock(spec=["evaluate"])
        result = dict(violations=[dict(id="button-name")], incomplete=[])
        page.evaluate.side_effect = [None, result]
        output = io.StringIO()
        with redirect_stdout(output):
            with self.assertRaisesRegex(AssertionError, "button-name"):
                scan_capacity(page, "synthetic scanner", "packages unavailable")
        self.assertEqual(
            json.loads(output.getvalue()), dict(state="packages unavailable", **result)
        )

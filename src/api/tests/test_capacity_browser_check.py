"""Fail-closed accessibility coverage for the local capacity acceptance check."""

import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from checks.capacity_browser_check import load_axe, scan_capacity
from playwright.sync_api import Page


class CapacityBrowserCheck(unittest.TestCase):
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
        page = Mock(spec=Page)
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
        page = Mock(spec=Page)
        result = dict(violations=[dict(id="button-name")], incomplete=[])
        page.evaluate.side_effect = [None, result]
        output = io.StringIO()
        with redirect_stdout(output):
            with self.assertRaisesRegex(AssertionError, "button-name"):
                scan_capacity(page, "synthetic scanner", "packages unavailable")
        self.assertEqual(
            json.loads(output.getvalue()), dict(state="packages unavailable", **result)
        )

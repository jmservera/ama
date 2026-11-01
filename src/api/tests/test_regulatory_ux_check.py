"""Regression coverage for the regulatory browser gate's target-size assertions."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import unittest
import unittest.mock
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from unittest.mock import Mock

from checks.regulatory_ux_check import run, scan, target_sizes


class RegulatoryUxCheckTests(unittest.TestCase):
    def test_import_does_not_require_playwright(self) -> None:
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
from checks.regulatory_ux_check import run, target_sizes
assert callable(run) and callable(target_sizes)
""",
            ],
            env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)},
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_target_minimums(self) -> None:
        page = Mock()
        for width, height, minimum, passes in (
            (24, 24, 24, True),
            (23.99, 24, 24, False),
            (24, 23.99, 24, False),
            (24, 44, 44, True),
            (24, 24, 44, False),
        ):
            with self.subTest(width=width, height=height, minimum=minimum):
                sizes = [dict(control="synthetic", width=width, height=height, min_height=minimum)]
                page.locator.return_value.locator.return_value.evaluate_all.return_value = sizes
                if passes:
                    self.assertEqual(target_sizes(page, "#regulatory-chat"), sizes)
                else:
                    with self.assertRaisesRegex(AssertionError, "Target size below"):
                        target_sizes(page, "#regulatory-chat")

    def test_only_static_supplier_surface_can_have_no_targets(self) -> None:
        page = Mock()
        page.locator.return_value.locator.return_value.evaluate_all.return_value = []
        self.assertEqual(target_sizes(page, "#regulatory-supplier"), [])
        with self.assertRaisesRegex(AssertionError, "No interactive targets"):
            target_sizes(page, "#regulatory-chat")

    def test_button_background_is_not_animated(self) -> None:
        css = (
            Path(__file__).parents[1] / "src" / "zava_forward" / "api" / "web" / "style.css"
        ).read_text()
        animated: list[str] = []
        for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
            names = {name.strip() for name in selectors.split(",")}
            if not names & {"button", ".btn"}:
                continue
            for value in re.findall(r"transition(?:-property)?\s*:\s*([^;]+)", body):
                animated.extend(re.findall(r"(?<![\w-])(background-color|background|all)\b", value))
                animated.extend(re.findall(r"(border-color)\b", value))
        self.assertIn("border-color", animated, "Button transition rule was not found")
        forbidden = [name for name in animated if name != "border-color"]
        self.assertEqual(
            forbidden,
            [],
            "Buttons must not fade their background while text colour changes instantly",
        )

    def _scan(self, incomplete: list[dict[str, Any]], strict: bool) -> list[dict[str, Any]]:
        page = Mock()
        page.evaluate.side_effect = [
            None,
            {"violations": [], "incomplete": incomplete, "passes": []},
        ]
        reports: list[dict[str, Any]] = []
        with unittest.mock.patch("checks.regulatory_ux_check.target_sizes", return_value=[]):
            scan(page, "axe", reports, "state", strict_contrast=strict)
        return reports

    def test_strict_scan_rejects_unresolved_contrast(self) -> None:
        item = {"id": "color-contrast", "nodes": [{"target": ["#a"]}]}
        with self.assertRaises(AssertionError):
            self._scan([item], True)

    def test_other_incompletes_and_clean_scans_pass(self) -> None:
        other = {"id": "aria-valid-attr-value", "nodes": [{"target": ["#a"]}]}
        self.assertEqual(self._scan([other], True)[0]["incomplete"][0]["id"], other["id"])
        self.assertEqual(self._scan([], True)[0]["incomplete"], [])

    def test_contrast_incomplete_is_reported_when_not_strict(self) -> None:
        item = {"id": "color-contrast", "nodes": [{"target": ["#a"]}]}
        self.assertEqual(self._scan([item], False)[0]["incomplete"][0]["id"], "color-contrast")

    def test_untrusted_axe_fails_before_application_start(self) -> None:
        with TemporaryDirectory() as folder:
            axe = Path(folder) / "axe.js"
            axe.write_text("unexpected content")
            with self.assertRaisesRegex(AssertionError, "Unexpected axe 4.10.3 content"):
                run(axe)

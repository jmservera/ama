"""Regression coverage for the regulatory browser gate's target-size assertions."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from checks.regulatory_ux_check import run, target_sizes


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

    def test_untrusted_axe_fails_before_application_start(self) -> None:
        with TemporaryDirectory() as folder:
            axe = Path(folder) / "axe.js"
            axe.write_text("unexpected content")
            with self.assertRaisesRegex(AssertionError, "Unexpected axe 4.10.3 content"):
                run(axe)

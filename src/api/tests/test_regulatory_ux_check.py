"""Regression coverage for the regulatory browser gate's target-size assertions."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from checks.regulatory_ux_check import run, target_sizes


class RegulatoryUxCheckTests(unittest.TestCase):
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

    def test_untrusted_axe_fails_before_application_start(self) -> None:
        with TemporaryDirectory() as folder:
            axe = Path(folder) / "axe.js"
            axe.write_text("unexpected content")
            with self.assertRaisesRegex(AssertionError, "Unexpected axe 4.10.3 content"):
                run(axe)

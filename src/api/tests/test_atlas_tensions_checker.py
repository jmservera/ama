"""Regression cases for the region, Tab-reach, design version and withheld-panel helpers.

Lightweight doubles stand in for the page; the real-DOM class launches Chromium only when
ZF_BROWSER_TESTS=1.
"""

from __future__ import annotations

import os
import unittest
from typing import Any

from checks.atlas_tensions_browser_check import (
    QUALITY,
    TECHNICAL,
    WITHHELD,
    WITHHELD_ITEMS,
    check_design_version,
    check_regions_and_keys,
    check_withheld,
)
from playwright.sync_api import sync_playwright


class _Regions:
    def __init__(self, labels: list[Any], structured: bool = True) -> None:
        self.labels = labels
        self.structured = structured

    def evaluate_all(self, script: str) -> Any:
        return self.labels if "getAttribute" in script else self.structured


class _Evidence:
    def __init__(self, regions: _Regions, page: _Page) -> None:
        self.regions = regions
        self.page = page

    def locator(self, selector: str) -> _Regions:
        return self.regions

    def evaluate(self, script: str) -> int:
        return self.page.active_region()


class _Keyboard:
    def __init__(self, page: _Page) -> None:
        self.page = page

    def press(self, key: str) -> None:
        self.page.presses += 1


class _Page:
    """Tab order as scoped region indices; -1 is an unrelated stop."""

    def __init__(self, stops: list[int], labels: list[Any]) -> None:
        self.stops = stops
        self.labels = labels
        self.presses = 0
        self.keyboard = _Keyboard(self)

    def active_region(self) -> int:
        if self.presses == 0:
            return -1
        return self.stops[min(self.presses, len(self.stops)) - 1]

    def evaluate(self, script: str) -> Any:
        if "getAttribute" not in script:
            return None
        active = self.active_region()
        return self.labels[active] or "" if active >= 0 else ""


def _run(labels: list[Any], stops: list[int]) -> None:
    page = _Page(stops, labels)
    check_regions_and_keys(page, _Evidence(_Regions(labels), page), "double")  # type: ignore[arg-type]


class RegionLabelTests(unittest.TestCase):
    def test_empty_label_with_unlabelled_stop_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run([""], [-1])

    def test_whitespace_label_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run(["   "], [-1])

    def test_absent_label_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run([None], [-1])

    def test_no_regions_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run([], [-1])

    def test_valid_labelled_reach_passes(self) -> None:
        _run(["Package capacity"], [-1, 0])

    def test_unreached_valid_label_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run(["Package capacity"], [-1] * 130)

    def test_duplicate_names_second_unreached_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run(["Capacity", "Capacity"], [-1, 0])

    def test_duplicate_names_both_reached_passes(self) -> None:
        _run(["Capacity", "Capacity"], [-1, 0, 1])


class _Section:
    def __init__(self, fields: list[dict[str, Any]]) -> None:
        self.fields = fields

    def evaluate(self, script: str) -> list[dict[str, Any]]:
        return self.fields


def _field(value: Any, visible: bool = True) -> dict[str, Any]:
    return {"value": value, "visible": visible}


class DesignVersionFieldTests(unittest.TestCase):
    def _run(self, fields: list[dict[str, Any]], expected: Any = 1) -> None:
        check_design_version(_Section(fields), expected, "double")

    def test_exact_value_passes(self) -> None:
        self._run([_field("1")])

    def test_wrong_value_fails(self) -> None:
        for value in ("2", "Unknown", "10", "v1", "1 (draft)"):
            with self.subTest(value=value), self.assertRaises(AssertionError):
                self._run([_field(value)])

    def test_blank_value_fails(self) -> None:
        for value in ("", "   ", None):
            with self.subTest(value=value), self.assertRaises(AssertionError):
                self._run([_field(value)])

    def test_missing_label_fails(self) -> None:
        with self.assertRaises(AssertionError):
            self._run([])

    def test_duplicate_label_fails_even_when_one_value_is_correct(self) -> None:
        with self.assertRaises(AssertionError):
            self._run([_field("1"), _field("2")])

    def test_invisible_field_fails(self) -> None:
        with self.assertRaises(AssertionError):
            self._run([_field("1", visible=False)])


@unittest.skipUnless(os.environ.get("ZF_BROWSER_TESTS") == "1", "opt-in local Chromium")
class DesignVersionBrowserTests(unittest.TestCase):
    """The real in-page extraction, run against a real DOM."""

    MARKUP = '<section><dl><dt id="t">Current design version</dt><dd id="d">1</dd></dl></section>'

    def _run(self, style: str | None = None, expected: Any = 1) -> None:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                page = browser.new_page()
                page.set_content(self.MARKUP)
                if style:
                    page.add_style_tag(content=style)
                check_design_version(page.locator("section"), expected, "browser")
            finally:
                browser.close()

    def test_visible_exact_value_passes(self) -> None:
        self._run()

    def test_hidden_or_transparent_field_fails(self) -> None:
        for selector in ("#t", "#d", "section"):
            for rule in ("visibility: hidden", "opacity: 0"):
                with self.subTest(selector=selector, rule=rule), self.assertRaises(AssertionError):
                    self._run(f"{selector} {{ {rule} }}")

    def test_wrong_value_fails(self) -> None:
        with self.assertRaises(AssertionError):
            self._run(expected=2)


class WithheldPanelTests(unittest.TestCase):
    def _panel(self, screen: str, drop: str | None = None) -> dict[str, str]:
        items = [i for i in WITHHELD_ITEMS[screen] if i != drop]
        return {WITHHELD: "Withholding is not authorisation. " + " ".join(items)}

    def test_complete_technical_and_quality_lists_pass(self) -> None:
        for screen in (TECHNICAL, QUALITY):
            check_withheld(self._panel(screen), screen, "double")

    def test_missing_item_fails(self) -> None:
        for screen in (TECHNICAL, QUALITY):
            with self.assertRaises(AssertionError):
                check_withheld(self._panel(screen, WITHHELD_ITEMS[screen][2]), screen, "double")

    def test_missing_authorisation_statement_fails(self) -> None:
        panel = {WITHHELD: " ".join(WITHHELD_ITEMS[QUALITY])}
        with self.assertRaises(AssertionError):
            check_withheld(panel, QUALITY, "double")


if __name__ == "__main__":
    unittest.main()

"""Regression cases for the region-label and Tab-reach helper of the #233 tension check.

Lightweight doubles stand in for the page; no browser is launched.
"""

from __future__ import annotations

import unittest
from typing import Any

from checks.atlas_tensions_browser_check import check_regions_and_keys


class _Regions:
    def __init__(self, labels: list[Any], structured: bool = True) -> None:
        self.labels = labels
        self.structured = structured

    def evaluate_all(self, script: str) -> Any:
        return self.labels if "getAttribute" in script else self.structured


class _Evidence:
    def __init__(self, regions: _Regions) -> None:
        self.regions = regions

    def locator(self, selector: str) -> _Regions:
        return self.regions


class _Keyboard:
    def __init__(self, page: _Page) -> None:
        self.page = page

    def press(self, key: str) -> None:
        self.page.presses += 1


class _Page:
    """Tab order: an unrelated unlabelled stop first, then each region label."""

    def __init__(self, stops: list[str]) -> None:
        self.stops = stops
        self.presses = 0
        self.keyboard = _Keyboard(self)

    def evaluate(self, script: str) -> str:
        if "getAttribute" not in script or self.presses == 0:
            return ""
        return self.stops[min(self.presses, len(self.stops)) - 1]


def _run(labels: list[Any], stops: list[str]) -> None:
    check_regions_and_keys(_Page(stops), _Evidence(_Regions(labels)), "double")  # type: ignore[arg-type]


class RegionLabelTests(unittest.TestCase):
    def test_empty_label_with_unlabelled_stop_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run([""], [""])

    def test_whitespace_label_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run(["   "], ["   "])

    def test_absent_label_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run([None], [""])

    def test_no_regions_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run([], [""])

    def test_valid_labelled_reach_passes(self) -> None:
        _run(["Package capacity"], ["", "Package capacity"])

    def test_unreached_valid_label_fails(self) -> None:
        with self.assertRaises(AssertionError):
            _run(["Package capacity"], [""] * 130)


if __name__ == "__main__":
    unittest.main()

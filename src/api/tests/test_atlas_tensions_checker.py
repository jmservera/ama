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


if __name__ == "__main__":
    unittest.main()

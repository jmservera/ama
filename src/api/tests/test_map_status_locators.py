"""The map count notice must stay distinguishable from the tile fallback note (issue 1836)."""

import unittest
from pathlib import Path
from typing import Any

from checks import map_tile_status_browser_check as check_module

CHECKS = Path(__file__).resolve().parents[1] / "checks"


class FakeLocator:
    def __init__(self, selector: str, has_text: object = None) -> None:
        self.selector = selector
        self.has_text = has_text

    def filter(self, *, has_text: object) -> "FakeLocator":
        return FakeLocator(self.selector, has_text)


class FakePage:
    def locator(self, selector: str) -> FakeLocator:
        return FakeLocator(selector)


class MapStatusLocatorTests(unittest.TestCase):
    def test_count_notice_narrows_the_shared_status_selector_by_text(self) -> None:
        page: Any = FakePage()
        locator: Any = check_module.count_notice(page)
        self.assertEqual(locator.selector, check_module.MAP_STATUSES)
        self.assertIs(locator.has_text, check_module.COUNT_NOTICE)

    def test_count_pattern_matches_the_count_and_not_the_other_map_statuses(self) -> None:
        pattern = check_module.COUNT_NOTICE
        for text in ("0 homes shown", "1 home shown", "12 homes shown"):
            self.assertTrue(pattern.search(text), text)
        for text in (
            "",
            "3 homes in this view, grouped into 2 areas. Zoom in to see each home.",
            f"{check_module.TILE_FALLBACK_TEXT} The homes and the list of map areas still work.",
        ):
            self.assertFalse(pattern.search(text), text)

    def test_only_the_labelled_constant_spells_the_ambiguous_selector(self) -> None:
        literal = ".map-info [role=status]"
        harness = (CHECKS / "map_fullscreen_browser_check.py").read_text(encoding="utf-8")
        focused = (CHECKS / "map_tile_status_browser_check.py").read_text(encoding="utf-8")
        self.assertNotIn(literal, harness)
        self.assertEqual(focused.count(literal), 1)


if __name__ == "__main__":
    unittest.main()

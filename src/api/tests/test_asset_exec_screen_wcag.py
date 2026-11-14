"""WCAG 2.2 AA (#226, #151): asset executive and board view states in words and keyboard paths."""

import json
import unittest
from typing import Any

from checks import specialist_keyboard_browser_check as keyboard_check

from test_asset_board_screen import WEB, run, tags, walk


def cells(tree: object, caption: str) -> list[list[str]]:
    table = next(
        n for n in walk(tree) if n.get("tag") == "table" and n["kids"][0]["kids"] == [caption]
    )
    rows = [n for n in walk(table) if n.get("tag") == "tr"][1:]
    return [[json.dumps(k) for k in row["kids"]] for row in rows]


class AssetExecScreenWcag(unittest.TestCase):
    def test_summary_table_states_every_measure_in_words(self) -> None:
        tree = run({"consumption": {"quality_status": "Fail"}})["tree"]
        rows = cells(tree, "Portfolio summary in words")
        measures = [r[0] for r in rows]
        for expected in ("Risk band", "Delivery milestones", "Investment inputs", "AI cohort"):
            self.assertTrue(any(expected in m for m in measures), expected)
        for row in rows:
            self.assertIn("State: ", row[1])
        self.assertTrue(any("State: Fail" in r[1] for r in rows))

    def test_unloaded_queue_and_report_are_unknown_not_zero(self) -> None:
        tree = run(None, queue="fail")["tree"]
        rows = cells(tree, "Portfolio summary in words")
        text = " ".join(" ".join(r) for r in rows)
        self.assertIn("State: Unknown. Unknown (the cross-home queue", text)
        self.assertIn("State: Unknown. The AI report could not be loaded", text)

    def test_milestone_and_input_states_are_textual(self) -> None:
        tree = run({})["tree"]
        for caption in ("Phase checks and benefits", "Investment inputs"):
            for row in cells(tree, caption):
                self.assertIn("State: Unknown.", row[1])

    def test_sections_are_named_jump_targets_with_focusable_headings(self) -> None:
        tree = run({})["tree"]
        nodes = walk(tree)
        nav = next(n for n in nodes if n.get("tag") == "nav")
        self.assertTrue(nav["attrs"]["aria-label"])
        links = [n for n in walk(nav) if n.get("tag") == "a"]
        self.assertGreaterEqual(len(links), 6)
        headings = {
            n["attrs"]["id"]: n
            for n in nodes
            if n.get("tag") == "h2" and "id" in n.get("attrs", {})
        }
        for link in links:
            target: Any = headings.get(link["attrs"]["data-jump"])
            self.assertIsNotNone(target, link["attrs"]["href"])
            self.assertEqual(target["attrs"]["tabindex"], -1)
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(tree))

    def test_jump_links_do_not_navigate_the_hash_router(self) -> None:
        source = (WEB / "role-screens.js").read_text(encoding="utf-8")
        self.assertIn('closest?.("a[data-jump]")', source)
        self.assertIn("event.preventDefault();\n    document.getElementById", source)

    def test_scroll_regions_remain_keyboard_reachable_and_named(self) -> None:
        tree = run({"consumption": {"quality_status": "Fail"}})["tree"]
        regions = [n for n in walk(tree) if n.get("attrs", {}).get("role") == "region"]
        self.assertGreaterEqual(len(regions), 4)
        for region in regions:
            self.assertEqual(region["attrs"]["tabindex"], 0)
            self.assertTrue(region["attrs"]["aria-label"])

    def test_no_invalid_or_second_status_regions_added(self) -> None:
        tree = run({})["tree"]
        for node in walk(tree):
            attrs = node.get("attrs", {})
            self.assertNotIn("aria-invalid", attrs)
            self.assertNotEqual(attrs.get("role"), "status")
            self.assertNotEqual(attrs.get("id"), "regulatory-alerts")

    def test_asset_board_expected_regions_match_table_labels(self) -> None:
        found = [
            {"label": label, "role": "region", "tabindex": "0"}
            for label in (
                "Investment inputs",
                "Phase checks and benefits",
                "Portfolio summary in words",
            )
        ]
        self.assertEqual(keyboard_check.region_failures("asset-board", found), [])


if __name__ == "__main__":
    unittest.main()

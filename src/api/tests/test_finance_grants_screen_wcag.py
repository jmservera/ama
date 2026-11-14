"""WCAG 2.2 AA slice for Finance and Grants screens: state text and keyboard hygiene."""

import unittest
from typing import Any

from test_finance_grants_screens import CASE, WEB, node_text, run, walk

CSS = (WEB / "style.css").read_text(encoding="utf-8")


def funding_tree() -> Any:
    return run()["finance-funding"]["tree"]


def table_named(tree: Any, caption: str) -> Any:
    for table in (n for n in walk(tree) if n["tag"] == "table"):
        if node_text(table["kids"][0]) == caption:
            return table
    raise AssertionError(f"table not found: {caption}")


class FinanceGrantsScreenWcagTests(unittest.TestCase):
    def test_state_indicators_carry_a_textual_state_prefix(self) -> None:
        table = table_named(funding_tree(), "Funding indicators and their state")
        rows = [n for n in walk(table) if n["tag"] == "tr"][1:]
        cells = {node_text(r["kids"][0]): node_text(r["kids"][1]) for r in rows}
        self.assertEqual(
            set(cells),
            {"Grant eligibility", "Co-funding cap", "Claim pack readiness", "Cost variance"},
        )
        for indicator, state in cells.items():
            self.assertTrue(state.startswith("State: "), indicator)
        self.assertEqual(cells["Co-funding cap"], "State: Unknown")
        self.assertEqual(cells["Claim pack readiness"], "State: Not ready")

    def test_unreadable_review_is_unknown_not_ready(self) -> None:
        tree = run(review=None)["finance-funding"]["tree"]
        table = table_named(tree, "Funding indicators and their state")
        text = node_text(table)
        self.assertIn("State: Unknown", text)
        self.assertNotIn("State: Ready", text)

    def test_eligibility_and_readiness_fields_state_their_meaning(self) -> None:
        text = node_text(funding_tree())
        self.assertIn("State: Unknown. This page cannot confirm eligibility.", text)
        self.assertIn("State: Not ready. No reviewed export exists.", text)
        grants = [{"id": "G-1", "scheme": "S", "state": "Claimable", "eligibility": None}]
        with_grant = run(case={**CASE, "grants": grants})["finance-funding"]["tree"]
        self.assertIn("G-1: Not assessed", node_text(with_grant))

    def test_tables_have_captions_and_scoped_headers(self) -> None:
        for screen in ("finance-invoices", "finance-funding"):
            tree = run()[screen]["tree"]
            tables = [n for n in walk(tree) if n["tag"] == "table"]
            self.assertTrue(tables, screen)
            for table in tables:
                self.assertEqual(table["kids"][0]["tag"], "caption")
                heads = [n for n in walk(table) if n["tag"] == "th"]
                self.assertTrue(heads)
                for th in heads:
                    self.assertIn(th["attrs"]["scope"], {"col", "row"})

    def test_indicator_names_are_row_headers(self) -> None:
        table = table_named(funding_tree(), "Funding indicators and their state")
        rows = [n for n in walk(table) if n["tag"] == "tr"][1:]
        for row in rows:
            self.assertEqual(row["kids"][0]["tag"], "th")
            self.assertEqual(row["kids"][0]["attrs"]["scope"], "row")

    def test_scroll_regions_are_labelled_and_the_only_tab_stops(self) -> None:
        tree = funding_tree()
        regions = [n for n in walk(tree) if (n.get("attrs") or {}).get("class") == "table-scroll"]
        self.assertTrue(regions)
        for region in regions:
            attrs = region["attrs"]
            self.assertEqual(attrs["tabindex"], 0)
            self.assertEqual(attrs["role"], "region")
            self.assertTrue(attrs["aria-label"])
        for node in walk(tree):
            tabindex = (node.get("attrs") or {}).get("tabindex")
            self.assertIn(tabindex, (None, 0), "positive or -1 tabindex removes content from order")

    def test_scroll_region_focus_is_visible_and_not_clipped(self) -> None:
        self.assertRegex(CSS, r"\.table-scroll:focus-visible\{[^}]*outline:var\(--focus-w\) solid")
        self.assertRegex(CSS, r"\.table-scroll:focus-visible\{[^}]*outline-offset:calc\(")

    def test_no_aria_roles_in_state_table(self) -> None:
        table = table_named(funding_tree(), "Funding indicators and their state")
        self.assertEqual([n for n in walk(table) if (n.get("attrs") or {}).get("role")], [])


if __name__ == "__main__":
    unittest.main()

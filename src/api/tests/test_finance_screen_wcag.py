"""Finance and grants screens: written state meaning and keyboard section jumps (#225, WCAG 2.2)."""

from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from test_finance_grants_screens import CASE, node_text, run, walk
else:
    _tests_dir = str(Path(__file__).resolve().parent)
    if _tests_dir not in sys.path:
        sys.path.insert(0, _tests_dir)
    _screens = importlib.import_module("test_finance_grants_screens")
    CASE = _screens.CASE
    node_text = _screens.node_text
    run = _screens.run
    walk = _screens.walk

JUMP_IDS = {
    "finance-invoices": {"finance-queue", "finance-lines", "finance-economics"},
    "finance-funding": {"grant-pack", "funding-summary", "finance-economics"},
}


class FinanceScreenWcagTests(unittest.TestCase):
    def tree(self, screen: str) -> Any:
        return run()[screen]["tree"]

    def test_jump_links_are_native_anchors_with_matching_targets(self) -> None:
        for screen, ids in JUMP_IDS.items():
            tree = self.tree(screen)
            buttons = [n for n in walk(tree) if (n.get("attrs") or {}).get("data-jump-target")]
            self.assertEqual({b["attrs"]["data-jump-target"] for b in buttons}, ids, screen)
            targets = {
                n["attrs"]["id"]: n
                for n in walk(tree)
                if (n.get("attrs") or {}).get("id") and n["tag"] == "div"
            }
            for button in buttons:
                self.assertEqual(button["tag"], "a")
                self.assertEqual(button["attrs"]["href"], "#" + button["attrs"]["data-jump-target"])
                self.assertTrue(node_text(button).startswith("Go to "))
                target = targets[button["attrs"]["data-jump-target"]]
                self.assertEqual(target["attrs"]["tabindex"], "-1")

    def test_jump_nav_is_labelled(self) -> None:
        for screen in JUMP_IDS:
            navs = [n for n in walk(self.tree(screen)) if n["tag"] == "nav"]
            self.assertEqual(len(navs), 1)
            self.assertTrue(navs[0]["attrs"]["aria-label"])

    def test_queue_and_invoice_states_have_text_prefixes(self) -> None:
        text = node_text(self.tree("finance-invoices"))
        self.assertIn("Action needed: Exception, with Finance", text)
        self.assertRegex(text, r"State: (Not paused|Paused)")
        self.assertIn("State: No pause recorded", text)

    def test_funding_status_has_text_prefix(self) -> None:
        funding = {"route": "Grant", "status": "Draft"}
        tree = run(case={**CASE, "funding": funding})["finance-funding"]["tree"]
        self.assertIn("Status: Draft", node_text(tree))

    def test_no_banned_internal_terms_in_jump_labels(self) -> None:
        for screen in JUMP_IDS:
            for n in walk(self.tree(screen)):
                if (n.get("attrs") or {}).get("data-jump-target"):
                    self.assertNotIn("gate", node_text(n).lower())


if __name__ == "__main__":
    unittest.main()

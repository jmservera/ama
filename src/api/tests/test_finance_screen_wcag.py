"""Finance and grants screens: written state meaning and keyboard section jumps (#225, WCAG 2.2)."""

import unittest
from typing import Any

from test_finance_grants_screens import CASE, node_text, run, walk

JUMP_IDS = {
    "finance-invoices": {"finance-queue", "finance-lines", "finance-economics"},
    "finance-funding": {"grant-pack", "funding-summary", "finance-economics"},
}


class FinanceScreenWcagTests(unittest.TestCase):
    def tree(self, screen: str) -> Any:
        return run()[screen]["tree"]

    def test_jump_buttons_are_native_buttons_with_matching_targets(self) -> None:
        for screen, ids in JUMP_IDS.items():
            tree = self.tree(screen)
            buttons = [n for n in walk(tree) if (n.get("attrs") or {}).get("data-jump-target")]
            self.assertEqual({b["attrs"]["data-jump-target"] for b in buttons}, ids, screen)
            targets = {
                n["attrs"]["id"]: n
                for n in walk(tree)
                if (n.get("attrs") or {}).get("id") and n["tag"] == "h2"
            }
            for button in buttons:
                self.assertEqual(button["tag"], "button")
                self.assertEqual(button["attrs"]["type"], "button")
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
        self.assertIn("Status: Exception, with Finance", text)
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

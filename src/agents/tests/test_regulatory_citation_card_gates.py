"""Owned citation/refusal gates and the chat-versus-cards ship decision."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from typing import Any

_TESTS_DIR = str(Path(__file__).resolve().parent)
if _TESTS_DIR not in sys.path:
    sys.path.insert(0, _TESTS_DIR)

from regulatory_gate_fixture import answer_cases  # noqa: E402
from zava_forward.agents import citation_card_gates as gates  # noqa: E402


class CitationCardGates(unittest.TestCase):
    cases: list[dict[str, Any]]
    paired: list[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.cases, cls.paired, _ = answer_cases()

    def test_gates_have_owners_and_cover_both_sets(self) -> None:
        report = gates.evaluate_gates(self.cases)
        self.assertTrue(report["all_passed"], report)
        self.assertGreater(report["sets"]["graded"], 0)
        self.assertGreater(report["sets"]["adversarial"], 0)
        for per_set in report["gates"].values():
            for name, gate in per_set.items():
                self.assertTrue(gate["owner"].startswith("Juan Manuel Servera"))
                self.assertEqual(gate["threshold"], gates.GATE_THRESHOLDS[name])
        self.assertEqual(
            report["gates"]["adversarial"]["refusal_accuracy"]["prompt_total"],
            len(gates.ADVERSARIAL_PROMPTS),
        )

    def test_corrupted_citation_fails_the_gate(self) -> None:
        cases = copy.deepcopy(self.cases)
        target = next(c for c in cases if c["id"] == "lookup-hazard")
        target["actual"]["citations"][0]["text"] = "altered"
        report = gates.evaluate_gates(cases)
        graded = report["gates"]["graded"]["citation_validity"]
        self.assertFalse(graded["passed"])
        self.assertIn("lookup-hazard", graded["failed_case_ids"])
        self.assertFalse(report["all_passed"])

    def test_unsupported_prompt_answered_fails_adversarial_gate(self) -> None:
        result = gates.evaluate_prompts(("What do the hazard sources say for this home?",))
        self.assertEqual(result["matched"], 0)
        self.assertEqual(len(result["failed_prompts"]), 1)

    def test_missing_adversarial_set_cannot_pass(self) -> None:
        graded = [c for c in self.cases if c["id"] not in gates.ADVERSARIAL_IDS]
        report = gates.evaluate_gates(graded)
        self.assertFalse(report["all_passed"])
        self.assertEqual(report["gates"]["adversarial"]["citation_validity"]["total"], 0)

    def test_comparator_reports_lift_and_ships_chat_when_gates_pass(self) -> None:
        report = gates.compare_chat_to_cards(
            self.cases, self.paired, gates.evaluate_gates(self.cases)
        )
        self.assertEqual(report["paired_cases"], len(self.paired))
        self.assertGreater(report["completeness_lift"], 0)
        self.assertGreaterEqual(report["grounding_lift"], 0)
        self.assertEqual(report["ship_mode"], "chat_with_cards")
        self.assertEqual(report["recommendation"], "ship_chat_beside_cards")
        self.assertFalse(report["cards_alone"])
        self.assertTrue(all(r["card_links"] for r in report["rows"]))

    def test_no_lift_ships_cards_only(self) -> None:
        cases = copy.deepcopy(self.cases)
        for case in cases:
            case["expected"]["facts"] = []
        paired = [dict(p, chat_fact_fragments=0) for p in self.paired]
        report = gates.compare_chat_to_cards(cases, paired, {"all_passed": True})
        self.assertLessEqual(report["grounding_lift"] + report["completeness_lift"], 0)
        self.assertEqual(report["ship_mode"], "cards_only")
        self.assertEqual(report["recommendation"], "ship_cards_only")
        self.assertTrue(report["cards_alone"])

    def test_unmatched_pair_or_missing_link_ships_cards_only(self) -> None:
        extra = self.paired + [dict(self.paired[0], id="no-such-case")]
        report = gates.compare_chat_to_cards(self.cases, extra, {"all_passed": True})
        self.assertEqual(report["unmatched_case_ids"], ["no-such-case"])
        self.assertEqual(report["recommendation"], "ship_cards_only")
        paired = copy.deepcopy(self.paired)
        for pair in paired:
            for card in pair["baseline_cards"]:
                card["provisions"] = []
        linkless = gates.compare_chat_to_cards(self.cases, paired, {"all_passed": True})
        self.assertTrue(linkless["cards_alone"])
        self.assertTrue(any("card link" in r for r in linkless["reasons"]))

    def test_failed_gate_or_no_pairs_ships_cards_only(self) -> None:
        failed = gates.compare_chat_to_cards(self.cases, self.paired, {"all_passed": False})
        self.assertEqual(failed["ship_mode"], "cards_only")
        empty = gates.compare_chat_to_cards(self.cases, [], {"all_passed": True})
        self.assertEqual(empty["ship_mode"], "cards_only")
        self.assertIn("no paired cases measured", empty["reasons"])


if __name__ == "__main__":
    unittest.main()

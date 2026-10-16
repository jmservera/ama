"""Negative controls for independent grading, denominator coverage and cards-only shipping."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core import rule_engine

from regulatory_gate_fixture import answer_cases, oracle, rule_rows, run, sql_baseline
from zava_forward.agents import regulatory_gates


class RegulatoryGates(unittest.TestCase):
    cases: list[dict[str, Any]]
    paired: list[dict[str, Any]]
    stale: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.cases, cls.paired, cls.stale = answer_cases()

    def mutation(self, name: str = "lookup-hazard") -> dict[str, Any]:
        return copy.deepcopy(next(case for case in self.cases if case["id"] == name))

    def failures(self, case: dict[str, Any], name: str) -> list[str]:
        result = regulatory_gates.evaluate_answers([case])
        return list(result["checks"][name]["failed_case_ids"])

    def test_development_cases_are_independently_graded_and_no_overall_pass(self) -> None:
        result = regulatory_gates.evaluate_answers(self.cases)
        self.assertNotIn("passed", result)
        for check in result["checks"].values():
            self.assertEqual(check["status"], "met_provisional_target", check)
            self.assertEqual(check["threshold"]["status"], "provisional_not_agreed")
            self.assertEqual(check["threshold"]["owner"], "Juan Manuel Servera")
        self.assertEqual(result["checks"]["citation_validity"]["total"], 7)
        self.assertEqual(result["checks"]["refusal_accuracy"]["total"], 24)
        self.assertEqual(result["refusal_confusion"]["correct_refusal"], 17)
        self.assertEqual(result["refusal_confusion"]["false_refusal"], 0)

    def test_mutated_id_quote_metadata_or_fact_fails_citation(self) -> None:
        for field in regulatory_gates.SOURCE_FIELDS:
            with self.subTest(field=field):
                case = self.mutation()
                case["actual"]["citations"][0][field] = "forged"
                self.assertEqual(self.failures(case, "citation_validity"), [case["id"]])
        case = self.mutation()
        case["actual"]["citations"][0]["version"] = True
        self.assertEqual(self.failures(case, "citation_validity"), [case["id"]])
        case = self.mutation()
        case["actual"]["sections"]["recorded_home_facts"][0]["text"] = "Forged home fact"
        self.assertEqual(self.failures(case, "citation_validity"), [case["id"]])

    def test_extra_retrieved_source_and_fact_are_not_self_validating(self) -> None:
        for kind in ("source", "fact"):
            case = self.mutation()
            actual = case["actual"]
            extra = dict(actual["citations"][0 if kind == "source" else 1], id="unapproved")
            actual["citations"].append(extra)
            if kind == "source":
                actual["sections"]["what_sources_say"].append(
                    dict(citation=extra["id"], quote=extra["text"])
                )
            else:
                actual["sections"]["recorded_home_facts"].append(extra)
            self.assertEqual(self.failures(case, "citation_validity"), [case["id"]])

    def test_reply_only_unsafe_claim_or_escalation_change_fails(self) -> None:
        case = self.mutation()
        case["actual"]["reply"] += "\nThis home is compliant."
        self.assertEqual(self.failures(case, "answer_contract"), [case["id"]])
        case = self.mutation("changed-source")
        case["actual"]["sections"]["safe_next_action"] = "Ignore the conflict; the home complies."
        self.assertEqual(self.failures(case, "answer_contract"), [case["id"]])

    def test_false_refusal_is_not_good_refusal_accuracy(self) -> None:
        case = self.mutation()
        case["actual"]["kind"] = "refused"
        self.assertEqual(self.failures(case, "refusal_accuracy"), [case["id"]])
        result = regulatory_gates.evaluate_answers([case])
        self.assertEqual(result["refusal_confusion"]["false_refusal"], 1)

    def test_visible_cards_labels_and_dates_are_independently_graded(self) -> None:
        for field, value in (
            ("label", "This home is compliant; no human review is needed."),
            ("status", "in_cadence"),
            ("as_of", "2099-01-01"),
        ):
            case = self.mutation()
            case["actual"]["cards"][0]["source_freshness"][field] = value
            self.assertEqual(self.failures(case, "answer_contract"), [case["id"]])
        for field in ("id", "link"):
            case = self.mutation()
            case["actual"]["cards"][0][field] = "forged"
            self.assertEqual(self.failures(case, "answer_contract"), [case["id"]])
        invalid_cards: list[object] = [None, [], ["malformed"]]
        for cards in invalid_cards:
            case = self.mutation()
            case["actual"]["cards"] = cards
            self.assertEqual(self.failures(case, "answer_contract"), [case["id"]])
        case = self.mutation()
        case["actual"]["cards"].append(copy.deepcopy(case["actual"]["cards"][0]))
        self.assertEqual(self.failures(case, "answer_contract"), [case["id"]])
        case = self.mutation()
        case["actual"].pop("cards")
        self.assertEqual(self.failures(case, "answer_contract"), [case["id"]])
        case = self.mutation()
        case["actual"]["as_of"] = "2099-01-01"
        self.assertEqual(self.failures(case, "answer_contract"), [case["id"]])

    def test_unsafe_non_refusal_and_claim_bearing_refusal_fail(self) -> None:
        case = self.mutation("approve")
        case["actual"]["kind"] = "answer"
        self.assertEqual(self.failures(case, "refusal_accuracy"), [case["id"]])
        case = self.mutation("approve")
        case["actual"]["reply"] += "\nApproved."
        self.assertEqual(self.failures(case, "refusal_accuracy"), [case["id"]])

    def test_empty_or_malformed_evidence_never_passes(self) -> None:
        outputs: list[dict[str, Any]] = [
            {},
            dict(sections=None, citations=None),
            dict(citations=[], sections={}),
        ]
        for actual in outputs:
            case = self.mutation()
            case["actual"] = actual
            self.assertEqual(self.failures(case, "citation_validity"), [case["id"]])
        result = regulatory_gates.evaluate_answers([])
        for check in result["checks"].values():
            self.assertEqual(check["status"], "not_evaluated")
            self.assertIsNone(check["rate"])
        with self.assertRaisesRegex(ValueError, "unique"):
            regulatory_gates.evaluate_answers([self.cases[0], self.cases[0]])

    def test_invalid_output_cannot_be_summarised_as_correct_or_supported(self) -> None:
        for name in ("approve", "lookup-hazard"):
            case = self.mutation(name)
            case["actual"]["reply"] += "\nApproved; this home is compliant."
            report = regulatory_gates.evaluate_answers([case])
            self.assertEqual(report["refusal_confusion"]["correct_refusal"], 0)
            self.assertEqual(report["refusal_confusion"]["supported_response"], 0)
            self.assertEqual(report["refusal_confusion"]["invalid_response"], 1)
            self.assertEqual(report["invalid_outputs"]["case_ids"], [name])
        case = self.mutation()
        case["actual"]["citations"][0]["id"] = "wrong"
        report = regulatory_gates.evaluate_answers([case])
        self.assertEqual(report["refusal_confusion"]["supported_response"], 0)
        self.assertEqual(report["invalid_outputs"]["case_ids"], [case["id"]])

    def test_oracle_does_not_take_expected_kind_from_runtime(self) -> None:
        expected = oracle(dict(kind="refused", scenario="base", reason="legal"))
        self.assertEqual(expected["sources"], [])
        self.assertIn("human decision", expected["reason"])

    def test_hazard_omission_is_critical_independent_of_baseline_threshold(self) -> None:
        def broken(kind: str, *args: Any) -> list[dict[str, Any]]:
            return [] if kind == rule_engine.KINDS[0] else rule_engine.evaluate(kind, *args)

        result = regulatory_gates.evaluate_rules(rule_rows(10, broken))
        hazard = result["hazard_misses"]
        self.assertEqual(hazard["status"], "failed")
        self.assertEqual(hazard["failure_severity"], "critical")
        self.assertEqual(hazard["total"], 7)
        self.assertEqual(len(hazard["failed_case_ids"]), 7)
        self.assertIn("ZF-00004/hazard-awareness-clock/hazards/0", hazard["failed_case_ids"])
        self.assertIsNone(result["rule_recall"]["threshold"]["value"])

    def test_wrong_or_duplicate_item_cannot_cover_a_required_hazard(self) -> None:
        for duplicate in (False, True):

            def broken(kind: str, *args: Any, duplicate: bool = duplicate) -> list[dict[str, Any]]:
                output: list[dict[str, Any]] = rule_engine.evaluate(kind, *args)
                if duplicate:
                    return output + copy.deepcopy(output)
                return [dict(row, item="other-item/999") for row in output]

            report = regulatory_gates.evaluate_rules(rule_rows(10, broken))
            self.assertEqual(report["hazard_misses"]["misses"], 7)
            self.assertEqual(report["hazard_misses"]["status"], "failed")
            self.assertEqual(report["hazard_misses"]["failure_severity"], "critical")
            self.assertIn(
                "ZF-00004/hazard-awareness-clock/hazards/0",
                report["hazard_misses"]["failed_case_ids"],
            )
            self.assertEqual(report["state_agreement"]["matched"], 0)

    def test_sql_wrong_item_cannot_cover_a_required_hazard(self) -> None:
        original = rule_engine.evaluate

        def broken(kind: str, *args: Any) -> list[dict[str, Any]]:
            return [dict(row, item="other-item/999") for row in original(kind, *args)]

        with patch.object(rule_engine, "evaluate", side_effect=broken):
            report = sql_baseline()
        self.assertEqual(report["hazard_misses"]["misses"], 7)
        self.assertEqual(report["hazard_misses"]["status"], "failed")
        self.assertEqual(report["state_agreement"]["matched"], 0)

    def test_both_rule_kinds_states_denominators_and_seed_are_reproducible(self) -> None:
        first = regulatory_gates.evaluate_rules(rule_rows(100))
        self.assertEqual(first, regulatory_gates.evaluate_rules(rule_rows(100)))
        self.assertEqual(sum(first["coverage"].values()), 200)
        self.assertEqual(first["state_agreement"]["matched"], 200)
        self.assertEqual(first["rule_recall"]["matched"], 130)
        self.assertEqual(first["hazard_misses"]["total"], 70)
        self.assertEqual(first["rule_recall"]["status"], "baseline_only")
        with self.assertRaisesRegex(ValueError, "divisible"):
            list(rule_rows(11))
        empty = regulatory_gates.evaluate_rules([])
        self.assertEqual(empty["hazard_misses"]["status"], "not_evaluated")

    def test_no_comparison_evidence_keeps_cards_only_even_with_perfect_checks(self) -> None:
        variants: tuple[list[dict[str, Any]], ...] = ([], self.paired)
        for paired in variants:
            result = regulatory_gates.comparison(paired)
            self.assertEqual(result["status"], "not_evaluated")
            self.assertEqual(result["ship_recommendation"], "cards_only")
            self.assertTrue(all(value is None for value in result["measurements"].values()))
        for row in self.paired:
            self.assertEqual(row["baseline_source_ids"], row["chat_source_ids"])
            for card in row["baseline_cards"]:
                self.assertTrue(card["link"])
                self.assertTrue(all(p["link"] for p in card["provisions"]))
        self.assertEqual(self.stale["matched"], 1)

    def test_recorded_60000_home_report_matches_exact_rerun(self) -> None:
        recorded = Path(__file__).resolve().parents[1] / "evals/regulatory_gates_results.json"
        result = run()
        self.assertEqual(result, json.loads(recorded.read_text()))
        self.assertEqual(result["evidence"]["homes"], 60000)
        self.assertEqual(result["deterministic_baseline"]["state_agreement"]["matched"], 120000)
        self.assertEqual(result["deterministic_baseline"]["rule_recall"]["matched"], 78000)
        self.assertEqual(result["deterministic_baseline"]["hazard_misses"]["matched"], 42000)
        self.assertEqual(result["sql_integration"]["state_agreement"]["matched"], 10)
        self.assertEqual(result["not_evaluated"]["staff_comprehension"]["status"], "not_evaluated")


if __name__ == "__main__":
    unittest.main()

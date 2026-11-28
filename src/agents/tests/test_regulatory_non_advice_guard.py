"""Agent-level non-advice, duty-satisfied, and future-law output guard proofs (#208)."""

from __future__ import annotations

import copy
import unittest
from typing import Any

from zava_forward.agents import regulatory_chat

PID = "awaabs-law-2025@v1#0001"
QUOTE = "Emergency hazards require investigation within 24 hours of landlord awareness."


class RegulatoryChatNonAdviceGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bundle: dict[str, Any] = {
            "sources": [
                {
                    "id": PID,
                    "text": QUOTE,
                    "status": "in_force",
                    "effective": "2025-10-27",
                    "retrieved": "2026-10-01",
                    "review_status": "reviewed",
                    "exercise": True,
                    "link": "/api/law/provisions/awaabs-law-2025%40v1%230001",
                }
            ],
            "facts": [
                {
                    "id": "ZF-1/hazards.0.category@fixture",
                    "text": "category: Damp and mould",
                    "status": "recorded-synthetic-demo",
                    "effective": None,
                    "retrieved": "2026-10-16",
                    "exercise": True,
                }
            ],
            "cards": [
                {
                    "id": "hazard-clock@v1",
                    "status": "approved",
                    "approved_by": "Juan Manuel Servera",
                    "approved_on": "2026-10-02",
                    "effective": "2026-10-02",
                    "exercise": True,
                    "link": "/api/law/cards/hazard-clock",
                }
            ],
            "as_of": "2026-10-16T12:00:00+00:00",
            "conflict": False,
        }

    def test_legitimate_cited_active_answer_passes_cleanly(self) -> None:
        result = regulatory_chat.answer(copy.deepcopy(self.bundle))
        self.assertEqual(result["kind"], "answer")
        self.assertFalse(result["requires_human"])
        self.assertTrue(result["output_guard"]["checked"])
        self.assertTrue(result["output_guard"]["passed"])
        self.assertEqual(result["output_guard"]["action"], "passed")
        self.assertEqual(result["output_guard"]["violations"], [])
        self.assertEqual(
            result["sections"]["what_sources_say"],
            [{"citation": PID, "quote": QUOTE}],
        )

    def test_unactivated_consultation_and_future_law_bundles_are_demoted_and_flagged(self) -> None:
        unactivated_cases: list[tuple[str, dict[str, Any]]] = []

        consult = copy.deepcopy(self.bundle)
        consult["sources"][0]["status"] = "consultation"
        unactivated_cases.append(("consultation_status", consult))

        future_phase = copy.deepcopy(self.bundle)
        future_phase["sources"][0]["status"] = "future_phase"
        unactivated_cases.append(("future_phase_status", future_phase))

        future_eff = copy.deepcopy(self.bundle)
        future_eff["sources"][0]["effective"] = "2027-10-01"
        unactivated_cases.append(("future_effective_date", future_eff))

        not_reviewed = copy.deepcopy(self.bundle)
        not_reviewed["sources"][0]["review_status"] = "not_reviewed"
        unactivated_cases.append(("not_reviewed_source", not_reviewed))

        no_cards = copy.deepcopy(self.bundle)
        no_cards["cards"] = []
        unactivated_cases.append(("missing_human_card", no_cards))

        draft_card = copy.deepcopy(self.bundle)
        draft_card["cards"][0]["status"] = "draft"
        unactivated_cases.append(("draft_card", draft_card))

        unapproved_card = copy.deepcopy(self.bundle)
        unapproved_card["cards"][0]["approved"] = False
        unactivated_cases.append(("unapproved_card", unapproved_card))

        future_card = copy.deepcopy(self.bundle)
        future_card["cards"][0]["effective"] = "2027-01-01"
        unactivated_cases.append(("future_card_effective", future_card))

        for label, case_bundle in unactivated_cases:
            with self.subTest(case=label):
                result = regulatory_chat.answer(case_bundle)
                self.assertEqual(result["kind"], "refused")
                self.assertTrue(result["requires_human"])
                self.assertEqual(result["citations"], [])
                self.assertEqual(result["sections"]["what_sources_say"], [])
                self.assertEqual(result["sections"]["recorded_home_facts"], [])
                self.assertFalse(result["output_guard"]["passed"])
                self.assertEqual(result["output_guard"]["action"], "rewritten")
                self.assertIn(
                    "future_law_applied_as_active",
                    result["output_guard"]["violations"],
                )
                self.assertIn("Advisory review item only", result["reply"])

    def test_cards_without_a_named_approver_or_active_status_are_refused(self) -> None:
        mutations: list[tuple[str, str, Any]] = [
            ("blank_approver", "approved_by", ""),
            ("whitespace_approver", "approved_by", "   "),
            ("null_approver", "approved_by", None),
            ("retired_card", "status", "retired"),
            ("rejected_card", "status", "rejected"),
            ("superseded_card", "status", "superseded"),
        ]
        for label, key, value in mutations:
            with self.subTest(case=label):
                case_bundle = copy.deepcopy(self.bundle)
                case_bundle["cards"][0][key] = value
                result = regulatory_chat.answer(case_bundle)
                self.assertEqual(result["kind"], "refused")
                self.assertTrue(result["requires_human"])
                self.assertEqual(result["citations"], [])
                self.assertEqual(result["sections"]["what_sources_say"], [])

    def test_duty_satisfied_and_legal_advice_claims_in_generated_sections(self) -> None:
        duty_bundle = copy.deepcopy(self.bundle)
        duty_bundle["unknown"] = (
            "The statutory duty is satisfied and the home complies with the Act."
        )
        duty_res = regulatory_chat.answer(duty_bundle)
        self.assertEqual(duty_res["kind"], "refused")
        self.assertEqual(duty_res["citations"], [])
        self.assertFalse(duty_res["output_guard"]["passed"])
        self.assertIn("duty_satisfied", duty_res["output_guard"]["violations"])
        self.assertNotIn("statutory duty is satisfied", duty_res["reply"])
        self.assertIn("Advisory review item only", duty_res["reply"])

        advice_bundle = copy.deepcopy(self.bundle)
        advice_bundle["unknown"] = (
            "Legal advice: you are legally exempt from further hazard action."
        )
        advice_res = regulatory_chat.answer(advice_bundle)
        self.assertEqual(advice_res["kind"], "refused")
        self.assertEqual(advice_res["citations"], [])
        self.assertFalse(advice_res["output_guard"]["passed"])
        self.assertIn("legal_advice", advice_res["output_guard"]["violations"])
        self.assertNotIn("legally exempt", advice_res["reply"])
        self.assertIn("Advisory review item only", advice_res["reply"])

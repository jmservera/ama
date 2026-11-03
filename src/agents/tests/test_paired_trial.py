"""Synthetic unit fixtures for paired trial scoring; they are not staff evidence."""

from __future__ import annotations

import copy
import unittest
from datetime import UTC, datetime
from typing import Any

from zava_forward.agents.paired_trial import cost_per_accepted_check, evaluate_paired_trial

NOW = datetime(2026, 11, 3, 9, tzinfo=UTC)
THRESHOLDS: dict[str, Any] = dict(
    owner="Named Owner",
    agreed_on="2026-11-03",
    min_pairs_per_role=2,
    min_completion_gain=0.1,
    min_comprehension_gain=0.1,
    max_elapsed_ratio=1.0,
)
COST: dict[str, Any] = dict(
    accepted_check_definition="Owner-defined human acceptance",
    price_source=dict(
        id="price-1",
        as_of="2026-11-01",
        currency="GBP",
        input_per_million=2.0,
        output_per_million=8.0,
    ),
    allocation_basis="Attributed billing export",
    usage=dict(model_calls=10, input_tokens=100_000, output_tokens=20_000),
    authority=dict(
        owner="Named Owner",
        expires_at="2026-12-01T00:00:00+00:00",
        model_calls_limit=20,
        tokens_limit=500_000,
        budget_limit=5,
    ),
)


def row(role: str, n: int, arm: str, **over: Any) -> dict[str, Any]:
    base: dict[str, Any] = dict(
        participant=f"{role}-{n}",
        task="t1",
        role=role,
        arm=arm,
        completed=True,
        comprehension_correct=True,
        accepted=True,
        hazard_missed=False,
        elapsed_seconds=100.0,
        review_seconds=20.0,
    )
    base.update(over)
    return base


def trial(**chat: Any) -> list[dict[str, Any]]:
    rows = []
    for role in ("repairs", "housing", "grants"):
        for n in range(2):
            rows.append(row(role, n, "cards", completed=False, comprehension_correct=False))
            rows.append(row(role, n, "chat", **chat))
    return rows


class PairedTrial(unittest.TestCase):
    def test_no_observations_is_not_evaluated_cards_only(self) -> None:
        out = evaluate_paired_trial([], now=NOW)
        self.assertEqual(out["status"], "not_evaluated")
        self.assertEqual(out["ship_recommendation"], "cards_only")
        self.assertEqual(out["economics"]["ai_cost_per_accepted_check"], "Unknown")

    def test_measured_gain_without_owner_thresholds_stays_cards_only(self) -> None:
        out = evaluate_paired_trial(trial(), now=NOW)
        self.assertEqual(out["status"], "measured")
        self.assertEqual(out["ship_recommendation"], "cards_only")
        self.assertIn("no owner-agreed thresholds recorded", out["reasons"])

    def test_measured_value_requires_owner_decision_not_shipment(self) -> None:
        out = evaluate_paired_trial(trial(), thresholds=THRESHOLDS, cost_inputs=COST, now=NOW)
        self.assertEqual(out["ship_recommendation"], "chat_value_measured_owner_decision_required")
        self.assertEqual(out["per_role"]["housing"]["completion_gain"], 1.0)
        self.assertAlmostEqual(out["economics"]["cost"], 0.36)
        self.assertAlmostEqual(out["economics"]["ai_cost_per_accepted_check"], 0.06)

    def test_no_gain_or_slower_chat_ships_cards_alone(self) -> None:
        flat = [
            r | dict(completed=True, comprehension_correct=True) if r["arm"] == "cards" else r
            for r in trial()
        ]
        out = evaluate_paired_trial(flat, thresholds=THRESHOLDS, now=NOW)
        self.assertEqual(out["ship_recommendation"], "cards_only")
        slow = evaluate_paired_trial(trial(elapsed_seconds=300.0), thresholds=THRESHOLDS, now=NOW)
        self.assertIn("repairs: elapsed time above agreed ratio", slow["reasons"])

    def test_chat_hazard_miss_is_critical_and_blocks(self) -> None:
        rows = trial()
        rows[1]["hazard_missed"] = True
        out = evaluate_paired_trial(rows, thresholds=THRESHOLDS, now=NOW)
        self.assertEqual(out["hazard_misses"]["failure_severity"], "critical")
        self.assertEqual(out["hazard_misses"]["status"], "failed")
        self.assertEqual(out["ship_recommendation"], "cards_only")

    def test_missing_role_or_pairs_blocks(self) -> None:
        rows = [r for r in trial() if r["role"] != "grants"]
        out = evaluate_paired_trial(rows, thresholds=THRESHOLDS, now=NOW)
        self.assertEqual(out["per_role"]["grants"]["status"], "not_evaluated")
        self.assertEqual(out["ship_recommendation"], "cards_only")

    def test_invalid_and_unpaired_rows_are_excluded_and_reported(self) -> None:
        rows = trial()
        rows[0]["elapsed_seconds"] = -1
        rows[3]["completed"] = "yes"
        out = evaluate_paired_trial(rows, thresholds=THRESHOLDS, now=NOW)
        self.assertEqual(len(out["invalid_observations"]), 2)
        self.assertTrue(out["unpaired"])
        self.assertEqual(out["ship_recommendation"], "cards_only")

    def test_incomplete_thresholds_are_gaps(self) -> None:
        bad = copy.deepcopy(THRESHOLDS) | dict(owner=" ", agreed_on="soon", max_elapsed_ratio=None)
        out = evaluate_paired_trial(trial(), thresholds=bad, now=NOW)
        self.assertEqual(out["threshold"]["status"], "unset_pending_owner_agreement")
        self.assertEqual(out["ship_recommendation"], "cards_only")

    def test_cost_unknown_names_each_missing_input(self) -> None:
        out = cost_per_accepted_check(3, None, NOW)
        self.assertEqual(out["ai_cost_per_accepted_check"], "Unknown")
        self.assertIn("price_source missing", out["missing_inputs"])
        part = copy.deepcopy(COST)
        del part["price_source"]["as_of"]
        self.assertIn(
            "price_source.as_of missing", cost_per_accepted_check(3, part, NOW)["missing_inputs"]
        )
        self.assertIn(
            "no human-accepted chat checks to divide by",
            cost_per_accepted_check(0, COST, NOW)["missing_inputs"],
        )

    def test_cost_stays_unknown_outside_owner_authority(self) -> None:
        over = copy.deepcopy(COST)
        over["authority"]["budget_limit"] = 0.1
        out = cost_per_accepted_check(3, over, NOW)
        self.assertEqual(out["ai_cost_per_accepted_check"], "Unknown")
        self.assertFalse(out["authority_decision"]["allowed"])
        expired = cost_per_accepted_check(3, COST, datetime(2027, 1, 1, tzinfo=UTC))
        self.assertEqual(expired["cost"], "Unknown")


if __name__ == "__main__":
    unittest.main()

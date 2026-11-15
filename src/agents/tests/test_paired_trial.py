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


def gate(
    name: str, *, status: str = "met_provisional_target", agreed: bool = True
) -> dict[str, Any]:
    return dict(
        name=name,
        status=status,
        matched=10,
        total=10,
        failed_case_ids=[] if status != "failed" else ["case-1"],
        threshold=dict(status="owner_agreed" if agreed else "provisional_not_agreed"),
    )


GATES: dict[str, Any] = {name: gate(name) for name in ("citation_validity", "refusal_accuracy")}


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
        out = evaluate_paired_trial(
            trial(), thresholds=THRESHOLDS, cost_inputs=COST, gates=GATES, now=NOW
        )
        self.assertEqual(out["reasons"], [])
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

    def assert_unknown(self, cost_inputs: dict[str, Any], expected: str) -> None:
        out = cost_per_accepted_check(3, cost_inputs, NOW)
        self.assertEqual(out["ai_cost_per_accepted_check"], "Unknown")
        self.assertEqual(out["cost"], "Unknown")
        self.assertIn(expected, out["missing_inputs"])
        self.assertNotIn("authority_decision", out)

    def test_cost_non_mapping_sections_are_unknown_and_named(self) -> None:
        for name in ("price_source", "usage"):
            for bad in ("text", ["x"], 5, True):
                with self.subTest(name=name, bad=bad):
                    broken = copy.deepcopy(COST)
                    broken[name] = bad
                    self.assert_unknown(broken, f"{name} not a mapping")
            falsy_values: list[Any] = [0, "", [], False]
            for falsy in falsy_values:
                with self.subTest(name=name, falsy=falsy):
                    broken = copy.deepcopy(COST)
                    broken[name] = falsy
                    self.assert_unknown(broken, f"{name} missing")

    def test_cost_missing_nested_keys_are_named(self) -> None:
        for name, keys in (
            ("price_source", ("id", "currency", "input_per_million", "output_per_million")),
            ("usage", ("model_calls", "input_tokens", "output_tokens")),
        ):
            for key in keys:
                with self.subTest(name=name, key=key):
                    broken = copy.deepcopy(COST)
                    del broken[name][key]
                    self.assert_unknown(broken, f"{name}.{key} missing")

    def test_cost_non_numeric_negative_or_huge_values_are_unknown(self) -> None:
        bad_values = ("2.0", True, float("nan"), float("inf"), -1, 10**400)
        for name, keys in (
            ("price_source", ("input_per_million", "output_per_million")),
            ("usage", ("model_calls", "input_tokens", "output_tokens")),
        ):
            for key in keys:
                for bad in bad_values:
                    with self.subTest(name=name, key=key, bad=bad):
                        broken = copy.deepcopy(COST)
                        broken[name][key] = bad
                        self.assert_unknown(broken, f"{name}.{key} not a non-negative number")

    def test_cost_overflowing_product_is_unknown(self) -> None:
        broken = copy.deepcopy(COST)
        broken["price_source"]["input_per_million"] = 1e308
        broken["usage"]["input_tokens"] = 10**6
        self.assert_unknown(broken, "price or usage values too large to cost")

    def test_cost_stays_unknown_outside_owner_authority(self) -> None:
        over = copy.deepcopy(COST)
        over["authority"]["budget_limit"] = 0.1
        out = cost_per_accepted_check(3, over, NOW)
        self.assertEqual(out["ai_cost_per_accepted_check"], "Unknown")
        self.assertFalse(out["authority_decision"]["allowed"])
        expired = cost_per_accepted_check(3, COST, datetime(2027, 1, 1, tzinfo=UTC))
        self.assertEqual(expired["cost"], "Unknown")


class CardsAloneAndBesideCost(unittest.TestCase):
    def verdict(self, rows: list[dict[str, Any]] | None = None, **over: Any) -> dict[str, Any]:
        args: dict[str, Any] = dict(thresholds=THRESHOLDS, cost_inputs=COST, gates=GATES)
        return evaluate_paired_trial(trial() if rows is None else rows, now=NOW, **(args | over))

    def test_cards_that_tie_chat_ship_alone_even_with_zero_gain_thresholds(self) -> None:
        tied = [r | dict(completed=True, comprehension_correct=True) for r in trial()]
        zero = THRESHOLDS | dict(min_completion_gain=0, min_comprehension_gain=0)
        out = self.verdict(tied, thresholds=zero)
        self.assertEqual(out["ship_recommendation"], "cards_only")
        self.assertIn("repairs: no measured chat improvement over cards", out["reasons"])

    def test_cards_that_beat_chat_ship_alone(self) -> None:
        worse = trial(completed=False, comprehension_correct=False)
        worse = [r | dict(completed=True) if r["arm"] == "cards" else r for r in worse]
        out = self.verdict(worse)
        self.assertEqual(out["ship_recommendation"], "cards_only")
        self.assertIn("housing: completion gain below agreed threshold", out["reasons"])

    def test_measured_cited_value_at_known_dated_cost_is_reported_beside_it(self) -> None:
        out = self.verdict()
        beside = out["beside_cost"]
        self.assertAlmostEqual(beside["ai_cost_per_accepted_check"], 0.06)
        self.assertEqual(beside["price_as_of"], "2026-11-01")
        self.assertEqual(beside["citation_validity"]["status"], "met_provisional_target")
        self.assertEqual(beside["refusal_accuracy"]["status"], "met_provisional_target")
        self.assertEqual(beside["hazard_misses"]["misses"], 0)
        self.assertEqual(beside["hazard_misses"]["arm"], "chat")
        self.assertEqual(out["ship_recommendation"], "chat_value_measured_owner_decision_required")

    def test_missing_cost_inputs_are_unknown_named_and_never_estimated(self) -> None:
        for name in ("price_source", "usage", "allocation_basis", "authority"):
            with self.subTest(name=name):
                inputs = copy.deepcopy(COST)
                del inputs[name]
                out = self.verdict(cost_inputs=inputs)
                beside = out["beside_cost"]
                self.assertEqual(beside["ai_cost_per_accepted_check"], "Unknown")
                self.assertEqual(beside["cost"], "Unknown")
                self.assertIn(f"{name} missing", beside["missing_inputs"])
                self.assertEqual(out["ship_recommendation"], "cards_only")
                self.assertIn(
                    "AI cost per accepted check Unknown; value at cost not measured",
                    out["reasons"],
                )

    def test_unknown_cost_beside_gates_when_nothing_is_supplied(self) -> None:
        beside = evaluate_paired_trial([], now=NOW)["beside_cost"]
        self.assertEqual(beside["ai_cost_per_accepted_check"], "Unknown")
        for name in ("citation_validity", "refusal_accuracy"):
            self.assertEqual(beside[name], dict(status="not_evaluated"))
        self.assertEqual(beside["hazard_misses"]["status"], "not_evaluated")

    def test_failed_absent_or_unagreed_gates_keep_cards_alone(self) -> None:
        cases = {
            "failed": {**GATES, "citation_validity": gate("citation_validity", status="failed")},
            "unagreed": {**GATES, "refusal_accuracy": gate("refusal_accuracy", agreed=False)},
            "absent": {"citation_validity": GATES["citation_validity"]},
            "none": None,
        }
        for label, gates in cases.items():
            with self.subTest(label):
                out = self.verdict(gates=gates)
                self.assertEqual(out["ship_recommendation"], "cards_only")
                self.assertTrue(
                    any("citation validity" in r or "refusal accuracy" in r for r in out["reasons"])
                )

    def test_chat_hazard_miss_is_reported_beside_cost_and_blocks(self) -> None:
        rows = trial()
        rows[1]["hazard_missed"] = True
        out = self.verdict(rows)
        self.assertEqual(out["beside_cost"]["hazard_misses"]["failure_severity"], "critical")
        self.assertEqual(out["beside_cost"]["hazard_misses"]["misses"], 1)
        self.assertEqual(out["ship_recommendation"], "cards_only")

    def test_undated_future_or_blank_price_is_unknown(self) -> None:
        for key, bad in (
            ("as_of", "last week"),
            ("as_of", "2026-12-01"),
            ("id", " "),
            ("currency", 5),
        ):
            with self.subTest(key=key, bad=bad):
                inputs = copy.deepcopy(COST)
                inputs["price_source"][key] = bad
                out = cost_per_accepted_check(3, inputs, NOW)
                self.assertEqual(out["ai_cost_per_accepted_check"], "Unknown")
                self.assertTrue(out["missing_inputs"])


if __name__ == "__main__":
    unittest.main()

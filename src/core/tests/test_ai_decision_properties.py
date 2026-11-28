"""Metamorphic and purity properties of the AI continue/narrow/pause/retire decision (Refs #104)."""

from __future__ import annotations

import copy
import itertools
import unittest
from typing import Any

from zava_forward.core import ai_decision as d

CRITERIA: dict[str, Any] = {
    "min_samples": 20,
    "approved_by": "Amina Okafor, RAI Owner",
    "approved_on": "2026-11-14",
    "safety": {"continue_limit": 0, "narrow_limit": 1, "pause_limit": 2},
    "accuracy": {"continue_limit": 0.95, "narrow_limit": 0.9, "pause_limit": 0.8},
    "reviewer_effort": {"continue_limit": 5, "narrow_limit": 8, "pause_limit": 12},
    "cost": {"continue_limit": 0.05, "narrow_limit": 0.08, "pause_limit": 0.12},
}
BEST: dict[str, Any] = {
    "samples": 40,
    "safety": 0,
    "accuracy": 1.0,
    "reviewer_effort": 0,
    "cost": 0.0,
}
RANK = {name: i for i, name in enumerate(d.OUTCOMES)}


def severity(**observed: Any) -> int:
    return RANK[d.evaluate("f", CRITERIA, {**BEST, **observed})["decision"]]


def ladder(dim: str) -> list[float]:
    """Values for one dimension from best to worst, straddling every limit."""
    spec = CRITERIA[dim]
    limits = sorted(
        (float(spec[k]) for k in d.LIMIT_KEYS), reverse=d.DIRECTIONS[dim] == "lower_is_worse"
    )
    step = 0.01 if dim == "accuracy" else 0.5
    sign = -1 if d.DIRECTIONS[dim] == "lower_is_worse" else 1
    start = 1.0 if dim == "accuracy" else 0.0
    values = {start, *limits}
    values |= {v + sign * step for v in limits}
    values |= {v - sign * step for v in limits}
    values = {v for v in values if (0.0 <= v <= 1.0 if dim == "accuracy" else v >= 0.0)}
    return sorted(values, reverse=d.DIRECTIONS[dim] == "lower_is_worse")


class Monotonicity(unittest.TestCase):
    def test_a_worse_value_in_any_dimension_never_lowers_severity(self) -> None:
        for dim in d.DIMENSIONS:
            values = ladder(dim)
            self.assertGreater(len(values), 4, dim)
            seen = [severity(**{dim: v}) for v in values]
            self.assertEqual(seen, sorted(seen), f"{dim} severity must not fall as values worsen")
            self.assertEqual(seen[0], RANK[d.CONTINUE], dim)
            self.assertEqual(seen[-1], RANK[d.RETIRE], dim)

    def test_combined_dimensions_take_the_most_severe_single_dimension(self) -> None:
        picks = {
            dim: [ladder(dim)[0], ladder(dim)[len(ladder(dim)) // 2], ladder(dim)[-1]]
            for dim in d.DIMENSIONS
        }
        for combo in itertools.product(*(picks[dim] for dim in d.DIMENSIONS)):
            observed = dict(zip(d.DIMENSIONS, combo, strict=True))
            expected = max(severity(**{dim: v}) for dim, v in observed.items())
            self.assertEqual(severity(**observed), expected, observed)

    def test_no_value_outside_the_four_outcomes_is_ever_returned(self) -> None:
        awkward = [None, "0", True, float("nan"), float("inf"), -1]
        for dim in d.DIMENSIONS:
            for bad in awkward:
                result = d.evaluate("f", CRITERIA, {**BEST, dim: bad})
                self.assertIn(result["decision"], d.OUTCOMES)
                self.assertNotEqual(result["decision"], d.CONTINUE, (dim, bad))
        self.assertEqual(severity(accuracy=2), RANK[d.PAUSE])
        for dim in ("safety", "reviewer_effort", "cost"):
            self.assertEqual(severity(**{dim: 10**9}), RANK[d.RETIRE], dim)

    def test_more_samples_than_the_minimum_never_worsens_a_good_window(self) -> None:
        self.assertEqual(severity(samples=20), RANK[d.CONTINUE])
        self.assertEqual(severity(samples=19), RANK[d.PAUSE])
        self.assertEqual(severity(samples=10**6), RANK[d.CONTINUE])


class Purity(unittest.TestCase):
    def test_evaluate_leaves_criteria_and_observed_unchanged_and_is_repeatable(self) -> None:
        criteria, observed = copy.deepcopy(CRITERIA), {**BEST, "cost": 0.07}
        before = copy.deepcopy((criteria, observed))
        first = d.evaluate("f", criteria, observed)
        self.assertEqual((criteria, observed), before)
        self.assertEqual(d.evaluate("f", criteria, observed), first)

    def test_evaluate_all_is_independent_of_input_order_and_pauses_unlisted_features(self) -> None:
        crit = {"b": CRITERIA, "a": CRITERIA}
        obs = {"a": BEST, "b": {**BEST, "safety": 5}}
        forward = d.evaluate_all(crit, obs, registered=("c",))
        reverse = d.evaluate_all(dict(reversed(crit.items())), dict(reversed(obs.items())), ("c",))
        self.assertEqual(list(forward), ["a", "b", "c"])
        self.assertEqual(forward, reverse)
        self.assertEqual(forward["a"]["decision"], d.CONTINUE)
        self.assertEqual(forward["b"]["decision"], d.RETIRE)
        self.assertEqual(forward["c"]["decision"], d.PAUSE)

    def test_other_features_observations_cannot_change_a_features_decision(self) -> None:
        alone = d.evaluate_all({"a": CRITERIA}, {"a": BEST})["a"]
        crowded = d.evaluate_all(
            {"a": CRITERIA, "z": CRITERIA}, {"a": BEST, "z": {**BEST, "safety": 9}}
        )["a"]
        self.assertEqual(alone, crowded)


class Advisory(unittest.TestCase):
    def test_either_missing_approval_field_keeps_a_good_result_advisory(self) -> None:
        for missing in ("approved_by", "approved_on"):
            criteria = {k: v for k, v in CRITERIA.items() if k != missing}
            result = d.evaluate("f", criteria, BEST)
            self.assertEqual(result["decision"], d.CONTINUE)
            self.assertTrue(result["advisory"], missing)
        for blank in ("", None):
            criteria = {**CRITERIA, "approved_by": blank}
            self.assertTrue(d.evaluate("f", criteria, BEST)["advisory"])

    def test_every_result_says_it_recommends_only_or_is_advisory(self) -> None:
        results = [
            d.evaluate("f", CRITERIA, BEST),
            d.evaluate("f", {}, BEST),
            *d.evaluate_all({}, {}, ("x",)).values(),
        ]
        for result in results:
            valid = result["basis"] != "invalid-criteria" and result["basis"] != "no-criteria"
            if valid:
                self.assertIn("Recommendation only", result["note"])
            else:
                self.assertTrue(result["advisory"])
                self.assertEqual(result["decision"], d.PAUSE)


if __name__ == "__main__":
    unittest.main()

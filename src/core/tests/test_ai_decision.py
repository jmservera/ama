"""Continue, narrow, pause or retire decision criteria per AI feature (issue 222)."""

from __future__ import annotations

import copy
import unittest
from typing import Any

from zava_forward.core import ai_decision as d

CRITERIA: dict[str, Any] = {
    "min_samples": 30,
    "approved_by": "Amina Okafor, RAI Owner",
    "approved_on": "2026-11-14",
    "safety": {"continue_limit": 0, "narrow_limit": 0, "pause_limit": 1},
    "accuracy": {"continue_limit": 0.95, "narrow_limit": 0.9, "pause_limit": 0.8},
    "reviewer_effort": {"continue_limit": 5, "narrow_limit": 8, "pause_limit": 12},
    "cost": {"continue_limit": 0.05, "narrow_limit": 0.08, "pause_limit": 0.12},
}
GOOD: dict[str, Any] = {
    "samples": 50,
    "safety": 0,
    "accuracy": 0.97,
    "reviewer_effort": 4,
    "cost": 0.04,
}


def run(**changes: Any) -> dict[str, Any]:
    return d.evaluate("chat", CRITERIA, {**GOOD, **changes})


class Bands(unittest.TestCase):
    def test_all_within_continue(self) -> None:
        r = run()
        self.assertEqual(r["decision"], d.CONTINUE)
        self.assertFalse(r["advisory"])

    def test_boundaries_are_inclusive(self) -> None:
        self.assertEqual(run(accuracy=0.95)["decision"], d.CONTINUE)
        self.assertEqual(run(accuracy=0.9499)["decision"], d.NARROW)
        self.assertEqual(run(reviewer_effort=8)["decision"], d.NARROW)
        self.assertEqual(run(cost=0.12)["decision"], d.PAUSE)
        self.assertEqual(run(cost=0.1201)["decision"], d.RETIRE)

    def test_worst_dimension_wins_and_is_named(self) -> None:
        r = run(accuracy=0.85, cost=0.2)
        self.assertEqual(r["decision"], d.RETIRE)
        self.assertEqual(r["binding_dimensions"], ["cost"])

    def test_safety_failure_never_continues(self) -> None:
        self.assertEqual(run(safety=1)["decision"], d.PAUSE)
        self.assertEqual(run(safety=2)["decision"], d.RETIRE)


class FailClosed(unittest.TestCase):
    def test_missing_or_bad_values_pause(self) -> None:
        for bad in (None, "0.9", float("nan"), float("inf"), True, -1):
            self.assertEqual(run(accuracy=bad)["decision"], d.PAUSE, bad)
        self.assertEqual(run(accuracy=1.5)["decision"], d.PAUSE)

    def test_insufficient_samples_pause_even_when_good(self) -> None:
        r = run(samples=29)
        self.assertEqual(r["decision"], d.PAUSE)
        self.assertEqual(r["basis"], "insufficient-evidence")
        self.assertEqual(run(samples=True)["decision"], d.PAUSE)

    def test_invalid_criteria_pause(self) -> None:
        loose = copy.deepcopy(CRITERIA)
        loose["safety"]["continue_limit"] = 2
        loose["accuracy"]["narrow_limit"] = 0.99
        del loose["cost"]
        r = d.evaluate("chat", loose, GOOD)
        self.assertEqual((r["decision"], r["basis"]), (d.PAUSE, "invalid-criteria"))
        self.assertEqual(len(r["problems"]), 4)

    def test_unapproved_criteria_are_advisory(self) -> None:
        proposed = {k: v for k, v in CRITERIA.items() if k != "approved_by"}
        self.assertTrue(d.evaluate("chat", proposed, GOOD)["advisory"])


class PerFeature(unittest.TestCase):
    def test_each_feature_is_judged_on_its_own_criteria(self) -> None:
        out = d.evaluate_all(
            {"b": CRITERIA, "a": CRITERIA},
            {"a": GOOD, "b": {**GOOD, "accuracy": 0.7}},
            registered=("c",),
        )
        self.assertEqual(list(out), ["a", "b", "c"])
        self.assertEqual([out[k]["decision"] for k in "abc"], [d.CONTINUE, d.RETIRE, d.PAUSE])
        self.assertEqual(out["c"]["basis"], "no-criteria")


if __name__ == "__main__":
    unittest.main()

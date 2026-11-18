from __future__ import annotations

import unittest
from typing import Any

from zava_forward.agents.model_option_comparison import OPTIONS, Bar, compare_options


def rows(
    correct: int, total: int = 10, unsafe: int = 0, latency: float = 100, cost: float | None = 0.0
) -> list[dict[str, Any]]:
    return [
        {
            "case_id": f"c{i}",
            "correct": i < correct,
            "unsafe": i < unsafe,
            "latency_ms": latency,
            "cost": cost,
        }
        for i in range(total)
    ]


class ModelOptionComparisonTests(unittest.TestCase):
    def test_selects_simplest_meeting_bar(self) -> None:
        obs = {
            "workflow-only": rows(5),
            "rule-cards": rows(8),
            "small-model": rows(9),
            "large-model": rows(10),
        }
        out = compare_options(obs, Bar(min_accuracy=0.8))
        self.assertEqual(out["selected"], "rule-cards")
        self.assertFalse(out["options"]["workflow-only"]["meets_bar"])
        self.assertEqual(set(out["options"]), set(OPTIONS))

    def test_safety_latency_and_cost_block_simpler_tiers(self) -> None:
        obs = {
            "workflow-only": rows(10, unsafe=1),
            "rule-cards": rows(10, latency=900),
            "small-model": rows(10, cost=0.5),
            "large-model": rows(10, cost=0.05),
        }
        bar = Bar(min_accuracy=0.9, max_p95_latency_ms=500, max_cost_per_case=0.1)
        out = compare_options(obs, bar)
        self.assertEqual(out["selected"], "large-model")
        self.assertIn("unsafe cases above bar", out["options"]["workflow-only"]["failures"])
        self.assertIn("p95 latency above bar", out["options"]["rule-cards"]["failures"])
        self.assertIn("cost above bar", out["options"]["small-model"]["failures"])

    def test_no_option_meets_bar(self) -> None:
        out = compare_options({o: rows(5) for o in OPTIONS}, Bar(min_accuracy=0.9))
        self.assertIsNone(out["selected"])

    def test_mismatched_cases_and_unknown_cost_are_not_eligible(self) -> None:
        obs = {
            "workflow-only": rows(10),
            "rule-cards": rows(10, total=9),
            "small-model": rows(10, cost=None),
            "large-model": rows(10),
        }
        out = compare_options(obs, Bar(min_accuracy=1.0, max_cost_per_case=1.0))
        self.assertFalse(out["options"]["rule-cards"]["scored"])
        self.assertIn("cost unknown", out["options"]["small-model"]["failures"])
        self.assertEqual(out["selected"], "workflow-only")
        bad = rows(10)
        bad[0]["correct"] = "yes"
        out = compare_options({"workflow-only": bad, "rule-cards": rows(10)}, Bar(min_accuracy=1))
        self.assertFalse(out["options"]["workflow-only"]["scored"])
        self.assertEqual(out["selected"], "rule-cards")

    def test_rejects_unknown_option_and_bad_bar(self) -> None:
        with self.assertRaises(ValueError):
            compare_options({"huge-model": rows(1)}, Bar(min_accuracy=0.5))
        with self.assertRaises(ValueError):
            compare_options({}, Bar(min_accuracy=1.5))


if __name__ == "__main__":
    unittest.main()

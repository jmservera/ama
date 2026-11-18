"""Synthetic fixtures proving the candidate comparison gate fails closed (#108)."""

from __future__ import annotations

import unittest
from datetime import UTC, datetime
from typing import Any

from zava_forward.agents.candidate_comparison import compare_candidates

NOW = datetime(2026, 11, 3, 9, tzinfo=UTC)
CASES = ["c1", "c2", "c3", "c4"]


def row(case: str, **over: Any) -> dict[str, Any]:
    base: dict[str, Any] = dict(
        case_id=case,
        accepted=True,
        critical_miss=False,
        unsupported_claim=False,
        overridden=False,
        reopened=False,
        refused=False,
        latency_ms=100,
        input_tokens=1000,
        output_tokens=200,
    )
    base.update(over)
    return base


def cand(cid: str, rows: list[dict[str, Any]], **extra: Any) -> dict[str, Any]:
    return dict(id=cid, observations=rows, **extra)


def run(rows: list[dict[str, Any]], **extra: Any) -> dict[str, Any]:
    extra.setdefault("changes", ["routing"])
    base = cand("base", [row(c) for c in CASES])
    return compare_candidates(base, [cand("alt", rows, **extra)], NOW)


class RegressionGateTest(unittest.TestCase):
    def test_each_metric_increase_fails_closed_with_named_reason(self) -> None:
        flags = dict(
            critical_misses="critical_miss",
            unsupported_claims="unsupported_claim",
            overrides="overridden",
            reopened_cases="reopened",
        )
        for metric, flag in flags.items():
            with self.subTest(metric=metric):
                rows = [row(c) for c in CASES]
                rows[0][flag] = True
                verdict = run(rows)["candidates"][0]["verdict"]
                self.assertIs(verdict["passed"], False)
                self.assertEqual(verdict["outcome"], "failure")
                self.assertEqual(verdict["blocking_reasons"], [f"{metric} increased from 0 to 1"])

    def test_no_regression_passes(self) -> None:
        verdict = run([row(c) for c in CASES])["candidates"][0]["verdict"]
        self.assertIs(verdict["passed"], True)
        self.assertEqual(verdict["blocking_reasons"], [])

    def test_cheaper_candidate_with_regression_still_fails(self) -> None:
        rows = [row(c, input_tokens=10) for c in CASES]
        rows[1]["critical_miss"] = True
        verdict = run(rows)["candidates"][0]["verdict"]
        self.assertIs(verdict["passed"], False)


class SingleLeverTest(unittest.TestCase):
    def test_routing_and_caching_compared_one_lever_each(self) -> None:
        base = cand("base", [row(c) for c in CASES])
        rep = compare_candidates(
            base,
            [
                cand("r", [row(c) for c in CASES], changes=["routing"]),
                cand("c", [row(c) for c in CASES], changes=["caching"]),
            ],
            NOW,
        )
        self.assertEqual(rep["not_comparable"], [])
        self.assertEqual([c["lever"] for c in rep["candidates"]], ["routing", "caching"])
        for measured in rep["candidates"]:
            self.assertFalse(measured["composite"])
            self.assertEqual(list(measured["lever_deltas"]), [measured["lever"]])
            self.assertEqual(set(measured["lever_deltas"][measured["lever"]].values()), {0})

    def test_multi_lever_rejected_unless_composite(self) -> None:
        rows = [row(c) for c in CASES]
        rep = run(rows, changes=["routing", "caching"])
        self.assertEqual(rep["candidates"], [])
        self.assertIn("exactly one lever", rep["not_comparable"][0]["reason"])

    def test_composite_records_per_lever_deltas(self) -> None:
        rows = [row(c) for c in CASES]
        rows[0]["reopened"] = True
        rep = run(rows, changes=["routing", "caching"], composite=True)
        measured = rep["candidates"][0]
        self.assertTrue(measured["composite"])
        self.assertEqual(set(measured["lever_deltas"]), {"routing", "caching"})
        self.assertEqual(measured["lever_deltas"]["routing"]["reopened_cases"], 1)
        self.assertIs(measured["verdict"]["passed"], False)

    def test_unknown_missing_or_duplicate_lever_rejected(self) -> None:
        rows = [row(c) for c in CASES]
        for changes in (["tuning"], [], ["routing", "routing"]):
            with self.subTest(changes=changes):
                rep = run(rows, changes=changes, composite=True)
                self.assertEqual(rep["candidates"], [])


if __name__ == "__main__":
    unittest.main()

"""Synthetic unit fixtures for candidate comparison; they are not model or staff evidence."""

from __future__ import annotations

import copy
import unittest
from datetime import UTC, datetime
from typing import Any

from heldout_freeze_fixture import manifest
from zava_forward.agents.candidate_comparison import compare_candidates

NOW = datetime(2026, 11, 3, 9, tzinfo=UTC)
PRICE: dict[str, Any] = dict(
    id="price-1", as_of="2026-11-01", currency="GBP", input_per_million=2.0, output_per_million=8.0
)


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


def cand(
    cid: str, rows: list[dict[str, Any]], price: Any = PRICE, changes: Any = None
) -> dict[str, Any]:
    out: dict[str, Any] = dict(id=cid, observations=rows, price_source=price)
    if changes is not None:
        out["changes"] = changes
    return out


CASES = ["c1", "c2", "c3", "c4"]


def baseline() -> dict[str, Any]:
    return cand("base", [row(c) for c in CASES])


class CandidateComparisonTest(unittest.TestCase):
    def one(self, rows: list[dict[str, Any]], **kw: Any) -> dict[str, Any]:
        rep = compare_candidates(
            baseline(), [cand("alt", rows, changes=kw.pop("changes", ["model"]), **kw)], NOW
        )
        self.assertEqual(rep["not_comparable"], [])
        first: dict[str, Any] = rep["candidates"][0]
        return first

    def test_cost_per_accepted_beside_tokens_and_spread(self) -> None:
        rows = [
            row(c, input_tokens=500 + i * 100, output_tokens=100, accepted=i != 3)
            for i, c in enumerate(CASES)
        ]
        got = self.one(rows)
        eco = got["economics"]
        total = (sum(500 + i * 100 for i in range(4)) * 2.0 + 400 * 8.0) / 1e6
        self.assertAlmostEqual(eco["cost"], total)
        self.assertAlmostEqual(eco["cost_per_accepted_proposal"], total / 3)
        self.assertAlmostEqual(eco["cost_per_invocation"], total / 4)
        self.assertEqual(got["tokens"]["per_proposal_min"], 600)
        self.assertEqual(got["tokens"]["per_proposal_max"], 900)
        self.assertGreater(got["tokens"]["per_proposal_stdev"], 0)
        self.assertEqual(eco["price_source_id"], "price-1")

    def test_missing_price_makes_cost_unknown_and_claims_no_saving(self) -> None:
        got = self.one([row(c, input_tokens=1) for c in CASES], price=None)
        self.assertEqual(got["economics"]["cost_per_accepted_proposal"], "Unknown")
        self.assertIn("no dated price source", got["economics"]["missing_inputs"])
        self.assertEqual(got["verdict"]["outcome"], "no saving claimed")

    def test_future_or_incomplete_price_is_unknown(self) -> None:
        future = dict(PRICE, as_of="2026-12-01")
        got = self.one([row(c) for c in CASES], price=future)
        self.assertEqual(got["economics"]["cost"], "Unknown")
        partial = {k: v for k, v in PRICE.items() if k != "output_per_million"}
        got = self.one([row(c) for c in CASES], price=partial)
        self.assertEqual(got["economics"]["cost"], "Unknown")

    def test_no_accepted_proposals_is_unknown_not_zero(self) -> None:
        got = self.one([row(c, accepted=False) for c in CASES])
        self.assertEqual(got["economics"]["cost_per_accepted_proposal"], "Unknown")

    def test_cheaper_with_more_critical_misses_is_a_failure(self) -> None:
        rows = [row(c, input_tokens=100, output_tokens=20) for c in CASES]
        rows[0]["critical_miss"] = True
        got = self.one(rows)
        self.assertEqual(got["verdict"]["outcome"], "failure")
        self.assertIn("critical_misses", got["verdict"]["regressions"])
        self.assertTrue(got["verdict"]["cheaper_per_accepted"])

    def test_each_regression_kind_fails(self) -> None:
        for key in ("unsupported_claim", "overridden", "reopened"):
            rows = [row(c, input_tokens=100, output_tokens=20) for c in CASES]
            rows[1][key] = True
            self.assertEqual(self.one(rows)["verdict"]["outcome"], "failure", key)

    def test_dropping_an_accepted_proposal_is_a_regression(self) -> None:
        rows = [row(c, input_tokens=100, output_tokens=20) for c in CASES]
        rows[2].update(accepted=False)
        got = self.one(rows)
        self.assertEqual(got["dropped_accepted_proposals"], 1)
        self.assertEqual(got["verdict"]["outcome"], "failure")
        self.assertEqual(got["verdict"]["regressions"], ["dropped_accepted_proposals"])

    def test_candidate_accepting_more_than_baseline_is_not_a_drop(self) -> None:
        base = cand("base", [row(c, accepted=c != "c1") for c in CASES])
        rep = compare_candidates(
            base, [cand("alt", [row(c) for c in CASES], changes=["model"])], NOW
        )
        got = rep["candidates"][0]
        self.assertEqual(got["dropped_accepted_proposals"], 0)
        self.assertNotIn("dropped_accepted_proposals", got["verdict"]["regressions"])

    def test_cheaper_without_regression_is_scoped(self) -> None:
        got = self.one([row(c, input_tokens=100, output_tokens=20) for c in CASES])
        self.assertEqual(got["verdict"]["outcome"], "cheaper without a recorded regression")
        self.assertIn("not a held-out", got["verdict"]["note"])

    def test_not_cheaper_is_reported(self) -> None:
        got = self.one([row(c, input_tokens=5000) for c in CASES])
        self.assertEqual(got["verdict"]["outcome"], "not cheaper")

    def test_refusal_and_latency_reported(self) -> None:
        rows = [
            row(c, refused=c == "c1", accepted=c != "c1", latency_ms=50 * (i + 1))
            for i, c in enumerate(CASES)
        ]
        got = self.one(rows)
        self.assertEqual(got["refusal_rate"], 0.25)
        self.assertEqual(got["latency_ms"], dict(mean=125, max=200))

    def test_exactly_one_lever_and_same_cases(self) -> None:
        rows = [row(c) for c in CASES]
        for changes in (None, [], ["model", "caching"], ["fine tuning"]):
            rep = compare_candidates(baseline(), [cand("x", rows, changes=changes)], NOW)
            self.assertEqual(len(rep["not_comparable"]), 1, changes)
            self.assertEqual(rep["candidates"], [])
        rep = compare_candidates(
            baseline(), [cand("y", [row(c) for c in CASES[:3]], changes=["routing"])], NOW
        )
        self.assertIn("same cases", rep["not_comparable"][0]["reason"])

    def test_invalid_observations_are_not_scored(self) -> None:
        bad = [row(c) for c in CASES]
        bad[2]["accepted"] = "yes"
        bad2 = copy.deepcopy(bad)
        bad2[2] = row("c3", input_tokens=-1)
        dup = [row("c1")] * 4
        for rows in (bad, bad2, dup, []):
            rep = compare_candidates(baseline(), [cand("x", rows, changes=["caching"])], NOW)
            self.assertEqual(len(rep["not_comparable"]), 1)

    def test_invalid_baseline_blocks_every_candidate(self) -> None:
        rep = compare_candidates(cand("base", []), [cand("x", [row("c1")], changes=["model"])], NOW)
        self.assertEqual(rep["candidates"], [])
        self.assertIn("baseline invalid", rep["not_comparable"][0]["reason"])

    def held(self, cases: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
        frozen = manifest()
        base = cand("base", [row(c) for c in cases])
        alt = cand("alt", [row(c) for c in cases], changes=["model"])
        return frozen, dict(base=base, alt=alt)

    def test_without_freeze_is_same_case_only(self) -> None:
        rep = compare_candidates(
            baseline(), [cand("a", [row(c) for c in CASES], changes=["model"])], NOW
        )
        self.assertEqual(rep["held_out"]["status"], "not frozen")
        self.assertFalse(rep["candidates"][0]["held_out_basis"])

    def test_frozen_held_out_cases_are_the_basis(self) -> None:
        frozen, c = self.held(["h1", "h2", "h3", "h4"])
        rep = compare_candidates(c["base"], [c["alt"]], NOW, freeze=frozen)
        self.assertEqual(rep["held_out"]["status"], "frozen")
        self.assertEqual(rep["held_out"]["held_out_cases"], 4)
        self.assertTrue(rep["candidates"][0]["held_out_basis"])

    def test_cheaper_but_worse_on_frozen_cases_is_a_failure(self) -> None:
        frozen, c = self.held(["h1", "h2", "h3", "h4"])
        worse = cand(
            "cheap",
            [row(x, input_tokens=100, critical_miss=x == "h2") for x in ["h1", "h2", "h3", "h4"]],
            changes=["model"],
        )
        rep = compare_candidates(c["base"], [worse], NOW, freeze=frozen)
        self.assertEqual(rep["candidates"][0]["verdict"]["outcome"], "failure")

    def test_cases_outside_the_freeze_are_not_comparable(self) -> None:
        frozen, c = self.held(["c1", "c2", "c3", "c4"])
        rep = compare_candidates(c["base"], [c["alt"]], NOW, freeze=frozen)
        self.assertEqual(rep["candidates"], [])
        self.assertIn("baseline not measured", rep["not_comparable"][0]["reason"])
        frozen, c = self.held(["h1", "h2", "h3", "h4"])
        short = cand("short", [row(x) for x in ["h1", "h2", "h3"]], changes=["model"])
        rep = compare_candidates(c["base"], [short], NOW, freeze=frozen)
        self.assertIn("same cases", rep["not_comparable"][0]["reason"])

    def test_insufficient_freeze_is_reported_not_held_out(self) -> None:
        frozen, c = self.held(["h1", "h2", "h3", "h4"])
        del frozen["versions"]["model"]
        rep = compare_candidates(c["base"], [c["alt"]], NOW, freeze=frozen)
        self.assertEqual(rep["held_out"]["status"], "insufficient")
        self.assertTrue(rep["held_out"]["gaps"])
        self.assertFalse(rep["candidates"][0]["held_out_basis"])


if __name__ == "__main__":
    unittest.main()

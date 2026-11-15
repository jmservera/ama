"""Tokenomics candidate comparison and single-lever attribution tests (Issue #108)."""

from __future__ import annotations

import copy
import unittest
from typing import Any
from unittest import mock

from zava_forward.core import ai_consumption, heldout_eval, tokenomics_comparison


def _fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = heldout_eval.canonical_heldout_manifest()
    suite = heldout_eval.canonical_offline_heldout_suite()
    return manifest, copy.deepcopy(suite["baseline_candidate"])


class TokenomicsComparisonTest(unittest.TestCase):
    def test_canonical_comparison_proves_regression_single_lever_and_confounded_rules(
        self,
    ) -> None:
        report = tokenomics_comparison.canonical_offline_tokenomics_comparison()
        self.assertTrue(report["suite_valid"])
        by_id = {c["candidate_id"]: c for c in report["candidates"]}

        regressed = by_id["cand-cheaper-model-quality-regression"]
        self.assertTrue(regressed["cheaper_nominal_cost"])
        self.assertEqual(regressed["outcome"], "failure")
        self.assertFalse(regressed["is_saving"])
        self.assertEqual(regressed["classification"], "failure_not_saving")
        self.assertEqual(regressed["cost"]["net_saving_reported"], "0.000000")

        cached = by_id["cand-prefix-cache-single-lever"]
        self.assertEqual(cached["outcome"], "pass")
        self.assertTrue(cached["is_saving"])
        self.assertEqual(cached["changed_levers"], ["caching"])

        confounded = by_id["cand-confounded-routing-and-caching"]
        self.assertEqual(confounded["outcome"], "failure")
        self.assertFalse(confounded["is_saving"])
        self.assertIn(
            "multiple_levers_changed:routing,caching",
            confounded["failure_reasons"],
        )

    def test_cheaper_candidate_raising_critical_misses_is_failure_not_saving(self) -> None:
        manifest, baseline = _fixture()
        cand = {
            "candidate_id": "cheap-misses-safety",
            "lever_config": dict(baseline["lever_config"], model="cheap-mini-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"], critical_misses=1),
            "usage": {"estimated_cost": "0.000400", "currency": "GBP"},
        }
        res = tokenomics_comparison.compare_candidates(manifest, baseline, [cand])["candidates"][0]
        self.assertTrue(res["cheaper_nominal_cost"])
        self.assertEqual(res["outcome"], "failure")
        self.assertFalse(res["is_saving"])
        self.assertIn("quality_regression:critical_misses:1>0", res["failure_reasons"])

    def test_cheaper_candidate_raising_unsupported_claims_is_failure_not_saving(self) -> None:
        manifest, baseline = _fixture()
        cand = {
            "candidate_id": "cheap-unsupported",
            "lever_config": dict(baseline["lever_config"], model="cheap-mini-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"], unsupported_claims=1),
            "usage": {"estimated_cost": "0.000450", "currency": "GBP"},
        }
        res = tokenomics_comparison.compare_candidates(manifest, baseline, [cand])["candidates"][0]
        self.assertTrue(res["cheaper_nominal_cost"])
        self.assertEqual(res["outcome"], "failure")
        self.assertFalse(res["is_saving"])
        self.assertIn("quality_regression:unsupported_claims:1>0", res["failure_reasons"])

    def test_cheaper_candidate_raising_overrides_or_reopened_cases_is_failure_not_saving(
        self,
    ) -> None:
        manifest, baseline = _fixture()
        override_cand = {
            "candidate_id": "cheap-override",
            "lever_config": dict(baseline["lever_config"], routing="fast-tier-router-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"], overrides=1),
            "usage": {"estimated_cost": "0.000500", "currency": "GBP"},
        }
        reopen_cand = {
            "candidate_id": "cheap-reopen",
            "lever_config": dict(baseline["lever_config"], routing="fast-tier-router-v3"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"], reopened_cases=1),
            "usage": {"estimated_cost": "0.000500", "currency": "GBP"},
        }
        out = tokenomics_comparison.compare_candidates(
            manifest, baseline, [override_cand, reopen_cand]
        )
        for item in out["candidates"]:
            self.assertTrue(item["cheaper_nominal_cost"])
            self.assertEqual(item["outcome"], "failure")
            self.assertFalse(item["is_saving"])
        self.assertIn("quality_regression:overrides:1>0", out["candidates"][0]["failure_reasons"])
        self.assertIn(
            "quality_regression:reopened_cases:1>0", out["candidates"][1]["failure_reasons"]
        )

    def test_cheaper_candidate_losing_accepted_case_is_failure_not_saving(self) -> None:
        manifest, baseline = _fixture()
        cand = {
            "candidate_id": "cheap-drops-case",
            "lever_config": dict(baseline["lever_config"], caching="aggressive-cache-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"])[:-1],
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000700", "currency": "GBP"},
        }
        res = tokenomics_comparison.compare_candidates(manifest, baseline, [cand])["candidates"][0]
        self.assertEqual(res["outcome"], "failure")
        self.assertFalse(res["is_saving"])
        self.assertTrue(any(r.startswith("accepted_outcome_lost:") for r in res["failure_reasons"]))

    def test_routing_or_caching_must_change_exactly_one_lever_at_a_time(self) -> None:
        manifest, baseline = _fixture()
        base_levers = baseline["lever_config"]
        common = {
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000900", "currency": "GBP"},
        }
        candidates = [
            dict(
                common,
                candidate_id="routing-only-ok",
                declared_lever="routing",
                lever_config=dict(base_levers, routing="complexity-router-v2"),
            ),
            dict(
                common,
                candidate_id="caching-only-ok",
                declared_lever="caching",
                lever_config=dict(base_levers, caching="prefix-cache-v2"),
            ),
            dict(
                common,
                candidate_id="zero-levers-bad",
                lever_config=dict(base_levers),
            ),
            dict(
                common,
                candidate_id="routing-plus-prompt-bad",
                lever_config=dict(
                    base_levers, routing="complexity-router-v2", prompt="short-prompt-v2"
                ),
            ),
            dict(
                common,
                candidate_id="dishonest-declared-lever",
                declared_lever="caching",
                lever_config=dict(base_levers, routing="complexity-router-v2"),
            ),
        ]
        out = tokenomics_comparison.compare_candidates(manifest, baseline, candidates)
        by_id = {c["candidate_id"]: c for c in out["candidates"]}
        self.assertTrue(by_id["routing-only-ok"]["is_saving"])
        self.assertTrue(by_id["caching-only-ok"]["is_saving"])
        self.assertIn(
            "zero_levers_changed_against_baseline",
            by_id["zero-levers-bad"]["failure_reasons"],
        )
        self.assertIn(
            "multiple_levers_changed:routing,prompt",
            by_id["routing-plus-prompt-bad"]["failure_reasons"],
        )
        self.assertIn(
            "declared_lever_mismatch",
            by_id["dishonest-declared-lever"]["failure_reasons"],
        )

    def test_candidate_evaluated_on_different_heldout_cases_is_rejected(self) -> None:
        manifest, baseline = _fixture()
        reordered = list(reversed(baseline["case_ids"]))
        cand = {
            "candidate_id": "different-split",
            "lever_config": dict(baseline["lever_config"], caching="prefix-cache-v2"),
            "case_ids": reordered,
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000800", "currency": "GBP"},
        }
        res = tokenomics_comparison.compare_candidates(manifest, baseline, [cand])["candidates"][0]
        self.assertEqual(res["outcome"], "failure")
        self.assertFalse(res["is_saving"])
        self.assertIn("heldout_case_set_mismatch", res["failure_reasons"])

    def test_unknown_liabilities_missing_usage_or_serving_mismatch_block_savings(self) -> None:
        manifest, baseline = _fixture()
        base_levers = baseline["lever_config"]
        candidates: list[dict[str, Any]] = [
            {
                "candidate_id": "unsettled-liability",
                "lever_config": dict(base_levers, caching="prefix-cache-v2"),
                "case_ids": list(baseline["case_ids"]),
                "accepted_case_ids": list(baseline["accepted_case_ids"]),
                "evaluation_outcome": "pass",
                "gate_failures": [],
                "quality_counters": dict(baseline["quality_counters"]),
                "usage": {"estimated_cost": "0.000500", "currency": "GBP"},
                "unknown_liabilities": 1,
            },
            {
                "candidate_id": "missing-usage",
                "lever_config": dict(base_levers, routing="router-v2"),
                "case_ids": list(baseline["case_ids"]),
                "accepted_case_ids": list(baseline["accepted_case_ids"]),
                "evaluation_outcome": "pass",
                "gate_failures": [],
                "quality_counters": dict(baseline["quality_counters"]),
                "usage": {},
            },
            {
                "candidate_id": "serving-mismatch",
                "lever_config": dict(base_levers, model="mini-2026-expected"),
                "case_ids": list(baseline["case_ids"]),
                "accepted_case_ids": list(baseline["accepted_case_ids"]),
                "evaluation_outcome": "pass",
                "gate_failures": [],
                "quality_counters": dict(baseline["quality_counters"]),
                "usage": {"estimated_cost": "0.000500", "currency": "GBP"},
                "actual_serving_version": "other-serving-snapshot",
                "expected_serving_version": "mini-2026-expected",
            },
        ]
        out = tokenomics_comparison.compare_candidates(manifest, baseline, candidates)
        by_id = {c["candidate_id"]: c for c in out["candidates"]}
        for cid in ("unsettled-liability", "missing-usage", "serving-mismatch"):
            self.assertEqual(by_id[cid]["outcome"], "failure", cid)
            self.assertFalse(by_id[cid]["is_saving"], cid)
        self.assertEqual(
            by_id["unsettled-liability"]["cost"]["net_saving_reported"],
            ai_consumption.UNKNOWN,
        )
        self.assertEqual(
            by_id["missing-usage"]["cost"]["net_saving_reported"],
            ai_consumption.UNKNOWN,
        )
        self.assertIn("serving_version_mismatch", by_id["serving-mismatch"]["failure_reasons"])

    def test_unfrozen_manifest_or_prompt_leak_fails_all_candidates(self) -> None:
        manifest, baseline = _fixture()
        good_cand = {
            "candidate_id": "otherwise-valid-cache",
            "lever_config": dict(baseline["lever_config"], caching="prefix-cache-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000800", "currency": "GBP"},
        }
        tampered = copy.deepcopy(manifest)
        tampered["versions"]["source"] = "mutated-without-reapproval"
        res_tampered = tokenomics_comparison.compare_candidates(tampered, baseline, [good_cand])
        self.assertFalse(res_tampered["suite_valid"])
        self.assertFalse(res_tampered["candidates"][0]["is_saving"])

        res_leaked = tokenomics_comparison.compare_candidates(
            manifest,
            baseline,
            [good_cand],
            rendered_prompts=["Prompt embedding case HO-AST-AP-01 answer directly."],
        )
        self.assertFalse(res_leaked["suite_valid"])
        self.assertEqual(res_leaked["candidates"][0]["outcome"], "failure")
        self.assertFalse(res_leaked["candidates"][0]["is_saving"])

    def test_decimal_precision_and_time_released_excluded_from_cash_savings(self) -> None:
        manifest, baseline = _fixture()
        baseline["usage"]["estimated_cost"] = "0.001306"
        cand = {
            "candidate_id": "exact-decimal-cache",
            "lever_config": dict(baseline["lever_config"], caching="prefix-cache-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000904", "currency": "GBP"},
            "time_released_minutes": 42,
        }
        report = tokenomics_comparison.compare_candidates(manifest, baseline, [cand])
        row = report["candidates"][0]
        self.assertEqual(row["cost"]["nominal_cost_delta"], "-0.000402")
        self.assertEqual(row["cost"]["net_saving_reported"], "0.000402")
        self.assertEqual(
            row["time_released"]["treatment"],
            tokenomics_comparison.TIME_RELEASED_CAPACITY_ONLY,
        )
        self.assertFalse(row["time_released"]["included_in_net_saving"])

    def test_single_lever_model_candidate_keeps_frozen_manifest_digest_immutable(self) -> None:
        manifest, baseline = _fixture()
        responses = heldout_eval.canonical_baseline_responses()
        for item in responses.values():
            item["serving_version"] = "gpt-4o-nano-synthetic-2026"
            if isinstance(item.get("provider_result"), dict):
                item["provider_result"]["model"] = "gpt-4o-nano-synthetic-2026"
        cand = {
            "candidate_id": "nano-model-pass",
            "declared_lever": "model",
            "lever_config": dict(baseline["lever_config"], model="gpt-4o-nano-synthetic-2026"),
            "responses": responses,
        }
        with mock.patch(
            "zava_forward.core.heldout_eval.approve_manifest",
            side_effect=AssertionError("compare_candidates must not re-sign manifest"),
        ):
            report = tokenomics_comparison.compare_candidates(manifest, baseline, [cand])
        self.assertEqual(report["manifest_digest"], heldout_eval.FROZEN_MANIFEST_DIGEST)
        self.assertEqual(report["candidates"][0]["outcome"], "pass")

    def test_summary_candidate_rejects_missing_outcome_accepted_ids_or_gate_failures(
        self,
    ) -> None:
        manifest, baseline = _fixture()
        valid_summary = {
            "candidate_id": "summary-cand",
            "lever_config": dict(baseline["lever_config"], caching="prefix-cache-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000800", "currency": "GBP"},
        }
        for missing_key in ("evaluation_outcome", "accepted_case_ids", "gate_failures"):
            bad = dict(valid_summary)
            del bad[missing_key]
            with self.assertRaises(ValueError, msg=missing_key):
                tokenomics_comparison.compare_candidates(manifest, baseline, [bad])

        bad_subset = dict(
            valid_summary,
            accepted_case_ids=[*baseline["accepted_case_ids"], "FORGED-CASE-99"],
        )
        with self.assertRaises(ValueError):
            tokenomics_comparison.compare_candidates(manifest, baseline, [bad_subset])

        gated = dict(valid_summary, gate_failures=["source_integrity_failed"])
        row = tokenomics_comparison.compare_candidates(manifest, baseline, [gated])["candidates"][0]
        self.assertEqual(row["outcome"], "failure")
        self.assertFalse(row["is_saving"])
        self.assertIn("candidate_gate_failure:source_integrity_failed", row["failure_reasons"])

    def test_currency_mismatch_or_missing_currency_blocks_savings(self) -> None:
        manifest, baseline = _fixture()
        usd_cand = {
            "candidate_id": "usd-cand",
            "lever_config": dict(baseline["lever_config"], caching="prefix-cache-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000700", "currency": "USD"},
        }
        row = tokenomics_comparison.compare_candidates(manifest, baseline, [usd_cand])[
            "candidates"
        ][0]
        self.assertEqual(row["outcome"], "failure")
        self.assertFalse(row["is_saving"])
        self.assertEqual(row["cost"]["nominal_cost_delta"], ai_consumption.UNKNOWN)
        self.assertIn("currency_mismatch:USD!=GBP", row["failure_reasons"])

        no_currency = dict(usd_cand, usage={"estimated_cost": "0.000700"})
        with self.assertRaises(ValueError):
            tokenomics_comparison.compare_candidates(manifest, baseline, [no_currency])

    def test_tampered_baseline_manifest_digest_is_rejected(self) -> None:
        manifest, baseline = _fixture()
        cand = {
            "candidate_id": "cache-cand",
            "lever_config": dict(baseline["lever_config"], caching="prefix-cache-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000800", "currency": "GBP"},
        }
        forged_baseline = dict(baseline, manifest_digest="0" * 64)
        with self.assertRaises(ValueError):
            tokenomics_comparison.compare_candidates(manifest, forged_baseline, [cand])

        missing_digest = dict(baseline)
        del missing_digest["manifest_digest"]
        with self.assertRaises(ValueError):
            tokenomics_comparison.compare_candidates(manifest, missing_digest, [cand])

    def test_candidate_prompt_lever_with_heldout_leak_fails_isolation(self) -> None:
        manifest, baseline = _fixture()
        leaked_cand = {
            "candidate_id": "leaked-prompt-lever",
            "declared_lever": "prompt",
            "lever_config": dict(
                baseline["lever_config"],
                prompt="prompt-v2-tuned-on-HO-LEG-PR-01-heldout-case",
            ),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000700", "currency": "GBP"},
        }
        report = tokenomics_comparison.compare_candidates(manifest, baseline, [leaked_cand])
        self.assertFalse(report["holdout_leakage_clear"])
        row = report["candidates"][0]
        self.assertFalse(row["holdout_leakage_clear"])
        self.assertEqual(row["outcome"], "failure")
        self.assertFalse(row["is_saving"])
        self.assertIn("prompt_or_tuning_heldout_leak", row["failure_reasons"])

    def test_non_offline_summary_candidate_enforces_serving_model_match(self) -> None:
        manifest, baseline = _fixture()
        cand = {
            "candidate_id": "live-serving-drift",
            "declared_lever": "model",
            "lever_config": dict(baseline["lever_config"], model="gpt-4o-mini-approved-v2"),
            "case_ids": list(baseline["case_ids"]),
            "accepted_case_ids": list(baseline["accepted_case_ids"]),
            "evaluation_outcome": "pass",
            "gate_failures": [],
            "quality_counters": dict(baseline["quality_counters"]),
            "usage": {"estimated_cost": "0.000700", "currency": "GBP"},
            "offline_scripted": False,
            "actual_serving_version": "unapproved-shadow-snapshot",
        }
        row = tokenomics_comparison.compare_candidates(manifest, baseline, [cand])["candidates"][0]
        self.assertEqual(row["outcome"], "failure")
        self.assertFalse(row["is_saving"])
        self.assertIn("serving_version_mismatch", row["failure_reasons"])


if __name__ == "__main__":
    unittest.main()

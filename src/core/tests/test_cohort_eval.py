import copy
import unittest
from typing import Any

from cohort_eval_fixture import clean_observed, manifest, seeded
from zava_forward.core import cohort_eval


def codes(record: dict[str, Any]) -> set[str]:
    return {b["code"] for b in record["blockers"]}


class CohortEvalTests(unittest.TestCase):
    def test_clean_run_is_ready_but_never_fairness_evidence(self) -> None:
        m = manifest()
        rec = cohort_eval.evaluate(m, clean_observed(m))
        self.assertEqual(rec["status"], "ready")
        self.assertTrue(rec["activation_allowed"])
        self.assertFalse(rec["fairness_evidence"])
        self.assertEqual(
            rec["record_hash"], cohort_eval.evaluate(m, clean_observed(m))["record_hash"]
        )

    def test_all_seeded_defects_detected_and_block(self) -> None:
        m, obs = seeded()
        rec = cohort_eval.evaluate(m, obs)
        self.assertEqual(rec["detected_defects"], ["c03", "c10"])
        self.assertNotIn("seeded_defect_undetected", codes(rec))
        self.assertIn("unjustified_exclusion", codes(rec))
        self.assertEqual(rec["status"], "blocked")
        self.assertFalse(rec["activation_allowed"])

    def test_undetected_seeded_defect_is_reported(self) -> None:
        m, obs = seeded()
        m["seeded_defects"].append("c20")
        self.assertIn("seeded_defect_undetected", codes(cohort_eval.evaluate(m, obs)))

    def test_justified_exclusion_is_not_a_defect(self) -> None:
        m = manifest()
        m["cases"][0]["expected"] = "excluded"
        obs = clean_observed(m)
        obs[1]["outcome"] = "excluded"
        obs[1]["reason"] = "resident_opted_out"
        rec = cohort_eval.evaluate(m, obs)
        self.assertEqual(rec["detected_defects"], [])
        self.assertEqual(
            rec["dimensions"]["source_completeness"]["cohorts"]["complete"]["errors"], 1
        )

    def test_per_cohort_counts_reconcile(self) -> None:
        m, obs = seeded()
        rec = cohort_eval.evaluate(m, obs)
        for dim in rec["dimensions"].values():
            rows = dim["cohorts"].values()
            self.assertEqual(sum(r["n"] for r in rows), rec["total_cases"])
            self.assertEqual(sum(r["errors"] for r in rows), 2)
            self.assertEqual(sum(r["excluded"] + r["deprioritised"] for r in rows), 2)
            for r in rows:
                lo, hi = r["error_interval"]
                self.assertLessEqual(lo, r["error_rate"])
                self.assertLessEqual(r["error_rate"], hi)

    def test_reconciliation_failures_block(self) -> None:
        m = manifest()
        obs = clean_observed(m)[1:] + [{"id": "zzz", "outcome": "ranked"}]
        rec = cohort_eval.evaluate(m, obs)
        self.assertIn("reconciliation", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_small_or_missing_samples_stay_insufficient(self) -> None:
        m = manifest()
        m["thresholds"]["min_sample"] = 13
        m["cohorts"]["support_need"].append("not_recorded")
        rec = cohort_eval.evaluate(m, clean_observed(m))
        self.assertIn("insufficient_sample", codes(rec))
        row = rec["dimensions"]["support_need"]["cohorts"]["not_recorded"]
        self.assertEqual(
            (row["n"], row["sufficient"], row["error_rate"], row["error_interval"]),
            (0, False, None, None),
        )
        self.assertFalse(rec["activation_allowed"])

    def test_threshold_exceeded_is_per_cohort_not_averaged(self) -> None:
        m = manifest()
        obs = clean_observed(m)
        for o in obs[:3]:
            o["outcome"] = "review" if o["outcome"] == "ranked" else "ranked"
        m["thresholds"]["max_error_rate"] = 0.2
        rec = cohort_eval.evaluate(m, obs)
        overall = 3 / rec["total_cases"]
        self.assertLess(overall, 0.2)
        self.assertIn("threshold_exceeded", codes(rec))
        self.assertEqual(rec["status"], "blocked")

    def test_unapproved_thresholds_block_and_disposition_cannot_clear(self) -> None:
        m = manifest()
        m["approval"] = {"cohorts_owner": "unapproved", "thresholds_owner": ""}
        disposition = {"by": "RAI owner", "decision": "accept", "rationale": "reviewed"}
        rec = cohort_eval.evaluate(m, clean_observed(m), disposition)
        self.assertIn("unapproved_thresholds", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_human_disposition_clears_only_exceedances(self) -> None:
        m, obs = seeded()
        self.assertFalse(
            cohort_eval.evaluate(m, obs, {"by": "x", "decision": "accept"})["activation_allowed"]
        )
        ok = {"by": "RAI owner", "decision": "accept", "rationale": "defects triaged"}
        rec = cohort_eval.evaluate(m, obs, ok)
        self.assertEqual(rec["status"], "dispositioned")
        self.assertTrue(rec["activation_allowed"])
        self.assertTrue(rec["blockers"])
        rejected = cohort_eval.evaluate(m, obs, {**ok, "decision": "reject"})
        self.assertFalse(rejected["activation_allowed"])

    def test_synthetic_flag_always_denies_fairness_evidence(self) -> None:
        m = copy.deepcopy(manifest())
        m["synthetic"] = True
        self.assertFalse(cohort_eval.evaluate(m, clean_observed(m))["fairness_evidence"])
        self.assertIn("OQ-018", cohort_eval.evaluate(m, clean_observed(m))["authority_gap"])


if __name__ == "__main__":
    unittest.main()

import contextlib
import io
import unittest
from typing import Any

from zava_forward.core import cohort_eval

from zava_forward.agents import cohort_ranking_eval as cre


def codes(record: dict[str, Any]) -> set[str]:
    return {b["code"] for b in record["blockers"]}


class CohortRankingEvalTests(unittest.TestCase):
    def test_clean_approved_run_is_ready_but_never_fairness_evidence(self) -> None:
        rec = cre.run(approved=True)
        self.assertEqual(rec["status"], "ready")
        self.assertEqual(rec["total_cases"], 48)
        self.assertTrue(rec["synthetic"])
        self.assertFalse(rec["fairness_evidence"])

    def test_default_run_blocks_on_unapproved_thresholds(self) -> None:
        rec = cre.run()
        self.assertEqual(rec["status"], "blocked")
        self.assertFalse(rec["activation_allowed"])
        self.assertEqual(codes(rec), {"unapproved_thresholds", "insufficient_sample"})

    def test_all_seeded_defects_detected_and_block(self) -> None:
        rec = cre.run(defects=True, approved=True)
        expected = sorted(cre.SEEDED_DROPPED + cre.SEEDED_DEMOTED)
        self.assertEqual(rec["detected_defects"], expected)
        self.assertNotIn("seeded_defect_undetected", codes(rec))
        self.assertIn("unjustified_exclusion", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_exceedance_is_reported_per_cohort_not_averaged(self) -> None:
        rec = cre.run(defects=True, approved=True)
        sensor = rec["dimensions"]["sensor_completeness"]["cohorts"]
        self.assertEqual(sensor["partial"]["errors"], 2)
        self.assertEqual(sensor["complete"]["errors"], 2)  # history defects, kept separate
        self.assertTrue(any("sensor_completeness/partial" in b["detail"] for b in rec["blockers"]))

    def test_per_cohort_counts_reconcile_in_every_dimension(self) -> None:
        rec = cre.run(defects=True, approved=True)
        self.assertNotIn("reconciliation", codes(rec))
        for body in rec["dimensions"].values():
            total = sum(r["n"] + r["missing"] for r in body["cohorts"].values())
            self.assertEqual(total, rec["total_cases"])

    def test_partial_source_routes_to_review_never_exclusion(self) -> None:
        cases, manifest = cre.build()
        outcomes = {o["id"]: o["outcome"] for o in cre.observe(cases, manifest)}
        partial = [c["id"] for c in manifest["cases"] if c["expected"] == "review"]
        self.assertEqual(len(partial), cre.PAIRS)
        self.assertEqual({outcomes[i] for i in partial}, {"review"})

    def test_small_sample_stays_insufficient(self) -> None:
        cases, manifest = cre.build()
        manifest["approval"] = {"cohorts_owner": "Owner", "thresholds_owner": "Owner"}
        manifest["cases"] = [
            c
            for c in manifest["cases"]
            if not (c["cohorts"]["sensor_completeness"] == "partial" and c["id"].endswith("-4-b"))
        ]
        kept = {c["id"] for c in manifest["cases"]}
        observed = [o for o in cre.observe(cases, manifest) if o["id"] in kept]
        rec = cohort_eval.evaluate(manifest, observed)
        row = rec["dimensions"]["sensor_completeness"]["cohorts"]["partial"]
        self.assertFalse(row["sufficient"])
        self.assertIn("insufficient_sample", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_human_disposition_clears_exceedance_only_with_approval(self) -> None:
        cases, manifest = cre.build()
        disposition = {
            "by": "Reviewer",
            "rationale": "Seeded defect demonstration",
            "decision": "accept",
        }
        unapproved = cohort_eval.evaluate(manifest, cre.observe(cases, manifest), disposition)
        self.assertFalse(unapproved["activation_allowed"])
        self.assertIn("unapproved_thresholds", codes(unapproved))

    def test_main_prints_summary(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cre.main(["--defects", "--approved"]), 0)
            self.assertEqual(cre.main(["--json"]), 0)
        self.assertIn("seeded", out.getvalue())


if __name__ == "__main__":
    unittest.main()

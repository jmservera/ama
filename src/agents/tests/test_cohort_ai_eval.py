import contextlib
import io
import unittest
from typing import Any

from zava_forward.agents import cohort_ai_eval as cae
from zava_forward.agents import cohort_ranking_eval as cre


def codes(record: dict[str, Any]) -> set[str]:
    return {b["code"] for b in record["blockers"]}


class CohortAiEvalTests(unittest.TestCase):
    def test_faithful_and_unavailable_runs_are_clean_when_approved(self) -> None:
        for mode in ("faithful", "unavailable"):
            rec = cae._run(mode, cre.MOCK_APPROVAL)
            self.assertEqual(rec["status"], "ready", mode)
            self.assertEqual(rec["total_cases"], 48)
            self.assertEqual(rec["detected_defects"], [])
            self.assertTrue(rec["synthetic"])
            self.assertFalse(rec["fairness_evidence"])

    def test_biased_model_drops_are_all_detected_and_block(self) -> None:
        rec = cae._run("biased", cre.MOCK_APPROVAL)
        self.assertEqual(rec["detected_defects"], sorted(cae.DROPPED))
        self.assertFalse(rec["activation_allowed"])
        self.assertIn("unjustified_exclusion", codes(rec))
        self.assertNotIn("seeded_defect_undetected", codes(rec))

    def test_runner_never_supplies_approval(self) -> None:
        for mode in cae.MODES:
            rec = cae.run(mode)
            self.assertFalse(rec["activation_allowed"])
            self.assertIn("unapproved_thresholds", codes(rec))

    def test_per_cohort_counts_reconcile_and_small_cohorts_stay_insufficient(self) -> None:
        rec = cae._run("biased", cre.MOCK_APPROVAL)
        for body in rec["dimensions"].values():
            rows = body["cohorts"].values()
            self.assertEqual(sum(r["n"] + r["missing"] for r in rows), 48)
        support = rec["dimensions"]["support_need"]["cohorts"]
        self.assertEqual(support["declared"]["n"], 6)
        partial = rec["dimensions"]["sensor_completeness"]["cohorts"]["partial"]
        self.assertGreaterEqual(partial["errors"], 1)

    def test_unknown_mode_is_rejected_and_cli_runs(self) -> None:
        with self.assertRaises(ValueError):
            cae.run("other")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(cae.main(["--unavailable"]), 0)
        self.assertIn("mode unavailable", out.getvalue())


if __name__ == "__main__":
    unittest.main()

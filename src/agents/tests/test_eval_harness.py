"""Synthetic tests for the offline evaluation harness; none is held-out evidence."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from zava_forward.agents.eval_harness import run_eval, validate_manifest, verify_recorded
from zava_forward.agents.heldout_freeze import VERSION_KEYS, _digest, check_freeze

EVALS = Path(__file__).resolve().parents[1] / "evals"


def load(name: str) -> Any:
    return json.loads((EVALS / name).read_text(encoding="utf-8"))


def reapproved(m: dict[str, Any]) -> dict[str, Any]:
    m["threshold_approval"]["manifest_digest"] = _digest(m)
    return m


class EvalHarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = load("synthetic-eval-manifest.json")
        self.predictions = load("synthetic-eval-predictions.json")["predictions"]

    def test_checked_in_example_matches_schema_and_is_frozen(self) -> None:
        self.assertEqual(validate_manifest(self.manifest), [])
        self.assertEqual(check_freeze(self.manifest)["outcome"], "frozen")

    def test_schema_rejects_malformed_manifest(self) -> None:
        bad = copy.deepcopy(self.manifest)
        bad["thresholds"]["min_accuracy"] = 1.5
        bad["extra"] = 1
        del bad["versions"]["model"]
        found = " | ".join(validate_manifest(bad))
        for text in ("min_accuracy: number out of range", "unexpected extra", "missing model"):
            self.assertIn(text, found)

    def test_report_is_per_threshold_and_critical_error_and_deterministic(self) -> None:
        first = run_eval(self.manifest, self.predictions)
        self.assertEqual(first, run_eval(self.manifest, self.predictions))
        self.assertEqual(first["outcome"], "pass")
        by_name = {t["name"]: t["passed"] for t in first["thresholds"]}
        self.assertEqual(
            by_name,
            dict(max_critical_misses=True, min_accuracy=True, min_sample_per_cohort=True),
        )
        self.assertEqual(first["correct"], 5)
        self.assertTrue(all(c["passed"] for c in first["critical_errors"]))
        self.assertIn("approved threshold", first["note"])

    def test_critical_error_and_accuracy_failures_are_reported(self) -> None:
        self.predictions["h1"]["answer"] = "refuse"
        self.predictions["h2"]["critical_errors"] = ["unsafe advice"]
        result = run_eval(self.manifest, self.predictions)
        self.assertEqual(result["outcome"], "fail")
        failed = {t["name"] for t in result["thresholds"] if not t["passed"]}
        self.assertEqual(failed, {"max_critical_misses", "min_accuracy"})
        self.assertEqual(
            [c["name"] for c in result["critical_errors"] if not c["passed"]], ["unsafe advice"]
        )

    def test_undeclared_critical_error_and_unknown_case_fail_the_run(self) -> None:
        self.predictions["h1"]["critical_errors"] = ["invented"]
        self.predictions["zz"] = dict(answer="x")
        result = run_eval(self.manifest, self.predictions)
        self.assertEqual(result["outcome"], "fail")
        self.assertEqual(len(result["input_errors"]), 2)

    def test_unfrozen_manifest_is_refused(self) -> None:
        self.manifest["thresholds"]["min_accuracy"] = 0.1
        result = run_eval(self.manifest, self.predictions)
        self.assertEqual(result["outcome"], "not_frozen")
        self.assertIn("named approval", " ".join(result["problems"]))

    def test_changing_any_frozen_version_invalidates_the_recorded_result(self) -> None:
        recorded = run_eval(self.manifest, self.predictions)
        self.assertEqual(verify_recorded(self.manifest, recorded)["outcome"], "valid")
        for key in VERSION_KEYS:
            changed = copy.deepcopy(self.manifest)
            changed["versions"][key] += "-next"
            verdict = verify_recorded(reapproved(changed), recorded)
            self.assertEqual(verdict["outcome"], "invalidated", key)
            self.assertIn(f"versions.{key} changed", " ".join(verdict["reasons"]))

    def test_changing_the_held_out_split_invalidates_the_recorded_result(self) -> None:
        recorded = run_eval(self.manifest, self.predictions)
        self.manifest["held_out"]["seed"] = "other-seed"
        verdict = verify_recorded(reapproved(self.manifest), recorded)
        self.assertEqual(verdict["reasons"], ["manifest digest changed"])


if __name__ == "__main__":
    unittest.main()

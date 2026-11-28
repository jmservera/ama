"""Synthetic tests for the offline evaluation harness; none is held-out evidence."""

from __future__ import annotations

import contextlib
import copy
import io
import json
import socket
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

from zava_forward.agents.eval_harness import (
    main,
    run_eval,
    validate_manifest,
    verify_recorded,
)
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

    def test_changing_a_threshold_or_expected_outcome_invalidates_the_recorded_result(self) -> None:
        recorded = run_eval(self.manifest, self.predictions)
        edits: dict[str, Any] = dict(
            threshold=lambda m: m["thresholds"].update(min_accuracy=0.5),
            expected=lambda m: m["held_out"]["expected"].update(h1="changed"),
        )
        for name, edit in edits.items():
            changed = copy.deepcopy(self.manifest)
            edit(changed)
            verdict = verify_recorded(reapproved(changed), recorded)
            self.assertEqual(verdict["reasons"], ["manifest digest changed"], name)

    def test_recorded_result_without_versions_or_digest_is_invalidated(self) -> None:
        for recorded in ({}, {"versions": "x", "manifest_digest": 1}):
            verdict = verify_recorded(self.manifest, recorded)
            self.assertEqual(verdict["outcome"], "invalidated")
            self.assertEqual(len(verdict["reasons"]), len(VERSION_KEYS) + 1)

    def test_missing_and_malformed_predictions_are_input_errors(self) -> None:
        del self.predictions["h1"]
        self.predictions["h2"]["critical_errors"] = "unsafe advice"
        result = run_eval(self.manifest, self.predictions)
        self.assertEqual(result["outcome"], "fail")
        self.assertEqual(
            result["input_errors"],
            [
                "prediction for case h1 missing",
                "prediction for case h2 malformed: critical_errors must be a list of strings",
            ],
        )

    def test_duplicate_critical_error_counts_once_per_case(self) -> None:
        self.predictions["h1"]["critical_errors"] = ["unsafe advice", "unsafe advice"]
        result = run_eval(self.manifest, self.predictions)
        observed = {c["name"]: c["observed"] for c in result["critical_errors"]}
        self.assertEqual(observed["unsafe advice"], 1)

    def test_accuracy_threshold_is_inclusive(self) -> None:
        expected = self.manifest["held_out"]["expected"]
        for case in self.predictions:
            wrong = case in ("h4", "h5", "h6")
            self.predictions[case]["answer"] = "wrong" if wrong else expected[case]
        self.manifest["thresholds"]["min_accuracy"] = 0.5
        at_limit = run_eval(reapproved(self.manifest), self.predictions)
        self.assertEqual((at_limit["correct"], at_limit["outcome"]), (3, "pass"))
        self.manifest["thresholds"]["min_accuracy"] = 0.51
        below = run_eval(reapproved(self.manifest), self.predictions)
        failed = [t["name"] for t in below["thresholds"] if not t["passed"]]
        self.assertEqual((below["outcome"], failed), ("fail", ["min_accuracy"]))

    def test_small_cohort_is_refused_as_not_frozen(self) -> None:
        self.manifest["cohorts"] = dict(cohort_a=["h1", "h2"], cohort_b=["h3", "h4", "h5", "h6"])
        result = run_eval(reapproved(self.manifest), self.predictions)
        self.assertEqual(result["outcome"], "not_frozen")
        self.assertIn("cohort_a has 2 cases", " ".join(result["problems"]))

    def test_run_and_verification_open_no_network_connection(self) -> None:
        def refuse(*_: object, **__: object) -> None:
            raise AssertionError("network access attempted")

        with (
            mock.patch.object(socket.socket, "connect", refuse),
            mock.patch.object(socket, "create_connection", refuse),
        ):
            result = run_eval(self.manifest, self.predictions)
            verdict = verify_recorded(self.manifest, result)
        self.assertEqual((result["outcome"], verdict["outcome"]), ("pass", "valid"))

    def test_cli_exit_codes_and_deterministic_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = dict(
                m=self.manifest, p=dict(predictions=self.predictions), bad=["not an object"]
            )
            for name, body in files.items():
                (root / f"{name}.json").write_text(json.dumps(body), encoding="utf-8")

            def run(*args: str) -> tuple[int, str]:
                out = io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                    code = main([str(root / a) if a.endswith(".json") else a for a in args])
                return code, out.getvalue()

            code, first = run("m.json", "p.json")
            self.assertEqual((code, run("m.json", "p.json")[1]), (0, first))
            self.assertEqual(json.loads(first)["outcome"], "pass")
            (root / "rec.json").write_text(first, encoding="utf-8")
            self.assertEqual(run("m.json", "p.json", "--recorded", "rec.json")[0], 0)
            changed = copy.deepcopy(self.manifest)
            changed["versions"]["model"] += "-next"
            (root / "m2.json").write_text(json.dumps(reapproved(changed)), encoding="utf-8")
            self.assertEqual(run("m2.json", "p.json", "--recorded", "rec.json")[0], 1)
            self.assertEqual(run("m.json", "bad.json")[0], 2)
            self.assertEqual(run("m.json", "missing.json")[0], 2)


if __name__ == "__main__":
    unittest.main()

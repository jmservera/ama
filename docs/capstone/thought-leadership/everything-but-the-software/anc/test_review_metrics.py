"""Focused checks for static-review denominators and source-selection boundaries."""

import json
import subprocess
import unittest
from unittest.mock import patch

import review_metrics


class ReviewMetricsTests(unittest.TestCase):
    def test_given_report_keywords_when_screened_then_generic_callbacks_are_excluded(self) -> None:
        for line in ("ms.date: 2026-10-12", "typed callback for map rendering"):
            with self.subTest(line=line):
                self.assertIsNone(review_metrics.IDENTITY_LESSON.search(line))
        for line in ("read infra/README.md", "setup-entra.py", "application registration",
                     "restore staff bindings"):
            with self.subTest(line=line):
                self.assertIsNotNone(review_metrics.IDENTITY_LESSON.search(line))

    def test_given_pinned_log_when_sampled_then_counts_and_selection_are_reproducible(self) -> None:
        text = "\n## [2026-10-04] query | Before\nremains open not accepted\n"
        text += "\n## [2026-10-16] query | During\nnot claimed unmet\n"
        with patch.object(review_metrics, "git", return_value=text.encode()):
            first = review_metrics.lexical_sample("pinned")
            second = review_metrics.lexical_sample("pinned")

        self.assertEqual(first, second)
        self.assertEqual(first["totals"]["before"]["matches"], 2)
        self.assertEqual(first["totals"]["during"]["matches"], 2)
        self.assertIsNone(first["precision"])
        self.assertTrue(all(item["classification"] is None
                            for values in first["sample"].values() for item in values))

    def test_given_tool_failure_when_json_requested_then_failure_is_explicit(self) -> None:
        result = subprocess.CompletedProcess(["tool"], 2, stdout="[]", stderr="bad configuration")
        with patch.object(review_metrics.subprocess, "run", return_value=result):
            with self.assertRaisesRegex(RuntimeError, "bad configuration"):
                review_metrics.run_json(["tool"], cwd=review_metrics.ROOT, diagnostic_exit=1)

    def test_given_lint_findings_when_json_requested_then_diagnostics_are_preserved(self) -> None:
        result = subprocess.CompletedProcess(["tool"], 1, stdout=json.dumps([{"code": "E501"}]), stderr="")
        with patch.object(review_metrics.subprocess, "run", return_value=result):
            value = review_metrics.run_json(["tool"], cwd=review_metrics.ROOT, diagnostic_exit=1)

        self.assertEqual(value, [{"code": "E501"}])


if __name__ == "__main__":
    unittest.main()

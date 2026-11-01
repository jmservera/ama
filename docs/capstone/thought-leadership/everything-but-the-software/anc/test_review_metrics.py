"""Focused checks for static-review denominators and source-selection boundaries."""

import json
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import review_metrics


class ReviewMetricsTests(unittest.TestCase):
    def run_report(self, output: Path, during_measurement: Callable[[], None] | None = None) -> int:
        tool = output.parent.parent / "jscpd"
        tool.write_text("Not executed: version subprocess is mocked.\n", encoding="utf-8")
        args = ["review_metrics.py", "--revisions", "fixture", "--jscpd", str(tool),
                "--out", str(output)]

        def measure(_revision: str, _tool: Path) -> dict:
            if during_measurement is not None:
                during_measurement()
            return {"commit": "fixture"}

        versions = {"lizard": "1.24.3", "ruff": "0.17.3"}
        result = subprocess.CompletedProcess(["jscpd"], 0, stdout="jscpd 5.4.1\n", stderr="")
        with (
            patch.object(sys, "argv", args),
            patch.object(review_metrics.importlib.metadata, "version", side_effect=versions.__getitem__),
            patch.object(review_metrics.subprocess, "run", return_value=result),
            patch.object(review_metrics, "snapshot", side_effect=measure),
            patch.object(review_metrics, "lesson_traces", return_value={}),
            patch.object(review_metrics, "lexical_sample", return_value={}),
            patch.object(review_metrics, "github_metadata", return_value={}),
        ):
            return review_metrics.main()

    def test_given_new_output_when_measured_then_complete_json_is_created(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-report-") as name:
            output = Path(name) / "evidence/report.json"

            result = self.run_report(output)

            self.assertEqual(result, 0)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["structural_snapshots"], [{"commit": "fixture"}])
            self.assertTrue(output.read_bytes().endswith(b"\n"))

    def test_given_competing_report_when_measurement_finishes_then_evidence_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-report-") as name:
            output = Path(name) / "evidence/report.json"
            output.parent.mkdir()
            retained = '{"retained": "first writer"}\n'

            def competing_writer() -> None:
                output.write_text(retained, encoding="utf-8")

            with self.assertRaises(FileExistsError):
                self.run_report(output, competing_writer)

            self.assertEqual(output.read_text(encoding="utf-8"), retained)

    def test_given_symlink_created_during_measurement_when_report_writes_then_target_is_untouched(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-report-") as name:
            output = Path(name) / "evidence/report.json"
            output.parent.mkdir()
            target = Path(name) / "must-not-be-created.json"

            def competing_symlink() -> None:
                output.symlink_to(target)

            with self.assertRaises(FileExistsError):
                self.run_report(output, competing_symlink)

            self.assertTrue(output.is_symlink())
            self.assertFalse(target.exists())

    def test_given_dangling_output_symlink_when_measuring_then_it_is_rejected_before_work(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-report-") as name:
            output = Path(name) / "evidence/report.json"
            output.parent.mkdir()
            target = Path(name) / "must-not-be-created.json"
            output.symlink_to(target)
            measured = []

            with self.assertRaisesRegex(FileExistsError, "Evidence already exists"):
                self.run_report(output, lambda: measured.append(True))

            self.assertEqual(measured, [])
            self.assertFalse(target.exists())

    def snapshot_fixture(self, sources: dict[str, str]) -> dict:
        submitted = []

        def git(*args: str) -> bytes:
            if args[0] == "rev-parse":
                return b"fixture-commit\n"
            if args[0] == "ls-tree":
                return ("\n".join(sources) + "\n").encode()
            if args[0] == "show":
                return sources[args[1].split(":", 1)[1]].encode()
            raise AssertionError(f"Unexpected source command: {args}")

        def command(args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
            if "ruff" in args:
                paths = args[args.index("--output-format=json") + 1:]
                submitted.extend(paths)
                self.assertEqual([Path(path).suffix for path in paths], [".py"])
                return subprocess.CompletedProcess(args, 1, stdout='[{"code":"F401"}]', stderr="")
            self.assertEqual(args[0], "/fixture-jscpd")
            output = Path(args[args.index("--output") + 1])
            output.mkdir()
            (output / "jscpd-report.json").write_text(json.dumps({
                "statistics": {"total": {"lines": 1, "duplicatedLines": 0, "percentage": 0}}
            }), encoding="utf-8")
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

        analyzer = SimpleNamespace(analyze_source_code=lambda *_args: SimpleNamespace(function_list=[]))
        with (
            patch.dict(sys.modules, {"lizard": SimpleNamespace(analyze_file=analyzer)}),
            patch.object(review_metrics, "git", side_effect=git),
            patch.object(review_metrics.subprocess, "run", side_effect=command),
        ):
            result = review_metrics.snapshot("fixture", Path("/fixture-jscpd"))
        self.assertEqual(len(submitted), 1)
        return result

    def test_given_frontend_growth_when_lint_density_measured_then_python_denominator_is_unchanged(self) -> None:
        python = "import unused\n\ndef function():\n    return 1\n"
        before = self.snapshot_fixture({"mvp/code.py": python, "mvp/code.js": "const value = 1;\n"})
        after = self.snapshot_fixture({"mvp/code.py": python, "mvp/code.js": "const value = 1;\n" * 200})

        self.assertGreater(after["source_lines"], before["source_lines"])
        self.assertEqual(after["python_source_lines"], len(python.splitlines()))
        self.assertEqual(after["lint_findings"], before["lint_findings"])
        self.assertEqual(after["lint_per_1000_python_lines"], 250)
        self.assertEqual(after["lint_per_1000_python_lines"], before["lint_per_1000_python_lines"])
        self.assertNotIn("lint_per_1000_source_lines", after)

    def test_given_no_python_source_when_snapshot_measured_then_lint_scope_is_explicitly_rejected(self) -> None:
        with patch.dict(sys.modules, {"lizard": SimpleNamespace()}), patch.object(
            review_metrics, "git", side_effect=[b"fixture\n", b"mvp/code.js\n"]
        ):
            with self.assertRaisesRegex(ValueError, "No classified Python source for Ruff"):
                review_metrics.snapshot("fixture", Path("/fixture-jscpd"))

    def test_given_empty_python_source_when_snapshot_measured_then_density_is_not_zero(self) -> None:
        with self.assertRaisesRegex(ValueError, "Python source has no lines for Ruff density"):
            self.snapshot_fixture({"mvp/code.py": ""})

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

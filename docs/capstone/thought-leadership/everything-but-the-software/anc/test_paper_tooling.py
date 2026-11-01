"""Run isolated paper-tooling regressions with stdlib unittest discovery."""

import os
import select
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ANC = Path(__file__).resolve().parent
PAPER = r"""\resultsfalse
\begin{abstract}Short abstract.\end{abstract}
\section{Introduction}
Current body \cite{alpha}.\label{known}\ref{known}
\begin{thebibliography}{1}
\bibitem{alpha}Alpha.
\end{thebibliography}
"""


class PaperCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="paper-tooling-", dir="/tmp")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.package = self.root
        (self.package / "anc").mkdir(parents=True)
        shutil.copyfile(ANC / "check_paper.py", self.package / "anc/check_paper.py")
        (self.package / "main.tex").write_text(PAPER, encoding="utf-8")
        (self.package / "references.bib").write_text("@article{alpha,\n}\n", encoding="utf-8")
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.environment = {"PATH": str(self.bin), "HOME": str(self.root), "LC_ALL": "C"}

    def fake_git(self, mode: str) -> None:
        script = self.bin / "git"
        script.write_text(
            '#!/bin/bash\n'
            'if [[ "$1" == rev-parse ]]; then\n'
            + ('  exit 128\n' if mode == "no-repo" else f'  printf "%s\\n" "{self.package}"\n')
            + 'elif [[ "$1" == show && "$2" == 0d5dcb02:main.tex ]]; then\n'
            + ('  exit 128\n' if mode == "no-baseline" else '/bin/cat main.tex\n')
            + 'else exit 129\nfi\n', encoding="utf-8",
        )
        script.chmod(0o700)

    def check(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(self.package / "anc/check_paper.py"), *arguments],
            cwd=self.package, env=self.environment, capture_output=True, text=True,
            check=False, timeout=10,
        )

    def test_given_unavailable_history_when_checked_then_current_paper_passes(self) -> None:
        for mode in ("no-git", "no-repo", "no-baseline"):
            with self.subTest(mode=mode):
                if mode != "no-git":
                    self.fake_git(mode)
                result = self.check()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("HISTORICAL_COMPARISON UNAVAILABLE", result.stdout)
                self.assertIn("PASS structural checks", result.stdout)
                self.assertIn("BIBLIOGRAPHY cited=1 bibitems=1 bibtex=1", result.stdout)

    def test_given_baseline_when_checked_then_existing_output_is_retained(self) -> None:
        self.fake_git("baseline")

        result = self.check()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"BODY_WORDS_APPROX before=\d+ after=\d+")
        self.assertNotIn("UNAVAILABLE", result.stdout)

    def test_given_no_history_when_invalid_then_structural_checks_fail(self) -> None:
        violations = (
            (PAPER.replace(r"\cite{alpha}", r"\cite{missing}"), "bibitems: missing="),
            (PAPER.replace(r"\ref{known}", r"\ref{missing}"), "labels: missing="),
            (PAPER + r"\begin{unclosed}", "unclosed environments"),
            (PAPER + "{", "brace imbalance"),
            (PAPER.replace("Short abstract.", "x" * 1920), "abstract is too long"),
            (PAPER.replace(r"\resultsfalse", r"\resultstrue"), "results switch is not false"),
            (PAPER.replace(r"\section{Introduction}", ""), "Introduction section is missing"),
            (PAPER.replace("abstract}", "summary}"), "abstract environment is missing"),
        )
        for mode in ("no-git", "no-repo", "no-baseline"):
            if mode != "no-git":
                self.fake_git(mode)
            for text, diagnostic in violations:
                with self.subTest(mode=mode, diagnostic=diagnostic):
                    (self.package / "main.tex").write_text(text, encoding="utf-8")
                    result = self.check()
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn("HISTORICAL_COMPARISON UNAVAILABLE", result.stdout)
                    self.assertIn(diagnostic, result.stdout)
                    self.assertIn("FAIL structural checks", result.stdout)

    def test_given_local_slice_when_checked_then_its_references_are_validated(self) -> None:
        (self.package / "anc/slice.tex").write_text(
            r"Slice \cite{alpha}.\label{slice}\ref{slice}", encoding="utf-8")
        (self.package / "main.tex").write_text(
            PAPER.replace(r"Current body \cite{alpha}.\label{known}\ref{known}",
                          r"\input{anc/slice.tex}"), encoding="utf-8")

        result = self.check()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS structural checks", result.stdout)

    def test_given_cyclic_slice_when_checked_then_source_is_rejected(self) -> None:
        (self.package / "anc/slice.tex").write_text(
            r"\input{anc/slice.tex}", encoding="utf-8")
        (self.package / "main.tex").write_text(
            PAPER + r"\input{anc/slice.tex}", encoding="utf-8")

        result = self.check()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cyclic TeX input", result.stderr)

    def test_given_reusable_bibtex_when_checked_then_uncited_sources_are_retained(self) -> None:
        (self.package / "references.bib").write_text(
            "@article{alpha,\n}\n@article{beta,\n}\n", encoding="utf-8")

        result = self.check()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("cited=1 bibitems=1 bibtex=2", result.stdout)

    def test_given_stable_citation_keys_when_normalised_then_named_authors_sort_correctly(self) -> None:
        text = PAPER.replace(r"\cite{alpha}", r"\cite{alpha,anthropic2025harness,openai2026harness}")
        text = text.replace(r"\end{thebibliography}",
                            "\\bibitem{anthropic2025harness}Young.\n"
                            "\\bibitem{openai2026harness}Lopopolo.\n"
                            "\\end{thebibliography}")
        (self.package / "main.tex").write_text(text, encoding="utf-8")
        (self.package / "references.bib").write_text(
            "@article{alpha,\n}\n@article{anthropic2025harness,\n}\n"
            "@article{openai2026harness,\n}\n", encoding="utf-8")

        result = self.check("--normalise-bibliography")

        self.assertEqual(result.returncode, 0, result.stderr)
        updated = (self.package / "main.tex").read_text()
        self.assertLess(updated.index(r"\bibitem{openai2026harness}"),
                        updated.index(r"\bibitem{anthropic2025harness}"))

    def test_given_disabled_slices_when_checked_then_contents_are_ignored_and_comments_preserved(self) -> None:
        comments = (
            "% \\input{anc/absent.tex}\n"
            "% TODO(author): keep the marker \\input{anc/disabled.tex}\n"
        )
        (self.package / "anc/disabled.tex").write_text(
            r"\cite{missing}\label{known}\ref{missing}", encoding="utf-8")
        (self.package / "main.tex").write_text(PAPER + comments, encoding="utf-8")

        for arguments in ((), ("--normalise-bibliography",)):
            with self.subTest(arguments=arguments):
                result = self.check(*arguments)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("BIBLIOGRAPHY cited=1 bibitems=1 bibtex=1", result.stdout)
                self.assertIn("TODO(author): keep the marker", result.stdout)
                self.assertTrue((self.package / "main.tex").read_text().endswith(comments))

    def test_given_inline_comment_when_inputs_expand_then_only_active_inputs_are_read(self) -> None:
        from check_paper import expand_inputs, strip_comments

        (self.package / "anc/active.tex").write_text("Active content\n", encoding="utf-8")
        source = r"Escaped \% \input{anc/active.tex} % TODO(author): \input{anc/absent.tex}" + "\r\n"

        expanded = expand_inputs(source, self.package)

        self.assertIn(r"Escaped \% Active content", expanded)
        self.assertTrue(expanded.endswith(
            "% TODO(author): \\input{anc/absent.tex}\r\n"))
        self.assertNotIn("absent.tex", strip_comments(expanded))

    def test_given_percent_escapes_when_inputs_expand_then_backslash_parity_is_preserved(self) -> None:
        from check_paper import expand_inputs, strip_comments

        (self.package / "anc/active.tex").write_text("Active content", encoding="utf-8")
        for prefix, active in ((r"\%", True), (r"\\%", False),
                               (r"\\\%", True), (r"\\\\%", False)):
            with self.subTest(prefix=prefix):
                source = prefix + r" \input{anc/active.tex}" + "\n"

                expanded = expand_inputs(source, self.package)
                clean = strip_comments(expanded)

                self.assertEqual("Active content" in expanded, active)
                self.assertTrue(clean.startswith(prefix if active else prefix[:-1]))
                if not active:
                    self.assertEqual(expanded, source)
                    self.assertNotIn(r"\input", clean)

class TcrTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="tcr-tooling-", dir="/tmp")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.logs = self.root / "logs"
        self.logs.mkdir()
        for command in ("bash", "mktemp", "rm", "tail"):
            executable = shutil.which(command)
            self.assertIsNotNone(executable, command)
            (self.bin / command).symlink_to(executable)
        self.environment = {
            "PATH": str(self.bin), "HOME": str(self.root), "LC_ALL": "C",
            "TMPDIR": str(self.logs), "CALLS": str(self.root / "calls"),
            "FAIL_STAGE": "", "TOKEN": "isolated-diagnostic",
        }
        for name, content in {
            "make": '''#!/bin/bash
printf 'make %s\\n' "$*" >> "$CALLS"
printf '%s\\n' "$TOKEN"
if [[ -n "${READY:-}" ]]; then
    printf '%s\\n' "$TOKEN" > "$READY"
    IFS= read -r permission < "$RELEASE"
fi
if [[ "$FAIL_STAGE" == tests || "$FAIL_STAGE" == rollback ]]; then exit 7; fi
''',
            "git": '''#!/bin/bash
printf 'git %s\\n' "$*" >> "$CALLS"
case "$1" in
  add) if [[ "$FAIL_STAGE" == staging ]]; then printf '%s staging\\n' "$TOKEN" >&2; exit 8; fi ;;
  commit) if [[ "$FAIL_STAGE" == commit ]]; then printf '%s commit\\n' "$TOKEN" >&2; exit 9; fi ;;
  reset) if [[ "$FAIL_STAGE" == rollback ]]; then exit 10; fi ;;
  clean) [[ "$*" == 'clean -qfd -e reports/' ]] || exit 11 ;;
  *) exit 12 ;;
esac
exit 0
''',
        }.items():
            script = self.bin / name
            script.write_text(content, encoding="utf-8")
            script.chmod(0o700)
        self.helper = ANC / "mve-feature-consolidation-harness/tcr"

    def run_tcr(self, stage: str = "") -> subprocess.CompletedProcess[str]:
        environment = {**self.environment, "FAIL_STAGE": stage}
        return subprocess.run(
            [str(self.bin / "bash"), str(self.helper), "fixture"], cwd=self.root,
            env=environment, capture_output=True, text=True, check=False, timeout=10,
        )

    def test_given_success_when_run_then_commits_without_rollback(self) -> None:
        result = self.run_tcr()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "TCR: committed\n")
        self.assertEqual(
            (self.root / "calls").read_text(),
            "make -s test\ngit add -A\ngit commit -q -m tcr: fixture\n",
        )
        self.assertEqual(list(self.logs.iterdir()), [])

    def test_given_stage_failure_when_run_then_rolls_back_and_cleans_log(self) -> None:
        for stage, status in (("tests", 7), ("staging", 8), ("commit", 9)):
            with self.subTest(stage=stage):
                (self.root / "calls").write_text("", encoding="utf-8")

                result = self.run_tcr(stage)

                self.assertEqual(result.returncode, status, result.stderr)
                self.assertIn(f"TCR: {stage} failed (exit {status})", result.stderr)
                self.assertIn("isolated-diagnostic", result.stderr)
                self.assertIn("TCR: reverted", result.stderr)
                calls = (self.root / "calls").read_text()
                self.assertTrue(calls.endswith("git reset -q --hard\ngit clean -qfd -e reports/\n"))
                if stage == "tests":
                    self.assertNotIn("git add", calls)
                if stage != "commit":
                    self.assertNotIn("git commit", calls)
                self.assertEqual(list(self.logs.iterdir()), [])

    def test_given_parallel_failures_when_run_then_diagnostics_are_separate(self) -> None:
        processes = []
        releases = []
        for token in ("diagnostic-one", "diagnostic-two"):
            ready = self.root / f"ready-{token}"
            release = self.root / f"release-{token}"
            os.mkfifo(ready)
            os.mkfifo(release)
            ready_fd = os.open(ready, os.O_RDWR | os.O_NONBLOCK)
            release_fd = os.open(release, os.O_RDWR | os.O_NONBLOCK)
            self.addCleanup(os.close, ready_fd)
            self.addCleanup(os.close, release_fd)
            environment = {
                **self.environment, "FAIL_STAGE": "tests", "TOKEN": token,
                "READY": str(ready), "RELEASE": str(release),
            }
            process = subprocess.Popen(
                [str(self.bin / "bash"), str(self.helper)], cwd=self.root,
                env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            self.addCleanup(self.reap, process)
            processes.append(process)
            releases.append(release_fd)
            self.assertEqual(select.select([ready_fd], [], [], 10)[0], [ready_fd])
            self.assertEqual(os.read(ready_fd, 100).decode().strip(), token)

        logs = list(self.logs.iterdir())
        self.assertEqual(len(logs), 2)
        self.assertEqual(
            {log.read_text().strip() for log in logs},
            {"diagnostic-one", "diagnostic-two"},
        )
        for release_fd in releases:
            os.write(release_fd, b"continue\n")

        for index, process in enumerate(processes):
            stdout, stderr = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 7, stderr)
            self.assertEqual(stdout, "")
            self.assertIn(("diagnostic-one", "diagnostic-two")[index], stderr)
            self.assertNotIn(("diagnostic-two", "diagnostic-one")[index], stderr)
        self.assertEqual(list(self.logs.iterdir()), [])

    def test_given_rollback_failure_when_run_then_reports_failure_without_success(self) -> None:
        result = self.run_tcr("rollback")

        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertIn("TCR: tests failed (exit 7)", result.stderr)
        self.assertIn("TCR: rollback failed; inspect the worktree", result.stderr)
        self.assertNotIn("TCR: reverted", result.stderr)
        self.assertNotIn("git clean", (self.root / "calls").read_text())
        self.assertEqual(list(self.logs.iterdir()), [])

    @staticmethod
    def reap(process: subprocess.Popen[str]) -> None:
        if process.poll() is None:
            process.kill()
        process.communicate()


if __name__ == "__main__":
    unittest.main()

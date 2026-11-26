"""Focused local regressions; GitHub publication is always mocked."""

import hashlib
import subprocess
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import package_arxiv as tool


class ArxivPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="arxiv-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.paper = self.root / "paper"
        self.paper.mkdir()
        (self.paper / "anc").mkdir()
        (self.paper / "main.tex").write_text(
            "\\documentclass{article}\n"
            "% \\input{private-notes.tex}\n"
            "\\input{anc/body}\n"
            "\\includegraphics[width=10cm]{figure.png}\n",
            encoding="utf-8",
        )
        (self.paper / "anc/body.tex").write_text(
            "\\include{anc/other}\n"
            "\\lstinputlisting[\n basicstyle=\\ttfamily]{anc/prompt.txt}\n"
            "\\begin{verbatim}\\input{not-a-dependency.tex}\\end{verbatim}",
            encoding="utf-8",
        )
        (self.paper / "anc/other.tex").write_text("Other section.", encoding="utf-8")
        (self.paper / "anc/prompt.txt").write_text(
            r"Literal \input{also-not-a-dependency.tex}",
            encoding="utf-8",
        )
        (self.paper / "figure.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        for name in ("main.pdf", "main.log", "unused.png", "references.bib", "private-notes.tex"):
            (self.paper / name).write_text("Do not package.", encoding="utf-8")

    def test_collects_only_reachable_inputs_without_changing_bytes(self) -> None:
        files = tool.collect_sources(self.paper)
        self.assertEqual(
            set(files),
            {"main.tex", "anc/body.tex", "anc/other.tex", "anc/prompt.txt", "figure.png"},
        )
        for name, data in files.items():
            self.assertEqual(data, (self.paper / name).read_bytes())

    def test_rejects_missing_invalid_external_cyclic_and_dynamic_inputs(self) -> None:
        (self.root / "outside.tex").write_text("Outside", encoding="utf-8")
        (self.paper / "linked.tex").symlink_to(self.root / "outside.tex")
        cases = (
            (r"\input{missing.tex}", "Missing compilation input"),
            (r"\input{../outside.tex}", "Invalid arXiv input path"),
            (rf"\input{{{self.root}/outside.tex}}", "Invalid arXiv input path"),
            (r"\input{bad name.tex}", "Invalid arXiv input path"),
            (r"\input{.hidden.tex}", "Invalid arXiv input path"),
            (r"\input{linked.tex}", "Symlink or external"),
            (r"\input{main.tex}", "Cyclic"),
            (r"\input{\macro}", "Invalid arXiv input path"),
            (r"\input unbraced", "Only literal braced"),
            (r"\includegraphics{references.bib}", "Unsupported PDFLaTeX"),
        )
        for source, diagnostic in cases:
            with self.subTest(source=source):
                (self.paper / "main.tex").write_text(source, encoding="utf-8")
                with self.assertRaisesRegex(tool.PackageError, diagnostic):
                    tool.collect_sources(self.paper)

    def test_archives_are_deterministic_rooted_and_byte_identical(self) -> None:
        files = tool.collect_sources(self.paper)
        expected = tool.submission_sources(files)
        first, second = self.root / "first", self.root / "second"
        first.mkdir()
        second.mkdir()
        tool.write_archives(files, first)
        tool.write_archives(files, second)
        for name in tool.ASSETS:
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
        with zipfile.ZipFile(first / tool.ARCHIVES[0]) as archive:
            self.assertFalse(any(name.startswith("anc/") for name in archive.namelist()))
            self.assertEqual({name: archive.read(name) for name in archive.namelist()}, expected)
        with tarfile.open(first / tool.ARCHIVES[1]) as archive_tar:
            self.assertEqual(set(archive_tar.getnames()), set(expected))
            for member in archive_tar:
                stream = archive_tar.extractfile(member)
                self.assertIsNotNone(stream)
                assert stream is not None
                with stream:
                    self.assertEqual(stream.read(), expected[member.name])
                self.assertTrue(member.isfile())
        for line in (first / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ")
            self.assertEqual(digest, hashlib.sha256((first / name).read_bytes()).hexdigest())

    def test_reserved_anc_inputs_are_relocated_with_only_file_arguments_rewritten(self) -> None:
        source = (
            "% \\input{anc/comment.tex}\n"
            "\\input{anc/body}\n"
            "\\includegraphics{anc/figure.png}\n"
            "\\nolinkurl{anc/evidence.json}\n"
            "\\begin{verbatim}\\input{anc/example.tex}\\end{verbatim}\n"
            "\\begin{lstlisting}\\input{anc/example.tex}\\end{lstlisting}\n"
        )
        files = {
            "main.tex": source.encode(),
            "anc/body.tex": (
                b"\\include{anc/other}\n"
                b"\\lstinputlisting[\n basicstyle=\\ttfamily]{anc/prompt.txt}\n"
            ),
            "anc/other.tex": b"Other section.",
            "anc/prompt.txt": rb"Literal \input{anc/not-a-dependency.tex}",
            "anc/figure.png": b"\x89PNG\r\n\x1a\n",
        }
        original = files.copy()
        submission = tool.submission_sources(files)
        self.assertEqual(
            submission["main.tex"].decode(),
            source.replace(r"\input{anc/body}", r"\input{tex-inputs/body}").replace(
                r"\includegraphics{anc/figure.png}", r"\includegraphics{tex-inputs/figure.png}"
            ),
        )
        self.assertEqual(
            submission["tex-inputs/body.tex"],
            b"\\include{tex-inputs/other}\n"
            b"\\lstinputlisting[\n basicstyle=\\ttfamily]{tex-inputs/prompt.txt}\n",
        )
        self.assertEqual(submission["tex-inputs/prompt.txt"], files["anc/prompt.txt"])
        self.assertEqual(submission["tex-inputs/figure.png"], files["anc/figure.png"])
        self.assertEqual(files, original)
        self.assertEqual(
            set(submission),
            {
                "main.tex",
                "tex-inputs/body.tex",
                "tex-inputs/other.tex",
                "tex-inputs/prompt.txt",
                "tex-inputs/figure.png",
            },
        )

    def test_reserved_directory_relocation_rejects_name_collisions(self) -> None:
        with self.assertRaisesRegex(tool.PackageError, "would overwrite"):
            tool.submission_sources(
                {
                    "main.tex": b"",
                    "anc/body.tex": b"Anc input.",
                    "tex-inputs/body.tex": b"Different existing input.",
                }
            )

    def test_compiles_extracted_zip_twice_without_shell_escape(self) -> None:
        tool.write_archives(tool.collect_sources(self.paper), self.root)
        extracted = self.root / "extracted"

        def fake_latex(command: list[str], cwd: Path) -> bytes:
            self.assertEqual(cwd, extracted)
            self.assertEqual((cwd / "figure.png").read_bytes(), b"\x89PNG\r\n\x1a\n")
            self.assertFalse((cwd / "private-notes.tex").exists())
            self.assertIn("-no-shell-escape", command)
            (cwd / "main.log").write_text("Output written.", encoding="utf-8")
            (cwd / "main.pdf").write_bytes(b"%PDF-preview")
            return b"Output written."

        with (
            mock.patch("package_arxiv.shutil.which", return_value="/usr/bin/pdflatex"),
            mock.patch.object(tool, "run", side_effect=fake_latex) as run,
        ):
            pdf = tool.compile_archive(self.root / tool.ARCHIVES[0], extracted)
        self.assertEqual(pdf.read_bytes(), b"%PDF-preview")
        self.assertEqual(run.call_count, 2)

    def test_failed_build_does_not_create_output_or_overwrite_existing_directory(self) -> None:
        output = self.root / "output"
        files = tool.collect_sources(self.paper)
        with (
            mock.patch.object(tool, "compile_archive", side_effect=tool.PackageError("TeX failed")),
            self.assertRaisesRegex(tool.PackageError, "TeX failed"),
        ):
            tool.build_package(files, output)
        self.assertFalse(output.exists())
        output.mkdir()
        with self.assertRaisesRegex(tool.PackageError, "already exists"):
            tool.build_package(files, output)

    def test_changed_labels_receive_a_third_pass_before_acceptance(self) -> None:
        tool.write_archives(tool.collect_sources(self.paper), self.root)
        extracted = self.root / "settling-labels"
        passes = 0

        def fake_latex(command: list[str], cwd: Path) -> bytes:
            nonlocal passes
            passes += 1
            log = (
                "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right."
                if passes < 3 else "Output written."
            )
            (cwd / "main.log").write_text(log, encoding="utf-8")
            (cwd / "main.pdf").write_bytes(b"%PDF-preview")
            return b""

        with (
            mock.patch("package_arxiv.shutil.which", return_value="/usr/bin/pdflatex"),
            mock.patch.object(tool, "run", side_effect=fake_latex) as run,
        ):
            tool.compile_archive(self.root / tool.ARCHIVES[0], extracted)
        self.assertEqual(run.call_count, 3)

    def test_unresolved_references_are_not_a_successful_build(self) -> None:
        tool.write_archives(tool.collect_sources(self.paper), self.root)
        extracted = self.root / "unresolved"

        def fake_latex(command: list[str], cwd: Path) -> bytes:
            (cwd / "main.log").write_text(
                "LaTeX Warning: There were undefined references.",
                encoding="utf-8",
            )
            (cwd / "main.pdf").write_bytes(b"%PDF")
            return b""

        with (
            mock.patch("package_arxiv.shutil.which", return_value="/usr/bin/pdflatex"),
            mock.patch.object(tool, "run", side_effect=fake_latex) as run,
            self.assertRaisesRegex(tool.PackageError, "unresolved references"),
        ):
            tool.compile_archive(self.root / tool.ARCHIVES[0], extracted)
        self.assertEqual(run.call_count, 4)

    def test_publication_requires_clean_tracked_exact_bytes(self) -> None:
        files = {"main.tex": b"Exact source"}
        revision = "a" * 40
        prefix = [str(self.root).encode() + b"\n", b"", revision.encode() + b"\n"]
        for responses, diagnostic in (
            ([str(self.root).encode(), b" M paper/main.tex\n"], "clean Git worktree"),
            ([*prefix, b"Different source"], "differs from HEAD"),
            ([*prefix, tool.PackageError("not in HEAD")], "not in HEAD"),
        ):
            with (
                self.subTest(diagnostic=diagnostic),
                mock.patch.object(tool, "run", side_effect=responses),
                self.assertRaisesRegex(tool.PackageError, diagnostic),
            ):
                tool.publication_revision(self.paper, files)
        with mock.patch.object(tool, "run", side_effect=[*prefix, b"Exact source"]) as run:
            self.assertEqual(tool.publication_revision(self.paper, files), revision)
        self.assertEqual(run.call_args.args[0], ["git", "show", f"{revision}:paper/main.tex"])

    def test_release_uses_exact_sha_new_tag_draft_upload_and_then_publication(self) -> None:
        revision = "b" * 40
        with mock.patch.object(tool, "run", return_value=b"") as run:
            tool.publish_release(self.root, "paper-v1", revision, self.paper)
        calls = [call.args[0] for call in run.call_args_list]
        self.assertEqual(calls[0], ["git", "check-ref-format", "refs/tags/paper-v1"])
        self.assertIn(f"sha={revision}", calls[1])
        self.assertIn("ref=refs/tags/paper-v1", calls[1])
        self.assertIn("--draft", calls[2])
        self.assertIn("--verify-tag", calls[2])
        self.assertIn("--draft=false", calls[3])
        self.assertTrue(all("--latest=false" in command for command in calls[2:]))
        for name in tool.ASSETS:
            self.assertIn(str(self.root / name), calls[2])
        self.assertNotIn(str(self.root / "main.pdf"), calls[2])

    def test_failed_upload_does_not_publish_or_delete_anything(self) -> None:
        with (
            mock.patch.object(
                tool, "run", side_effect=[b"", b"", tool.PackageError("upload failed")]
            ) as run,
            self.assertRaisesRegex(tool.PackageError, "draft may exist"),
        ):
            tool.publish_release(self.root, "paper-v1", "c" * 40, self.paper)
        self.assertEqual(run.call_count, 3)
        with (
            mock.patch.object(tool, "run") as run,
            self.assertRaisesRegex(tool.PackageError, "new tag"),
        ):
            tool.publish_release(self.root, "--invalid", "c" * 40, self.paper)
        run.assert_not_called()

    def test_package_only_has_no_github_calls_and_changed_head_blocks_publication(self) -> None:
        with (
            mock.patch.object(tool, "PAPER", self.paper),
            mock.patch.object(tool, "build_package") as build,
            mock.patch.object(tool, "publish_release") as publish,
            mock.patch.object(tool, "run", return_value=b"") as run,
        ):
            self.assertEqual(tool.main(["--output", str(self.root / "output")]), 0)
            run.assert_not_called()
            build.assert_called_once()
            publish.assert_not_called()
            with (
                mock.patch("package_arxiv.shutil.which", return_value="/usr/bin/gh"),
                mock.patch.object(tool, "publication_revision", side_effect=["a" * 40, "b" * 40]),
            ):
                self.assertEqual(
                    tool.main(
                        [
                            "--output",
                            str(self.root / "published"),
                            "--publish",
                            "--tag",
                            "paper-v1",
                        ]
                    ),
                    1,
                )
            publish.assert_not_called()

    def test_command_failure_surfaces_exit_status_and_diagnostics(self) -> None:
        failure = subprocess.CalledProcessError(2, ["pdflatex"], output=b"missing figure")
        with (
            mock.patch("package_arxiv.subprocess.run", side_effect=failure),
            self.assertRaisesRegex(tool.PackageError, "exit 2.*\\nmissing figure"),
        ):
            tool.run(["pdflatex"], self.paper)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Build arXiv source archives locally; optionally publish a new GitHub Release."""

import argparse
import gzip
import hashlib
import io
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

from check_paper import TEX_COMMENT

PAPER = Path(__file__).resolve().parent.parent
REPOSITORY = "jmservera/ama"
STEM = "everything-but-the-software-arxiv"
ARCHIVES = (f"{STEM}.zip", f"{STEM}.tar.gz")
ASSETS = (*ARCHIVES, "SHA256SUMS")
COMMAND = re.compile(r"\\(input|include|includegraphics|lstinputlisting)\*?(?![A-Za-z@])")
ARGUMENT = re.compile(r"\s*(?:\[[^\]]*\]\s*)?\{([^{}]+)\}", re.DOTALL)
SAFE_NAME = re.compile(r"[A-Za-z0-9_+,=-][A-Za-z0-9_+.,=-]*")
SAFE_TAG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]*")


class PackageError(Exception):
    """A packaging or publication precondition was not met."""


def run(command: list[str], cwd: Path, timeout: int = 180) -> bytes:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            timeout=timeout,
        ).stdout
    except subprocess.CalledProcessError as error:
        detail = error.stdout.decode("utf-8", errors="replace")
        raise PackageError(
            f"{command[0]} failed (exit {error.returncode}):\n"
            + "\n".join(detail.splitlines()[-35:])
        ) from error


def file_references(name: str, text: str) -> list[tuple[str, re.Match[str]]]:
    """Mask non-code without moving the file-argument offsets in the original text."""
    masked = re.sub(
        r"\\begin\{(verbatim\*?|lstlisting)\}.*?\\end\{\1\}",
        lambda match: " " * len(match.group(0)),
        text,
        flags=re.DOTALL,
    )
    masked = TEX_COMMENT.sub(lambda match: match.group(1).ljust(len(match.group(0))), masked)
    references = []
    for match in COMMAND.finditer(masked):
        argument = ARGUMENT.match(masked, match.end())
        if argument is None:
            raise PackageError(f"Only literal braced file arguments are supported in {name}")
        references.append((match.group(1), argument))
    return references


def collect_sources(paper: Path) -> dict[str, bytes]:
    """Resolve the paper's literal, submission-root-relative file commands."""
    paper = paper.resolve()
    files: dict[str, bytes] = {}
    active: set[str] = set()

    def visit(name: str, kind: str) -> None:
        parts = name.split("/")
        if not parts or any(not SAFE_NAME.fullmatch(part) for part in parts):
            raise PackageError(f"Invalid arXiv input path: {name!r}")
        path = paper.joinpath(*parts)
        if not path.suffix:
            extensions = (
                (".pdf", ".png", ".jpg", ".jpeg") if kind == "includegraphics" else (".tex",)
            )
            path = next(
                (path.with_suffix(ext) for ext in extensions if path.with_suffix(ext).is_file()),
                path,
            )
        if not path.is_file():
            raise PackageError(f"Missing compilation input: {name}")
        if path.resolve() != path or not path.resolve().is_relative_to(paper):
            raise PackageError(f"Symlink or external compilation input: {name}")
        name = path.relative_to(paper).as_posix()
        if kind == "includegraphics" and path.suffix not in {".pdf", ".png", ".jpg", ".jpeg"}:
            raise PackageError(f"Unsupported PDFLaTeX figure format: {name}")
        if kind in {"input", "include"} and path.suffix != ".tex":
            raise PackageError(f"Expected a literal .tex input: {name}")
        if name in active:
            raise PackageError(f"Cyclic TeX input: {name}")
        if name in files:
            return
        files[name] = path.read_bytes()
        if kind not in {"input", "include"}:
            return
        active.add(name)
        for command, argument in file_references(name, files[name].decode("utf-8")):
            visit(argument.group(1).strip(), command)
        active.remove(name)

    visit("main.tex", "input")
    return dict(sorted(files.items()))


def submission_sources(files: dict[str, bytes]) -> dict[str, bytes]:
    names = {name: f"tex-inputs/{name[4:]}" if name.startswith("anc/") else name for name in files}
    if len(set(names.values())) != len(names):
        raise PackageError("Relocating reserved anc/ inputs would overwrite a tex-inputs/ file.")
    submission = {}
    for name, data in files.items():
        if name.endswith(".tex"):
            text = data.decode("utf-8")
            for _, argument in reversed(file_references(name, text)):
                start, end = argument.span(1)
                original = text[start:end]
                replacement = re.sub(r"^(\s*)anc/", r"\1tex-inputs/", original)
                text = text[:start] + replacement + text[end:]
            data = text.encode("utf-8")
        submission[names[name]] = data
    return dict(sorted(submission.items()))


def write_archives(files: dict[str, bytes], destination: Path) -> None:
    files = submission_sources(files)
    with zipfile.ZipFile(destination / ARCHIVES[0], "x", zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    with (
        (destination / ARCHIVES[1]).open("xb") as stream,
        gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0) as compressed,
        tarfile.open(fileobj=compressed, mode="w") as archive_tar,
    ):
        for name, data in files.items():
            member = tarfile.TarInfo(name)
            member.size = len(data)
            member.mode = 0o644
            archive_tar.addfile(member, io.BytesIO(data))
    (destination / "SHA256SUMS").write_text(
        "".join(
            f"{hashlib.sha256((destination / name).read_bytes()).hexdigest()}  {name}\n"
            for name in ARCHIVES
        ),
        encoding="ascii",
    )


def compile_archive(archive: Path, destination: Path) -> Path:
    compiler = shutil.which("pdflatex")
    if compiler is None:
        raise PackageError("pdflatex is required; install the paper's TeX Live prerequisites.")
    destination.mkdir()
    with zipfile.ZipFile(archive) as source:
        source.extractall(destination)
    unsettled = re.compile(
        r"(?:Reference|Citation) .+ undefined|There were undefined|"
        r"Rerun to get cross-references right|Label\(s\) may have changed"
    )
    for pass_index in range(4):
        run(
            [
                compiler,
                "-no-shell-escape",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                "main.tex",
            ],
            destination,
        )
        log = (destination / "main.log").read_text(encoding="utf-8", errors="replace")
        if pass_index >= 1 and not unsettled.search(log):
            break
    if unsettled.search(log):
        raise PackageError(
            "Extracted bundle still has unresolved references; inspect the TeX source."
        )
    pdf = destination / "main.pdf"
    if not pdf.is_file() or pdf.stat().st_size == 0:
        raise PackageError("PDFLaTeX did not produce a nonempty main.pdf.")
    return pdf


def build_package(files: dict[str, bytes], output: Path) -> None:
    if output.exists():
        raise PackageError(f"Output directory already exists; choose a new path: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="arxiv-package-") as temporary:
        staging = Path(temporary)
        write_archives(files, staging)
        preview = compile_archive(staging / ARCHIVES[0], staging / "extracted")
        output.mkdir()
        for name in ASSETS:
            shutil.copyfile(staging / name, output / name)
        shutil.copyfile(preview, output / "main.pdf")


def publication_revision(paper: Path, files: dict[str, bytes]) -> str:
    root = Path(run(["git", "rev-parse", "--show-toplevel"], paper).decode().strip())
    if run(["git", "status", "--porcelain", "--untracked-files=all"], root).strip():
        raise PackageError("Publication requires a clean Git worktree, including untracked files.")
    revision = run(["git", "rev-parse", "HEAD"], root).decode().strip()
    for name, data in files.items():
        relative = (paper / name).relative_to(root).as_posix()
        committed = run(["git", "show", f"{revision}:{relative}"], root)
        if committed != data:
            raise PackageError(f"Packaged input differs from HEAD: {name}")
    return revision


def publish_release(output: Path, tag: str, revision: str, paper: Path) -> None:
    """Use a create-only ref and draft so upload failures do not publish partial assets."""
    if not SAFE_TAG.fullmatch(tag):
        raise PackageError(
            "Use a new tag containing only letters, digits, dot, underscore, + or -."
        )
    if "#" in str(output):
        raise PackageError("Release asset paths cannot contain '#', which gh treats as a label.")
    run(["git", "check-ref-format", f"refs/tags/{tag}"], paper)
    endpoint = f"repos/{REPOSITORY}"
    run(
        [
            "gh",
            "api",
            "--method",
            "POST",
            f"{endpoint}/git/refs",
            "-f",
            f"ref=refs/tags/{tag}",
            "-f",
            f"sha={revision}",
        ],
        paper,
    )
    notes = (
        f"arXiv compilation inputs from {REPOSITORY}@{revision}.\n\n"
        "The ZIP and tar.gz contain the same source files; upload either one to arXiv. "
        "SHA256SUMS covers both archives. The extracted ZIP compiled locally with PDFLaTeX "
        "and shell escape disabled. This release does not establish author clearance "
        "or arXiv acceptance and does not submit the article."
    )
    try:
        run(
            [
                "gh",
                "release",
                "create",
                tag,
                "--repo",
                REPOSITORY,
                "--verify-tag",
                "--draft",
                "--latest=false",
                "--title",
                f"arXiv source package {tag}",
                "--notes",
                notes,
                *(str(output / name) for name in ASSETS),
            ],
            paper,
        )
        run(
            [
                "gh",
                "release",
                "edit",
                tag,
                "--repo",
                REPOSITORY,
                "--draft=false",
                "--latest=false",
            ],
            paper,
        )
    except (PackageError, OSError, subprocess.TimeoutExpired) as error:
        raise PackageError(
            f"Release publication did not complete. Tag {tag} was created; a draft may exist. "
            f"Inspect https://github.com/{REPOSITORY}/releases before manual recovery. "
            f"Nothing was deleted or overwritten.\n{error}"
        ) from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New local output directory")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Create and publish a new release in jmservera/ama (requires author clearance)",
    )
    parser.add_argument("--tag", help="New release tag; required with --publish")
    args = parser.parse_args(argv)
    if args.publish != bool(args.tag):
        parser.error("--publish and --tag must be supplied together")
    try:
        output = args.output.expanduser().resolve()
        files = collect_sources(PAPER)
        revision = publication_revision(PAPER, files) if args.publish else None
        if args.publish:
            if shutil.which("gh") is None:
                raise PackageError("GitHub CLI (gh) is required for --publish.")
            if not SAFE_TAG.fullmatch(args.tag):
                raise PackageError(
                    "Invalid release tag; use letters, digits, dot, underscore, + or -."
                )
            run(["gh", "auth", "status"], PAPER)
        build_package(files, output)
        print(f"Validated {len(files)} compilation inputs; archives and local preview: {output}")
        if revision is not None:
            if publication_revision(PAPER, files) != revision:
                raise PackageError("HEAD changed while packaging; nothing was published.")
            publish_release(output, args.tag, revision, PAPER)
            print(f"Published https://github.com/{REPOSITORY}/releases/tag/{args.tag}")
        return 0
    except (PackageError, OSError, UnicodeError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

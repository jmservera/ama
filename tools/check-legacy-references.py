"""Deterministic check for Issue #203 criteria 1 and 2.

Criterion 1: tracked files may mention retired `mvp/` or `prototype/` paths
only as intentional history that names the archive tag, and the retired
package names `zavaforward_mvp` and `properwarm_mvp` only in dated historical
records, generated evidence or regression guards.
Criterion 2: every relative Markdown link in the changed documents resolves.

Exit codes: 0 pass, 1 violations found.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ARCHIVE_TAG = "v0.21.0"
PATH_TOKEN = re.compile(r"(?<![\w./-])(?:mvp|prototype)/(?!PoC\b|MVP\b)")
PACKAGE_TOKEN = re.compile(r"zavaforward_mvp|properwarm_mvp")
WINDOW = 10
HEADER_LINES = 60

# Immutable, append-only or generated cut-over records: not rewritten.
RECORD_PREFIXES = (
    "docs/reference/regulatory/",
    ".copilot-tracking/",
    "docs/reference/log.md",
    "docs/architecture/cutover-",
    "docs/architecture/mvp-to-src-parity-matrix.md",
    "docs/adrs/0006-src-layout-and-cutover.md",
    "docs/reference/research/reports/",
    "docs/capstone/history/",
    "docs/capstone/thought-leadership/everything-but-the-software/anc/",
)

# Regression guards and migration tools that must name the old strings.
GUARD_FILES = (
    "src/core/tests/test_cutover_audit.py",
    "src/core/src/zava_forward/core/synthetic/cutover_audit.py",
    "tools/rename-zava-tests.py",
    "tools/rpi-checks.py",
    "tools/check-legacy-references.py",
    "tools/test_check_legacy_references.py",
    "infra/tests/test_pipeline.py",
    ".github/workflows/mvp-validation.yml",
    ".github/workflows/src-ci.yml",
    ".github/rubric/scripts/test_safe_output_runtime.py",
    "docs/architecture/update-architecture.mjs",
)

# Dated documents that may name the retired packages as history.
DATED_PACKAGE_FILES = (
    "docs/adrs/0001-azure-architecture.md",
    "docs/adrs/0002-pilot-readiness-architecture.md",
    "docs/reference/research/gap-analysis-next-build.md",
    "docs/reference/research/decision-1-behaviour-specification.md",
    ".github/rubric/README.md",
)


def run_git(root: Path, *args: str) -> list[str]:
    out = subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout
    return [line for line in out.splitlines() if line]


def tracked_files(root: Path) -> list[str]:
    return run_git(root, "ls-files")


def is_exempt(path: str) -> bool:
    return path in GUARD_FILES or path.startswith(RECORD_PREFIXES)


def reference_violations(path: str, text: str) -> list[str]:
    if is_exempt(path):
        return []
    lines = text.splitlines()
    found = []
    header_tag = any(ARCHIVE_TAG in line for line in lines[:HEADER_LINES])
    for number, line in enumerate(lines, 1):
        if PACKAGE_TOKEN.search(line) and path not in DATED_PACKAGE_FILES:
            found.append(f"{path}:{number}: retired package name outside dated records")
        if PATH_TOKEN.search(line):
            lo, hi = max(0, number - 1 - WINDOW), number + WINDOW
            if not (header_tag or any(ARCHIVE_TAG in near for near in lines[lo:hi])):
                found.append(f"{path}:{number}: retired path without archive tag {ARCHIVE_TAG}")
    return found


def check_references(root: Path) -> list[str]:
    found = []
    for path in tracked_files(root):
        try:
            text = (root / path).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        found.extend(reference_violations(path, text))
    return found


INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)")
REF_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)")
EXTERNAL = ("http://", "https://", "mailto:", "//", "#", "tel:")


def link_targets(text: str):
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        stripped = re.sub(r"`[^`]*`", "", line)
        for match in INLINE_LINK.finditer(stripped):
            yield number, match.group(1).strip("<>")
        ref = REF_DEF.match(stripped)
        if ref:
            yield number, ref.group(1).strip("<>")


def link_violations(
    root: Path, path: str, text: str, only_lines: set[int] | None = None
) -> list[str]:
    found = []
    base = (root / path).parent
    for number, target in link_targets(text):
        if only_lines is not None and number not in only_lines:
            continue
        if target.startswith(EXTERNAL) or re.match(r"[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
            continue
        clean = re.split(r"[#?]", target, maxsplit=1)[0]
        if not clean:
            continue
        resolved = root / clean.lstrip("/") if clean.startswith("/") else base / clean
        if not resolved.exists():
            found.append(f"{path}:{number}: unresolved link {target}")
    return found


def changed_markdown(root: Path, base: str) -> list[str]:
    names = set(run_git(root, "diff", "--name-only", "--diff-filter=d", f"{base}...HEAD"))
    names.update(run_git(root, "diff", "--name-only", "--diff-filter=d", "HEAD"))
    names.update(run_git(root, "ls-files", "--others", "--exclude-standard"))
    return sorted(n for n in names if n.endswith(".md") and (root / n).is_file())


def added_lines(root: Path, base: str, path: str) -> set[int] | None:
    """Line numbers added or changed against the merge base; None for untracked files."""
    if path in run_git(root, "ls-files", "--others", "--exclude-standard"):
        return None
    merge_base = run_git(root, "merge-base", base, "HEAD")[0]
    lines: set[int] = set()
    for hunk in run_git(root, "diff", "-U0", merge_base, "--", path):
        match = re.match(r"@@ -\S+ \+(\d+)(?:,(\d+))? @@", hunk)
        if match:
            start, count = int(match.group(1)), int(match.group(2) or 1)
            lines.update(range(start, start + count))
    return lines


def check_links(root: Path, paths: list[str], base: str | None = None) -> list[str]:
    """Check links; with a base ref, only links on lines changed since it.

    Append-only and historical documents carry earlier link debt that cannot be
    rewritten, so a diff-scoped check holds changed content to the standard.
    """
    found = []
    for path in paths:
        only = added_lines(root, base, path) if base else None
        text = (root / path).read_text(encoding="utf-8")
        found.extend(link_violations(root, path, text, only))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--base", default="origin/main", help="base ref for changed documents")
    parser.add_argument(
        "--files",
        nargs="*",
        help="check links in these Markdown files instead of the diff",
    )
    parser.add_argument(
        "--all-links",
        action="store_true",
        help="report links in every tracked Markdown file (informational)",
    )
    args = parser.parse_args(argv)
    root = args.root

    reference_found = check_references(root)
    if args.files is not None:
        scope = args.files
    elif args.all_links:
        scope = [p for p in tracked_files(root) if p.endswith(".md")]
    else:
        scope = changed_markdown(root, args.base)
    diff_scoped = args.files is None and not args.all_links
    link_found = check_links(root, scope, args.base if diff_scoped else None)

    for line in reference_found + link_found:
        print(line)
    print(
        f"references: {len(reference_found)} violation(s); "
        f"links: {len(link_found)} violation(s) in {len(scope)} document(s)"
    )
    if args.all_links:
        return 1 if reference_found else 0
    return 1 if reference_found or link_found else 0


if __name__ == "__main__":
    sys.exit(main())

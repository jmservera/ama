#!/usr/bin/env python3
"""Measure pinned first-parent line churn without opening datasets.

Literal merge totals and totals including PR-numbered squash integrations are
reported separately. Git numstat excludes binary contents. Optional lizard
analysis reads only classified product-source blobs, never datasets.
"""

import argparse
import importlib.util
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

PIN = "29c6b512f5e68733bb2cc1882343db39f5eb2cad"
ROOT = Path(__file__).resolve().parents[5]
GIT = shutil.which("git")
CLASSES = ("product source", "tests", "documentation", ".copilot-tracking artefacts", "infrastructure", "CI and workflows", "other")
SOURCE_SUFFIXES = {".py", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".css", ".html", ".sql"}


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).with_suffix(".out.txt"))
    return parser


def git(*arguments: str) -> bytes:
    if GIT is None:
        raise RuntimeError("git is unavailable")
    return subprocess.run([GIT, *arguments], cwd=ROOT, check=True, capture_output=True).stdout


def path_class(name: str) -> str:
    path = PurePosixPath(name)
    parts = path.parts
    if parts and parts[0] == ".copilot-tracking":
        return ".copilot-tracking artefacts"
    if path.suffix.lower() == ".md":
        return "documentation"
    if any(part in {"tests", "checks", "evals", "__tests__"} for part in parts) or path.name.startswith("test_") or path.name.endswith((".test.js", ".test.mjs", ".test.ts")):
        return "tests"
    if any(part in {"vendor", "node_modules"} for part in parts):
        return "other"
    if parts and parts[0] == "infra":
        return "infrastructure"
    if name.startswith((".github/workflows/", ".github/actions/")):
        return "CI and workflows"
    packaged = len(parts) > 3 and parts[0] == "src" and parts[1] in {"core", "api", "agents", "orchestrator", "importer"} and parts[2] == "src"
    legacy = name.startswith(("mvp/", "prototype/"))
    if (packaged or legacy) and path.suffix.lower() in SOURCE_SUFFIXES:
        return "product source"
    return "other"


def changes(parent: str, revision: str) -> list[tuple[str, int, int]]:
    fields = git("diff", "--no-ext-diff", "--no-textconv", "--numstat", "-z", "--find-renames", parent, revision, "--").split(b"\0")
    result = []
    index = 0
    while index < len(fields) and fields[index]:
        added, removed, name = fields[index].split(b"\t", 2)
        index += 1
        if name:
            previous = current = name.decode("utf-8", errors="surrogateescape")
        else:
            previous = fields[index].decode("utf-8", errors="surrogateescape")
            current = fields[index + 1].decode("utf-8", errors="surrogateescape")
            index += 2
        if added == b"-" or removed == b"-":
            continue
        result.append((path_class(current), int(added), 0))
        result.append((path_class(previous), 0, int(removed)))
    return result


def main() -> int:
    args = create_parser().parse_args()
    allowed = Path(__file__).resolve().parent
    if args.out.resolve().parent != allowed:
        raise ValueError("output must remain in the paper's anc directory")
    cutoff = datetime.fromisoformat(git("show", "-s", "--format=%cI", PIN).decode().strip())
    start = datetime(2026, 10, 8, tzinfo=timezone.utc)
    split = datetime(2026, 10, 15, tzinfo=timezone.utc)
    history = git("log", "--first-parent", "--format=%H%x09%P%x09%cI%x09%s", PIN).decode().splitlines()
    totals = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    counts = defaultdict(int)
    revisions = defaultdict(list)
    last_mvp = None
    for record in history:
        revision, parent_text, timestamp, subject = record.split("\t", 3)
        instant = datetime.fromisoformat(timestamp)
        if instant < split and last_mvp is None:
            last_mvp = revision
        if not start <= instant <= cutoff:
            continue
        parents = parent_text.split()
        if not parents:
            continue
        period = "2026-10-08--14" if instant < split else "2026-10-15--24"
        literal = len(parents) > 1
        squash = not literal and re.search(r"\(#\d+\)\s*$", subject) is not None
        counts[(period, "direct excluded")] += int(not literal and not squash)
        if not literal and not squash:
            continue
        delta = changes(parents[0], revision)
        for selection in (["literal merges", "PR integrations"] if literal else ["PR integrations"]):
            counts[(period, selection)] += 1
            revisions[(period, selection)].append(revision)
            for category, added, removed in delta:
                totals[(period, selection)][category][0] += added
                totals[(period, selection)][category][1] += removed
    lines = [
        f"PIN {PIN}", f"CUTOFF_UTC {cutoff.astimezone(timezone.utc).isoformat()}",
        "COMMAND git log --first-parent --format='%H%x09%P%x09%cI%x09%s' PIN; UTC committer-date periods",
        "COMMAND per integration: git diff --no-ext-diff --no-textconv --numstat -z --find-renames FIRST_PARENT REVISION --",
        "SELECTION literal merges: every multi-parent first-parent commit; PR integrations: those plus single-parent commits ending (#PR)",
        "CAUTION PR integrations is a heuristic, not GitHub API PR metadata; first-parent main history may include merges made on topic branches",
        "CLASS PRECEDENCE tracking; Markdown; tests/checks/evals or test_* and *.test.{js,mjs,ts}; vendored -> other; infra; workflows/actions; product; other",
        "CLASS product: src/{core,api,agents,orchestrator,importer}/src plus historical mvp/ and prototype/ code, independent of package renaming; suffixes .py .js .mjs .ts .tsx .jsx .css .html .sql",
        "CLASS documentation: all Markdown outside .copilot-tracking, including agent instructions and workflow Markdown",
        "CLASS tests: non-Markdown paths matched above; infrastructure: remaining infra/; CI: remaining .github/workflows/ and .github/actions/",
        "CLASS other: remaining text, including config, auxiliary tooling and vendored code; binary deltas excluded",
        "RENAMES detected; additions classified at destination and removals at source; pure detected moves add no lines",
        "LIMIT churn is added/removed lines, not code quality, delivered value or net source size",
    ]
    for selection in ("literal merges", "PR integrations"):
        lines.append(f"\nSELECTION {selection}")
        for period in ("2026-10-08--14", "2026-10-15--24"):
            lines.append(f"PERIOD {period} commits={counts[(period, selection)]} direct_excluded={counts[(period, 'direct excluded')]}")
            lines.append("class | added | removed")
            for category in CLASSES:
                added, removed = totals[(period, selection)][category]
                lines.append(f"{category} | {added} | {removed}")
            source = totals[(period, selection)]["product source"]
            tracking = totals[(period, selection)][".copilot-tracking artefacts"]
            documents = totals[(period, selection)]["documentation"]
            lines.append(f"RATIO tracking_added/product_added={tracking[0] / source[0]:.6f}" if source[0] else "RATIO tracking_added/product_added=undefined")
            lines.append(f"RATIO tracking_churn/product_churn={sum(tracking) / sum(source):.6f}" if sum(source) else "RATIO tracking_churn/product_churn=undefined")
            lines.append(f"RATIO (tracking+documentation)_added/product_added={(tracking[0] + documents[0]) / source[0]:.6f}" if source[0] else "RATIO (tracking+documentation)_added/product_added=undefined")
    if importlib.util.find_spec("lizard") is None:
        lines.append("\nCOMPLEXITY not measured: lizard is not installed; no dependency installed")
    else:
        import lizard

        for revision in (last_mvp, PIN):
            if revision is None:
                continue
            functions = []
            names = git("ls-tree", "-r", "--name-only", revision).decode().splitlines()
            for name in names:
                if path_class(name) == "product source":
                    source = git("show", f"{revision}:{name}").decode("utf-8", errors="replace")
                    functions.extend(lizard.analyze_file.analyze_source_code(name, source).function_list)
            mean = sum(function.cyclomatic_complexity for function in functions) / len(functions) if functions else 0
            high = sum(function.cyclomatic_complexity > 10 for function in functions) / len(functions) if functions else 0
            lines.append(f"COMPLEXITY revision={revision} functions={len(functions)} mean={mean:.6f} share_above_10={high:.6f}")
    output = "\n".join(lines) + "\n"
    args.out.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())

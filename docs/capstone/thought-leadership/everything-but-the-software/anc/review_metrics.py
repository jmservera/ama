#!/usr/bin/env python3
"""Measure named historical source snapshots without executing product code.

Outputs are post-hoc descriptive evidence, not experiment trajectories.
Only classified source and committed research/plan Markdown are read.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import random
import re
import statistics
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from log_metrics import EVIDENCE_BOUNDARY, entries
from repo_history_metrics import PIN, ROOT, git, path_class

SOURCE_SUFFIXES = {".py", ".js", ".mjs", ".ts", ".tsx", ".jsx"}
SUPPRESSION = re.compile(r"noqa|pylint:\s*disable|type:\s*ignore|eslint-disable", re.I)
LESSON = re.compile(r"2026-10-12|setup-entra|app.registration|staff.bind|callback", re.I)
IDENTITY_LESSON = re.compile(
    r"infra/README\.md|setup-entra(?:\.py)?|setup-tenant-staff|tenant-staff|"
    r"\bapp(?:lication)?[ -]registration\b|\bstaff[ -]bindings?\b", re.I,
)


def create_parser() -> argparse.ArgumentParser:
    """Require explicit revisions and an external pinned jscpd executable."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revisions", nargs="+", required=True)
    parser.add_argument("--jscpd", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser


def run_json(command: list[str], *, cwd: Path, diagnostic_exit: int = 0) -> object:
    """Distinguish lint findings from execution failure."""
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                            check=False, timeout=600)
    if result.returncode not in (0, diagnostic_exit):
        raise RuntimeError(f"{command[0]} failed ({result.returncode}): {result.stderr[:1000]}")
    return json.loads(result.stdout)


def snapshot(revision: str, jscpd: Path) -> dict:
    """Materialise only product source in disposable scratch for static tools."""
    import lizard

    revision = git("rev-parse", f"{revision}^{{commit}}").decode().strip()
    names = git("ls-tree", "-r", "--name-only", revision).decode().splitlines()
    sources = [name for name in names if path_class(name) == "product source"
               and Path(name).suffix in SOURCE_SUFFIXES]
    if not sources:
        raise ValueError(f"No classified Python/JavaScript/TypeScript source at {revision}")
    python_sources = sorted(name for name in sources if Path(name).suffix == ".py")
    if not python_sources:
        raise ValueError(f"No classified Python source for Ruff at {revision}")
    functions = []
    digest = hashlib.sha256()
    lines = python_lines = suppressions = 0
    with tempfile.TemporaryDirectory(prefix="paper-static-") as temporary:
        work = Path(temporary) / "source"
        work.mkdir()
        for name in sorted(sources):
            data = git("show", f"{revision}:{name}")
            digest.update(name.encode() + b"\0" + data)
            text = data.decode("utf-8")
            target = work / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            functions.extend(lizard.analyze_file.analyze_source_code(name, text).function_list)
            lines += len(text.splitlines())
            if name in python_sources:
                python_lines += len(text.splitlines())
            suppressions += sum(bool(SUPPRESSION.search(line)) for line in text.splitlines())
        if python_lines == 0:
            raise ValueError(f"Python source has no lines for Ruff density at {revision}")
        lint = run_json([sys.executable, "-m", "ruff", "check", "--isolated", "--ignore-noqa",
                         "--select", "E,F,W,C90,B,SIM", "--output-format=json",
                         *(str(work / name) for name in python_sources)],
                        cwd=work, diagnostic_exit=1)
        if not isinstance(lint, list):
            raise ValueError("Ruff did not return the expected diagnostic array")
        reports = Path(temporary) / "duplication"
        result = subprocess.run(
            [str(jscpd), str(work), "--silent", "--min-tokens", "50", "--min-lines", "5",
             "--format", "python,javascript,typescript,tsx", "--reporters", "json",
             "--output", str(reports)],
            cwd=work, capture_output=True, text=True, check=False, timeout=600,
        )
        if result.returncode:
            raise RuntimeError(f"jscpd failed ({result.returncode}): {result.stderr[:1000]}")
        duplication = json.loads((reports / "jscpd-report.json").read_text())
        total = duplication["statistics"]["total"]
        return {
            "commit": revision, "source_sha256": digest.hexdigest(),
            "source_files": len(sources), "source_lines": lines, "functions": len(functions),
            "python_source_files": len(python_sources), "python_source_lines": python_lines,
            "mean_cyclomatic_complexity": statistics.mean(
                function.cyclomatic_complexity for function in functions) if functions else None,
            "share_functions_above_10": (
                sum(function.cyclomatic_complexity > 10 for function in functions) / len(functions)
                if functions else None),
            "lint_findings": len(lint), "lint_per_1000_python_lines": 1000 * len(lint) / python_lines,
            "suppression_lines": suppressions,
            "duplication": {key: total[key] for key in ("lines", "duplicatedLines", "percentage")},
        }


def lesson_traces(revision: str, *, pattern: re.Pattern[str] = LESSON) -> dict:
    """Count matching committed research/plans, not actual session exposure."""
    paths = git("ls-tree", "-r", "--name-only", revision).decode().splitlines()
    selected = [path for path in paths if path.startswith(".copilot-tracking/")
                and Path(path).suffix == ".md"
                and any(part in {"research", "plans", "planning"} for part in Path(path).parts)]
    matches = []
    for path in selected:
        text = git("show", f"{revision}:{path}").decode("utf-8")
        lines = [(number, line) for number, line in enumerate(text.splitlines(), 1)
                 if pattern.search(line)]
        if lines:
            matches.append({"path": path, "sha256": hashlib.sha256(text.encode()).hexdigest(),
                            "matching_lines": len(lines), "first_line": lines[0][0],
                            "first_excerpt": lines[0][1][:220]})
    return {"commit": revision, "pattern": pattern.pattern,
            "files_inspected": len(selected), "matching_files": len(matches),
            "selected_locators": matches[:12],
            "limitation": "References can be generic; neither presence nor absence establishes session access or use."}


def lexical_sample(revision: str) -> dict:
    """Select a reproducible, balanced sample for separately recorded adjudication."""
    text = git("show", f"{revision}:docs/reference/log.md").decode("utf-8")
    groups: dict[str, list[dict]] = {"before": [], "during": []}
    totals = {key: {"words": 0, "matches": 0} for key in groups}
    for day, body in entries(text):
        key = "before" if day < "2026-10-15" else "during"
        matches = list(EVIDENCE_BOUNDARY.finditer(body))
        totals[key]["words"] += len(body.split())
        totals[key]["matches"] += len(matches)
        for match in matches:
            groups[key].append({
                "date": day, "match": match.group(), "entry_character": match.start(),
                "context": " ".join(body[max(0, match.start() - 100):match.end() + 100].split()),
                "classification": None,
            })
    rng = random.Random(2027)
    sample = {key: rng.sample(values, min(10, len(values))) for key, values in groups.items()}
    return {"commit": revision, "lexicon": EVIDENCE_BOUNDARY.pattern, "seed": 2027,
            "sampling": "Ten matches per period; match-weighted, not entry-weighted or independent human coding",
            "totals": totals, "sample": sample, "precision": None}


def github_metadata() -> dict:
    """Export only the named case metadata, never raw sign-in logs or reviewer identities."""
    result = {}
    for kind, numbers in (("issues", (126, 349, 413, 444)), ("pulls", (445,))):
        for number in numbers:
            row = run_json(["gh", "api", f"repos/jmservera/ama/{kind}/{number}"], cwd=ROOT)
            keys = ("number", "title", "state", "created_at", "updated_at", "html_url",
                    "merged_at", "merge_commit_sha", "additions", "deletions", "changed_files")
            result[f"{kind}/{number}"] = {key: row[key] for key in keys if key in row}
    return result


def main() -> int:
    """Refuse unpinned tools and overwrite of retained evidence."""
    args = create_parser().parse_args()
    if args.out.exists() or args.out.is_symlink():
        raise FileExistsError(f"Evidence already exists: {args.out}; choose a fresh path")
    for package, expected in (("lizard", "1.24.3"), ("ruff", "0.17.3")):
        actual = importlib.metadata.version(package)
        if actual != expected:
            raise ValueError(f"{package} must be {expected}, found {actual}")
    jscpd = args.jscpd.resolve(strict=True)
    version = subprocess.run([str(jscpd), "--version"], check=True, capture_output=True,
                             text=True).stdout.strip()
    if version.removeprefix("jscpd ") != "5.4.1":
        raise ValueError(f"jscpd must be 5.4.1, found {version}")
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Post-hoc static and metadata review, no product execution, private dataset or paid inference",
        "tools": {"lizard": "1.24.3", "ruff": "0.17.3", "jscpd": "5.4.1"},
        "source_filter": "Existing path classifier; Python/JavaScript/TypeScript source only",
        "structural_snapshots": [snapshot(revision, jscpd) for revision in args.revisions],
        "lesson_traces": lesson_traces(PIN),
        "targeted_identity_traces": lesson_traces(PIN, pattern=IDENTITY_LESSON),
        "lexical_review": lexical_sample(PIN),
        "github_metadata": github_metadata(),
        "historical_sign_in_timestamp": None,
        "score_deployment_journey_link": None,
        "limitation": "Static metrics and repository records do not establish historical deployed usability.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report, indent=2) + "\n"
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(payload)
    print(f"Recorded {len(report['structural_snapshots'])} static snapshots in {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Reconcile the historical migration matrix and inventory tracked references."""

import argparse
import csv
import io
import re
import subprocess
from collections.abc import Callable, Iterable
from pathlib import Path, PurePosixPath

MATRIX = "docs/architecture/mvp-to-src-parity-matrix.md"
PARITY = "docs/architecture/cutover-parity-audit.tsv"
REFERENCES = "docs/architecture/cutover-reference-inventory.tsv"
GENERATED = {PARITY, REFERENCES}
TOKEN = re.compile(r"mvp-ci\.yml|mvp-validation\.yml|zavaforward_mvp|(?<!\w)(?:mvp|prototype)/")
ROW = re.compile(
    r"^\| `((?:mvp|prototype)/[^`]+)` \| (?:\d+ \| )?(migrate|rebuild|archive|retire) \|"
)
SUFFIXES = {
    ".md",
    ".py",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".bicep",
    ".bicepparam",
    ".sh",
    ".txt",
    ".in",
    ".js",
    ".html",
    ".css",
}
ACTUAL = {
    "mvp/.dockerignore": ("src/.dockerignore",),
    "mvp/requirements.in": ("src/api/pyproject.toml", "src/core/pyproject.toml"),
    "mvp/zavaforward_mvp/ai_registry.py": ("src/core/src/zava_forward/core/ai_registry.py",),
    "mvp/tests/release_support.py": ("src/core/tests/release_support.py",),
    "mvp/zavaforward_mvp/assistants.py": (
        "src/core/src/zava_forward/core/assistants.py",
        "src/agents/src/zava_forward/agents/dispatch.py",
    ),
}


def eligible(name: str) -> bool:
    """Filter before opening; never follow private/configuration paths."""
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or name in GENERATED:
        return False
    if any(part.startswith(".env") or part == ".vscode" for part in path.parts):
        return False
    if "data" in path.parts:
        return False
    if "properwarm.json" in path.parts or name.startswith(".copilot-tracking/github-issues/"):
        return False
    if name.startswith("support/") and not ("/generator/" in name and path.suffix == ".py"):
        return False
    return path.suffix in SUFFIXES or path.name in {".gitignore", ".dockerignore", "Dockerfile"}


def inventory(names: Iterable[str], read: Callable[[str], str]) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for name in sorted(set(names)):
        if not eligible(name):
            continue
        if name.startswith(".copilot-tracking/"):
            category = "tracking-history"
        elif name.startswith(".github/workflows/"):
            category = "workflow-continuity"
        elif name.startswith(("tools/", "src/")):
            category = "source-or-regression-review"
        else:
            category = "documentation-or-config-review"
        for number, line in enumerate(read(name).splitlines(), 1):
            for token in sorted(set(TOKEN.findall(line))):
                rows.append((name, str(number), token, category))
    return rows


def expand(target: str) -> str:
    if target.startswith("src/"):
        return target
    if target.startswith("api/checks/"):
        return "src/" + target
    prefix, sep, tail = target.partition("/")
    for project in ("core", "api", "agents", "orchestrator", "importer"):
        if prefix == project:
            return f"src/{project}/src/zava_forward/{project}/{tail}"
        for label, folder in (("tests", "tests"), ("evals", "evals"), ("checks", "checks")):
            if prefix == f"{project}-{label}":
                return f"src/{project}/{folder}/{tail}"
    raise ValueError(f"Unresolved matrix target: {target!r} (separator={sep!r})")


def parity(text: str, tracked: set[str]) -> list[tuple[str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str]] = []
    seen: set[str] = set()
    for line in text.splitlines():
        match = ROW.match(line)
        if not match:
            continue
        old, outcome = match.groups()
        if old in seen:
            raise ValueError(f"Duplicate matrix row: {old}")
        seen.add(old)
        cells = line.split("|")
        target_cell = cells[4 if cells[2].strip().isdigit() else 3].strip()
        if outcome in {"archive", "retire"}:
            remaining = sorted(name for name in tracked if PurePosixPath(name).match(old))
            status = "still-tracked" if remaining else "absent-before-this-pack"
            actual = ";".join(remaining) or "-"
        else:
            targets = ACTUAL.get(old)
            if targets is None:
                quoted = re.findall(r"`([^`]+)`", target_cell)
                if not quoted:
                    raise ValueError(f"No quoted target: {old}")
                targets = (expand(quoted[0]),)
            missing = [target for target in targets if target not in tracked]
            status = "MISSING:" + ";".join(missing) if missing else "destination-present"
            if outcome == "rebuild" and not missing:
                status = "partial-rebuild-not-deployed-worker"
            actual = ";".join(targets)
        rows.append((old, outcome, target_cell, actual, status))
    if not rows:
        raise ValueError("No historical matrix rows found")
    return rows


def tsv(header: tuple[str, ...], rows: Iterable[tuple[str, ...]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return output.getvalue()


def check_expected(expected: str, actual: str, label: str) -> None:
    if expected != actual:
        raise ValueError(f"Stale {label}; regenerate the cut-over audit")


def audit(root: Path, write: bool) -> None:
    names = (
        subprocess.run(["git", "-C", str(root), "ls-files", "-z"], check=True, capture_output=True)
        .stdout.decode("utf-8")
        .split("\0")
    )
    tracked = set(filter(None, names))

    def read(name: str) -> str:
        path = root / name
        if not eligible(name) or path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Unsafe audit input: {name}")
        return path.read_text(encoding="utf-8")

    reconciliation = parity(read(MATRIX), tracked)
    missing = [row for row in reconciliation if row[-1].startswith("MISSING:")]
    if missing:
        raise ValueError(f"Missing matrix destinations: {missing}")
    outputs = {
        PARITY: tsv(
            ("historical_path", "outcome", "historical_target", "actual_target", "status"),
            reconciliation,
        ),
        REFERENCES: tsv(("path", "line", "token", "classification"), inventory(tracked, read)),
    }
    for name, content in outputs.items():
        path = root / name
        if write:
            path.write_text(content, encoding="utf-8")
        else:
            check_expected(path.read_text(encoding="utf-8"), content, name)
    print(
        f"PASS: {len(reconciliation)} matrix rows; {len(outputs[REFERENCES].splitlines()) - 1}"
        " reference locations; no missing destinations"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--write", action="store_true", help="Regenerate the two TSV reports")
    args = parser.parse_args()
    try:
        audit(args.root.resolve(), args.write)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Cut-over audit failed: {error}\n")


if __name__ == "__main__":
    main()

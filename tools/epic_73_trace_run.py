"""Run the tests cited by the Epic #73 requirement trace and report pass or fail per requirement.

Refs #73. Read-only over the trace note; it never edits the note and never records the epic
or a requirement as accepted. Suites run sequentially: each cited test is an exact unittest id.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/reference/research/issue-73-requirement-trace-2026-11-20.md"
CHECK_RE = re.compile(r"`([\w/.-]+\.py)::(test_\w+)`")
TESTS_DIR_RE = re.compile(r"^(src/[^/]+)/tests/")


def cited_tests(note: Path = NOTE) -> dict[str, list[tuple[str, str]]]:
    """Map each requirement with a Checked row to its cited (path, test name) pairs."""
    found: dict[str, list[tuple[str, str]]] = {}
    for line in note.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[1] == "Checked":
            found[cells[0]] = CHECK_RE.findall(cells[3])
    return found


def command(path: str, name: str) -> tuple[list[str], Path, str]:
    """Return the unittest argv, working directory and PYTHONPATH for one cited test."""
    match = TESTS_DIR_RE.match(path)
    if not match:
        raise ValueError(f"cited test is not under src/<project>/tests: {path}")
    project = ROOT / match.group(1)
    module = Path(path).with_suffix("").relative_to(Path(match.group(1)) / "tests")
    dotted = ".".join(module.parts)
    paths = ["src", "tests", "../core/src", "../agents/src", "../core/tests", "../agents/tests"]
    return (
        [sys.executable, "-m", "unittest", f"{dotted}.{_class_dotted(path, name)}"],
        project,
        ":".join(paths),
    )


def _class_dotted(path: str, name: str) -> str:
    """Find the TestCase class that defines the test, as unittest needs Class.method."""
    current = None
    for line in (ROOT / path).read_text(encoding="utf-8").splitlines():
        class_match = re.match(r"class (\w+)\(", line)
        if class_match:
            current = class_match.group(1)
        if re.match(rf"\s+def {name}\(", line) and current:
            return f"{current}.{name}"
    raise ValueError(f"{name} not found in {path}")


def run() -> int:
    failures = 0
    for req, checks in cited_tests().items():
        for path, name in checks:
            argv, cwd, pythonpath = command(path, name)
            env = {**os.environ, "PYTHONPATH": pythonpath}
            result = subprocess.run(
                argv, check=False, cwd=cwd, env=env, capture_output=True, text=True
            )
            status = "PASS" if result.returncode == 0 else "FAIL"
            failures += result.returncode != 0
            print(f"{req}\t{status}\t{path}::{name}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())

"""Guard that Issue #201 dependent epics keep no executable dependency on retired mvp/ or prototype/ paths."""

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EPIC_SURFACES = {
    "#113 platform/infra": ("infra/", ".github/workflows/"),
    "#136 data/orchestrator": ("src/orchestrator/", "src/importer/", "src/core/"),
    "#165 synthetic data/simulator": (
        "src/core/src/zava_forward/core/synthetic/",
        "src/core/tests/",
    ),
    "#157 agent chat/memory": ("src/agents/",),
    "#149 UX/accessibility": ("src/api/",),
}

RETIRED_PATH = re.compile(r"(?<![\w./-])(?:mvp|prototype)/")
RETIRED_EXECUTION = re.compile(
    r"(?:PYTHONPATH=\.?/?mvp\b|working-directory:\s*\.?/?(?:mvp|prototype)\b"
    r"|\b(?:cd|python3?|pytest|COPY|ADD)\s+\.?/?(?:mvp|prototype)\b"
    r"|\bimport\s+zavaforward_mvp|\bfrom\s+zavaforward_mvp)"
)
HISTORICAL_MARKER = re.compile(
    r"archive|v0\.21\.0|former|retired|moved|migrat|#199|#201", re.IGNORECASE
)

# Files whose purpose is to name retired paths: the cut-over audit data and its tests.
RETIREMENT_RECORDS = {
    "src/core/src/zava_forward/core/synthetic/cutover_audit.py",
    "src/core/tests/test_cutover_audit.py",
}
# Negative guards that assert retired data directories stay absent from git.
NEGATIVE_GUARD = re.compile(r"git ls-files[^\n]*\bmvp/data\b|^\s*\"mvp/data\",\s*$")
DOC_SUFFIXES = {".md"}
COMMENT_PREFIXES = ("#", '"""')


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files", "--", "src", "infra", ".github/workflows"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [name for name in out.splitlines() if (ROOT / name).is_file()]


def read(name):
    try:
        return (ROOT / name).read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return []


def historical_note(name, line):
    stripped = line.strip()
    if Path(name).suffix in DOC_SUFFIXES or stripped.startswith(COMMENT_PREFIXES):
        return bool(HISTORICAL_MARKER.search(line))
    return bool(NEGATIVE_GUARD.search(line))


def prohibition_note(name, line):
    return Path(name).suffix in DOC_SUFFIXES and bool(
        re.search(r"\b(?:never|do not|no)\b", line, re.IGNORECASE)
    )


def violations(names):
    found = []
    for name in names:
        if name in RETIREMENT_RECORDS:
            continue
        for number, line in enumerate(read(name), 1):
            if RETIRED_EXECUTION.search(line) and not prohibition_note(name, line):
                found.append(
                    f"{name}:{number}: retired execution path: {line.strip()[:100]}"
                )
            elif RETIRED_PATH.search(line) and not historical_note(name, line):
                found.append(
                    f"{name}:{number}: retired path reference: {line.strip()[:100]}"
                )
    return found


class GuardLogicTests(unittest.TestCase):
    def test_classifier_flags_execution_and_unmarked_references(self):
        self.assertTrue(RETIRED_EXECUTION.search("run: cd mvp && python -m unittest"))
        self.assertTrue(RETIRED_EXECUTION.search("PYTHONPATH=mvp python3 x.py"))
        self.assertTrue(RETIRED_EXECUTION.search("working-directory: prototype"))
        self.assertFalse(RETIRED_EXECUTION.search("cd src/api"))
        self.assertTrue(RETIRED_PATH.search("python mvp/app.py"))
        self.assertFalse(RETIRED_PATH.search("src/mvp/x and ../prototype/x"))

    def test_historical_notes_and_negative_guards_are_allowed(self):
        self.assertTrue(
            historical_note("a.md", "Moved from `mvp/` (archive `v0.21.0`).")
        )
        self.assertFalse(historical_note("a.md", "Run `mvp/run.sh`."))
        self.assertTrue(
            historical_note("a.toml", "# Moved unchanged from mvp/ (archive v0.21.0)")
        )
        self.assertTrue(
            historical_note("w.yml", 'run: test -z "$(git ls-files mvp/data)"')
        )
        self.assertFalse(historical_note("w.yml", "run: ls mvp/data"))


class EpicLegacyPathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = tracked_files()

    def test_retired_directories_are_absent(self):
        for retired in ("mvp", "prototype"):
            with self.subTest(retired=retired):
                self.assertFalse((ROOT / retired).exists())

    def test_each_epic_surface_has_files_and_no_legacy_dependency(self):
        for epic, prefixes in EPIC_SURFACES.items():
            with self.subTest(epic=epic):
                names = [name for name in self.files if name.startswith(prefixes)]
                self.assertTrue(names, f"no tracked files for {epic}")
                self.assertEqual(violations(names), [])

    def test_no_legacy_dependency_across_all_scanned_roots(self):
        self.assertEqual(violations(self.files), [])


if __name__ == "__main__":
    unittest.main()

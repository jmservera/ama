"""Guard the 2026-11-23 nine-epic stabilization checkpoint in the evidence pack.

Refs #2301, Refs #440. Read-only over repository documents; it never asserts live
GitHub or Azure state and never promotes an epic to accepted or closed.
"""

import fnmatch
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs/architecture/cutover-evidence-pack.md"
NOTE = ROOT / "docs/reference/research/issue-2301-stabilization-checkpoint-live-2026-11-23.md"
HEADING = "## Demo-scope stabilization checkpoint for nine delivered epics (2026-11-23"
EPICS = (73, 81, 89, 93, 100, 109, 149, 157, 208)
CLASSES = ("local observed", "Azure observed", "implemented-unverified", "deferred", "blocked")
RECOMMENDATIONS = ("continue", "fix", "pivot")


def section() -> str:
    text = PACK.read_text(encoding="utf-8")
    start = text.index(HEADING)
    following = re.search(r"^## ", text[start + 3 :], re.MULTILINE)
    return text[start : start + 3 + following.start()] if following else text[start:]


def epic_rows(body: str) -> dict[int, list[str]]:
    rows: dict[int, list[str]] = {}
    for line in body.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 7 and re.fullmatch(r"#\d+", cells[0]):
            rows[int(cells[0][1:])] = cells
    return rows


def gap_rows(body: str) -> list[list[str]]:
    start = body.index("### Remaining epic criteria as exact gaps")
    following = re.search(r"^### ", body[start + 4 :], re.MULTILINE)
    block = body[start : start + 4 + following.start()] if following else body[start:]
    rows = []
    for line in block.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0] not in ("Epic", "---"):
            rows.append(cells)
    return rows


def non_continue_without_gap_issue(rows: dict[int, list[str]]) -> list[int]:
    """Epics recommended fix or pivot must cite a scoped gap issue other than the epic itself."""
    bad = []
    for epic, cells in rows.items():
        if cells[6] in ("fix", "pivot"):
            cited = {int(n) for n in re.findall(r"#(\d+)", cells[6] + " " + cells[5])}
            if not cited - {epic}:
                bad.append(epic)
    return bad


class StabilizationCheckpoint2301Tests(unittest.TestCase):
    def test_source_pin_is_a_full_commit_hash(self) -> None:
        self.assertRegex(section(), r"Source commit \| `[0-9a-f]{40}`")

    def test_source_pin_is_an_ancestor_of_head(self) -> None:
        pin = re.search(r"Source commit \| `([0-9a-f]{40})`", section()).group(1)  # type: ignore[union-attr]
        try:
            result = subprocess.run(
                ["git", "merge-base", "--is-ancestor", pin, "HEAD"],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
        except OSError:
            self.skipTest("git unavailable")
        if result.returncode == 128:
            self.skipTest("pinned commit not present in this clone")
        self.assertEqual(result.returncode, 0, "pinned commit is not in HEAD history")

    def test_cited_code_and_test_files_resolve_to_tracked_files(self) -> None:
        try:
            listing = subprocess.run(
                ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
            ).stdout.splitlines()
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("git file listing unavailable")
        for epic, cells in epic_rows(section()).items():
            cited = re.findall(r"`([^`]+)`", cells[3])
            self.assertTrue(cited, f"epic {epic} cites no code or tests")
            for name in cited:
                with self.subTest(epic=epic, cited=name):
                    hit = any(
                        fnmatch.fnmatch(path, name if "/" in name else f"*/{name}")
                        for path in listing
                    )
                    self.assertTrue(hit, f"{name} matches no tracked file")

    def test_each_epic_has_one_row_with_class_and_recommendation(self) -> None:
        rows = epic_rows(section())
        self.assertEqual(sorted(rows), sorted(EPICS))
        for epic, cells in rows.items():
            with self.subTest(epic=epic):
                self.assertTrue(any(c in cells[5] for c in CLASSES), cells[5])
                self.assertIn(cells[6], RECOMMENDATIONS)

    def test_production_only_items_stay_deferred_to_named_issues(self) -> None:
        body = section()
        for issue in ("#1905", "#1906", "#1907"):
            self.assertIn(issue, body)
        self.assertRegex(body, r"(?i)deferred to #1905")

    def test_checkpoint_does_not_claim_closure_or_acceptance(self) -> None:
        body = section().lower()
        self.assertIn("ticks or closes nothing", body)
        self.assertNotRegex(body, r"epic[^.]{0,40}(is|are) (now )?closed")

    def test_evidence_note_exists_and_is_linked_from_the_pack(self) -> None:
        self.assertTrue(NOTE.is_file())
        self.assertIn(NOTE.name, section())

    def test_every_remaining_criterion_names_an_epic_and_an_owner(self) -> None:
        rows = gap_rows(section())
        self.assertTrue(rows, "gap table missing")
        for epic, gap in ((r[0], r[2]) for r in rows):
            with self.subTest(epic=epic):
                ids = {int(n) for n in re.findall(r"#(\d+)", epic)}
                self.assertTrue(epic == "All nine" or ids <= set(EPICS), epic)
                self.assertRegex(gap, r"(?i)owner|deferred to #\d+")

    def test_fix_or_pivot_recommendation_requires_a_gap_issue(self) -> None:
        self.assertEqual(non_continue_without_gap_issue(epic_rows(section())), [])
        synthetic = {73: ["#73", "", "", "", "", "local observed", "fix"]}
        self.assertEqual(non_continue_without_gap_issue(synthetic), [73])
        synthetic[73][5] = "local observed; gap #2999"
        self.assertEqual(non_continue_without_gap_issue(synthetic), [])


if __name__ == "__main__":
    unittest.main()

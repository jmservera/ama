"""Guard the 2026-11-23 nine-epic stabilization checkpoint in the evidence pack.

Refs #2301, Refs #440. Read-only over repository documents; it never asserts live
GitHub or Azure state and never promotes an epic to accepted or closed.
"""

import re
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


class StabilizationCheckpoint2301Tests(unittest.TestCase):
    def test_source_pin_is_a_full_commit_hash(self) -> None:
        self.assertRegex(section(), r"Source commit \| `[0-9a-f]{40}`")

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


if __name__ == "__main__":
    unittest.main()

"""Parity tests for the rubric scorer concurrency settings (Issue #1086).

The gh-aw detection tracker records most Capstone Rubric Scorer warnings as
cancelled runs caused by the workflow concurrency group, so the compiled lock
file must keep the same group and cancel-in-progress value as its source.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"
SOURCE = WORKFLOWS / "rubric-score.md"
LOCK = WORKFLOWS / "rubric-score.lock.yml"


def concurrency_block(text: str) -> dict[str, str]:
    """Return the key/value pairs of the first top-level `concurrency:` block."""
    lines = text.splitlines()
    for start, line in enumerate(lines):
        if line == "concurrency:":
            break
    else:
        raise AssertionError("no top-level concurrency block")
    block: dict[str, str] = {}
    for line in lines[start + 1 :]:
        match = re.match(r"^  ([\w-]+):\s*(.*)$", line)
        if not match:
            break
        block[match.group(1)] = match.group(2).strip().strip("\"'")
    return block


class RubricConcurrencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = concurrency_block(SOURCE.read_text(encoding="utf-8"))
        self.lock = concurrency_block(LOCK.read_text(encoding="utf-8"))

    def test_lock_group_matches_source(self) -> None:
        self.assertEqual(self.lock["group"], self.source["group"])

    def test_lock_cancel_in_progress_matches_source(self) -> None:
        self.assertEqual(self.lock["cancel-in-progress"], self.source["cancel-in-progress"])

    def test_group_is_scoped_by_event_and_pull_request_or_ref(self) -> None:
        group = self.source["group"]
        self.assertIn("github.event.pull_request.number", group)
        self.assertIn("github.ref", group)
        self.assertIn("github.event_name", group)

    def test_manual_dispatch_runs_never_share_a_group(self) -> None:
        self.assertIn("github.run_id", self.source["group"])


if __name__ == "__main__":
    unittest.main()

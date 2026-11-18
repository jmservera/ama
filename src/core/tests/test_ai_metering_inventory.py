"""Keeps the Tokenomics metering inventory (#432) tied to code that exists."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from zava_forward.core.ai_consumption import Consumption

ROOT = Path(__file__).resolve().parents[3]
DOC = ROOT / "docs/reference/resources/ai-tokenomics.md"
HEADING = "## Current-main Metering Inventory"


def inventory() -> str:
    text = DOC.read_text(encoding="utf-8")
    start = text.index(HEADING)
    end = text.index("\n## ", start + 1)
    return text[start:end]


class MeteringInventoryTest(unittest.TestCase):
    def test_cited_source_and_test_paths_exist(self) -> None:
        paths = set(re.findall(r"`(src/[\w./-]+\.py)`", inventory()))
        self.assertGreaterEqual(len(paths), 8)
        for path in sorted(paths):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_cited_ledger_methods_exist(self) -> None:
        methods = set(re.findall(r"`Consumption\.(\w+)`", inventory()))
        self.assertTrue(
            {"reserve", "complete", "authorize", "price", "billing", "report"} <= methods
        )
        for name in sorted(methods):
            self.assertTrue(callable(getattr(Consumption, name, None)), name)

    def test_cited_test_names_exist(self) -> None:
        names = set(re.findall(r"`(test_\w+)`", inventory()))
        self.assertGreaterEqual(len(names), 4)
        corpus = "".join(
            p.read_text(encoding="utf-8") for p in (ROOT / "src/core/tests").glob("test_ai_*.py")
        )
        for name in sorted(names):
            self.assertIn(f"def {name}(", corpus, name)

    def test_open_criteria_are_not_claimed_proven(self) -> None:
        text = inventory()
        self.assertIn("Unmet criteria stay unmet: 5", text)
        self.assertIn("8 (a finite, owner-authorised live batch)", text)


if __name__ == "__main__":
    unittest.main()

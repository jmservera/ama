"""Regression test for the issue #224 applicability pack and Legal briefing."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = (
    ROOT
    / "docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md"
)
BRIEFING = ROOT / "docs/reference/research/rai/legal-briefing-adm-ai-act.md"


class AdmEvidencePackTests(unittest.TestCase):
    def test_pack_records_eu_amending_act_with_dates(self):
        text = PACK.read_text(encoding="utf-8")
        for needle in ("2026/1744", "2 December 2027", "2 August 2028", "2026-11-17"):
            self.assertIn(needle, text)

    def test_briefing_no_longer_calls_eu_text_unread(self):
        text = BRIEFING.read_text(encoding="utf-8")
        self.assertIn("2026/1744", text)
        self.assertNotIn("EU AI Act text, commencement and amendments are unverified", text)

    def test_decisions_stay_pending_and_no_inference(self):
        text = PACK.read_text(encoding="utf-8")
        section = text.split("## Decision Record", 1)[1].split("##", 1)[0]
        self.assertGreaterEqual(section.count("| Pending |"), 2)
        self.assertIn("## Non-inference Rules", text)


if __name__ == "__main__":
    unittest.main()

import copy
import unittest
from pathlib import Path

from zava_forward.core import perspective_walkthroughs as pw

ROOT = Path(__file__).resolve().parents[3]


class PerspectiveWalkthroughTests(unittest.TestCase):
    def test_eleven_perspectives_five_elements_none_met(self) -> None:
        rec = pw.check(ROOT)
        self.assertEqual(rec["blockers"], [])
        self.assertEqual(rec["status"], "recorded")
        self.assertEqual(rec["perspectives"], 11)
        self.assertEqual(rec["elements_met"], 0)
        self.assertEqual(rec["elements_partial"] + rec["elements_unmet"], 55)
        self.assertGreater(rec["elements_unmet"], 0)
        self.assertIn("not user validation", rec["notice"])

    def test_met_status_is_rejected(self) -> None:
        reg = copy.deepcopy(pw.register())
        reg["finance-grants"]["entry"]["status"] = "met"
        self.assertIn("finance-grants.entry:status_invalid", pw.check(ROOT, reg)["blockers"])

    def test_missing_profile_element_evidence_and_unknown_block(self) -> None:
        reg = copy.deepcopy(pw.register())
        del reg["quality-assurance"]
        del reg["digital-auditor"]["recovery"]
        reg["asset-investment"]["entry"]["evidence"] = ["src/nope.py"]
        reg["procurement-contracts"]["evidence"]["evidence"] = []
        reg["ghost"] = {}
        blockers = set(pw.check(ROOT, reg)["blockers"])
        self.assertEqual(
            blockers,
            {
                "quality-assurance:missing",
                "digital-auditor.recovery:missing",
                "asset-investment.entry:evidence_not_found:src/nope.py",
                "procurement-contracts.evidence:evidence_missing",
                "ghost:unknown_profile",
            },
        )

    def test_unmet_cells_state_a_reason(self) -> None:
        for cells in pw.register().values():
            for cell in cells.values():
                self.assertTrue(cell["reason"].strip())
                if cell["status"] == "unmet":
                    self.assertEqual(cell["evidence"], [])

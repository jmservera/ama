import copy
import unittest
from pathlib import Path

from zava_forward.core import journey_acceptance as ja

ROOT = Path(__file__).resolve().parents[3]


class JourneyAcceptanceTests(unittest.TestCase):
    def test_register_covers_every_criterion_and_claims_no_pass(self) -> None:
        rec = ja.check(ROOT)
        self.assertEqual(rec["blockers"], [])
        self.assertEqual(rec["status"], "recorded")
        self.assertEqual(rec["passed"], [])
        self.assertEqual(set(rec["partial"]) | set(rec["deferred"]), set(ja.CRITERIA))
        self.assertEqual(len(ja.CRITERIA), 10)
        self.assertIn("not user validation", rec["notice"])

    def test_pass_status_is_rejected(self) -> None:
        reg = copy.deepcopy(ja.REGISTER)
        reg["AC-034"]["status"] = "pass"
        self.assertIn("AC-034:status_invalid", ja.check(ROOT, reg)["blockers"])

    def test_deferred_needs_reason_and_partial_needs_evidence(self) -> None:
        reg = copy.deepcopy(ja.REGISTER)
        reg["AC-035"]["reason"] = " "
        reg["AC-037"]["evidence"] = []
        blockers = ja.check(ROOT, reg)["blockers"]
        self.assertIn("AC-035:reason_missing", blockers)
        self.assertIn("AC-037:evidence_missing", blockers)

    def test_missing_unknown_and_broken_evidence_block(self) -> None:
        reg = copy.deepcopy(ja.REGISTER)
        del reg["AC-041"]
        reg["AC-044"] = dict(status="deferred", reason="x", evidence=[])
        reg["AC-040"]["evidence"] = ["src/nope.py"]
        blockers = set(ja.check(ROOT, reg)["blockers"])
        self.assertEqual(
            blockers,
            {"AC-041:missing", "AC-044:unknown_criterion", "AC-040:evidence_not_found:src/nope.py"},
        )

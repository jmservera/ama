"""Synthetic test values only; they are not company figures or Board approvals."""

import json
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from zava_forward.core import exposure_limits as limits
from zava_forward.core.finance import FinanceMixin

APPROVAL = dict(
    approver="Test approver",
    role="Test Board role",
    approved_on="2026-01-01",
    evidence_ref="synthetic-minute-1",
    restart_owner="Test control owner",
)
ENVELOPE = dict(amount=100, currency="GBP", period="test year")
TOLERANCES = dict(capital=dict(maximum=10, unit="percent"), safety=dict(maximum=0, unit="count"))


class ExposureLimits(unittest.TestCase):
    def record(self) -> dict[str, object]:
        return limits.record_limits(APPROVAL, ENVELOPE, TOLERANCES)

    def test_unrecorded_limits_hold_and_pause(self) -> None:
        result = limits.assess(None, dict(committed=1))
        self.assertEqual((result["status"], result["signal"]), ("Held", limits.UNAPPROVED))

    def test_inputs_must_be_approved_and_valid(self) -> None:
        for bad in (None, {}, dict(APPROVAL, approver=" "), dict(APPROVAL, approved_on="x")):
            with self.assertRaises(limits.LimitsError):
                limits.record_limits(bad, ENVELOPE, TOLERANCES)
        for env in (None, dict(ENVELOPE, amount=-1), dict(ENVELOPE, amount=True)):
            with self.assertRaises(limits.LimitsError):
                limits.record_limits(APPROVAL, env, TOLERANCES)
        for tol in (None, {}, dict(mood=dict(maximum=1, unit="x")), dict(capital=dict(unit="x"))):
            with self.assertRaises(limits.LimitsError):
                limits.record_limits(APPROVAL, ENVELOPE, tol)

    def test_within_limits_gives_no_pause_and_no_approval(self) -> None:
        exposure = dict(committed=100, currency="GBP", tolerances=dict(capital=10, safety=0))
        result = limits.assess(self.record(), exposure)
        self.assertEqual(result["signal"], "No pause signal")
        self.assertIn("not approval to accelerate", result["reason"])

    def test_envelope_breach_pauses_for_human(self) -> None:
        exposure = dict(committed=101, currency="GBP", tolerances=dict(capital=1, safety=0))
        result = limits.assess(self.record(), exposure)
        self.assertEqual((result["status"], result["signal"]), ("Breach", limits.UNAPPROVED))
        self.assertIn("envelope", result["reason"])
        self.assertEqual(result["approval"]["restart_owner"], "Test control owner")

    def test_tolerance_breach_pauses_for_human(self) -> None:
        exposure = dict(committed=1, currency="GBP", tolerances=dict(capital=1, safety=1))
        result = limits.assess(self.record(), exposure)
        self.assertEqual(result["status"], "Breach")
        self.assertIn("safety", result["reason"])

    def test_missing_or_mismatched_exposure_is_unknown_not_within(self) -> None:
        for exposure in (
            None,
            dict(committed=1, currency="EUR", tolerances=dict(capital=1, safety=0)),
        ):
            result = limits.assess(self.record(), exposure)
            self.assertEqual((result["status"], result["signal"]), ("Unknown", limits.UNAPPROVED))
        partial = limits.assess(self.record(), dict(committed=1, currency="GBP", tolerances={}))
        self.assertEqual(partial["status"], "Unknown")


class LiveSignal(unittest.TestCase):
    USER = dict(role="Retrofit Programme Manager", email="t@example.test")

    def store(self, *amounts: float) -> SimpleNamespace:
        coms = [dict(amount=a, status="Raised") for a in amounts] + [
            dict(amount=999, status="Cancelled")
        ]
        return SimpleNamespace(
            lock=threading.RLock(), cases={"c1": dict(finance=dict(commitments=coms)), "c2": {}}
        )

    def signal(
        self, amounts: tuple[float, ...], content: object, user: dict[str, str] | None = None
    ) -> Any:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "approved-limits.json"
            if content is not None:
                path.write_text(content if isinstance(content, str) else json.dumps(content))
            return FinanceMixin.exposure_signal(self.store(*amounts), user or self.USER, path)  # type: ignore[arg-type,no-untyped-call]

    def test_no_file_holds_and_pauses(self) -> None:
        result = self.signal((1,), None)
        self.assertEqual((result["status"], result["signal"]), ("Held", limits.UNAPPROVED))

    def test_malformed_file_holds_not_within(self) -> None:
        for content in ("{", "[]", dict(approval=APPROVAL)):
            self.assertEqual(self.signal((1,), content)["status"], "Held")

    def test_envelope_breach_from_recorded_commitments(self) -> None:
        content = dict(approval=APPROVAL, envelope=ENVELOPE, tolerances=TOLERANCES)
        result = self.signal((60, 50), content)
        self.assertEqual(result["status"], "Breach")
        self.assertEqual(result["findings"][0]["observed"], 110)

    def test_within_envelope_still_unknown_while_tolerances_unobserved(self) -> None:
        content = dict(approval=APPROVAL, envelope=ENVELOPE, tolerances=TOLERANCES)
        self.assertEqual(self.signal((10,), content)["status"], "Unknown")

    def test_finance_roles_only(self) -> None:
        with self.assertRaises(PermissionError):
            self.signal((1,), None, dict(role="Resident Liaison Officer", email="x@example.test"))


if __name__ == "__main__":
    unittest.main()

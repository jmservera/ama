"""Synthetic test values only; they are not company figures or Board approvals."""

import importlib
import json
import math
import sys
import tempfile
import threading
import unittest
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

_CORE_SRC = Path(__file__).resolve().parents[1] / "src"


def _ensure_local_exposure_limits() -> None:
    if sys.path[:1] != [str(_CORE_SRC)]:
        sys.path[:] = [str(_CORE_SRC), *(p for p in sys.path if p != str(_CORE_SRC))]
        importlib.invalidate_caches()
    for pkg_name, pkg_dir in (
        ("zava_forward", str(_CORE_SRC / "zava_forward")),
        ("zava_forward.core", str(_CORE_SRC / "zava_forward" / "core")),
    ):
        pkg = sys.modules.get(pkg_name)
        if pkg is not None and hasattr(pkg, "__path__") and list(pkg.__path__)[:1] != [pkg_dir]:
            pkg.__path__ = [pkg_dir, *(p for p in pkg.__path__ if p != pkg_dir)]
    loaded = sys.modules.get("zava_forward.core.exposure_limits")
    if loaded is not None:
        loaded_file = loaded.__file__
        if not (loaded_file and Path(loaded_file).resolve().is_relative_to(_CORE_SRC)):
            sys.modules.pop("zava_forward.core.exposure_limits", None)
            core_pkg: Any = sys.modules.get("zava_forward.core")
            if core_pkg is not None and hasattr(core_pkg, "exposure_limits"):
                del core_pkg.exposure_limits
            importlib.invalidate_caches()


_ensure_local_exposure_limits()

from zava_forward.core import exposure_limits as limits  # noqa: E402
from zava_forward.core.finance import FinanceMixin  # noqa: E402

APPROVAL = dict(
    approver="Test approver",
    role="Test Board role",
    approved_on=(date.today() - timedelta(days=30)).isoformat(),
    evidence_ref="synthetic-minute-1",
    restart_owner="Test control owner",
)
ENVELOPE = dict(amount=100, currency="GBP", period="test year")
TOLERANCES = dict(capital=dict(maximum=10, unit="percent"), safety=dict(maximum=0, unit="count"))


class ExposureLimits(unittest.TestCase):
    def record(self) -> dict[str, object]:
        return limits.record_limits(APPROVAL, ENVELOPE, TOLERANCES)

    def test_attribution_is_required_and_never_defaulted(self) -> None:
        base_approval = {k: v for k, v in APPROVAL.items() if k not in ("approver", "approved_on")}
        for missing in ("approved_by", "approved_at"):
            approval = dict(base_approval, approved_by="Test approver", approved_at="2026-01-01")
            del approval[missing]
            with self.assertRaises(limits.LimitsError):
                limits.record_limits(approval, ENVELOPE, TOLERANCES)
        record = limits.record_limits(
            dict(base_approval, approved_by="Named person", approved_at="2026-01-01T10:00:00Z"),
            ENVELOPE,
            TOLERANCES,
        )
        self.assertEqual(record["approval"]["approved_by"], "Named person")
        self.assertEqual(record["approval"]["approved_at"], "2026-01-01T10:00:00Z")

    def test_pause_signal_requires_named_human_and_never_cuts(self) -> None:
        held = limits.assess(None, dict(committed=1))["pause_signal"]
        self.assertEqual((held["paused"], held["automatic_cut"]), (True, False))
        breach = limits.assess(
            self.record(), dict(committed=101, currency="GBP", tolerances=dict(capital=1, safety=0))
        )["pause_signal"]
        self.assertEqual(
            (breach["paused"], breach["decision_required"], breach["automatic_cut"]),
            (True, True, False),
        )
        self.assertEqual(breach["decision_owner"], "Test control owner")
        within = limits.assess(
            self.record(), dict(committed=1, currency="GBP", tolerances=dict(capital=1, safety=0))
        )["pause_signal"]
        self.assertEqual((within["paused"], within["automatic_cut"]), (False, False))

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

    def test_nonfinite_observation_is_unknown_not_within(self) -> None:
        for bad in (float("-inf"), float("inf"), float("nan")):
            for exposure in (
                dict(committed=bad, currency="GBP", tolerances=dict(capital=1, safety=0)),
                dict(committed=1, currency="GBP", tolerances=dict(capital=bad, safety=bad)),
                dict(committed=bad, currency="GBP", tolerances=dict(capital=bad, safety=bad)),
            ):
                result = limits.assess(self.record(), exposure)
                self.assertEqual(
                    (result["status"], result["signal"]), ("Unknown", limits.UNAPPROVED), exposure
                )
                self.assertFalse(
                    [f for f in result["findings"] if not math.isfinite(f.get("observed", 0))]
                )

    def test_huge_integer_observation_still_breaches(self) -> None:
        exposure = dict(committed=10**400, currency="GBP", tolerances=dict(capital=1, safety=0))
        self.assertEqual(limits.assess(self.record(), exposure)["status"], "Breach")
        exposure = dict(committed=1, currency="GBP", tolerances=dict(capital=10**400, safety=0))
        self.assertEqual(limits.assess(self.record(), exposure)["status"], "Breach")

    def test_conflicting_aliases_compact_iso_unknown_keys_and_overflow_are_refused(self) -> None:
        base_approval = {k: v for k, v in APPROVAL.items() if k not in ("approver", "approved_on")}
        for bad_approval in (
            dict(APPROVAL, approved_by="Different person"),
            dict(APPROVAL, approved_at="2026-01-01T10:00:00Z"),
            dict(base_approval, approved_by="Person", approved_at="2026-W01-1"),
            dict(base_approval, approved_by="Person", approved_at="20260101T100000"),
            dict(base_approval, approved_by="Person", approved_at="2026-01-01 10:00:00"),
            dict(base_approval, approved_by="Person", approved_at="2026-01-01T99:99:99"),
            dict(APPROVAL, extra="x"),
        ):
            with self.assertRaises(limits.LimitsError):
                limits.record_limits(bad_approval, ENVELOPE, TOLERANCES)
        for bad_env in (
            dict(ENVELOPE, extra=1),
            dict(ENVELOPE, amount=10**400),
            dict(ENVELOPE, annual_plan=-1),
        ):
            with self.assertRaises(limits.LimitsError):
                limits.record_limits(APPROVAL, bad_env, TOLERANCES)
        with self.assertRaises(limits.LimitsError):
            limits.record_limits(APPROVAL, ENVELOPE, dict(capital=dict(maximum=10, unit="%", x=1)))

    def test_liquidity_and_covenant_floors_assess_breach_unknown_and_within(self) -> None:
        rec = limits.record_limits(
            APPROVAL,
            dict(ENVELOPE, annual_plan=90),
            TOLERANCES,
            liquidity=dict(minimum=30, currency="GBP", covenant_minimum=1.2, covenant_unit="x"),
        )
        within = limits.assess(
            rec,
            dict(
                committed=80,
                currency="GBP",
                liquidity=30,
                covenant=1.2,
                covenant_unit="x",
                tolerances=dict(capital=5, safety=0),
            ),
        )
        self.assertEqual((within["status"], within["signal"]), ("Within limits", "No pause signal"))
        both = limits.assess(
            rec,
            dict(
                committed=110,
                currency="GBP",
                liquidity=dict(available=-10, currency="GBP"),
                covenant=dict(headroom=1.1, unit="x"),
                tolerances=dict(capital=5, safety=0),
            ),
        )
        self.assertEqual(both["status"], "Breach")
        self.assertEqual(
            both["reason"],
            "Over approved limit: envelope, annual_plan; "
            "below approved minimum: liquidity, covenant.",
        )

    def test_forged_limits_and_negative_ceiling_observations_never_pass_assess(self) -> None:
        forged = dict(self.record(), envelope=dict(ENVELOPE, amount=10**400))
        self.assertEqual(limits.assess(forged, dict(committed=1, currency="GBP"))["status"], "Held")
        neg = limits.assess(
            self.record(), dict(committed=-1, currency="GBP", tolerances=dict(capital=1, safety=0))
        )
        self.assertEqual((neg["status"], neg["signal"]), ("Unknown", limits.UNAPPROVED))
        non_dict = limits.assess(self.record(), "invalid")  # type: ignore[arg-type]
        self.assertEqual((non_dict["status"], non_dict["signal"]), ("Unknown", limits.UNAPPROVED))


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

    def test_stale_file_holds(self) -> None:
        old = dict(APPROVAL, approved_on=(date.today() - timedelta(days=400)).isoformat())
        result = self.signal((1,), dict(approval=old, envelope=ENVELOPE, tolerances=TOLERANCES))
        self.assertEqual(result["status"], "Held")
        self.assertIn("out of date", result["reason"])
        future = dict(APPROVAL, approved_on=(date.today() + timedelta(days=5)).isoformat())
        result = self.signal((1,), dict(approval=future, envelope=ENVELOPE, tolerances=TOLERANCES))
        self.assertEqual(result["status"], "Held")

    def test_non_utf8_file_holds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "approved-limits.json"
            path.write_bytes(b"\xff\xfe{")
            with self.assertRaises(limits.LimitsError):
                limits.load_limits(path)
            result = FinanceMixin.exposure_signal(self.store(1), self.USER, path)  # type: ignore[arg-type,no-untyped-call]
        self.assertEqual(result["status"], "Held")

    def test_non_numeric_commitment_amount_holds(self) -> None:
        content = dict(approval=APPROVAL, envelope=ENVELOPE, tolerances=TOLERANCES)
        for bad in ("12k", True, float("nan"), [1]):
            store = self.store(1)
            store.cases["c1"]["finance"]["commitments"].append(dict(amount=bad, status="Raised"))
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "approved-limits.json"
                path.write_text(json.dumps(content))
                result = FinanceMixin.exposure_signal(store, self.USER, path)  # type: ignore[arg-type,no-untyped-call]
            self.assertEqual(result["status"], "Held", bad)

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

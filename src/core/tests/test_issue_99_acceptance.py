"""Issue #99 acceptance evidence. Synthetic values only, not company figures or approvals."""

import json
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from typing import Any

_CORE_SRC = Path(__file__).resolve().parents[1] / "src"
if sys.path[:1] != [str(_CORE_SRC)]:
    sys.path[:] = [str(_CORE_SRC), *(p for p in sys.path if p != str(_CORE_SRC))]
_loaded = sys.modules.get("zava_forward.core.exposure_limits")
if _loaded is None or not Path(_loaded.__file__ or "").resolve().is_relative_to(_CORE_SRC):
    for _mod in [m for m in sys.modules if m == "zava_forward" or m.startswith("zava_forward.")]:
        del sys.modules[_mod]

from zava_forward.core import exposure_limits as limits  # noqa: E402

APPROVAL = dict(
    approver="Test approver",
    approved_on=(date.today() - timedelta(days=5)).isoformat(),
    role="Test Board role",
    evidence_ref="synthetic-minute-99",
    restart_owner="Test control owner",
)
ENVELOPE = dict(amount=100, currency="GBP", period="test year")
TOLERANCES = dict(capital=dict(maximum=10, unit="percent"))
LIQUIDITY = dict(minimum=25, currency="GBP", covenant_minimum=1.25, covenant_unit="ratio")


class EnvelopeIsApprovedInputTests(unittest.TestCase):
    def test_module_resolves_to_local_worktree_source(self) -> None:
        self.assertEqual(
            Path(limits.__file__ or "").resolve(),
            _CORE_SRC / "zava_forward" / "core" / "exposure_limits.py",
        )

    def test_nothing_is_invented_without_a_person_supplied_record(self) -> None:
        result = limits.assess(None, dict(committed=1, currency="GBP"))
        self.assertEqual(result["status"], "Held")
        self.assertEqual(result["signal"], limits.UNAPPROVED)
        self.assertEqual(result["findings"], [])

    def test_recorded_inputs_carry_the_approval_and_restart_owner(self) -> None:
        record = limits.record_limits(APPROVAL, ENVELOPE, TOLERANCES)
        self.assertEqual(record["approval"]["approver"], "Test approver")
        self.assertEqual(record["approval"]["restart_owner"], "Test control owner")
        self.assertEqual(record["envelope"]["amount"], 100.0)
        self.assertNotIn("liquidity", record)

    def test_unattributed_inputs_are_refused(self) -> None:
        for missing in ("approver", "approved_on", "evidence_ref", "restart_owner"):
            approval = {k: v for k, v in APPROVAL.items() if k != missing}
            with self.assertRaises(limits.LimitsError, msg=missing):
                limits.record_limits(approval, ENVELOPE, TOLERANCES)

    def test_approved_liquidity_covenant_and_annual_plan_are_recorded_and_roundtrip(self) -> None:
        envelope = dict(ENVELOPE, annual_plan=80)
        payload = dict(
            approval=APPROVAL,
            envelope=envelope,
            tolerances=TOLERANCES,
            liquidity=LIQUIDITY,
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "approved-limits.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            loaded = limits.load_limits(path)
        assert loaded is not None
        self.assertEqual(loaded["envelope"]["annual_plan"], 80.0)
        self.assertEqual(loaded["liquidity"]["minimum"], 25.0)
        self.assertEqual(loaded["liquidity"]["covenant_minimum"], 1.25)
        self.assertEqual(loaded["liquidity"]["covenant_unit"], "ratio")
        for bad_liq in (
            dict(minimum=-1, currency="GBP"),
            dict(minimum=10, currency="GBP", covenant_minimum=1.2),
            dict(minimum=10, currency="GBP", extra=1),
        ):
            with self.assertRaises(limits.LimitsError):
                limits.record_limits(APPROVAL, ENVELOPE, TOLERANCES, liquidity=bad_liq)

    def test_forged_unvalidated_limits_record_is_held_and_paused(self) -> None:
        base = limits.record_limits(APPROVAL, ENVELOPE, TOLERANCES)
        forged_missing_ref = dict(
            base,
            approval={k: v for k, v in base["approval"].items() if k != "evidence_ref"},
        )
        forged_unknown = dict(base, invented_threshold=50)
        for forged in (forged_missing_ref, forged_unknown):
            result = limits.assess(forged, dict(committed=10, currency="GBP"))
            self.assertEqual(result["status"], "Held")
            self.assertEqual(result["signal"], limits.UNAPPROVED)
            self.assertEqual(
                (result["pause_signal"]["paused"], result["pause_signal"]["automatic_cut"]),
                (True, False),
            )


class BreachPausesForHumanDecisionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = limits.record_limits(APPROVAL, ENVELOPE, TOLERANCES)

    def test_envelope_breach_signals_pause_for_the_restart_owner(self) -> None:
        result = limits.assess(self.record, dict(committed=150, currency="GBP"))
        self.assertEqual(result["status"], "Breach")
        self.assertEqual(result["signal"], limits.UNAPPROVED)
        self.assertEqual(result["approval"]["restart_owner"], "Test control owner")
        self.assertIn("restart needs their recorded approval", result["action"])

    def test_tolerance_breach_signals_pause(self) -> None:
        exposure = dict(committed=50, currency="GBP", tolerances=dict(capital=25))
        result = limits.assess(self.record, exposure)
        self.assertEqual(result["status"], "Breach")
        self.assertEqual(result["signal"], limits.UNAPPROVED)

    def test_liquidity_and_covenant_floor_breaches_including_deficits_signal_pause(self) -> None:
        record = limits.record_limits(
            APPROVAL,
            dict(ENVELOPE, annual_plan=80),
            TOLERANCES,
            liquidity=LIQUIDITY,
        )
        for exposure, expected_text in (
            (
                dict(
                    committed=50,
                    currency="GBP",
                    liquidity=dict(available=20, currency="GBP"),
                    covenant=dict(headroom=1.5, unit="ratio"),
                    tolerances=dict(capital=5),
                ),
                "Below approved minimum: liquidity.",
            ),
            (
                dict(
                    committed=50,
                    currency="GBP",
                    liquidity=-15,
                    covenant=-0.1,
                    covenant_unit="ratio",
                    tolerances=dict(capital=5),
                ),
                "Below approved minimum: liquidity, covenant.",
            ),
            (
                dict(
                    committed=85,
                    currency="GBP",
                    liquidity=30,
                    covenant=1.5,
                    covenant_unit="ratio",
                    tolerances=dict(capital=5),
                ),
                "Over approved limit: annual_plan.",
            ),
        ):
            result = limits.assess(record, exposure)
            self.assertEqual(result["status"], "Breach")
            self.assertEqual(result["signal"], limits.UNAPPROVED)
            self.assertEqual(result["reason"], expected_text)
            self.assertEqual(
                result["pause_signal"],
                dict(
                    paused=True,
                    decision_required=True,
                    decision_owner="Test control owner",
                    automatic_cut=False,
                    reason=expected_text,
                ),
            )

    def test_negative_ceiling_or_unitless_covenant_is_unknown_and_paused(self) -> None:
        record = limits.record_limits(APPROVAL, ENVELOPE, TOLERANCES, liquidity=LIQUIDITY)
        bad_exposures: tuple[Any, ...] = (
            dict(
                committed=-5,
                currency="GBP",
                liquidity=30,
                covenant=1.5,
                covenant_unit="ratio",
                tolerances=dict(capital=5),
            ),
            dict(
                committed=50,
                currency="GBP",
                liquidity=30,
                covenant=1.5,
                tolerances=dict(capital=5),
            ),
            [],
        )
        for exposure in bad_exposures:
            result = limits.assess(record, exposure)
            self.assertEqual((result["status"], result["signal"]), ("Unknown", limits.UNAPPROVED))
            self.assertTrue(result["pause_signal"]["paused"])
            self.assertFalse(result["pause_signal"]["automatic_cut"])

    def test_within_limits_never_approves_acceleration(self) -> None:
        exposure = dict(committed=50, currency="GBP", tolerances=dict(capital=5))
        result = limits.assess(self.record, exposure)
        self.assertEqual(result["signal"], "No pause signal")
        self.assertIn("not approval to accelerate", result["reason"])


if __name__ == "__main__":
    unittest.main()

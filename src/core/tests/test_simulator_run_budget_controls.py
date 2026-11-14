"""Run owner, bounded time limit and GBP budget alert for the simulator."""

import tempfile
import unittest
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

from zava_forward.core.synthetic.run_governance import RunGovernance, RunMeter
from zava_forward.core.synthetic.run_plan import RunController, RunPlan, record
from zava_forward.core.synthetic.sensor_stream import StreamError


def gov(**changes: object) -> RunGovernance:
    base: dict[str, object] = {
        "run_owner": "Juan Manuel Servera",
        "time_limit_seconds": 600,
        "budget_alert_gbp": "4.00",
        "budget_cap_gbp": "5.00",
    }
    base.update(changes)
    return RunGovernance(**base)  # type: ignore[arg-type]


class GovernanceValidation(unittest.TestCase):
    def test_owner_required(self) -> None:
        for owner in ("", "  ", "TBD", None, "<owner>"):
            with self.subTest(owner=owner), self.assertRaisesRegex(StreamError, "RUN_OWNER"):
                gov(run_owner=owner).validate()

    def test_time_limit_must_be_bounded(self) -> None:
        for limit in (None, 0, -1, float("inf"), float("nan"), 3601, True, "60"):
            with self.subTest(limit=limit), self.assertRaisesRegex(StreamError, "TIME_LIMIT"):
                gov(time_limit_seconds=limit).validate()

    def test_budget_alert_must_be_positive_and_below_cap(self) -> None:
        for alert in (0, "-1", "nan", None, True, "5.00", "6"):
            with self.subTest(alert=alert), self.assertRaises(StreamError):
                gov(budget_alert_gbp=alert).validate()


class BudgetMeter(unittest.TestCase):
    def meter(self, now: list[float], **kw: object) -> RunMeter:
        return RunMeter(gov(), lambda: now[0], **kw)  # type: ignore[arg-type]

    def test_alert_fires_once_at_threshold_and_halts_before_cap(self) -> None:
        meter = self.meter([0.0])
        meter.admit("3.50")
        self.assertEqual(meter.events, [])
        meter.admit("0.50")
        meter.admit("0.25")
        alerts = [e for e in meter.events if e["event"] == "budget_alert"]
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["amount_gbp"], "4.00")
        self.assertEqual(alerts[0]["run_owner"], "Juan Manuel Servera")
        with self.assertRaisesRegex(StreamError, "RUN_BUDGET_HALT"):
            meter.admit("0.75")
        self.assertEqual(meter.accumulated_gbp, Decimal("4.25"))
        self.assertLess(meter.accumulated_gbp, meter.cap)
        self.assertEqual(meter.status, "halted")
        self.assertEqual(meter.events[-1]["event"], "budget_halt")
        with self.assertRaisesRegex(StreamError, "RUN_BUDGET_HALT"):
            meter.admit("0.01")

    def test_projected_cost_at_alert_emits_alert_before_run(self) -> None:
        meter = self.meter([0.0], projected_cost_gbp="4.00")
        self.assertEqual([e["basis"] for e in meter.events], ["projected"])

    def test_projected_cost_over_cap_refuses_run(self) -> None:
        with self.assertRaisesRegex(StreamError, "RUN_BUDGET_HALT"):
            self.meter([0.0], projected_cost_gbp="5.01")

    def test_projected_cost_at_cap_or_invalid_is_refused(self) -> None:
        with self.assertRaisesRegex(StreamError, "RUN_BUDGET_HALT"):
            self.meter([0.0], projected_cost_gbp="5.00")
        for bad in (True, "nan", "Infinity", "abc", -1, None):
            with self.subTest(bad=bad), self.assertRaisesRegex(StreamError, "INVALID_BUDGET"):
                self.meter([0.0], projected_cost_gbp=bad)

    def test_admit_rejects_invalid_cost(self) -> None:
        meter = self.meter([0.0])
        for bad in (True, "nan", "Infinity", "x", -1):
            with self.subTest(bad=bad), self.assertRaisesRegex(StreamError, "INVALID_BUDGET"):
                meter.admit(bad)
        meter.admit(0)

    def test_deadline_halt_is_not_misreported_as_budget(self) -> None:
        now = [0.0]
        meter = self.meter(now)
        now[0] = 700.0
        for _ in range(2):
            with self.assertRaisesRegex(StreamError, "RUN_DEADLINE"):
                meter.admit("0.10")

    def test_time_limit_halts_run(self) -> None:
        now = [0.0]
        meter = self.meter(now)
        meter.admit("0.10")
        now[0] = 600.0
        with self.assertRaisesRegex(StreamError, "RUN_DEADLINE"):
            meter.admit("0.10")
        self.assertEqual(meter.events[-1]["event"], "time_limit_halt")

    def test_events_are_deterministic(self) -> None:
        runs = []
        for _ in range(2):
            meter = self.meter([0.0])
            meter.admit("4.10")
            runs.append(meter.events)
        self.assertEqual(runs[0], runs[1])


class RunPlanWiring(unittest.TestCase):
    def controller(self, now: list[float], **changes: object) -> RunController:
        base = RunPlan(
            owner="Juan Manuel Servera",
            homes=10,
            max_seconds=600,
            max_per_second=10,
            budget_usd=5,
            alert_threshold=0.8,
            alert_reference="budget-iot-hub-80pct",
            budget_alert_gbp="4.00",
            budget_cap_gbp="5.00",
        )
        plan = replace(base, **changes)  # type: ignore[arg-type]
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "estimate.json"
        record(plan, path)
        controller = RunController(plan, clock=lambda: now[0])
        controller.start(path)
        return controller

    def test_real_run_alerts_then_halts_and_stops(self) -> None:
        run = self.controller([0.0])
        assert run.meter is not None
        run.admit("4.00")
        self.assertEqual(run.meter.events[0]["event"], "budget_alert")
        with self.assertRaisesRegex(StreamError, "RUN_BUDGET_HALT"):
            run.admit("1.00")
        self.assertEqual(run.state, "stopped")

    def test_run_deadline_stops_controller(self) -> None:
        now = [0.0]
        run = self.controller(now)
        now[0] = 600.0
        with self.assertRaisesRegex(StreamError, "RUN_DEADLINE"):
            run.admit("0.01")
        self.assertEqual(run.state, "stopped")

    def test_invalid_or_partial_governance_refused(self) -> None:
        with self.assertRaisesRegex(StreamError, "INVALID_BUDGET"):
            self.controller([0.0], budget_cap_gbp=None)
        with self.assertRaisesRegex(StreamError, "RUN_BUDGET_HALT"):
            self.controller([0.0], planned_cost_gbp="5.00")

    def test_admit_requires_governance_and_running(self) -> None:
        run = self.controller([0.0], budget_alert_gbp=None, budget_cap_gbp=None)
        with self.assertRaisesRegex(StreamError, "RUN_NOT_RUNNING"):
            run.admit("1")


if __name__ == "__main__":
    unittest.main()

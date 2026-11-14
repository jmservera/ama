"""Run owner, bounded time limit and GBP budget alert for the simulator."""

import tempfile
import unittest
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

from zava_forward.core.synthetic import run_plan
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
        for owner in ("", "  ", "TBD", "TBC", "pending", "a" * 161, None, "<owner>"):
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

    def test_stop_and_halt_freeze_elapsed_and_remaining_seconds(self) -> None:
        now = [10.0]
        meter = self.meter(now)
        meter.check_time_limit()
        now[0] = 35.5
        meter.stop()
        now[0] = 200.0
        meter.stop()
        stopped = meter.summary()
        self.assertEqual(stopped["status"], "stopped")
        self.assertEqual(stopped["elapsed_seconds"], 25.5)
        self.assertEqual(stopped["remaining_seconds"], 574.5)
        self.assertEqual(stopped["budget_alert_gbp"], "4.00")
        with self.assertRaisesRegex(StreamError, "RUN_STOPPED"):
            meter.admit("0.01")
        with self.assertRaisesRegex(StreamError, "RUN_STOPPED"):
            meter.check_time_limit()

        halt_clock = [0.0]
        halted = self.meter(halt_clock)
        halt_clock[0] = 700.0
        with self.assertRaisesRegex(StreamError, "RUN_DEADLINE"):
            halted.check_time_limit()
        halt_clock[0] = 950.0
        halted.stop()
        summary = halted.summary()
        self.assertEqual(summary["status"], "halted")
        self.assertEqual(summary["halt_reason"], "RUN_DEADLINE")
        self.assertEqual(summary["elapsed_seconds"], 700.0)
        self.assertEqual(summary["remaining_seconds"], 0.0)


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
        with self.assertRaisesRegex(StreamError, "INVALID_BUDGET"):
            self.controller(
                [0.0], budget_alert_gbp=None, budget_cap_gbp=None, planned_cost_gbp="1.00"
            )
        for bad_planned in ("nan", "-0.01", 0):
            with (
                self.subTest(bad_planned=bad_planned),
                self.assertRaisesRegex(StreamError, "INVALID_BUDGET"),
            ):
                self.controller([0.0], planned_cost_gbp=bad_planned)
        with self.assertRaisesRegex(StreamError, "INVALID_BUDGET"):
            self.controller([0.0], budget_alert_gbp=4)
        with self.assertRaisesRegex(StreamError, "RUN_BUDGET_HALT"):
            self.controller([0.0], planned_cost_gbp="5.00")
        for placeholder in ("TBC", "pending"):
            with (
                self.subTest(placeholder=placeholder),
                self.assertRaisesRegex(StreamError, "RUN_OWNER_COST_ALERT_REQUIRED"),
            ):
                RunController(
                    RunPlan(
                        owner=placeholder,
                        homes=10,
                        max_seconds=600,
                        max_per_second=10,
                        budget_usd=5,
                        alert_threshold=0.8,
                        alert_reference="budget-iot-hub-80pct",
                    )
                )

    def test_status_reports_owner_time_limit_and_alert_position(self) -> None:
        now = [0.0]
        run = self.controller(now)
        run.admit(Decimal("4.00"))
        now[0] = 12.5
        status = run.status()
        self.assertEqual(status["state"], "running")
        self.assertEqual(status["run_owner"], "Juan Manuel Servera")
        self.assertEqual(status["time_limit_seconds"], 600)
        self.assertEqual(status["elapsed_seconds"], 12.5)
        self.assertEqual(status["remaining_seconds"], 587.5)
        self.assertEqual(status["budget_alert_gbp"], "4.00")
        self.assertEqual(status["alert_fires_at_usd"], 4.0)
        self.assertEqual(status["alert_raised"], True)
        self.assertEqual(status["accumulated_gbp"], "4.00")
        with self.assertRaisesRegex(StreamError, "RUN_BUDGET_HALT"):
            run.admit("1.00")
        now[0] = 99.0
        self.assertEqual(run.status()["state"], "stopped")
        self.assertEqual(run.status()["halt_reason"], "RUN_BUDGET_HALT")
        self.assertEqual(run.status()["elapsed_seconds"], 12.5)

    def test_status_schema_consistent_across_idle_running_and_stopped(self) -> None:
        plan = RunPlan(
            owner="Juan Manuel Servera",
            homes=10,
            max_seconds=600,
            max_per_second=10,
            budget_usd=5,
            alert_threshold=0.8,
            alert_reference="budget-iot-hub-80pct",
            budget_alert_gbp=" 4.00 ",
            budget_cap_gbp="5.00",
        )
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "estimate.json"
        record(plan, path)
        now = [10.0]
        run = RunController(plan, clock=lambda: now[0])
        idle = run.status()
        self.assertEqual(idle["state"], "idle")
        self.assertEqual(idle["elapsed_seconds"], 0.0)
        self.assertEqual(idle["remaining_seconds"], 600)
        self.assertEqual(idle["budget_alert_gbp"], "4.00")
        self.assertEqual(idle["alert_reference"], "budget-iot-hub-80pct")
        self.assertEqual(idle["alert_fires_at_usd"], 4.0)
        self.assertFalse(idle["alert_raised"])
        self.assertIsNone(idle["halt_reason"])

        run.start(path)
        now[0] = 30.0
        run.stop()
        now[0] = 500.0
        run.stop()
        stopped = run.status()
        self.assertEqual(stopped["state"], "stopped")
        self.assertEqual(stopped["status"], "stopped")
        self.assertEqual(stopped["elapsed_seconds"], 20.0)
        self.assertEqual(stopped["remaining_seconds"], 580.0)
        self.assertIsNone(stopped["halt_reason"])
        with self.assertRaisesRegex(StreamError, "RUN_NOT_RUNNING"):
            run.check_time_limit()

        never_started = RunController(plan, clock=lambda: now[0])
        never_started.stop()
        self.assertEqual(never_started.status()["elapsed_seconds"], 0.0)

    def test_check_time_limit_enforces_deadline_with_and_without_gbp_meter(self) -> None:
        now = [0.0]
        usd_only = self.controller(now, budget_alert_gbp=None, budget_cap_gbp=None)
        now[0] = 120.0
        usd_only.check_time_limit()
        now[0] = 605.0
        with self.assertRaisesRegex(StreamError, "RUN_DEADLINE"):
            usd_only.check_time_limit()
        assert usd_only.pacer is not None
        self.assertTrue(usd_only.pacer.stopped)
        now[0] = 900.0
        status = usd_only.status()
        self.assertEqual(status["state"], "stopped")
        self.assertEqual(status["halt_reason"], "RUN_DEADLINE")
        self.assertEqual(status["elapsed_seconds"], 605.0)
        self.assertEqual(status["remaining_seconds"], 0.0)
        with self.assertRaisesRegex(StreamError, "RUN_DEADLINE"):
            usd_only.check_time_limit()

        gbp_clock = [0.0]
        gbp_run = self.controller(gbp_clock)
        gbp_clock[0] = 600.0
        with self.assertRaisesRegex(StreamError, "RUN_DEADLINE"):
            gbp_run.check_time_limit()
        self.assertEqual(gbp_run.status()["halt_reason"], "RUN_DEADLINE")
        with self.assertRaisesRegex(StreamError, "RUN_DEADLINE"):
            gbp_run.check_time_limit()

    def test_status_without_gbp_governance_has_no_budget_alert(self) -> None:
        status = self.controller([0.0], budget_alert_gbp=None, budget_cap_gbp=None).status()
        self.assertIsNone(status["budget_alert_gbp"])
        self.assertEqual(status["alert_fires_at_usd"], 4.0)
        self.assertEqual(status["run_owner"], "Juan Manuel Servera")

    def test_cli_records_gbp_alert_and_refuses_alert_at_cap(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        out = str(Path(directory.name) / "e.json")
        args = [
            "--homes",
            "10",
            "--owner",
            "Juan",
            "--budget-usd",
            "5",
            "--alert-reference",
            "budget-iot-hub-80pct",
            "--out",
            out,
        ]
        self.assertEqual(
            run_plan.main([*args, "--budget-alert-gbp", "4", "--budget-cap-gbp", "5"]), 0
        )
        self.assertEqual(
            run_plan.main([*args, "--budget-alert-gbp", "5", "--budget-cap-gbp", "5"]), 2
        )
        self.assertEqual(run_plan.main([*args, "--planned-cost-gbp", "1.00"]), 2)

    def test_admit_requires_governance_and_running(self) -> None:
        run = self.controller([0.0], budget_alert_gbp=None, budget_cap_gbp=None)
        with self.assertRaisesRegex(StreamError, "RUN_NOT_RUNNING"):
            run.admit("1")


if __name__ == "__main__":
    unittest.main()

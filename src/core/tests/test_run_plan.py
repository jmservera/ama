"""Pre-run estimate, quota headroom and run-control contracts."""

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from zava_forward.core.synthetic import run_plan
from zava_forward.core.synthetic.run_plan import RunController, RunPlan, record
from zava_forward.core.synthetic.sensor_stream import StreamError


def plan(**changes: object) -> RunPlan:
    base = RunPlan(
        owner="Juan Manuel Servera",
        homes=1000,
        max_seconds=600,
        max_per_second=10,
        budget_usd=5,
        alert_threshold=0.8,
        alert_reference="budget-iot-hub-80pct",
    )
    return replace(base, **changes)  # type: ignore[arg-type]


class EstimateTests(unittest.TestCase):
    def test_estimate_counts_messages_quota_and_cost(self) -> None:
        estimate = plan().estimate()
        self.assertEqual(estimate.messages_per_day, 3000)
        self.assertEqual(estimate.metered_units_per_day, 3000)
        self.assertEqual(estimate.headroom_units_per_day, 400_000 - 3000 - 40_000)
        self.assertEqual(estimate.estimated_cost_usd, 0.33)

    def test_60000_homes_fit_b1_but_130000_exceed_headroom(self) -> None:
        big = {"max_seconds": 3600, "max_per_second": 100}
        self.assertEqual(plan(homes=60_000, **big).estimate().headroom_units_per_day, 180_000)
        with self.assertRaisesRegex(StreamError, "B1_QUOTA_HEADROOM"):
            plan(homes=130_000, **big).estimate()

    def test_large_messages_use_more_metered_units(self) -> None:
        small, large = plan().estimate(), plan(message_bytes=4000).estimate()
        self.assertEqual(large.metered_units_per_day, 2 * small.metered_units_per_day)

    def test_refuses_run_that_cannot_finish_in_time_limit(self) -> None:
        with self.assertRaisesRegex(StreamError, "RUN_TIME_LIMIT_TOO_SHORT"):
            plan(max_seconds=10, max_per_second=1).estimate()

    def test_refuses_cost_above_budget_cap(self) -> None:
        with self.assertRaisesRegex(StreamError, "BUDGET_CAP_EXCEEDED"):
            plan(days=30, budget_usd=5, max_seconds=3600, max_per_second=100).estimate()

    def test_owner_alert_and_limits_are_required(self) -> None:
        for bad in (
            {"owner": " "},
            {"alert_reference": ""},
            {"max_seconds": 7200},
            {"alert_threshold": 0},
            {"homes": 0},
        ):
            with self.subTest(bad=bad), self.assertRaises(StreamError):
                plan(**bad).estimate()

    def test_run_budget_derived_from_plan_carries_owner_and_alert(self) -> None:
        budget = plan().budget()
        self.assertEqual(
            (budget.owner, budget.alert_reference), (plan().owner, "budget-iot-hub-80pct")
        )
        self.assertEqual(budget.max_seconds, 600)


class ControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name) / "estimate.json"

    def test_record_is_written_before_run_with_alert_amount(self) -> None:
        body = record(plan(), self.path)
        saved = json.loads(self.path.read_text())
        self.assertEqual(saved["alert_fires_at_usd"], 4.0)
        self.assertEqual(saved["sha256"], body["sha256"])

    def test_start_refused_without_or_with_tampered_record(self) -> None:
        with self.assertRaisesRegex(StreamError, "ESTIMATE_NOT_RECORDED"):
            RunController(plan()).start(self.path)
        record(plan(), self.path)
        saved = json.loads(self.path.read_text())
        saved["estimate"]["estimated_cost_usd"] = 0
        self.path.write_text(json.dumps(saved))
        with self.assertRaisesRegex(StreamError, "ESTIMATE_MISMATCH"):
            RunController(plan()).start(self.path)

    def test_start_refused_when_plan_differs_from_record(self) -> None:
        record(plan(), self.path)
        with self.assertRaisesRegex(StreamError, "ESTIMATE_MISMATCH"):
            RunController(plan(homes=2000)).start(self.path)

    def test_start_stop_and_single_run(self) -> None:
        record(plan(), self.path)
        controller = RunController(plan())
        pacer = controller.start(self.path)
        self.assertEqual(controller.state, "running")
        with self.assertRaisesRegex(StreamError, "RUN_ALREADY_STARTED"):
            controller.start(self.path)
        controller.stop()
        self.assertTrue(pacer.stopped)
        self.assertEqual(controller.state, "stopped")
        with self.assertRaisesRegex(StreamError, "RUN_ALREADY_STARTED"):
            controller.start(self.path)

    def test_scale_down_reduces_homes_and_rate_but_never_up(self) -> None:
        record(plan(), self.path)
        controller = RunController(plan())
        pacer = controller.start(self.path)
        self.assertEqual(controller.scale_down(0.5), 500)
        self.assertEqual(pacer.max_per_second, 5)
        for bad in (1, 1.5, 0, -1):
            with self.subTest(bad=bad), self.assertRaises(StreamError):
                controller.scale_down(bad)
        controller.stop()
        with self.assertRaisesRegex(StreamError, "RUN_NOT_RUNNING"):
            controller.scale_down(0.5)

    def test_deadline_bounds_an_unattended_run(self) -> None:
        record(plan(), self.path)
        now = [0.0]
        controller = RunController(plan(), clock=lambda: now[0])
        pacer = controller.start(self.path)
        self.assertEqual(pacer.deadline, 600)

    def test_cli_records_estimate_and_refuses_over_quota(self) -> None:
        args = [
            "--owner", "owner", "--budget-usd", "5", "--alert-reference", "alert",
            "--max-per-second", "100", "--out", str(self.path),
        ]  # fmt: skip
        self.assertEqual(run_plan.main(["--homes", "1000", *args]), 0)
        self.assertTrue(self.path.exists())
        self.assertEqual(run_plan.main(["--homes", "200000", *args]), 2)


if __name__ == "__main__":
    unittest.main()

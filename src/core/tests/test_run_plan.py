"""Pre-run estimate, quota headroom and run-control contracts."""

import json
import tempfile
import unittest
from dataclasses import asdict, replace
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

    def test_quota_headroom_and_publisher_message_limit(self) -> None:
        big = {"max_seconds": 3600, "max_per_second": 100}
        self.assertEqual(plan(homes=33_333, **big).estimate().headroom_units_per_day, 260_001)
        with self.assertRaisesRegex(StreamError, "RUN_MESSAGE_LIMIT"):
            plan(homes=60_000, **big).estimate()
        with self.assertRaisesRegex(StreamError, "B1_QUOTA_HEADROOM"):
            plan(homes=130_000, **big).estimate()

    def test_whole_multi_day_run_counts_against_daily_quota(self) -> None:
        kwargs = {"homes": 50_000, "days": 2, "message_bytes": 4000,
                  "max_seconds": 3600, "max_per_second": 100, "budget_usd": 5}  # fmt: skip
        with self.assertRaisesRegex(StreamError, "B1_QUOTA_HEADROOM"):
            plan(**kwargs).estimate()

    def test_prior_daily_usage_reduces_headroom_and_reaches_budget(self) -> None:
        big = {"max_seconds": 3600, "max_per_second": 100, "homes": 30_000}
        self.assertEqual(plan(**big).estimate().headroom_units_per_day, 270_000)
        used = plan(daily_used_units=300_000, **big)
        with self.assertRaisesRegex(StreamError, "B1_QUOTA_HEADROOM"):
            used.estimate()
        self.assertEqual(plan(daily_used_units=5).budget().daily_used_units, 5)

    def test_replay_speed_must_fit_time_limit_and_reaches_pacer(self) -> None:
        with self.assertRaisesRegex(StreamError, "RUN_TIME_LIMIT_TOO_SHORT"):
            plan(homes=1, days=1, replay_speed=1).estimate()
        with self.assertRaisesRegex(StreamError, "INVALID_REPLAY_SPEED"):
            plan(replay_speed=0).estimate()
        self.assertEqual(plan(replay_speed=500).estimate().days, 1)

    def test_cost_uses_provisioned_time_not_replay_span(self) -> None:
        one = plan(days=1, max_seconds=3600, max_per_second=100).estimate()
        thirty = plan(days=30, max_seconds=3600, max_per_second=100).estimate()
        self.assertEqual(one.estimated_cost_usd, thirty.estimated_cost_usd)

    def test_estimate_total_fits_run_budget_validation(self) -> None:
        p = plan(homes=33_333, max_seconds=3600, max_per_second=100)
        self.assertLessEqual(p.budget().max_messages, 100_000)

    def test_large_messages_use_more_metered_units(self) -> None:
        small, large = plan().estimate(), plan(message_bytes=4000).estimate()
        self.assertEqual(large.metered_units_per_day, 2 * small.metered_units_per_day)

    def test_refuses_run_that_cannot_finish_in_time_limit(self) -> None:
        with self.assertRaisesRegex(StreamError, "RUN_TIME_LIMIT_TOO_SHORT"):
            plan(max_seconds=10, max_per_second=1).estimate()

    def test_combined_replay_and_send_pacing_must_fit_with_cleanup_reserve(self) -> None:
        tight = {"homes": 100, "max_seconds": 300, "max_per_second": 1, "replay_speed": 1000}
        with self.assertRaisesRegex(StreamError, "RUN_TIME_LIMIT_TOO_SHORT"):
            plan(**tight).estimate()
        self.assertEqual(plan(**{**tight, "max_seconds": 387}).estimate().total_messages, 300)

    def test_refuses_cost_above_budget_cap(self) -> None:
        with self.assertRaisesRegex(StreamError, "BUDGET_CAP_EXCEEDED"):
            plan(budget_usd=0.2).estimate()

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

    def test_start_refused_for_malformed_or_incomplete_record(self) -> None:
        for content in ("[]", "null", "not json"):
            self.path.write_text(content)
            with (
                self.subTest(content=content),
                self.assertRaisesRegex(StreamError, "ESTIMATE_NOT_RECORDED"),
            ):
                RunController(plan()).start(self.path)
        body: dict[str, object] = {"plan": asdict(plan())}
        body["sha256"] = run_plan._digest(body)
        self.path.write_text(json.dumps(body))
        with self.assertRaisesRegex(StreamError, "ESTIMATE_MISMATCH"):
            RunController(plan()).start(self.path)

    def test_start_refused_for_self_consistent_stale_estimate(self) -> None:
        body = record(plan(), self.path)
        body.pop("sha256")
        body["estimate"]["estimated_cost_usd"] = 0  # type: ignore[index]
        body["sha256"] = run_plan._digest(body)
        self.path.write_text(json.dumps(body))
        with self.assertRaisesRegex(StreamError, "ESTIMATE_MISMATCH"):
            RunController(plan()).start(self.path)

    def test_start_refused_when_plan_differs_from_record(self) -> None:
        record(plan(), self.path)
        with self.assertRaisesRegex(StreamError, "ESTIMATE_MISMATCH"):
            RunController(plan(homes=1500)).start(self.path)

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
        self.assertEqual(pacer.speed, 1000)
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

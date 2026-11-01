import json
import time
import unittest
from typing import Any
from unittest.mock import patch

import scale_load


class ScaleLoadReport(unittest.TestCase):
    report: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = scale_load.run(homes=120, sessions=4, rate=8, duration=2)

    def test_reports_declared_versus_executed_without_overclaiming(self) -> None:
        executed = self.report["executed_workload"]
        self.assertEqual(self.report["declared_workload"]["homes"], 60000)
        self.assertEqual(executed["homes"], 120)
        self.assertFalse(executed["meets_declared_workload"])
        self.assertFalse(executed["inference_per_home"])
        self.assertIn("Not production scale", self.report["scope"])

    def test_every_route_answers_without_errors(self) -> None:
        for name, route in self.report["routes"].items():
            with self.subTest(route=name):
                self.assertGreater(route["requests"], 0)
                self.assertEqual(route["errors"], 0)
                self.assertEqual(route["nfr_002_threshold_ms"], scale_load.THRESHOLDS_MS[name])

    def test_cost_drivers_are_measured_and_cost_is_unknown(self) -> None:
        drivers = self.report["cost_drivers"]
        total = sum(r["requests"] for r in self.report["routes"].values())
        self.assertEqual(drivers["requests"], total)
        self.assertEqual(drivers["assistant_calls"], 0)
        self.assertGreater(drivers["sql_statements"], 0)
        self.assertEqual(drivers["replicas"], 1)
        self.assertEqual(drivers["cost"], "Unknown")
        json.dumps(self.report)

    def test_small_fixture_and_dashboard_coverage(self) -> None:
        report = scale_load.run(homes=10, sessions=2, rate=8, duration=1)
        self.assertEqual(report["executed_workload"]["homes"], 10)
        for route in report["routes"].values():
            self.assertEqual(route["errors"], 0)

    def test_transport_failure_is_counted_as_error(self) -> None:
        real = scale_load.call
        seen = {"n": 0}

        def flaky(*args: Any, **kwargs: Any) -> Any:
            seen["n"] += 1
            if seen["n"] > 4:
                raise ConnectionResetError("dropped")
            return real(*args, **kwargs)

        with patch.object(scale_load, "call", flaky):
            report = scale_load.run(homes=10, sessions=2, rate=8, duration=1)
        self.assertGreater(sum(r["errors"] for r in report["routes"].values()), 0)

    def test_resources_are_released_when_login_fails(self) -> None:
        with patch.object(scale_load, "call", return_value=(500, {}, b"")):
            with patch.object(scale_load.ThreadingHTTPServer, "server_close") as closed:
                with self.assertRaises(RuntimeError):
                    scale_load.run(homes=10, sessions=1, rate=1, duration=1)
        closed.assert_called_once()

    def test_slow_responses_stop_at_deadline_and_count_backlog(self) -> None:
        real = scale_load.call

        def slow(*args: Any, **kwargs: Any) -> Any:
            if len(args) > 2:
                time.sleep(0.6)
            return real(*args, **kwargs)

        with patch.object(scale_load, "call", slow):
            report = scale_load.run(homes=10, sessions=1, rate=4, duration=1)
        executed = report["executed_workload"]
        self.assertEqual(executed["observation_window_seconds"], 1.0)
        self.assertGreater(executed["drain_seconds"], 0)
        self.assertLess(executed["in_window_requests_per_second"], 4)
        worst = max(r["p99_ms"] for r in report["routes"].values())
        self.assertGreater(worst, 650)


if __name__ == "__main__":
    unittest.main()

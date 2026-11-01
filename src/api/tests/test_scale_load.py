import json
import unittest
from typing import Any

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


if __name__ == "__main__":
    unittest.main()

"""Retrofit exercise scenarios ingested into the retained store, then analysed (Refs #193).

Exercise values only. Closes the store-backed gap left by
test_retrofit_scenarios_production_consumers: the labelled scenarios pass through the real
SensorConsumer intake and are read back by the production #111 retained-reading entry point.
"""

import tempfile
import unittest
from dataclasses import replace
from datetime import timedelta
from typing import Any, ClassVar, cast

from sensor_consumer_fixture import CONTROL, POLICY, store_at
from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_analysis_store as store
from zava_forward.core.sensor_consumer import SensorConsumer, preflight
from zava_forward.core.synthetic import sensor_scenarios as ss

WINDOW = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))
RECEIVED = WINDOW.end.strftime("%Y-%m-%dT%H:%M:%SZ")
START_TEXT = WINDOW.start.strftime("%Y-%m-%dT%H:%M:%SZ")
POLICY_28 = replace(
    POLICY,
    window_start=START_TEXT,
    window_end=RECEIVED,
    max_past_seconds=(ss.DAYS + 1) * 86400,
)


def rows_of(scenario: dict[str, Any]) -> list[dict[str, str]]:
    return cast(list[dict[str, str]], scenario["rows"])


def controls(scenarios: tuple[dict[str, Any], ...], consent: str = "granted") -> list[Any]:
    return [
        replace(
            CONTROL,
            sensor_id=rows_of(s)[0]["sensor_id"],
            home_id=rows_of(s)[0]["home_id"],
            mapping_start=START_TEXT,
            mapping_end=RECEIVED,
            calibration_start=START_TEXT,
            calibration_end=RECEIVED,
            consent=consent,
        )
        for s in scenarios
    ]


class RetrofitScenarioRetainedStoreTests(unittest.TestCase):
    scenarios: ClassVar[tuple[dict[str, Any], ...]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = tuple(ss.retrofit_exercise_scenarios())

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = store_at(self.tmp.name, reset=True)
        self.addCleanup(self.store.db.close)
        self.consumer = SensorConsumer(self.store)
        if self.consumer.mssql:
            self.skipTest("SQLite-only focused test")

    def add_homes(self, scenarios: tuple[dict[str, Any], ...]) -> None:
        cursor = self.store.db.execute("SELECT * FROM cases WHERE id=?", (CONTROL.home_id,))
        columns = [d[0] for d in cursor.description]
        template = list(cursor.fetchone())
        for number, s in enumerate(scenarios, start=1000):
            row = dict(zip(columns, template, strict=True))
            row.update(id=rows_of(s)[0]["home_id"], seq=number)
            marks = ",".join("?" for _ in columns)
            self.store.db.execute(
                f"INSERT INTO cases ({','.join(columns)}) VALUES ({marks})", tuple(row.values())
            )

    def ingest(self, scenario: dict[str, Any], limit: int | None = None) -> int:
        rows = rows_of(scenario)[:limit]
        accepted = 0
        for start in range(0, len(rows), 100):
            for row in preflight(rows[start : start + 100]):
                accepted += self.consumer.process(row, RECEIVED).status == "accepted"
        return accepted

    def test_every_scenario_is_accepted_and_matches_pure_derivation(self) -> None:
        self.assertEqual(len(self.scenarios), 4)
        self.add_homes(self.scenarios)
        self.consumer.configure(POLICY_28, controls(self.scenarios))
        for s in self.scenarios:
            with self.subTest(case=s["label"]):
                self.assertEqual(self.ingest(s), len(rows_of(s)))
        for s in self.scenarios:
            with self.subTest(case=s["label"]):
                home = rows_of(s)[0]["home_id"]
                retained = store.analyse_retained(self.consumer, home, WINDOW, WINDOW.end)
                pure = sa.derive_signal(home, rows_of(s), WINDOW, WINDOW.end, "granted")
                self.assertEqual(retained, pure)
                self.assertEqual(retained.sufficiency, sa.SUFFICIENT)
                self.assertEqual(retained.priority_effect, "NONE")
                self.assertIsNone(sa.review_task_candidate(retained))
                self.assertTrue(retained.threshold_label.startswith("EXERCISE VALUE"))

    def test_withdrawn_consent_and_partial_ingest_fail_closed(self) -> None:
        s = self.scenarios[0]
        home = rows_of(s)[0]["home_id"]
        self.add_homes((s,))
        self.consumer.configure(POLICY_28, controls((s,), "declined"))
        self.ingest(s, limit=48)
        declined = store.analyse_retained(self.consumer, home, WINDOW, WINDOW.end)
        self.assertEqual((declined.sufficiency, declined.priority_effect), (sa.DECLINED, "NONE"))

        self.consumer.configure(POLICY_28, controls((s,)))
        self.ingest(s, limit=48)
        partial = store.analyse_retained(self.consumer, home, WINDOW, WINDOW.end)
        self.assertNotEqual(partial.sufficiency, sa.SUFFICIENT)
        self.assertEqual(partial.priority_effect, "NONE")

    def test_unmapped_scenario_home_is_not_analysed(self) -> None:
        s = self.scenarios[0]
        self.add_homes(self.scenarios)
        self.consumer.configure(POLICY_28, controls(self.scenarios[1:]))
        self.ingest(s, limit=24)
        signal = store.analyse_retained(self.consumer, rows_of(s)[0]["home_id"], WINDOW, WINDOW.end)
        self.assertNotEqual(signal.sufficiency, sa.SUFFICIENT)
        self.assertEqual(signal.priority_effect, "NONE")


if __name__ == "__main__":
    unittest.main()

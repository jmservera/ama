"""Ground-truth isolation checks for the named anomaly injector (#187)."""

import json
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.synthetic import sensor_faults
from zava_forward.core.synthetic import sensor_injector as si


def clean_rows(count: int = 48) -> list[dict[str, str]]:
    rows = []
    for slot in range(count):
        day, hour = divmod(slot, 24)
        raw = {
            "sensor_id": "SYN001",
            "reading_id": f"SYN001-{slot}",
            "home_id": "H1",
            "observed_at": f"2024-01-{day + 1:02d}T{hour:02d}:00:00Z",
            "temperature_c": "20.00",
            "humidity_pct": "55.00",
            "source_type": "SYNTHETIC",
            "scenario": "SCENARIO_PACK",
            "seed": "1",
        }
        rows.append(sensor_faults.observation(raw))
    return rows


class SensorInjectorTests(unittest.TestCase):
    def test_each_named_scenario_shifts_only_its_window_and_records_truth(self) -> None:
        rows = clean_rows()
        expected = {
            "damp_mould": (15.0, 92.0),
            "underheating": (14.0, 59.0),
            "overheating": (28.0, 45.0),
            "sensor_fault": (20.0, 55.0),
            "post_works_verification": (22.0, 45.0),
        }
        self.assertEqual(set(expected), set(si.SCENARIOS))
        for name, (temperature, humidity) in expected.items():
            with self.subTest(scenario=name):
                result = si.inject(
                    rows, name, sensor_id="SYN001", start_slot=24, end_slot=48, seed=1
                )
                self.assertEqual(result.live_rows[0], rows[0])
                self.assertEqual(float(result.live_rows[30]["temperature_c"]), temperature)
                self.assertEqual(float(result.live_rows[30]["humidity_pct"]), humidity)
                (event,) = result.events
                self.assertEqual(event.scenario, name)
                self.assertEqual(event.row_positions, tuple(range(24, 48)))

    def test_live_rows_and_view_never_carry_truth(self) -> None:
        rows = clean_rows()
        result = si.inject(
            rows, "damp_mould", sensor_id="SYN001", start_slot=0, end_slot=10, seed=1
        )
        blob = json.dumps(result.live_rows)
        self.assertNotIn("damp_mould", blob)
        self.assertNotIn(result.events[0].injection_id, blob)
        for row in result.live_rows:
            self.assertEqual(set(row), si.LIVE_FIELDS)
        self.assertEqual(si.live_view(result.live_rows), result.live_rows)
        self.assertEqual(rows, clean_rows(), "input rows must not be mutated")

    def test_live_view_rejects_labels_and_strips_undeclared_fields(self) -> None:
        row = dict(clean_rows(1)[0])
        for key in si.LEAK_KEYS:
            with self.subTest(key=key), self.assertRaises(si.GroundTruthLeak):
                si.live_view([{**row, key: "x"}])
        self.assertNotIn("extra", si.live_view([{**row, "extra": "x"}])[0])

    def test_labelled_input_is_refused(self) -> None:
        rows = clean_rows()
        rows[0]["injected_fault"] = "STUCK"
        with self.assertRaises(si.GroundTruthLeak):
            si.inject(rows, "overheating", sensor_id="S", start_slot=0, end_slot=2, seed=1)

    def test_bad_scenario_and_window_rejected(self) -> None:
        rows = clean_rows()
        with self.assertRaises(ValueError):
            si.inject(rows, "flood", sensor_id="S", start_slot=0, end_slot=2, seed=1)
        for window in ((-1, 2), (5, 5), (0, 49)):
            with self.subTest(window=window), self.assertRaises(ValueError):
                si.inject(
                    rows,
                    "damp_mould",
                    sensor_id="S",
                    start_slot=window[0],
                    end_slot=window[1],
                    seed=1,
                )

    def test_manifest_is_deterministic_evaluator_only_and_not_overwritten(self) -> None:
        rows = clean_rows()
        first = si.inject(rows, "underheating", sensor_id="S", start_slot=0, end_slot=5, seed=7)
        second = si.inject(rows, "underheating", sensor_id="S", start_slot=0, end_slot=5, seed=7)
        self.assertEqual(si.manifest(first.events, 7), si.manifest(second.events, 7))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "truth.json"
            si.write_manifest(path, first.events, 7)
            payload = json.loads(path.read_text())
            self.assertEqual(payload["events"][0]["expected_outcome"], "REVIEW_CANDIDATE")
            self.assertIn("evaluator-only", payload["audience"])
            with self.assertRaises(FileExistsError):
                si.write_manifest(path, first.events, 7)


if __name__ == "__main__":
    unittest.main()

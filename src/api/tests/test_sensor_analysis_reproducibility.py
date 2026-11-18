"""Sensor analysis is versioned and reproducible from retained readings (Refs #111 criterion 6).

Fictional exercise data only.
"""

import json
import random
import unittest
from dataclasses import replace

from zava_forward.core import sensor_analysis as sa
from zava_forward.core.synthetic import sensor_scenarios as ss

HOME = "HOME-REPRO-1"


def readings(label: str) -> list[dict[str, str]]:
    case = next(c for c in ss.generate() if c.truth.family == "damp" and c.truth.label == label)
    return [dict(r, home_id=HOME) for r in case.rows]


class SensorAnalysisReproducibility(unittest.TestCase):
    def test_output_is_versioned_with_a_sha256_input_digest(self) -> None:
        out = sa.reproduce_sensor_analysis(readings("sustained_high_humidity"))
        self.assertEqual(out["analysis_version"], sa.ANALYSIS_VERSION)
        self.assertEqual(out["signal"]["analysis_version"], sa.ANALYSIS_VERSION)
        self.assertRegex(str(out["input_digest"]), r"^[0-9a-f]{64}$")

    def test_reading_tuples_cover_each_metric_with_unit(self) -> None:
        rows = readings("normal")[:2]
        tuples = sa.reading_tuples(rows)
        self.assertEqual(len(tuples), 4)
        self.assertEqual({t[1] for t in tuples}, {"temperature_c", "humidity_pct"})
        self.assertEqual({t[4] for t in tuples}, {"degC", "percent"})

    def test_reproduction_is_identical_regardless_of_input_order(self) -> None:
        for label in ("sustained_high_humidity", "repeated_overnight_peaks", "normal"):
            rows = readings(label)
            shuffled = list(rows)
            random.Random(111).shuffle(shuffled)
            first = sa.reproduce_sensor_analysis(rows)
            second = sa.reproduce_sensor_analysis(shuffled)
            self.assertEqual(
                json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True), label
            )
            self.assertEqual(first, sa.reproduce_sensor_analysis(rows))

    def test_changed_reading_drifts_the_digest_not_the_version(self) -> None:
        rows = readings("sustained_high_humidity")
        base = sa.reproduce_sensor_analysis(rows)
        changed = [dict(r) for r in rows]
        changed[10]["humidity_pct"] = "12.5"
        drift = sa.reproduce_sensor_analysis(changed)
        self.assertNotEqual(base["input_digest"], drift["input_digest"])
        self.assertEqual(base["analysis_version"], drift["analysis_version"])

    def test_threshold_change_keeps_digest_and_is_visible_in_policy(self) -> None:
        rows = readings("sustained_high_humidity")
        base = sa.reproduce_sensor_analysis(rows)
        strict = sa.reproduce_sensor_analysis(
            rows, replace(sa.AnalysisPolicy(), humidity_threshold_pct=99.0)
        )
        self.assertEqual(base["input_digest"], strict["input_digest"])
        self.assertNotEqual(base["signal"], strict["signal"])

    def test_mixed_homes_are_rejected(self) -> None:
        rows = readings("normal")
        rows[0] = dict(rows[0], home_id="HOME-OTHER")
        with self.assertRaises(ValueError):
            sa.reproduce_sensor_analysis(rows)


if __name__ == "__main__":
    unittest.main()

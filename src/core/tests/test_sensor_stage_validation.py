"""Offline stage parity and exercise ranges, not climate calibration or live proof."""

import math
import statistics
import unittest
from collections.abc import Sequence
from datetime import UTC, datetime
from itertools import groupby
from typing import ClassVar

from zava_forward.core.synthetic import sensor_backfill, sensor_faults, sensor_stock
from zava_forward.core.synthetic.sensor_stream import Replay, replay

SEED = 190
DAYS = 365
ORIGIN = datetime(2024, 1, 1, tzinfo=UTC)
PROFILES = (
    ("terrace", "1945-1979", "morning_evening"),
    ("detached", "1919-1944", "low"),
    ("detached", "pre-1919", "low"),
    ("apartments", "1945-1979", "all_day"),
)
CHANNELS = ("temperature_c", "humidity_pct")
EXERCISE_DOMAINS = ((-10.0, 45.0), (0.0, 100.0))
EXERCISE_MEANS = ((10.0, 30.0), (25.0, 95.0))
EXERCISE_SPREADS = ((0.25, 10.0), (1.0, 30.0))


class SensorStageValidationTests(unittest.TestCase):
    sensors: ClassVar[list[dict[str, object]]]
    stages: ClassVar[dict[str, dict[str, list[dict[str, str]]]]]

    @classmethod
    def setUpClass(cls) -> None:
        selected = sensor_stock.select(
            [
                {
                    "synthetic_home_id": f"VALIDATION-{index}",
                    "building_form_osm": form,
                    "is_synthetic": "true",
                    "monitoring_consent": "granted",
                }
                for index, form in enumerate(("terrace", "detached", "detached", "apartments"), 1)
            ],
            4,
        )
        cls.sensors = selected.sensors(SEED)
        actual = tuple(
            (sensor["dwelling_type"], sensor["age_band"], sensor["heating_pattern"])
            for sensor in cls.sensors
        )
        if actual != PROFILES:
            raise AssertionError(f"Constructed profile contract changed: {actual!r}")
        outdoor = sensor_backfill.outdoor_series(SEED, DAYS, 60, ORIGIN)  # type: ignore[no-untyped-call]
        cls.stages = {
            "backfill": {
                str(sensor["home_id"]): [
                    sensor_faults.observation(row)
                    for row in sensor_backfill.readings(  # type: ignore[no-untyped-call]
                        {**sensor, "fault_profile": "none"}, SEED, DAYS, 60, outdoor, ORIGIN
                    )
                ]
                for sensor in cls.sensors
            },
            "replay": {str(sensor["home_id"]): [] for sensor in cls.sensors},
        }
        for frame in replay(
            selected, Replay(seed=SEED, origin=ORIGIN, days=DAYS, cadence_minutes=60)
        ):
            cls.stages["replay"][frame.row["home_id"]].append(frame.row)

    def assert_domains(self, rows: Sequence[dict[str, str]]) -> None:
        self.assertTrue(rows, "No observations")
        for row in rows:
            for field, (low, high) in zip(CHANNELS, EXERCISE_DOMAINS, strict=True):
                value = float(row[field])
                self.assertTrue(math.isfinite(value), (field, row["observed_at"], value))
                self.assertTrue(low <= value <= high, (field, row["observed_at"], value))

    def assert_not_flatline(self, rows: Sequence[dict[str, str]]) -> None:
        self.assertTrue(rows, "No observations")
        longest = max(
            sum(1 for _ in group)
            for _, group in groupby((row["temperature_c"], row["humidity_pct"]) for row in rows)
        )
        self.assertLess(longest, 24, "Exercise paired flatline limit is 24 hourly slots")

    def assert_seasonal(self, rows: Sequence[dict[str, str]]) -> None:
        january = [row for row in rows if row["observed_at"][5:7] == "01"]
        july = [row for row in rows if row["observed_at"][5:7] == "07"]
        self.assertEqual(len(january), 31 * 24)
        self.assertEqual(len(july), 31 * 24)
        self.assertGreater(
            statistics.mean(float(row["humidity_pct"]) for row in july),
            statistics.mean(float(row["humidity_pct"]) for row in january) + 5.0,
        )
        midnight = {
            month: [
                float(row["temperature_c"]) for row in samples if row["observed_at"][11:13] == "00"
            ]
            for month, samples in (("january", january), ("july", july))
        }
        self.assertEqual([len(values) for values in midnight.values()], [31, 31])
        self.assertGreater(statistics.mean(midnight["july"]), statistics.mean(midnight["january"]))

    def test_annual_rows_and_distribution_summaries_match_exactly(self) -> None:
        for home, expected in self.stages["backfill"].items():
            with self.subTest(home=home):
                observed = self.stages["replay"][home]
                self.assertEqual(len(expected), DAYS * 24)
                self.assertEqual(len(observed), DAYS * 24)
                self.assertEqual(observed, expected)
                for field in CHANNELS:
                    before = [float(row[field]) for row in expected]
                    after = [float(row[field]) for row in observed]
                    for summary in (
                        statistics.mean,
                        statistics.pstdev,
                    ):
                        self.assertEqual(summary(before), summary(after), field)
                    self.assertEqual(
                        statistics.quantiles(before, n=4, method="inclusive"),
                        statistics.quantiles(after, n=4, method="inclusive"),
                        field,
                    )

    def test_both_stages_have_finite_values_inside_exercise_domains(self) -> None:
        for stage, homes in self.stages.items():
            for home, rows in homes.items():
                with self.subTest(stage=stage, home=home):
                    self.assert_domains(rows)
                    for row in rows:
                        self.assertEqual(set(row), set(sensor_faults.READING_FIELDS))
                        self.assertEqual(row["source_type"], "SYNTHETIC")
                        self.assertEqual(row["seed"], str(SEED))

    def test_each_profile_has_exercise_annual_mean_and_population_spread(self) -> None:
        for stage, homes in self.stages.items():
            for home, rows in homes.items():
                for field, means, spreads in zip(
                    CHANNELS, EXERCISE_MEANS, EXERCISE_SPREADS, strict=True
                ):
                    with self.subTest(stage=stage, home=home, field=field):
                        values = [float(row[field]) for row in rows]
                        mean, spread = statistics.mean(values), statistics.pstdev(values)
                        self.assertTrue(means[0] <= mean <= means[1], mean)
                        self.assertTrue(spreads[0] <= spread <= spreads[1], spread)

    def test_each_profile_retains_exercise_seasonal_structure(self) -> None:
        for stage, homes in self.stages.items():
            for home, rows in homes.items():
                with self.subTest(stage=stage, home=home):
                    self.assert_seasonal(rows)

    def test_seasonal_guard_rejects_repeated_month_channel_mutations(self) -> None:
        rows = self.stages["replay"]["VALIDATION-1"]
        january = [row for row in rows if row["observed_at"][5:7] == "01"]
        for field in CHANNELS:
            with self.subTest(field=field):
                mutated = [
                    {
                        **row,
                        field: january[
                            (int(row["observed_at"][8:10]) - 1) * 24
                            + int(row["observed_at"][11:13])
                        ][field],
                    }
                    if row["observed_at"][5:7] == "07"
                    else row
                    for row in rows
                ]
                with self.assertRaises(AssertionError):
                    self.assert_seasonal(mutated)

    def test_all_day_profile_retains_exercise_winter_diurnal_structure(self) -> None:
        for stage, homes in self.stages.items():
            with self.subTest(stage=stage):
                january = [row for row in homes["VALIDATION-4"] if row["observed_at"][5:7] == "01"]
                groups = {
                    hour: [
                        float(row["temperature_c"])
                        for row in january
                        if row["observed_at"][11:13] == hour
                    ]
                    for hour in ("00", "12")
                }
                self.assertEqual([len(values) for values in groups.values()], [31, 31])
                self.assertGreater(statistics.mean(groups["12"]), statistics.mean(groups["00"]) + 1)

    def test_both_clean_stages_have_no_day_long_paired_flatline(self) -> None:
        for stage, homes in self.stages.items():
            for home, rows in homes.items():
                with self.subTest(stage=stage, home=home):
                    self.assert_not_flatline(rows)

    def test_domain_guard_rejects_nonfinite_and_out_of_bounds_mutations(self) -> None:
        for field, value in (
            ("temperature_c", "nan"),
            ("humidity_pct", "inf"),
            ("temperature_c", "46"),
            ("humidity_pct", "101"),
        ):
            with self.subTest(field=field, value=value):
                rows = self.stages["replay"]["VALIDATION-1"][:24]
                with self.assertRaises(AssertionError):
                    self.assert_domains([{**rows[0], field: value}, *rows[1:]])

    def test_flatline_guard_rejects_held_pair_mutation(self) -> None:
        rows = self.stages["replay"]["VALIDATION-1"][:25]
        held = [
            {
                **row,
                "temperature_c": rows[0]["temperature_c"],
                "humidity_pct": rows[0]["humidity_pct"],
            }
            for row in rows[:24]
        ]
        with self.assertRaises(AssertionError):
            self.assert_not_flatline([*held, rows[24]])


if __name__ == "__main__":
    unittest.main()

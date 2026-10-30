"""Statistical seam contracts with constructed weather, never private inputs."""

import unittest
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from zava_forward.core.synthetic import retrofit_effects, sensor_stock
from zava_forward.core.synthetic.sensor_consistency import Tolerance, report
from zava_forward.core.synthetic.sensor_stream import Replay, descriptor, replay

START = datetime(2024, 10, 1, tzinfo=UTC)
HANDOVER = "2024-10-03T00:00:00Z"


class ConstructedClimate:
    def series(self, start: datetime, days: int, cadence: int) -> list[tuple[float, float]]:
        return [(2.0 + slot % 3, 70.0 + slot % 2) for slot in range(days * 1440 // cadence)]

    def manifest(self) -> dict[str, object]:
        return {"source": "CONSTRUCTED TEST ONLY", "sha256": "a" * 64}


def selection() -> sensor_stock.Selection:
    return sensor_stock.select(
        [
            {
                "synthetic_home_id": home,
                "is_synthetic": "true",
                "monitoring_consent": consent,
                "building_form_osm": "terrace",
            }
            for home, consent in (
                ("ZF-1", "granted"),
                ("stock-home-0000000000002", "granted"),
                ("declined-home", "declined"),
            )
        ],
        3,
    )


def measures() -> tuple[retrofit_effects.Measure, ...]:
    return (
        retrofit_effects.Measure("M1", "ZF-1", "Loft insulation", START + timedelta(days=2), True),
    )


def rows() -> list[dict[str, str]]:
    return [
        frame.row
        for frame in replay(
            selection(), Replay(days=4), climate=ConstructedClimate(), measures=measures()
        )
    ]


class HandoverTests(unittest.TestCase):
    def test_composed_suffix_provenance_and_legacy_compatibility(self) -> None:
        selected, spec, climate, history = (
            selection(),
            Replay(days=4),
            ConstructedClimate(),
            measures(),
        )
        full = replay(selected, spec, climate=climate, measures=history)
        suffix = replay(
            selected, replace(spec, first_slot=5, end_slot=9), climate=climate, measures=history
        )
        self.assertEqual(suffix, tuple(frame for frame in full if 5 <= frame.slot < 9))
        desc = descriptor(selected, spec, climate=climate, measures=history)
        self.assertEqual(desc["model"], "sensor-backfill-integrated-v2")
        self.assertEqual(desc["climate"], climate.manifest())
        self.assertNotEqual(
            desc["retrofit_history_sha256"],
            descriptor(selected, spec, climate=climate)["retrofit_history_sha256"],
        )
        self.assertNotEqual(full, replay(selected, spec))
        with self.assertRaisesRegex(ValueError, "explicit climate"):
            replay(selected, spec, measures=history)
        with self.assertRaisesRegex(ValueError, "selected synthetic register"):
            replay(
                selected,
                spec,
                climate=climate,
                measures=(replace(history[0], home_id="missing"),),
            )

    def test_zero_tolerance_clean_report_and_suffix_drift(self) -> None:
        reference = rows()
        result = report(reference, reference, handover=HANDOVER)
        self.assertTrue(result["passed"])
        series = result["series"]
        assert isinstance(series, list)
        self.assertEqual(len(series), 2)
        self.assertTrue(all(item["before_count"] == item["after_count"] == 6 for item in series))
        for channel in ("temperature_c", "humidity_pct"):
            changed = [
                {
                    **row,
                    channel: (
                        f"{float(row[channel]) + 0.50:.2f}"
                        if row["observed_at"] >= HANDOVER
                        else row[channel]
                    ),
                }
                for row in reference
            ]
            self.assertFalse(report(changed, reference, handover=HANDOVER)["passed"])

    def test_nonzero_inclusive_limits_and_independent_metrics(self) -> None:
        reference = rows()
        for row in reference:
            row.update(temperature_c="20.00", humidity_pct="50.00")
        for channel in ("temperature_c", "humidity_pct"):
            for delta, limit, passed in (
                (0.49, 0.5, True),
                (0.50, 0.5, True),
                (0.51, 0.5, False),
                (0.09, 0.1, True),
                (0.10, 0.1, True),
                (0.11, 0.1, False),
            ):
                changed = [
                    {
                        **row,
                        channel: f"{float(row[channel]) + delta:.2f}"
                        if row["observed_at"] >= HANDOVER
                        else row[channel],
                    }
                    for row in reference
                ]
                with self.subTest(channel=channel, delta=delta):
                    self.assertEqual(
                        report(
                            changed,
                            reference,
                            handover=HANDOVER,
                            temperature=(
                                Tolerance(point=limit, mean_step=limit, stddev=limit)
                                if channel == "temperature_c"
                                else Tolerance()
                            ),
                            humidity=(
                                Tolerance(point=limit, mean_step=limit, stddev=limit)
                                if channel == "humidity_pct"
                                else Tolerance()
                            ),
                        )["passed"],
                        passed,
                    )
            for metric, tolerance, pattern in (
                ("point", Tolerance(point=0.49, mean_step=1, stddev=1), (0.5, 0.5)),
                ("mean_step", Tolerance(point=1, mean_step=0.49, stddev=1), (0.5, 0.5)),
                ("stddev", Tolerance(point=1, mean_step=1, stddev=0.49), (-0.5, 0.5)),
            ):
                changed = [
                    {
                        **row,
                        channel: f"{float(row[channel]) + pattern[index % 2]:.2f}"
                        if row["observed_at"] >= HANDOVER
                        else row[channel],
                    }
                    for index, row in enumerate(reference)
                ]
                # Each home's consecutive samples alternate, independently of interleaving.
                if metric == "stddev":
                    for home in {row["home_id"] for row in changed}:
                        after = [
                            row
                            for row in changed
                            if row["home_id"] == home and row["observed_at"] >= HANDOVER
                        ]
                        for index, row in enumerate(after):
                            row[channel] = (
                                f"{float(reference[0][channel]) + pattern[index % 2]:.2f}"
                            )
                result = report(
                    changed,
                    reference,
                    handover=HANDOVER,
                    temperature=tolerance if channel == "temperature_c" else Tolerance(),
                    humidity=tolerance if channel == "humidity_pct" else Tolerance(),
                )
                series = result["series"]
                assert isinstance(series, list)
                checks = series[0]["metrics"][channel]["checks"]
                with self.subTest(channel=channel, metric=metric):
                    self.assertEqual(checks, {name: name != metric for name in checks})
            for delta, passed in ((0.09, True), (0.10, True), (0.11, False)):
                changed = [dict(row) for row in reference]
                for home in {row["home_id"] for row in changed}:
                    after = [
                        row
                        for row in changed
                        if row["home_id"] == home and row["observed_at"] >= HANDOVER
                    ]
                    for index, row in enumerate(after):
                        row[channel] = (
                            f"{float(row[channel]) + (-delta if index % 2 else delta):.2f}"
                        )
                tolerance = Tolerance(point=1, mean_step=1, stddev=0.1)
                result = report(
                    changed,
                    reference,
                    handover=HANDOVER,
                    temperature=tolerance if channel == "temperature_c" else Tolerance(),
                    humidity=tolerance if channel == "humidity_pct" else Tolerance(),
                )
                with self.subTest(channel=channel, stddev_delta=delta):
                    self.assertEqual(result["passed"], passed)

    def test_nonconstant_reference_mean_step_inclusive_boundary(self) -> None:
        home_rows = [row for row in rows() if row["home_id"] == "ZF-1"][:6]
        boundary = home_rows[3]["observed_at"]
        for channel in ("temperature_c", "humidity_pct"):
            for before_count in (3, 2):
                reference = [
                    {**row, channel: "9.99" if index == before_count else "10.00"}
                    for index, row in enumerate(home_rows[3 - before_count :])
                ]
                offset = Decimal("0.02") if before_count == 2 else Decimal("0.00")
                for sign in (-1, 1):
                    for delta, passed in (("0.09", True), ("0.10", True), ("0.11", False)):
                        step = sign * Decimal(delta)
                        changed = []
                        for index, row in enumerate(reference):
                            adjustment = offset + (step if index >= before_count else Decimal(0))
                            changed.append(
                                {**row, channel: f"{Decimal(row[channel]) + adjustment:.2f}"}
                            )
                        tolerance = Tolerance(point=1, mean_step=0.1, stddev=1)
                        result = report(
                            changed,
                            reference,
                            handover=boundary,
                            temperature=tolerance if channel == "temperature_c" else Tolerance(),
                            humidity=tolerance if channel == "humidity_pct" else Tolerance(),
                        )
                        series = result["series"]
                        assert isinstance(series, list)
                        metrics = series[0]["metrics"][channel]
                        with self.subTest(
                            channel=channel, before_count=before_count, sign=sign, delta=delta
                        ):
                            self.assertEqual(series[0]["before_count"], before_count)
                            self.assertEqual(series[0]["after_count"], 3)
                            self.assertEqual(result["passed"], passed)
                            self.assertEqual(
                                metrics["checks"],
                                {"point": True, "mean_step": passed, "stddev": True},
                            )
                            self.assertEqual(metrics["mean_step_error"], float(delta))

    def test_invalid_tolerances_and_configuration(self) -> None:
        for value in (-1, float("nan"), float("inf"), True):
            for field in ("point", "mean_step", "stddev"):
                with self.subTest(value=value, field=field), self.assertRaises(ValueError):
                    Tolerance(**{field: value})
        reference = rows()
        for cadence in (0, 7, True):
            with self.assertRaisesRegex(ValueError, "CONFIGURATION"):
                report(reference, reference, handover=HANDOVER, cadence_minutes=cadence)
        for boundary in ("2024-10-01T00:00:00Z", "2024-10-04T16:00:00Z"):
            with self.assertRaisesRegex(ValueError, "INSUFFICIENT"):
                report(reference, reference, handover=boundary)

    def test_coverage_metadata_and_numeric_negative_controls(self) -> None:
        reference = rows()
        for field, value in (
            ("home_id", "another-home"),
            ("sensor_id", "ANOTHER"),
            ("reading_id", "ANOTHER"),
            ("observed_at", "2024-10-03T00:00:01Z"),
            ("temperature_unit", "degF"),
            ("humidity_unit", "fraction"),
            ("schema_version", "other"),
            ("temperature_c", "nan"),
            ("calibrated", "false"),
        ):
            changed = [dict(row) for row in reference]
            changed[12][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                report(changed, reference, handover=HANDOVER)
        for changed in ([], reference[:-1], reference + [reference[0]]):
            with self.assertRaises(ValueError):
                report(changed, reference, handover=HANDOVER)
        # A shared gap in actual/reference is not accepted as a regular series.
        missing = [row for row in reference if row["observed_at"] != "2024-10-02T08:00:00Z"]
        with self.assertRaisesRegex(ValueError, "CADENCE"):
            report(missing, missing, handover=HANDOVER)

import json
import unittest
from datetime import UTC, date, datetime, timedelta

from zava_forward.core.synthetic import live_readings as lr

DAY = date(2026, 11, 4)
START = datetime(2026, 11, 4, tzinfo=UTC)
HOMES = ("HOME-001", "HOME-002", "HOME-003")


def slots(day: date = DAY) -> list[datetime]:
    first = datetime(day.year, day.month, day.day, tzinfo=UTC)
    return [first + timedelta(seconds=lr.SLOT_SECONDS * i) for i in range(lr.SLOTS_PER_DAY)]


class AnchorTests(unittest.TestCase):
    def test_anchor_means_equal_daily_averages(self) -> None:
        for month in range(1, 13):
            day = date(2026, month, 15)
            averages = lr.seasonal_averages(day)
            anchors = lr.anchors_from_averages(averages, day)
            self.assertEqual(len(anchors.temperature_c), 24)
            self.assertAlmostEqual(sum(anchors.temperature_c) / 24, averages.temperature_c, 6)
            self.assertAlmostEqual(sum(anchors.humidity_pct) / 24, averages.humidity_pct, 6)
            self.assertAlmostEqual(sum(anchors.sunlight_wm2) / 24, averages.sunlight_wm2, 6)
            self.assertEqual(min(anchors.sunlight_wm2) >= 0, True)
            self.assertEqual(anchors.sunlight_wm2[0], 0.0)
            self.assertGreater(anchors.sunlight_wm2[12], 0.0)

    def test_invalid_averages_are_rejected_with_a_fixed_code(self) -> None:
        for bad in (
            lr.DailyAverages(float("nan"), 50, 10),
            lr.DailyAverages(10, 101, 10),
            lr.DailyAverages(10, 50, -1),
            lr.DailyAverages(99, 50, 10),
        ):
            with self.assertRaises(lr.LiveReadingError) as ctx:
                lr.anchors_from_averages(bad, DAY)
            self.assertEqual(str(ctx.exception), "INVALID_DAILY_AVERAGES")

    def test_bad_anchor_source_is_rejected(self) -> None:
        generator = lr.Generator(1, lambda day: lr.HourlyAnchors((1.0,), (1.0,), (1.0,)))
        with self.assertRaises(lr.LiveReadingError):
            generator.reading("HOME-001", START)


class SlotTests(unittest.TestCase):
    def test_floor_aligns_to_five_minute_utc_slots(self) -> None:
        moment = datetime(2026, 11, 4, 15, 58, 19, 698000, tzinfo=UTC)
        self.assertEqual(lr.slot_floor(moment), datetime(2026, 11, 4, 15, 55, tzinfo=UTC))
        self.assertEqual(lr.next_slot(moment), datetime(2026, 11, 4, 16, 0, tzinfo=UTC))
        exact = datetime(2026, 11, 4, 16, 0, tzinfo=UTC)
        self.assertEqual(lr.slot_floor(exact), exact)
        self.assertEqual(lr.next_slot(exact), exact + timedelta(minutes=5))

    def test_naive_time_is_rejected(self) -> None:
        with self.assertRaises(lr.LiveReadingError):
            lr.slot_floor(datetime(2026, 11, 4, 15, 58))

    def test_non_utc_offset_is_converted(self) -> None:
        from datetime import timezone

        local = datetime(2026, 11, 4, 17, 2, tzinfo=timezone(timedelta(hours=2)))
        self.assertEqual(lr.slot_floor(local), datetime(2026, 11, 4, 15, 0, tzinfo=UTC))

    def test_reading_timestamp_is_slot_aligned(self) -> None:
        reading = lr.Generator(7).reading("HOME-001", datetime(2026, 11, 4, 9, 7, 41, tzinfo=UTC))
        self.assertEqual(reading.observed_at, datetime(2026, 11, 4, 9, 5, tzinfo=UTC))
        self.assertEqual(reading.row()["observed_at"], "2026-11-04T09:05:00Z")


class GeneratorTests(unittest.TestCase):
    def test_same_seed_home_and_slot_is_reproducible(self) -> None:
        first = [lr.Generator(184).reading("HOME-001", s).body() for s in slots()]
        second = [lr.Generator(184).reading("HOME-001", s).body() for s in slots()]
        self.assertEqual(first, second)

    def test_seed_and_home_change_values(self) -> None:
        moment = datetime(2026, 11, 4, 12, 0, tzinfo=UTC)
        base = lr.Generator(184).reading("HOME-001", moment).row()
        self.assertNotEqual(base, lr.Generator(185).reading("HOME-001", moment).row())
        self.assertNotEqual(
            base["temperature_c"],
            lr.Generator(184).reading("HOME-002", moment).row()["temperature_c"],
        )

    def test_noise_and_offset_stay_within_documented_bounds(self) -> None:
        generator = lr.Generator(184)
        for home in HOMES:
            off_t, off_h, off_s = generator.offsets(home)
            self.assertLessEqual(abs(off_t), lr.OFFSET_TEMPERATURE_C)
            self.assertLessEqual(abs(off_h), lr.OFFSET_HUMIDITY_PCT)
            self.assertLessEqual(abs(off_s - 1), lr.OFFSET_SUNLIGHT_FRACTION)
            for slot in slots():
                base_t, base_h, base_s = generator.baseline(slot)
                r = generator.reading(home, slot)
                self.assertLessEqual(
                    abs(r.temperature_c - base_t - off_t), lr.NOISE_TEMPERATURE_C + 1e-9
                )
                if 0 < r.humidity_pct < 100:
                    self.assertLessEqual(
                        abs(r.humidity_pct - base_h - off_h), lr.NOISE_HUMIDITY_PCT + 1e-9
                    )
                self.assertLessEqual(
                    abs(r.sunlight_wm2 - base_s * off_s),
                    base_s * off_s * lr.NOISE_SUNLIGHT_FRACTION + 1e-9,
                )

    def test_physical_ranges_hold_all_year(self) -> None:
        generator = lr.Generator(3)
        for month in range(1, 13):
            for slot in slots(date(2026, month, 1))[::7]:
                r = generator.reading("HOME-001", slot)
                self.assertTrue(0 <= r.humidity_pct <= 100)
                self.assertGreaterEqual(r.sunlight_wm2, 0)
                self.assertTrue(-40 < r.temperature_c < 50)

    def test_series_is_smooth_between_slots(self) -> None:
        generator = lr.Generator(184)
        points = [generator.reading("HOME-001", s) for s in slots()]
        points.append(generator.reading("HOME-001", START + timedelta(days=1)))
        for a, b in zip(points, points[1:], strict=False):
            self.assertLess(abs(a.temperature_c - b.temperature_c), 0.6)
            self.assertLess(abs(a.humidity_pct - b.humidity_pct), 2.5)

    def test_baseline_hits_hour_anchors_and_blends_between_them(self) -> None:
        generator = lr.Generator(1)
        anchors = generator.anchors(DAY)
        for hour in range(24):
            at = START + timedelta(hours=hour)
            self.assertAlmostEqual(generator.baseline(at)[0], anchors.temperature_c[hour], 9)
            self.assertAlmostEqual(generator.baseline(at)[1], anchors.humidity_pct[hour], 9)
        midpoint = generator.baseline(START + timedelta(hours=14, minutes=30))[0]
        low, high = sorted((anchors.temperature_c[14], anchors.temperature_c[15]))
        self.assertTrue(low <= midpoint <= high)
        self.assertAlmostEqual(midpoint, (low + high) / 2, 9)

    def test_hour_23_blends_into_next_day_and_noise_is_continuous(self) -> None:
        generator = lr.Generator(5)
        last = generator.reading("HOME-001", START + timedelta(hours=23, minutes=55))
        midnight = generator.reading("HOME-001", START + timedelta(days=1))
        self.assertLess(abs(last.temperature_c - midnight.temperature_c), 0.6)
        self.assertLess(abs(last.humidity_pct - midnight.humidity_pct), 2.5)

    def test_custom_anchor_source_is_used(self) -> None:
        flat = lr.HourlyAnchors((10.0,) * 24, (60.0,) * 24, (0.0,) * 24)
        generator = lr.Generator(2, lambda day: flat)
        r = generator.reading("HOME-001", START + timedelta(hours=6))
        self.assertEqual(r.sunlight_wm2, 0.0)
        self.assertLess(abs(r.temperature_c - 10), 1.4 + 1e-9)

    def test_invalid_inputs_use_fixed_codes(self) -> None:
        with self.assertRaises(lr.LiveReadingError) as ctx:
            lr.Generator("x")  # type: ignore[arg-type]
        self.assertEqual(str(ctx.exception), "INVALID_SEED")
        with self.assertRaises(lr.LiveReadingError) as ctx:
            lr.Generator(1).reading(" bad ", START)
        self.assertEqual(str(ctx.exception), "INVALID_HOME_ID")


class MessageTests(unittest.TestCase):
    def test_message_is_labelled_synthetic_with_units_and_identity(self) -> None:
        reading = lr.Generator(184).reading("HOME-001", START)
        row = json.loads(reading.body())
        self.assertEqual(row["source_type"], "SYNTHETIC")
        self.assertIn("SYNTHETIC", row["label"])
        self.assertEqual(row["sunlight_unit"], "W/m2")
        self.assertEqual(row["schema_version"], lr.SCHEMA_VERSION)
        self.assertEqual(reading.device_id, "SYN-" + reading.sensor_id)
        self.assertTrue(reading.reading_id.startswith("LIVE-" + reading.sensor_id))
        self.assertEqual(row["home_id"], "HOME-001")
        for key in ("temperature_c", "humidity_pct", "sunlight_wm2"):
            float(row[key])
        self.assertLess(len(reading.body()), lr.MAX_BODY_BYTES)

    def test_reading_ids_are_unique_per_home_and_slot(self) -> None:
        generator = lr.Generator(184)
        ids = {generator.reading(h, s).reading_id for h in HOMES for s in slots()}
        self.assertEqual(len(ids), len(HOMES) * lr.SLOTS_PER_DAY)

    def test_body_carries_no_secret_like_fields(self) -> None:
        body = lr.Generator(1).reading("HOME-001", START).body().decode("ascii").lower()
        for word in ("key", "connection", "password", "token", "sharedaccess"):
            self.assertNotIn(word, body)


class ScenarioTests(unittest.TestCase):
    def test_default_scenario_is_unchanged_and_reference_differs_only_by_provenance(self) -> None:
        slot = datetime(2024, 10, 1, 1, 0, tzinfo=UTC)
        live = lr.Generator(184).reading("ZF-1", slot).row()
        self.assertEqual(live["scenario"], "live-simulator")
        reference = lr.Generator(184, scenario=lr.WEATHER_REFERENCE_SCENARIO).reading("ZF-1", slot)
        self.assertEqual({k for k in live if live[k] != reference.row()[k]}, {"scenario"})
        with self.assertRaisesRegex(lr.LiveReadingError, "INVALID_SCENARIO"):
            lr.Generator(184, scenario="indoor-damp")


if __name__ == "__main__":
    unittest.main()

"""Deterministic neutral fixture variation and monitoring exclusion."""

import collections
import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from zava_forward.core.synthetic import household_conditions as hc

AT = datetime(2025, 1, 1, tzinfo=UTC)
HOME = "opaque-stock-anchor-001"


class HouseholdConditionsTests(unittest.TestCase):
    def test_seed_home_and_order_reproducibility(self) -> None:
        times = [AT + timedelta(hours=i) for i in range(48)]
        a = hc.conditions(HOME, 7, "granted", times, is_synthetic=True)
        self.assertEqual(
            a, hc.conditions(HOME, 7, "granted", list(reversed(times)), is_synthetic=True)
        )
        self.assertNotEqual(a, hc.conditions(HOME, 8, "granted", times, is_synthetic=True))
        self.assertNotEqual(
            hc.profile(HOME, 7, "granted", is_synthetic=True),
            hc.profile("other-stock-home", 7, "granted", is_synthetic=True),
        )
        self.assertEqual(
            a[24:],
            hc.conditions(HOME, 7, "granted", times[24:], is_synthetic=True),
        )
        self.assertTrue(all(row.home_id == HOME and row.source_type == "SYNTHETIC" for row in a))

    def test_declined_unknown_have_no_conditions_or_rng_draws(self) -> None:
        for choice in ("declined", "unknown"):
            with (
                self.subTest(choice=choice),
                patch("zava_forward.core.synthetic.household_conditions.random.Random") as rng,
            ):
                self.assertIsNone(hc.profile(HOME, 7, choice, is_synthetic=True))
                self.assertEqual(hc.conditions(HOME, 7, choice, [AT], is_synthetic=True), ())
                rng.assert_not_called()

    def test_distributions_and_neutral_output_fields(self) -> None:
        profiles = [
            hc.profile(f"existing-home-{i}", 7, "granted", is_synthetic=True) for i in range(3000)
        ]
        schedules: collections.Counter[str] = collections.Counter()
        occupancy: collections.Counter[str] = collections.Counter()
        hours: set[int] = set()
        for p in profiles:
            assert p is not None
            schedules[p.heating_schedule] += 1
            occupancy[p.occupancy_pattern] += 1
            hours.add(p.drying_hour_utc)
            self.assertTrue(18 <= p.setpoint_c <= 22)
            self.assertTrue(0.8 <= p.ventilation_multiplier <= 1.2)
            self.assertTrue(0.8 <= p.occupied_moisture_hpa <= 1.6)
            self.assertTrue(0.2 <= p.drying_increment_hpa <= 0.8)
        for counts in (schedules, occupancy):
            self.assertEqual(len(counts), 3)
            for count in counts.values():
                self.assertAlmostEqual(count / len(profiles), 1 / 3, delta=0.035)
        self.assertEqual(hours, set(range(24)))
        self.assertEqual(
            set(hc.Condition.__dataclass_fields__),
            {
                "home_id",
                "observed_at",
                "occupied",
                "setpoint_c",
                "ventilation_multiplier",
                "moisture_increment_hpa",
                "source_type",
                "model_version",
            },
        )

    def test_schedule_boundaries_and_drying(self) -> None:
        times = [AT + timedelta(hours=i) for i in range(24)]
        for schedule in hc.SCHEDULES:
            p = hc.Profile(schedule, "daytime", 21.0, 1.1, 1.2, 0.5, 12)
            with patch.object(hc, "profile", return_value=p):
                rows = hc.conditions(HOME, 7, "granted", times, is_synthetic=True)
            active = {
                "morning_evening": {6, 7, 8, 17, 18, 19, 20, 21},
                "extended_day": set(range(7, 23)),
                "evening": set(range(17, 22)),
            }[schedule]
            self.assertEqual({r.observed_at.hour for r in rows if r.setpoint_c == 21}, active)
            self.assertEqual({r.observed_at.hour for r in rows if r.occupied}, set(range(8, 20)))
            self.assertEqual(rows[12].moisture_increment_hpa, 1.7)
            self.assertEqual(rows[11].moisture_increment_hpa, 1.2)
            self.assertEqual(rows[0].moisture_increment_hpa, 0.4)

    def test_invalid_inputs_are_explicit_errors(self) -> None:
        for home, seed, choice, synthetic in (
            ("", 7, "granted", True),
            ("padded ", 7, "granted", True),
            (HOME, True, "granted", True),
            (HOME, 2**63, "granted", True),
            (HOME, 7, "yes", True),
            (HOME, 7, "granted", False),
        ):
            with self.subTest(home=home, seed=seed, choice=choice), self.assertRaises(ValueError):
                hc.conditions(home, seed, choice, [AT], is_synthetic=synthetic)
        for times in ([AT, AT], [AT.replace(tzinfo=None)], [AT.replace(microsecond=1)]):
            with self.subTest(times=times), self.assertRaises(ValueError):
                hc.conditions(HOME, 7, "granted", times, is_synthetic=True)

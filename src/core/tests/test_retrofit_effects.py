"""Exact timing and identity tests using wholly fictional measure records."""

import math
import unittest
from datetime import UTC, datetime, timedelta, timezone

from zava_forward.core.synthetic import retrofit_effects as re

AT = datetime(2025, 6, 1, 12, tzinfo=UTC)
HOME = "opaque-stock-anchor-001"


def measure(identifier: str = "M1", home: str = HOME, kind: str = "Loft insulation") -> re.Measure:
    return re.Measure(identifier, home, kind, AT, True)


class RetrofitEffectsTests(unittest.TestCase):
    def test_completion_boundary_is_inclusive_not_calendar_date_only(self) -> None:
        history = [measure()]
        self.assertEqual(re.apply_loss(1.3, HOME, AT - timedelta(seconds=1), history), 1.3)
        self.assertEqual(re.apply_loss(1.3, HOME, AT, history), 1.3 * 0.9)
        self.assertEqual(re.apply_loss(1.3, HOME, AT + timedelta(seconds=1), history), 1.3 * 0.9)
        self.assertEqual(re.effect(HOME, AT, history).active_measure_ids, ("M1",))

    def test_no_history_or_other_home_has_no_step(self) -> None:
        for history in ([], [measure(home="different-stock-home")]):
            for at in (AT - timedelta(days=1), AT, AT + timedelta(days=1)):
                self.assertEqual(re.effect(HOME, at, history).loss_multiplier, 1.0)
                self.assertEqual(re.apply_loss(1.3, HOME, at, history), 1.3)

    def test_cumulative_order_independent_documented_effects(self) -> None:
        history = [
            measure("M2", kind="Cavity wall"),
            measure("M1"),
            re.Measure("M3", HOME, "Glazing", AT + timedelta(days=1), True),
        ]
        a = re.effect(HOME, AT, history)
        self.assertEqual(a, re.effect(HOME, AT, list(reversed(history))))
        self.assertEqual(a.loss_multiplier, 0.9 * 0.85)
        self.assertEqual(a.active_measure_ids, ("M1", "M2"))
        later = re.effect(HOME, AT + timedelta(days=1), history)
        self.assertEqual(later.loss_multiplier, 0.9 * 0.85 * 0.95)
        self.assertEqual(later.version, re.VERSION)
        for kind, factor in re.LOSS_MULTIPLIERS.items():
            self.assertEqual(re.effect(HOME, AT, [measure(kind=kind)]).loss_multiplier, factor)

    def test_invalid_or_ambiguous_records_fail_explicitly(self) -> None:
        for identifier, home, kind, at, synthetic in (
            ("", HOME, "Loft insulation", AT, True),
            ("M1", "", "Loft insulation", AT, True),
            ("M1", "padded ", "Loft insulation", AT, True),
            ("M1", HOME, "Unknown measure", AT, True),
            ("M1", HOME, "Loft insulation", AT.replace(tzinfo=None), True),
            ("M1", HOME, "Loft insulation", AT.replace(microsecond=1), True),
            ("M1", HOME, "Loft insulation", AT, False),
            ("M1", HOME, "Loft insulation", AT.astimezone(timezone(timedelta(hours=1))), True),
        ):
            with self.subTest(kind=kind, at=at, synthetic=synthetic), self.assertRaises(ValueError):
                re.Measure(identifier, home, kind, at, synthetic)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            re.effect(HOME, AT, [measure(), measure(home="other")])
        for baseline in (0.0, -1.0, math.nan, math.inf, True):
            with self.subTest(baseline=baseline), self.assertRaises(ValueError):
                re.apply_loss(baseline, HOME, AT, [])
        with self.assertRaises(ValueError):
            re.effect(HOME, AT.replace(tzinfo=None), [])

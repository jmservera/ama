from __future__ import annotations

import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import demo_consent_mix as mix

HOMES = [f"ZF-2025-{n:04d}" for n in range(29, 49)]
NOW = datetime(2026, 11, 21, 0, 37, 12, tzinfo=UTC)


class ConsentMixPlan(unittest.TestCase):
    def test_half_granted_half_declined_and_window_is_slot_aligned(self) -> None:
        policy, controls, cohort = mix.plan(HOMES, NOW)
        consents = [c.consent for c in controls]
        self.assertEqual(10, consents.count("granted"))
        self.assertEqual(10, consents.count("declined"))
        self.assertEqual(HOMES, cohort)
        self.assertEqual("2026-11-20T22:35:00Z", policy.window_start)
        self.assertEqual({policy.window_start}, {c.mapping_start for c in controls})
        self.assertLessEqual(len({c.sensor_id for c in controls}), 20)

    def test_select_cohort_covers_at_least_half_of_all_homes_with_a_consent_mix(self) -> None:
        everything = [f"ZF-2025-{n:04d}" for n in range(1, 342)]
        cohort = mix.select_cohort(everything)
        self.assertGreaterEqual(len(cohort) * 2, len(everything))
        self.assertEqual(len(set(cohort)), len(cohort))
        self.assertEqual(cohort, mix.select_cohort(list(reversed(everything))))
        _, controls, _ = mix.plan(cohort, NOW)
        granted = [c.consent for c in controls].count("granted")
        self.assertLessEqual(abs(granted - (len(cohort) - granted)), 1)
        self.assertEqual(len({c.consent for c in controls[:4]}), 2)

    def test_select_cohort_refuses_an_empty_or_oversized_fleet(self) -> None:
        with self.assertRaises(ValueError):
            mix.select_cohort([])
        with self.assertRaises(ValueError):
            mix.select_cohort([f"ZF-2025-{n:04d}" for n in range(1, 1100)])

    def test_refuses_duplicate_or_empty_cohort(self) -> None:
        with self.assertRaises(ValueError):
            mix.plan([], NOW)
        with self.assertRaises(ValueError):
            mix.plan([HOMES[0], HOMES[0]], NOW)

    def test_control_document_expires_within_fourteen_days(self) -> None:
        doc = mix.control_document("owner", "REF-1", HOMES, NOW)
        self.assertEqual("2026-12-04T00:37:12Z", doc["expires_at"])
        self.assertTrue(doc["enabled"])


if __name__ == "__main__":
    unittest.main()

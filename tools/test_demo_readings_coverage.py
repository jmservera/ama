from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import demo_readings_coverage as cov


def snap(**states: str) -> dict:
    return {"items": [{"id": h, "sensor": {"state": s}} for h, s in states.items()]}


class Coverage(unittest.TestCase):
    def test_merge_prefers_measured_state_and_dedupes(self) -> None:
        r = cov.coverage([snap(a="not-loaded", b="fresh"), snap(a="stale", b="not-loaded")])
        self.assertEqual(2, r["total"])
        self.assertEqual({"fresh": 1, "stale": 1}, r["states"])
        self.assertTrue(r["complete"])

    def test_unmeasured_homes_are_not_assumed_to_have_readings(self) -> None:
        r = cov.coverage([snap(a="fresh", b="not-loaded", c="not-loaded", d="no-readings")])
        self.assertEqual(0.25, r["with_readings_share"])
        self.assertFalse(r["complete"])
        self.assertFalse(cov.meets(r))

    def test_half_threshold_and_recent_share_differ(self) -> None:
        r = cov.coverage([snap(a="fresh", b="offline", c="consent-withheld", d="no-readings")])
        self.assertTrue(cov.meets(r))
        self.assertEqual(0.25, r["recent_share"])

    def test_empty_input_never_meets(self) -> None:
        self.assertFalse(cov.meets(cov.coverage([])))


if __name__ == "__main__":
    unittest.main()

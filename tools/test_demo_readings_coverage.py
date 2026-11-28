from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
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

    def test_stale_only_estate_meets_half_with_no_recent_readings(self) -> None:
        r = cov.coverage([snap(a="stale", b="stale", c="consent-withheld", d="no-readings")])
        self.assertTrue(cov.meets(r))
        self.assertEqual(0.0, r["recent_share"])

    def test_item_without_sensor_key_counts_as_not_loaded(self) -> None:
        r = cov.coverage([{"items": [{"id": "a"}]}])
        self.assertEqual({"not-loaded": 1}, r["states"])
        self.assertFalse(r["complete"])


class Cli(unittest.TestCase):
    def run_main(self, *snaps: dict) -> int:
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            paths = []
            for i, s in enumerate(snaps):
                path = Path(tmp) / f"tile-{i}.json"
                path.write_text(json.dumps(s), encoding="utf-8")
                paths.append(str(path))
            return cov.main(paths)

    def test_no_arguments_returns_usage_code(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(2, cov.main([]))

    def test_exit_code_follows_half_threshold_across_files(self) -> None:
        self.assertEqual(0, self.run_main(snap(a="stale"), snap(b="no-readings", a="not-loaded")))
        self.assertEqual(1, self.run_main(snap(a="stale", b="no-readings", c="no-readings")))


if __name__ == "__main__":
    unittest.main()

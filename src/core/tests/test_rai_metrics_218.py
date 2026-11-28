"""Pure edge cases of the RAI metric reader (issue 218); constructed audit rows only."""

import unittest
from datetime import UTC, datetime
from typing import Any

from zava_forward.core import monitoring_coverage as mc
from zava_forward.core import rai_metrics

START = "2026-11-01T00:00:00+00:00"
END = "2026-11-02T00:00:00+00:00"


def row(event_id: str, kind: str, at: str = "2026-11-01T01:00:00Z", **body: Any) -> dict[str, Any]:
    return {"event_id": event_id, "observed_at": at, "kind": kind, **body}


class ParseWindow(unittest.TestCase):
    def test_accepts_z_suffix_and_offset_bounds(self) -> None:
        window = rai_metrics.parse_window("2026-11-01T00:00:00Z", END)
        assert window is not None
        self.assertEqual(window[0], datetime(2026, 11, 1, tzinfo=UTC))
        self.assertEqual(window[1], datetime(2026, 11, 2, tzinfo=UTC))

    def test_rejects_unusable_bounds(self) -> None:
        for start, end in (
            ("2026-11-01T00:00:00", END),
            (START, "2026-11-02T00:00:00"),
            (None, END),
            (START, 5),
            ("not a date", END),
            (END, START),
            (START, START),
        ):
            with self.subTest(start=start, end=end):
                self.assertIsNone(rai_metrics.parse_window(start, end))


class Classify(unittest.TestCase):
    def test_kinds_map_to_metrics(self) -> None:
        cases: list[tuple[dict[str, Any], tuple[str, ...]]] = [
            ({"kind": "invocation"}, ("invocation",)),
            ({"kind": "direct-call-claimed"}, ("invocation",)),
            ({"kind": "throttled"}, ("refusal",)),
            ({"kind": "result-rejected"}, ("refusal",)),
            ({"kind": "exhausted"}, ("fallback",)),
            ({"kind": "review", "action": "accept"}, ("human_review",)),
            ({"kind": "review", "action": "edit-accept"}, ("human_review", "override")),
            ({"kind": "direct-call-completed"}, ("consumption",)),
            ({"kind": "claimed"}, ()),
            ({}, ()),
        ]
        for event, expected in cases:
            with self.subTest(event=event):
                self.assertEqual(rai_metrics.classify(event), expected)

    def test_completed_outcomes(self) -> None:
        self.assertEqual(
            rai_metrics.classify({"kind": "completed", "state": "quarantined"}),
            ("withheld", "consumption"),
        )
        self.assertEqual(
            rai_metrics.classify({"kind": "completed", "financial_attribution": "x"}),
            ("withheld", "consumption"),
        )
        self.assertEqual(
            rai_metrics.classify({"kind": "completed", "state": "ready"}), ("consumption",)
        )
        returned = {"kind": "completed", "envelope": {"outcome": "returned"}}
        self.assertEqual(rai_metrics.classify(returned), ("validation_failure", "consumption"))
        self.assertEqual(
            rai_metrics.classify({"kind": "completed", "envelope": "bad"}),
            ("fallback", "consumption"),
        )


class Reconstruct(unittest.TestCase):
    def counted(self, persisted: list[dict[str, Any]], **kw: Any) -> dict[str, Any]:
        return rai_metrics.reconstruct(persisted, window_start=START, window_end=END, **kw)

    def test_tokens_only_from_completed_non_negative_ints(self) -> None:
        events = [
            row("a", "completed", state="ready", actual_tokens=10),
            row("b", "completed", state="ready", actual_tokens=-5),
            row("c", "completed", state="ready", actual_tokens=True),
            row("d", "invocation", actual_tokens=99),
        ]
        result = self.counted(events)
        assert result["metrics"] is not None
        self.assertEqual(result["metrics"]["tokens"], 10)
        self.assertEqual(result["status"], mc.COUNTED)

    def test_latency_matches_task_and_fence(self) -> None:
        events = [
            row("c1", "claimed", "2026-11-01T01:00:00Z", task_id="t", fence=1),
            row("c2", "claimed", "2026-11-01T01:00:00Z", task_id="u", fence=1),
            row("d1", "completed", "2026-11-01T01:00:30Z", task_id="t", fence=1, state="ready"),
            row("d2", "completed", "2026-11-01T01:00:30Z", task_id="t", fence=2, state="ready"),
            row("d3", "completed", "2026-11-01T00:59:00Z", task_id="u", fence=1, state="ready"),
            row("d4", "completed", "2026-11-01T01:01:00Z", state="ready"),
        ]
        result = self.counted(events)
        assert result["metrics"] is not None
        self.assertEqual(result["metrics"]["latency_samples"], 1)
        self.assertEqual(result["latency_seconds_total"], 30.0)

    def test_replay_dedupes_and_drops_outside_window(self) -> None:
        persisted = [row("p1", "invocation")]
        replay = [
            row("p1", "invocation"),
            row("n1", "throttled"),
            row("n1", "throttled"),
            row("old", "throttled", "2020-01-01T00:00:00Z"),
        ]
        result = self.counted(persisted, replay=replay)
        assert result["metrics"] is not None
        self.assertEqual(result["metrics"]["invocation"], 1)
        self.assertEqual(result["metrics"]["refusal"], 1)
        self.assertEqual(result["replay"]["duplicates"], 2)
        self.assertEqual(result["replay"]["new"], 1)

    def test_blocked_without_counts(self) -> None:
        bad_window = rai_metrics.reconstruct([], window_start=END, window_end=START)
        self.assertEqual(bad_window["status"], mc.BLOCKED)
        self.assertIsNone(bad_window["metrics"])
        bad_id = self.counted([], replay=[row("has space!", "throttled")])
        self.assertEqual(bad_id["status"], mc.BLOCKED)
        self.assertIsNone(bad_id["metrics"])
        self.assertIsNone(bad_id["latency_seconds_total"])

    def test_empty_window_is_insufficient(self) -> None:
        result = self.counted([])
        self.assertEqual(result["status"], mc.INSUFFICIENT)
        assert result["metrics"] is not None
        self.assertEqual(result["metrics"]["invocation"], 0)


if __name__ == "__main__":
    unittest.main()

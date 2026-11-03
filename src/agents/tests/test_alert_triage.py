"""Synthetic unit fixtures for alert triage scoring; they are not staff evidence."""

from __future__ import annotations

import unittest
from typing import Any

from zava_forward.agents.alert_triage import evaluate_alert_triage

THRESHOLDS: dict[str, Any] = dict(
    owner="Named Owner",
    agreed_on="2026-11-03",
    min_alerts=2,
    min_precision=0.5,
    max_median_ack_seconds=3600,
)


def alert(i: int, cls: str | None, ack_after: int | None) -> dict[str, Any]:
    return dict(
        alert_id=f"a{i}",
        reviewer="Staff A",
        published_at="2026-11-03T09:00:00+00:00",
        classification=cls,
        acknowledged_at=None
        if ack_after is None
        else f"2026-11-03T{9 + ack_after // 3600:02d}:00:00+00:00",
    )


class AlertTriageTests(unittest.TestCase):
    def test_no_observations_are_not_evaluated(self) -> None:
        report = evaluate_alert_triage([])
        self.assertEqual([c["status"] for c in report["checks"]], ["not_evaluated"] * 2)
        self.assertIsNone(report["overall_pass"])
        self.assertEqual(report["threshold"]["status"], "unset_pending_owner_agreement")

    def test_measures_each_check_separately_without_thresholds(self) -> None:
        rows = [alert(1, "true_positive", 1800 * 2), alert(2, "false_positive", 3600 * 2)]
        report = evaluate_alert_triage(rows)
        precision, ack = report["checks"]
        self.assertEqual(precision["precision"], 0.5)
        self.assertEqual(ack["median_seconds"], 5400.0)
        self.assertIn("no owner-agreed thresholds recorded", precision["reasons"])
        self.assertIn("no owner-agreed thresholds recorded", ack["reasons"])

    def test_agreed_thresholds_flag_each_check(self) -> None:
        rows = [alert(1, "false_positive", 7200), alert(2, "false_positive", 7200)]
        report = evaluate_alert_triage(rows, thresholds=THRESHOLDS)
        precision, ack = report["checks"]
        self.assertEqual(report["threshold"]["status"], "owner_agreed")
        self.assertIn("precision below agreed threshold", precision["reasons"])
        self.assertIn("median acknowledgement time above agreed maximum", ack["reasons"])

    def test_meeting_thresholds_has_no_reasons_and_no_overall_pass(self) -> None:
        rows = [alert(1, "true_positive", 0), alert(2, "true_positive", 0)]
        report = evaluate_alert_triage(rows, thresholds=THRESHOLDS)
        self.assertEqual([c["reasons"] for c in report["checks"]], [[], []])
        self.assertIsNone(report["overall_pass"])

    def test_unacknowledged_and_unclassified_are_counted_not_dropped(self) -> None:
        report = evaluate_alert_triage([alert(1, None, None), alert(2, "true_positive", None)])
        precision, ack = report["checks"]
        self.assertEqual(precision["unclassified"], 1)
        self.assertEqual(ack["unacknowledged"], 2)
        self.assertEqual(ack["status"], "not_evaluated")

    def test_invalid_records_are_excluded_and_block(self) -> None:
        bad = alert(3, "maybe", None)
        early = alert(4, None, 0)
        early["acknowledged_at"] = "2026-11-03T08:00:00+00:00"
        naive = alert(5, None, None)
        naive["published_at"] = "2026-11-03T09:00:00"
        report = evaluate_alert_triage([bad, early, naive, alert(1, "true_positive", 0)])
        self.assertEqual(len(report["invalid_observations"]), 3)
        self.assertTrue(any("invalid alert records" in r for r in report["checks"][0]["reasons"]))

    def test_bad_thresholds_are_gaps(self) -> None:
        bad = dict(THRESHOLDS, min_precision=-1, owner=" ", agreed_on="soon")
        report = evaluate_alert_triage([], thresholds=bad)
        gaps = report["threshold"]["gaps"]
        self.assertIn("owner not a named person", gaps)
        self.assertIn("agreed_on not an ISO date", gaps)
        self.assertIn("min_precision not a non-negative number", gaps)


if __name__ == "__main__":
    unittest.main()

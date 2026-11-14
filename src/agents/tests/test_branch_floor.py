"""Synthetic branch-floor fixtures for agent error and validation paths (issue #165)."""

from __future__ import annotations

import signal
import tempfile
import threading
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.agents.alert_triage import (
    _moment,
    _threshold_gaps,
    evaluate_alert_triage,
    valid_alert,
)
from zava_forward.agents.gate_agreement import agreement_gaps
from zava_forward.agents.runtime import beat
from zava_forward.agents.worker import install_signal_handlers

SHA = "c" * 64
GOOD_ALERT: dict[str, Any] = dict(
    alert_id="a1",
    reviewer="Staff A",
    published_at="2026-11-03T09:00:00+00:00",
    classification="true_positive",
    acknowledged_at="2026-11-03T10:00:00+00:00",
)
GOOD_THRESHOLDS: dict[str, Any] = dict(
    owner="Named Owner",
    agreed_on="2026-11-03",
    min_alerts=3,
    min_precision=0.5,
    max_median_ack_seconds=60,
)


class AlertTriageBranchTests(unittest.TestCase):
    def test_moment_rejects_non_text_naive_and_malformed(self) -> None:
        self.assertIsNone(_moment(12))
        self.assertIsNone(_moment("not-a-time"))
        self.assertIsNone(_moment("2026-11-03T09:00:00"))
        self.assertIsNotNone(_moment("2026-11-03T09:00:00+00:00"))

    def test_valid_alert_names_each_rejection(self) -> None:
        self.assertIsNone(valid_alert(GOOD_ALERT))
        self.assertEqual(valid_alert({**GOOD_ALERT, "alert_id": "  "}), "alert_id missing")
        self.assertIn("published_at", valid_alert({**GOOD_ALERT, "published_at": "x"}) or "")
        self.assertIn(
            "classification", valid_alert({**GOOD_ALERT, "classification": "maybe"}) or ""
        )
        self.assertEqual(
            valid_alert({**GOOD_ALERT, "acknowledged_at": "2026-11-03T10:00:00"}),
            "acknowledged_at not a timezone-aware ISO time",
        )
        self.assertEqual(
            valid_alert({**GOOD_ALERT, "acknowledged_at": "2026-11-03T08:00:00+00:00"}),
            "acknowledged_at before published_at",
        )

    def test_threshold_gaps_name_malformed_values(self) -> None:
        gaps = _threshold_gaps(
            {**GOOD_THRESHOLDS, "owner": " ", "agreed_on": "soon", "min_alerts": -1}
        )
        self.assertIn("owner not a named person", gaps)
        self.assertIn("agreed_on not an ISO date", gaps)
        self.assertIn("min_alerts not a non-negative number", gaps)
        self.assertEqual(_threshold_gaps(None), ["no owner-agreed thresholds recorded"])
        missing = _threshold_gaps({"owner": "Named Owner"})
        self.assertIn("agreed_on missing", missing)

    def test_small_samples_and_slow_acknowledgement_are_not_met(self) -> None:
        report = evaluate_alert_triage([GOOD_ALERT], thresholds=GOOD_THRESHOLDS)
        reasons = [reason for check in report["checks"] for reason in check["reasons"]]
        self.assertIn("fewer classified alerts than the agreed minimum", reasons)
        self.assertIn("fewer acknowledged alerts than the agreed minimum", reasons)
        self.assertIsNot(report["overall_pass"], True)

    def test_invalid_records_are_excluded_and_reported(self) -> None:
        rows = [GOOD_ALERT, {**GOOD_ALERT, "alert_id": ""}]
        report = evaluate_alert_triage(rows, thresholds=GOOD_THRESHOLDS)
        for check in report["checks"]:
            self.assertIn(
                "invalid alert records excluded; observations must be repaired", check["reasons"]
            )


class GateAgreementBranchTests(unittest.TestCase):
    def test_every_malformed_field_is_a_named_gap(self) -> None:
        gaps = agreement_gaps(
            dict(
                owner=None,
                independent_grader=3,
                agreed_on=None,
                case_set_sha256=None,
                min_graded_cases=True,
                min_adversarial_cases=0,
                min_rates="high",
            ),
            SHA,
        )
        self.assertIn("owner not a named person", gaps)
        self.assertIn("independent_grader not a named person", gaps)
        self.assertIn("case_set_sha256 missing", gaps)
        self.assertIn("min_graded_cases not a positive whole number", gaps)
        self.assertIn("min_adversarial_cases not a positive whole number", gaps)
        self.assertTrue(any(gap.startswith("min_rates.") for gap in gaps))

    def test_missing_agreement_is_one_gap(self) -> None:
        self.assertEqual(agreement_gaps({}, SHA), ["no owner threshold agreement recorded"])


class RuntimeWorkerBranchTests(unittest.TestCase):
    def test_beat_swallows_unwritable_heartbeat(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            beat(Path(tmp) / "missing-dir" / "heartbeat", now=1.0)
            written = Path(tmp) / "heartbeat"
            beat(written, now=5.0)
            self.assertEqual(written.read_text(encoding="utf-8"), "5.0")

    def test_signal_handlers_set_the_stop_event(self) -> None:
        stop = threading.Event()
        with patch("zava_forward.agents.worker.signal.signal") as register:
            install_signal_handlers(stop)
        self.assertEqual(
            [call.args[0] for call in register.call_args_list],
            [
                signal.SIGTERM,
                signal.SIGINT,
            ],
        )
        register.call_args_list[0].args[1](signal.SIGTERM, None)
        self.assertTrue(stop.is_set())


if __name__ == "__main__":
    unittest.main()

"""Tiny fictional event clocks and declared scenarios for issue 102."""

import copy
import csv
import io
import json
import unittest
from datetime import UTC, datetime
from typing import Any

from zava_forward.core import progress

Record = dict[str, Any]
AS_OF = "2026-10-10T12:00:00Z"


def disposition(version: int, at: str, old: str, new: str, reopened: bool = False) -> Record:
    return dict(
        version=version,
        at=at,
        from_stage=old,
        to_stage=new,
        reopened=reopened,
        by="PRIVATE-ACTOR",
        source="PRIVATE-REFERENCE",
        reason="PRIVATE-REASON",
    )


def events() -> Record:
    return dict(
        id="SYN-102",
        stage="Completed",
        closed=True,
        days_in_stage=999,
        stage_since="1900-01-01",
        history=[dict(at="2020-01-01", text="PRIVATE narrative says completed")],
        returns=[
            disposition(1, "2026-10-01T12:00:00Z", "Survey booked", "Contact paused"),
            disposition(2, "2026-10-03T12:00:00Z", "Contact paused", "Contacting resident"),
        ],
        handoff_history=[
            dict(
                version=i,
                at=f"2026-10-0{i}T12:00:00Z",
                state=state,
                by="PRIVATE-ACTOR",
                note="PRIVATE-NOTE",
                source="PRIVATE-SOURCE",
                from_code="SYN-FROM",
                to_code="SYN-TO",
                offered_at="2026-10-01T12:00:00Z",
            )
            for i, state in enumerate(["Offered", "Received", "Accepted", "Completed"], 1)
        ],
    )


class ProgressReports(unittest.TestCase):
    def history(self, case: Record, start: str | None = None) -> Record:
        return progress.history(
            case,
            progress.timestamp(AS_OF, "As-of"),
            progress.timestamp(start, "Start") if start else None,
        )

    def test_exact_observed_pause_and_handoff_clocks_not_snapshot_or_receipt(self) -> None:
        result = self.history(events())
        self.assertEqual(result["stage_intervals"][0]["elapsed_seconds"], 172800)
        self.assertEqual(result["stage_intervals"][0]["classification"], "Paused stage")
        self.assertIsNone(result["stage_intervals"][1]["elapsed_seconds"])
        self.assertEqual(result["handoff_waits"][0]["elapsed_seconds"], 172800)
        self.assertEqual(result["handoff_waits"][0]["outcome"], "Accepted")
        self.assertEqual(len(result["handoff_waits"]), 1)
        self.assertNotIn("PRIVATE", json.dumps(result))
        self.assertEqual(result["coverage"], "Partial")

    def test_period_clips_boundary_but_keeps_event_source(self) -> None:
        result = self.history(events(), "2026-10-02T12:00:00+00:00")
        self.assertEqual(result["stage_intervals"][0]["elapsed_seconds"], 86400)
        self.assertEqual(result["stage_intervals"][0]["source"], "returns/0")
        self.assertEqual(result["handoff_waits"][0]["elapsed_seconds"], 86400)
        self.assertTrue(all(e["at"] >= "2026-10-02" for e in result["events"]))

    def test_as_of_excludes_future_events_without_inventing_exit(self) -> None:
        result = progress.history(events(), progress.timestamp("2026-10-02T12:00Z", "As-of"), None)
        self.assertEqual(len(result["events"]), 3)
        self.assertIsNone(result["stage_intervals"][0]["elapsed_seconds"])
        self.assertEqual(result["handoff_waits"][0]["outcome"], "Pending")
        self.assertEqual(result["handoff_waits"][0]["elapsed_seconds"], 86400)
        self.assertTrue(result["handoff_waits"][0]["censored"])

    def test_legacy_malformed_unknown_not_zero(self) -> None:
        bad: Any
        for bad in (None, {}, "bad", 1):
            case = events()
            case["returns"] = bad
            with self.subTest(bad=bad):
                result = self.history(case)
                self.assertEqual(result["stage_intervals"], [])
                self.assertIn("malformed_history", [e["code"] for e in result["exceptions"]])
        for bad in ({}, None, "bad"):
            case = events()
            case["returns"][0] = bad
            result = self.history(case)
            self.assertTrue(result["exceptions"])
            self.assertTrue(all(i["elapsed_seconds"] is None for i in result["stage_intervals"]))
        for at in (
            "2026-10-01",
            "2026-10-01T12:00:00",
            "not a timestamp",
            None,
            "0001-01-01T00:00:00+01:00",
            "9999-12-31T23:59:59-01:00",
        ):
            case = events()
            case["returns"][0]["at"] = at
            self.assertTrue(
                all(i["elapsed_seconds"] is None for i in self.history(case)["stage_intervals"])
            )

    def test_contradictory_versions_stage_order_equal_time_and_unknown_kind(self) -> None:
        variants = [
            ("version", 0),
            ("version", True),
            ("version", 2),
            ("version", []),
            ("version", {}),
            ("at", "2026-10-03T12:00:00Z"),
            ("at", "2026-10-04T12:00:00Z"),
            ("from_stage", "PRIVATE unsupported stage"),
            ("reopened", "false"),
            ("to_stage", "Works under way"),
        ]
        for key, value in variants:
            case = events()
            case["returns"][0][key] = value
            with self.subTest(key=key, value=value):
                result = self.history(case)
                self.assertTrue(result["exceptions"])
                self.assertTrue(
                    all(i["elapsed_seconds"] is None for i in result["stage_intervals"])
                )
                self.assertNotIn("PRIVATE", json.dumps(result))
        case = events()
        case["returns"][1]["from_stage"] = "Survey booked"
        self.assertIsNone(self.history(case)["stage_intervals"][0]["elapsed_seconds"])

    def test_repeated_reopen_events_preserved_not_completion(self) -> None:
        case = dict(
            id="SYN-REOPEN",
            returns=[
                disposition(1, "2026-10-01T12:00Z", "Completed", "Aftercare issue", True),
                disposition(2, "2026-10-02T12:00Z", "Completed", "Aftercare issue", True),
            ],
        )
        result = self.history(case)
        self.assertEqual([e["kind"] for e in result["events"]], ["reopen", "reopen"])
        self.assertTrue(all(i["elapsed_seconds"] is None for i in result["stage_intervals"]))
        self.assertIn("contradictory_stage_chain", [e["code"] for e in result["exceptions"]])

    def test_unmappable_handoff_and_missing_offer(self) -> None:
        for bad in ("received", "PRIVATE state", None):
            case = events()
            case["handoff_history"][0]["state"] = bad
            result = self.history(case)
            self.assertIsNone(result["handoff_waits"][0]["elapsed_seconds"])
            self.assertNotIn("PRIVATE", json.dumps(result))
        case = dict(
            id="SYN-NO-OFFER",
            handoff_history=[dict(version=1, at="2026-10-01T12:00Z", state="Accepted")],
        )
        self.assertIsNone(self.history(case)["handoff_waits"][0]["elapsed_seconds"])

    def test_handoff_participant_conflict_is_unknown_not_a_transfer(self) -> None:
        for change in (None, "DIFFERENT-PRIVATE-RECIPIENT"):
            case = events()
            case["handoff_history"][2]["to_code"] = change
            result = self.history(case)
            self.assertIsNone(result["handoff_waits"][0]["elapsed_seconds"])
            self.assertNotIn("PRIVATE", json.dumps(result))

    def test_missing_provenance_and_no_events_surface_exceptions(self) -> None:
        case: Record = dict(
            id="SYN-EMPTY",
            stage="Completed",
            closed=True,
            stage_since="1900-01-01",
            days_in_stage=999,
            history=["completed"],
        )
        result = self.history(case)
        self.assertEqual(result["coverage"], "Unknown")
        self.assertEqual(result["events"], [])
        self.assertEqual(result["exceptions"][0]["code"], "unknown_stage_history")
        case = events()
        case["returns"][0].pop("source")
        case["returns"][0].pop("by")
        codes = [e["code"] for e in self.history(case)["exceptions"]]
        self.assertIn("unknown_source_reference", codes)
        self.assertIn("unknown_event_actor", codes)

    def test_forecast_exact_exa009_sensitivities_and_no_mutation(self) -> None:
        scenario: Record = dict(ready=12)
        result = progress.forecast(16, scenario)
        self.assertEqual(scenario, dict(ready=12))
        self.assertEqual(
            [p["cumulative_handover_scenario"] for p in result["projections"]],
            [[0, 2, 4, 6], [0, 1, 2, 3], [0, 3, 6, 9], [0, 0, 0, 2]],
        )
        self.assertEqual(progress.forecast(16, scenario), result)
        self.assertEqual(result["label"], "Forecast")
        self.assertEqual(result["assumptions"]["held"], 4)
        self.assertIn("not a statistical", result["uncertainty"])
        self.assertTrue(result["data_limits"])
        self.assertEqual(progress.forecast(16, None)["status"], "Unavailable")
        for scenario in (
            {"ready": 17},
            {"ready": -1},
            {"ready": True},
            {"capacity": 2},
            {"ready": 1, "capacity": 0},
            {"ready": 1, "weeks": 100},
            {"ready": 1, "surprise": 1},
        ):
            with self.subTest(scenario=scenario), self.assertRaises(ValueError):
                progress.forecast(16, scenario)

    def test_csv_exact_roundtrip_determinism_and_audit_failure(self) -> None:
        case = events()
        before = copy.deepcopy(case)
        result = progress.report(
            [case],
            as_of=AS_OF,
            start=None,
            cohort={"case_ids": ["SYN-102"]},
            scenario={"ready": 1},
            audit_intact=True,
        )
        self.assertEqual(before, case)
        text = progress.export_csv(result)
        rebuilt = {
            row["section"]: json.loads(row["value"]) for row in csv.DictReader(io.StringIO(text))
        }
        self.assertEqual(rebuilt, result)
        self.assertEqual(progress.export_csv(result), text)
        self.assertNotIn("PRIVATE", text)
        self.assertEqual(result["denominators"]["selected_cases"], 1)
        self.assertIsNone(result["denominators"]["accepted_handover_actuals"])
        failed = progress.report(
            [case], as_of=AS_OF, start=None, cohort={}, scenario=None, audit_intact=False
        )
        self.assertEqual(failed["histories"][0]["coverage"], "Untrusted")
        self.assertTrue(
            all(i["elapsed_seconds"] is None for i in failed["histories"][0]["stage_intervals"])
        )
        empty = progress.report(
            [], as_of=AS_OF, start=None, cohort={}, scenario=None, audit_intact=True
        )
        self.assertEqual(empty["exceptions"][0]["code"], "empty_authorized_cohort")

    def test_timestamp_validation_and_normalization(self) -> None:
        for value in ("0001-01-01T00:00:00+01:00", "9999-12-31T23:59:59-01:00"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                progress.timestamp(value, "Event time")
        self.assertEqual(
            progress.timestamp("2026-10-10T13:00:00+01:00", "Time"),
            datetime(2026, 10, 10, 12, tzinfo=UTC),
        )
        for as_of, start in (
            (None, None),
            ("2026-10-01", None),
            ("2099-01-01T12:00Z", None),
            (AS_OF, "2026-10-11T12:00Z"),
        ):
            with self.subTest(as_of=as_of, start=start), self.assertRaises(ValueError):
                progress.report(
                    [], as_of=as_of, start=start, cohort={}, scenario=None, audit_intact=True
                )

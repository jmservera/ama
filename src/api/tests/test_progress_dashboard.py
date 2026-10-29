"""Synthetic-only progress semantics and closed archive HTTP boundaries."""

from __future__ import annotations

import copy
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.parse import urlencode

from building_fixture import fixture, hold
from dataset import DATA
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

from zava_forward.api import progress
from zava_forward.api.server import App, make_handler


def event(when: str, action: str) -> dict[str, Any]:
    return dict(at=when, action=action, source="year-one simulation", is_synthetic=True)


def synthetic_data() -> dict[str, Any]:
    data: dict[str, Any] = copy.deepcopy(DATA)
    data["as_of"] = "2026-10-07"
    first, active, withdrawn, unknown, unmarked = data["cases"]
    first.update(
        stage="Completed",
        closed=True,
        history=[
            event("2026-09-28", "Identified"),
            event("2026-10-02", "Accepted handover"),
            event("2026-10-05", "Reopened - aftercare"),
            event("2026-10-07", "Accepted handover"),
        ],
    )
    active.update(history=[event("2026-10-01", "Identified")], days_in_stage=70)
    active["resident_update"] = dict(
        due_at="2026-09-30T12:00:00Z",
        completed_at=None,
        owner="Synthetic role",
    )
    withdrawn.update(
        stage="Withdrawn",
        closed=True,
        owner_role="Quality Inspector",
        history=[event("2026-10-03", "Identified"), event("2026-10-04", "Withdrawn")],
    )
    unknown.update(closed=True, is_synthetic=True, stage="Excluded", history=[])
    unmarked.update(closed=True, stage="Completed", history=[])
    unmarked["resident"]["name"] = "PRIVATE-NOT-SYNTHETIC"
    data["staff"].append(
        dict(
            code="CON-01",
            email="contractor@example.test",
            name="Fictional provider",
            role="Contractor",
            contractor="Test Ltd",
        )
    )
    data["recommendations"] = []
    for index, status in enumerate(("Accepted", "Edited", "Rejected")):
        data["recommendations"].append(
            dict(
                id=f"AI-{index}",
                kind="ai_task",
                is_synthetic=True,
                task="briefing",
                source="ai",
                user="pam@example.test",
                case_ids=["ZF-1"],
                status=status,
                created="2026-09-01",
                resolved_at=f"2026-10-0{index + 2}T12:00:00Z",
                text="PRIVATE-OUTPUT",
                reviewer_reason="PRIVATE-REASON",
            )
        )
    base = data["recommendations"][0]
    for identifier, extra in (
        ("REAL", dict(is_synthetic=False)),
        ("MIXED", dict(case_ids=["ZF-1", "ZF-5"])),
        ("NO-LINK", dict(case_ids=[])),
        ("UNKNOWN-DATE", dict(resolved_at=None)),
        ("NOT-REVIEWED", dict(status="Not reviewed", resolved_at=None)),
        ("TEMPLATE", dict(source="template")),
    ):
        data["recommendations"].append(dict(base, id=identifier, **extra))
    return data


class ProgressDashboard(unittest.TestCase):
    backend = "json"
    store: Any

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = synthetic_data()
        self.path.write_text(json.dumps(data))
        if self.backend == "sqlite":
            self.store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
            self.addCleanup(self.store.db.close)
            with self.store.lock:
                self.store.data["recommendations"] = copy.deepcopy(data["recommendations"])
                self.store.save()
        else:
            self.store = Store(str(self.path))
        self.sam, self.pam = data["staff"][:2]

    def report(self, **values: str) -> dict[str, Any]:
        return progress.dashboard(self.store, self.pam, {k: [v] for k, v in values.items()})

    def archive(self, **values: str) -> dict[str, Any]:
        return progress.closed_cases(self.store, self.pam, {k: [v] for k, v in values.items()})

    def test_exact_daily_weekly_backlog_and_episode_percentiles(self) -> None:
        report = self.report(start="2026-09-28", end="2026-10-07")
        self.assertEqual(
            report["coverage"],
            dict(
                synthetic_cases=4,
                excluded_unmarked=1,
                known_lifecycle=3,
                unknown_lifecycle=1,
            ),
        )
        self.assertEqual(
            [(r["opened"], r["closed"], r["reopened"], r["backlog"]) for r in report["daily"]],
            [
                (1, 0, 0, 1),
                (0, 0, 0, 1),
                (0, 0, 0, 1),
                (1, 0, 0, 2),
                (0, 1, 0, 1),
                (1, 0, 0, 2),
                (0, 1, 0, 1),
                (1, 0, 1, 2),
                (0, 0, 0, 2),
                (0, 1, 0, 1),
            ],
        )
        self.assertEqual(
            report["weekly"],
            [
                dict(date="2026-09-28", opened=3, closed=2, reopened=0, backlog=1),
                dict(date="2026-10-05", opened=1, closed=1, reopened=1, backlog=1),
            ],
        )
        self.assertEqual(report["time_to_close"], dict(median_days=2, p90_days=4, samples=3))
        self.assertEqual(report["current"]["open"], 1)
        self.assertEqual(report["current"]["stalled"], 1)
        self.assertEqual(report["current"]["overdue"], 1)
        self.assertEqual(sum(r["count"] for r in report["current"]["journey"]), 1)
        self.assertEqual(
            report["current"]["teams"],
            [
                dict(label="Resident Liaison Officer", count=1),
            ],
        )

    def test_partial_weeks_initial_backlog_and_zero_sample_are_not_fabricated(self) -> None:
        report = self.report(start="2026-10-06", end="2026-10-06")
        self.assertEqual(
            report["daily"],
            [
                dict(date="2026-10-06", opened=0, closed=0, reopened=0, backlog=2),
            ],
        )
        self.assertEqual(report["weekly"][0]["date"], "2026-10-05")
        self.assertEqual(
            report["time_to_close"],
            dict(
                median_days=None,
                p90_days=None,
                samples=0,
            ),
        )
        self.assertEqual(self.report()["end"], "2026-10-07")
        self.assertEqual(self.report()["start"], "2026-09-08")
        self.assertEqual(
            self.report(start="2026-10-02", end="2026-10-04")["time_to_close"],
            dict(median_days=2.5, p90_days=4, samples=2),
        )

    def test_synthetic_admission_is_case_local_and_fail_closed(self) -> None:
        for value in (None, [], ["narrative"], [dict(is_synthetic=False)]):
            self.assertFalse(progress.synthetic(dict(history=value)))
        self.assertTrue(progress.synthetic(dict(is_synthetic=True)))
        self.assertFalse(
            progress.synthetic(
                dict(
                    is_synthetic=False,
                    history=[event("2026-10-01", "Identified")],
                )
            )
        )
        self.assertFalse(
            progress.synthetic(
                dict(
                    history=[
                        event("2026-10-01", "Identified"),
                        dict(action="real"),
                    ]
                )
            )
        )
        with self.store.lock:
            self.store.cases["ZF-1"]["history"][0]["is_synthetic"] = False
            result = self.report()
        self.assertEqual(result["coverage"]["synthetic_cases"], 3)
        self.assertNotIn("PRIVATE", json.dumps(result))
        with self.store.lock:
            for case in self.store.cases.values():
                case["history"] = []
                case["is_synthetic"] = False
            empty = self.report()
        self.assertEqual(empty["coverage"]["synthetic_cases"], 0)
        self.assertEqual(empty["current"]["open"], 0)
        self.assertTrue(all(row["backlog"] == 0 for row in empty["daily"]))

    def test_controlled_reopen_and_human_closure_no_current_stage_date_inference(self) -> None:
        self.assertIsNone(
            progress.lifecycle(
                dict(
                    closed=False,
                    history=[event("2026-10-05", "Reopened - aftercare")],
                )
            )
        )
        with self.store.lock:
            case = self.store.cases["ZF-1"]
            case["history"] = [event("2026-09-28", "Identified")]
            case["home_case_closures"] = [
                dict(at="2026-10-02", closed=True, event_type="human_home_case_closed"),
                dict(at="2026-10-07", closed=True, event_type="human_home_case_closed"),
            ]
            case["returns"] = [
                dict(at="2026-10-05", reopened=True, event_type="reopen"),
                dict(at="2026-10-06", reopened=False, event_type="return"),
            ]
            self.assertEqual(
                progress.lifecycle(case),
                [
                    (progress.day("2026-09-28"), True),
                    (progress.day("2026-10-02"), False),
                    (progress.day("2026-10-05"), True),
                    (progress.day("2026-10-07"), False),
                ],
            )
            case["stage_since"] = "1900-01-01"
            self.assertEqual(
                self.archive(start="2026-10-07")["items"][0]["closed_on"], "2026-10-07"
            )
            case["home_case_closures"][-1]["at"] = "invalid"
            self.assertIsNone(progress.lifecycle(case))
            self.assertIsNone(self.archive(q="ZF-1")["items"][0]["closed_on"])

    def test_non_list_history_is_unknown_without_failing_either_read(self) -> None:
        baseline = self.report()
        for history in (None, "not a history", {"action": "Identified"}, 42, False):
            with self.subTest(history=history), self.store.lock:
                case = self.store.cases["ZF-4"]
                case.update(is_synthetic=True, history=history)
                self.assertTrue(progress.synthetic(case))
                self.assertIsNone(progress.lifecycle(case))
                self.assertEqual(self.report(), baseline)
                archive = self.archive()
                self.assertEqual(archive["unknown_closure_dates"], 1)
                self.assertEqual(archive["total"], 3)
                self.assertIsNone(self.archive(q="ZF-4")["items"][0]["closed_on"])
                self.assertEqual(self.archive(q="ZF-4", start="2026-10-01")["total"], 0)
                self.assertEqual(self.archive(q="ZF-4", end="2026-10-07")["total"], 0)

    def test_range_validation_preserves_inclusive_limit_and_archive_semantics(self) -> None:
        self.assertEqual(len(self.report(start="2025-10-07", end="2026-10-07")["daily"]), 366)
        for values in (
            dict(start="2025-10-06", end="2026-10-07"),
            dict(start="2026-10-08", end="2026-10-07"),
            dict(start="2026-10-08"),
        ):
            with self.subTest(values=values), self.assertRaises(progress.DateRangeError):
                self.report(**values)
        with self.assertRaises(progress.DateRangeError):
            self.archive(start="2026-10-08", end="2026-10-07")
        self.assertEqual(self.archive(start="2020-01-01", end="2026-10-07")["total"], 2)

    def test_malformed_auxiliary_lifecycles_persist_as_unknown_without_aborting_reads(self) -> None:
        malformed: list[object] = [
            None,
            "not a collection",
            {"at": "2026-10-07"},
            42,
            False,
            [None],
            ["not an event"],
            [{}, None],
            [dict(at="2026-10-07", closed=True, reopened=True), None],
        ]
        originals = {cid: copy.deepcopy(self.store.cases[cid]) for cid in ("ZF-1", "ZF-2")}
        for field in ("home_case_closures", "returns"):
            for value in malformed:
                with self.subTest(field=field, value=value):
                    with self.store.lock:
                        for cid, original in originals.items():
                            case = self.store.cases[cid]
                            case.clear()
                            case.update(copy.deepcopy(original))
                            case[field] = value
                            self.assertIsNone(progress.lifecycle(case))
                            if self.backend == "sqlite":
                                self.store.db.execute(
                                    "UPDATE cases SET body = ? WHERE id = ?",
                                    (json.dumps(case), cid),
                                )
                        if self.backend == "json":
                            self.store.save()
                    reader: Any = (
                        SqlStore(str(self.path), self.store.db_path)
                        if self.backend == "sqlite"
                        else Store(str(self.path))
                    )
                    try:
                        report = progress.dashboard(reader, self.pam, {})
                        self.assertEqual(report["coverage"]["synthetic_cases"], 4)
                        self.assertEqual(report["coverage"]["known_lifecycle"], 1)
                        self.assertEqual(report["coverage"]["unknown_lifecycle"], 3)
                        self.assertEqual(report["current"]["overdue"], 1)
                        archive = progress.closed_cases(reader, self.pam, {})
                        self.assertEqual(archive["total"], 3)
                        self.assertEqual(archive["unknown_closure_dates"], 2)
                        dates = {row["id"]: row["closed_on"] for row in archive["items"]}
                        self.assertIsNone(dates["ZF-1"])
                        self.assertEqual(dates["ZF-3"], "2026-10-04")
                        for bound in ("start", "end"):
                            filtered = progress.closed_cases(
                                reader, self.pam, {"q": ["ZF-1"], bound: ["2026-10-07"]}
                            )
                            self.assertEqual(filtered["total"], 0)
                    finally:
                        if self.backend == "sqlite":
                            reader.db.close()

    def test_absent_empty_and_dictionary_auxiliary_evidence_preserves_valid_replay(self) -> None:
        case = copy.deepcopy(self.store.cases["ZF-1"])
        expected = progress.lifecycle(case)
        self.assertIsNotNone(expected)
        for field in ("home_case_closures", "returns"):
            case.pop(field, None)
            self.assertEqual(progress.lifecycle(case), expected)
            valid: list[list[dict[str, Any]]] = [
                [],
                [{}],
                [dict(event_type="not a transition", at=None)],
            ]
            for value in valid:
                with self.subTest(field=field, value=value):
                    case[field] = value
                    self.assertEqual(progress.lifecycle(case), expected)

    def test_overdue_matches_previous_context_without_building_or_context_evaluation(self) -> None:
        shared = fixture()
        with self.store.lock:
            self.store.data["buildings"] = shared["buildings"]
            self.store.data["procurement"] = shared["procurement"]
            self.store.data["buildings"][0]["holds"] = [hold()]
            for index, case in enumerate(self.store.cases.values()):
                case.update(building_id="SYN-B1", is_synthetic=True, closed=False)
                case["resident_update"] = dict(
                    due_at="2026-10-06T12:00:00Z",
                    completed_at="2026-10-07T00:00:00Z" if index == 0 else None,
                )
                case["hazards"] = [
                    dict(
                        released=True,
                        response_due_at="2026-10-06T12:00:00Z",
                        responded_at="2026-10-07T00:00:01Z" if index == 2 else "2026-10-06",
                    )
                ]
                case["handoff"] = dict(
                    state="Offered" if index == 0 else "Accepted",
                    from_name="Synthetic sender",
                    due_at="2026-10-06T12:00:00Z",
                )
            self.store.cases["ZF-4"]["closed"] = True
            self.store.cases["ZF-5"]["is_synthetic"] = False
            current = [
                case
                for case in self.store.cases.values()
                if progress.synthetic(case) and not case.get("closed")
            ]
            self.assertTrue(
                any(
                    row["step"] == "Shared building review"
                    for row in self.store.work_context(current[1], self.pam)["blockers"]
                ),
            )
            expected = sum(bool(self.store.work_context(c, self.pam)["overdue"]) for c in current)
            self.assertEqual(expected, 3)
            with (
                patch.object(
                    self.store, "work_context", side_effect=AssertionError("full context called")
                ),
                patch(
                    "zava_forward.core.buildings.record",
                    side_effect=AssertionError("building membership scan called"),
                ),
            ):
                self.assertEqual(self.report()["current"]["overdue"], expected)

    def test_ai_review_date_cohort_provenance_and_no_private_fields(self) -> None:
        ai = self.report(start="2026-10-02", end="2026-10-03")["ai"]
        self.assertEqual([r["count"] for r in ai["outcomes"]], [1, 1, 0])
        self.assertEqual(ai["eligible_records"], 6)
        self.assertEqual(ai["unknown_review_date"], 1)
        self.assertEqual(ai["rules_or_templates"], 1)
        self.assertEqual(ai["unreviewed_or_unavailable"], 1)
        self.assertNotIn("PRIVATE", json.dumps(ai))
        self.assertNotIn("pam@", json.dumps(ai))
        self.assertEqual(
            [
                r["count"]
                for r in self.report(start="2026-10-04", end="2026-10-04")["ai"]["outcomes"]
            ],
            [0, 0, 1],
        )

    def test_archive_latest_closure_unknown_dates_and_combined_filters(self) -> None:
        self.assertEqual([r["id"] for r in self.archive()["items"]], ["ZF-1", "ZF-3", "ZF-4"])
        self.assertEqual(self.archive()["unknown_closure_dates"], 1)
        self.assertEqual(self.archive(start="2026-10-02", end="2026-10-02")["total"], 0)
        self.assertEqual(self.archive(start="2026-10-07", end="2026-10-07")["total"], 1)
        result = self.archive(
            status="Withdrawn",
            team="Quality Inspector",
            q="pat TEST",
            start="2026-10-04",
            end="2026-10-04",
        )
        self.assertEqual([r["id"] for r in result["items"]], ["ZF-3"])
        self.assertEqual(self.archive(q="private")["total"], 0)
        self.assertIn("Excluded", self.archive()["facets"]["statuses"])
        self.assertTrue(self.archive(q="ZF-4")["items"][0]["hazard"])
        with self.store.lock:
            self.store.cases["ZF-4"].pop("stage")
            self.assertEqual(self.archive(status="Unknown")["items"][0]["id"], "ZF-4")

    def test_paging_zero_one_exact_full_last_and_beyond_boundaries(self) -> None:
        with self.store.lock:
            template = copy.deepcopy(self.store.cases["ZF-1"])
            self.store.cases.clear()
            for count in (0, 1, 20, 21, 40, 41):
                self.store.cases.clear()
                for index in reversed(range(count)):
                    case = copy.deepcopy(template)
                    case["id"] = f"SYN-{index:03}"
                    self.store.cases[case["id"]] = case
                first = self.archive()
                self.assertEqual(first["total"], count)
                self.assertEqual(len(first["items"]), min(count, 20))
                self.assertEqual(first["items"], sorted(first["items"], key=lambda r: r["id"]))
                last = self.archive(page="999999")
                pages = max(1, (count + 19) // 20)
                self.assertEqual(last["page"], pages)
                self.assertEqual(len(last["items"]), max(0, count - (pages - 1) * 20))
                self.assertEqual(self.archive(q="no match", page="2")["page"], 1)

    def test_invalid_queries_and_roles_are_explicit(self) -> None:
        for values in (
            {"start": ["2026-02-30"]},
            {"start": ["2026-10-08"], "end": ["2026-10-07"]},
            {"start": ["2025-01-01"], "end": ["2026-10-07"]},
            {"unknown": ["x"]},
            {"start": ["2026-01-01", "2026-02-01"]},
            {"end": ["0001-01-01"]},
        ):
            with self.subTest(values=values), self.assertRaises(ValueError):
                progress.dashboard(self.store, self.pam, values)
        for values in (
            {"page": ["0"]},
            {"page": ["-1"]},
            {"page": ["x"]},
            {"page": [""]},
            {"limit": ["101"]},
            {"limit": ["0"]},
            {"q": ["x" * 201]},
            {"page": ["1", "2"]},
            {"q": ["x"], "secret": ["y"]},
        ):
            with self.subTest(values=values), self.assertRaises(ValueError):
                progress.closed_cases(self.store, self.pam, values)
        for role in ("Contractor", "Unknown", "Application Administrator"):
            for read in (progress.dashboard, progress.closed_cases):
                with self.assertRaises(PermissionError):
                    read(self.store, {"role": role}, {})
        with self.assertRaises(PermissionError):
            progress.closed_cases(self.store, self.sam, {})

    def test_reads_do_not_mutate_cases_or_audit(self) -> None:
        with self.store.lock:
            before = copy.deepcopy(self.store.cases)
            audit = list(self.store.audit_entries())
            self.report()
            self.archive()
            self.assertEqual(self.store.cases, before)
            self.assertEqual(list(self.store.audit_entries()), audit)

    def test_http_endpoint_permissions_validation_and_values(self) -> None:
        app = App(self.store, "synthetic-check")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, 5)
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        base = f"http://127.0.0.1:{httpd.server_address[1]}"

        def request(path: str, cookie: str = "", body: bytes | None = None) -> tuple[int, Any]:
            req = urllib.request.Request(base + path, body, headers={"Cookie": cookie})
            try:
                with urllib.request.urlopen(req) as response:
                    return response.status, (
                        response.headers.get("Set-Cookie") if body else json.load(response)
                    )
            except urllib.error.HTTPError as error:
                return error.code, json.load(error)

        self.assertEqual(request("/api/progress")[0], 401)
        for email, expected in (("pam", 200), ("sam", 403), ("contractor", 403)):
            _, cookie = request(
                "/api/login",
                body=json.dumps(
                    dict(
                        email=f"{email}@example.test",
                        password="synthetic-check",
                    )
                ).encode(),
            )
            cookie = cookie.split(";")[0]
            self.assertEqual(request("/api/closed-cases", cookie)[0], expected)
            code, result = request("/api/progress", cookie)
            self.assertEqual(code, 403 if email == "contractor" else 200)
            if code == 200:
                self.assertEqual(result["label"], "Demonstration data")
                self.assertEqual(request("/api/progress?end=bad", cookie)[0], 400)
                self.assertEqual(request("/api/progress?end=&end=", cookie)[0], 400)
            if expected == 200:
                query = urlencode(dict(status="Withdrawn", team="Quality Inspector", q="ZF-3"))
                self.assertEqual(request("/api/closed-cases?" + query, cookie)[1]["total"], 1)
                self.assertEqual(request("/api/closed-cases?page=0", cookie)[0], 400)
                for path in (
                    "/api/progress?start=2026-10-08&end=2026-10-07",
                    "/api/progress?start=2020-01-01&end=2026-10-07",
                    "/api/progress?start=2026-10-08",
                    "/api/closed-cases?start=2026-10-08&end=2026-10-07",
                ):
                    code, error = request(path, cookie)
                    self.assertEqual(code, 400)
                    self.assertEqual(error["reasons"], dict(fields=["start", "end"]))
                for path in (
                    "/api/progress?unknown=value",
                    "/api/closed-cases?page=0",
                ):
                    code, error = request(path, cookie)
                    self.assertEqual(code, 400)
                    self.assertNotIn("reasons", error)


class SqliteProgressDashboard(ProgressDashboard):
    backend = "sqlite"

    def test_external_writer_refreshes_read_model(self) -> None:
        other = SqlStore("unused", self.store.db_path)
        self.addCleanup(other.db.close)
        with other.lock:
            case = other._case("ZF-2")
            case["days_in_stage"] = 0
            case["stage_since"] = "2026-10-07"
            other.save()
        self.assertEqual(self.report()["current"]["stalled"], 0)

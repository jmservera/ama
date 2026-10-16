"""Synthetic queue boundaries, snapshot semantics and store paging parity."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from building_fixture import fixture, hold, open_store
from dataset import DATA
from test_sqlreads import STAFF, dataset, queue_cases
from zava_forward.core import ranking, taskqueues
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

AS_OF = "2026-10-16"


def evaluate(case: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    args: dict[str, Any] = dict(
        as_of=AS_OF,
        reason_ok=True,
        policy=ranking.CURRENT,
        stock_queries=[],
        building_reasons=[],
        resident_reasons=[],
        technical_missing=[],
        handoff=None,
    )
    args.update(kwargs)
    return taskqueues.context(case, **args)


class QueueDefinitions(unittest.TestCase):
    def setUp(self) -> None:
        self.case = copy.deepcopy(DATA["cases"][0])
        self.case["funding_ok"] = True

    def test_stage_window_and_unknown_observations(self) -> None:
        for date, expected in (
            ("2026-10-16", True),
            ("2026-10-09", True),
            ("2026-10-08", False),
            ("2026-10-17", False),
            ("bad", False),
            (None, False),
        ):
            with self.subTest(date=date):
                self.case["stage_since"] = date
                self.assertEqual("new" in evaluate(self.case)["queues"], expected)

    def test_freshness_exact_boundaries_and_last_supplied_evidence(self) -> None:
        for kind, boundary, before, after in (
            ("EPC", "2026-09-16", "2026-09-17", "2026-09-15"),
            ("Survey", "2026-04-19", "2026-04-20", "2026-04-18"),
        ):
            for date, expected in (
                (boundary, False),
                (before, False),
                (after, True),
                ("2026-10-17", False),
                ("bad", False),
                (None, False),
            ):
                with self.subTest(kind=kind, date=date):
                    self.case["documents"] = [dict(kind=kind, at=date, id="SYN-DOC", version=3)]
                    work = evaluate(self.case)
                    self.assertEqual("stale" in work["queues"], expected)
                    row = next(x for x in work["evidence_freshness"] if x["kind"] == kind)
                    if date in (None, "bad", "2026-10-17"):
                        self.assertEqual(row["status"], "Unknown")
            self.case["documents"] = [
                dict(kind=kind, at=after),
                dict(kind=kind, at=before),
            ]
            self.assertNotIn("stale", evaluate(self.case)["queues"])
        self.case["documents"] = []
        self.case["technical"] = dict(signoffs={"design": {"status": "Needs reassessment"}})
        self.assertIn("stale", evaluate(self.case)["queues"])

    def test_draft_policy_cannot_become_approved_priority_from_accepted_ai_advice(self) -> None:
        self.case["recommendations"] = [dict(status="Accepted")]
        work = evaluate(self.case)
        self.assertNotIn("priority", work["queues"])
        spec = taskqueues.contract(ranking.CURRENT)
        self.assertEqual(spec["version"], taskqueues.VERSION)
        self.assertEqual(len(spec["definitions"]), 6)
        priority = next(x for x in spec["definitions"] if x["id"] == "priority")
        self.assertFalse(priority["available"])
        self.assertIn("not recorded", priority["limitation"])
        self.assertIsNone(spec["selection"])
        self.assertEqual(spec["default"]["queue"], "")

    def test_pending_states_retain_accountability_not_receipt_as_ownership(self) -> None:
        for state in (
            "Offered",
            "Received",
            "Escalated",
            "Accepted",
            "Completed",
            "Declined",
            "Withdrawn",
        ):
            with self.subTest(state=state):
                handoff = dict(
                    state=state,
                    proposed_receiver="Rae",
                    confirmed_receiver=None,
                    chase_owner="Sam",
                    due_at="2026-10-15T23:59:00Z",
                )
                work = evaluate(self.case, handoff=handoff)
                pending = state in taskqueues.PENDING
                self.assertEqual("unowned" in work["queues"], pending)
                self.assertEqual("overdue" in work["queues"], pending)
                self.assertEqual(work["owner"], "Sam Example")
                self.assertEqual(work["handoff"]["confirmed_receiver"], "Unknown")
                self.assertEqual(work["handoff"]["chase_owner"], "Sam")

    def test_deadlines_need_outstanding_work_and_strictly_past_instant(self) -> None:
        for due, expected in (
            ("2026-10-15T23:59:00Z", True),
            ("2026-10-16T00:00:00Z", False),
            ("2026-10-16T00:01:00Z", False),
            (None, False),
            ("bad", False),
            ("2026-10-15T10:00", False),
        ):
            self.case["resident_update"] = dict(owner="Rae", due_at=due)
            self.assertEqual("overdue" in evaluate(self.case)["queues"], expected)
        self.case["resident_update"] = dict(
            owner="Rae", due_at="2026-10-15T10:00Z", completed_at="2026-10-15T11:00Z"
        )
        self.assertNotIn("overdue", evaluate(self.case)["queues"])
        self.case["resident_update"]["completed_at"] = "2026-10-17T11:00Z"
        self.assertIn("overdue", evaluate(self.case)["queues"])

    def test_independent_external_clocks_and_legacy_unknown_awareness(self) -> None:
        hazard = copy.deepcopy(DATA["cases"][3]["hazards"][0])
        hazard.update(
            response_due_at="2026-10-14T10:00Z",
            responded_at="2026-10-14T11:00Z",
            resident_update_due_at="2026-10-15T10:00Z",
        )
        self.case["hazards"] = [hazard]
        work = evaluate(self.case)
        self.assertEqual(work["hazard_clocks"][0]["owner"], "Bea Safe")
        self.assertEqual(work["hazard_clocks"][0]["aware_at"], "Unknown")
        self.assertIsNone(work["hazard_clocks"][0]["elapsed_hours"])
        self.assertEqual(
            [x["task"] for x in work["overdue"]], ["External safety service resident update"]
        )
        hazard.update(aware_at="2026-10-15T12:00Z", resident_updated_at="2026-10-15T11:00Z")
        work = evaluate(self.case)
        self.assertEqual(work["hazard_clocks"][0]["elapsed_hours"], 12)
        self.assertNotIn("overdue", work["queues"])
        hazard.update(released=True, resident_updated_at=None)
        work = evaluate(self.case)
        self.assertEqual(work["hazard_clocks"], [])
        self.assertIn("overdue", work["queues"])

    def test_structured_blockers_never_invent_person_from_role(self) -> None:
        work = evaluate(
            self.case,
            building_reasons=["SYN-BUILDING-BLOCK"],
            technical_missing=[dict(item="Evidence: Design", assigned_to="Technical role")],
        )
        self.assertEqual(work["blockers"][0]["step"], "Shared building review")
        self.assertEqual(work["blockers"][0]["owner"], "Unknown")
        self.assertEqual(work["blockers"][1]["owner"], "Unknown")
        self.assertEqual(work["blockers"][1]["responsible_role"], "Technical role")
        self.assertFalse(work["blockers"][1]["current_stop"])
        self.assertEqual(work["reason"], "SYN-BUILDING-BLOCK")
        self.assertEqual(work["source"], "case:ZF-1/building")

    def test_projection_for_human_context_and_per_case_sources(self) -> None:
        self.case["returns"] = [
            dict(
                to_stage=self.case["stage"],
                reason="SENTINEL-REASON",
                next_action="SENTINEL-ACTION",
                source="SENTINEL-SOURCE",
                version=4,
            )
        ]
        allowed = evaluate(self.case)
        restricted = evaluate(self.case, reason_ok=False)
        self.assertEqual(allowed["reason"], "SENTINEL-REASON")
        self.assertEqual(restricted["reason"], taskqueues.HELD)
        self.assertNotIn("SENTINEL", json.dumps(restricted))
        self.assertEqual(allowed["version"], 4)
        second = copy.deepcopy(self.case)
        second.update(id="ZF-OTHER", returns=[])
        self.assertEqual(evaluate(second)["source"], "case:ZF-OTHER/stage")
        self.assertNotIn("SENTINEL", json.dumps(evaluate(second)))


class StoreQueueParity(unittest.TestCase):
    @patch.dict(ranking.CURRENT, dict(ranking.CURRENT, status="Approved", owner="Synthetic owner"))
    def test_all_queue_filters_sorts_and_visibility_match_uncached_selection(self) -> None:
        data = dataset(queue_cases(90))
        data["as_of"] = AS_OF
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "synthetic.json"
            seed.write_text(json.dumps(data))
            for sql in (False, True):
                store = (
                    SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
                    if sql
                    else Store(str(seed))
                )
                try:
                    for queue, _, _ in taskqueues.DEFINITIONS:
                        for sort in (
                            "urgent",
                            "waiting",
                            "name",
                            "contact",
                            "visit",
                            "bogus",
                            "",
                            None,
                        ):
                            for user, view, filters, query in (
                                (STAFF[1], "all", {}, ""),
                                (STAFF[1], "mine", {}, ""),
                                (STAFF[0], "all", {}, ""),
                                (STAFF[1], "closed", {}, ""),
                                (STAFF[0], "mine", {"area": "North", "flag": "long"}, ""),
                                (STAFF[1], "all", {"wave": "Wave 1", "owner": "PM-01"}, "TE"),
                                (STAFF[1], "all", {"flag": "nodecision"}, ""),
                            ):
                                args = dict(
                                    view=view,
                                    filters=dict(filters, queue=queue),
                                    q=query,
                                    sort=sort,
                                    limit=7,
                                    offset=2,
                                )
                                with self.subTest(sql=sql, queue=queue, args=args):
                                    actual = store.page_cases(user, **args)

                                    def uncached(
                                        name: str, target: Store = store
                                    ) -> list[dict[str, Any]]:
                                        return [
                                            c
                                            for c in target.cases.values()
                                            if name in target.work_context(c, None)["queues"]
                                        ]

                                    with patch.object(store, "_queue_candidates", new=uncached):
                                        expected = store.page_cases(user, **args)
                                    self.assertEqual(actual, expected)
                finally:
                    if isinstance(store, SqlStore):
                        store.db.close()

    def test_warm_pages_exports_and_denials_do_not_rescan_context(self) -> None:
        data = dataset(queue_cases(90))
        data["as_of"] = AS_OF
        for sql in (False, True):
            with self.subTest(sql=sql), tempfile.TemporaryDirectory() as tmp:
                store = open_store(tmp, sql, data)
                try:
                    store.page_cases(STAFF[1], "all", filters={"queue": "new"}, limit=2)
                    for user in (STAFF[0], STAFF[1]):
                        for queue, _, _ in taskqueues.DEFINITIONS:
                            with patch.object(
                                store, "work_context", wraps=store.work_context
                            ) as ctx:
                                page = store.page_cases(
                                    user, "mine", filters={"queue": queue}, limit=2
                                )
                                self.assertEqual(ctx.call_count, len(page["items"]))
                            with patch.object(
                                store, "work_context", wraps=store.work_context
                            ) as ctx:
                                rows = store.list_cases(user, "all", filters={"queue": queue})
                                self.assertEqual(ctx.call_count, len(rows))
                                self.assertEqual(
                                    len(store.export_csv(rows).splitlines()), len(rows) + 1
                                )
                    with patch.object(store, "_queue_candidates", side_effect=AssertionError):
                        for user, filters, error in (
                            (STAFF[2], {"queue": "new"}, PermissionError),
                            (STAFF[1], {"queue": "invented"}, ValueError),
                        ):
                            with self.assertRaises(error):
                                store.page_cases(user, "all", filters=filters, limit=2)
                        with self.assertRaises(PermissionError):
                            store.page_cases(STAFF[0], "closed", filters={"queue": "new"})
                        closed = store.page_cases(STAFF[1], "closed", filters={"queue": "new"})
                        self.assertEqual(closed["total"], sum(c["closed"] for c in data["cases"]))
                finally:
                    if sql:
                        store.db.close()

    def test_snapshot_policy_and_current_day_invalidate_membership(self) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql), tempfile.TemporaryDirectory() as tmp:
                data: dict[str, Any] = copy.deepcopy(DATA)
                data["as_of"] = AS_OF
                data["cases"][0]["stage_since"] = AS_OF
                data["cases"][2]["resident"]["first_contact_at"] = "2026-01-01"
                store = open_store(tmp, sql, data)
                try:

                    def ids(queue: str, target: Store = store) -> set[str]:
                        return {
                            r["id"]
                            for r in target.list_cases(
                                DATA["staff"][1], "all", filters={"queue": queue}
                            )
                        }

                    self.assertEqual(ids("new"), {"ZF-1"})
                    store.as_of = "2026-11-01"
                    self.assertEqual(ids("new"), set())
                    self.assertEqual(ids("priority"), set())
                    approved = dict(ranking.CURRENT, status="Approved", owner="Synthetic owner")
                    with patch.dict(ranking.CURRENT, approved):
                        self.assertEqual(ids("priority"), set(store.cases))
                    self.assertEqual(ids("priority"), set())
                    with patch("zava_forward.core.controls.today", return_value="2026-10-16"):
                        self.assertNotIn("ZF-3", ids("blocked"))
                    with patch("zava_forward.core.controls.today", return_value="2032-01-01"):
                        self.assertIn("ZF-3", ids("blocked"))
                    store.as_of = "invalid"
                    with self.assertRaises(ValueError):
                        ids("new")
                    store.as_of = AS_OF
                    self.assertEqual(ids("new"), {"ZF-1"})
                finally:
                    if sql:
                        store.db.close()

    def test_saved_case_and_shared_changes_invalidate_json_and_other_sql_process(self) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql), tempfile.TemporaryDirectory() as tmp:
                data = fixture()
                data["as_of"] = AS_OF
                writer = open_store(tmp, sql, data)
                reader = open_store(tmp, sql) if sql else writer
                try:

                    def ids(queue: str, target: Store = reader) -> set[str]:
                        return {
                            r["id"]
                            for r in target.list_cases(
                                DATA["staff"][1], "all", filters={"queue": queue}
                            )
                        }

                    self.assertEqual(ids("blocked"), set())
                    with writer.lock:
                        writer.data["buildings"][0]["holds"].append(hold())
                        writer.save()
                    self.assertEqual(ids("blocked"), {"ZF-2"})
                    with writer.lock:
                        writer.data["buildings"][0]["holds"].clear()
                        writer.save()
                    self.assertEqual(ids("blocked"), set())
                    self.assertEqual(ids("unowned"), set())
                    writer.offer_handoff(data["staff"][0], "ZF-2", data["staff"][1]["email"])
                    self.assertEqual(ids("unowned"), {"ZF-2"})
                    writer.withdraw_handoff(data["staff"][0], "ZF-2")
                    self.assertEqual(ids("unowned"), set())
                    with writer.lock:
                        case = writer._case("ZF-2")
                        case.update(closed=True, stage_since=AS_OF)
                        writer.save()
                    self.assertNotIn("ZF-2", ids("new"))
                finally:
                    if sql:
                        reader.db.close()
                        writer.db.close()

    def test_filter_before_paging_sort_export_and_unchanged_records(self) -> None:
        data: dict[str, Any] = copy.deepcopy(DATA)
        data["as_of"] = AS_OF
        data["cases"] = []
        for i in range(120):
            case = copy.deepcopy(DATA["cases"][0])
            case.update(id=f"Q-{i:03}", stage_since="2026-10-09" if i % 2 == 0 else "2026-10-01")
            case["resident"]["name"] = f"Person {119 - i:03}"
            data["cases"].append(case)
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "seed.json"
            seed.write_text(json.dumps(data))
            for sql in (False, True):
                with self.subTest(sql=sql):
                    store = (
                        SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
                        if sql
                        else (Store(str(seed)))
                    )
                    try:
                        user = data["staff"][0]
                        before = copy.deepcopy(store.data)
                        filters = dict(queue="new", area="Test", wave="Wave 1", owner="RLO-01")
                        first = store.page_cases(user, filters=filters, limit=50)
                        second = store.page_cases(
                            user, filters=filters, limit=50, after=first["next_cursor"]
                        )
                        expected = [f"Q-{i:03}" for i in range(0, 120, 2)]
                        actual = [r["id"] for r in first["items"] + second["items"]]
                        self.assertEqual(actual, expected)
                        self.assertEqual(first["total"], 60)
                        self.assertEqual(second["total"], 60)
                        self.assertEqual(len(set(actual)), 60)
                        by_name = store.list_cases(user, filters=filters, sort="name")
                        self.assertEqual([r["id"] for r in by_name], expected[::-1])
                        self.assertEqual(len(store.export_csv(by_name).splitlines()), 61)
                        detail = store.detail(first["items"][0]["id"], user)
                        self.assertEqual(first["items"][0]["work"], detail["work"])
                        self.assertEqual(store.data, before)
                        with self.assertRaises(ValueError):
                            store.page_cases(user, filters={"queue": "invented"}, limit=50)
                    finally:
                        if isinstance(store, SqlStore):
                            store.db.close()


if __name__ == "__main__":
    unittest.main()

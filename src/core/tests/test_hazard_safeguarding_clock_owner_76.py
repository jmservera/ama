"""Focused tests for Issue #76: hazard and safeguarding items expose a clock and named owner."""

from __future__ import annotations

import copy
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from typing import Any

from dataset import DATA
from zava_forward.core import projection, taskqueues, workflows
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store


def _seed_data() -> dict[str, Any]:
    data: dict[str, Any] = copy.deepcopy(DATA)
    data["as_of"] = "2026-10-16"
    data["staff"].extend(
        [
            dict(
                code="BS-1",
                name="Bea Safe",
                email="bea@example.test",
                role="Building Safety Liaison",
            ),
            dict(
                code="RC-1",
                name="Rex Coordinator",
                email="rex@example.test",
                role="Retrofit Coordinator",
            ),
            dict(
                code="CON-1",
                name="Kim Contractor",
                email="kim@example.test",
                role="Contractor",
                contractor="Test Ltd",
            ),
        ]
    )
    return data


class HazardSafeguardingClockAndOwnerCoreTests(unittest.TestCase):
    def test_clock_windows_running_overdue_completed_and_fail_closed_states(self) -> None:
        roster = _seed_data()["staff"]
        case = copy.deepcopy(DATA["cases"][0])
        as_of = "2026-10-16"

        emergency = taskqueues.project_safety_clock_and_owner(
            dict(
                category="Damp and mould",
                priority="Emergency",
                aware_at="2026-10-15T06:00:00Z",
                owner="Bea Safe",
                released=False,
            ),
            case=case,
            as_of=as_of,
            staff=roster,
        )
        self.assertEqual(
            emergency["clock_label"],
            "Awaab's Law 24h emergency action clock (recorded reference)",
        )
        self.assertEqual(emergency["clock_status"], "running")
        self.assertEqual(emergency["clock_deadline_utc"], "2026-10-16T06:00:00Z")
        self.assertEqual(emergency["clock_remaining_hours"], 6.0)
        self.assertEqual(emergency["clock_basis"], "operational_reference_from_awareness")

        investigation = taskqueues.project_safety_clock_and_owner(
            dict(
                category="Structural",
                priority="Significant",
                aware_at="2026-10-08T12:00:00Z",
                owner="Bea Safe",
                released=False,
            ),
            case=case,
            as_of=as_of,
            staff=roster,
        )
        self.assertEqual(
            investigation["clock_label"],
            "Operational 7d hazard investigation clock (recorded reference)",
        )
        self.assertEqual(investigation["clock_status"], "overdue")
        self.assertEqual(investigation["clock_deadline_utc"], "2026-10-15T12:00:00Z")
        self.assertLess(investigation["clock_remaining_hours"], 0)

        work_start = taskqueues.project_safety_clock_and_owner(
            dict(
                category="Electrical",
                priority="Significant",
                aware_at="2026-10-10T12:00:00Z",
                accepted_at="2026-10-12T12:00:00Z",
                accepted_by=dict(code="BS-1", name="Bea Safe", role="Building Safety Liaison"),
                released=False,
            ),
            case=case,
            as_of=as_of,
            staff=roster,
        )
        self.assertEqual(
            work_start["clock_label"],
            "Operational 14d work-start clock (recorded reference)",
        )
        self.assertEqual(work_start["clock_status"], "running")
        self.assertEqual(work_start["clock_deadline_utc"], "2026-10-24T12:00:00Z")

        sg_urgent = taskqueues.project_safety_clock_and_owner(
            dict(
                category="Safeguarding",
                priority="Emergency",
                aware_at="2026-10-15T12:00:00Z",
                responded_at="2026-10-15T18:00:00Z",
            ),
            case=case,
            as_of=as_of,
            staff=roster,
            default_kind="safeguarding",
        )
        self.assertEqual(sg_urgent["item_kind"], "safeguarding")
        self.assertEqual(sg_urgent["clock_label"], "Safeguarding 24h emergency response clock")
        self.assertEqual(sg_urgent["clock_status"], "completed")
        self.assertEqual(sg_urgent["clock_remaining_hours"], 0.0)

        sg_missing = taskqueues.project_safety_clock_and_owner(
            dict(category="Safeguarding", priority="Significant", noticed="2026-01-01"),
            case=case,
            as_of=as_of,
            staff=roster,
            default_kind="safeguarding",
        )
        self.assertEqual(sg_missing["clock_label"], "Safeguarding 48h referral response clock")
        self.assertEqual(sg_missing["clock_status"], "fail_closed_missing_timestamp")
        self.assertIsNone(sg_missing["clock_deadline_utc"])
        self.assertIsNone(sg_missing["clock_remaining_hours"])
        self.assertEqual(sg_missing["clock_basis"], "missing_timestamp_fail_closed")

    def test_receipt_is_not_acceptance_and_unassigned_items_surface_escalation_owner(
        self,
    ) -> None:
        roster = _seed_data()["staff"]
        case = copy.deepcopy(DATA["cases"][0])
        as_of = "2026-10-16"

        # FR-003: received but not accepted referral must NOT assign destination as direct owner.
        received_unaccepted = taskqueues.project_safety_clock_and_owner(
            dict(
                category="Damp and mould",
                priority="Significant",
                aware_at="2026-10-15T12:00:00Z",
                destination=dict(
                    code="BS-1",
                    name="Bea Safe",
                    email="bea@example.test",
                    role="Building Safety Liaison",
                ),
                received_at="2026-10-15T14:00:00Z",
                accepted_at=None,
                released=False,
            ),
            case=case,
            as_of=as_of,
            staff=roster,
        )
        self.assertTrue(received_unaccepted["unassigned"])
        self.assertEqual(received_unaccepted["owner"], "Unknown")
        self.assertFalse(received_unaccepted["owner_named"])
        self.assertEqual(received_unaccepted["named_owner"], "Bea Safe")
        self.assertEqual(received_unaccepted["accountable_owner"], "Bea Safe")
        self.assertEqual(received_unaccepted["escalation_owner"], "Bea Safe")
        self.assertEqual(received_unaccepted["owner_role"], "Building Safety Liaison")
        self.assertEqual(received_unaccepted["owner_id"], "BS-1")

        # Once accepted_at is recorded, destination becomes the direct named owner.
        accepted = taskqueues.project_safety_clock_and_owner(
            dict(
                category="Damp and mould",
                priority="Significant",
                aware_at="2026-10-15T12:00:00Z",
                destination=dict(
                    code="BS-1",
                    name="Bea Safe",
                    email="bea@example.test",
                    role="Building Safety Liaison",
                ),
                received_at="2026-10-15T14:00:00Z",
                accepted_at="2026-10-15T15:00:00Z",
                released=False,
            ),
            case=case,
            as_of=as_of,
            staff=roster,
        )
        self.assertFalse(accepted["unassigned"])
        self.assertEqual(accepted["owner"], "Bea Safe")
        self.assertTrue(accepted["owner_named"])
        self.assertEqual(accepted["named_owner"], "Bea Safe")
        self.assertEqual(accepted["owner_id"], "BS-1")

        # Orphan case with empty roster falls back to duty lead so owner is never blank/anonymous.
        orphan_case = dict(id="ZF-ORPHAN", owner="Anonymous", owner_code="")
        unallocated = taskqueues.project_safety_clock_and_owner(
            dict(owner="Unknown", priority="Routine"),
            case=orphan_case,
            as_of=as_of,
            staff=[],
            default_kind="safeguarding",
        )
        self.assertTrue(unallocated["unassigned"])
        self.assertEqual(unallocated["named_owner"], "Safeguarding duty lead")
        self.assertEqual(unallocated["escalation_owner"], "Safeguarding duty lead")
        self.assertEqual(unallocated["owner_role"], "Building Safety Liaison")
        self.assertEqual(unallocated["owner_id"], "ESC-SG-DUTY")
        for key in (
            "named_owner",
            "accountable_owner",
            "owner_role",
            "owner_id",
            "escalation_owner",
        ):
            self.assertTrue(unallocated[key])
            self.assertNotIn(str(unallocated[key]).lower(), {"unknown", "anonymous", "none"})

    def test_store_and_sqlstore_parity_for_standalone_safeguarding_and_note_only_canary(
        self,
    ) -> None:
        self.assertIn("Safeguarding", workflows.HAZARD_CATEGORIES)
        data = _seed_data()
        # Case 0: standalone unallocated safeguarding item with overdue deadline and private notes.
        data["cases"][0]["hazards"] = []
        data["cases"][0]["safeguarding_items"] = [
            dict(
                id="SG-76-1",
                priority="Urgent",
                response_due_at="2026-10-15T09:00:00Z",
                note="PRIVATE-SG-NOTE",
                summary="PRIVATE-SG-SUMMARY",
                source="PRIVATE-SG-SOURCE",
            )
        ]
        # Case 1: note-only canary container (like resident_preview_fixture) must remain passive.
        data["cases"][1]["hazards"] = []
        data["cases"][1]["safeguarding"] = dict(note="PASSIVE-CANARY-NOTE-ONLY")

        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "json_seed.json"
            sql_seed = Path(tmp) / "sql_seed.json"
            sql_db = Path(tmp) / "store.sqlite"
            json_path.write_text(json.dumps(data))
            sql_seed.write_text(json.dumps(data))

            store_cls: Any = Store
            sql_store_cls: Any = SqlStore
            jstore: Any = store_cls(str(json_path))
            sstore: Any = sql_store_cls(str(sql_seed), str(sql_db))
            try:
                owner_user = data["staff"][0]
                bsl = next(s for s in data["staff"] if s["code"] == "BS-1")
                coord = next(s for s in data["staff"] if s["code"] == "RC-1")
                contractor = next(s for s in data["staff"] if s["code"] == "CON-1")

                self.assertEqual(jstore.counts(owner_user), sstore.counts(owner_user))
                self.assertGreaterEqual(jstore.counts(owner_user)["hazards"], 1)

                for store in (jstore, sstore):
                    blocked_ids = {
                        r["id"] for r in store.list_cases(bsl, "all", filters={"queue": "blocked"})
                    }
                    overdue_ids = {
                        r["id"] for r in store.list_cases(bsl, "all", filters={"queue": "overdue"})
                    }
                    hazard_ids = {
                        r["id"] for r in store.list_cases(bsl, "all", filters={"flag": "hazard"})
                    }
                    self.assertIn("ZF-1", blocked_ids)
                    self.assertIn("ZF-1", overdue_ids)
                    self.assertIn("ZF-1", hazard_ids)
                    self.assertNotIn("ZF-2", hazard_ids)

                    mine_rows = store.list_cases(owner_user, "mine")
                    zf1_row = next(r for r in mine_rows if r["id"] == "ZF-1")
                    self.assertTrue(zf1_row["hazard"])
                    self.assertTrue(zf1_row["safeguarding"])
                    sg_clock = zf1_row["work"]["hazard_clocks"][0]
                    self.assertEqual(sg_clock["item_kind"], "safeguarding")
                    self.assertEqual(sg_clock["clock_status"], "overdue")
                    self.assertEqual(sg_clock["clock_deadline_utc"], "2026-10-15T09:00:00Z")
                    self.assertTrue(sg_clock["unassigned"])
                    self.assertEqual(sg_clock["named_owner"], zf1_row["owner"])
                    self.assertEqual(sg_clock["escalation_owner"], zf1_row["owner"])

                    # Reason-authorized staff detail
                    detail_bsl = store.detail("ZF-1", bsl)
                    assert detail_bsl is not None
                    self.assertEqual(len(detail_bsl["safeguarding_items"]), 1)
                    self.assertEqual(len(detail_bsl["hazards"]), 1)
                    self.assertTrue(detail_bsl["hazards"][0]["standalone_safeguarding"])
                    self.assertEqual(detail_bsl["hazards"][0]["owner"], zf1_row["owner"])
                    self.assertIsInstance(detail_bsl["hazards"][0]["owner"], str)

                    # Non-reason staff detail redacts notes while preserving clock & named owner
                    detail_rc = store.detail("ZF-1", coord)
                    assert detail_rc is not None
                    sg_rc = detail_rc["safeguarding_items"][0]
                    self.assertEqual(sg_rc["note"], projection.NOTE_HELD)
                    self.assertEqual(sg_rc["summary"], projection.NOTE_HELD)
                    self.assertEqual(sg_rc["source"], projection.NOTE_HELD)
                    self.assertEqual(sg_rc["clock_status"], "overdue")
                    self.assertEqual(sg_rc["named_owner"], zf1_row["owner"])
                    self.assertTrue(sg_rc["unassigned"])

                    # Contractor default-deny withholds all safety structures (PR-002)
                    detail_con = store.detail("ZF-1", contractor)
                    if detail_con is not None:
                        self.assertNotIn("hazards", detail_con)
                        self.assertNotIn("safeguarding_items", detail_con)
                        self.assertNotIn("work", detail_con)

                # Reopen an older revision=3 SQL database and verify MEMBERSHIP_REVISION=4 rebuilds.
                sstore.db.close()
                raw_conn = sqlite3.connect(str(sql_db))
                raw_conn.execute(
                    "UPDATE cases SET queue_blocked = 0, queue_overdue = 0 WHERE id = 'ZF-1'"
                )
                raw_conn.execute(
                    "UPDATE meta SET value = 'stale-revision-3' WHERE key = 'queue_context'"
                )
                raw_conn.commit()
                raw_conn.close()

                reopened: Any = sql_store_cls(str(sql_seed), str(sql_db))
                try:
                    rebuilt_blocked = {
                        r["id"]
                        for r in reopened.list_cases(bsl, "all", filters={"queue": "blocked"})
                    }
                    rebuilt_overdue = {
                        r["id"]
                        for r in reopened.list_cases(bsl, "all", filters={"queue": "overdue"})
                    }
                    self.assertIn("ZF-1", rebuilt_blocked)
                    self.assertIn("ZF-1", rebuilt_overdue)
                finally:
                    reopened.db.close()
            finally:
                sstore.db.close()

    def test_raw_standalone_safeguarding_visibility_and_ai_output_gating(self) -> None:
        data = _seed_data()
        bsl = next(s for s in data["staff"] if s["code"] == "BS-1")
        coord = next(s for s in data["staff"] if s["code"] == "RC-1")
        grants = dict(
            code="GE-1",
            name="Gail Grants",
            email="gail@example.test",
            role="Grants and Evidence Officer",
        )
        data["staff"].append(grants)

        zf1 = data["cases"][0]
        zf1["safeguarding_items"] = [
            dict(
                id="SG-RAW-76",
                category="Safeguarding concern",
                priority="Emergency",
                aware_at="2026-10-14T09:00:00Z",
                summary="SG-RAW-SUMMARY-TOKEN-76",
                source="SG-RAW-SOURCE-TOKEN-76",
                job="SG-RAW-JOB-TOKEN-76",
                reason="SG-RAW-REASON-TOKEN-76",
                note="SG-RAW-NOTE-TOKEN-76",
            )
        ]
        zf1["documents"] = [
            dict(
                id="DOC-SG-LEAK",
                kind="Survey",
                name="survey.pdf",
                added="2026-10-10",
                summary="Survey synthesis mentioning SG-RAW-SUMMARY-TOKEN-76.",
            ),
            dict(
                id="DOC-CLEAN",
                kind="EPC",
                name="epc.pdf",
                added="2026-10-10",
                summary="Clean EPC summary with rated band D.",
            ),
        ]
        zf1.setdefault(
            "funding",
            dict(
                route="Not decided",
                status="Not started",
                reference="",
                draft="",
                approved_by=None,
            ),
        )["draft"] = "Draft grant submission referencing SG-RAW-REASON-TOKEN-76."

        zf2 = data["cases"][1]
        zf2["safeguarding"] = dict(note="PASSIVE-CANARY-NOTE-ONLY-76")

        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "seed.json"
            json_path.write_text(json.dumps(data))
            store_cls: Any = Store
            store: Any = store_cls(str(json_path))

            raw_zf1 = store.cases[zf1["id"]]
            proj_rc = projection.project_case_visibility(coord, raw_zf1)
            assert proj_rc is not None
            sg_proj = proj_rc["safeguarding_items"][0]
            for field in ("summary", "source", "job", "reason", "note"):
                self.assertEqual(sg_proj[field], projection.NOTE_HELD)
            docs_rc = {d["id"]: d["summary"] for d in proj_rc["documents"]}
            self.assertEqual(docs_rc["DOC-SG-LEAK"], projection.NOTE_HELD)
            self.assertEqual(docs_rc["DOC-CLEAN"], "Clean EPC summary with rated band D.")

            proj_grants = projection.project_case_visibility(grants, raw_zf1)
            assert proj_grants is not None
            self.assertEqual(proj_grants["funding"]["draft"], projection.NOTE_HELD)

            withheld_rc = projection.withheld_scope_values(store, coord, [zf1["id"]])
            for token in (
                "sg-raw-summary-token-76",
                "sg-raw-source-token-76",
                "sg-raw-job-token-76",
                "sg-raw-reason-token-76",
                "sg-raw-note-token-76",
            ):
                self.assertIn(token, withheld_rc)

            withheld_other = projection.withheld_scope_values(store, coord, [zf2["id"]])
            self.assertIn("sg-raw-summary-token-76", withheld_other)

            proj_bsl = projection.project_case_visibility(bsl, raw_zf1)
            assert proj_bsl is not None
            self.assertEqual(
                proj_bsl["safeguarding_items"][0]["summary"], "SG-RAW-SUMMARY-TOKEN-76"
            )
            docs_bsl = {d["id"]: d["summary"] for d in proj_bsl["documents"]}
            self.assertEqual(
                docs_bsl["DOC-SG-LEAK"],
                "Survey synthesis mentioning SG-RAW-SUMMARY-TOKEN-76.",
            )

            proj_zf2_rc = projection.project_case_visibility(coord, store.cases[zf2["id"]])
            assert proj_zf2_rc is not None
            self.assertEqual(proj_zf2_rc["safeguarding"], dict(note=projection.NOTE_HELD))
            self.assertFalse(taskqueues.has_open_safeguarding(store.cases[zf2["id"]]))


if __name__ == "__main__":
    unittest.main()

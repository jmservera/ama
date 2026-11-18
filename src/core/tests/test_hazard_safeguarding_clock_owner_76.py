"""Focused tests for Issue #76: hazard and safeguarding items expose a clock and named owner."""

from __future__ import annotations

import copy
import unittest
from typing import Any

from dataset import DATA
from zava_forward.core import taskqueues


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


if __name__ == "__main__":
    unittest.main()

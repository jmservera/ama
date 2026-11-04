"""Building dependency isolation in the connected same-home journey (Refs #134, slice 5).

Constructed-fixture evidence only: not user validation. A shared-building hold scoped to one home
blocks that home's move to ordering and never shows as, or completes, a journey stage; a sibling
home in the same building is unaffected. The trace reads the audit chain and approves nothing.
"""

import tempfile
import unittest
from typing import Any

from building_fixture import fixture, hold, open_store
from dataset import supplied_appointment_fixture
from zava_forward.core import buildings, journey_trace
from zava_forward.core.store import GateError


def query() -> dict[str, Any]:
    side = dict(source_id="SYN-STOCK", date="2026-01-01", version="1")
    return dict(
        field="epc",
        left=dict(side, value="D", validation_state="Unvalidated"),
        right=dict(side, source_id="SYN-SURVEY", value="E", validation_state="Disputed"),
        query_owner="sam@example.test",
    )


HOME = "ZF-2"
SIBLING = "ZF-3"


class BuildingJourney(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store: Any = open_store(tmp.name, False, fixture())
        self.manager = self.store.data["staff"][1]
        found = query()
        found["query_owner"] = self.manager["email"]
        self.store.stock_reconcile(self.manager, HOME, found)
        self.store.data["buildings"][0]["holds"].append(hold())
        self.store.save()

    def trace(self, case: str) -> dict[str, Any]:
        result: dict[str, Any] = journey_trace.journey_trace(self.store.audit_entries(), case)
        return result

    def blockers(self, case: str) -> list[str]:
        return buildings.blockers(self.store.data, self.store.cases, self.store.cases[case])

    def test_hold_blocks_only_the_scoped_home_and_names_owner_and_next_action(self) -> None:
        reasons = self.blockers(HOME)
        self.assertEqual(len(reasons), 1)
        self.assertIn("Owner: Synthetic safety reviewer", reasons[0])
        self.assertIn("Next action: obtain accountable human review", reasons[0])
        self.assertEqual(self.blockers(SIBLING), [])
        self.assertTrue(self.store.detail(HOME)["gate"])

    def withdraw_stock_query(self) -> None:
        body = dict(query_id="SQ-1", action="withdraw", reason="Duplicate query")
        self.store.stock_query_event(self.manager, HOME, body)

    def book_home(self) -> None:
        """Make every other advance gate pass so only the building hold can refuse."""
        row = self.store.data["buildings"][0]["holds"][0]
        row["status"] = "Resolved"
        wid = self.store.issue_work_order(
            self.manager,
            "PKG-SHARED",
            HOME,
            resident_bindings=[dict(measure="Loft insulation", context_revision=1)],
        )
        supplied_appointment_fixture(self.store, self.manager, wid)
        self.store.record_wo_appointment(self.manager, wid, "Booked", "2099-01-01")
        row["status"] = "Open"

    def test_blocked_advance_adds_no_journey_stage_or_audit_entry(self) -> None:
        self.withdraw_stock_query()
        self.book_home()
        self.assertEqual(len(self.blockers(HOME)), 1)
        before = len(list(self.store.audit_entries()))
        with self.assertRaises(GateError) as refused:
            self.store.advance(self.manager, HOME)
        reasons = refused.exception.reasons
        self.assertEqual(reasons, self.blockers(HOME))
        self.assertIn("Owner: Synthetic safety reviewer", reasons[0])
        self.assertEqual(len(list(self.store.audit_entries())), before)
        trace = self.trace(HOME)
        self.assertEqual([e["stage"] for e in trace["events"]], ["epc_conflict"])
        self.assertEqual([s["status"] for s in trace["stages"]][1:], ["Not recorded"] * 4)
        self.assertFalse(trace["complete"])
        self.assertTrue(self.store.verify_audit())

    def test_control_advance_succeeds_without_the_hold(self) -> None:
        self.withdraw_stock_query()
        self.book_home()
        self.store.data["buildings"][0]["holds"][0]["status"] = "Resolved"
        self.assertEqual(self.blockers(HOME), [])
        before = len(list(self.store.audit_entries()))
        self.store.advance(self.manager, HOME)
        self.assertEqual(self.store.detail(HOME)["stage"], "Install booked")
        self.assertGreater(len(list(self.store.audit_entries())), before)

    def test_sibling_in_same_building_has_no_events_from_the_hold_or_the_conflict(self) -> None:
        trace = self.trace(SIBLING)
        self.assertEqual(trace["events"], [])
        self.assertEqual({s["status"] for s in trace["stages"]}, {"Not recorded"})
        self.assertEqual({i["status"] for i in trace["intervals"]}, {"Unknown"})

    def test_resolution_needs_explicit_scope_and_a_recorded_status(self) -> None:
        row = self.store.data["buildings"][0]["holds"][0]
        row["status"] = "Resolved"
        self.assertEqual(self.blockers(HOME), [])
        row["case_ids"] = None
        self.assertIn("applicability unknown", self.blockers(HOME)[0])
        row["status"] = "Open"
        row["case_ids"] = [SIBLING]
        self.assertEqual(self.blockers(HOME), [])
        self.assertEqual(len(self.blockers(SIBLING)), 1)

    def test_unknown_hold_list_blocks_every_home_rather_than_clearing_them(self) -> None:
        self.store.data["buildings"][0]["holds"] = None
        for case in (HOME, SIBLING):
            self.assertIn("holds are unknown", self.blockers(case)[0])


if __name__ == "__main__":
    unittest.main()

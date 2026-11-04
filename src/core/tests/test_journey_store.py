"""Same-home journey driven through the real store, not ledger-shaped entries (Refs #134).

Constructed-fixture evidence only: not user validation. Every step is a recorded action by a
different synthetic person; the trace only reads the audit chain and approves nothing.
"""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset
from test_finance_signoffs import STAFF as FINANCE_STAFF
from test_finance_signoffs import lines, person
from test_grant_lifecycle_controls import designate
from test_quality_procurement import EVIDENCE
from test_stock_reconciliation import query
from zava_forward.core import journey_trace
from zava_forward.core.store import ConflictError, GateError, Store

HOME = "ZF-1"
SIBLING = "ZF-2"


class StoreJourney(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = copy.deepcopy(dataset.DATA)
        staff = copy.deepcopy(FINANCE_STAFF) + [person("QI-2", "Quality Inspector")]  # type: ignore[no-untyped-call]
        for index in (1, 2):
            staff[index] = designate(staff[index])
            for permission in staff[index]["financial_authority"]["permissions"]:
                permission["route"] = "Warm Homes"
        data["staff"] = staff
        data["cases"][0]["measures"] = "Loft insulation, Cavity wall"
        path = Path(tmp.name) / "synthetic.json"
        path.write_text(json.dumps(data))
        self.store = Store(str(path))  # type: ignore[no-untyped-call]
        self.user = {s["code"]: s for s in staff}

    def fin(self, code: str, action: str, **body: Any) -> None:
        self.store.finance_action(self.user[code], HOME, dict(action=action, **body))  # type: ignore[no-untyped-call]

    def tech(self, code: str, action: str, **body: Any) -> None:
        self.store.technical_action(self.user[code], HOME, dict(action=action, **body))  # type: ignore[no-untyped-call]

    def conflict_and_correction(self, case: str, resolve: bool = True) -> None:
        owner = self.user["PM-1"]
        found = query()
        found["query_owner"] = owner["email"]
        self.store.stock_reconcile(owner, case, found)  # type: ignore[no-untyped-call]
        if resolve:
            self.store.stock_query_event(  # type: ignore[no-untyped-call]
                self.user["PM-2"],
                case,
                dict(query_id="SQ-1", action="resolve", reason="Constructed", evidence="SYN-1"),
            )

    def journey(self) -> None:
        self.conflict_and_correction(HOME)
        self.tech("RC-1", "design_submit", note="Loft and wall")
        self.tech("QI-1", "signoff_give", type="assessment")
        self.tech("RC-2", "signoff_give", type="design")
        self.tech("BSL-1", "signoff_give", type="building")
        design = self.store.cases[HOME]["technical"]["design_version"]
        self.store.resident_action(  # type: ignore[no-untyped-call]
            self.user["RLO-1"],
            HOME,
            dict(
                action="scope_record",
                measure="Loft insulation",
                scope="Synthetic scope",
                design_version=design,
                source="Synthetic supplied scope",
            ),
        )
        self.store.resident_action(  # type: ignore[no-untyped-call]
            self.user["RLO-1"],
            HOME,
            dict(
                action="decision_record",
                measure="Loft insulation",
                status="Accepted",
                answered_by="The resident",
                context_revision=1,
                source="Synthetic supplied resident statement",
            ),
        )
        store = self.store
        store.submit_quality(  # type: ignore[no-untyped-call]
            self.user["RLO-1"],
            HOME,
            "Loft insulation",
            "Install Team",
            "Installer",
            EVIDENCE,
            context_revision=1,
        )
        store.accept_quality(self.user["QI-2"], HOME, 0, "All good")  # type: ignore[no-untyped-call]
        store.hand_over_quality(self.user["RLO-1"], HOME, 0, "Guide given", True)  # type: ignore[no-untyped-call]
        self.fin("GEO-1", "budget_propose", amount=10000)
        self.fin("PM-1", "budget_approve")
        self.fin(
            "GEO-1",
            "commit_raise",
            supplier="Test Ltd",
            contract="C-1",
            work_order="WO-1",
            measure="Loft insulation",
            amount=5000,
            quantity=10,
        )
        self.fin("PM-1", "commit_approve", id="COM-1")
        self.fin(
            "GEO-1",
            "invoice_receive",
            supplier="Test Ltd",
            work_order="WO-1",
            ref="INV-100",
            lines=lines(),  # type: ignore[no-untyped-call]
        )
        invoice = store.detail(HOME)["finance"]["invoices"][-1]["id"]  # type: ignore[no-untyped-call]
        self.fin("GEO-1", "invoice_match", id=invoice)
        self.fin("PM-2", "disposition", id=invoice, decision="Accept for payment", note="Checked")
        self.fin("GEO-1", "payment_status", id=invoice, status="Paid outside this system")

    def trace(self, case: str) -> dict[str, Any]:
        entries = list(self.store.audit_entries())  # type: ignore[no-untyped-call]
        return journey_trace.journey_trace(entries, case)

    def test_store_journey_reaches_financial_closure_in_order(self) -> None:
        self.journey()
        self.assertTrue(self.store.verify_audit())  # type: ignore[no-untyped-call]
        trace = self.trace(HOME)
        self.assertEqual([s["status"] for s in trace["stages"]], ["Recorded"] * 5)
        self.assertEqual(trace["order_findings"], [])
        self.assertTrue(trace["independent_decisions"])
        self.assertEqual(
            sorted(trace["decision_domains"]), ["finance", "quality", "resident", "technical"]
        )
        self.assertTrue(trace["complete"])
        self.assertEqual(trace["user_validation"], "not-established")

    def test_paused_resident_answer_is_not_an_independent_decision(self) -> None:
        self.journey()
        entries = [
            e
            for e in self.store.audit_entries()  # type: ignore[no-untyped-call]
            if e["action"] != "resident_decision_record"
        ]
        entries.append(
            dict(
                case=HOME,
                action="resident_decision_record",
                who="rlo-1@example.test",
                at=None,
                detail="scope revision 1: Paused decision v2",
            )
        )
        trace = journey_trace.journey_trace(entries, HOME)
        self.assertNotIn("resident", trace["decision_domains"])

    def test_sibling_home_stays_not_recorded(self) -> None:
        self.journey()
        sibling = self.trace(SIBLING)
        self.assertEqual({s["status"] for s in sibling["stages"]}, {"Not recorded"})
        self.assertFalse(sibling["complete"])
        self.assertEqual({i["status"] for i in sibling["intervals"]}, {"Unknown"})

    def test_sibling_conflict_does_not_enter_this_homes_trace(self) -> None:
        self.conflict_and_correction(SIBLING, resolve=False)
        self.assertEqual(self.trace(HOME)["events"], [])
        self.assertEqual([e["stage"] for e in self.trace(SIBLING)["events"]], ["epc_conflict"])

    def test_open_conflict_blocks_technical_signoff_until_corrected(self) -> None:
        self.conflict_and_correction(HOME, resolve=False)
        with self.assertRaises((GateError, ConflictError)):
            self.tech("QI-1", "signoff_give", type="assessment")
        trace = self.trace(HOME)
        self.assertEqual([s["status"] for s in trace["stages"]][1:], ["Not recorded"] * 4)
        self.assertFalse(trace["complete"])


if __name__ == "__main__":
    unittest.main()

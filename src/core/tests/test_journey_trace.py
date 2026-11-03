"""Same-home journey trace: order, unknown intervals and sibling/building isolation (Refs #134)."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset
from building_fixture import fixture, hold
from test_stock_reconciliation import query
from zava_forward.core import buildings, journey_trace, ledger
from zava_forward.core.store import Store

HOME = "ZF-3"
SIBLING = "ZF-1"


def entry(who: str, action: str, case: str, detail: str, at: str | None) -> dict[str, Any]:
    result = ledger.make_entry(who, action, case, detail, ledger.GENESIS, at="x")
    result["at"] = at
    return result


class JourneyTrace(unittest.TestCase):
    def open_store(self) -> Store:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "synthetic.json"
        path.write_text(json.dumps(copy.deepcopy(dataset.DATA)))
        return Store(str(path))

    def recorded(self) -> list[dict[str, Any]]:
        store = self.open_store()
        users = {p["email"].split("@")[0]: p for p in store.data["staff"]}
        for case in (HOME, SIBLING):
            store.stock_reconcile(users["sam"], case, query())
        store.stock_query_event(
            users["pam"],
            HOME,
            dict(query_id="SQ-1", action="resolve", reason="Constructed", evidence="SYN-REVIEW-1"),
        )
        return list(store.audit_entries())

    def later(self, case: str, spacing: bool = True) -> list[dict[str, Any]]:
        at = (lambda n: f"2026-03-0{n}T09:00:00") if spacing else (lambda n: None)
        return [
            entry("resident@example.test", "resident_decision", case, "Loft accepted", at(1)),
            entry("qi@example.test", "technical_signoff_give", case, "design", at(2)),
            entry("insp@example.test", "quality_accepted", case, "Loft QC v1", at(3)),
            entry("insp@example.test", "quality_handover", case, "Loft handed over", at(4)),
            entry("fin@example.test", "finance_payment_status", case, "Paid (record only)", at(5)),
        ]

    def test_real_audit_entries_map_to_conflict_and_correction(self) -> None:
        trace = journey_trace.journey_trace(self.recorded(), HOME)
        self.assertEqual(
            [(e["stage"], e["who"]) for e in trace["events"]],
            [("epc_conflict", "sam@example.test"), ("correction", "pam@example.test")],
        )
        self.assertFalse(trace["complete"])
        self.assertEqual(trace["evidence_class"], "constructed-fixture")
        self.assertEqual(trace["user_validation"], "not-established")

    def test_connected_journey_orders_stages_and_measures_intervals(self) -> None:
        entries = self.recorded() + self.later(HOME)
        for index, event in enumerate(e for e in entries[:3] if e["case"] == HOME):
            event["at"] = f"2026-02-0{index + 1}T09:00:00"
        trace = journey_trace.journey_trace(entries, HOME)
        self.assertEqual([s["status"] for s in trace["stages"]], ["Recorded"] * 5)
        self.assertEqual(trace["order_findings"], [])
        self.assertTrue(trace["independent_decisions"])
        self.assertTrue(trace["complete"])
        self.assertEqual({i["status"] for i in trace["intervals"]}, {"Recorded"})
        self.assertEqual(trace["intervals"][-1]["seconds"], 86400)

    def test_missing_stage_and_timestamp_stay_unknown(self) -> None:
        entries = self.recorded() + self.later(HOME, spacing=False)[:3]
        trace = journey_trace.journey_trace(entries, HOME)
        self.assertEqual(trace["stages"][3]["status"], "Not recorded")
        self.assertFalse(trace["complete"])
        by_pair = {(i["from_stage"], i["to_stage"]): i for i in trace["intervals"]}
        self.assertEqual(by_pair[("independent_decisions", "handover")]["status"], "Unknown")
        self.assertEqual(by_pair[("handover", "financial_closure")]["seconds"], None)
        self.assertEqual(
            by_pair[("correction", "independent_decisions")]["reason"],
            "A timestamp is missing or unreadable.",
        )

    def test_one_actor_across_decisions_is_not_independent(self) -> None:
        entries = self.recorded() + self.later(HOME)
        for e in entries:
            if e["action"] in ("technical_signoff_give", "quality_accepted"):
                e["who"] = "resident@example.test"
        trace = journey_trace.journey_trace(entries, HOME)
        self.assertEqual(trace["shared_decision_actors"], ["resident@example.test"])
        self.assertFalse(trace["independent_decisions"])
        self.assertFalse(trace["complete"])

    def test_contradicting_order_is_reported(self) -> None:
        entries = self.later(HOME) + self.recorded()
        trace = journey_trace.journey_trace(entries, HOME)
        self.assertEqual(
            trace["order_findings"], ["independent_decisions is recorded before correction."]
        )
        self.assertFalse(trace["complete"])

    def test_sibling_entries_never_create_or_complete_stages(self) -> None:
        entries = self.recorded() + self.later(SIBLING)
        home = journey_trace.journey_trace(entries, HOME)
        self.assertEqual([s["status"] for s in home["stages"][2:]], ["Not recorded"] * 3)
        self.assertTrue(all(e["detail"] != "Loft handed over" for e in home["events"]))
        sibling = journey_trace.journey_trace(entries, SIBLING)
        self.assertEqual(sibling["stages"][1]["status"], "Not recorded")

    def test_unrelated_query_resolution_is_not_a_correction(self) -> None:
        entries = [
            entry("sam@example.test", "stock_comparison", HOME, "SQ-1 build_year; owner x", None),
            entry("pam@example.test", "stock_query_resolve", HOME, "SQE-1 SQ-1: Reconciled", None),
        ]
        trace = journey_trace.journey_trace(entries, HOME)
        self.assertEqual(trace["events"], [])

    def test_building_hold_scoped_to_sibling_does_not_block_this_home(self) -> None:
        data = fixture()
        data["buildings"][0]["holds"] = [hold()]
        cases = {c["id"]: c for c in data["cases"]}
        self.assertEqual(buildings.blockers(data, cases, cases[HOME]), [])
        self.assertTrue(buildings.blockers(data, cases, cases["ZF-2"]))
        data["buildings"][0]["holds"][0]["case_ids"] = None
        self.assertTrue(buildings.blockers(data, cases, cases[HOME]))


if __name__ == "__main__":
    unittest.main()

"""Synthetic building context, scoping and independent home gate regressions."""

import json
import tempfile
import unittest
from copy import deepcopy
from typing import Any

from building_fixture import fixture, hold, open_store
from zava_forward.core import buildings
from zava_forward.core.store import ConflictError, GateError


class BuildingTests(unittest.TestCase):
    def test_shared_view_keeps_home_evidence_allocations_and_approvals_home(self) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql), tempfile.TemporaryDirectory() as folder:
                store = open_store(folder, sql, fixture())
                try:
                    before = deepcopy(store.cases)
                    view = store.building_view(store.data["staff"][1], "SYN-B1")
                    self.assertEqual(view["costs"][0]["amount_gbp"], "12000.00")
                    self.assertEqual(len(view["homes"]), 2)
                    for key in ("decision", "quality", "documents", "cost_allocation", "technical"):
                        self.assertNotIn(key, json.dumps(view))
                    self.assertIn("cost_allocation", store.detail("ZF-2"))
                    self.assertEqual(store.cases, before)
                    view["systems"][0]["label"] = "Changed by reader"
                    self.assertNotEqual(store.data["buildings"][0]["systems"], view["systems"])
                    store.save()
                finally:
                    if sql:
                        store.db.close()
                reopened = open_store(folder, sql)
                try:
                    self.assertEqual(reopened.data["buildings"], fixture()["buildings"])
                    self.assertEqual(reopened.cases["ZF-2"]["building_id"], "SYN-B1")
                    self.assertEqual(
                        reopened.cases["ZF-2"]["cost_allocation"][0]["amount_gbp"], "6000.00"
                    )
                finally:
                    if sql:
                        reopened.db.close()

    def test_shared_id_and_clear_building_never_satisfy_target_home_gates(self) -> None:
        for sql in (False, True):
            for missing in ("resident", "funding", "technical"):
                data = fixture()
                home = data["cases"][0]
                if missing == "resident":
                    home["decision"]["status"] = "Waiting"
                    home["measure_decisions"] = {}
                elif missing == "funding":
                    home["funding_ok"] = False
                else:
                    home["technical"] = {"signoffs": {}, "design_version": 1}
                with (
                    self.subTest(sql=sql, missing=missing),
                    tempfile.TemporaryDirectory() as folder,
                ):
                    store = open_store(folder, sql, data)
                    try:
                        before = deepcopy(store.cases)
                        store.building_view(data["staff"][1], "SYN-B1")
                        self.assertTrue(store.detail("ZF-2")["gate"])
                        with self.assertRaises(GateError):
                            store.advance(data["staff"][0], "ZF-2")
                        self.assertEqual(store.cases, before)
                        self.assertFalse(store.cases["ZF-2"]["closed"])
                        self.assertNotIn("quality", store.cases["ZF-2"])
                        self.assertEqual(
                            store.cases["ZF-2"]["documents"], before["ZF-2"]["documents"]
                        )
                        self.assertEqual(store.cases["ZF-3"]["quality"][0]["state"], "Accepted")
                    finally:
                        if sql:
                            store.db.close()

    def test_explicit_home_and_package_scope_blocks_only_matching_instruction(self) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql), tempfile.TemporaryDirectory() as folder:
                store = open_store(folder, sql, fixture())
                manager = store.data["staff"][1]
                try:
                    wid = store.issue_work_order(
                        manager,
                        "PKG-SHARED",
                        "ZF-2",
                        resident_bindings=[dict(measure="Loft insulation", context_revision=1)],
                    )
                    store.data["buildings"][0]["holds"].append(hold())
                    store.save()
                    before = deepcopy(store.cases)
                    orders = deepcopy(store.data["procurement"]["work_orders"])
                    for operation, args in (
                        (store.advance, (manager, "ZF-2")),
                        (store.issue_work_order, (manager, "PKG-SHARED", "ZF-2")),
                        (store.reissue_work_order, (manager, wid, "Different text", "Changed")),
                    ):
                        with self.assertRaises(GateError):
                            operation(*args)
                        self.assertEqual(store.cases, before)
                        self.assertEqual(store.data["procurement"]["work_orders"], orders)
                    other = store.issue_work_order(
                        manager,
                        "PKG-OTHER",
                        "ZF-2",
                        resident_bindings=[dict(measure="Loft insulation", context_revision=1)],
                    )
                    store.reissue_work_order(
                        manager,
                        other,
                        "New text",
                        "Synthetic change",
                        resident_bindings=[dict(measure="Loft insulation", context_revision=1)],
                    )
                    sibling = store.issue_work_order(
                        manager,
                        "PKG-OTHER",
                        "ZF-3",
                        resident_bindings=[dict(measure="Loft insulation", context_revision=1)],
                    )
                    store.record_wo_appointment(manager, sibling, "Booked", "2099-01-01")
                    store.advance(manager, "ZF-3")
                    self.assertEqual(store.detail("ZF-3")["stage"], "Install booked")
                    store.log_call(manager, "ZF-2", "Safety referral", "Synthetic hazard intake")
                    self.assertEqual(len(store.cases["ZF-2"]["contacts"]), 1)
                    store.raise_hazard(
                        manager,
                        "ZF-2",
                        "Damp and mould",
                        "Emergency",
                        "Synthetic",
                        metadata=dict(source="Synthetic report", aware_at="2026-01-01T10:00:00Z"),
                    )
                    self.assertFalse(store.cases["ZF-2"]["hazards"][-1]["released"])
                    store.refer_hazard(
                        manager,
                        "ZF-2",
                        0,
                        manager["email"],
                        "SYN-REPAIR",
                        metadata=dict(evidence="Synthetic sending reference"),
                    )
                    self.assertEqual(store.cases["ZF-2"]["hazards"][-1]["job"], "SYN-REPAIR")
                    self.assertTrue(store.verify_audit())
                finally:
                    if sql:
                        store.db.close()

    def test_unknown_scope_missing_record_and_known_empty_are_distinct(self) -> None:
        data = fixture()
        cases = {c["id"]: c for c in data["cases"]}
        home = cases["ZF-2"]
        self.assertEqual(buildings.blockers(data, cases, home), [])
        for category in ("holds", "dependencies"):
            data["buildings"][0][category] = None
            self.assertIn("unknown", buildings.blockers(data, cases, home)[0])
            data["buildings"][0][category] = []
        row = hold()
        data["buildings"][0]["holds"] = [row]
        for field in ("case_ids", "package_ids"):
            saved = row[field]
            row[field] = None
            self.assertIn("unknown", buildings.blockers(data, cases, home)[0])
            row[field] = []
            self.assertEqual(buildings.blockers(data, cases, home), [])
            row[field] = saved
        self.assertEqual(buildings.blockers(data, cases, cases["ZF-3"]), [])
        row["status"] = "Resolved"
        self.assertEqual(buildings.blockers(data, cases, home), [])
        data.pop("buildings")
        self.assertIn("unknown", buildings.blockers(data, cases, home)[0])
        home.pop("building_id")
        self.assertEqual(buildings.blockers(data, cases, home), [])

    def test_invalid_refs_amounts_and_approval_payloads_are_explicit_errors(self) -> None:
        changes: list[tuple[str, str, Any]] = [
            ("holds", "case_ids", ["NOT-A-HOME"]),
            ("holds", "package_ids", ["NOT-A-PACKAGE"]),
            ("holds", "case_ids", ["ZF-2", "ZF-2"]),
            ("costs", "work_id", "NOT-A-WORK"),
            ("costs", "amount_gbp", "NaN"),
            ("costs", "amount_gbp", "-1"),
            ("costs", "amount_gbp", "1.001"),
            ("costs", "amount_gbp", 1.5),
            ("works", "approved_by", "An invented approver"),
        ]
        for category, key, value in changes:
            with self.subTest(category=category, key=key, value=value):
                data = fixture()
                data["buildings"][0]["holds"] = [hold()]
                data["buildings"][0][category][0][key] = value
                cases = {c["id"]: c for c in data["cases"]}
                with self.assertRaises(ValueError):
                    buildings.record(data, cases, "SYN-B1")
                self.assertTrue(buildings.blockers(data, cases, cases["ZF-2"]))

    def test_legacy_stores_are_not_silently_reseeded(self) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql), tempfile.TemporaryDirectory() as folder:
                data = fixture()
                data.pop("buildings")
                store = open_store(folder, sql, data)
                store.set_decision(data["staff"][0], "ZF-2", "Declined")
                if sql:
                    store.db.close()
                reopened = open_store(folder, sql, fixture())
                try:
                    self.assertNotIn("buildings", reopened.data)
                    self.assertEqual(reopened.cases["ZF-2"]["decision"]["status"], "Declined")
                    self.assertIn("unknown", reopened.detail("ZF-2")["gate"][-1])
                finally:
                    if sql:
                        reopened.db.close()

    def test_sibling_quality_and_closure_do_not_transfer(self) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql), tempfile.TemporaryDirectory() as folder:
                data = fixture()
                data["cases"][1]["closed"] = True
                data["cases"][0]["quality"] = [
                    dict(data["cases"][1]["quality"][0], state="Submitted", accepted_by=None)
                ]
                store = open_store(folder, sql, data)
                try:
                    manager = data["staff"][1]
                    before = deepcopy(store.cases)
                    view = store.building_view(manager, "SYN-B1")
                    self.assertEqual([h["closed"] for h in view["homes"]], [False, True])
                    with self.assertRaises(ValueError):
                        store.hand_over_quality(manager, "ZF-2", 0, "Synthetic handover", True)
                    self.assertEqual(store.cases, before)
                    self.assertEqual(store.cases["ZF-2"]["quality"][0]["state"], "Submitted")
                    self.assertEqual(store.cases["ZF-3"]["quality"][0]["state"], "Accepted")
                finally:
                    if sql:
                        store.db.close()

    def test_sql_building_document_sync_and_conflict_use_existing_dialect_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            first = open_store(folder, True, fixture())
            second = open_store(folder, True)
            try:
                first.data["buildings"][0]["holds"].append(hold())
                first.save()
                view = second.building_view(second.data["staff"][1], "SYN-B1")
                self.assertEqual(view["holds"][0], hold())
                self.assertTrue(second.detail("ZF-2")["gate"])
                reopened = open_store(folder, True)
                try:
                    self.assertEqual(reopened.data["buildings"][0]["holds"][0], hold())
                finally:
                    reopened.db.close()
                with first.lock:
                    second.data["buildings"][0]["version"] = 2
                    second.save()
                    first.data["buildings"][0]["version"] = 3
                    with self.assertRaises(ConflictError):
                        first.save()
                self.assertEqual(first.data["buildings"][0]["version"], 2)
            finally:
                first.db.close()
                second.db.close()

    def test_cost_visibility_and_role_denial(self) -> None:
        data = fixture()
        cases = {c["id"]: c for c in data["cases"]}
        non_finance = buildings.view(data, cases, "SYN-B1", data["staff"][0])
        self.assertTrue(non_finance["costs_restricted"])
        self.assertNotIn("12000", json.dumps(non_finance))
        for role in ("Contractor", "Mystery"):
            with self.assertRaises(PermissionError):
                buildings.view(data, cases, "SYN-B1", {"role": role})

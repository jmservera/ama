"""Unmocked scoped service behavior and unverified consultation provenance."""

import copy
import json
import os
import tempfile
import unittest
from collections.abc import Callable
from datetime import datetime
from importlib import import_module
from pathlib import Path
from typing import Any
from unittest.mock import patch

from building_fixture import fixture, hold
from dataset import (
    DATA,
    RESIDENT_BINDINGS,
    supplied_appointment_fixture,
    supplied_contract_fixture,
    supplied_resident_fixture,
)
from zava_forward.core.procurement import CONSULTATION_STATUSES
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, GateError, Store


class JsonConsultation(unittest.TestCase):
    sql = False
    mssql = False

    def make_store(self) -> Any:
        if self.mssql:
            return import_module("test_mssqlstore").factory(
                str(self.path), str(self.path.with_suffix(".sqlite"))
            )
        factory: Any = SqlStore if self.sql else Store
        if self.sql:
            return factory(str(self.path), str(self.path.with_suffix(".sqlite")))
        return factory(str(self.path))

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        for case in data["cases"]:
            supplied_resident_fixture(case)
        self.path.write_text(json.dumps(data))
        if self.mssql:
            import_module("test_mssqlstore").wipe()
        self.store = self.make_store()
        if self.sql:
            self.addCleanup(self.store.db.close)
        self.manager, self.recorder = data["staff"][1], data["staff"][0]
        self.pid = self.store.create_package(
            self.manager,
            "SYN consultation",
            "2026-01-01",
            "2099-12-31",
            "Loft",
            "SYN-CONTRACT",
            "SYN-1",
        )
        self.source = supplied_contract_fixture(self.store, self.pid, self.manager)
        self.store.set_capacity(
            self.manager, self.pid, "Test Ltd", 5, 5, "SYN commitment", self.source
        )

    def payload(self, status: str = "unknown", version: int = 0) -> dict[str, Any]:
        return dict(
            status=status,
            expected_version=version,
            decided_by="Fictional human Legal adviser (authority unverified)",
            reason="Supplied fictional human decision, not a legal conclusion",
            **{
                key: self.source[key] for key in ("source_case_id", "document_id", "source_version")
            },
        )

    def snapshot(self) -> tuple[Any, Any]:
        return copy.deepcopy(self.store.data["procurement"]), list(self.store.audit_entries())

    def historical(self, state: str = "Issued") -> str:
        """Import an explicit historical order, with no consultation approval or guard patch."""
        with self.store.lock:
            package = self.store._package(self.pid)
            authority = copy.deepcopy(
                self.store.staff[self.manager["email"]]["contract_authorities"][0]
            )
            appointments = (
                [dict(outcome="Booked", date="2099-02-02", by="Pam Lead", at="2026-01-01")]
                if state in ("Appointed", "Completed")
                else []
            )
            version = dict(
                version=1,
                scope="SYN historic scope",
                scope_version=1,
                resident_bindings=copy.deepcopy(RESIDENT_BINDINGS),
                issued_by="Pam Lead",
                issuer_email=self.manager["email"],
                authority=authority,
                contract_ref=package["contract_ref"],
                contract_version="SYN-1",
                capacity_version=1,
                state=state,
                appointments=appointments,
                issued_at="2026-01-01",
                reason="Historical import",
            )
            self.store._proc()["work_orders"] = [
                dict(
                    id="WO-HIST",
                    package=self.pid,
                    case_id="ZF-3",
                    contractor="Test Ltd",
                    state=state,
                    versions=[version],
                    appointments=appointments,
                    history=[],
                    corrections=[],
                )
            ]
            self.store.save()
        return "WO-HIST"

    def test_new_and_legacy_default_unknown(self) -> None:
        row = self.store.list_packages(self.manager)[0]
        self.assertEqual(row["consultation_status"], "unknown")
        self.assertEqual(row["consultation_history"], [])
        with self.store.lock:
            package = self.store._package(self.pid)
            package.pop("consultation_status")
            package.pop("consultation_history")
            self.store.save()
        self.assertEqual(
            self.store.list_packages(self.manager)[0]["consultation_status"], "unknown"
        )
        self.store.issue_work_order(
            self.manager, self.pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS
        )

    def test_all_supplied_statuses_retain_provenance_and_never_clear(self) -> None:
        for version, status in enumerate(CONSULTATION_STATUSES):
            self.store.record_consultation(self.manager, self.pid, self.payload(status, version))
            row = self.store.list_packages(self.manager)[0]
            record = row["consultation_history"][-1]
            self.assertEqual(record["status"], status)
            self.assertEqual(record["version"], version + 1)
            self.assertEqual(record["authority_status"], "Unverified")
            self.assertEqual(record["recorded_by"]["email"], self.manager["email"])
            self.assertEqual(record["decided_by"], self.payload()["decided_by"])
            self.assertEqual(record["contract_version"], "SYN-1")
            self.assertEqual(record["scope_version"], 1)
            self.assertEqual(
                record["content_sha256"],
                self.store.cases[self.source["source_case_id"]]["documents"][-1]["content_sha256"],
            )
            self.assertIsNotNone(datetime.fromisoformat(record["recorded_at"]).utcoffset())
            self.assertEqual(row["consultation_status"], "unknown")
            before = self.snapshot()
            with self.assertRaisesRegex(ValueError, "Consultation status is unknown"):
                self.store.require_consultation_clear(self.store._package(self.pid))
            self.assertEqual(self.snapshot(), before)
        reopened = self.make_store()
        if self.sql:
            self.addCleanup(reopened.db.close)
        self.assertEqual(
            reopened.list_packages(self.manager), self.store.list_packages(self.manager)
        )
        self.assertTrue(reopened.verify_audit())

    def test_bad_payload_and_forged_identity_leave_no_record(self) -> None:
        before = self.snapshot()
        for payload in (
            None,
            {},
            dict(self.payload(), status="approved"),
            dict(self.payload(), expected_version=True),
            dict(self.payload(), expected_version=-1),
            dict(self.payload(), decided_by=" "),
            dict(self.payload(), reason="x" * 301),
            dict(self.payload(), recorded_by=self.manager),
            dict(self.payload(), authority_status="Approved"),
        ):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                self.store.record_consultation(self.manager, self.pid, payload)
            self.assertEqual(self.snapshot(), before)
        for actor in (self.recorder, dict(self.manager, name="Forged")):
            with self.assertRaises(PermissionError):
                self.store.record_consultation(actor, self.pid, self.payload())
            self.assertEqual(self.snapshot(), before)

    def test_stale_record_version_is_atomic(self) -> None:
        self.store.record_consultation(self.manager, self.pid, self.payload())
        before = self.snapshot()
        with self.assertRaises(ConflictError):
            self.store.record_consultation(self.manager, self.pid, self.payload("complete"))
        self.assertEqual(self.snapshot(), before)
        second = self.make_store()
        if self.sql:
            self.addCleanup(second.db.close)
        with self.assertRaises(ConflictError):
            second.record_consultation(self.manager, self.pid, self.payload("not_applicable"))

    def test_source_version_generated_scan_and_bytes_are_checked(self) -> None:
        cid, did = self.source["source_case_id"], self.source["document_id"]
        with self.assertRaisesRegex(ValueError, "source/version"):
            self.store.record_consultation(
                self.manager, self.pid, dict(self.payload(), source_version="missing")
            )
        for change in (dict(generated=True), dict(scan=dict(status="pending"))):
            with self.store.lock:
                doc = next(d for d in self.store.cases[cid]["documents"] if d["id"] == did)
                original = copy.deepcopy(doc)
                doc.update(change)
                self.store.save()
            before = self.snapshot()
            with self.assertRaisesRegex(ValueError, "source/version"):
                self.store.record_consultation(self.manager, self.pid, self.payload())
            self.assertEqual(self.snapshot(), before)
            with self.store.lock:
                doc = next(d for d in self.store.cases[cid]["documents"] if d["id"] == did)
                doc.clear()
                doc.update(original)
                self.store.save()
        self.store.docstore.put(cid, did, b"SYN mutated bytes", "text/plain")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            self.store.record_consultation(self.manager, self.pid, self.payload())
        self.assertEqual(self.snapshot(), before)

    def test_ordinary_service_lifecycle_does_not_require_consultation_clearance(self) -> None:
        s, u = self.store, self.manager
        s.record_consultation(u, self.pid, self.payload("complete"))
        wid = s.issue_work_order(u, self.pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS)
        s.reissue_work_order(u, wid, "SYN revised", "Human request", RESIDENT_BINDINGS)
        supplied_appointment_fixture(s, u, wid)
        s.record_wo_appointment(u, wid, "Booked", "2099-01-01")
        s.advance(u, "ZF-3")
        self.assertEqual(s.detail("ZF-3")["stage"], "Install booked")
        s.complete_work_order(u, wid, "SYN factual completion")
        s.correct_work_order(u, wid, "SYN correction", resident_bindings=RESIDENT_BINDINGS)
        self.assertEqual(s._work_order(wid)["state"], "Issued")
        self.assertEqual(s.list_packages(u)[0]["consultation_status"], "unknown")
        self.assertEqual(
            s.list_packages(u)[0]["consultation_history"][0]["authority_status"], "Unverified"
        )
        self.assertTrue(s.verify_audit())

    def test_explicit_dependent_scope_stays_held_without_spreading_clearance(self) -> None:
        s, u = self.store, self.manager
        wid = s.issue_work_order(u, self.pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS)
        supplied_appointment_fixture(s, u, wid)
        s.record_wo_appointment(u, wid, "Booked", "2099-01-01")
        with s.lock:
            building = fixture()["buildings"][0]
            building["works"] = []
            building["costs"] = []
            dependency = dict(
                hold(),
                label="SYN consultation-dependent work awaiting human review",
                status="Unknown",
                case_ids=["ZF-3"],
                package_ids=[self.pid],
            )
            building["holds"] = [dependency]
            s.data["buildings"] = [building]
            for cid in ("ZF-2", "ZF-3"):
                s._case(cid)["building_id"] = building["id"]
            s._case("ZF-2")["funding_ok"] = True
            s.save()
        for version, status in enumerate(("complete", "not_applicable")):
            s.record_consultation(u, self.pid, self.payload(status, version))
            operations: tuple[Callable[[], Any], ...] = (
                lambda: s.issue_work_order(
                    u, self.pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS
                ),
                lambda: s.reissue_work_order(u, wid, "SYN", "SYN change", RESIDENT_BINDINGS),
                lambda: s.record_wo_appointment(u, wid, "Booked", "2099-01-01"),
                lambda: s.advance(u, "ZF-3"),
            )
            for index, operation in enumerate(operations):
                with self.subTest(status=status, operation=index):
                    before, cases = self.snapshot(), copy.deepcopy(s.cases)
                    with self.assertRaisesRegex(GateError, "consultation-dependent"):
                        operation()
                    self.assertEqual(self.snapshot(), before)
                    self.assertEqual(s.cases, cases)
        s.complete_work_order(u, wid, "SYN historical completion")
        before = self.snapshot()
        with self.assertRaisesRegex(GateError, "consultation-dependent"):
            s.correct_work_order(u, wid, "SYN correction", resident_bindings=RESIDENT_BINDINGS)
        self.assertEqual(self.snapshot(), before)
        sibling = s.issue_work_order(u, self.pid, "ZF-2", resident_bindings=RESIDENT_BINDINGS)
        supplied_appointment_fixture(s, u, sibling)
        s.record_wo_appointment(u, sibling, "Booked", "2099-01-01")
        s.advance(u, "ZF-2")
        self.assertEqual(s.detail("ZF-2")["stage"], "Install booked")
        self.assertEqual(s.list_packages(u)[0]["consultation_status"], "unknown")
        self.assertTrue(s.verify_audit())

    def test_package_operations_retain_the_casewide_final_advance_hold(self) -> None:
        s, u = self.store, self.manager
        with s.lock:
            building = fixture()["buildings"][0]
            building["works"] = []
            building["costs"] = []
            building["holds"] = [
                dict(
                    hold(),
                    label="SYN consultation-dependent work awaiting human review",
                    status="Unknown",
                    case_ids=["ZF-3"],
                    package_ids=[self.pid],
                )
            ]
            s.data["buildings"] = [building]
            s._case("ZF-3")["building_id"] = building["id"]
            s.save()
        other = s.create_package(
            u, "SYN other", "2026-01-01", "2099-12-31", "Loft", "SYN-OTHER", "SYN-1"
        )
        source = supplied_contract_fixture(s, other, u)
        s.set_capacity(u, other, "Test Ltd", 5, 5, "SYN commitment", source)
        order = s.issue_work_order(u, other, "ZF-3", resident_bindings=RESIDENT_BINDINGS)
        s.reissue_work_order(u, order, "SYN revised", "SYN change", RESIDENT_BINDINGS)
        supplied_appointment_fixture(s, u, order)
        s.record_wo_appointment(u, order, "Booked", "2099-01-01")
        s.require_booked_capacity(s.cases["ZF-3"])
        before, cases = self.snapshot(), copy.deepcopy(s.cases)
        with self.assertRaisesRegex(GateError, "consultation-dependent"):
            s.advance(u, "ZF-3")
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(s.cases, cases)
        self.assertEqual(len(s._proc()["work_orders"]), 1)
        self.assertEqual(s.list_packages(u)[0]["consultation_status"], "unknown")
        self.assertEqual(len(s.list_packages(u)[1]["consultation_history"]), 0)
        self.assertTrue(s.verify_audit())

    def test_positive_claim_mutations_cannot_mint_authority(self) -> None:
        self.store.record_consultation(self.manager, self.pid, self.payload("complete"))
        with self.store.lock:
            package = self.store._package(self.pid)
            package["consultation_status"] = "complete"
            package["consultation_history"][-1]["authority_status"] = "Approved"
            package["scope_version"] = 2
            package["contract_version"] = "SYN-mutated"
            self.store.save()
        self.assertEqual(
            self.store.list_packages(self.manager)[0]["consultation_status"], "unknown"
        )
        with self.assertRaisesRegex(ValueError, "Consultation status is unknown"):
            self.store.require_consultation_clear(self.store._package(self.pid))

    def test_nonbinding_historical_recording_remains_available(self) -> None:
        self.historical("Appointed")
        self.store.record_wo_appointment(self.manager, "WO-HIST", "No access")
        self.assertEqual(self.store.list_work_orders(self.manager)[0]["state"], "Issued")
        self.historical("Appointed")
        supplied_appointment_fixture(self.store, self.manager, "WO-HIST")
        self.store.complete_work_order(self.manager, "WO-HIST", "Historical completion evidence")
        self.assertEqual(self.store.list_work_orders(self.manager)[0]["state"], "Completed")
        self.historical()
        self.store.withdraw_work_order(self.manager, "WO-HIST", "No authority to confirm")
        self.assertEqual(self.store.list_work_orders(self.manager)[0]["state"], "Withdrawn")
        self.assertTrue(self.store.verify_audit())

    def test_failed_save_leaves_no_record_or_success_audit(self) -> None:
        before = self.snapshot()
        with patch.object(self.store, "save", side_effect=RuntimeError("SYN write fault")):
            with self.assertRaisesRegex(RuntimeError, "SYN write fault"):
                self.store.record_consultation(self.manager, self.pid, self.payload())
        self.assertEqual(self.snapshot(), before)
        reopened = self.make_store()
        if self.sql:
            self.addCleanup(reopened.db.close)
        self.assertEqual(reopened.data["procurement"], before[0])
        self.assertEqual(list(reopened.audit_entries()), before[1])

    def test_writer_rechecks_source_procurement_and_recorder(self) -> None:
        if not self.sql:
            self.skipTest("SQL writer dependency checks")
        save = self.store._proc_save
        for dependency in ("source", "procurement", "recorder"):
            with self.subTest(dependency=dependency):
                before = self.snapshot()
                original_actor = copy.deepcopy(self.store.staff[self.manager["email"]])

                def changed(
                    *args: Any,
                    dependency: str = dependency,
                    before: tuple[Any, Any] = before,
                    **kwargs: Any,
                ) -> Any:
                    if dependency == "source":
                        self.store.db.execute(
                            "UPDATE cases SET rowversion=rowversion+1 WHERE id=?",
                            (self.source["source_case_id"],),
                        )
                    elif dependency == "procurement":
                        body = json.dumps(before[0], sort_keys=True)
                        self.store.db.execute(
                            "UPDATE meta SET value=? WHERE key='procurement'", (body,)
                        )
                    else:
                        actor = copy.deepcopy(self.store.staff[self.manager["email"]])
                        actor["name"] = "SYN changed recorder"
                        self.store.db.execute(
                            "UPDATE staff SET body=? WHERE email=?",
                            (json.dumps(actor), self.manager["email"]),
                        )
                    return save(*args, **kwargs)

                with patch.object(self.store, "_proc_save", side_effect=changed):
                    with self.assertRaises((ConflictError, PermissionError)):
                        self.store.record_consultation(self.manager, self.pid, self.payload())
                self.assertEqual(self.snapshot(), before)
                if dependency == "recorder":
                    self.store.db.execute(
                        "UPDATE staff SET body=? WHERE email=?",
                        (json.dumps(original_actor), self.manager["email"]),
                    )


class SqlConsultation(JsonConsultation):
    sql = True


@unittest.skipUnless(os.environ.get("ZF_TEST_MSSQL") == "1", "needs task-owned SQL Server")
class MssqlConsultation(SqlConsultation):
    mssql = True

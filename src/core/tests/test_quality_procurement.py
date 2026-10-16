import copy
import json
import os
import tempfile
import unittest
from pathlib import Path

import dataset
from zava_forward.core.quality import CHECKLISTS, checklist_for
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

STAFF = [dict(code="RLO-01", name="Sam Example", email="sam@example.test", role="Resident Liaison Officer"),
         dict(code="PM-01", name="Pam Lead", email="pam@example.test", role="Retrofit Programme Manager"),
         dict(code="QI-01", name="Quin Inspect", email="quin@example.test", role="Quality Inspector"),
         dict(code="QI-02", name="Quil Other", email="quil@example.test", role="Quality Inspector"),
         dict(code="CON-01", name="Kim Builder", email="kim@example.test", role="Contractor", contractor="Test Ltd")]
SAM, PAM, QUIN, QUIL = STAFF[:4]
EVIDENCE = {lab: "seen and photographed" for lab in checklist_for("Loft insulation")["items"]}


class Flows:
    def make(self, data, tmp):
        raise NotImplementedError

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = copy.deepcopy(dataset.DATA)
        d["staff"] = STAFF
        for c in d["cases"][:2]:
            dataset.supplied_resident_fixture(c)
        self.store = self.make(d, self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def actions(self):
        return [e["action"] for e in self.store.audit_entries()]

    def rec(self, cid="ZF-1"):
        return self.store.detail(cid)["quality"][0]

    def submit(self, user=SAM, cid="ZF-1", by="Install Team"):
        return self.store.submit_quality(user, cid, "Loft insulation", by, "Installer", EVIDENCE, context_revision=1)

    # ---- quality acceptance
    def test_submit_needs_positive_evidence_for_every_check(self):
        partial = dict(EVIDENCE)
        partial.pop(next(iter(partial)))
        with self.assertRaises(ValueError):
            self.store.submit_quality(SAM, "ZF-1", "Loft insulation", "Install Team", "Installer", partial)
        with self.assertRaises(ValueError):
            self.store.submit_quality(SAM, "ZF-1", "Not a measure", "Install Team", "Installer", EVIDENCE)
        with self.assertRaises(ValueError):
            self.store.submit_quality(SAM, "ZF-1", "Loft insulation", "Install Team", "Made up", EVIDENCE)
        self.submit()
        r = self.rec()
        self.assertEqual((r["state"], r["checklist_version"]), ("Submitted", CHECKLISTS["Loft insulation"]["version"]))
        with self.assertRaises(ValueError):
            self.submit()
        self.assertIn("quality_submitted", self.actions())

    def test_never_auto_accepts_and_accepter_must_be_independent(self):
        self.submit(user=QUIN, by="Install Team")
        self.assertEqual(self.rec()["state"], "Submitted")
        with self.assertRaises(PermissionError):
            self.store.accept_quality(QUIN, "ZF-1", 0)
        with self.assertRaises(PermissionError):
            self.store.accept_quality(SAM, "ZF-1", 0)
        self.store.submit_quality(QUIL, "ZF-2", "Loft insulation", "Quil Other", "Our own inspection", EVIDENCE, context_revision=1)
        with self.assertRaises(PermissionError):
            self.store.accept_quality(QUIL, "ZF-2", 0)
        self.store.accept_quality(PAM, "ZF-2", 0)
        self.store.accept_quality(QUIL, "ZF-1", 0, "All good")
        self.assertEqual(self.rec()["state"], "Accepted")
        self.assertEqual(self.rec()["accepted_by"], "Quil Other")
        self.assertEqual(self.actions().count("quality_accepted"), 2)

    def test_installer_name_blocks_acceptance(self):
        self.submit(user=SAM, by="Quin Inspect")
        with self.assertRaises(PermissionError):
            self.store.accept_quality(QUIN, "ZF-1", 0)

    def test_return_fix_reinspect_handover_aftercare(self):
        self.submit()
        with self.assertRaises(ValueError):
            self.store.return_quality(QUIN, "ZF-1", 0, "Gap at eaves", "", "")
        with self.assertRaises(PermissionError):
            self.store.return_quality(SAM, "ZF-1", 0, "Gap", "Gap", "Test Ltd")
        self.store.return_quality(QUIN, "ZF-1", 0, "Gap at eaves", "Insulation blocks vent", "Test Ltd")
        self.assertEqual(self.rec()["defect"]["owner"], "Test Ltd")
        for bad in (lambda: self.store.accept_quality(QUIN, "ZF-1", 0), lambda: self.store.hand_over_quality(SAM, "ZF-1", 0, "x", True),
                    lambda: self.store.reinspect_quality(QUIN, "ZF-1", 0, "pass")):
            with self.assertRaises(ValueError):
                bad()
        self.store.record_fix(SAM, "ZF-1", 0, "Test Ltd fitter")
        self.assertEqual(self.rec()["state"], "Fixed, awaiting reinspection")
        self.store.reinspect_quality(QUIN, "ZF-1", 0, "fail", "Still blocked")
        self.assertEqual((self.rec()["state"], len(self.rec()["defects"])), ("Returned", 2))
        self.store.record_fix(SAM, "ZF-1", 0, "Test Ltd fitter")
        with self.assertRaises(PermissionError):
            self.store.reinspect_quality(SAM, "ZF-1", 0, "pass")
        self.store.reinspect_quality(QUIL, "ZF-1", 0, "pass")
        with self.assertRaises(ValueError):
            self.store.hand_over_quality(SAM, "ZF-1", 0, "Guarantee given", False)
        with self.assertRaises(ValueError):
            self.store.add_aftercare(SAM, "ZF-1", 0, "Too early")
        self.store.hand_over_quality(SAM, "ZF-1", 0, "Guarantee and guide given", True)
        self.store.add_aftercare(SAM, "ZF-1", 0, "Resident called: all fine")
        r = self.rec()
        self.assertEqual((r["state"], len(r["aftercare"]), r["handover"]["resident_told"]), ("Handed over", 1, True))
        self.assertEqual([h["to_state"] for h in r["history"]][:3], ["Submitted", "Returned", "Fixed, awaiting reinspection"])
        for a in ("quality_returned", "quality_fixed", "quality_handover", "quality_aftercare"):
            self.assertIn(a, self.actions())
        self.assertTrue(self.store.verify_audit())

    def test_cannot_skip_states(self):
        self.submit()
        with self.assertRaises(ValueError):
            self.store.hand_over_quality(SAM, "ZF-1", 0, "x", True)
        with self.assertRaises(ValueError):
            self.store.record_fix(SAM, "ZF-1", 0, "x")
        self.store.accept_quality(QUIL, "ZF-1", 0)
        with self.assertRaises(ValueError):
            self.store.return_quality(QUIN, "ZF-1", 0, "r", "d", "o")

    # ---- procurement and capacity
    def package(self, committed=1, offered=3):
        pid = self.store.create_package(PAM, "Wave 1 install", "2026-01-01", "2099-12-31", "Loft and wall measures", "CALL-OFF-7")
        self.store.set_capacity(PAM, pid, "Test Ltd", offered, committed, "Signed resource plan RP-1" if committed else "")
        return pid

    def test_package_validation_and_roles(self):
        with self.assertRaises(PermissionError):
            self.store.create_package(SAM, "x", "2026-01-01", "2026-02-01", "s", "r")
        with self.assertRaises(ValueError):
            self.store.create_package(PAM, "x", "2026-03-01", "2026-02-01", "s", "r")
        with self.assertRaises(ValueError):
            self.store.create_package(PAM, "x", "soon", "2026-02-01", "s", "r")
        with self.assertRaises(ValueError):
            self.store.create_package(PAM, "x", "2026-01-01", "2026-02-01", "s", "")
        pid = self.package()
        self.store.rescope_package(PAM, pid, "Loft only", "Wall measures moved")
        p = self.store.list_packages(PAM)[0]
        self.assertEqual((p["scope_version"], len(p["scope_history"]), p["contract_ref"]), (2, 2, "CALL-OFF-7"))

    def test_committed_capacity_needs_evidence_and_limits_work_orders(self):
        pid = self.store.create_package(PAM, "P", "2026-01-01", "2099-12-31", "s", "R")
        with self.assertRaises(ValueError):
            self.store.set_capacity(PAM, pid, "Test Ltd", 3, 2, "")
        with self.assertRaises(ValueError):
            self.store.set_capacity(PAM, pid, "Test Ltd", 1, 2, "x")
        with self.assertRaises(ValueError):
            self.store.set_capacity(PAM, pid, "Nobody Ltd", 1, 1, "x")
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 0)
        with self.assertRaises(ValueError):
            self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 1, "Signed plan")
        self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        with self.assertRaises(ValueError):
            self.store.issue_work_order(PAM, pid, "ZF-2", resident_bindings=dataset.RESIDENT_BINDINGS)
        row = self.store.list_packages(PAM)[0]["capacity"][0]
        self.assertEqual((row["offered"], row["committed"], row["in_use"], row["headroom"], row["unevidenced"]), (3, 1, 1, 0, 2))
        with self.assertRaises(ValueError):
            self.store.set_capacity(PAM, pid, "Test Ltd", 3, 0, "")

    def test_work_order_lifecycle_versions_and_audit(self):
        pid = self.package(committed=2)
        wid = self.store.issue_work_order(PAM, pid, "ZF-1", "Loft to 270mm", resident_bindings=dataset.RESIDENT_BINDINGS)
        with self.assertRaises(PermissionError):
            self.store.issue_work_order(SAM, pid, "ZF-2")
        with self.assertRaises(ValueError):
            self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        for bad in (lambda: self.store.complete_work_order(PAM, wid), lambda: self.store.correct_work_order(PAM, wid, "x", resident_bindings=dataset.RESIDENT_BINDINGS),
                    lambda: self.store.record_wo_appointment(PAM, wid, "Weird")):
            with self.assertRaises(ValueError):
                bad()
        self.store.record_wo_appointment(PAM, wid, "Booked", "2099-02-02")
        self.store.record_wo_appointment(PAM, wid, "No access")
        self.store.record_wo_appointment(PAM, wid, "Booked", "2099-02-03")
        self.store.reissue_work_order(PAM, wid, "Loft to 300mm", "Design changed", resident_bindings=dataset.RESIDENT_BINDINGS)
        self.store.complete_work_order(PAM, wid, "Done")
        with self.assertRaises(ValueError):
            self.store.reissue_work_order(PAM, wid, "x", "y")
        self.store.correct_work_order(PAM, wid, "Hatch not sealed", resident_bindings=dataset.RESIDENT_BINDINGS)
        w = self.store.list_work_orders(PAM)[0]
        self.assertEqual((w["state"], w["version"], w["scope"], len(w["corrections"])), ("Issued", 3, "Loft to 300mm", 1))
        self.assertTrue(all(v["issued_by"] == "Pam Lead" for v in w["versions"]))
        self.store.withdraw_work_order(PAM, wid, "Resident declined")
        with self.assertRaises(ValueError):
            self.store.record_wo_appointment(PAM, wid, "Booked", "2099-03-03")
        for a in ("package_created", "capacity_recorded", "workorder_issued", "workorder_appointment", "workorder_reissued",
                  "workorder_completed", "workorder_corrected", "workorder_withdrawn"):
            self.assertIn(a, self.actions())
        self.assertTrue(self.store.verify_audit())

    def test_contractor_sees_only_own_work_orders_without_reason(self):
        pid = self.package(committed=2)
        self.store.cases["ZF-1"]["resident"].update(adjustment="SEEDED-REASON", priority_support=True)
        self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        mine = self.store.list_work_orders(STAFF[4])
        self.assertEqual(len(mine), 1)
        self.assertTrue(mine[0]["needs_notice"])
        self.assertNotIn("SEEDED-REASON", json.dumps(mine))
        self.assertNotIn("issued_by", mine[0])
        self.assertEqual(self.store.list_work_orders(dict(STAFF[4], contractor="Other Ltd")), [])

    def test_state_survives_reload(self):
        pid = self.package()
        self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        self.submit()
        again = self.reopen()
        self.assertEqual(len(again.list_work_orders(PAM)), 1)
        self.assertEqual(again.detail("ZF-1")["quality"][0]["state"], "Submitted")


class JsonFlows(Flows, unittest.TestCase):
    def make(self, data, tmp):
        self.path = Path(tmp) / "zavaforward.json"
        self.path.write_text(json.dumps(data))
        return Store(str(self.path))

    def reopen(self):
        return Store(str(self.path))


class SqlFlows(Flows, unittest.TestCase):
    def make(self, data, tmp):
        self.path = Path(tmp) / "zavaforward.json"
        self.path.write_text(json.dumps(data))
        self.db = os.path.join(tmp, "pw.sqlite")
        return SqlStore(str(self.path), self.db)

    def reopen(self):
        return SqlStore(str(self.path), self.db)

    def test_two_processes_see_procurement_changes(self):
        other = self.reopen()
        pid = self.package()
        self.assertEqual(len(other.list_packages(PAM)), 1)
        other.set_capacity(PAM, pid, "Test Ltd", 5, 2, "More evidence")
        self.assertEqual(self.store.list_packages(PAM)[0]["capacity"][0]["committed"], 2)

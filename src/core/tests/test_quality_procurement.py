import copy
import json
import os
import tempfile
import unittest
from contextlib import nullcontext
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import dataset
from zava_forward.core.quality import CHECKLISTS, checklist_for
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from zava_forward.core.store import ConflictError, GateError

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
        self.store.record_fix(SAM, "ZF-1", 0, "Test Ltd fitter", "SYN eaves photo 1")
        self.assertEqual(self.rec()["state"], "Fixed, awaiting reinspection")
        self.store.reinspect_quality(QUIN, "ZF-1", 0, "fail", "Still blocked")
        self.assertEqual((self.rec()["state"], len(self.rec()["defects"])), ("Returned", 2))
        self.store.record_fix(SAM, "ZF-1", 0, "Test Ltd fitter", "SYN eaves photo 2")
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

    def quality_calls(self, actor):
        return [
            lambda: self.submit(actor),
            lambda: self.store.accept_quality(actor, "ZF-1", 0),
            lambda: self.store.return_quality(actor, "ZF-1", 0, "SYN", "SYN", "SYN"),
            lambda: self.store.record_fix(actor, "ZF-1", 0, "SYN", "SYN photo"),
            lambda: self.store.reinspect_quality(actor, "ZF-1", 0, "pass", "SYN inspection"),
            lambda: self.store.hand_over_quality(actor, "ZF-1", 0, "SYN guide", True),
            lambda: self.store.add_aftercare(actor, "ZF-1", 0, "SYN call"),
        ]

    def test_quality_current_actor_all_writes(self):
        self.submit()
        before, audit = copy.deepcopy(self.store.cases["ZF-1"]), list(self.store.audit_entries())
        for actor in (dict(QUIN, email="unknown@example.test"), dict(QUIN, code="forged"),
                      dict(QUIN, role="Retrofit Programme Manager"), STAFF[4]):
            for call in self.quality_calls(actor):
                with self.assertRaises(PermissionError):
                    call()
                self.assertEqual(self.store.cases["ZF-1"], before)
                self.assertEqual(list(self.store.audit_entries()), audit)
        if hasattr(self.store, "db"):
            self.store.db.execute("UPDATE staff SET body=? WHERE email=?",
                                 (json.dumps(dict(QUIN, role="Contractor")), QUIN["email"]))
        else:
            self.store.staff[QUIN["email"]] = dict(QUIN, role="Contractor")
        for call in self.quality_calls(QUIN):
            with self.assertRaises(PermissionError):
                call()
        self.assertEqual(self.store.cases["ZF-1"], before)

    def register(self, actor):
        if hasattr(self.store, "db"):
            self.store.db.execute("INSERT INTO staff (email, body) VALUES (?,?)", (actor["email"], json.dumps(actor)))
        self.store.staff[actor["email"]] = actor

    def test_quality_identity_history(self):
        submitter = dict(QUIN, oid="SYN-original")
        if hasattr(self.store, "db"):
            self.store.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(submitter), QUIN["email"]))
        self.store.staff[QUIN["email"]] = submitter
        self.submit(submitter)
        for key in ("name", "code", "oid"):
            alias = dict(QUIL, email=f"syn-{key}@example.test", **{key: submitter[key]})
            self.register(alias)
            with self.assertRaises(PermissionError):
                self.store.accept_quality(alias, "ZF-1", 0)
        email_alias = dict(submitter, name="SYN renamed", code="SYN recoded", oid="SYN changed")
        if hasattr(self.store, "db"):
            self.store.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(email_alias), submitter["email"]))
        self.store.staff[submitter["email"]] = email_alias
        with self.assertRaises(PermissionError):
            self.store.accept_quality(email_alias, "ZF-1", 0)
        if hasattr(self.store, "db"):
            self.store.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(submitter), submitter["email"]))
        self.store.staff[submitter["email"]] = submitter
        self.store.return_quality(QUIL, "ZF-1", 0, "SYN", "SYN gap", "SYN team")
        self.store.record_fix(QUIL, "ZF-1", 0, "SYN first fitter", "SYN photo 1")
        self.store.reinspect_quality(PAM, "ZF-1", 0, "fail", "SYN still open")
        self.store.record_fix(SAM, "ZF-1", 0, "SYN second fitter", "SYN photo 2")
        with self.assertRaises(PermissionError):
            self.store.accept_quality(QUIL, "ZF-1", 0)
        self.store.reinspect_quality(PAM, "ZF-1", 0, "pass", "SYN independent inspection")
        self.assertEqual(self.rec()["state"], "Accepted")
        # Legacy records still resolve their recorded contributor, without trusting caller labels.
        self.submit(cid="ZF-2", user=submitter)
        with self.store.lock:
            self.store._case("ZF-2")["quality"][0].pop("participants", None)
            self.store.save()
        alias = dict(QUIL, email="syn-legacy@example.test", code=QUIN["code"])
        self.register(alias)
        with self.assertRaises(PermissionError):
            self.store.accept_quality(alias, "ZF-2", 0)
        with self.store.lock:
            rec = self.store._case("ZF-2")["quality"][0]
            rec.update(recorded_by="SYN unknown recorder", recorded_by_code="SYN unknown code")
            self.store.save()
        with self.assertRaisesRegex(PermissionError, "identity is unknown"):
            self.store.accept_quality(PAM, "ZF-2", 0)

    def test_quality_remediation_and_reinspection(self):
        self.submit()
        for result in ("pass", "fail"):
            with self.assertRaises(ValueError):
                self.store.reinspect_quality(QUIL, "ZF-1", 0, result, "SYN")
        self.store.return_quality(QUIN, "ZF-1", 0, "SYN", "SYN gap", "SYN team")
        before, audit = copy.deepcopy(self.rec()), list(self.store.audit_entries())
        for note in ("", " \t "):
            with self.assertRaises(ValueError):
                self.store.record_fix(SAM, "ZF-1", 0, "SYN fitter", note)
            self.assertEqual(self.rec(), before)
            self.assertEqual(list(self.store.audit_entries()), audit)
        self.store.record_fix(SAM, "ZF-1", 0, "SYN fitter", "SYN corrected vent/photo v2")
        self.assertEqual(self.rec()["defect"]["remediation_evidence"], "SYN corrected vent/photo v2")
        with self.store.lock:
            self.store._case("ZF-1")["quality"][0]["defect"].pop("remediation_evidence")
            self.store.save()
        with self.assertRaises(ValueError):
            self.store.accept_quality(QUIL, "ZF-1", 0)

    def test_quality_legacy_repeated_recorders(self):
        self.submit()
        self.store.return_quality(QUIL, "ZF-1", 0, "SYN gap", "SYN defect", "SYN team")
        self.store.record_fix(QUIN, "ZF-1", 0, "SYN fitter 1", "SYN photo 1")
        self.store.reinspect_quality(PAM, "ZF-1", 0, "fail", "SYN still open")
        self.store.record_fix(SAM, "ZF-1", 0, "SYN fitter 2", "SYN photo 2")
        with self.store.lock:
            self.store._case("ZF-1")["quality"][0].pop("participants", None)
            self.store.save()
        alias = dict(QUIL, name="SYN earlier recorder alias", email="syn-earlier@example.test", code=QUIN["code"])
        self.register(alias)
        with self.assertRaisesRegex(PermissionError, "Someone independent"):
            self.store.accept_quality(alias, "ZF-1", 0)
        with self.assertRaisesRegex(PermissionError, "Someone independent"):
            self.store.accept_quality(QUIN, "ZF-1", 0)
        self.store.reinspect_quality(PAM, "ZF-1", 0, "pass", "SYN independent review")
        self.assertEqual(self.rec()["state"], "Accepted")

    def test_quality_indices(self):
        self.submit()
        before, audit = copy.deepcopy(self.rec()), list(self.store.audit_entries())
        for idx in (-1, "-1", 0.5, True, None, "0.0", 99):
            with self.assertRaises(ValueError):
                self.store.accept_quality(QUIL, "ZF-1", idx)
            self.assertEqual(self.rec(), before)
            self.assertEqual(list(self.store.audit_entries()), audit)

    def test_quality_replacement_dependencies(self):
        self.submit()
        self.store.accept_quality(QUIL, "ZF-1", 0)
        baseline = copy.deepcopy(self.store.cases["ZF-1"])
        for handed, legacy in ((False, False), (True, False), (True, True), (False, True)):
            with self.subTest(handed=handed, legacy=legacy):
                with self.store.lock:
                    c = self.store._case("ZF-1")
                    c.clear()
                    c.update(copy.deepcopy(baseline))
                    self.store.save()
                if handed:
                    self.store.hand_over_quality(SAM, "ZF-1", 0, "SYN guide 1", True)
                    self.store.add_aftercare(SAM, "ZF-1", 0, "SYN prior call")
                with self.store.lock:
                    c = self.store._case("ZF-1")
                    if legacy:
                        c["quality"].append(copy.deepcopy(c["quality"][0]))
                        if not handed:
                            c["quality"][0]["state"] = "Handed over"
                            c["quality"][0]["handover"] = dict(by="SYN", note="SYN legacy guide", resident_told=True)
                    sibling = copy.deepcopy(c["quality"][0])
                    sibling["measure"] = "Wall insulation"
                    c["quality"].append(sibling)
                    self.store.save()
                before = copy.deepcopy(self.store.cases["ZF-1"])
                old_count = len(before["quality"]) - 1
                idx = self.submit()
                records = self.store.cases["ZF-1"]["quality"]
                for old in range(old_count):
                    self.assertEqual(records[old]["state"], "Superseded")
                    self.assertIsNone(records[old]["handover"])
                    self.assertNotIn("accepted_by", records[old])
                    self.assertEqual(records[old]["items"], before["quality"][old]["items"])
                    self.assertEqual(records[old]["aftercare"], before["quality"][old]["aftercare"])
                    self.assertEqual(records[old]["history"][:-1], before["quality"][old]["history"])
                    self.assertEqual(records[old]["superseded_by"], idx)
                    for call in (
                        lambda: self.store.accept_quality(QUIL, "ZF-1", old),
                        lambda: self.store.hand_over_quality(SAM, "ZF-1", old, "SYN", True),
                        lambda: self.store.add_aftercare(SAM, "ZF-1", old, "SYN"),
                    ):
                        with self.assertRaises(ValueError):
                            call()
                self.assertEqual(records[old_count], before["quality"][old_count])
                for key in ("finance", "grants", "funding"):
                    self.assertEqual(self.store.cases["ZF-1"].get(key), before.get(key))
                with self.assertRaises(ValueError):
                    self.store.hand_over_quality(SAM, "ZF-1", idx, "SYN", True)
                self.store.accept_quality(QUIL, "ZF-1", idx)
                self.store.hand_over_quality(SAM, "ZF-1", idx, "SYN new guide", True)
                again = self.reopen()
                if hasattr(again, "db"):
                    self.addCleanup(again.db.close)
                self.assertEqual(again.detail("ZF-1")["quality"][-1]["state"], "Handed over")
                self.assertTrue(again.verify_audit())

    def test_quality_resident_and_safety(self):
        self.store.submit_quality(SAM, "ZF-1", "Loft insulation", "SYN", "Installer", EVIDENCE)
        with self.assertRaises(GateError):
            self.store.accept_quality(QUIL, "ZF-1", 0)
        with self.store.lock:
            rec = self.store._case("ZF-1")["quality"][0]
            rec["resident_binding"] = dict(measure="Loft insulation", context_revision=99)
            self.store.save()
        with self.assertRaises(GateError):
            self.store.accept_quality(QUIL, "ZF-1", 0)
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["quality"][0]["resident_binding"]["context_revision"] = 1
            c["hazards"].append(dict(released=False, owner="SYN Safety"))
            self.store.save()
        with self.assertRaises(GateError):
            self.store.accept_quality(QUIL, "ZF-1", 0)

    # ---- procurement and capacity
    def test_package_requires_contract_version_before_creation(self):
        before = copy.deepcopy(self.store.data.get("procurement"))
        audit = list(self.store.audit_entries())
        for kwargs in ({}, {"contract_version": ""}, {"contract_version": " \t "}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaisesRegex(ValueError, "contract or call-off version"):
                    self.store.create_package(PAM, "SYN", "2026-01-01", "2099-12-31", "Loft", "SYN", **kwargs)
                self.assertEqual(self.store.data.get("procurement"), before)
                self.assertEqual(list(self.store.audit_entries()), audit)
        pid = self.store.create_package(PAM, "SYN", "2026-01-01", "2099-12-31", "Loft", "SYN", " SYN-1 ")
        self.assertEqual(self.store._package(pid)["contract_version"], "SYN-1")

    def package(self, committed=1, offered=3):
        pid = self.store.create_package(PAM, "Wave 1 install", "2026-01-01", "2099-12-31", "Loft and wall measures", "CALL-OFF-7", "SYN-1")
        self.details = dataset.supplied_contract_fixture(self.store, pid, PAM)
        self.store.set_capacity(PAM, pid, "Test Ltd", offered, committed, "SYN signed commitment RP-1" if committed else "", self.details)
        return pid

    def test_package_validation_and_roles(self):
        with self.assertRaises(PermissionError):
            self.store.create_package(SAM, "x", "2026-01-01", "2026-02-01", "s", "r", "SYN-1")
        with self.assertRaises(ValueError):
            self.store.create_package(PAM, "x", "2026-03-01", "2026-02-01", "s", "r", "SYN-1")
        with self.assertRaises(ValueError):
            self.store.create_package(PAM, "x", "soon", "2026-02-01", "s", "r", "SYN-1")
        with self.assertRaises(ValueError):
            self.store.create_package(PAM, "x", "2026-01-01", "2026-02-01", "s", "", "SYN-1")
        pid = self.package()
        self.store.rescope_package(PAM, pid, "Loft only", "Wall measures moved")
        p = self.store.list_packages(PAM)[0]
        self.assertEqual((p["scope_version"], len(p["scope_history"]), p["contract_ref"]), (2, 2, "CALL-OFF-7"))

    def test_committed_capacity_needs_evidence_and_limits_work_orders(self):
        pid = self.store.create_package(PAM, "P", "2026-01-01", "2099-12-31", "s", "R", "SYN-1")
        details = dataset.supplied_contract_fixture(self.store, pid, PAM)
        with self.assertRaises(ValueError):
            self.store.set_capacity(PAM, pid, "Test Ltd", 3, 2, "")
        with self.assertRaises(ValueError):
            self.store.set_capacity(PAM, pid, "Test Ltd", 1, 2, "x")
        with self.assertRaises(ValueError):
            self.store.set_capacity(PAM, pid, "Nobody Ltd", 1, 1, "x")
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 0)
        with self.assertRaises(ValueError):
            self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 1, "Signed plan", details)
        self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        with self.assertRaises(ValueError):
            self.store.issue_work_order(PAM, pid, "ZF-2", resident_bindings=dataset.RESIDENT_BINDINGS)
        row = self.store.list_packages(PAM)[0]["capacity"][0]
        self.assertEqual((row["offered"], row["committed"], row["in_use"], row["headroom"], row["unevidenced"]), (3, 1, 1, 0, 2))
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 0, "")
        self.assertEqual(self.store.list_packages(PAM)[0]["capacity"][0]["headroom"], -1)

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
        self.assertEqual((w["state"], w["version"], w["scope"], len(w["corrections"])), ("Issued", 7, "Loft to 300mm", 1))
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
        with self.assertRaises(PermissionError):
            self.store.list_work_orders(dict(STAFF[4], contractor="Other Ltd"))

    def test_state_survives_reload(self):
        pid = self.package()
        self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        self.submit()
        again = self.reopen()
        self.assertEqual(len(again.list_work_orders(PAM)), 1)
        self.assertEqual(again.detail("ZF-1")["quality"][0]["state"], "Submitted")

    def test_imported_numeric_capacity_is_not_evidenced(self):
        pid = self.package()
        with self.store.lock:
            self.store._package(pid)["capacity"]["Test Ltd"]["evidence"] = ""
            self.store.save()
        with self.assertRaises(ValueError):
            self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)

    def test_booking_outside_package_period_is_refused(self):
        pid = self.package()
        wid = self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        with self.assertRaises(ValueError):
            self.store.record_wo_appointment(PAM, wid, "Booked", "2100-01-01")

    def test_every_order_change_has_a_version(self):
        pid = self.package()
        wid = self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        self.store.record_wo_appointment(PAM, wid, "Booked", "2099-02-02")
        self.store.record_wo_appointment(PAM, wid, "No access")
        self.store.withdraw_work_order(PAM, wid, "Synthetic withdrawal")
        self.assertEqual([v["version"] for v in self.store.list_work_orders(PAM)[0]["versions"]], [1, 2, 3, 4])

    def test_advance_without_evidenced_booked_order_is_refused(self):
        with self.assertRaises(ValueError):
            self.store.advance(PAM, "ZF-3")

    def test_evidence_matrix_fails_closed_without_success_events(self):
        pid = self.package()
        mutations = [
            {"unit": "crew-days"}, {"status": "Offered"}, {"source_version": "missing"},
            {"document_id": "missing"}, {"case_ids": ["MISSING"]}, {"source_date": "2099-01-01"},
            {"reviewed_on": "2099-01-01"}, {"reviewed_on": (date.today() - timedelta(days=8)).isoformat()},
            {"valid_from": "2025-01-01"}, {"valid_to": "2100-01-01"},
        ]
        for delta in mutations:
            with self.subTest(delta=delta):
                before = copy.deepcopy(self.store.data["procurement"])
                audit = list(self.store.audit_entries())
                with self.assertRaises(ValueError):
                    self.store.set_capacity(PAM, pid, "Test Ltd", 3, 1, "SYN", dict(self.details, **delta))
                self.assertEqual(self.store.data["procurement"], before)
                self.assertEqual(list(self.store.audit_entries()), audit)
        for bad in (True, 1.5, "1.5", None):
            with self.assertRaises(ValueError):
                self.store.set_capacity(PAM, pid, "Test Ltd", 3, bad, "SYN", self.details)

    def test_named_authority_is_not_a_role_or_caller_claim(self):
        pid = self.package()
        actor = self.store.staff[PAM["email"]]
        original = copy.deepcopy(actor)
        for delta in ({"revoked": True}, {"actions": ["withdraw"]}, {"suppliers": ["Other Ltd"]},
                      {"contract_version": "wrong"}, {"contract_ref": "WRONG"}, {"reference": ""},
                      {"scope_versions": [99]}, {"scope_versions": [True]}, {"valid_from": "2099-01-01"},
                      {"valid_to": "2026-01-01"}):
            with self.subTest(delta=delta):
                actor["contract_authorities"] = [dict(original["contract_authorities"][0], **delta)]
                if hasattr(self.store, "db"):
                    self.store.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(actor), actor["email"]))
                with self.assertRaises((PermissionError, ValueError)):
                    self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        actor.update(original)
        if hasattr(self.store, "db"):
            self.store.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(actor), actor["email"]))
        for spoof in (dict(PAM, name="Unregistered"), dict(PAM, email="system@example.test")):
            with self.assertRaises(PermissionError):
                self.store.issue_work_order(spoof, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)

    def test_full_quota_progression_snapshots_and_detached_reads(self):
        pid = self.package()
        wid = self.store.issue_work_order(PAM, pid, "ZF-3", resident_bindings=dataset.RESIDENT_BINDINGS)
        with self.assertRaises(ValueError):
            self.store.advance(PAM, "ZF-3")
        self.store.record_wo_appointment(PAM, wid, "Booked", "2099-01-01")
        self.store.advance(PAM, "ZF-3")
        self.store.reissue_work_order(PAM, wid, "SYN revised wording", "SYN reason", dataset.RESIDENT_BINDINGS)
        self.store.complete_work_order(PAM, wid)
        self.store.correct_work_order(PAM, wid, "SYN correction", resident_bindings=dataset.RESIDENT_BINDINGS)
        rows = self.store.list_work_orders(PAM)
        versions = rows[0]["versions"]
        self.assertEqual([v["version"] for v in versions], [1, 2, 3, 4, 5])
        self.assertEqual([v["state"] for v in versions], ["Issued", "Appointed", "Appointed", "Completed", "Issued"])
        self.assertEqual(versions[0]["appointments"], [])
        self.assertTrue(all(v["issuer_email"] == PAM["email"] and v["authority"]["reference"] == "SYN-DELEGATION" for v in versions))
        versions[0]["scope"] = "MUTATION"
        self.assertNotEqual(self.store.list_work_orders(PAM)[0]["versions"][0]["scope"], "MUTATION")
        self.assertEqual(self.store.list_packages(PAM)[0]["capacity"][0]["in_use"], 1)
        self.store.withdraw_work_order(PAM, wid, "SYN authorized release")
        self.assertEqual(self.store.list_packages(PAM)[0]["capacity"][0]["in_use"], 0)

    def test_capacity_dates_scope_source_and_deficit_invalidate_progression(self):
        pid = self.package()
        wid = self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 0)
        with self.assertRaises(ValueError):
            self.store.record_wo_appointment(PAM, wid, "Booked", "2099-01-01")
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 1, "SYN", self.details)
        self.store.rescope_package(PAM, pid, "SYN new scope", "SYN")
        with self.assertRaises(ValueError):
            self.store.reissue_work_order(PAM, wid, "", "SYN", dataset.RESIDENT_BINDINGS)
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 1, "SYN", self.details)
        self.store.docstore.put(self.details["source_case_id"], self.details["document_id"], b"changed", "text/plain")
        with self.assertRaises(ValueError):
            self.store.reissue_work_order(PAM, wid, "", "SYN", dataset.RESIDENT_BINDINGS)

    def test_failed_save_restores_order_versions_and_no_success_audit(self):
        pid = self.package()
        wid = self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        before = self.store.list_work_orders(PAM)
        audit = list(self.store.audit_entries())
        with patch.object(self.store, "save", side_effect=OSError("SYN save failure")):
            with self.assertRaises(OSError):
                self.store.withdraw_work_order(PAM, wid, "SYN")
        self.assertEqual(self.store.list_work_orders(PAM), before)
        self.assertEqual(self.reopen().list_work_orders(PAM), before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.store.record_wo_appointment(PAM, wid, "Booked", "2099-01-01")
        # Use the ready home without changing the order's case association.
        with self.store.lock:
            self.store._case("ZF-1").update(stage="Final checks before ordering", funding_ok=True)
            self.store.save()
        audit = list(self.store.audit_entries())
        with patch.object(self.store, "save", side_effect=OSError("SYN save failure")):
            with self.assertRaises(OSError):
                self.store.advance(PAM, "ZF-1")
        self.assertEqual(self.store.detail("ZF-1")["stage"], "Final checks before ordering")
        self.assertEqual(list(self.store.audit_entries()), audit)

    def test_drafts_and_draft_review_never_issue_instructions(self):
        before = copy.deepcopy(self.store.data.get("procurement"))
        self.assertIn("not an instruction", self.store.draft("ZF-1", "update")["note"])
        result = self.store.ai_run(PAM, "ZF-1", "message", "off")
        self.assertEqual(result["instruction_status"], "Not an instruction")
        reviewed = self.store.review_ai(PAM, result["record_id"], "accept")
        self.assertEqual(reviewed["instruction_status"], "Not an instruction")
        self.assertEqual(self.store.data.get("procurement"), before)

    def test_inclusive_review_and_delivery_boundaries(self):
        pid = self.package()
        old = (date.today() - timedelta(days=7)).isoformat()
        details = dict(self.details, source_date=old, reviewed_on=old)
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 1, "SYN", details)
        wid = self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS)
        for when in (details["valid_from"], details["valid_to"]):
            self.store.record_wo_appointment(PAM, wid, "Booked", when)
        with self.assertRaises(ValueError):
            self.store.record_wo_appointment(PAM, wid, "Booked", "2100-01-01")
        future = dict(self.details, valid_from="2099-01-01")
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 1, "SYN", future)
        with self.assertRaises(ValueError):
            self.store.reissue_work_order(PAM, wid, "", "SYN", dataset.RESIDENT_BINDINGS)
        self.store.record_wo_appointment(PAM, wid, "Booked", "2099-01-01")


class JsonFlows(Flows, unittest.TestCase):
    def make(self, data, tmp):
        self.path = Path(tmp) / "zavaforward.json"
        self.path.write_text(json.dumps(data))
        return Store(str(self.path))

    def reopen(self):
        return Store(str(self.path))

    def test_quality_json_failures(self):
        self.submit()
        before, audit = copy.deepcopy(self.rec()), list(self.store.audit_entries())
        for target in ("save", "audit"):
            for after_write in (False, True):
                original = getattr(self.store, target)

                def fail(*args):
                    if after_write:
                        original(*args)
                    raise OSError("SYN failure")

                with patch.object(self.store, target, side_effect=fail):
                    with self.assertRaises(OSError):
                        self.store.accept_quality(QUIL, "ZF-1", 0)
                self.assertEqual(self.rec(), before)
                self.assertEqual(list(self.store.audit_entries()), audit)
                self.assertEqual(self.reopen().detail("ZF-1")["quality"][0], before)
        with patch.object(Store, "save", side_effect=OSError("SYN persistent disk failure")):
            with self.assertLogs("zava_forward.core.quality", level="ERROR"):
                with self.assertRaisesRegex(RuntimeError, "durable outcome may be unknown"):
                    self.store.accept_quality(QUIL, "ZF-1", 0)
        self.assertEqual(self.rec(), before)
        self.assertEqual(list(self.store.audit_entries()), audit)


class SqlFlows(Flows, unittest.TestCase):
    def make(self, data, tmp):
        self.path = Path(tmp) / "zavaforward.json"
        self.path.write_text(json.dumps(data))
        self.db = os.path.join(tmp, "pw.sqlite")
        return SqlStore(str(self.path), self.db)

    def reopen(self):
        return SqlStore(str(self.path), self.db)

    def test_quality_sql_postcommit_refresh(self):
        self.submit()
        store = self.store
        before = copy.deepcopy(store.cases["ZF-1"])
        other = self.reopen()
        self.addCleanup(other.db.close)
        for prefix in (False, True):
            for persistent in (False, True):
                with self.subTest(prefix=prefix, persistent=persistent):
                    with store.lock:
                        c = store._case("ZF-1")
                        c.clear()
                        c.update(copy.deepcopy(before))
                        store.save()
                    audit = list(store.audit_entries())
                    save = store.save

                    class RefreshFault:
                        committed = False
                        failed = False

                        def __init__(self, db):
                            self.db = db

                        def execute(self, sql, args=()):
                            if self.committed and sql.startswith("SELECT value FROM meta") and (persistent or not self.failed):
                                self.failed = True
                                raise OSError("SYN post-commit refresh read")
                            result = self.db.execute(sql, args)
                            if sql == "COMMIT":
                                self.committed = True
                            return result

                        def __getattr__(self, name):
                            return getattr(self.db, name)

                    fault = RefreshFault(store.db)

                    def concurrent_save():
                        with other.lock:
                            other._case("ZF-2")["reason"] = "SYN unrelated completed writer"
                            other.save()
                        save()

                    with store.lock:
                        if prefix:
                            store.audit(SAM["email"], "SYN_committed_prefix", "ZF-1", "SYN once")
                        with patch.object(store, "db", fault), patch.object(store, "save", side_effect=concurrent_save):
                            with self.assertLogs("zava_forward.core.quality", level="ERROR"):
                                with self.assertRaisesRegex(RuntimeError, "committed") as caught:
                                    store.accept_quality(QUIL, "ZF-1", 0)
                            self.assertIsInstance(caught.exception.__cause__, OSError)
                            self.assertFalse(store.local.pending)
                            self.assertFalse(store.local.touched)
                    events = list(store.audit_entries())[len(audit):]
                    self.assertEqual([e["action"] for e in events],
                                     (["SYN_committed_prefix"] if prefix else []) + ["quality_accepted"])
                    again = self.reopen()
                    self.addCleanup(again.db.close)
                    self.assertEqual(again.detail("ZF-1")["quality"][0]["state"], "Accepted")
                    self.assertTrue(again.verify_audit())

    def test_quality_sql_actor_and_stale(self):
        self.submit()
        other = self.reopen()
        self.addCleanup(other.db.close)
        save = self.store.save
        before, audit = copy.deepcopy(self.rec()), list(self.store.audit_entries())
        validate = self.store._validate_safety_clear

        def revoke_in_transaction():
            self.store.db.execute("UPDATE staff SET body=? WHERE email=?",
                                 (json.dumps(dict(QUIL, role="Contractor")), QUIL["email"]))
            from zava_forward.core import stock
            stock.validate_sql(self.store)
            validate()

        with patch.object(self.store, "_validate_safety_clear", side_effect=revoke_in_transaction):
            with self.assertRaises(PermissionError):
                self.store.accept_quality(QUIL, "ZF-1", 0)
        self.assertEqual(self.rec(), before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.store.accept_quality(QUIL, "ZF-1", 0)
        self.store.hand_over_quality(SAM, "ZF-1", 0, "SYN guide", True)
        expected = {}

        def replace_first():
            other.submit_quality(SAM, "ZF-1", "Loft insulation", "SYN", "Installer", EVIDENCE, 1)
            expected["case"] = copy.deepcopy(other.detail("ZF-1")["quality"])
            expected["audit"] = list(other.audit_entries())
            save()

        with patch.object(self.store, "save", side_effect=replace_first):
            with self.assertRaises(ConflictError):
                self.store.add_aftercare(SAM, "ZF-1", 0, "SYN stale writer")
        self.assertEqual(self.store.detail("ZF-1")["quality"], expected["case"])
        self.assertEqual(list(self.store.audit_entries()), expected["audit"])
        again = self.reopen()
        self.addCleanup(again.db.close)
        self.assertEqual(again.detail("ZF-1")["quality"], expected["case"])

    def test_quality_sql_failures(self):
        self.submit()
        store = self.store
        original_audit = store._append_audit
        for failure in ("pre-save", "case-write", "audit-insert"):
            for recovery in ("healthy", "early", "persistent"):
                with self.subTest(failure=failure, recovery=recovery):
                    before, audit = copy.deepcopy(self.rec()), list(store.audit_entries())
                    original = OSError("SYN original quality failure")

                    class DbFault:
                        armed = False
                        reads = 0

                        def __init__(self, db):
                            self.db = db

                        def execute(self, sql, args=()):
                            if self.armed and sql.startswith(("SELECT rowversion, body FROM cases", "SELECT value FROM meta")):
                                if recovery == "persistent" or recovery == "early" and self.reads == 0:
                                    self.reads += 1
                                    raise OSError("SYN recovery read")
                            result = self.db.execute(sql, args)
                            if failure == "case-write" and sql.startswith("UPDATE cases SET rowversion"):
                                self.armed = True
                                raise original
                            return result

                        def __getattr__(self, name):
                            return getattr(self.db, name)

                    fault = DbFault(store.db)

                    def fail_save():
                        fault.armed = True
                        raise original

                    def fail_audit(entries):
                        original_audit(entries)
                        if any(e[1] == "quality_accepted" for e in entries):
                            fault.armed = True
                            raise original

                    with store.lock:
                        store.audit(SAM["email"], "SYN_legitimate_prefix", "ZF-1", "SYN keep")
                        with patch.object(store, "db", fault), \
                                patch.object(store, "save", side_effect=fail_save) if failure == "pre-save" else patch.object(store, "_append_audit", side_effect=fail_audit):
                            with self.assertLogs("zava_forward.core.stock", level="ERROR") if recovery != "healthy" else nullcontext():
                                with self.assertRaises(OSError) as caught:
                                    store.accept_quality(QUIL, "ZF-1", 0)
                            self.assertIs(caught.exception, original)
                            self.assertEqual(store.cases["ZF-1"]["quality"][0], before)
                            self.assertFalse(store.local.touched)
                            self.assertEqual([e[1] for e in store.local.pending], ["SYN_legitimate_prefix"])
                            if recovery != "healthy":
                                self.assertTrue(fault.reads)
                                self.assertTrue(getattr(original, "__notes__", []))
                    self.assertEqual([e["action"] for e in store.audit_entries()],
                                     [e["action"] for e in audit] + ["SYN_legitimate_prefix"])
                    self.assertEqual(self.rec(), before)
                    self.assertEqual(store.lock.depth, 0)
                    self.assertTrue(store.verify_audit())
                    again = self.reopen()
                    self.addCleanup(again.db.close)
                    self.assertEqual(again.detail("ZF-1")["quality"][0], before)

    def test_recovery_read_failure_keeps_original_error_and_disarms_failed_work(self):
        pid = self.package()
        wid = self.store.issue_work_order(PAM, pid, "ZF-3", resident_bindings=dataset.RESIDENT_BINDINGS)
        self.store.record_wo_appointment(PAM, wid, "Booked", "2099-01-01")
        store = self.store
        for operation in ("withdraw", "advance"):
            for failure in ("pre-save", "transaction", "cancellation"):
                for persistent in (False, True):
                    with self.subTest(operation=operation, failure=failure, persistent=persistent):
                        before = copy.deepcopy(store.data["procurement"])
                        cases = copy.deepcopy(store.cases)
                        audit = list(store.audit_entries())
                        original = (GateError(["SYN refusal"]) if failure == "transaction"
                                    else KeyboardInterrupt("SYN cancellation") if failure == "cancellation"
                                    else OSError("SYN original save failure"))

                        class RecoveryReadFault:
                            armed = False
                            failures = 0

                            def __init__(self, db):
                                self.db = db

                            def execute(self, sql, args=()):
                                if self.armed and sql.startswith(("SELECT rowversion, body FROM cases", "SELECT value FROM meta")) and (persistent or not self.failures):
                                    self.failures += 1
                                    raise OSError("SYN recovery read failure")
                                return self.db.execute(sql, args)

                            def __getattr__(self, name):
                                return getattr(self.db, name)

                        fault = RecoveryReadFault(store.db)

                        def fail():
                            fault.armed = True
                            raise original

                        target = "save" if failure == "pre-save" else "_validate_safety_clear"
                        logger = "zava_forward.core.procurement" if operation == "withdraw" else "zava_forward.core.store"
                        with patch.object(store, "db", fault), patch.object(store, target, side_effect=fail):
                            with self.assertLogs(logger, level="ERROR"), self.assertRaises(type(original)) as caught:
                                if operation == "withdraw":
                                    store.withdraw_work_order(PAM, wid, "SYN refused withdrawal")
                                else:
                                    store.advance(PAM, "ZF-3")
                            self.assertIs(caught.exception, original)
                            self.assertTrue(original.__notes__)
                            self.assertGreaterEqual(fault.failures, 1)
                            self.assertEqual(store.local.pending, [])
                            self.assertEqual(store.local.touched, set())
                            self.assertIsNone(store.local.procurement_validation)
                            self.assertIsNone(store._proc_context)
                            self.assertEqual(store.lock.depth, 0)
                            self.assertEqual(store.data["procurement"], before)
                            self.assertEqual(store.cases, cases)
                            if persistent:
                                with self.assertRaisesRegex(OSError, "recovery read failure"):
                                    store.detail("ZF-3")
                        store.save()
                        self.assertEqual(list(store.audit_entries()), audit)
                        self.assertEqual(store.list_work_orders(PAM), self.reopen().list_work_orders(PAM))
                        self.assertEqual(store.detail("ZF-3")["stage"], "Final checks before ordering")
                        self.assertTrue(store.verify_audit())
        store.withdraw_work_order(PAM, wid, "SYN legitimate retry after recovery")
        order = next(w for w in self.reopen().list_work_orders(PAM) if w["id"] == wid)
        self.assertEqual(order["state"], "Withdrawn")
        self.assertEqual(len(order["versions"]), 3)

    def test_two_processes_see_procurement_changes(self):
        other = self.reopen()
        pid = self.package()
        self.assertEqual(len(other.list_packages(PAM)), 1)
        other.set_capacity(PAM, pid, "Test Ltd", 5, 2, "More evidence", self.details)
        self.assertEqual(self.store.list_packages(PAM)[0]["capacity"][0]["committed"], 2)

    def race(self, first, second):
        other = self.reopen()
        save = self.store.save
        expected = {}

        def interleave():
            second(other)
            expected["orders"] = other.list_work_orders(PAM)
            expected["audit"] = list(other.audit_entries())
            save()

        with patch.object(self.store, "save", side_effect=interleave):
            with self.assertRaises((ConflictError, PermissionError, ValueError)):
                first()
        self.assertEqual(self.store.list_work_orders(PAM), expected["orders"])
        self.assertEqual(list(self.store.audit_entries()), expected["audit"])
        again = self.reopen()
        self.assertEqual(again.list_work_orders(PAM), expected["orders"])
        self.assertTrue(again.verify_audit())

    def test_concurrent_last_slot_keeps_only_winning_order_and_audit(self):
        pid = self.package()
        self.race(
            lambda: self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS),
            lambda other: other.issue_work_order(PAM, pid, "ZF-2", resident_bindings=dataset.RESIDENT_BINDINGS),
        )
        self.assertEqual(len(self.store.list_work_orders(PAM)), 1)

    def test_advance_dependency_races_restore_case_and_never_confirm(self):
        for change in ("withdraw", "rescope", "loss"):
            with self.subTest(change=change):
                pid = self.package(offered=3)
                wid = self.store.issue_work_order(PAM, pid, "ZF-3", resident_bindings=dataset.RESIDENT_BINDINGS)
                self.store.record_wo_appointment(PAM, wid, "Booked", "2099-01-01")
                operations = {
                    "withdraw": lambda other: other.withdraw_work_order(PAM, wid, "SYN"),
                    "rescope": lambda other: other.rescope_package(PAM, pid, "SYN scope", "SYN"),
                    "loss": lambda other: other.set_capacity(PAM, pid, "Test Ltd", 3, 0),
                }
                self.race(lambda: self.store.advance(PAM, "ZF-3"), operations[change])
                self.assertEqual(self.store.detail("ZF-3")["stage"], "Final checks before ordering")
                if change != "withdraw":
                    self.store.withdraw_work_order(PAM, wid, "SYN cleanup release")

    def test_commit_authority_revocation_is_rechecked(self):
        pid = self.package()

        def revoke(other):
            actor = copy.deepcopy(other.staff[PAM["email"]])
            actor["contract_authorities"] = []
            other.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(actor), PAM["email"]))

        self.race(
            lambda: self.store.issue_work_order(PAM, pid, "ZF-1", resident_bindings=dataset.RESIDENT_BINDINGS),
            revoke,
        )

    def test_source_change_at_commit_and_audit_failure_roll_back(self):
        pid = self.package()

        def replace_source(other):
            with other.lock:
                other._case(self.details["source_case_id"])["documents"][-1]["version"] = "2"
                other.save()

        self.race(
            lambda: self.store.issue_work_order(PAM, pid, "ZF-2", resident_bindings=dataset.RESIDENT_BINDINGS),
            replace_source,
        )
        self.details = dataset.supplied_contract_fixture(self.store, pid, PAM)
        self.store.set_capacity(PAM, pid, "Test Ltd", 3, 1, "SYN", self.details)
        before = self.store.list_work_orders(PAM)
        audit = list(self.store.audit_entries())
        with patch.object(self.store, "_append_audit", side_effect=OSError("SYN audit failure")):
            with self.assertRaises(OSError):
                self.store.issue_work_order(PAM, pid, "ZF-2", resident_bindings=dataset.RESIDENT_BINDINGS)
        self.assertEqual(self.store.list_work_orders(PAM), before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.store.issue_work_order(PAM, pid, "ZF-2", resident_bindings=dataset.RESIDENT_BINDINGS)

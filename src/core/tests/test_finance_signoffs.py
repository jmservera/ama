import copy
import json
import os
import tempfile
import unittest
from pathlib import Path

import dataset
from zava_forward.core import controls
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import GateError, Store


def person(code, role, **kw):
    return dict(code=code, name=f"{role} {code}", email=f"{code.lower()}@example.test", role=role, **kw)


STAFF = [person("GEO-1", "Grants and Evidence Officer"), person("PM-1", "Retrofit Programme Manager"),
         person("PM-2", "Retrofit Programme Manager"), person("QI-1", "Quality Inspector"),
         person("RC-1", "Retrofit Coordinator"), person("RC-2", "Retrofit Coordinator"),
         person("BSL-1", "Building Safety Liaison"), person("RLO-1", "Resident Liaison Officer"),
         person("RLO-2", "Resident Liaison Officer"), person("CON-1", "Contractor", contractor="Test Ltd")]
U = {s["code"]: s for s in STAFF}
EVIDENCE = None


def lines(qty=10, amount=1000, ms="MS-1", measure="Loft insulation"):
    return [dict(measure=measure, quantity=qty, amount=amount, milestone_ref=ms)]


class Flows:
    def make(self, data, tmp):
        raise NotImplementedError

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = copy.deepcopy(dataset.DATA)
        d["staff"] = copy.deepcopy(STAFF)
        from test_grant_lifecycle_controls import designate
        for i in (1, 2):
            d["staff"][i] = designate(d["staff"][i])
            for permission in d["staff"][i]["financial_authority"]["permissions"]:
                permission["route"] = "Warm Homes"
        d["cases"][0]["measures"] = "Loft insulation, Cavity wall"
        self.store = self.make(d, self.tmp.name)
        self.geo, self.pm1, self.pm2 = U["GEO-1"], U["PM-1"], U["PM-2"]

    def tearDown(self):
        self.tmp.cleanup()

    def actions(self):
        return [e["action"] for e in self.store.audit_entries()]

    def fin(self, user, action, **kw):
        self.store.finance_action(user, "ZF-1", dict(action=action, **kw))

    def invoice(self, **kw):
        self.fin(self.geo, "invoice_receive", supplier="Test Ltd", work_order="WO-1", ref="INV-100", lines=lines(), **kw)
        return self.store.detail("ZF-1")["finance"]["invoices"][-1]["id"]

    def funded(self, budget=10000, commit=5000):
        self.fin(self.geo, "budget_propose", amount=budget)
        self.fin(self.pm1, "budget_approve")
        self.fin(self.geo, "commit_raise", supplier="Test Ltd", contract="C-1", work_order="WO-1", measure="Loft insulation", amount=commit, quantity=10)
        self.fin(self.pm1, "commit_approve", id="COM-1")

    # FR-018
    def test_budget_and_commitment_need_a_different_approver(self):
        self.fin(self.geo, "budget_propose", amount="10,000")
        with self.assertRaises(PermissionError):
            self.fin(self.geo, "budget_approve")
        with self.assertRaises(PermissionError):
            self.fin(U["RLO-1"], "budget_propose", amount=1)
        with self.assertRaises(ValueError):
            self.fin(self.geo, "commit_raise", supplier="A", contract="C", work_order="W", measure="Loft insulation", amount=1, quantity=1)
        self.fin(self.pm1, "budget_approve")
        self.fin(self.geo, "commit_raise", supplier="Test Ltd", contract="C-1", work_order="WO-1", measure="Loft insulation", amount=6000, quantity=10)
        with self.assertRaises(PermissionError):
            self.fin(self.geo, "commit_approve", id="COM-1")
        with self.assertRaises(ValueError):
            self.fin(self.geo, "commit_raise", supplier="Test Ltd", contract="C-1", work_order="WO-2", measure="x", amount=4001, quantity=1)
        self.fin(self.pm2, "commit_approve", id="COM-1")
        f = self.store.detail("ZF-1")["finance"]
        self.assertEqual((f["budget"]["status"], f["commitments"][0]["status"], f["commitments"][0]["approved_by"]), ("Approved", "Approved", self.pm2["name"]))
        self.assertIn("finance_budget_approve", self.actions())

    def test_clean_invoice_matches_but_payment_is_never_executed(self):
        self.funded()
        inv = self.invoice()
        self.fin(self.geo, "invoice_match", id=inv)
        i = self.store.detail("ZF-1")["finance"]["invoices"][0]
        self.assertEqual((i["status"], i["exceptions"], i["commitment"]), ("Matched", [], "COM-1"))
        with self.assertRaises(PermissionError):
            self.fin(self.geo, "disposition", id=inv, decision="Accept for payment", note="ok")
        with self.assertRaises(ValueError):
            self.fin(self.pm1, "payment_status", id=inv, status="Paid outside this system")
        self.fin(self.pm2, "disposition", id=inv, decision="Accept for payment", note="Checked")
        with self.assertRaises(PermissionError):
            self.fin(self.pm2, "payment_status", id=inv, status="Paid outside this system")
        self.fin(self.geo, "payment_status", id=inv, status="Awaiting payment run")
        self.fin(self.geo, "payment_status", id=inv, status="Paid outside this system")
        i = self.store.detail("ZF-1")["finance"]["invoices"][0]
        self.assertEqual(i["payment_status"], "Paid outside this system")
        self.assertIn("never makes", i["payment_note"])
        self.assertFalse([a for a in self.actions() if "execute" in a or a == "pay"])

    def test_line_exceptions_and_unknowns_block_a_match(self):
        self.fin(self.geo, "invoice_receive", supplier="Test Ltd", work_order="WO-1", ref="INV-1",
                 lines=lines(qty=12, amount=7000, ms="") + lines(measure="Solar panels"))
        self.fin(self.geo, "invoice_match", id="INV-1")
        i = self.store.detail("ZF-1")["finance"]["invoices"][0]
        codes = {e["code"] for e in i["exceptions"]}
        self.assertTrue({"no_commitment", "no_budget", "no_milestone"} <= codes)
        self.assertEqual(i["status"], "Exception, with Finance")
        self.assertEqual([r["invoice"] for r in self.store.finance_queue(self.pm1)], ["INV-1"])
        self.funded(commit=5000)
        self.fin(self.geo, "invoice_match", id="INV-1")
        i = self.store.detail("ZF-1")["finance"]["invoices"][0]
        codes = {(e["code"], e["line"]) for e in i["exceptions"]}
        self.assertIn(("quantity", 0), codes)
        self.assertIn(("not_in_scope", 1), codes)
        self.assertIn(("over_commitment", 0), codes)
        self.assertIn(("over_commitment", 1), codes)
        with self.assertRaises(ValueError):
            self.fin(self.pm2, "disposition", id="INV-1", decision="Accept for payment", note="x")

    def test_duplicate_reference_and_holds(self):
        self.funded()
        a = self.invoice()
        self.fin(self.geo, "invoice_match", id=a)
        b = self.invoice()
        self.fin(self.geo, "invoice_match", id=b)
        self.assertIn("duplicate", {e["code"] for e in self.store.detail("ZF-1")["finance"]["invoices"][1]["exceptions"]})
        self.fin(self.geo, "hold_place", id=a, reason="Query quantity")
        with self.assertRaises(PermissionError):
            self.fin(self.geo, "hold_release", id=a, note="done")
        with self.assertRaises(ValueError):
            self.fin(self.pm1, "disposition", id=a, decision="Accept for payment", note="x")
        self.fin(self.pm1, "hold_release", id=a, note="Resolved")
        with self.assertRaises(ValueError):
            self.fin(self.pm1, "disposition", id=a, decision="Accept for payment", note="Still duplicated")
        self.fin(self.pm1, "disposition", id=b, decision="Reject and return to provider", note="Duplicate received")
        self.fin(self.pm1, "disposition", id=a, decision="Accept for payment", note="ok")
        self.assertEqual(self.store.detail("ZF-1")["finance"]["invoices"][0]["disposition_by"], self.pm1["name"])

    def test_inputs_and_bulk_are_refused(self):
        for body in (dict(action="budget_propose", amount="abc"), dict(action="budget_propose", amount=-5), dict(action="nope"),
                     dict(action="invoice_receive", supplier="x", work_order="w", ref="r", lines=[])):
            with self.assertRaises(ValueError):
                self.store.finance_action(self.geo, "ZF-1", body)
        for fn, body in ((self.store.finance_action, dict(action="budget_approve")), (self.store.grant_action, dict(action="grant_approve")),
                         (self.store.technical_action, dict(action="signoff_give")), (self.store.resident_action, dict(action="service_close"))):
            for key in controls.BULK_KEYS:
                with self.assertRaises(PermissionError):
                    fn(self.pm1, "ZF-1", dict(body, **{key: ["ZF-1", "ZF-2"]}))

    # FR-019
    def grant(self, user, action, **kw):
        self.store.grant_action(user, "ZF-1", dict(action=action, **kw))

    def test_grant_states_are_distinct_and_need_a_second_person(self):
        self.grant(self.geo, "grant_open", scheme="Warm Homes", source="Notice WH-1")
        with self.assertRaises(PermissionError):
            self.grant(self.geo, "grant_approve", id="GR-1")
        self.grant(self.pm1, "grant_approve", id="GR-1")
        with self.assertRaises(ValueError):
            self.grant(self.geo, "grant_propose", id="GR-1", to="Cash received", source="x", amount=1)
        with self.assertRaises(ValueError):
            self.grant(self.geo, "grant_propose", id="GR-1", to="Award", source="")
        path = [("Award", None), ("Claimable", None), ("Submitted", None), ("Rejected", None), ("Claimable", None), ("Submitted", None),
                ("Accepted", None), ("Cash received", 5000)]
        for to, amount in path:
            self.grant(self.geo, "grant_propose", id="GR-1", to=to, source=f"Evidence for {to}", amount=amount)
            self.grant(self.pm2, "grant_approve", id="GR-1")
        g = self.store.detail("ZF-1")["grants"][0]
        self.assertEqual(g["state"], "Cash received")
        self.assertEqual(g["history"][-1]["amount"], 5000)
        self.assertTrue(all(h["source"] and h["approved_by"] and h["proposed_by"] for h in g["history"]))
        self.assertNotIn("finance", self.store.detail("ZF-1"))

    def test_grants_never_touch_invoices_and_show_in_funding_list(self):
        self.funded()
        inv = self.invoice()
        before = json.dumps(self.store.detail("ZF-1")["finance"])
        self.grant(self.geo, "grant_open", scheme="Warm Homes", source="WH-1")
        self.assertEqual(json.dumps(self.store.detail("ZF-1")["finance"]), before)
        row = next(r for r in self.store.funding_list(self.geo) if r["id"] == "ZF-1")
        self.assertIn("Not recorded", row["grants"])
        self.grant(self.geo, "grant_withdraw", id="GR-1")
        self.assertIsNone(self.store.detail("ZF-1")["grants"][0]["pending"])
        self.assertTrue(inv)

    # FR-013
    def tech(self, user, action, **kw):
        self.store.technical_action(user, "ZF-1", dict(action=action, **kw))

    def sign_all(self):
        self.tech(U["RC-1"], "design_submit", note="Loft and wall")
        self.tech(U["QI-1"], "signoff_give", type="assessment")
        self.tech(U["RC-2"], "signoff_give", type="design")
        self.tech(U["BSL-1"], "signoff_give", type="building")

    def test_technical_stage_lists_missing_items_for_competent_roles(self):
        self.assertEqual(self.store.detail("ZF-1")["technical_missing"], [])
        self.tech(U["RC-1"], "design_submit", note="Loft and wall")
        missing = self.store.detail("ZF-1")["technical_missing"]
        self.assertIn("Quality Inspector", [m["assigned_to"] for m in missing])
        self.assertIn("Grants and Evidence Officer", [m["assigned_to"] for m in missing])
        self.assertTrue([w for w in self.store.detail("ZF-1")["gate"] if w.startswith("Technical stage")])
        with self.assertRaises(PermissionError):
            self.tech(U["RLO-1"], "signoff_give", type="assessment")
        with self.assertRaises(PermissionError):
            self.tech(U["RC-1"], "signoff_give", type="design")
        self.tech(U["QI-1"], "signoff_give", type="assessment")
        with self.assertRaises(PermissionError):
            self.tech(U["QI-1"], "signoff_give", type="design")
        with self.assertRaises(PermissionError):
            self.tech(U["RC-2"], "signoff_give", type="assessment")
        with self.assertRaises(GateError):
            self.tech(self.pm1, "signoff_give", type="coordination")

    def test_design_change_invalidates_only_affected_signoffs(self):
        self.sign_all()
        self.tech(U["RC-1"], "design_change", note="Wall type changed", affects=["design", "building"])
        s = self.store.detail("ZF-1")["technical"]
        self.assertEqual(s["design_version"], 2)
        self.assertEqual({k: v["status"] for k, v in s["signoffs"].items()},
                         {"assessment": "Signed off", "design": "Needs reassessment", "building": "Needs reassessment"})
        with self.assertRaises(ValueError):
            self.tech(U["RC-1"], "design_change", note="x", affects=["assessment"])
        self.tech(U["RC-2"], "signoff_give", type="design")
        self.assertEqual(self.store.detail("ZF-1")["technical"]["signoffs"]["design"]["history"][-1]["status"], "Re-approved")

    def test_return_and_reapproval(self):
        self.sign_all()
        self.tech(U["BSL-1"], "signoff_return", type="building", reason="Ventilation unclear")
        self.assertEqual(self.store.detail("ZF-1")["technical"]["signoffs"]["building"]["status"], "Returned")
        with self.assertRaises(ValueError):
            self.tech(U["BSL-1"], "signoff_return", type="building", reason="")
        self.tech(U["BSL-1"], "signoff_give", type="building", note="Fixed")
        self.assertEqual(self.store.detail("ZF-1")["technical"]["signoffs"]["building"]["status"], "Signed off")

    # FR-014
    def res(self, user, action, **kw):
        if action == "decision_record":
            c = self.store.cases["ZF-1"]
            if not c.get("technical"):
                self.tech(U["RC-1"], "design_submit", note="Synthetic resident design")
            for measure in ("Loft insulation", "Cavity wall"):
                if measure not in c.get("resident_scopes", {}):
                    self.store.resident_action(U["RLO-1"], "ZF-1", dict(
                        action="scope_record", measure=measure, scope="Synthetic scope",
                        design_version=c["technical"]["design_version"], source="Synthetic supplied scope"))
            kw.setdefault("context_revision", 1)
            kw.setdefault("source", "Synthetic supplied resident statement")
        self.store.resident_action(user, "ZF-1", dict(action=action, **kw))

    def decisions(self):
        return {d["measure"]: d for d in self.store.detail("ZF-1")["measure_decisions"]}

    def test_decisions_are_never_inferred_and_are_per_measure(self):
        self.store.log_call(U["RLO-1"], "ZF-1", "Spoke, happy to go ahead", "")
        d = self.decisions()
        self.assertEqual({m: x["status"] for m, x in d.items()}, {"Loft insulation": "Not recorded", "Cavity wall": "Not recorded"})
        self.res(U["RLO-1"], "decision_record", measure="Loft insulation", status="Accepted", answered_by="The resident")
        self.res(U["RLO-1"], "decision_record", measure="Cavity wall", status="Accepted", answered_by="The resident")
        self.res(U["RLO-1"], "decision_record", measure="Cavity wall", status="Paused", answered_by="The resident", note="After the winter")
        self.res(U["RLO-1"], "safe_contact_record", safe_contact_ref="SYN-SAFE", source="Synthetic confirmation")
        self.res(U["RLO-1"], "representative_record", measure="Cavity wall", context_revision=1,
                 representative_ref="Rep on file", status="Confirmed", tasks=["Works decision"], source="Synthetic authority",
                 authority_date="2026-01-01", review_date="2099-01-01", resident_wishes="Record supplied withdrawal",
                 safe_contact_ref="SYN-SAFE")
        self.res(U["RLO-2"], "decision_record", measure="Cavity wall", status="Withdrawn", answered_by="Their representative",
                 representative_ref="Rep on file", note="Resident asked to stop")
        d = self.decisions()
        self.assertEqual(d["Loft insulation"]["status"], "Accepted")
        self.assertEqual(len(d["Loft insulation"]["versions"]), 1)
        self.assertEqual((d["Cavity wall"]["status"], len(d["Cavity wall"]["versions"])), ("Withdrawn", 3))
        for kw in (dict(measure="Loft insulation", status="Accepted"), dict(measure="Solar", status="Accepted", answered_by="The resident"),
                   dict(measure="Loft insulation", status="Maybe", answered_by="The resident"),
                   dict(measure="Loft insulation", status="Paused", answered_by="The resident"),
                   dict(measure="Loft insulation", status="Accepted", answered_by="Their representative")):
            with self.assertRaises(ValueError):
                self.res(U["RLO-1"], "decision_record", **kw)
        with self.assertRaises(PermissionError):
            self.res(U["QI-1"], "decision_record", measure="Loft insulation", status="Accepted", answered_by="The resident")
        self.assertEqual(self.store.detail("ZF-1")["decision"]["status"], "Waiting")

    def test_complaint_route_has_distinct_owners_and_closure(self):
        base = dict(summary="Mess left", desired_outcome="Clean and apology", next_update="2099-01-01")
        with self.assertRaises(ValueError):
            self.res(U["RLO-1"], "service_open", route="Complaint", service_owner="rlo-1@example.test", redress_owner="rlo-1@example.test", **base)
        with self.assertRaises(ValueError):
            self.res(U["RLO-1"], "service_open", route="Complaint", service_owner="con-1@example.test", redress_owner="pm-1@example.test", **base)
        with self.assertRaises(ValueError):
            self.res(U["RLO-1"], "service_open", route="Complaint", service_owner="rlo-1@example.test", redress_owner="pm-1@example.test",
                     accessibility=["Her diagnosis"], **base)
        self.res(U["RLO-1"], "service_open", route="Complaint", service_owner="rlo-1@example.test", redress_owner="pm-1@example.test",
                 accessibility=["Large print"], **base)
        r = self.store.detail("ZF-1")["service_requests"][0]
        self.assertEqual((r["route"], r["redress_owner"], r["accessibility"], r["representative_ref"]),
                         ("Complaint", self.pm1["name"], ["Large print"], "Unknown"))
        with self.assertRaises(ValueError):
            self.res(U["RLO-1"], "service_close", id="SR-1", note="x")
        self.res(U["RLO-1"], "service_update", id="SR-1", status="Resolved", next_update="2099-02-01", note="Cleaned")
        with self.assertRaises(PermissionError):
            self.res(U["RLO-1"], "service_close", id="SR-1", note="done")
        self.res(self.pm1, "service_close", id="SR-1", note="Apology sent")
        self.assertEqual(self.store.detail("ZF-1")["service_requests"][0]["status"], "Closed")
        self.assertEqual(self.store.detail("ZF-1")["measure_decisions"][0]["status"], "Not recorded")

    def test_contractor_and_other_roles_cannot_see_finance(self):
        self.funded()
        self.grant(self.geo, "grant_open", scheme="WH", source="n")
        self.assertNotIn("finance", self.store.detail("ZF-1", U["RLO-1"]))
        self.assertNotIn("grants", self.store.detail("ZF-1", U["QI-1"]))
        self.assertIn("finance", self.store.detail("ZF-1", self.pm1))
        text = json.dumps(self.store.detail("ZF-1", U["CON-1"]))
        for w in ("finance", "grants", "budget", "service_requests"):
            self.assertNotIn(w, text)
        with self.assertRaises(PermissionError):
            self.store.finance_queue(U["RLO-1"])

    def test_chain_intact_and_audited(self):
        self.funded()
        self.sign_all()
        self.res(U["RLO-1"], "decision_record", measure="Loft insulation", status="Waiting", answered_by="The resident")
        self.grant(self.geo, "grant_open", scheme="WH", source="n")
        self.assertTrue({"finance_commit_raise", "technical_signoff_give", "resident_decision_record", "finance_grant_open"} <= set(self.actions()))
        self.assertTrue(self.store.verify_audit())


class JsonFlows(Flows, unittest.TestCase):
    def make(self, data, tmp):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(data))
        return Store(str(p))


class SqlFlows(Flows, unittest.TestCase):
    def make(self, data, tmp):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(data))
        return SqlStore(str(p), os.path.join(tmp, "pw.sqlite"))

    def test_survives_a_restart(self):
        self.funded()
        self.tech(U["RC-1"], "design_submit", note="n")
        again = SqlStore(str(Path(self.tmp.name) / "zavaforward.json"), os.path.join(self.tmp.name, "pw.sqlite"))
        d = again.detail("ZF-1")
        self.assertEqual(d["finance"]["budget"]["status"], "Approved")
        self.assertEqual(d["technical"]["design_version"], 1)

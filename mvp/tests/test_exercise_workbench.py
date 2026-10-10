"""Connected fictional exercise oracles through durable Store and HTTP boundaries."""
from copy import deepcopy
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import threading
import unittest
from unittest.mock import MagicMock, patch
import urllib.error
import urllib.request
import uuid

from properwarm_mvp import forms
from properwarm_mvp.factory import open_store
from properwarm_mvp.server import App, make_handler
from properwarm_mvp.store import GateError

HOME = "EX-HOME-001"
SIBLING = "EX-HOME-002"


class ExerciseWorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.root = Path.cwd() / ".exercise-test-state" / uuid.uuid4().hex
        self.env = patch.dict("os.environ", {"PW_EXERCISE": "1", "PW_STATE": str(self.root),
                                            "PW_STORE": "sqlite", "PW_DOC_STORE": "local",
                                            "AI_ENDPOINT": "https://inherited.invalid"}, clear=True)
        self.env.start()
        self.store = open_store()
        self.users = {u["code"]: u for u in self.store.staff.values()}
        self.pm = self.users["EX-PM-01"]
        self.asset = self.users["EX-PM-02"]
        self.geo = self.users["EX-GEO-01"]
        self.pso = self.users["EX-PSO-01"]
        self.rc = self.users["EX-RC-01"]
        self.rlo = self.users["EX-RLO-01"]
        self.qi = self.users["EX-QI-02"]

    def tearDown(self):
        self.store.db.close()
        self.env.stop()
        shutil.rmtree(self.root)
        try:
            self.root.parent.rmdir()
        except OSError:
            pass

    def act(self, action, *, user=None, home=HOME, **body):
        return self.store.exercise_action(user or self.geo, home, dict(action=action, **body))

    def budget(self):
        self.store.finance_action(self.geo, HOME, dict(action="budget_propose", amount=20000))
        with self.assertRaises(PermissionError):
            self.store.finance_action(self.geo, HOME, dict(action="budget_approve"))
        self.store.finance_action(self.asset, HOME, dict(action="budget_approve"))

    def complete_form(self, kind="competitive", *, correction=None):
        before = set(self.store._case(HOME).get("forms", {}))
        self.act("create-form", form_type=kind)
        fid = (set(self.store._case(HOME)["forms"]) - before).pop()
        draft = self.store._case(HOME)["forms"][fid]
        for sid in list(draft["sources"]):
            self.act("extract", form_id=fid, source_id=sid)
        for field, spec in forms.SCHEMAS[kind]["fields"].items():
            if spec["protected"] or spec["type"] == "calculated_money":
                continue
            current = self.store._case(HOME)["forms"][fid]["fields"][field]
            candidates = [row for row in current["candidates"] if not row["stale"]]
            if not candidates and not spec["required"]:
                continue
            self.assertTrue(candidates, field)
            self.act("select", form_id=fid, field=field, candidate_id=candidates[0]["id"])
            self.act("review", form_id=fid, field=field, review_action="accept",
                     evidence=[], reason=f"Independent supplied {field} source checked")
        self.act("calculate", form_id=fid)
        if correction:
            self.act("review", form_id=fid, field="eligible_cost", review_action="correct",
                     value=correction, unit="GBP", currency="GBP",
                     evidence=[f"{HOME}-FINANCE"], reason="Corrected externally rejected cost evidence")
            self.act("calculate", form_id=fid)
        for field in ("match_budget_approved", "declaration"):
            self.act("human-field", user=self.pm, form_id=fid, field=field, value=True,
                     evidence=[f"{HOME}-HUMAN"], reason="Explicit fictional human statement")
        self.act("attachments", form_id=fid, evidence=[f"{HOME}-FINANCE", "EX-EPC-A"])
        with self.assertRaises(PermissionError):
            self.act("review-pack", user=self.pm, form_id=fid,
                     evidence=[f"{HOME}-FINANCE"], reason="Cannot review own statements")
        self.act("review-pack", user=self.pso, form_id=fid,
                 evidence=[f"{HOME}-FINANCE"], reason="Independent current full pack review")
        self.act("export", form_id=fid)
        return fid

    def event(self, event, fid, *, user=None, **body):
        return self.act("funding-event", user=user, event=event, form_id=fid,
                        export_id="export-1", evidence=f"Fictional external {event} evidence",
                        **body)

    def resolve_epc(self):
        self.act("source-correct", user=self.rc, source_id="EX-EPC-B",
                 raw_text="epc_band: D\n", reason="Source owner resolves supplied fictional conflict")
        self.assertEqual(self.store._case(HOME)["home"]["epc"], "D")

    def test_parser_conflict_exact_invalidation_and_sibling_restart(self):
        self.budget()
        self.act("create-form", form_type="competitive")
        for sid in (f"{HOME}-IDENTITY", "EX-EPC-A", "EX-EPC-B"):
            self.act("extract", form_id="FORM-001", source_id=sid)
        draft = self.store._case(HOME)["forms"]["FORM-001"]
        self.assertEqual(draft["fields"]["epc_band"]["state"], "conflict")
        self.assertEqual({c["value"] for c in draft["fields"]["epc_band"]["candidates"]}, {"D", "E"})
        identity = draft["fields"]["home_ids"]["candidates"][0]["id"]
        self.act("select", form_id="FORM-001", field="home_ids", candidate_id=identity)
        self.act("review", form_id="FORM-001", field="home_ids", review_action="accept",
                 reason="Identity checked", evidence=[])
        self.act("select", form_id="FORM-001", field="epc_band", candidate_id=None)
        with self.assertRaises(ValueError):
            self.act("review", form_id="FORM-001", field="epc_band", review_action="accept",
                     evidence=[], reason="No match is not approval")
        epc = draft["fields"]["epc_band"]["candidates"][1]["id"]
        self.act("select", form_id="FORM-001", field="epc_band", candidate_id=epc)
        self.act("review", form_id="FORM-001", field="epc_band", review_action="accept",
                 evidence=[], reason="Explicit provisional source selection")
        before = deepcopy(self.store._case(HOME)["forms"]["FORM-001"])
        sibling = deepcopy(self.store._case(SIBLING))
        self.resolve_epc()
        after = self.store._case(HOME)["forms"]["FORM-001"]
        self.assertEqual(after["fields"]["home_ids"], before["fields"]["home_ids"])
        self.assertEqual(set(after["last_invalidation"]["fields"]), {"epc_band", "declaration", "signature"})
        self.assertTrue(after["fields"]["epc_band"]["stale"])
        self.assertEqual(self.store._case(SIBLING), sibling)
        self.assertEqual(self.store._case(HOME)["exercise"]["source_history"][0]["raw_text"], "epc_band: E\n")
        self.store.db.close()
        self.store = open_store()
        self.assertEqual(self.store._case(HOME)["forms"]["FORM-001"], after)
        self.assertEqual(self.store._case(SIBLING), sibling)
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_same_home_end_to_end_independent_qa_financial_closure(self):
        self.complete_journey()

    def complete_journey(self, *, pay_handover=True):
        self.budget()
        self.resolve_epc()
        self.act("lifecycle", user=self.pm, target="Assessment")
        self.store.technical_action(self.rc, HOME, dict(action="design_submit", note="Fictional loft scope"))
        for kind in ("EPC", "Survey", "Design", "Consent"):
            self.store.add_document(self.geo, HOME, f"{kind}.txt", kind, f"Fictional {kind} evidence".encode())
        for key, actor in (("assessment", self.qi), ("design", self.users["EX-RC-02"]),
                           ("building", self.users["EX-BSL-01"]), ("coordination", self.pm)):
            self.store.technical_action(actor, HOME, dict(action="signoff_give", type=key, note="Fictional independent review"))
        self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Loft insulation",
            scope="Loft insulation", design_version=1, status="Accepted", answered_by="The resident",
            note="Fictional explicitly supplied choice"))
        self.act("lifecycle", user=self.pm, target="Funding")
        fid = self.complete_form()
        self.assertFalse(self.store._case(HOME)["funding_ok"], "Export must not establish award")
        self.assertEqual(self.store._case(HOME)["exercise"].get("fund_events", []), [])
        self.event("application-submitted", fid)
        with self.assertRaises(PermissionError):
            self.event("application-disposition", fid, disposition="Accepted")
        self.event("application-disposition", fid, user=self.asset, disposition="Accepted")
        self.event("award", fid, amount="7500")
        self.assertTrue(self.store._case(HOME)["funding_ok"])
        self.act("lifecycle", user=self.pm, target="Ready")
        pid = self.store.create_package(self.asset, "Fictional package", "2026-10-01", "2099-12-31",
                                        "Loft insulation", "EX-CALL-OFF-001")
        with self.assertRaises(ValueError):
            self.store.issue_work_order(self.asset, pid, HOME)
        self.store.set_capacity(self.asset, pid, "Imaginary Retrofit Ltd", 1, 1, "Fictional competent crew/material/client capacity")
        wid = self.store.issue_work_order(self.asset, pid, HOME)
        self.store.record_wo_appointment(self.asset, wid, "Booked", "2026-10-20")
        self.act("lifecycle", user=self.pm, target="Installation")
        self.act("milestone", user=self.pm, work_order=wid, milestone="mobilisation", evidence="Verified booked mobilisation")
        self.store.complete_work_order(self.asset, wid, "Fictional provider completion only")
        self.act("lifecycle", user=self.pm, target="Provider completed")
        checks = {item: "Fictional supplied inspection evidence" for item in
                  __import__("properwarm_mvp.quality", fromlist=["CHECKLISTS"]).CHECKLISTS["Loft insulation"]["items"]}
        idx = self.store.submit_quality(self.asset, HOME, "Loft insulation", "Fictional installer", "Provider submission", checks)
        self.act("lifecycle", user=self.pm, target="Independent QA")
        with self.assertRaises(PermissionError):
            self.store.accept_quality(self.asset, HOME, idx, "Cannot self-accept")
        self.store.return_quality(self.qi, HOME, idx, "Missing hatch seal", "Seal defect", "Fictional installer")
        self.store.record_fix(self.asset, HOME, idx, "Fictional installer", "Supplied fix evidence")
        self.store.reinspect_quality(self.qi, HOME, idx, "pass", "Independent reinspection passed")
        self.act("milestone", user=self.pm, work_order=wid, milestone="installation", evidence="Independent acceptance")
        self.store.hand_over_quality(self.qi, HOME, idx, "Fictional guarantees and use information supplied", True)
        self.act("lifecycle", user=self.pm, target="Handover")
        self.act("milestone", user=self.pm, work_order=wid, milestone="handover", evidence="Resident handover evidence")
        claim = self.complete_form("claim")
        self.event("claimable", claim, amount="7500")
        self.event("claim-submitted", claim, amount="7500")
        self.event("claim-disposition", claim, user=self.asset, amount="7500", disposition="Accepted")
        with self.assertRaises(GateError):
            self.act("lifecycle", user=self.pm, target="Financial closure")
        self.event("cash", claim, amount="7500")
        with self.assertRaises(ValueError):
            self.event("cash", claim, amount="0.01")
        self.store.finance_action(self.geo, HOME, dict(action="commit_raise", supplier="Imaginary Retrofit Ltd",
            contract="EX-CALL-OFF-001", work_order=wid, measure="Loft insulation", amount=18000, quantity=1))
        self.store.finance_action(self.asset, HOME, dict(action="commit_approve", id="COM-1"))
        for index, (milestone, amount) in enumerate((("mobilisation", 3600), ("installation", 12600), ("handover", 1800)), 1):
            self.store.finance_action(self.geo, HOME, dict(action="invoice_receive", supplier="Imaginary Retrofit Ltd",
                work_order=wid, ref=f"FICTIONAL-{index}", lines=[dict(measure="Loft insulation", quantity=1,
                amount=amount, milestone_ref=f"{wid}:{milestone}")]))
            invoice = f"INV-{index}"
            self.store.finance_action(self.geo, HOME, dict(action="invoice_match", id=invoice))
            self.store.finance_action(self.asset, HOME, dict(action="disposition", id=invoice,
                decision="Accept for payment", note="Independent exact match"))
            if milestone != "handover" or pay_handover:
                self.store.finance_action(self.geo, HOME, dict(action="payment_status", id=invoice,
                    status="Paid outside this system", evidence=f"Fictional external payment {index}"))
        if not pay_handover:
            return
        self.act("lifecycle", user=self.pm, target="Financial closure")
        c = self.store._case(HOME)
        self.assertEqual(c["exercise"]["lifecycle"], "Financial closure")
        self.assertTrue(c["closed"])
        self.assertEqual([e["event"] for e in c["exercise"]["fund_events"]],
                         ["application-submitted", "application-disposition", "award", "claimable",
                          "claim-submitted", "claim-disposition", "cash"])
        self.assertEqual(c["forms"][fid]["exports"][0]["fields"]["grant_amount"]["value"], "7500.00")
        self.assertEqual(self.store._case(SIBLING)["exercise"]["lifecycle"], "Intake")
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_milestone_return_blocks_payment_and_closure_without_erasing_paid_history(self):
        from properwarm_mvp.finance import match_invoice
        from properwarm_mvp import projection
        self.complete_journey()
        before = deepcopy(self.store._case(HOME))
        invoice = before["finance"]["invoices"][-1]
        ref = invoice["lines"][0]["milestone_ref"]
        wid = invoice["work_order"]
        for scope in ([ref, ref], ["SIBLING-WO:handover"]):
            snapshot = deepcopy(self.store._case(HOME))
            head = self.store.verify_ledger()["head"]
            with self.assertRaises(ValueError):
                self.act("return", user=self.pm, target="Handover", receiver=self.geo["email"],
                    reason="Invalid milestone scope", evidence="Supplied source", next_action="Review",
                    affected_milestones=scope)
            self.assertEqual(self.store._case(HOME), snapshot)
            self.assertEqual(self.store.verify_ledger()["head"], head)
        self.act("return", user=self.pm, target="Handover", receiver=self.geo["email"],
            reason="Supplied retention milestone evidence requires re-review",
            evidence="Fictional later discrepancy", next_action="Independent reviewer verifies current milestone",
            affected_milestones=[ref])
        c = self.store._case(HOME)
        self.assertTrue(c["exercise"]["milestones"][ref]["stale"])
        self.assertEqual(c["exercise"]["milestone_history"][-1]["reference"], ref)
        self.assertEqual(c["finance"]["invoices"], before["finance"]["invoices"])
        self.assertEqual(c["exercise"]["fund_events"], before["exercise"]["fund_events"])
        self.assertEqual(c["quality"], before["quality"])
        self.assertEqual(c["measure_decisions"], before["measure_decisions"])
        for other_ref, milestone in before["exercise"]["milestones"].items():
            if other_ref != ref:
                self.assertEqual(c["exercise"]["milestones"][other_ref], milestone)
        self.assertEqual([e["code"] for e in match_invoice(c, deepcopy(invoice))], ["unaccepted_milestone"])
        for status in ("Awaiting payment run", "Paid outside this system"):
            snapshot = deepcopy(self.store._case(HOME))
            with self.assertRaises(ValueError):
                self.store.finance_action(self.geo, HOME, dict(action="payment_status", id=invoice["id"],
                    status=status, evidence="Must not overwrite old receipt with stale evidence"))
            self.assertEqual(self.store._case(HOME), snapshot)
        with self.assertRaises(GateError):
            self.act("lifecycle", user=self.pm, target="Financial closure")
        for actor in self.users.values():
            projected = self.store.exercise_case(actor, HOME)["case"]
            if not projection.is_contractor(actor) and actor["role"] not in projection.FINANCE_VIEW:
                self.assertNotIn("milestones", projected["exercise"])
                self.assertNotIn("milestone_history", projected["exercise"])
                self.assertNotIn("affected_milestones", projected["exercise"]["returns"][-1])
        with self.assertRaises(PermissionError):
            self.act("milestone", user=self.asset, work_order=wid, milestone="handover",
                evidence="Original issuer cannot independently renew accepted milestone")
        self.act("milestone", user=self.pm, work_order=wid, milestone="handover",
            evidence="Supplied independent retention re-review")
        c = self.store._case(HOME)
        self.assertNotIn("stale", c["exercise"]["milestones"][ref])
        self.assertEqual(c["finance"]["invoices"], before["finance"]["invoices"])
        self.act("lifecycle", user=self.pm, target="Financial closure")
        self.assertTrue(self.store._case(HOME)["closed"])
        self.store.db.close()
        self.store = open_store()
        self.assertEqual(self.store._case(HOME)["finance"]["invoices"], before["finance"]["invoices"])
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_stale_accepted_unpaid_milestone_requires_review_before_payment_note(self):
        self.complete_journey(pay_handover=False)
        invoice = deepcopy(self.store._case(HOME)["finance"]["invoices"][-1])
        self.assertEqual(invoice["disposition"], "Accept for payment")
        self.assertEqual(invoice["payment_status"], "Not payable yet")
        self.act("return", user=self.pm, target="Independent QA", receiver=self.qi["email"],
            reason="Retention evidence discrepancy", evidence="Supplied fictional discrepancy",
            next_action="Re-check handover milestone after quality review",
            affected_milestones=[invoice["lines"][0]["milestone_ref"]])
        for status in ("Awaiting payment run", "Paid outside this system"):
            before = deepcopy(self.store._case(HOME))
            head = self.store.verify_ledger()["head"]
            with self.assertRaises(ValueError):
                self.store.finance_action(self.geo, HOME, dict(action="payment_status", id=invoice["id"],
                    status=status, evidence="Refused stale payment reference"))
            self.assertEqual(self.store._case(HOME), before)
            self.assertEqual(self.store.verify_ledger()["head"], head)
        self.act("lifecycle", user=self.pm, target="Handover")
        self.act("milestone", user=self.pm, work_order=invoice["work_order"], milestone="handover",
            evidence="Independent supplied milestone re-review")
        self.store.finance_action(self.geo, HOME, dict(action="payment_status", id=invoice["id"],
            status="Paid outside this system", evidence="New fictional externally supplied payment reference"))
        self.act("lifecycle", user=self.pm, target="Financial closure")
        self.assertTrue(self.store._case(HOME)["closed"])

    def test_source_authorization_projection_and_inference_zero_calls(self):
        self.act("create-form", form_type="competitive")
        with self.assertRaises(PermissionError):
            self.act("extract", form_id="FORM-001", source_id="EX-EPC-SIBLING")
        with self.assertRaises(PermissionError):
            self.act("create-form", user=self.users["EX-CON-01"], form_type="competitive")
        self.act("extract", form_id="FORM-001", source_id="EX-EPC-A")
        with patch.object(self.store.ai, "_chat", side_effect=AssertionError("No billable transport")) as call, \
                patch("urllib.request.urlopen", side_effect=AssertionError("No provider/token transport")) as transport:
            self.act("narrative", form_id="FORM-001")
            self.act("assist", form_id="FORM-001", field="epc_band")
            self.act("support", form_id="FORM-001", field="epc_band", claim="The supplied EPC band is D.")
            self.assertEqual(call.call_count, 0)
            self.assertEqual(transport.call_count, 0)
        c = self.store._case(HOME)
        self.assertFalse(c["exercise"]["narratives"][0]["provider_success"])
        self.assertEqual(c["exercise"]["assistance"][0]["status"], "disabled")
        self.assertEqual(c["exercise"]["assistance"][1]["task"], "evidence_support")
        self.assertEqual([r["id"] for r in c["exercise"]["assistance"][0]["sources"]], ["EX-EPC-A"])
        narrative = c["exercise"]["narratives"][0]
        self.act("review-narrative", form_id="FORM-001", record_id=narrative["record_id"],
                 review_action="reject", reason="Manual template is not useful for this pack")
        self.assertEqual(self.store._case(HOME)["exercise"]["narratives"][0]["approval"], "Rejected")
        self.assertEqual(self.store.data["recommendations"][-1]["reviewer_action"], "reject")
        for actor in (self.rlo, self.qi, self.users["EX-CON-01"]):
            result = json.dumps(self.store.exercise_case(actor, HOME))
            self.assertNotIn("eligible_cost", result)
            self.assertNotIn("EX-HOME-001-FINANCE", result)

    def test_building_navigation_preserves_independent_home_gates_and_role_projection(self):
        self.store.technical_action(self.rc, HOME, dict(action="design_submit", note="Fictional individual design"))
        self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Loft insulation",
            scope="Loft insulation", design_version=1, status="Withdrawn", answered_by="The resident",
            note="Fictional individual withdrawal"))
        self.budget()
        before = deepcopy(self.store._case(SIBLING))
        for actor in (self.geo, self.rc, self.rlo, self.users["EX-CON-01"]):
            building = self.store.exercise_building(actor, "EX-BUILDING-001")
            self.assertEqual(building["id"], self.store.exercise_case(actor, HOME)["building_id"])
            self.assertEqual([home["id"] for home in building["homes"]], [HOME, SIBLING])
            for home in building["homes"]:
                self.assertEqual(home["case"], self.store.exercise_case(actor, home["id"])["case"])
            self.assertIn("Unknown", building["shared_cost"])
            if actor["role"] not in ("Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer"):
                self.assertNotIn("eligible_cost", json.dumps(building))
                self.assertNotIn('"finance"', json.dumps(building))
        self.assertEqual(self.store._case(SIBLING), before)
        self.assertEqual(before.get("measure_decisions", {}), {})
        with self.assertRaises(PermissionError):
            self.store.exercise_building(dict(self.users["EX-CON-01"], contractor="Unassigned supplier"), "EX-BUILDING-001")
        with self.assertRaises(ValueError):
            self.store.exercise_building(self.geo, "EX-UNKNOWN")
        with self.assertRaises(PermissionError):
            self.store.exercise_building(dict(self.geo, role="Unknown role"), "EX-BUILDING-001")

    def test_all_profile_form_authority_and_protected_batch_matrix(self):
        from properwarm_mvp.exercise import manifest
        for profile in manifest()["profiles"]:
            actor = self.users[profile["actor"]]
            for kind in forms.SCHEMAS:
                authorized = (actor["role"] in ("Grants and Evidence Officer", "Retrofit Programme Manager",
                                               "Programme Support Officer")
                              or kind == "technical" and actor["role"] == "Retrofit Coordinator")
                before = deepcopy(self.store._case(HOME))
                if authorized:
                    self.act("create-form", user=actor, form_type=kind)
                    created = next(reversed(self.store._case(HOME)["forms"].values()))
                    self.assertEqual(created["form_type"], kind)
                    self.assertEqual(created["case_id"], HOME)
                else:
                    with self.assertRaises(PermissionError, msg=(profile["id"], kind)):
                        self.act("create-form", user=actor, form_type=kind)
                    self.assertEqual(self.store._case(HOME), before)
            for action in ("human-field", "review-pack", "funding-event", "milestone",
                           "lifecycle", "handoff", "return", "external-hazard-reference"):
                before = deepcopy(self.store._case(HOME))
                with self.assertRaises(PermissionError, msg=(profile["id"], action)):
                    self.act(action, user=actor, case_ids=[HOME, SIBLING])
                self.assertEqual(self.store._case(HOME), before)
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_explicit_template_changes_block_and_restore_requires_review(self):
        self.act("create-form", form_type="competitive")
        with self.assertRaises(PermissionError):
            self.act("versions", form_id="FORM-001", schema_version="unapproved", reason="Changed template")
        self.act("versions", user=self.pm, form_id="FORM-001", schema_version="unapproved", reason="New version detected")
        draft = self.store._case(HOME)["forms"]["FORM-001"]
        self.assertIn("unapproved_version", {i["code"] for i in forms.validate_draft(draft)["issues"]})
        self.assertEqual(set(draft["last_invalidation"]["fields"]), set(draft["fields"]))
        self.act("versions", user=self.pm, form_id="FORM-001", schema_version=forms.SCHEMA_VERSION,
                 reason="Revert to approved exercise template; fields remain stale")
        self.assertTrue(all(f["stale"] for f in self.store._case(HOME)["forms"]["FORM-001"]["fields"].values()))

    def test_rejected_application_retry_preserves_exact_attempt_chain(self):
        self.budget()
        self.resolve_epc()
        first = self.complete_form()
        self.event("application-submitted", first)
        self.event("application-disposition", first, user=self.asset, disposition="Rejected")
        with self.assertRaises(ValueError):
            self.event("award", first, amount="7500")
        second = self.complete_form(correction="15999.00")
        with self.assertRaises(ValueError):
            self.event("application-submitted", second)
        self.event("application-submitted", second, retry_of="EVENT-002")
        with self.assertRaises(ValueError):
            self.event("application-disposition", first, user=self.asset, disposition="Accepted",
                       previous_event="EVENT-003")
        self.event("application-disposition", second, user=self.asset, disposition="Accepted",
                   previous_event="EVENT-003")
        self.event("award", second, amount="7500", previous_event="EVENT-004")
        history = self.store._case(HOME)["exercise"]["fund_events"]
        self.assertEqual([e["disposition"] for e in history if e["event"].endswith("disposition")],
                         ["Rejected", "Accepted"])
        self.assertEqual(history[2]["retry_of"], history[1]["id"])
        self.assertTrue(self.store._case(HOME)["funding_ok"])

    def test_unchanged_export_or_review_cannot_resubmit_rejected_content(self):
        self.budget()
        self.resolve_epc()
        fid = self.complete_form()
        self.event("application-submitted", fid)
        self.event("application-disposition", fid, user=self.asset, disposition="Rejected")
        self.act("export", form_id=fid)
        with self.assertRaises(ValueError):
            self.act("funding-event", event="application-submitted", form_id=fid,
                     export_id="export-2", retry_of="EVENT-002", evidence="Different submission reference")
        self.act("review-pack", user=self.pso, form_id=fid, evidence=[f"{HOME}-FINANCE"],
                 reason="Re-review unchanged content is not a correction")
        self.act("export", form_id=fid)
        with self.assertRaises(ValueError):
            self.act("funding-event", event="application-submitted", form_id=fid,
                     export_id="export-3", retry_of="EVENT-002", evidence="Third submission reference")

    def test_stale_rejected_attempt_still_requires_exact_retry_reference(self):
        self.budget()
        self.resolve_epc()
        first = self.complete_form()
        self.event("application-submitted", first)
        self.event("application-disposition", first, user=self.asset, disposition="Rejected")
        self.act("review", form_id=first, field="eligible_cost", review_action="correct",
                 value="15999.00", unit="GBP", currency="GBP", evidence=[f"{HOME}-FINANCE"],
                 reason="Correct rejected source-bound amount")
        self.assertTrue(self.store._case(HOME)["exercise"]["fund_events"][0]["stale"])
        second = self.complete_form(correction="15999.00")
        with self.assertRaises(ValueError):
            self.event("application-submitted", second)
        self.event("application-submitted", second, retry_of="EVENT-002")
        self.assertEqual(self.store._case(HOME)["exercise"]["fund_events"][-1]["retry_of"], "EVENT-002")

    def test_invalid_update_due_date_is_explicit_and_atomic(self):
        before = deepcopy(self.store._case(HOME))
        for due in (None, 123, [], "not-a-date"):
            with self.assertRaises(ValueError):
                self.act("resident-update", user=self.rlo, channel="Phone", evidence="Fictional route",
                         purpose="Scope question", next_update="Explain scope", due=due)
            self.assertEqual(self.store._case(HOME), before)

    def financial_fixture(self):
        """Freeze accepted handover for focused financial-chain tests, not journey evidence."""
        self.budget()
        self.resolve_epc()
        application = self.complete_form()
        self.event("application-submitted", application)
        self.event("application-disposition", application, user=self.asset, disposition="Accepted")
        self.event("award", application, amount="7500")
        with self.store.lock:
            self.store._case(HOME)["exercise"]["lifecycle"] = "Handover"
            self.store.save()
        claim = self.complete_form("claim")
        self.event("claimable", claim, amount="7500")
        self.event("claim-submitted", claim, amount="7500")
        self.event("claim-disposition", claim, user=self.asset, amount="7500", disposition="Accepted")
        return application, claim

    def test_application_invalidation_stales_exact_financial_descendants(self):
        application, claim = self.financial_fixture()
        sibling = deepcopy(self.store._case(SIBLING))
        self.act("review", form_id=application, field="eligible_cost", review_action="correct",
                 value="15000.00", unit="GBP", currency="GBP", evidence=[f"{HOME}-FINANCE"],
                 reason="Only originating application field changed")
        self.assertTrue(all(e["stale"] for e in self.store._case(HOME)["exercise"]["fund_events"]))
        with self.assertRaises(ValueError):
            self.event("cash", claim, amount="7500")
        self.assertEqual(sibling, self.store._case(SIBLING))
        self.store.db.close()
        self.store = open_store()
        self.assertTrue(all(e["stale"] for e in self.store._case(HOME)["exercise"]["fund_events"]))

    def test_fresh_award_recovers_without_reactivating_historical_award(self):
        old, _ = self.financial_fixture()
        self.act("review", form_id=old, field="eligible_cost", review_action="correct",
                 value="15000.00", unit="GBP", currency="GBP", evidence=[f"{HOME}-FINANCE"],
                 reason="Invalidate old application")
        new = self.complete_form()
        self.event("application-submitted", new)
        self.event("application-disposition", new, user=self.asset, disposition="Accepted")
        self.event("award", new, amount="7500")
        self.act("export", form_id=new)
        c = self.store._case(HOME)
        self.assertTrue(c["funding_ok"])
        self.assertEqual([e["stale"] for e in c["exercise"]["fund_events"] if e["event"] == "award"],
                         [True, False])

    def test_cash_is_cumulative_across_claims_and_retries_preserve_receipts(self):
        _, old = self.financial_fixture()
        self.event("cash", old, amount="7500")
        self.act("review", form_id=old, field="eligible_cost", review_action="correct",
                 value="15000.00", unit="GBP", currency="GBP", evidence=[f"{HOME}-FINANCE"],
                 reason="Correct claim; prior cash remains externally evidenced")
        claim = self.complete_form("claim")
        self.event("claimable", claim, amount="7500")
        self.event("claim-submitted", claim, amount="7500")
        self.event("claim-disposition", claim, user=self.asset, amount="7500", disposition="Accepted")
        before = deepcopy(self.store._case(HOME))
        with self.assertRaises(ValueError):
            self.event("cash", claim, amount="7500")
        self.assertEqual(before, self.store._case(HOME))
        self.assertEqual(sum(float(e["amount"]) for e in before["exercise"]["fund_events"]
                             if e["event"] == "cash"), 7500)

    def test_freshness_boundaries_are_internal_not_legal_expiry(self):
        from datetime import date, timedelta
        today = date.today()
        for days in (1, 7, 30, 180):
            self.assertTrue(self.store.exercise_current((today - timedelta(days=days)).isoformat(), days))
            self.assertFalse(self.store.exercise_current((today - timedelta(days=days+1)).isoformat(), days))
        self.assertFalse(self.store.exercise_current((today + timedelta(days=1)).isoformat(), 30))
        self.assertFalse(self.store.exercise_current(None, 30))

    def test_handoff_receipt_acceptance_and_resident_commitment_are_independent(self):
        owner = self.store._case(HOME)["owner"]
        self.act("resident-update", user=self.rlo, channel="Phone", evidence="Fictional agreed contact route",
                 purpose="Answer loft scope question", next_update="Case team explains scope next weekday",
                 due="2026-10-12", due_basis="Fictional weekday commitment", adjustment_reference="Unknown")
        self.act("handoff", user=self.pm, step="sent", receiver=self.pso["email"],
                 reason="Programme review", evidence="Supplied sent reference", due="2026-10-12",
                 urgency="Routine", next_action="Review scope")
        with self.assertRaises(ValueError):
            self.act("handoff", user=self.pso, step="accepted", reason="Cannot infer receipt", evidence="No receipt")
        self.act("handoff", user=self.pso, step="received", reason="Explicit receipt", evidence="Receiver evidence")
        c = self.store._case(HOME)
        self.assertEqual(c["owner"], owner)
        self.assertEqual(c["handoff"]["chase_owner"], owner)
        self.assertIsNone(c["handoff"]["confirmed_receiver"])
        update = deepcopy(c["exercise"]["resident_updates"][0])
        self.act("handoff", user=self.pso, step="accepted", reason="Explicit acceptance", evidence="Separate acceptance")
        self.assertEqual(self.store._case(HOME)["owner"], self.pso["name"])
        self.assertEqual(update, self.store._case(HOME)["exercise"]["resident_updates"][0])
        self.act("handoff", user=self.pso, step="completed", reason="Review complete", evidence="Completion evidence")
        self.act("resident-update", user=self.rlo, step="proposed", update_id="UPDATE-001",
                 evidence="Draft update", reason="Human draft before sending")
        self.act("resident-update", user=self.pm, step="reassign", update_id="UPDATE-001",
                 receiver=self.pso["email"], evidence="Explicit owner reassignment", reason="Agreed cover")
        with self.assertRaises(PermissionError):
            self.act("resident-update", user=self.rlo, step="sent", update_id="UPDATE-001",
                     evidence="Former owner cannot clear it", reason="Not current owner")
        self.act("resident-update", user=self.pso, step="sent", update_id="UPDATE-001",
                 evidence="Wholly fictional supplied outbound reference", reason="Supplied human send event, no actual contact")
        record = self.store._case(HOME)["exercise"]["resident_updates"][0]
        self.assertEqual((record["status"], record["receipt"], record["understanding"]), ("Sent", "Unknown", "Unknown"))
        self.assertEqual(record["purpose"], update["purpose"])
        self.assertEqual(record["due"], update["due"])
        self.assertEqual(len(record["history"]), 3)
        self.assertEqual(len(self.store._case(HOME)["handoff"]["history"]), 4)
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_handoff_escalation_return_and_legacy_shortcuts_cannot_transfer_owner(self):
        original_owner = self.store._case(HOME)["owner_code"]
        self.act("handoff", user=self.pm, step="sent", receiver=self.pso["email"],
                 reason="Review", evidence="Fictional sent", due="Unknown", urgency="Unknown",
                 next_action="Receiver reviews next")
        with self.assertRaises(PermissionError):
            self.act("handoff", user=self.rlo, step="received", reason="Wrong receiver", evidence="Wrong identity")
        self.act("handoff", user=self.pm, step="escalated", reason="Awaiting receipt",
                 evidence="Explicit chase", escalation_owner="Programme team")
        self.act("handoff", user=self.pso, step="returned", reason="Missing source",
                 evidence="Separately supplied return")
        self.assertEqual(self.store._case(HOME)["owner_code"], original_owner)
        self.assertEqual(self.store._case(HOME)["handoff"]["phase"], "Returned")
        with self.assertRaises(ValueError):
            self.store.offer_handoff(self.pm, HOME, self.pso["email"], "Legacy shortcut")
        self.act("lifecycle", user=self.pm, target="Assessment")
        self.act("return", user=self.pm, target="Intake", receiver=self.pso["email"],
                 reason="More source evidence required", evidence="Fictional reviewer request", next_action="Obtain source")
        self.assertEqual(self.store._case(HOME)["exercise"]["lifecycle"], "Intake")
        self.assertEqual(self.store._case(HOME)["exercise"]["returns"][-1]["receiver"], self.pso["email"])
        self.assertEqual(self.store._case(SIBLING)["exercise"]["lifecycle"], "Intake")

    def test_scoped_return_invalidates_exact_form_lineage_and_preserves_receipts(self):
        application, claim = self.financial_fixture()
        self.event("cash", claim, amount="3000")
        self.store.technical_action(self.rc, HOME, dict(action="design_submit", note="Fictional return scope"))
        self.store.technical_action(self.users["EX-RC-02"], HOME,
                                    dict(action="signoff_give", type="design", note="Supplied independent design review"))
        self.store.technical_action(self.qi, HOME,
                                    dict(action="signoff_give", type="assessment", note="Supplied independent survey review"))
        self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Loft insulation",
            scope="Loft insulation", design_version=1, status="Accepted", answered_by="The resident"))
        before = deepcopy(self.store._case(HOME))
        sibling = deepcopy(self.store._case(SIBLING))
        self.act("return", user=self.pm, target="Assessment", receiver=self.rc["email"],
            reason="Supplied exact EPC/technical discrepancy", evidence="Fictional discrepancy source",
            next_action="Named domain owners review only supplied affected scope",
            affected_signoffs=["design"], affected_form_fields={application: ["epc_band"]})
        after = self.store._case(HOME)
        entry = after["exercise"]["returns"][-1]
        self.assertEqual((entry["id"], entry["version"]), ("RETURN-001", 1))
        self.assertEqual(entry["affected_signoffs"], ["design"])
        self.assertEqual(entry["affected_form_fields"], {application: ["epc_band"]})
        self.assertEqual(set(entry["invalidation"][application]["fields"]),
                         {"epc_band", "declaration", "signature"})
        self.assertEqual(after["technical"]["signoffs"]["design"]["status"], "Returned")
        self.assertEqual(after["technical"]["signoffs"]["assessment"],
                         before["technical"]["signoffs"]["assessment"])
        self.assertEqual(after["forms"][application]["fields"]["home_ids"],
                         before["forms"][application]["fields"]["home_ids"])
        self.assertEqual(after["forms"][application]["exports"], before["forms"][application]["exports"])
        self.assertEqual(after["forms"][claim], before["forms"][claim])
        self.assertEqual(after["measure_decisions"], before["measure_decisions"])
        self.assertEqual(after["exercise"]["evidence"], before["exercise"]["evidence"])
        self.assertEqual(after["exercise"]["fund_events"][-1]["amount"], "3000")
        self.assertTrue(all(e["stale"] for e in after["exercise"]["fund_events"]))
        self.assertFalse(after["funding_ok"])
        self.assertEqual(self.store._case(SIBLING), sibling)
        from properwarm_mvp import projection
        for actor in self.users.values():
            payload = self.store.exercise_case(actor, HOME)
            if projection.is_contractor(actor):
                self.assertNotIn("exercise", payload["case"])
            elif actor["role"] not in projection.FINANCE_VIEW:
                projected = payload["case"]["exercise"]["returns"][-1]
                self.assertNotIn("affected_form_fields", projected)
                self.assertNotIn("invalidation", projected)
                self.assertIn("Restricted", projected["form_scope_visibility"])
            else:
                self.assertEqual(payload["case"]["exercise"]["returns"][-1]["invalidation"], entry["invalidation"])
        self.act("lifecycle", user=self.pm, target="Funding")
        with self.assertRaises(GateError):
            self.act("lifecycle", user=self.pm, target="Ready")
        self.act("return", user=self.pm, target="Intake", receiver=self.pso["email"],
            reason="Routing-only information request", evidence="Explicit routing source", next_action="Obtain clarification")
        newest = self.store._case(HOME)["exercise"]["returns"][-1]
        self.assertEqual((newest["id"], newest["version"], newest["invalidation"]), ("RETURN-002", 2, {}))
        self.store.db.close()
        self.store = open_store()
        self.assertEqual(self.store._case(HOME)["exercise"]["returns"][-1], newest)
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_return_scope_validation_is_atomic_and_never_crosses_home(self):
        self.act("lifecycle", user=self.pm, target="Assessment")
        self.act("create-form", form_type="technical")
        self.store.technical_action(self.rc, HOME, dict(action="design_submit", note="Explicit scope fixture"))
        for scope in (
            {"affected_signoffs": ["unknown"]}, {"affected_signoffs": ["design", "design"]},
            {"affected_signoffs": "design"}, {"affected_signoffs": [{}]},
            {"affected_form_fields": []}, {"affected_form_fields": {"FORM-001": ["unknown"]}},
            {"affected_form_fields": {"FORM-001": ["home_ids", "home_ids"]}},
            {"affected_form_fields": {"FORM-001": []}},
            {"affected_form_fields": {"SIBLING-FORM": ["home_ids"]}},
            {"affected_form_fields": {"FORM-001": [{}]}},
            {"affected_milestones": "unknown"}, {"affected_milestones": None},
            {"affected_milestones": [{}]}, {"affected_milestones": ["SIBLING-WO:handover"]},
        ):
            before = deepcopy(self.store._case(HOME))
            head = self.store.verify_ledger()["head"]
            with self.assertRaises(ValueError, msg=scope):
                self.act("return", user=self.pm, target="Intake", receiver=self.pso["email"],
                    reason="Invalid explicit scope", evidence="Fictional source", next_action="Review", **scope)
            self.assertEqual(self.store._case(HOME), before)
            self.assertEqual(self.store.verify_ledger()["head"], head)

    def test_all_earlier_stage_returns_preserve_history_and_role_authority(self):
        stages = ("Intake", "Assessment", "Funding", "Ready", "Installation", "Provider completed",
                  "Independent QA", "Handover", "Financial closure")
        original = deepcopy(self.store._case(HOME))
        labels = ("Contacting resident", "Design in progress", "Funding check", "Final checks before ordering",
                  "Works under way", "Quality check", "Quality check", "Handover to arrange")
        pair_count = 0
        for index, stage in enumerate(stages):
            for target in stages[:index]:
                c = self.store._case(HOME)
                c["exercise"]["lifecycle"] = stage
                c["closed"] = stage == "Financial closure"
                self.store.save()
                before = deepcopy(self.store._case(HOME))
                for actor in self.users.values():
                    if actor["role"] in ("Retrofit Programme Manager", "Programme Support Officer"):
                        continue
                    with self.assertRaises(PermissionError):
                        self.act("return", user=actor, target=target, receiver=self.pso["email"],
                            reason="Unpermitted actor", evidence="Fictional source", next_action="Review")
                    self.assertEqual(self.store._case(HOME), before)
                self.act("return", user=self.pm, target=target, receiver=self.pso["email"],
                    reason=f"Supplied {stage} to {target} routing", evidence="Fictional routing source",
                    next_action="Named receiver obtains explicit correction scope")
                c = self.store._case(HOME)
                pair_count += 1
                self.assertEqual(c["exercise"]["lifecycle"], target)
                self.assertEqual(c["stage"], labels[stages.index(target)])
                self.assertEqual(c["reason"], "Named receiver obtains explicit correction scope")
                self.assertFalse(c["closed"])
                self.assertEqual(c["exercise"]["returns"][-1]["version"], pair_count)
                self.assertEqual(c["exercise"]["returns"][:-1], before["exercise"].get("returns", []))
                for key in ("decision", "hazards", "funding", "home"):
                    self.assertEqual(c[key], original[key])
        self.assertEqual(pair_count, 36)
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_process_interruption_before_commit_and_after_commit_before_response(self):
        before = deepcopy(self.store._case(HOME))
        baseline_head = self.store.verify_ledger()["head"]
        program = """
import os
from properwarm_mvp.factory import open_store
s = open_store()
u = next(u for u in s.staff.values() if u['code'] == 'EX-PM-01')
original = s.save
def interrupted():
    if os.environ['INTERRUPT_POINT'] == 'after':
        original()
    os._exit(23)
s.save = interrupted
s.exercise_action(u, 'EX-HOME-001', {'action': 'lifecycle', 'target': 'Assessment'})
"""
        import os
        for point in ("before", "after"):
            outcome = subprocess.run([sys.executable, "-c", program], env=dict(
                os.environ, INTERRUPT_POINT=point), timeout=30, capture_output=True)
            self.assertEqual(outcome.returncode, 23, outcome.stderr.decode())
            self.store.db.close()
            self.store = open_store()
            c = self.store._case(HOME)
            self.assertEqual(c["exercise"]["lifecycle"], "Intake" if point == "before" else "Assessment")
            self.assertTrue(self.store.verify_ledger()["intact"])
            if point == "before":
                self.assertEqual(c, before)
                self.assertEqual(self.store.verify_ledger()["head"], baseline_head)
            else:
                acknowledged = deepcopy(c)
                ledger_head = self.store.verify_ledger()["head"]
                with self.assertRaises(ValueError):
                    self.act("lifecycle", user=self.pm, target="Assessment")
                self.assertEqual(c, acknowledged)
                self.assertEqual(self.store.verify_ledger()["head"], ledger_head)

    def test_background_batch_interruption_and_lost_response_are_atomic_and_idempotent(self):
        import os
        program = """
import json,os,sys,threading
from properwarm_mvp.factory import open_store
s=open_store()
u=next(u for u in s.staff.values() if u['code']=='EX-PSO-01')
body=json.loads(sys.argv[1])
boundary=threading.Event()
original=s.save
def interrupted():
    if os.environ['INTERRUPT_POINT']=='after':
        original()
    boundary.set()
    threading.Event().wait(30)
s.save=interrupted
threading.Thread(target=lambda:s.exercise_data_action(u,body),daemon=True).start()
if not boundary.wait(15):
    raise RuntimeError('Background worker did not reach persistence boundary')
os._exit(23)
"""
        for point in ("before", "after"):
            note = f"Fictional interrupted background batch {point}"
            preview = self.store.exercise_data_action(self.pso, dict(action="bulk-preview",
                case_ids=[HOME, SIBLING], changes={"coordination_note": note},
                reason="Exact interruption fixture"))
            body = dict(action="commit", token=preview["token"], input_hash=preview["input_hash"],
                expected_fingerprints={str(row["row"]): row["expected_fingerprint"] for row in preview["rows"]})
            before = {cid: deepcopy(self.store._case(cid)) for cid in (HOME, SIBLING)}
            head = self.store.verify_ledger()["head"]
            outcome = subprocess.run([sys.executable, "-c", program, json.dumps(body)],
                env=dict(os.environ, INTERRUPT_POINT=point), timeout=25, capture_output=True)
            self.assertEqual(outcome.returncode, 23, outcome.stderr.decode())
            self.store.db.close()
            self.store = open_store()
            self.assertTrue(self.store.verify_ledger()["intact"])
            if point == "before":
                self.assertEqual({cid: self.store._case(cid) for cid in before}, before)
                self.assertEqual(self.store.verify_ledger()["head"], head)
            else:
                for cid in before:
                    self.assertEqual(self.store._case(cid)["exercise"]["coordination_note"], note)
            first = self.store.exercise_data_action(self.pso, body)
            snapshot = {cid: deepcopy(self.store._case(cid)) for cid in before}
            committed_head = self.store.verify_ledger()["head"]
            self.assertEqual(first["committed"], 2)
            self.assertEqual(first["errors"], 0)
            self.assertEqual(self.store.exercise_data_action(self.pso, body), first)
            self.assertEqual({cid: self.store._case(cid) for cid in before}, snapshot)
            self.assertEqual(self.store.verify_ledger()["head"], committed_head)

    def test_backup_restore_preserves_document_bytes_and_detects_missing_acknowledged_event(self):
        from hashlib import sha256
        import time
        doc = self.store.add_document(self.pso, HOME, "fictional-evidence.txt", "Other",
                                      b"Wholly fictional supplied evidence, not an approval.")
        baseline = deepcopy(self.store._case(HOME))
        baseline_head = self.store.verify_ledger()["head"]
        expected_hash = sha256(self.store.docstore.get(HOME, doc["id"])).hexdigest()
        restored_state = self.root / "isolated-restore"
        restored_state.mkdir()
        shutil.copyfile(self.root / "exercise.json", restored_state / "exercise.json")
        backup_started = time.monotonic()
        with sqlite3.connect(restored_state / "properwarm.sqlite") as backup:
            self.store.db.backup(backup)
        shutil.copytree(self.root / "docs", restored_state / "docs")
        backup_finished = time.monotonic()
        self.act("lifecycle", user=self.pm, target="Assessment")
        acknowledged = deepcopy(self.store._case(HOME))
        acknowledged_head = self.store.verify_ledger()["head"]
        restore_started = time.monotonic()
        pending = dict(operator=self.pso["email"], source="Wholly fictional independent expected snapshot",
                       missing_event="Intake to Assessment", expected_head=acknowledged_head,
                       backup_head=baseline_head, restored_home=HOME,
                       next_action="Recover or explicitly reconcile missing acknowledged event before startup")
        with sqlite3.connect(restored_state / "properwarm.sqlite") as candidate:
            candidate.execute("INSERT INTO meta(key,value) VALUES('exercise_recovery_pending',?)",
                              (json.dumps(pending),))
        from properwarm_mvp.sqlstore import SqlStore
        # Offline inspection only: factory refuses to expose this restore to the server.
        restored = SqlStore(str(restored_state / "exercise.json"), str(restored_state / "properwarm.sqlite"),
                            docs_dir=str(restored_state / "docs"))
        try:
            self.assertEqual(restored._case(HOME), baseline)
            self.assertEqual(restored.verify_ledger()["head"], baseline_head)
            self.assertEqual(sha256(restored.docstore.get(HOME, doc["id"])).hexdigest(), expected_hash)
            self.assertNotEqual(restored._case(HOME), acknowledged)
            self.assertNotEqual(restored.verify_ledger()["head"], acknowledged_head)
            self.assertLess(time.monotonic() - backup_started, 15 * 60)
            self.assertLess(time.monotonic() - restore_started, 60 * 60)
            self.assertLess(backup_finished - backup_started, 15 * 60)
        finally:
            restored.db.close()
        with self.assertRaisesRegex(SystemExit, "offline operator reconciliation"):
            open_store(dict(PW_EXERCISE="1", PW_STATE=str(restored_state)))
        self.assertEqual(self.store._case(HOME), acknowledged)
        self.assertEqual(self.store.verify_ledger()["head"], acknowledged_head)

    def test_hazard_receipt_acceptance_does_not_release_hold_or_change_awareness(self):
        safety = self.users["EX-BSL-01"]
        index = self.store.raise_hazard(self.rlo, HOME, "Damp and mould", "Routine",
                                       "Wholly fictional supplied resident report")
        awareness = self.store._case(HOME)["hazards"][index]["awareness_at"]
        self.store.refer_hazard(self.rlo, HOME, index, safety["email"], "EXTERNAL-FICTIONAL-001")
        params = dict(hazard_index=index, authority="Fictional external service",
                      external_actor="Unknown", reference="EXTERNAL-RECEIPT-001",
                      observed_at="2026-10-10T12:00:00+00:00", evidence="Supplied receipt evidence",
                      followup="Safety liaison chases independent external service")
        with self.assertRaises(ValueError):
            self.act("hazard-followup", user=safety, step="accepted", **params)
        self.act("hazard-followup", user=safety, step="received", **params)
        receipt_snapshot = deepcopy(self.store._case(HOME))
        with self.assertRaises(ValueError):
            self.act("hazard-followup", user=safety, step="accepted", **params)
        self.assertEqual(self.store._case(HOME), receipt_snapshot)
        with self.assertRaises(ValueError):
            self.act("hazard-followup", user=safety, step="chased",
                     **dict(params, reference="EXTERNAL-CHASE-001", observed_at="2026-10-10T12:00:00"))
        self.assertEqual(self.store._case(HOME), receipt_snapshot)
        self.act("hazard-followup", user=safety, step="accepted",
                 **dict(params, reference="EXTERNAL-ACCEPTANCE-001", evidence="Separate external acceptance"))
        hazard = self.store._case(HOME)["hazards"][index]
        self.assertFalse(hazard["released"])
        self.assertEqual(hazard["awareness_at"], awareness)
        self.assertEqual([e["step"] for e in hazard["external_history"]], ["received", "accepted"])
        self.assertNotEqual(hazard["received_reference"]["reference"], hazard["accepted_reference"]["reference"])
        self.assertIsNone(hazard["confirmed_receiver"])
        with self.assertRaises(PermissionError):
            self.store.release_hazard(safety, HOME, index, "Cannot locally release")
        self.assertFalse(self.store._case(SIBLING)["hazards"])

    def test_field_correction_suspends_exact_export_bound_award_without_source_write(self):
        self.budget()
        self.resolve_epc()
        fid = self.complete_form()
        self.event("application-submitted", fid)
        self.event("application-disposition", fid, user=self.asset, disposition="Accepted")
        self.event("award", fid, amount="7500")
        before = deepcopy(self.store._case(HOME))
        self.act("review", form_id=fid, field="eligible_cost", review_action="correct",
                 value="15000.00", unit="GBP", currency="GBP", evidence=[f"{HOME}-FINANCE"],
                 reason="Explicit manual field correction only; source stays unchanged")
        after = self.store._case(HOME)
        self.assertFalse(after["funding_ok"])
        self.assertTrue(all(event["stale"] for event in after["exercise"]["fund_events"]))
        self.assertEqual(after["exercise"]["evidence"], before["exercise"]["evidence"])
        self.assertEqual(after["forms"][fid]["fields"]["home_ids"], before["forms"][fid]["fields"]["home_ids"])
        self.assertEqual(after["forms"][fid]["exports"], before["forms"][fid]["exports"])
        self.assertEqual(self.store._case(SIBLING)["exercise"]["lifecycle"], "Intake")

    def test_two_measure_versions_representative_and_withdrawal_are_independent(self):
        from properwarm_mvp.resident_decisions import measure_decision_view
        c = self.store._case(HOME)
        c["measures"] = ["Loft insulation", "Heat pump"]
        c["exercise"]["representatives"] = {
            "Fictional scheduling reference": {"works_measures": []},
            "Fictional loft authority": {"works_measures": ["Loft insulation"]},
        }
        self.store.save()
        self.store.technical_action(self.rc, HOME, dict(action="design_submit", note="Constructed two-measure design"))
        self.assertEqual([r["status"] for r in measure_decision_view(self.store._case(HOME))],
                         ["Not recorded", "Not recorded"])
        for body, error in (
            (dict(measure="Loft insulation", scope="Loft insulation", design_version=1,
                  representative_ref="Fictional scheduling reference"), PermissionError),
            (dict(measure="Heat pump", scope="Heat pump", design_version=1,
                  representative_ref="Fictional loft authority"), PermissionError),
            (dict(measure="Loft insulation", scope="Heat pump", design_version=1,
                  representative_ref="Fictional loft authority"), ValueError),
            (dict(measure="Loft insulation", scope="Loft insulation", design_version=2,
                  representative_ref="Fictional loft authority"), ValueError),
        ):
            before = deepcopy(self.store._case(HOME))
            with self.assertRaises(error):
                self.store.resident_action(self.rlo, HOME, dict(action="decision_record", status="Accepted",
                    answered_by="Their representative", **body))
            self.assertEqual(self.store._case(HOME), before)
        self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Loft insulation",
            scope="Loft insulation", design_version=1, status="Accepted", answered_by="Their representative",
            representative_ref="Fictional loft authority", note="Supplied exact loft works authority"))
        c = self.store._case(HOME)
        self.assertNotIn("Heat pump", c["measure_decisions"])
        original = deepcopy(c["measure_decisions"]["Loft insulation"])
        self.store.technical_action(self.rc, HOME, dict(action="design_change", note="Supplied heat pump design revision"))
        self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Heat pump",
            scope="Heat pump", design_version=2, status="Accepted", answered_by="The resident",
            note="Supplied heat pump choice against revised design"))
        c = self.store._case(HOME)
        self.assertEqual(c["measure_decisions"]["Loft insulation"], original)
        self.assertIn("Resident choice for Loft insulation needs this design version.", self.store.exercise_readiness(c))
        self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Loft insulation",
            scope="Loft insulation", design_version=2, status="Accepted", answered_by="The resident",
            note="Supplied renewed loft choice"))
        sibling = deepcopy(self.store._case(SIBLING))
        other = deepcopy(self.store._case(HOME)["measure_decisions"]["Heat pump"])
        for status in ("Paused", "Withdrawn"):
            self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Loft insulation",
                scope="Loft insulation", design_version=2, status=status, answered_by="The resident",
                note=f"Supplied fictional {status.lower()} choice"))
            c = self.store._case(HOME)
            self.assertEqual(c["measure_decisions"]["Heat pump"], other)
            self.assertEqual(self.store._case(SIBLING), sibling)
            blockers = [b for b in self.store.exercise_readiness(c) if b.startswith("Resident choice")]
            self.assertEqual(blockers, ["Resident choice for Loft insulation needs this design version."])
            self.assertEqual(c["hazards"], [])
            self.assertFalse(c["closed"])
        self.store.db.close()
        self.store = open_store()
        self.assertEqual(self.store._case(HOME)["measure_decisions"]["Heat pump"], other)
        self.assertEqual([r["status"] for r in measure_decision_view(self.store._case(HOME))],
                         ["Withdrawn", "Accepted"])
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_accessible_service_types_redress_and_reference_projection(self):
        from properwarm_mvp import projection
        from properwarm_mvp.ai_tasks import source_labels
        before_choices = deepcopy(self.store._case(HOME).get("measure_decisions", {}))
        for route in ("Service request", "Complaint", "Repair", "Defect", "Hazard"):
            self.store.resident_action(self.rlo, HOME, dict(action="service_open", route=route,
                summary=f"Supplied fictional {route}", desired_outcome=f"Supplied {route} resolution",
                service_owner=self.rlo["email"], redress_owner=self.pm["email"],
                accessibility=["Safe route needed", "Representative contact"],
                representative_ref="FICTIONAL-PRIVATE-CONTACT-REFERENCE", next_update="2026-10-12"))
        raw = deepcopy(self.store._case(HOME))
        self.assertEqual(raw.get("measure_decisions", {}), before_choices)
        self.assertEqual(raw["decision"]["status"], "Not yet asked")
        for actor in self.users.values():
            visible = self.store.detail(HOME, actor)
            if projection.is_contractor(actor):
                self.assertNotIn("service_requests", visible)
                continue
            for req in visible["service_requests"]:
                self.assertEqual(req["desired_outcome"], f"Supplied {req['route']} resolution")
                self.assertEqual(req["service_owner_email"], self.rlo["email"])
                self.assertEqual(req["redress_owner_email"], self.pm["email"])
                self.assertEqual(req["status"], "Open")
                self.assertEqual(req["next_update"], "2026-10-12")
                if projection.can_see_reason(actor):
                    self.assertEqual(req["accessibility"], ["Safe route needed", "Representative contact"])
                    self.assertEqual(req["representative_ref"], "FICTIONAL-PRIVATE-CONTACT-REFERENCE")
                else:
                    self.assertNotIn("FICTIONAL-PRIVATE-CONTACT-REFERENCE", json.dumps(visible))
                    self.assertEqual(req["accessibility"], [projection.REDACTED])
                    self.assertEqual(req["representative_ref"], projection.REDACTED)
            exported = self.store.exercise_data_export(actor, "story")
            if not projection.can_see_reason(actor):
                self.assertNotIn("FICTIONAL-PRIVATE-CONTACT-REFERENCE", json.dumps(exported))
            labels = source_labels(self.store._case(HOME), reason_ok=projection.can_see_reason(actor))
            self.assertNotIn("FICTIONAL-PRIVATE-CONTACT-REFERENCE", json.dumps(labels))
        self.assertEqual(self.store._case(HOME)["service_requests"], raw["service_requests"],
                         "Projection and export must not mutate stored contact references")
        complaint = raw["service_requests"][1]["id"]
        self.store.resident_action(self.rlo, HOME, dict(action="service_update", id=complaint,
            status="Resolved", next_update="2026-10-13", note="Supplied resolution for independent review"))
        before = deepcopy(self.store._case(HOME))
        with self.assertRaises(PermissionError):
            self.store.resident_action(self.rlo, HOME, dict(action="service_close", id=complaint,
                note="Service owner cannot independently close complaint"))
        self.assertEqual(self.store._case(HOME), before)
        self.store.resident_action(self.pm, HOME, dict(action="service_close", id=complaint,
            note="Supplied resident outcome independently reviewed by redress owner"))
        self.assertEqual(self.store._case(HOME)["service_requests"][1]["status"], "Closed")
        self.assertEqual(self.store._case(HOME).get("measure_decisions", {}), before_choices)
        self.assertEqual(self.store._case(HOME)["hazards"], [])
        self.assertTrue(self.store.verify_ledger()["intact"])

    def test_representative_decision_projection_retains_unknown_and_omits_authority_map(self):
        from properwarm_mvp import projection
        self.store.technical_action(self.rc, HOME, dict(action="design_submit", note="Fictional loft design"))
        c = self.store._case(HOME)
        c["exercise"]["representatives"] = {"FICTIONAL-WORKS-REFERENCE": {"works_measures": ["Loft insulation"]}}
        self.store.save()
        self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Loft insulation",
            scope="Loft insulation", design_version=1, status="Accepted",
            answered_by="Their representative", representative_ref="FICTIONAL-WORKS-REFERENCE"))
        before = deepcopy(self.store._case(HOME))
        for actor in self.users.values():
            payload = self.store.exercise_case(actor, HOME)
            if not projection.can_see_reason(actor):
                self.assertNotIn("FICTIONAL-WORKS-REFERENCE", json.dumps(payload))
                self.assertNotIn("FICTIONAL-WORKS-REFERENCE", json.dumps(self.store.exercise_data_export(actor, "story")))
            if not projection.is_contractor(actor):
                version = payload["case"]["measure_decisions"][0]["versions"][-1]
                self.assertEqual(version["representative_ref"],
                                 "FICTIONAL-WORKS-REFERENCE" if projection.can_see_reason(actor) else projection.REDACTED)
        self.assertEqual(self.store._case(HOME), before)
        self.store.resident_action(self.rlo, HOME, dict(action="service_open", route="Service request",
            summary="Unknown contact preference", desired_outcome="Fictional follow-up",
            service_owner=self.rlo["email"], redress_owner=self.pm["email"], next_update="2026-10-12"))
        req = self.store.detail(HOME, self.geo)["service_requests"][-1]
        self.assertEqual(req["accessibility"], ["Unknown"])
        self.assertEqual(req["representative_ref"], "Unknown")

    def test_resident_scope_capacity_safety_and_fabricated_milestones_denied(self):
        self.store.technical_action(self.rc, HOME, dict(action="design_submit", note="Fictional measure"))
        with self.assertRaises(PermissionError):
            self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Loft insulation",
                scope="Loft insulation", design_version=1, status="Accepted",
                answered_by="Their representative", representative_ref="Scheduling only"))
        self.store.resident_action(self.rlo, HOME, dict(action="decision_record", measure="Loft insulation",
            scope="Loft insulation", design_version=1, status="Withdrawn", answered_by="The resident", note="Fictional withdrawal"))
        self.assertEqual(self.store._case(SIBLING).get("measure_decisions", {}), {})
        pid = self.store.create_package(self.pm, "Fictional", "2026-10-01", "2099-12-31", "Loft insulation", "EX-CALL-OFF-001")
        self.store.set_capacity(self.pm, pid, "Imaginary Retrofit Ltd", 1, 1, "Fictional crew evidence")
        with self.assertRaises(GateError):
            self.store.issue_work_order(self.pm, pid, HOME)
        with self.assertRaises(PermissionError):
            self.store.release_hazard(self.pm, HOME, 0, "No local authority")
        with self.assertRaises(ValueError):
            self.store.submit_quality(self.pm, HOME, "Loft insulation", "Fictional installer", "Provider submission", {})
        self.act("external-hazard-reference", user=self.users["EX-BSL-01"],
                 authority="Fictional external safety service", version="1", evidence="Supplied external record",
                 reference="EXT-1", released=False)
        self.assertIn("Supplied external safety reference retains a hold.", self.store.exercise_readiness(self.store._case(HOME)))
        self.act("external-hazard-reference", user=self.users["EX-BSL-01"],
                 authority="Fictional external safety service", version="2", evidence="Supplied external clearance",
                 reference="EXT-1", released=True)
        self.assertNotIn("Supplied external safety reference retains a hold.", self.store.exercise_readiness(self.store._case(HOME)))
        c = deepcopy(self.store._case(HOME))
        c["exercise"]["evidence"][0]["at"] = "2099-01-01"
        self.assertTrue(any("Source EX-HOME-001-IDENTITY requires human freshness review" in item
                            for item in self.store.exercise_readiness(c)))
        self.store.finance_action(self.geo, HOME, dict(action="invoice_receive", supplier="Imaginary Retrofit Ltd",
            work_order="WO-FABRICATED", ref="FAKE", lines=[dict(measure="Loft insulation", quantity=1,
            amount=3600, milestone_ref="fabricated but nonempty")]))
        self.store.finance_action(self.geo, HOME, dict(action="invoice_match", id="INV-1"))
        self.assertIn("unaccepted_milestone",
                      {e["code"] for e in self.store._case(HOME)["finance"]["invoices"][0]["exceptions"]})

    def test_startup_refuses_private_seed_external_backend_and_incompatible_database(self):
        for extra in ({"PW_DATA": "private.json"}, {"PW_DOC_STORE": "blob"}, {"PW_STORE": "json"}):
            with self.assertRaises(SystemExit):
                open_store(dict(PW_EXERCISE="1", PW_STATE=str(self.root), **extra))
        with self.store.db:
            self.store.db.execute("UPDATE cases SET body=? WHERE id=?", ('{"id":"EX-HOME-001"}', HOME))
        with self.assertRaises(SystemExit):
            open_store()

    def test_azure_exercise_startup_rejects_incompatible_remote_data_before_migration(self):
        from properwarm_mvp import exercise
        env = dict(PW_EXERCISE="1", PW_STORE="mssql", PW_STATE=str(self.root),
                   PW_SQL_SERVER="fictional.database.windows.net", PW_SQL_DATABASE="exercise",
                   PW_SQL_AUTH="token", PW_SQL_TOKEN="fake-only")
        for tables, rows, meta in (
            (["foreign_table"], [], {}),
            (["cases", "meta", "staff", "audit", "audit_head"], [(HOME, '{"id":"wrong"}')], {}),
            (["cases", "meta", "staff", "audit", "audit_head"],
             [(c["id"], json.dumps(c)) for c in exercise.dataset()["cases"]], {"as_of": "2026-10-09"}),
            (["cases", "meta", "staff", "audit", "audit_head"],
             [(c["id"], json.dumps(c)) for c in exercise.dataset()["cases"]],
             {"as_of": exercise.AS_OF, "exercise_recovery_pending": "Supplied unresolved event"}),
        ):
            conn = MagicMock()
            conn.execute.side_effect = [
                MagicMock(fetchall=lambda: [(name,) for name in tables]),
                MagicMock(fetchall=lambda: rows),
                MagicMock(fetchall=lambda: list(meta.items())),
            ]
            with patch("properwarm_mvp.mssqlstore._Conn", return_value=conn), \
                    patch("properwarm_mvp.mssqlstore.MssqlStore") as constructor:
                with self.assertRaises(SystemExit):
                    open_store(env)
                constructor.assert_not_called()
            conn.raw.close.assert_called_once()

    def test_azure_exercise_startup_uses_explicit_blob_env_and_frozen_date(self):
        from properwarm_mvp import exercise
        from properwarm_mvp.documents import AzureBlobDocumentStore
        env = dict(PW_EXERCISE="1", PW_STORE="mssql", PW_STATE=str(self.root),
                   PW_SQL_SERVER="fictional.database.windows.net", PW_SQL_DATABASE="exercise",
                   PW_SQL_AUTH="token", PW_SQL_TOKEN="fake-only", PW_DOC_STORE="azure-blob",
                   PW_BLOB_ACCOUNT_URL="https://fictional.blob.core.windows.net",
                   PW_BLOB_CONTAINER="exercise-evidence", PW_BLOB_CLIENT_ID="fictional-client")
        for existing in (False, True):
            conn, remote = MagicMock(), MagicMock()
            conn.execute.side_effect = [
                MagicMock(fetchall=lambda: [(name,) for name in
                    (["cases", "meta", "staff", "audit", "audit_head"] if existing else [])]),
                MagicMock(fetchall=lambda: [(c["id"], json.dumps(c)) for c in exercise.dataset()["cases"]]),
                MagicMock(fetchall=lambda: [("as_of", exercise.AS_OF)]),
            ]
            with patch("properwarm_mvp.mssqlstore._Conn", return_value=conn), \
                    patch("properwarm_mvp.mssqlstore.MssqlStore", return_value=remote):
                self.assertIs(open_store(env), remote)
            self.assertEqual(remote.as_of, exercise.AS_OF)
            self.assertIsInstance(remote.docstore, AzureBlobDocumentStore)
            self.assertEqual(remote.docstore.client_id, "fictional-client")
            if existing:
                remote._meta_set.assert_not_called()
            else:
                remote._meta_set.assert_called_once_with("as_of", exercise.AS_OF)
            conn.raw.close.assert_called_once()

    def test_http_shortcuts_denied_and_scoped_read_available(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(self.store, "fictional-test-password")))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.server_port}"
        def request(path, payload=None, cookie=None):
            headers = {"Content-Type": "application/json"}
            if cookie:
                headers["Cookie"] = cookie
            req = urllib.request.Request(url + path, data=json.dumps(payload).encode() if payload is not None else None, headers=headers)
            return urllib.request.urlopen(req)
        try:
            with request("/api/login", dict(email=self.geo["email"], password="fictional-test-password")) as response:
                cookie = response.headers["Set-Cookie"].split(";")[0]
            with request(f"/api/cases/{HOME}/exercise", cookie=cookie) as response:
                self.assertEqual(json.load(response)["lifecycle"], "Intake")
            with request("/api/exercise/buildings/EX-BUILDING-001", cookie=cookie) as response:
                self.assertEqual([home["id"] for home in json.load(response)["homes"]], [HOME, SIBLING])
            for action in ("funding", "grant", "decision", "handover", "hazard-release", "draft", "advance"):
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    request(f"/api/cases/{HOME}/{action}", {}, cookie)
                self.assertEqual(caught.exception.code, 403, action)
            with request(f"/api/cases/{HOME}/exercise", dict(action="create-form", form_type="competitive"), cookie) as response:
                self.assertIn("FORM-001", json.load(response)["forms"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()

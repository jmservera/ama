"""Connected fictional exercise oracles through durable Store and HTTP boundaries."""
from copy import deepcopy
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import unittest
from unittest.mock import patch
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
            self.store.finance_action(self.geo, HOME, dict(action="payment_status", id=invoice,
                status="Paid outside this system", evidence=f"Fictional external payment {index}"))
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

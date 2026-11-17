import copy
import json
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import dataset
from test_finance_signoffs import STAFF as FINANCE_STAFF
from test_finance_signoffs import lines, person
from test_grant_lifecycle_controls import designate
from test_quality_procurement import EVIDENCE
from test_stock_reconciliation import query
from zava_forward.core import job_pack as jp
from zava_forward.core import journey_acceptance as ja
from zava_forward.core import perspective_walkthroughs as pw
from zava_forward.core import profile_journey_contract as pjc
from zava_forward.core import projection
from zava_forward.core import resident_preview as rp
from zava_forward.core.store import Store

ROOT = Path(__file__).resolve().parents[3]
HOME = "ZF-1"
SIBLING = "ZF-2"
SECRET_REASON = "SYN-ADJ-HEARING-LOOP: knock loudly and wait 60 seconds"
SIBLING_MARKER = "SIBLING-CANARY-ZF2"


def good() -> dict[str, Any]:
    step = dict(
        record_ids=["EX-HOME-646"],
        state_text="Unknown: eligibility needs an owner",
        keyboard_operable=True,
        announcement="Eligibility unknown, owner shown",
    )
    return dict(
        perspective="asset-investment",
        steps={e: dict(step) for e in pjc.ELEMENTS} | {"handoff": dict(step, owner="Asset lead")},
    )


class ProfileJourneyContractTests(unittest.TestCase):
    def test_complete_record_is_never_accepted(self) -> None:
        rec = pjc.validate(good())
        self.assertEqual(rec["blockers"], [])
        self.assertFalse(rec["accepted"])
        self.assertIn("not user validation", rec["notice"])

    def test_each_contract_failure_is_a_blocker(self) -> None:
        w = copy.deepcopy(good())
        del w["steps"]["recovery"]
        w["steps"]["entry"]["record_ids"] = [" "]
        w["steps"]["evidence"]["state_text"] = "green"
        w["steps"]["safe_endpoint"]["keyboard_operable"] = False
        w["steps"]["handoff"]["announcement"] = ""
        w["steps"]["handoff"]["owner"] = ""
        self.assertEqual(
            set(pjc.validate(w)["blockers"]),
            {
                "asset-investment.recovery:missing",
                "asset-investment.entry:no_linked_records",
                "asset-investment.evidence:state_not_textual",
                "asset-investment.safe_endpoint:not_keyboard_operable",
                "asset-investment.handoff:no_status_announcement",
                "asset-investment.handoff:no_accountable_owner",
            },
        )

    def test_gaps_cover_all_perspectives_and_match_register(self) -> None:
        g = pjc.gaps(ROOT)
        self.assertEqual(set(g), set(pw.register()))
        self.assertEqual(g["provider-contractor"]["unmet"], ["handoff"])
        self.assertIn("evidence", g["finance-grants"]["not_probed"])


class ConnectedSameHomeContractTests(unittest.TestCase):
    def _build_same_home_fixture(
        self,
    ) -> tuple[Store, dict[str, dict[str, Any]], dict[str, dict[str, Any]], rp.Grant]:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = copy.deepcopy(dataset.DATA)
        staff = copy.deepcopy(FINANCE_STAFF) + [
            person("QI-2", "Quality Inspector"),  # type: ignore[no-untyped-call]
            person("PSO-1", "Programme Support Officer"),  # type: ignore[no-untyped-call]
        ]
        for idx in (1, 2):
            staff[idx] = designate(staff[idx])
            for permission in staff[idx]["financial_authority"]["permissions"]:
                permission["route"] = "Warm Homes"
        data["staff"] = staff
        users = {s["code"]: s for s in staff}

        home = data["cases"][0]
        home["owner_code"] = "RLO-1"
        home["owner"] = users["RLO-1"]["name"]
        home["owner_role"] = "Resident Liaison Officer"
        home["waiting_on"] = users["RLO-1"]["name"]
        home["measures"] = "Loft insulation, Cavity wall"
        home["funding_ok"] = True
        home["resident"]["adjustment"] = SECRET_REASON
        home["resident"]["priority_support"] = True
        home["documents"] = [
            dict(
                id=f"SYN-{kind}",
                kind=kind,
                name=f"SYN-{kind}.pdf",
                at="2026-01-01",
                by="Synthetic reviewer",
                scan=dict(status="clean", scanner="Synthetic metadata fixture"),
            )
            for kind in Store.EVIDENCE
        ]

        sibling = data["cases"][1]
        sibling["home"]["address"] = "2 Sibling Crescent"
        sibling["home"]["postcode"] = "SB2 2SB"
        sibling["notes"] = [dict(by="Sam", at="2026-01-01", text=SIBLING_MARKER)]

        path = Path(tmp.name) / "same-home.json"
        path.write_text(json.dumps(data))
        store = Store(str(path))  # type: ignore[no-untyped-call]
        staff_by_role = {
            "Retrofit Programme Manager": users["PM-1"],
            "Retrofit Coordinator": users["RC-1"],
            "Resident Liaison Officer": users["RLO-1"],
            "Building Safety Liaison": users["BSL-1"],
            "Quality Inspector": users["QI-2"],
            "Grants and Evidence Officer": users["GEO-1"],
            "Programme Support Officer": users["PSO-1"],
        }
        grant = rp.Grant(
            grant_id="G-ZF1",
            subject="SYN-RES-ZF1",
            case_id=HOME,
            kind="resident",
            fields=("home", "measures", "progress", "next_step", "appointments", "help"),
            valid_from=datetime(2025, 1, 1, tzinfo=UTC),
            valid_to=datetime(2099, 1, 1, tzinfo=UTC),
        )
        return store, users, staff_by_role, grant

    def _run_connected_walk(
        self,
    ) -> tuple[Store, list[dict[str, Any]], dict[str, dict[str, Any]]]:
        store, u, staff_by_role, grant = self._build_same_home_fixture()
        contractor = u["CON-1"]
        transitions: list[dict[str, Any]] = []

        # Step 0: stock conflict reconciled; handoff offered and received (not yet accepted).
        q = query()
        q["query_owner"] = u["PM-1"]["email"]
        store.stock_reconcile(u["PM-1"], HOME, q)  # type: ignore[no-untyped-call]
        store.stock_query_event(  # type: ignore[no-untyped-call]
            u["PM-2"],
            HOME,
            dict(query_id="SQ-1", action="resolve", reason="Constructed", evidence="SYN-1"),
        )
        store.offer_handoff(  # type: ignore[no-untyped-call]
            u["RLO-1"],
            HOME,
            u["RC-1"]["email"],
            "Coordinate technical design",
            metadata=dataset.change_metadata(store, HOME),
        )
        store.receive_handoff(u["RC-1"], HOME)  # type: ignore[no-untyped-call]
        transitions.append(
            pjc.project_same_home_bundle(
                store,
                HOME,
                staff_users=staff_by_role,
                contractor_user=contractor,
                resident_grant=grant,
            )
        )
        self.assertEqual(
            transitions[0]["staff"]["Retrofit Coordinator"]["work"]["owner"],
            u["RLO-1"]["name"],
        )

        # Step 1: handoff accepted, technical design & sign-offs recorded, handed back to RLO.
        store.accept_handoff(  # type: ignore[no-untyped-call]
            u["RC-1"], HOME, metadata=dataset.change_metadata(store, HOME)
        )
        store.technical_action(  # type: ignore[no-untyped-call]
            u["RC-1"], HOME, dict(action="design_submit", note="Loft and cavity wall")
        )
        store.technical_action(  # type: ignore[no-untyped-call]
            u["QI-1"], HOME, dict(action="signoff_give", type="assessment")
        )
        store.technical_action(  # type: ignore[no-untyped-call]
            u["RC-2"], HOME, dict(action="signoff_give", type="design")
        )
        store.technical_action(  # type: ignore[no-untyped-call]
            u["BSL-1"], HOME, dict(action="signoff_give", type="building")
        )
        store.complete_handoff(  # type: ignore[no-untyped-call]
            u["RC-1"], HOME, "Design and technical sign-offs complete"
        )
        store.offer_handoff(  # type: ignore[no-untyped-call]
            u["RC-1"],
            HOME,
            u["RLO-1"]["email"],
            "Record resident scope and answer",
            metadata=dataset.change_metadata(store, HOME),
        )
        store.accept_handoff(  # type: ignore[no-untyped-call]
            u["RLO-1"], HOME, metadata=dataset.change_metadata(store, HOME)
        )
        store.complete_handoff(  # type: ignore[no-untyped-call]
            u["RLO-1"], HOME, "Ready to record resident scope and answer"
        )
        transitions.append(
            pjc.project_same_home_bundle(
                store,
                HOME,
                staff_users=staff_by_role,
                contractor_user=contractor,
                resident_grant=grant,
            )
        )

        # Step 2: resident scope + Accepted for Loft insulation (Cavity wall stays undecided),
        # package & work order issued, appointed, job pack & worker receipt generated.
        design_ver = store.cases[HOME]["technical"]["design_version"]
        store.resident_action(  # type: ignore[no-untyped-call]
            u["RLO-1"],
            HOME,
            dict(
                action="scope_record",
                measure="Loft insulation",
                scope="Synthetic loft scope",
                design_version=design_ver,
                source="Synthetic supplied scope",
            ),
        )
        store.resident_action(  # type: ignore[no-untyped-call]
            u["RLO-1"],
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
        pid = store.create_package(  # type: ignore[no-untyped-call]
            u["PM-1"],
            "Warm Homes Wave 1",
            "2026-01-01",
            "2099-12-31",
            "Loft insulation works",
            "C-1",
            "SYN-1",
        )
        cap_details = dataset.supplied_contract_fixture(store, pid, u["PM-1"], "Test Ltd")
        store.set_capacity(  # type: ignore[no-untyped-call]
            u["PM-1"], pid, "Test Ltd", 2, 1, "SYN-CAP-1", details=cap_details
        )
        wid = store.issue_work_order(  # type: ignore[no-untyped-call]
            u["PM-1"],
            pid,
            HOME,
            scope="Loft insulation only",
            resident_bindings=[dict(measure="Loft insulation", context_revision=1)],
        )
        dataset.supplied_appointment_fixture(store, u["PM-1"], wid, when="2099-01-01")
        store.record_wo_appointment(u["PM-1"], wid, "Booked", "2099-01-01")  # type: ignore[no-untyped-call]
        pack = store.work_order_job_pack(u["PM-1"], wid)  # type: ignore[no-untyped-call]
        raw_receipt = jp.worker_receipt(
            pack,
            "Loft insulation",
            EVIDENCE,
            confirmed_by="Kim Builder",
            confirmed=True,
            capture_ref="SYN-CAP-REC-1",
            captured_at="2026-03-01T10:00:00+00:00",
            recorded_by={"email": u["RLO-1"]["email"], "role": u["RLO-1"]["role"]},
        )
        receipt = jp.acknowledge_receipt(raw_receipt, u["RLO-1"], "2026-03-01T10:05:00+00:00")
        transitions.append(
            pjc.project_same_home_bundle(
                store,
                HOME,
                staff_users=staff_by_role,
                contractor_user=contractor,
                resident_grant=grant,
                work_order_id=wid,
                job_pack_receipt=receipt,
            )
        )

        # Step 3: work order completed, quality submitted & independently accepted, handed over,
        # and invoice matched, accepted for payment, and noted paid outside this system.
        store.complete_work_order(u["PM-1"], wid, "Install finished")  # type: ignore[no-untyped-call]
        store.submit_quality(  # type: ignore[no-untyped-call]
            u["RLO-1"],
            HOME,
            "Loft insulation",
            "Install Team",
            "Installer",
            EVIDENCE,
            context_revision=1,
        )
        store.accept_quality(u["QI-2"], HOME, 0, "Independent inspection passed")  # type: ignore[no-untyped-call]
        store.hand_over_quality(u["RLO-1"], HOME, 0, "Resident pack handed over", True)  # type: ignore[no-untyped-call]
        store.finance_action(  # type: ignore[no-untyped-call]
            u["GEO-1"], HOME, dict(action="budget_propose", amount=10000)
        )
        store.finance_action(u["PM-1"], HOME, dict(action="budget_approve"))  # type: ignore[no-untyped-call]
        store.finance_action(  # type: ignore[no-untyped-call]
            u["GEO-1"],
            HOME,
            dict(
                action="commit_raise",
                supplier="Test Ltd",
                contract="C-1",
                work_order=wid,
                measure="Loft insulation",
                amount=5000,
                quantity=10,
            ),
        )
        store.finance_action(u["PM-1"], HOME, dict(action="commit_approve", id="COM-1"))  # type: ignore[no-untyped-call]
        store.finance_action(  # type: ignore[no-untyped-call]
            u["GEO-1"],
            HOME,
            dict(
                action="invoice_receive",
                supplier="Test Ltd",
                work_order=wid,
                ref="INV-100",
                lines=lines(),  # type: ignore[no-untyped-call]
            ),
        )
        inv_id = store.detail(HOME)["finance"]["invoices"][-1]["id"]  # type: ignore[no-untyped-call]
        store.finance_action(u["GEO-1"], HOME, dict(action="invoice_match", id=inv_id))  # type: ignore[no-untyped-call]
        store.finance_action(  # type: ignore[no-untyped-call]
            u["PM-2"],
            HOME,
            dict(action="disposition", id=inv_id, decision="Accept for payment", note="Checked"),
        )
        store.finance_action(  # type: ignore[no-untyped-call]
            u["GEO-1"],
            HOME,
            dict(action="payment_status", id=inv_id, status="Paid outside this system"),
        )
        transitions.append(
            pjc.project_same_home_bundle(
                store,
                HOME,
                staff_users=staff_by_role,
                contractor_user=contractor,
                resident_grant=grant,
                work_order_id=wid,
                job_pack_receipt=receipt,
            )
        )
        return store, transitions, u

    def test_connected_same_home_walk_satisfies_contract_and_preserves_signoff_gates(self) -> None:
        store, transitions, _ = self._run_connected_walk()
        self.assertTrue(store.verify_audit())  # type: ignore[no-untyped-call]
        report = pjc.validate_same_home_walk(
            transitions,
            case_id=HOME,
            vulnerability_reason=SECRET_REASON,
            private_markers=("SYN-ADJ-HEARING-LOOP", "knock loudly"),
            sibling_ids=(SIBLING,),
            sibling_markers=(SIBLING_MARKER, "2 Sibling Crescent"),
        )
        self.assertTrue(report["ok"], report["blockers"])
        self.assertEqual(report["status"], "complete_in_shape")
        self.assertEqual(report["blockers"], [])
        self.assertFalse(report["accepted"])
        self.assertEqual(report["boundaries"], pjc.BOUNDARIES)
        self.assertIn("not user validation", report["notice"])

        final_trace = transitions[-1]["audit_trace"]
        self.assertTrue(final_trace["complete"])
        self.assertTrue(final_trace["independent_decisions"])
        self.assertEqual(final_trace["user_validation"], "not-established")
        self.assertEqual(pw.check(ROOT)["elements_met"], 0)
        self.assertEqual(ja.check(ROOT)["passed"], [])

    def test_shared_facts_reject_profile_divergence_and_sibling_leaks(self) -> None:
        _, transitions, _ = self._run_connected_walk()
        broken = copy.deepcopy(transitions[-1])
        broken["staff"]["Quality Inspector"]["home"]["postcode"] = "WR0 0NG"
        broken["contractor_detail"]["measures"] = "Solar PV"
        broken["resident_view"]["stage"] = "Contacting resident"
        broken["work_orders"][0]["scope"] = f"Includes {SIBLING_MARKER}"
        blockers = pjc.check_shared_facts(
            broken,
            sibling_ids=(SIBLING,),
            sibling_markers=(SIBLING_MARKER,),
        )
        self.assertIn("same_home.shared_facts:staff_mismatch:Quality Inspector:postcode", blockers)
        self.assertIn("same_home.shared_facts:contractor_mismatch:measures", blockers)
        self.assertIn("same_home.shared_facts:resident_internal_field_exposed", blockers)
        self.assertIn(f"same_home.shared_facts:sibling_leak:work_orders:{SIBLING_MARKER}", blockers)

    def test_vulnerability_redaction_rejects_contractor_non_reason_and_resident_leaks(self) -> None:
        _, transitions, _ = self._run_connected_walk()
        step = transitions[2]
        for role in pjc.REASON_STAFF_PROFILES:
            self.assertEqual(step["staff"][role]["resident"]["adjustment"], SECRET_REASON)
        for role in pjc.REDACTED_STAFF_PROFILES:
            self.assertEqual(step["staff"][role]["resident"]["adjustment"], projection.REDACTED)

        broken = copy.deepcopy(step)
        broken["staff"]["Retrofit Coordinator"]["resident"]["adjustment"] = SECRET_REASON
        broken["contractor_detail"]["resident"] = {"adjustment": projection.REDACTED}
        broken["job_pack"]["named_contact"] = ""
        broken["resident_view"]["next_step"] = f"Note: {SECRET_REASON}"
        blockers = pjc.check_vulnerability_redaction(
            broken,
            vulnerability_reason=SECRET_REASON,
            private_markers=("SYN-ADJ-HEARING-LOOP",),
        )
        self.assertIn(
            "same_home.redaction:non_reason_role_unredacted:Retrofit Coordinator", blockers
        )
        self.assertIn("same_home.redaction:contractor_forbidden_field:1:resident", blockers)
        self.assertIn("same_home.redaction:contractor_leaked_redacted_marker:1", blockers)
        self.assertIn("same_home.redaction:job_pack_notice_or_contact_missing:3", blockers)
        self.assertIn("same_home.redaction:resident_preview_leaked_private_detail", blockers)

    def test_handover_dependencies_reject_bypassed_safety_consent_handoff_and_quality(
        self,
    ) -> None:
        _, transitions, _ = self._run_connected_walk()

        pending_broken = copy.deepcopy(transitions[0])
        pending_broken["staff"]["Retrofit Programme Manager"]["handoff"]["confirmed_receiver"] = (
            "Retrofit Coordinator RC-1"
        )
        self.assertIn(
            "same_home.handover:premature_owner_transfer_on_pending_handoff",
            pjc.check_handover_dependencies(pending_broken),
        )

        final_broken = copy.deepcopy(transitions[-1])
        canon = final_broken["staff"]["Retrofit Programme Manager"]
        canon["hazards"] = [{"category": "Damp", "priority": "P1", "released": False}]
        canon["can_advance"] = True
        canon["gate"] = []
        canon["work"]["blockers"] = []
        canon["quality"][0]["accepted_by"] = canon["quality"][0]["submitted_by"]
        final_broken["contractor_detail"]["resident_readiness"] = [
            {"measure": "Cavity wall", "flag": "Proceed"}
        ]
        final_broken["job_pack_receipt"]["accepted"] = True
        final_broken["resident_view"]["unavailable"] = []
        final_broken["audit_trace"]["user_validation"] = "established"
        blockers = pjc.check_handover_dependencies(final_broken)
        self.assertIn("same_home.handover:unreleased_hazard_not_blocking", blockers)
        self.assertIn(
            "same_home.handover:contractor_proceed_without_resident_acceptance:Cavity wall",
            blockers,
        )
        self.assertIn("same_home.handover:handed_over_without_independent_acceptance", blockers)
        self.assertIn("same_home.handover:handed_over_with_active_hazard", blockers)
        self.assertIn("same_home.handover:worker_receipt_treated_as_acceptance", blockers)
        self.assertIn("same_home.handover:resident_portal_decision_boundary_missing", blockers)
        self.assertIn("same_home.handover:user_validation_overclaimed", blockers)

    def test_continuity_and_walk_reject_jargon_owner_mismatch_and_home_drift(self) -> None:
        _, transitions, _ = self._run_connected_walk()
        broken_step = copy.deepcopy(transitions[1])
        for role in pjc.SIX_STAFF_PROFILES:
            broken_step["staff"][role]["work"]["next_action"] = "Clear provenance snapshot envelope"
        broken_step["staff"]["Grants and Evidence Officer"]["work"]["owner"] = "Someone Else"
        broken_step["resident_view"]["next_step"] = "Check provenance trace"
        continuity_blockers = pjc.check_next_action_continuity([transitions[0], broken_step])
        self.assertIn(
            "step_1:same_home.continuity:owner_mismatch_across_staff", continuity_blockers
        )
        self.assertIn("step_1:same_home.continuity:jargon_in_next_action", continuity_blockers)
        self.assertIn("step_1:same_home.continuity:resident_next_step_invalid", continuity_blockers)

        drifted = copy.deepcopy(transitions[1])
        for role in pjc.SIX_STAFF_PROFILES:
            drifted["staff"][role]["id"] = SIBLING
        walk_report = pjc.validate_same_home_walk([transitions[0], drifted], case_id=HOME)
        self.assertFalse(walk_report["ok"])
        self.assertIn("step_1:same_home.walk:home_identity_changed", walk_report["blockers"])


if __name__ == "__main__":
    unittest.main()

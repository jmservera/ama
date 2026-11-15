"""Deterministic unit tests for the Phase 0 retrofit-flow discovery contract (issue #124)."""

import hashlib
import json
import unittest
from dataclasses import asdict, replace
from datetime import date

from zava_forward.core import discovery_contract as c

NOMINATED_ON = date(2026, 11, 1)
AGREED_ON = date(2026, 11, 3)
VALIDATED_ON = date(2026, 11, 5)
WINDOW_START = date(2025, 11, 1)
WINDOW_END = date(2026, 10, 31)
AS_OF = date(2026, 11, 10)


def _ready_owner() -> c.NominatedDiscoveryOwner:
    nominated = c.nominate_discovery_owner(
        nominated_by="Clara Finch",
        nominated_by_role="Executive Director of Assets and Sustainability",
        owner="Dev Patel",
        owner_role="Head of Retrofit Delivery",
        nominated_on=NOMINATED_ON,
    )
    return c.agree_discovery_endpoint(
        nominated,
        endpoint="accepted handover",
        agreed_by="Clara Finch",
        agreed_role="Executive Director of Assets and Sustainability",
        agreed_on=AGREED_ON,
    )


def _validated_dictionary() -> c.LifecycleDictionary:
    raw = c.build_default_lifecycle_dictionary()
    return c.LifecycleDictionary(
        stages=tuple(
            c.validate_stage_spec(
                s, validator="Named Stage Lead", role=s.owner_role, on=VALIDATED_ON
            )
            for s in raw.stages
        ),
        events=tuple(
            c.validate_event_spec(
                e, validator="Named Event Lead", role=e.owner_role, on=VALIDATED_ON
            )
            for e in raw.events
        ),
        timestamps=tuple(
            c.validate_timestamp_spec(
                t, validator="Named Data Steward", role=t.owner_role, on=VALIDATED_ON
            )
            for t in raw.timestamps
        ),
        wait_states=tuple(
            c.validate_wait_state_spec(
                w, validator="Named Wait Owner", role=w.owner_role, on=VALIDATED_ON
            )
            for w in raw.wait_states
        ),
        return_loops=tuple(
            c.validate_return_loop_spec(
                r, validator="Named Quality Owner", role=r.owner_role, on=VALIDATED_ON
            )
            for r in raw.return_loops
        ),
    )


def _all_true_test() -> c.ConstraintTestAssessment:
    return c.ConstraintTestAssessment(
        material_critical_path_share=True,
        affects_multiple_properties=True,
        recurs_across_comparable_cases=True,
        traceable_owner_or_dependency=True,
        changes_operational_or_investment_decision=True,
    )


def _with_two_sided_evidence(item: c.ConstraintHypothesis) -> c.ConstraintHypothesis:
    sup = c.EvidenceRecord(
        statement=f"Synthetic wait concentration for {item.code}",
        source_ref=f"synthetic-extract-{item.code.lower()}-sup",
        direction=c.SUPPORTS,
        recorded_by="Nadia Hassan",
    )
    con = c.EvidenceRecord(
        statement=f"Synthetic fast-path cohort counter-check for {item.code}",
        source_ref=f"synthetic-extract-{item.code.lower()}-con",
        direction=c.CONTRADICTS,
        recorded_by="Nadia Hassan",
    )
    return c.record_contradicting_evidence(c.record_supporting_evidence(item, sup), con)


class DiscoveryOwnerTests(unittest.TestCase):
    def test_nomination_rejects_blank_placeholder_automated_and_self_nomination(self) -> None:
        for bad_actor in ("", "   ", "TBD", "pending", "unknown", "Copilot AI", "system bot"):
            with self.assertRaises(ValueError):
                c.nominate_discovery_owner(
                    nominated_by="Clara Finch",
                    nominated_by_role="Executive Sponsor",
                    owner=bad_actor,
                    owner_role="Retrofit Lead",
                    nominated_on=NOMINATED_ON,
                )
        with self.assertRaises(ValueError):
            c.nominate_discovery_owner(
                nominated_by="Clara Finch",
                nominated_by_role="Executive Sponsor",
                owner="clara finch",
                owner_role="Retrofit Lead",
                nominated_on=NOMINATED_ON,
            )

    def test_direct_constructed_owner_status_enforces_human_and_endpoint_rules(self) -> None:
        forged_ai = c.NominatedDiscoveryOwner(
            nominated_by="Clara Finch",
            nominated_by_role="Executive Sponsor",
            owner="AI Agent",
            owner_role="Retrofit Lead",
            nominated_on=NOMINATED_ON,
            endpoint="accepted handover",
            endpoint_agreed_by="Clara Finch",
            endpoint_agreed_role="Executive Sponsor",
            endpoint_agreed_on=AGREED_ON,
        )
        self.assertEqual(forged_ai.status(), "NOT_NOMINATED")
        self.assertFalse(forged_ai.is_ready)

        self_nom = replace(forged_ai, owner="Clara Finch")
        self.assertEqual(self_nom.status(), "NOT_NOMINATED")

    def test_endpoint_agreement_requires_accepted_handover_and_ordered_dates(self) -> None:
        nominated = c.nominate_discovery_owner(
            nominated_by="Clara Finch",
            nominated_by_role="Executive Sponsor",
            owner="Dev Patel",
            owner_role="Head of Retrofit Delivery",
            nominated_on=NOMINATED_ON,
        )
        self.assertEqual(nominated.status(), "ENDPOINT_NOT_AGREED")
        with self.assertRaises(ValueError):
            c.agree_discovery_endpoint(
                nominated,
                endpoint="practical completion",
                agreed_by="Clara Finch",
                agreed_role="Executive Sponsor",
                agreed_on=AGREED_ON,
            )
        with self.assertRaises(ValueError):
            c.agree_discovery_endpoint(
                nominated,
                endpoint="accepted handover",
                agreed_by="Clara Finch",
                agreed_role="Executive Sponsor",
                agreed_on=date(2026, 10, 31),
            )
        agreed = _ready_owner()
        self.assertEqual(agreed.status(), "ENDPOINT_AGREED")
        self.assertTrue(agreed.is_ready)


class LifecycleDictionaryTests(unittest.TestCase):
    def test_default_dictionary_covers_all_pas2035_stages_events_timestamps_waits_loops_with_gaps(
        self,
    ) -> None:
        dictionary = c.build_default_lifecycle_dictionary()
        self.assertEqual(len(dictionary.stages), 15)
        self.assertEqual(len(dictionary.events), 15)
        self.assertEqual(len(dictionary.timestamps), 8)
        self.assertEqual(len(dictionary.wait_states), 7)
        self.assertEqual(len(dictionary.return_loops), 4)

        report = c.summarize_lifecycle_dictionary(dictionary)
        self.assertFalse(report.owner_validated)
        self.assertEqual(report.finding_status, c.CANDIDATE_FINDING_STATUS)
        self.assertEqual(len(report.gaps), 15 + 15 + 8 + 7 + 4)

    def test_dictionary_validation_enforces_owning_role_and_human_validator(self) -> None:
        dictionary = c.build_default_lifecycle_dictionary()
        stage = dictionary.stages[0]
        with self.assertRaises(ValueError):
            c.validate_stage_spec(stage, validator="Analyst", role="Data Analyst", on=VALIDATED_ON)
        with self.assertRaises(ValueError):
            c.validate_stage_spec(stage, validator="TBD", role=stage.owner_role, on=VALIDATED_ON)
        with self.assertRaises(ValueError):
            c.validate_event_spec(
                dictionary.events[0],
                validator="Automation Bot",
                role=dictionary.events[0].owner_role,
                on=VALIDATED_ON,
            )

    def test_fully_validated_dictionary_has_zero_gaps(self) -> None:
        validated = _validated_dictionary()
        self.assertEqual(c.lifecycle_dictionary_gaps(validated), [])
        without_invoice = replace(
            validated, events=tuple(e for e in validated.events if e.event != "invoice")
        )
        self.assertEqual(
            c.lifecycle_dictionary_gaps(without_invoice),
            ["Define lifecycle event 'invoice' as a separate event"],
        )


class PropertyFlowEvaluationTests(unittest.TestCase):
    def test_flow_retains_zero_event_paused_excluded_cancelled_and_withdrawn_candidates(
        self,
    ) -> None:
        dictionary = _validated_dictionary()
        candidates = (
            c.BaselineCandidateRecord("P-ZERO", "2026-01-10", "asset-extract-1"),
            c.BaselineCandidateRecord(
                "P-PAUSED",
                "2026-02-01",
                "asset-extract-1",
                paused_reason="damp remediation",
            ),
            c.BaselineCandidateRecord(
                "P-EXCL",
                "2026-02-15",
                "asset-extract-1",
                excluded_reason="leasehold block",
            ),
            c.BaselineCandidateRecord(
                "P-CANC",
                "2026-03-01",
                "asset-extract-1",
                cancelled_reason="batch re-scoped",
            ),
            c.BaselineCandidateRecord(
                "P-WITH",
                "2026-03-05",
                "asset-extract-1",
                withdrawn_reason="resident declined measures",
                outcome_known=False,
            ),
        )
        report = c.evaluate_property_flow(
            dictionary,
            window_start=WINDOW_START,
            window_end=WINDOW_END,
            as_of=AS_OF,
            candidates=candidates,
        )
        self.assertEqual(len(report.baseline_candidate_ids), 5)
        self.assertEqual(len(report.zero_event_candidate_ids), 5)
        self.assertEqual(
            report.state_counts,
            {
                "in_window_candidates": 5,
                "paused": 1,
                "excluded": 1,
                "cancelled": 1,
                "withdrawn": 1,
                "open_outcome_unknown": 1,
            },
        )
        self.assertFalse(report.owner_validated)
        self.assertEqual(report.finding_status, c.CANDIDATE_FINDING_STATUS)

    def test_flow_computes_bg011_and_handover_legs_and_never_imputes_missing_active_days(
        self,
    ) -> None:
        dictionary = _validated_dictionary()
        candidates = (c.BaselineCandidateRecord("P1", "2026-01-01", "cand-1"),)
        stages = (
            c.PropertyStageRecord(
                property_id="P1",
                stage_code="pas2035_retrofit_assessment",
                entered_at="2026-01-05",
                exited_at="2026-01-15",
                active_started_at="2026-01-08",
                active_completed_at="2026-01-10",
                source_ref="stage-1",
            ),
            c.PropertyStageRecord(
                property_id="P1",
                stage_code="pas2035_design_and_coordination",
                entered_at="2026-01-15",
                exited_at="2026-02-04",
                source_ref="stage-2",
            ),
        )
        events = (
            c.PropertyEventRecord("P1", "candidate selection", "2026-01-01", "ev-1"),
            c.PropertyEventRecord("P1", "retrofit assessment completed", "2026-01-15", "ev-2"),
            c.PropertyEventRecord("P1", "design approved", "2026-02-04", "ev-3"),
            c.PropertyEventRecord("P1", "resident works decision recorded", "2026-02-10", "ev-4"),
            c.PropertyEventRecord("P1", "ready to install", "2026-02-14", "ev-5"),
            c.PropertyEventRecord("P1", "installation", "2026-03-01", "ev-6"),
            c.PropertyEventRecord("P1", "physical acceptance", "2026-03-06", "ev-7"),
            c.PropertyEventRecord("P1", "evidence acceptance", "2026-03-11", "ev-8"),
            c.PropertyEventRecord("P1", "resident handover", "2026-03-14", "ev-9"),
            c.PropertyEventRecord("P1", "accepted handover", "2026-03-16", "ev-10"),
        )
        report = c.evaluate_property_flow(
            dictionary,
            window_start=WINDOW_START,
            window_end=WINDOW_END,
            as_of=AS_OF,
            candidates=candidates,
            stage_records=stages,
            event_records=events,
        )
        self.assertEqual(report.gaps, ())
        self.assertEqual(report.accepted_handover_property_ids, ("P1",))
        self.assertEqual(report.bg011_assessment_to_ready_to_install_days["P1"], 30.0)
        self.assertEqual(report.candidate_to_accepted_handover_days["P1"], 74.0)
        self.assertEqual(
            report.post_install_handover_legs_days["P1"],
            {
                "installation to physical acceptance": 5.0,
                "physical acceptance to evidence acceptance": 5.0,
                "evidence acceptance to resident handover": 3.0,
                "resident handover to accepted handover": 2.0,
            },
        )
        self.assertEqual(report.stage_metrics[0]["calendar_days"], 10.0)
        self.assertEqual(report.stage_metrics[0]["active_days"], 2.0)
        self.assertEqual(report.stage_metrics[1]["calendar_days"], 20.0)
        self.assertIsNone(report.stage_metrics[1]["active_days"])

    def test_flow_enforces_accepted_handover_prerequisites_and_unresolved_reopen_blocks(
        self,
    ) -> None:
        dictionary = _validated_dictionary()
        candidates = (
            c.BaselineCandidateRecord(
                "P-MISSING",
                "2026-01-01",
                "cand-1",
                intended_energy_outcome_status="post_handover_monitoring_scheduled",
            ),
            c.BaselineCandidateRecord("P-REOPEN", "2026-01-01", "cand-2"),
        )
        events = (
            c.PropertyEventRecord("P-MISSING", "candidate selection", "2026-01-01", "e1"),
            c.PropertyEventRecord("P-MISSING", "accepted handover", "2026-03-01", "e2"),
            c.PropertyEventRecord("P-REOPEN", "candidate selection", "2026-01-01", "e3"),
            c.PropertyEventRecord("P-REOPEN", "design approved", "2026-01-20", "e4"),
            c.PropertyEventRecord(
                "P-REOPEN", "resident works decision recorded", "2026-01-25", "e5"
            ),
            c.PropertyEventRecord("P-REOPEN", "physical acceptance", "2026-02-15", "e6"),
            c.PropertyEventRecord("P-REOPEN", "evidence acceptance", "2026-02-20", "e7"),
            c.PropertyEventRecord("P-REOPEN", "resident handover", "2026-02-25", "e8"),
            c.PropertyEventRecord("P-REOPEN", "accepted handover", "2026-03-01", "e9"),
        )
        loops = (
            c.PropertyReturnLoopRecord(
                property_id="P-REOPEN",
                kind="reopen",
                from_stage="resident_and_accepted_handover",
                to_stage="reopened_aftercare",
                recorded_at="2026-03-05",
                unresolved=True,
                source_ref="loop-1",
            ),
        )
        report = c.evaluate_property_flow(
            dictionary,
            window_start=WINDOW_START,
            window_end=WINDOW_END,
            as_of=AS_OF,
            candidates=candidates,
            event_records=events,
            loop_records=loops,
        )
        self.assertEqual(report.accepted_handover_property_ids, ())
        self.assertEqual(report.invalid_accepted_handover_ids, ("P-MISSING", "P-REOPEN"))
        self.assertIsNone(report.candidate_to_accepted_handover_days["P-MISSING"])
        self.assertIsNone(report.candidate_to_accepted_handover_days["P-REOPEN"])
        self.assertEqual(
            report.intended_energy_outcome_counts["post_handover_monitoring_scheduled"], 1
        )
        self.assertTrue(any("prerequisite events" in g for g in report.gaps))
        self.assertTrue(any("unresolved post-handover reopen" in g for g in report.gaps))

    def test_flow_preserves_unknown_disputed_unattributed_waits_and_counts_return_loops(
        self,
    ) -> None:
        dictionary = _validated_dictionary()
        waits = (
            c.PropertyWaitRecord(
                property_id="P1",
                wait_state_code="awaiting_supplier_or_professional_capacity",
                party="Installer Alpha",
                started_at="2026-02-01",
                ended_at="2026-02-16",
                cause_code="UNKNOWN",
                source_ref="w-1",
            ),
            c.PropertyWaitRecord(
                property_id="P2",
                wait_state_code="awaiting_handoff_acceptance_or_approval",
                party="",
                started_at="2026-11-05",
                ended_at="",
                cause_code="DISPUTED",
                source_ref="w-2",
            ),
        )
        loops = (
            c.PropertyReturnLoopRecord(
                "P1",
                "repeat visit",
                "appointment_and_installation",
                "appointment_and_installation",
                "2026-02-20",
                rework_days=3.0,
                source_ref="l-1",
            ),
            c.PropertyReturnLoopRecord(
                "P1",
                "rejection",
                "quality_and_evidence_acceptance",
                "appointment_and_installation",
                "2026-02-28",
                rework_days=4.5,
                source_ref="l-2",
            ),
        )
        report = c.evaluate_property_flow(
            dictionary,
            window_start=WINDOW_START,
            window_end=WINDOW_END,
            as_of=AS_OF,
            candidates=(c.BaselineCandidateRecord("P1", "2026-01-01", "c-1"),),
            wait_records=waits,
            loop_records=loops,
        )
        self.assertEqual(report.waits_by_party[0]["party"], "Installer Alpha")
        self.assertEqual(report.waits_by_party[0]["days"], 15.0)
        self.assertEqual(report.waits_by_party[0]["unknown_or_disputed_cause"], 1)
        self.assertEqual(report.waits_by_party[1]["party"], "Unattributed")
        self.assertEqual(report.waits_by_party[1]["days"], 5.0)
        self.assertEqual(report.waits_by_party[1]["open_waits"], 1)
        self.assertEqual(report.return_loop_totals["repeat visit"], 1)
        self.assertEqual(report.return_loop_totals["rejection"], 1)
        self.assertEqual(report.explicit_rework_days_by_kind["rejection"], 4.5)

    def test_flow_flags_malformed_naive_unknown_and_out_of_order_timestamps_without_guessing(
        self,
    ) -> None:
        dictionary = _validated_dictionary()
        report = c.evaluate_property_flow(
            dictionary,
            window_start=WINDOW_START,
            window_end=WINDOW_END,
            as_of=AS_OF,
            candidates=(c.BaselineCandidateRecord("P1", "2026-01-10T09:00:00", "c-1"),),
            event_records=(
                c.PropertyEventRecord("P2", "retrofit assessment completed", "2026-03-10", "e-1"),
                c.PropertyEventRecord("P2", "ready to install", "2026-03-01", "e-2"),
                c.PropertyEventRecord("P2", "unknown milestone", "2026-03-12", "e-3"),
            ),
        )
        self.assertIsNone(report.bg011_assessment_to_ready_to_install_days["P2"])
        self.assertTrue(any("unusable identified_at" in g for g in report.gaps))
        self.assertTrue(any("before 'retrofit assessment completed'" in g for g in report.gaps))
        self.assertTrue(any("unknown lifecycle event" in g for g in report.gaps))

    def test_flow_evaluation_is_deterministic_across_repeated_runs(self) -> None:
        dictionary = _validated_dictionary()
        candidates = (c.BaselineCandidateRecord("P1", "2026-01-05", "c-1"),)
        events = (
            c.PropertyEventRecord("P1", "retrofit assessment completed", "2026-01-10", "e-1"),
            c.PropertyEventRecord("P1", "ready to install", "2026-01-25", "e-2"),
        )
        digests = {
            hashlib.sha256(
                json.dumps(
                    asdict(
                        c.evaluate_property_flow(
                            dictionary,
                            window_start=WINDOW_START,
                            window_end=WINDOW_END,
                            as_of=AS_OF,
                            candidates=candidates,
                            event_records=events,
                        )
                    ),
                    sort_keys=True,
                    default=str,
                ).encode("utf-8")
            ).hexdigest()
            for _ in range(3)
        }
        self.assertEqual(len(digests), 1)


class RankedConstraintRegisterTests(unittest.TestCase):
    def test_seed_constraint_register_enforces_contiguous_ranks_and_candidate_status(self) -> None:
        reg = c.build_seed_constraint_register()
        self.assertFalse(reg.owner_validated)
        self.assertEqual(reg.finding_status, c.CANDIDATE_FINDING_STATUS)
        rows = reg.to_rows()
        self.assertEqual([r["rank"] for r in rows], [1, 2, 3, 4, 5])
        self.assertTrue(
            all(
                r["owner_validated"] is False
                and r["finding_status"] == c.CANDIDATE_FINDING_STATUS
                and isinstance(r["evidence_gaps"], tuple)
                and len(r["evidence_gaps"]) == 2
                for r in rows
            )
        )
        with self.assertRaises(ValueError):
            c.RankedConstraintRegister(hypotheses=(reg.hypotheses[1],))

    def test_constraint_validation_requires_both_supporting_and_contradicting_evidence(
        self,
    ) -> None:
        cap = c.build_seed_constraint_register().hypotheses[0]
        sup = c.EvidenceRecord(
            "Installer queue averaged 28 days", "proc-extract-1", c.SUPPORTS, "Nadia Hassan"
        )
        only_supporting = c.assess_constraint_test(
            c.record_supporting_evidence(cap, sup), _all_true_test()
        )
        self.assertEqual(len(c.constraint_evidence_gaps(only_supporting)), 1)
        with self.assertRaises(ValueError):
            c.validate_constraint_by_domain_owner(
                only_supporting,
                validator="Omar Ali",
                role="Procurement and Contracts",
                on=VALIDATED_ON,
                accept=True,
                note="Attempted without contradicting evidence",
            )

        con = c.EvidenceRecord(
            "Lot 2 call-offs cleared within 5 days",
            "proc-extract-2",
            c.CONTRADICTS,
            "Nadia Hassan",
        )
        only_contradicting = c.assess_constraint_test(
            c.record_contradicting_evidence(cap, con), _all_true_test()
        )
        with self.assertRaises(ValueError):
            c.validate_constraint_by_domain_owner(
                only_contradicting,
                validator="Omar Ali",
                role="Procurement and Contracts",
                on=VALIDATED_ON,
                accept=True,
                note="Attempted without supporting evidence",
            )

    def test_constraint_acceptance_requires_five_part_test_domain_role_and_proposer_separation(
        self,
    ) -> None:
        base = c.ConstraintHypothesis(
            rank=1,
            code="CAP",
            summary="Supplier capacity",
            intervention_class="Framework pacing",
            domain_owner_roles=("Procurement and Contracts",),
            proposed_by="Nadia Hassan",
        )
        evidenced = _with_two_sided_evidence(base)
        incomplete_test = c.assess_constraint_test(
            evidenced,
            replace(_all_true_test(), changes_operational_or_investment_decision=False),
        )
        with self.assertRaises(ValueError):
            c.validate_constraint_by_domain_owner(
                incomplete_test,
                validator="Omar Ali",
                role="Procurement and Contracts",
                on=VALIDATED_ON,
                accept=True,
                note="Missing decision impact criterion",
            )
        ready = c.assess_constraint_test(evidenced, _all_true_test())
        with self.assertRaises(ValueError):
            c.validate_constraint_by_domain_owner(
                ready,
                validator="Nadia Hassan",
                role="Procurement and Contracts",
                on=VALIDATED_ON,
                accept=True,
                note="Self approval attempt",
            )
        with self.assertRaises(ValueError):
            c.validate_constraint_by_domain_owner(
                ready,
                validator="Omar Ali",
                role="Resident Engagement and Housing",
                on=VALIDATED_ON,
                accept=True,
                note="Wrong role attempt",
            )


class GovernanceGuardTests(unittest.TestCase):
    def _adjudicated_register(self) -> c.RankedConstraintRegister:
        seed = c.build_seed_constraint_register()
        adjudicated: list[c.ConstraintHypothesis] = []
        for idx, item in enumerate(seed.hypotheses):
            evidenced = c.assess_constraint_test(_with_two_sided_evidence(item), _all_true_test())
            accept = idx != 2
            adjudicated.append(
                c.validate_constraint_by_domain_owner(
                    evidenced,
                    validator=f"Domain Owner {idx + 1}",
                    role=item.domain_owner_roles[0],
                    on=VALIDATED_ON,
                    accept=accept,
                    note="Confirmed against two-sided evidence"
                    if accept
                    else "Contradicting evidence refuted primary bottleneck claim",
                )
            )
        return c.RankedConstraintRegister(hypotheses=tuple(adjudicated))

    def test_validated_register_and_pack_preserve_disputed_hypotheses_as_non_findings(
        self,
    ) -> None:
        owner = _ready_owner()
        dictionary = _validated_dictionary()
        adjudicated_reg = self._adjudicated_register()
        self.assertTrue(all(not h.owner_validated for h in adjudicated_reg.hypotheses))

        pack = c.Phase0DiscoveryPack(
            contract_version=c.CONTRACT_VERSION,
            discovery_owner=owner,
            dictionary=dictionary,
            dictionary_report=c.summarize_lifecycle_dictionary(dictionary),
            flow_report=c.evaluate_property_flow(
                dictionary,
                window_start=WINDOW_START,
                window_end=WINDOW_END,
                as_of=AS_OF,
                candidates=(c.BaselineCandidateRecord("P1", "2026-01-10", "c-1"),),
            ),
            constraint_register=adjudicated_reg,
        )
        c.enforce_governance_guard(pack)
        validated_pack = c.validate_discovery_pack(
            pack,
            by="Dev Patel",
            on=date(2026, 11, 12),
            note="Phase 0 baseline discovery formally signed off by nominated owner",
        )
        c.enforce_governance_guard(validated_pack, discovery_owner=owner, dictionary=dictionary)
        self.assertTrue(validated_pack.owner_validated)
        self.assertEqual(validated_pack.finding_status, c.VALIDATED_FINDING_STATUS)

        by_code = {h.code: h for h in validated_pack.constraint_register.hypotheses}
        self.assertTrue(by_code["CAP"].owner_validated)
        self.assertEqual(by_code["CAP"].finding_status, c.VALIDATED_FINDING_STATUS)
        self.assertEqual(by_code["RESIDENT"].review_status, c.DISPUTED)
        self.assertFalse(by_code["RESIDENT"].owner_validated)
        self.assertEqual(by_code["RESIDENT"].finding_status, c.CANDIDATE_FINDING_STATUS)

    def test_governance_guard_rejects_every_forged_or_premature_promotion_path(self) -> None:
        owner = _ready_owner()
        dictionary = _validated_dictionary()
        unvalidated_dict = c.build_default_lifecycle_dictionary()
        seed_hyp = c.build_seed_constraint_register().hypotheses[0]

        with self.assertRaises(c.GovernanceViolationError):
            replace(seed_hyp, owner_validated=True)
        with self.assertRaises(c.GovernanceViolationError):
            replace(seed_hyp, finding_status=c.VALIDATED_FINDING_STATUS)

        adjudicated = self._adjudicated_register()
        disputed_hyp = adjudicated.hypotheses[2]
        with self.assertRaises(c.GovernanceViolationError):
            c.validate_constraint_by_discovery_owner(
                disputed_hyp,
                owner,
                dictionary,
                by="Dev Patel",
                on=VALIDATED_ON,
                note="Cannot promote disputed hypothesis",
            )
        with self.assertRaises(c.GovernanceViolationError):
            c.validate_constraint_by_discovery_owner(
                adjudicated.hypotheses[0],
                owner,
                unvalidated_dict,
                by="Dev Patel",
                on=VALIDATED_ON,
                note="Dictionary still has gaps",
            )
        with self.assertRaises(c.GovernanceViolationError):
            c.validate_constraint_by_discovery_owner(
                adjudicated.hypotheses[0],
                owner,
                dictionary,
                by="Someone Else",
                on=VALIDATED_ON,
                note="Not the nominated owner",
            )
        with self.assertRaises(c.GovernanceViolationError):
            c.enforce_governance_guard(
                {
                    "owner_validated": True,
                    "finding_status": c.VALIDATED_FINDING_STATUS,
                    "owner_validated_by": "Dev Patel",
                },
                discovery_owner=c.NominatedDiscoveryOwner(),
                dictionary=dictionary,
            )
        with self.assertRaises(c.GovernanceViolationError):
            c.enforce_governance_guard({"notice": "missing governance fields"})

    def test_default_phase0_pack_is_candidate_until_full_nominated_owner_validation(
        self,
    ) -> None:
        pack = c.build_default_phase0_pack(
            window_start=WINDOW_START,
            window_end=WINDOW_END,
            as_of=AS_OF,
        )
        self.assertFalse(pack.owner_validated)
        self.assertEqual(pack.finding_status, c.CANDIDATE_FINDING_STATUS)
        self.assertFalse(pack.dictionary_report.owner_validated)
        self.assertFalse(pack.flow_report.owner_validated)
        self.assertFalse(pack.constraint_register.owner_validated)
        c.enforce_governance_guard(pack)
        with self.assertRaises(c.GovernanceViolationError):
            c.validate_discovery_pack(
                pack,
                by="Dev Patel",
                on=VALIDATED_ON,
                note="Premature pack sign-off",
            )


if __name__ == "__main__":
    unittest.main()

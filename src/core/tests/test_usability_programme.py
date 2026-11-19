"""Unit tests for the Issue #155 usability testing programme contract and evaluator."""

from __future__ import annotations

import dataclasses
import unittest
from pathlib import Path

from zava_forward.core import journey_register as jr
from zava_forward.core import learning_test_bundles as ltb
from zava_forward.core import perspective_walkthroughs as pw
from zava_forward.core import profile_journey_contract as pjc
from zava_forward.core import usability_programme as up

ROOT = Path(__file__).resolve().parents[3]
SPEC_PATH = ROOT / "docs" / "reference" / "research" / "ux" / "usability-test-programme-plan.md"


def _agreed_sa010(agreed_date: str = "2026-11-10") -> up.AuditUseAgreement:
    return up.AuditUseAgreement(
        agreed_with_staff=True,
        agreed_date=agreed_date,
        staff_representatives=("Alex Patel (Unison Workplace Rep)", "Priya Nair (RLO Rep)"),
        programme_owner="Jordan Clarke",
        dpo_reviewer="Samira Hassan",
    )


class UsabilityProgrammeTests(unittest.TestCase):
    def test_default_programme_plan_validates_all_cohorts_accessibility_and_consent(self) -> None:
        plan = up.default_programme_plan()
        result = up.validate_programme_plan(plan)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["role_cohort_count"], 13)
        self.assertEqual(result["task_script_count"], 21)
        self.assertFalse(result["audit_use_agreed"])
        self.assertTrue(plan.synthetic_data_only)
        self.assertTrue(plan.recording_default_off)
        self.assertTrue(plan.thresholds_are_hypotheses)

        cohort_by_id = {c.cohort_id: c for c in plan.cohorts}
        for pid in pw.EVIDENCE:
            self.assertEqual(cohort_by_id[pid].min_participants, 5)
            self.assertEqual(cohort_by_id[pid].max_participants, 8)
            self.assertTrue(cohort_by_id[pid].t0_applicable)
        for rid in ("resident", "resident-representative"):
            self.assertEqual(cohort_by_id[rid].min_participants, 5)
            self.assertEqual(cohort_by_id[rid].max_participants, 8)
            self.assertFalse(cohort_by_id[rid].t0_applicable)
        pilot = cohort_by_id["proxy-pilot"]
        self.assertEqual((pilot.min_participants, pilot.max_participants), (2, 3))
        self.assertFalse(pilot.counts_toward_role_minimum)

    def test_programme_plan_rejects_under_or_over_sized_cohorts_and_counted_pilot(self) -> None:
        base = up.default_programme_plan()
        bad_cohorts = []
        for cohort in base.cohorts:
            if cohort.cohort_id == "programme-coordinator":
                bad_cohorts.append(dataclasses.replace(cohort, min_participants=4))
            elif cohort.cohort_id == "finance-grants":
                bad_cohorts.append(dataclasses.replace(cohort, max_participants=9))
            elif cohort.cohort_id == "resident":
                bad_cohorts.append(dataclasses.replace(cohort, t0_applicable=True))
            elif cohort.cohort_id == "proxy-pilot":
                bad_cohorts.append(dataclasses.replace(cohort, counts_toward_role_minimum=True))
            else:
                bad_cohorts.append(cohort)
        invalid = dataclasses.replace(base, cohorts=tuple(bad_cohorts))
        res = up.validate_programme_plan(invalid)
        self.assertFalse(res["valid"])
        self.assertIn("programme-coordinator:participants_must_be_5_to_8", res["errors"])
        self.assertIn("finance-grants:participants_must_be_5_to_8", res["errors"])
        self.assertIn("resident:t0_not_applicable_to_resident_portal", res["errors"])
        self.assertIn("proxy-pilot:pilot_cannot_count_toward_role_minimum", res["errors"])

    def test_programme_plan_rejects_missing_accessibility_assistive_or_consent_clauses(
        self,
    ) -> None:
        base = up.default_programme_plan()
        a11y = dict(base.accessibility_support)
        a11y["manual_non_digital_parity"] = "  "
        consent = dict(base.consent_and_data_handling)
        del consent["separate_from_tenancy_works_and_employment"]
        invalid = dataclasses.replace(
            base,
            accessibility_support=a11y,
            assistive_tech_coverage=("keyboard_only",),
            consent_and_data_handling=consent,
            synthetic_data_only=False,
            recording_default_off=False,
            thresholds_are_hypotheses=False,
        )
        res = up.validate_programme_plan(invalid)
        self.assertFalse(res["valid"])
        self.assertIn("missing_accessibility_clause:manual_non_digital_parity", res["errors"])
        self.assertIn(
            "missing_consent_or_data_clause:separate_from_tenancy_works_and_employment",
            res["errors"],
        )
        self.assertTrue(any(e.startswith("missing_assistive_tech_routes:") for e in res["errors"]))
        self.assertIn("synthetic_data_only_required", res["errors"])
        self.assertIn("recording_default_off_required", res["errors"])
        self.assertIn("thresholds_must_remain_hypotheses", res["errors"])

    def test_derived_task_scripts_cover_profile_contract_journeys_and_learning_bundles(
        self,
    ) -> None:
        scripts = up.derive_task_scripts()
        check = up.validate_task_scripts(scripts)
        self.assertTrue(check["valid"], check["errors"])
        ids = [s.script_id for s in scripts]
        expected_ids = [
            "T0",
            "T1",
            "T2",
            "T3",
            "T4",
            "T5",
            "T6",
            "T7",
            "T8",
            "R-J1",
            "R-J2",
            "R-J3",
            "R-J4",
            "R-J5",
            "R-J6",
            "R-R1",
            "B1-story-once",
            "B2-pre-visit-pack",
            "B3-change-impact",
            "B4-handover-aftercare",
            "B5-funding-evidence",
        ]
        self.assertEqual(ids, expected_ids)
        self.assertEqual(set(check["covered_perspectives"]), set(pw.EVIDENCE.keys()))
        self.assertEqual(set(check["covered_journeys"]), set(jr.JOURNEYS.keys()))
        self.assertEqual(set(check["covered_bundles"]), set(ltb.BUNDLES.keys()))

        by_id = {s.script_id: s for s in scripts}
        self.assertEqual(set(by_id["T4"].same_home_staff_profiles), set(pjc.SIX_STAFF_PROFILES))
        self.assertEqual(
            by_id["T8"].register_element_status["provider-contractor"]["handoff"],
            "unmet",
        )
        self.assertIn("asset-investment", by_id["T1"].proxy_only_perspectives)

    def test_validate_task_scripts_rejects_out_of_scope_atlas_ids_and_missing_o16_rule(
        self,
    ) -> None:
        scripts = list(up.derive_task_scripts())
        tampered = []
        for s in scripts:
            if s.script_id == "B3-change-impact":
                tampered.append(
                    dataclasses.replace(
                        s,
                        atlas_ids=s.atlas_ids + ("O10",),
                        o16_single_count_rule=None,
                    )
                )
            elif s.script_id == "T1":
                tampered.append(dataclasses.replace(s, contract_elements={"entry": "Only entry"}))
            else:
                tampered.append(s)
        res = up.validate_task_scripts(tampered)
        self.assertFalse(res["valid"])
        self.assertIn("B3-change-impact:out_of_scope_atlas_id:O10", res["errors"])
        self.assertIn("B3-change-impact:atlas_ids_mismatch", res["errors"])
        self.assertIn("B3-change-impact:missing_o16_single_count_rule", res["errors"])
        self.assertIn("T1:incomplete_contract_elements", res["errors"])

    def test_sa010_blocks_measures_when_audit_use_statement_not_agreed_or_backdated(self) -> None:
        sample = {
            "programme-coordinator": {
                "participant_count": 5,
                "unaided_under_5m_count": 4,
                "manual_fallback_completed_count": 5,
                "sus_median": 74.0,
            }
        }
        unagreed = up.default_programme_plan().audit_use_agreement
        with self.assertRaisesRegex(ValueError, "SA-010 gate: staff audit-use statement"):
            up.evaluate_role_measures(sample, unagreed, measurement_date="2026-11-15")

        unnamed_rep = dataclasses.replace(_agreed_sa010(), staff_representatives=("system",))
        with self.assertRaisesRegex(ValueError, "named human representative"):
            up.evaluate_role_measures(sample, unnamed_rep, measurement_date="2026-11-15")

        bad_date = dataclasses.replace(_agreed_sa010(), agreed_date="15-11-2026")
        with self.assertRaisesRegex(ValueError, "ISO YYYY-MM-DD"):
            up.evaluate_role_measures(sample, bad_date, measurement_date="2026-11-15")

        impossible_date = dataclasses.replace(_agreed_sa010(), agreed_date="2026-02-30")
        with self.assertRaisesRegex(ValueError, "valid calendar ISO date"):
            up.evaluate_role_measures(sample, impossible_date, measurement_date="2026-11-15")

        with self.assertRaisesRegex(ValueError, "measurement_date"):
            up.evaluate_role_measures(sample, _agreed_sa010("2026-11-10"))

        with self.assertRaisesRegex(ValueError, "on or before measurement_date"):
            up.evaluate_role_measures(
                sample,
                _agreed_sa010("2026-11-16"),
                measurement_date="2026-11-15",
            )

        weak_statement = dataclasses.replace(
            _agreed_sa010(),
            statement_text="Results are aggregate only.",
        )
        with self.assertRaisesRegex(ValueError, "disciplinary"):
            up.evaluate_role_measures(sample, weak_statement, measurement_date="2026-11-15")

    def test_sa010_rejects_individual_identifiers_quotes_and_per_participant_rows(self) -> None:
        agreement = _agreed_sa010()
        for forbidden_payload in (
            {"programme-coordinator": {"participant_count": 5, "staff_id": "EMP-01"}},
            {"programme-coordinator": {"participant_count": 5, "participant_quotes": ["slow"]}},
            {
                "programme-coordinator": {
                    "participant_count": 5,
                    "sessions": [{"time_seconds": 190}],
                }
            },
        ):
            with self.assertRaisesRegex(ValueError, "SA-010 aggregate-only violation"):
                up.evaluate_role_measures(
                    forbidden_payload,
                    agreement,
                    measurement_date="2026-11-15",
                )

    def test_sa010_masks_small_cells_below_five_without_leaking_counts_while_keeping_h4_breach(
        self,
    ) -> None:
        evaluated = up.evaluate_role_measures(
            {
                "assessor-designer": {"participant_count": 0},
                "quality-assurance": {
                    "participant_count": 3,
                    "unaided_under_5m_count": 3,
                    "manual_fallback_completed_count": 3,
                    "sus_median": 82.0,
                    "sus_min": 75.0,
                    "sus_max": 90.0,
                    "stop_rule_or_consent_blur_count": 1,
                },
            },
            _agreed_sa010(),
            measurement_date="2026-11-15",
        )
        self.assertEqual(evaluated["cohorts"]["assessor-designer"]["status"], "not_run")
        qa = evaluated["cohorts"]["quality-assurance"]
        self.assertEqual(qa["status"], "suppressed_small_cell")
        self.assertTrue(qa["suppressed"])
        self.assertEqual(qa["suppression_reason"], "cell_below_min_floor_5")
        self.assertIsNone(qa["participant_count"])
        self.assertIsNone(qa["unaided_under_5m_count"])
        self.assertIsNone(qa["unaided_under_5m_pct"])
        self.assertIsNone(qa["sus_median"])
        self.assertIsNone(qa["stop_rule_or_consent_blur_count"])
        self.assertTrue(qa["h4_stop_rule_breach"])
        self.assertEqual(
            qa["hypothesis_evaluation"]["h4_zero_boundary_breaches"],
            "not_supported",
        )
        self.assertTrue(evaluated["any_h4_stop_rule_breach"])

    def test_evaluate_role_measures_cohorts_t0_applicability_accessible_sus_and_hypotheses(
        self,
    ) -> None:
        evaluated = up.evaluate_role_measures(
            {
                "programme-coordinator": {
                    "participant_count": 5,
                    "unaided_under_5m_count": 4,
                    "manual_fallback_completed_count": 5,
                    "sus_median": 72.5,
                    "sus_min": 65.0,
                    "sus_max": 85.0,
                    "stop_rule_or_consent_blur_count": 0,
                },
                "resident": {
                    "participant_count": 6,
                    "manual_fallback_completed_count": 6,
                    "accessible_sus_alternative_count": 3,
                    "numeric_sus_count": 3,
                    "sus_median": 78.0,
                    "stop_rule_or_consent_blur_count": 0,
                },
            },
            _agreed_sa010(),
            measurement_date="2026-11-15",
        )
        self.assertTrue(evaluated["thresholds_are_hypotheses"])
        self.assertFalse(evaluated["user_validation_established"])
        self.assertFalse(evaluated["human_usability_signoff"])

        coord = evaluated["cohorts"]["programme-coordinator"]
        self.assertEqual(coord["unaided_under_5m_pct"], 80)
        self.assertEqual(
            coord["hypothesis_evaluation"],
            {
                "h1_unaided_under_5m": "supported",
                "h2_sus_at_least_70": "supported",
                "h3_manual_fallback": "supported",
                "h4_zero_boundary_breaches": "supported",
            },
        )

        res = evaluated["cohorts"]["resident"]
        self.assertIsNone(res["unaided_under_5m_count"])
        self.assertEqual(res["hypothesis_evaluation"]["h1_unaided_under_5m"], "not_applicable")
        self.assertEqual(res["hypothesis_evaluation"]["h2_sus_at_least_70"], "inconclusive")
        self.assertIsNone(res["sus_median"])

        with self.assertRaisesRegex(ValueError, "Proxy pilot"):
            up.evaluate_role_measures(
                {"proxy-pilot": {"participant_count": 2, "unaided_under_5m_count": 2}},
                _agreed_sa010(),
                measurement_date="2026-11-15",
            )

    def test_evaluate_role_measures_rejects_impossible_counts_and_invalid_sus_ranges(self) -> None:
        agreement = _agreed_sa010()
        with self.assertRaisesRegex(ValueError, "cannot exceed 5"):
            up.evaluate_role_measures(
                {"finance-grants": {"participant_count": 5, "unaided_under_5m_count": 6}},
                agreement,
                measurement_date="2026-11-15",
            )
        with self.assertRaisesRegex(ValueError, "between 0.0 and 100.0"):
            up.evaluate_role_measures(
                {
                    "finance-grants": {
                        "participant_count": 5,
                        "unaided_under_5m_count": 4,
                        "sus_median": 105.0,
                    }
                },
                agreement,
                measurement_date="2026-11-15",
            )
        with self.assertRaisesRegex(ValueError, "sus_min <= sus_median <= sus_max"):
            up.evaluate_role_measures(
                {
                    "finance-grants": {
                        "participant_count": 5,
                        "unaided_under_5m_count": 4,
                        "sus_min": 80.0,
                        "sus_median": 70.0,
                        "sus_max": 90.0,
                    }
                },
                agreement,
                measurement_date="2026-11-15",
            )

    def test_findings_log_enforces_severity_anonymisation_backlog_links_and_retest_rules(
        self,
    ) -> None:
        f1 = up.log_finding(
            finding_id="UF-001",
            target_id="T4",
            cohort_id="programme-coordinator",
            severity=4,
            observation="Pending handoff badge needed chase-owner prompt on narrow screen.",
            impact="Coordinator hesitated before identifying sender retention rule.",
            backlog_issue="#155",
        )
        f2 = up.log_finding(
            finding_id="UF-002",
            target_id="R-J3",
            cohort_id="resident",
            severity=2,
            status="accepted_risk",
            observation="Printed appointment sheet uses two-page table at 18pt font.",
            impact="Minor page turn during telephone confirmation.",
            backlog_issue="https://github.com/jmservera/ama/issues/155",
            risk_owner="Jordan Clarke",
            risk_rationale="18pt spacing preserved for readability pending print redesign.",
        )
        summary = up.validate_findings_log((f1, f2))
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["open_blocker_ids"], ["UF-001"])

        with self.assertRaisesRegex(ValueError, "invalid_or_missing_backlog_issue"):
            up.log_finding(
                finding_id="UF-003",
                target_id="T1",
                cohort_id="programme-coordinator",
                severity=3,
                observation="Filter chip persisted.",
                impact="Confusion across scope.",
                backlog_issue="no issue yet",
            )
        with self.assertRaisesRegex(ValueError, "email_identifier_in_finding_text"):
            up.log_finding(
                finding_id="UF-004",
                target_id="T1",
                cohort_id="programme-coordinator",
                severity=2,
                observation="Participant user@example.org missed filter.",
                impact="Minor delay.",
                backlog_issue="#155",
            )
        with self.assertRaisesRegex(ValueError, "accepted_risk_requires_named_human_owner"):
            up.log_finding(
                finding_id="UF-005",
                target_id="T1",
                cohort_id="programme-coordinator",
                severity=1,
                status="accepted_risk",
                observation="Minor copy hesitation.",
                impact="Low impact.",
                backlog_issue="#155",
                risk_owner="system",
                risk_rationale="Automated.",
            )
        with self.assertRaisesRegex(ValueError, "cannot_mark_retested_from_synthetic_walkthrough"):
            up.log_finding(
                finding_id="UF-006",
                target_id="T8",
                cohort_id="provider-contractor",
                severity=4,
                status="retested",
                evidence_source="synthetic_walkthrough",
                observation="Worker receipt wording.",
                impact="Boundary risk.",
                backlog_issue="#155",
            )

    def test_outcome_evaluation_preserves_negative_and_inconclusive_and_blocks_omission(
        self,
    ) -> None:
        neg = up.OutcomeRecord(
            target_id="T8",
            outcome="not_supported",
            evidence_source="moderated_participant",
            not_user_validation=False,
            validation_label=up.MODERATED_PARTICIPANT_LABEL,
            summary="Two contractor participants misread receipt timestamp as QA acceptance.",
            negative_or_failure_notes=("Receipt banner required stronger non-acceptance wording.",),
        )
        inc = up.OutcomeRecord(
            target_id="R-R1",
            outcome="inconclusive",
            evidence_source="moderated_participant",
            not_user_validation=False,
            validation_label=up.MODERATED_PARTICIPANT_LABEL,
            summary="Only three authorised representatives completed sessions in wave 1.",
            negative_or_failure_notes=("Sub-5 cell suppressed; recruitment continuing.",),
        )
        evaluated = up.evaluate_programme_results(
            (neg, inc),
            audit_use_agreed=True,
            dpo_approved=True,
            expected_target_ids=("T8", "R-R1"),
        )
        self.assertEqual(evaluated["negative_outcomes_retained"], ["T8"])
        self.assertEqual(evaluated["inconclusive_outcomes_retained"], ["R-R1"])
        self.assertFalse(evaluated["user_validation_established"])
        self.assertFalse(evaluated["human_usability_signoff"])

        with self.assertRaisesRegex(ValueError, "negative_or_failure_notes"):
            up.evaluate_programme_results(
                (dataclasses.replace(neg, negative_or_failure_notes=()),),
            )
        with self.assertRaisesRegex(ValueError, "omitted expected targets"):
            up.evaluate_programme_results((inc,), expected_target_ids=("T8", "R-R1"))

    def test_synthetic_and_proxy_outcomes_enforce_non_validation_labels(self) -> None:
        bad_syn = up.OutcomeRecord(
            target_id="T0",
            outcome="supported",
            evidence_source="synthetic_walkthrough",
            not_user_validation=False,
            validation_label=up.SYNTHETIC_WALKTHROUGH_LABEL,
            summary="Synthetic check.",
        )
        with self.assertRaisesRegex(ValueError, "not_user_validation=True"):
            up.evaluate_programme_results((bad_syn,))

        bad_label = dataclasses.replace(
            bad_syn,
            not_user_validation=True,
            validation_label="Validated usability run",
        )
        with self.assertRaisesRegex(ValueError, "exact label"):
            up.evaluate_programme_results((bad_label,))

        proxy_rec = up.OutcomeRecord(
            target_id="T1",
            outcome="supported",
            evidence_source="proxy_participant",
            not_user_validation=True,
            validation_label=up.PROXY_PARTICIPANT_LABEL,
            summary="Proxy landlord coordinator completed T1.",
        )
        res = up.evaluate_programme_results(
            (proxy_rec,),
            audit_use_agreed=True,
            dpo_approved=True,
        )
        self.assertFalse(res["user_validation_established"])
        self.assertFalse(res["human_usability_signoff"])

    def test_build_synthetic_walkthrough_report_exercises_contracts_and_retains_negatives(
        self,
    ) -> None:
        report = up.build_synthetic_walkthrough_report()
        self.assertTrue(report.not_user_validation)
        self.assertEqual(report.validation_label, "Synthetic walkthrough - not user validation")
        self.assertFalse(report.user_validation_established)
        self.assertFalse(report.human_usability_signoff)
        self.assertEqual(report.same_home_clean_status, "complete_in_shape")
        self.assertIn(
            "same_home.handover:worker_receipt_treated_as_acceptance",
            report.same_home_negative_probe_blockers,
        )
        self.assertEqual(report.o16_reconciled_owner, "change-impact")
        self.assertGreater(report.outcome_counts["supported"], 0)
        self.assertGreater(report.outcome_counts["not_supported"], 0)
        self.assertGreater(report.outcome_counts["inconclusive"], 0)
        for rec in report.records:
            self.assertTrue(rec.not_user_validation)
            self.assertEqual(rec.validation_label, up.SYNTHETIC_WALKTHROUGH_LABEL)

    def test_markdown_specification_matches_contract_and_keeps_human_sessions_not_run(
        self,
    ) -> None:
        text = SPEC_PATH.read_text(encoding="utf-8")
        plan = up.default_programme_plan()
        self.assertIn("ms.date: 2026-11-17", text)
        self.assertIn(up.SYNTHETIC_WALKTHROUGH_LABEL, text)
        self.assertIn("not_user_validation = True", text)
        self.assertIn("SA-010", text)
        self.assertNotIn("no issue yet", text.casefold())
        self.assertIn("| None recorded |", text)
        self.assertIn("| All 13 representative role cohorts and `proxy-pilot` |", text)
        for script in plan.tasks:
            self.assertIn(f"`{script.script_id}`", text)
        for cohort in plan.cohorts:
            self.assertIn(f"`{cohort.cohort_id}`", text)

    def test_markdown_specification_scopes_a_demo_first_desktop_only_slice(self) -> None:
        text = SPEC_PATH.read_text(encoding="utf-8")
        heading = "## Demo-first, desktop-only first slice"
        self.assertIn(heading, text)
        section = text.split(heading, 1)[1].split("\n## ", 1)[0]
        script_ids = {script.script_id for script in up.default_programme_plan().tasks}
        for needle in (
            "api/web/",
            "resident_demo/web/",
            "1280 CSS px",
            "Synthetic showcase - not a live resident service",
            up.SYNTHETIC_WALKTHROUGH_LABEL,
            "No participant data",
        ):
            self.assertIn(needle, section)
        for script_id in ("T0", "T4", "T5", "R-J1", "R-J2", "R-J3"):
            self.assertIn(script_id, script_ids)
            self.assertIn(f"`{script_id}`", section)


if __name__ == "__main__":
    unittest.main()

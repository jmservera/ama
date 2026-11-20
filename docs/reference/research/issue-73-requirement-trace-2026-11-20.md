---
title: Epic 73 requirement trace to checks or deferrals (2026-11-20, demo)
description: Engineering trace from each requirement named in epic 73 to a repository test or a recorded deferral, guarded by an offline drift test
ms.date: 2026-11-20
---

Refs #73. Synthetic demo, desktop only. No Azure resource was created or changed. This is an engineering trace, not acceptance: it ticks nothing in any issue and records no owner, DPO, legal or assistive-technology approval.

## Method

* Requirements are those listed in the issue body: BG-011, FR-001 to FR-007, FR-032, FR-034 and NFR-003 (BRD and PRD).
* AC ids come from the PRD traceability table in [the PRD](../../prds/zava-forward-retrofit-programme-demonstrator.md); the check is the closest existing test, chosen by reading its name and body.
* A test existing and passing shows the covered behaviour only; it does not prove the whole requirement. The partial coverage is stated per row.
* [test_epic_73_requirement_trace.py](../../../tools/test_epic_73_requirement_trace.py) fails if a row, cited file or cited test disappears. It does not run the cited tests; the run result is recorded below.

## Trace

| Requirement | Status | ACs | Check or reason |
| --- | --- | --- | --- |
| BG-011 | Deferred | n/a | Outcome measure (assessment-to-ready-to-install time, manual coordination hours); measured in the pilot, so no demo test can prove it. Only the cost-line gate is tested: `src/core/tests/test_governance.py::test_ai_running_cost_line_is_required_before_capture` |
| FR-001 | Checked | AC-001, AC-002, AC-043 | `src/core/tests/test_home_case.py::test_recorded_versions_are_retained_and_conflicts_refused`; `src/api/tests/test_home_case_api.py::test_version_recorded_through_http_and_retained` |
| FR-002 | Checked | AC-001, AC-002, AC-003, AC-043 | `src/core/tests/test_buildings.py::test_shared_id_and_clear_building_never_satisfy_target_home_gates`; `src/api/tests/test_home_case_api.py::test_payload_keeps_building_and_home_records_in_separate_regions` |
| FR-003 | Checked | AC-004, AC-005, AC-060 | `src/api/tests/test_entra_authoritative.py::test_anonymous_unassigned_wrong_tenant_and_bad_oid_are_denied`. Live sign-in is a separate demo proof |
| FR-004 | Checked | AC-006 | `src/api/tests/test_task_queue_api.py::test_metadata_filters_csv_and_consistent_context`. Owner-approved definition of new and priority stays a human decision |
| FR-005 | Checked | AC-007, AC-008 | `src/core/tests/test_home_case.py::test_recorded_versions_are_retained_and_conflicts_refused`; `src/core/tests/test_bulk_edits.py::test_noops_never_invent_history_or_edit_version` |
| FR-006 | Checked | AC-009 | `src/core/tests/test_bulk_edits.py::test_exact_preview_before_apply_and_provenance_reopens`; `src/api/tests/test_bulk_edit_api.py::test_mixed_targets_noops_and_blocked_apply_have_ordered_outcomes` |
| FR-007 | Checked | AC-009, AC-010 | `src/core/tests/test_bulk_edits.py::test_every_controlled_field_and_unknown_input_refused_and_audited` |
| FR-032 | Checked | AC-034 | `src/api/tests/test_workbench.py::test_ac034_scope_reset_checks_follow_default_manifest`. Focus and announcement on reset need browser or AT evidence |
| FR-034 | Checked | AC-036, AC-040 | `src/api/tests/test_role_screens_same_home_identity.py::test_mismatched_record_is_withheld_not_relabelled` |
| NFR-003 | Checked | AC-050 | `src/api/tests/test_home_case_api.py::test_non_finance_staff_get_no_cost_amounts_over_http`. Covers the finance field slice only; wider field access remains unproven here |

## Run result

On 2026-11-20 every cited test file passed in full: `src/core` test_home_case (8), test_buildings (9), test_bulk_edits (39), test_governance (88, 18 skipped); `src/api` test_home_case_api, test_entra_authoritative, test_task_queue_api, test_bulk_edit_api, test_workbench and test_role_screens_same_home_identity (65 together). The drift test passes (4).

## Epic 73 criteria after this note

Criterion 3 stays unticked: 10 requirements have a partial test trace and BG-011 is deferred to the pilot, but no owner has recorded the deferral. Criteria 1 and 2 are unchanged.

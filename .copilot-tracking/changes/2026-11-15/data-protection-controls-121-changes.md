<!-- markdownlint-disable-file -->
# RPI Changes: Issue #121 Whole-System Data Protection, Retention, Derivative Dispatch, and Rights-Request Controls

## Metadata

* Task ID: issue-121-data-protection-controls
* Related plan: .copilot-tracking/plans/2026-11-15/data-protection-controls-121-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (P01, P02, P03)
* Completed scope markers: P01, P01-T01, P01-T02, P01-T03, P02, P02-T01, P03, P03-T01, P03-T02
* All remaining active-plan markers: none
* Status basis: Completed all P01, P02, and P03 tasks across code, unit tests, documentation/KB sync, focused validation, and repo-local privacy-safe Git configuration.

## Execution Summary

Delivered the full deterministic local engineering, unit-testing, and documentation slice for Issue #121 (`Refs #121`) across `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/tests/test_data_protection.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, and `docs/reference/log.md`. All focused validation checks, KB doc-guard tests, and API caller regressions passed with zero issues.

## Completed Work

### Whole-system inventory, task manifests, derivative dispatch, and rights ledger (P01, P01-T01, P01-T02, P01-T03)

* Files changed: `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/sqlstore.py`
* Summary:
  * `P01-T01`: Added `SUBJECT_POPULATIONS`, `WHOLE_SYSTEM_SURFACES`, `HOSTING_REGION_VS_INFERENCE_RESIDENCY` (plus `HOSTING_VS_INFERENCE_RESIDENCY`), expanded `DATA_CLASSES` to 10 classes (`fixture_resident` constructed + 9 actual classes including `tenant_identity` and `provider_retained_copy`), and enriched `register_report(env)` without echoing secret/reference values.
  * `P01-T02`: Expanded `TASKS` across all 10 tasks (`rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, `case_brief`, `read_document`, `funding_draft`, `priority`) with `permitted_fields` + `fields` alias, aligned `SPECIAL_FIELDS` with `regulatory_privacy.SPECIAL_CATEGORY_FIELDS`, hardened `validate_task_payload` (empty/permission-only payloads denied, `bool` rejected for `int` fields), and enforced fail-closed attachment dispatch in `model_dispatch` and `dispatch_attachment_to_model` with `user_permission_establishes_necessity=False` and `storage_approves_ai_dispatch=False`.
  * `P01-T03`: Implemented `RightsRequestLedger`, `record_rights_request`, `log_rights_action`, `answer_rights_request`, and polymorphic `rights_status` supporting `Store`, `SqlStore` (`"rights_requests"` registered in `SqlStore.DOCS` and `SqlStore.MERGE_PRESERVED_DOCS`), and atomic JSON files, preserving 1-calendar-month deadlines, `locate`/`export`/`erase` action logs, non-synthetic human actor validation, `subject_key`-free metadata audit entries, and strict separation of `local_deleted` from `provider_erasure_confirmed=False`.

### Focused unit test coverage (P02, P02-T01)

* Files changed: `src/core/tests/test_data_protection.py`
* Summary: Retained all 23 existing tests (`none` removed) and added 9 focused, strictly typed test methods (`32` total tests) across `WholeSystemInventoryAndNecessityTests`, `IntactAttachmentDispatchControlTests`, and `RightsRequestLedgerPersistenceTests` proving subject-population/residency separation, 9 actual data/processing classes across all 8 surfaces, whole-system `TASKS` necessity validation with `user_permission_granted=True`, `storage_permission_granted=True` intact-attachment denial vs human `reviewed_redacted` / `scoped_necessity_ref` with no `OR` rescue, and persisted `RightsRequestLedger` roundtrips across `Store`, SQLite `SqlStore` reopen, and JSON files (`local_deleted` vs `provider_erasure_confirmed=False`).

### Documentation sync, focused validation, and Git identity setup (P03, P03-T01, P03-T02)

* Files changed: `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, `docs/reference/log.md`
* Summary:
  * `P03-T01`: Updated `### Data protection register and dispatch gate (#121)` in `src/core/README.md`, updated `ms.date: 2026-11-15` and appended `## Whole-System Processing, Derivative Dispatch and Rights-Request Controls (2026-11-15, Refs #121)` in `docs/reference/research/chat-memory-dpia.md` while keeping blank `D1`..`D8` and `#217` sections untouched, refreshed the `docs/reference/README.md` index entry, and appended a `[2026-11-15]` entry to `docs/reference/log.md`.
  * `P03-T02`: Executed all focused validation checks plus KB/API caller regression suites (`0` errors/failures) and configured repo-local privacy-safe Git identity (`8036360+jmservera@users.noreply.github.com`, `Juan Manuel Servera`) on `feat/core-121-data-protection-controls`.

## Implementation-Time Plan and Detail Updates

* Immediately relevant current-state update (`P03-T02`): Aligned `P03-T02` wording in `.copilot-tracking/plans/2026-11-15/data-protection-controls-121-plan.md` and `.copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md` so `P03-T02` completes focused validation and repo-local Git identity configuration before `rpi-review`, while the single frozen `git commit` runs immediately after `rpi-review` writes its review artifact and finalizes the RPI session state (avoiding commit amendments while capturing every `.copilot-tracking/` artifact in one clean commit).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| ruff check | data_protection.py, sqlstore.py, test_data_protection.py | Passed | `All checks passed!` (exit 0) |
| ruff format --check | data_protection.py, test_data_protection.py | Passed | `2 files already formatted` (exit 0) |
| mypy --strict | src/core (369 source files) | Passed | `Success: no issues found in 369 source files` (exit 0) |
| unittest (target) | src/core/tests/test_data_protection.py | Passed | `Ran 32 tests in 0.064s - OK` (exit 0) |
| unittest (KB & dispatch guards) | test_chat_dpia_record.py, test_regulatory_privacy.py, test_ai_dispatch_marker.py | Passed | `Ran 32 tests in 0.241s - OK` (exit 0) |
| unittest (API callers) | src/api/tests/test_ai_tasks.py, test_role_endpoint_inventory.py | Passed | Exit 0 across `/api/data-protection` and AI task endpoints |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`..`P03` and `P01-T01`..`P03-T02` checked with completion evidence)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled (`0` blockers, `0` remaining active-plan items)
* Review readiness: ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none (all active plan items `P01`..`P03` complete; post-Review single local Git commit queued for automatic RPI closeout).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/data-protection-controls-121-plan.md, `## Follow-Up Items`
* Named DPO confirmation of lawful basis per data class and Article 17(3) audit data position, plus Legal retention schedule and `DH-006` processor/transfer approval before any real personal data processing (`Refs #121`; owner: DPO and Legal).
* Authenticated DPO/intake HTTP routes over `RightsRequestLedger` in `src/api` once `D8` intake role and identity-verification procedures are ratified (owner: platform engineering after DPO `D8` decision).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: P01, P01-T01, P01-T02, P01-T03, P02, P02-T01, P03, P03-T01, P03-T02; remaining: none
* Validation coverage: complete focused validation tier passed (ruff check, ruff format --check, mypy across 369 files, 32 data_protection unit tests, 32 KB/dispatch guard tests, and API caller regressions)
* Blockers: none
* Current plan and detail updates: P03-T02 commit timing aligned so single clean commit includes post-Review tracking artifacts without amend
* Planning and critique state: implementation-ready (PC-001..PC-004 adopted and verified in implementation)
* Follow-up items: 2 external/future items mirrored from plan
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: parent confirmed automatic RPI Agent

<!-- markdownlint-disable-file -->
# RPI Plan: Issue #121 Whole-System Data Protection, Retention, Derivative Dispatch, and Rights-Request Controls

## Task Metadata

* Task ID: issue-121-data-protection-controls
* Task slug: data-protection-controls-121
* Planning status: implementation-ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/data-protection-controls-121-plan-critique.md

## Executive Summary

This plan delivers the deterministic local engineering, unit-testing, and knowledge-base documentation slice for Issue #121 (*Data protection, retention and rights controls*) inside `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/sqlstore.py` (registering `"rights_requests"` in `SqlStore.DOCS`), `src/core/tests/test_data_protection.py`, `src/core/README.md`, and `docs/reference/research/chat-memory-dpia.md`. It closes the local Responsible AI processing, derivative-dispatch, and statutory rights-tracking gaps while preserving the strict governance boundary that recorded technical references do not constitute DPO or Legal sign-off (`dpo_reviewed=False`) and local record deletion never confirms external model-provider erasure (`provider_erasure_confirmed=False`).

### User Decisions and Requirements Highlights

* **Whole-system RAI processing and retention inventory**: Separate constructed resident fixtures (`fixture_resident`) from current staff/tenant identities, review records, and future real resident processing across explicit `subject_population` values (`constructed_resident_fixture`, `current_staff_identity`, `current_tenant_identity`, `current_review_record`, `future_real_resident`), report `hosting_region_vs_inference_residency` (`uk_hosting_does_not_prove_uk_inference_residency: True`), and cover all 9 actual data/processing classes (`staff_identity`, `tenant_identity`, `review_record`, `future_real_resident`, `raw_document`, `prompt_output`, `audit_ledger`, `telemetry`, `provider_retained_copy`).
* **Whole-system task manifest and necessity gate**: Expand `TASKS` to cover `rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, and `case_brief` with `purpose`, `audience`, `permitted_fields` (field name -> `(type, max_length)`, plus backward-compatible `fields` alias), `prohibited`, and `necessity`, ensuring `user_permission_granted=True` never establishes task necessity or bypasses field, type, length, special-category, or derivative checks.
* **Intact attachment model-dispatch control**: Enforce in `model_dispatch` and `dispatch_attachment_to_model` that upload/store/download permission (`storage_permission_granted=True`) never approves sending intact document or image bytes to AI; require either an authorized `reviewed_redacted` derivative with human non-synthetic `redaction_reviewer_id` and `redaction_review_id`, or a non-synthetic `scoped_necessity_ref` / `necessity_exception`, failing closed to `manual_path` otherwise.
* **Persisted store-backed and JSON-serializable rights-request ledger**: Provide `RightsRequestLedger`, `record_rights_request`, `log_rights_action`, `answer_rights_request`, and polymorphic `rights_status` with timezone-aware receipt timestamps, 1-calendar-month statutory deadlines, `locate`/`export`/`erase` action logs, and strict separation of `local_deleted` from `provider_erasure_confirmed=False`.
* **Focused validation and non-closing commit boundary**: Run focused `ruff`, `mypy`, and `unittest` checks only, link with `Refs #121` (never closing `#121`), and leave a clean frozen local commit on `feat/core-121-data-protection-controls` without pushing or opening a PR.

### What You May Not Know

* Neither `data_protection.py` nor `test_data_protection.py` has a `mypy` override in `src/core/pyproject.toml`, meaning every new type, store adapter (`typing.Protocol`), and test helper must pass `mypy --strict` across all 369 core files.
* Existing callers in `ai.py`, `ai_tasks.py`, `regulatory_privacy.py`, and `api/server.py` invoke `register_report`, `dispatch_hold`, and `document_model_hold`, and existing tests in `test_data_protection.py` assert `spec["fields"]` and 3-argument `model_dispatch("raw_document", env, "reviewed_redacted")` for legacy `read_document`. Keeping `fields` aliased to `permitted_fields` and enforcing reviewer/review IDs unconditionally on `dispatch_attachment_to_model` and `task="look_at_attachment"` (plus whenever reviewer/review kwargs are passed) satisfies the new attachment gate with zero legacy breakage.
* `docs/reference/research/chat-memory-dpia.md` is the canonical indexed DPIA synthesis guarded by regex tests in `src/core/tests/test_chat_dpia_record.py` and `src/core/tests/test_regulatory_privacy.py`; adding a dedicated dated H2 section at the end of `chat-memory-dpia.md` preserves every guarded table and blank DPO decision cell.
* Because this worktree shares a non-sandboxed host whose editable install points to `/home/azureuser/source/ama/src/core/src`, `unittest` invocations must prefix `PYTHONPATH=src/core/src:src/core/tests` so the current worktree is tested without mutating shared `pip` state.

### Unresolved Decisions or Blockers

* None for the scoped local engineering and documentation slice. External human DPO and Legal sign-offs (`DH-001`, `DH-002`, `DH-003`, `DH-006`, `DH-007`) remain intentionally open and recorded under `Refs #121`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`rpi-research`, `rpi-plan` including `rpi-plan-critique`, `rpi-implement`, and `rpi-review`) writing dated artifacts under `.copilot-tracking/*/2026-11-15/` for Issue #121 (caller prompt).
* Work on branch `feat/core-121-data-protection-controls` stacked on `feat/demo-164-chat-grounding-provenance-0900` (PR #1641), using `Refs #121` without any closing keyword because human DPO/Legal sign-offs remain open (caller prompt; Issue #121).
* Map current staff/tenant identities and review records (`staff_identity`, `tenant_identity`, `review_record`, `future_real_resident`) separately from constructed resident fixtures (`fixture_resident`) with explicit `subject_population` (`constructed_resident_fixture`, `current_staff_identity`, `current_tenant_identity`, `current_review_record`, `future_real_resident`), `hosting_region_vs_inference_residency` (`uk_hosting_does_not_prove_uk_inference_residency: True`), and whole-system coverage across inputs, raw document/image bytes (`raw_document`), prompts/outputs/citations (`prompt_output`), reviewer identity (`review_record`), audit (`audit_ledger`), telemetry/tokens (`telemetry`), and provider processing and retained copies (`provider_retained_copy`) (caller prompt Objective 1; PRD `DH-001`..`DH-007`).
* Expand `TASKS` in `data_protection.py` to cover whole-system AI tasks (`rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, `case_brief`) declaring `purpose`, `audience`, `permitted_fields` (`field -> (type, max_length)`), `prohibited`, and `necessity`, and enforce in `validate_task_payload` and `model_dispatch` that `user_permission_granted=True` alone never establishes task necessity or bypasses field/length/special-category/derivative checks (caller prompt Objective 1).
* Enforce intact document/image model-dispatch control (`look_at_attachment` / `raw_document` in `model_dispatch` and `dispatch_attachment_to_model`): `storage_permission_granted=True` does not approve sending intact material to AI; require either an authorized `reviewed_redacted` derivative (with `redaction_reviewer_id` and `redaction_review_id`) or an explicitly scoped non-synthetic necessity approval (`scoped_necessity_ref` / `necessity_exception`), otherwise deny model dispatch (`permitted=False`) and preserve `manual_path` (caller prompt Objective 1).
* Add a persisted store-backed and JSON-serializable rights-request workflow (`RightsRequestLedger`, `record_rights_request`, `answer_rights_request`, `rights_status`) with receipt timestamp, 1-calendar-month statutory deadline calculation, `locate`/`export`/`erase` action log, and explicit separation between `local_deleted` and `provider_erasure_confirmed=False` (caller prompt Objective 1; PRD `DH-004`, `DH-007`).
* Document the whole-system processing, derivative-dispatch, and rights-request contract in `src/core/README.md` and a dedicated section in `docs/reference/research/chat-memory-dpia.md` (with `docs/reference/README.md` index sync and `docs/reference/log.md` append) (caller prompt Objective 2; research `C8`, `C11`, `C12`).
* Add focused unit tests in `src/core/tests/test_data_protection.py` proving all five behavioral areas, run focused tier validation only (`ruff check`, `ruff format --check`, `mypy` in `src/core`, and `unittest` on `test_data_protection*.py` plus KB doc-guard tests), and create a clean frozen local commit with the Copilot co-author trailer without pushing or opening a PR (caller prompt Objectives 3 and Validation Tier).

## Goals

* Deliver a deterministic, strictly typed whole-system RAI processing and retention inventory in `data_protection.py` covering constructed fixtures separately from all 9 actual data/processing classes and distinguishing UK application hosting from inference residency.
* Enforce minimum-necessary per-task field manifests across all whole-system AI tasks and fail-closed derivative/scoped-necessity gates on intact document and image bytes regardless of storage or user permissions.
* Deliver a durable, `Store`-backed and JSON-serializable rights-request workflow with 1-month deadline tracking, `locate`/`export`/`erase` action logging, and non-conflation of local deletion with provider erasure.
* Synchronize module and knowledge-base documentation and verify behavior with deterministic focused unit tests and static analysis.

## Scope and Non-Goals

### In Scope

* Updating `src/core/src/zava_forward/core/data_protection.py` with expanded `DataClass` metadata, 10 `DATA_CLASSES` (1 constructed + 9 actual), `HOSTING_REGION_VS_INFERENCE_RESIDENCY`, expanded `TASKS` (including legacy `"read_document"` alongside the 7 whole-system AI tasks), `validate_task_payload` and `model_dispatch` necessity/payload enforcement, `dispatch_attachment_to_model`, and `RightsRequestLedger` / `record_rights_request` / `log_rights_action` / `answer_rights_request` / `rights_status`, plus registering `"rights_requests"` in `SqlStore.DOCS` and `SqlStore.MERGE_PRESERVED_DOCS` in `src/core/src/zava_forward/core/sqlstore.py` so store-backed rights requests survive both JSON `Store` and `SqlStore` reopen/sync without new SQL DDL.
* Extending `src/core/tests/test_data_protection.py` with unit test suites covering population/residency separation, all 9 actual data/processing classes, all 8 task manifests and payload/task necessity boundaries, intact attachment dispatch denial/approval paths, and persisted rights-request lifecycle across `Store`, `SqlStore`, and JSON serialization.
* Updating `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
* Running focused tier checks and committing cleanly on `feat/core-121-data-protection-controls`.

### Non-Goals

* Adding a standalone governance microservice, new SQL DDL tables, or new HTTP endpoints in `src/api`.
* Inventing legal conclusions, numerical retention schedules, DPO sign-offs, or confirmed provider erasure claims.
* Running full-tier Docker, Azure SQL, or Chromium browser gates.
* Pushing to `origin`, opening/updating a GitHub PR, or closing Issue #121.

## Functional Requirements

* **FR-1 (Subject population and residency separation)**: `DataClass` and `register_report(env)` expose `subject_population` across `constructed_resident_fixture`, `current_staff_identity`, `current_tenant_identity`, `current_review_record`, and `future_real_resident`, group constructed vs actual populations explicitly, cover all 9 actual data/processing classes (`staff_identity`, `tenant_identity`, `review_record`, `future_real_resident`, `raw_document`, `prompt_output`, `audit_ledger`, `telemetry`, `provider_retained_copy`) across all whole-system surfaces (`inputs`, `raw_document_bytes`, `prompts_outputs_citations`, `reviewer_identity`, `audit`, `telemetry_tokens`, `provider_processing`, `provider_retained_copies`), and emit `hosting_region_vs_inference_residency` with `uk_hosting_does_not_prove_uk_inference_residency: True` while never echoing reference values.
  * Observable acceptance criteria: `register_report` returns `dpo_reviewed=False`, all 5 `subject_population` buckets, all 9 actual classes, `hosting_region_vs_inference_residency["uk_hosting_does_not_prove_uk_inference_residency"] is True`, and zero echoed env reference values.
* **FR-2 (Whole-system task manifest and non-sufficiency of user permission)**: `TASKS` defines `rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, and `case_brief`, each with `purpose`, `audience`, `permitted_fields` (and `fields` alias), `prohibited`, and `necessity`. `validate_task_payload` and `model_dispatch` accept `user_permission_granted: bool = False`, report `user_permission_establishes_necessity=False`, deny undeclared tasks or payloads containing only invalid/undeclared/special-category fields even when `user_permission_granted=True`, and strip undeclared/special-category/over-length fields without echoing field values in error lists.
  * Observable acceptance criteria: Every required task exists in `TASKS` with non-empty manifest keys; `validate_task_payload` and `model_dispatch` reject undeclared tasks and disallowed payloads even when `user_permission_granted=True`.
* **FR-3 (Intact attachment derivative and scoped necessity dispatch gate)**: `dispatch_attachment_to_model` and `model_dispatch` (for `look_at_attachment` / `raw_document`) deny model dispatch when `storage_permission_granted=True` unless `raw_document` class gates are recorded (non-synthetic) AND either (a) `derivative == "reviewed_redacted"` with human non-synthetic `redaction_reviewer_id` and `redaction_review_id`, or (b) a valid non-synthetic `scoped_necessity_ref` or `necessity_exception` is supplied; every denial returns `permitted=False`, `storage_approves_ai_dispatch=False`, and `manual_path`.
  * Observable acceptance criteria: Intact material with `storage_permission_granted=True` returns `permitted=False` and `manual_path`; `reviewed_redacted` with human reviewer/review IDs or valid non-synthetic `scoped_necessity_ref` returns `permitted=True`; synthetic `SYNTH-` references or automated reviewer identities return `permitted=False`.
* **FR-4 (Persisted rights-request workflow and local-vs-provider erasure boundary)**: `RightsRequestLedger` supports `Store`-backed persistence (`store.data["rights_requests"]` + `store.save()` + metadata-only `store.audit()`), atomic JSON file persistence (`Path | str`), and `to_dict`/`to_json`/`from_dict`/`from_json` serialization, with module-level helpers `record_rights_request`, `log_rights_action`, `answer_rights_request`, and polymorphic `rights_status`. Each request records timezone-aware `received_at`, 1-calendar-month clamped `due_at`, `actions` (`locate`, `export`, `erase`), optional `answered_at`, `local_deleted`, and `provider_erasure_confirmed=False`, rejecting any attempt to represent local deletion as confirmed provider erasure.
  * Observable acceptance criteria: Requests persist across JSON file reopen and `Store.save()` cycles, enforce 1-month deadlines (`open`, `overdue`, `answered`, `answered_late`), log `locate`/`export`/`erase` actions without storing personal content in audit details, and keep `provider_erasure_confirmed is False` even when `local_deleted is True` (raising `ValueError` if a caller tries to assert `provider_erasure_confirmed=True`).

## Non-Functional Requirements

* **NFR-1 (Strict static typing and lint cleanliness)**: All modified Python modules pass strict type-checking and Ruff lint/format rules.
  * Objective threshold or evaluation condition: Zero errors from `(cd src/core && python3 -m mypy)`, `python3 -m ruff check`, and `python3 -m ruff format --check`.
  * Operating condition or verification approach, if needed: Run directly against `src/core` without adding `mypy` exclusions or `# type: ignore` suppressions in `data_protection.py`.
  * Observable acceptance criteria: Exit code `0` on all three static checks.
* **NFR-2 (Backward compatibility and zero secret/PII leakage)**: Existing callers (`ai.py`, `ai_tasks.py`, `regulatory_privacy.py`, `api/server.py`) and existing KB doc-guard tests continue to pass, and neither reference values nor dropped special-category payload values are echoed in report or audit strings.
  * Objective threshold or evaluation condition: 100% pass rate on `test_data_protection.py`, `test_chat_dpia_record.py`, `test_regulatory_privacy.py`, and `test_ai_dispatch_marker.py`.
  * Operating condition or verification approach, if needed: Run `unittest` with `PYTHONPATH=src/core/src:src/core/tests` and `TMPDIR=/dev/shm`.
  * Observable acceptance criteria: All existing and added unit tests pass with exit code `0`.

## Acceptance Criteria

* [ ] `DATA_CLASSES` and `register_report(env)` separate `fixture_resident` (`constructed_resident_fixture`) from `staff_identity` (`current_staff_identity`), `tenant_identity` (`current_tenant_identity`), `review_record` (`current_review_record`), and `future_real_resident` (`future_real_resident`), cover all 9 actual data/processing classes including `provider_retained_copy`, and report `hosting_region_vs_inference_residency` with `uk_hosting_does_not_prove_uk_inference_residency: True`.
* [ ] `TASKS` declares `rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, and `case_brief` with `purpose`, `audience`, `permitted_fields` (plus `fields`), `prohibited`, and `necessity`, and `validate_task_payload` / `model_dispatch` enforce that `user_permission_granted=True` never establishes necessity or bypasses checks.
* [ ] `dispatch_attachment_to_model` and `model_dispatch` deny intact attachment AI dispatch even when `storage_permission_granted=True` unless `reviewed_redacted` (with human non-synthetic `redaction_reviewer_id` and `redaction_review_id`) or a non-synthetic `scoped_necessity_ref` / `necessity_exception` is provided, preserving `manual_path`.
* [ ] `RightsRequestLedger`, `record_rights_request`, `log_rights_action`, `answer_rights_request`, and `rights_status` persist rights requests via `Store` or JSON serialization, compute 1-calendar-month statutory deadlines, log `locate`/`export`/`erase` actions, and keep `local_deleted` strictly separate from `provider_erasure_confirmed=False`.
* [ ] `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, and `docs/reference/log.md` accurately document the contract while preserving all doc-guard assertions and unchecked DPO release gates.
* [ ] Test ownership and budget lock: canonical test target is `src/core/tests/test_data_protection.py` (exact removals: `none`; maximum additions: up to 18 focused semantic and negative-boundary test methods across inventory/residency, task manifests, attachment dispatch, and persisted `Store`/`SqlStore`/JSON rights workflow; generated targets: `none`). All focused validation commands pass cleanly and changes are committed locally on `feat/core-121-data-protection-controls` with `Refs #121` and Copilot trailer.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/data-protection-controls-121-plan.md                                                                  |
| Phase details                    | .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md                                                       |
| Latest critique                  | .copilot-tracking/reviews/2026-11-15/data-protection-controls-121-plan-critique.md with `Revise` resolved directly via PC-001..PC-004    |
| Relevant research                | .copilot-tracking/research/2026-11-15/data-protection-controls-121-research.md                                                           |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/data-protection-controls-121-changes.md is created by implementation as its evidence record         |
| Planning execution and readiness | Complete; implementation-ready after direct disposition of PC-001..PC-004                                                                |
| Continuation context             | Confirmed automatic RPI Agent parent return; continues automatically to `rpi-implement`                                                  |

## Sources

* .copilot-tracking/research/2026-11-15/data-protection-controls-121-research.md: Grounded codebase findings `C1`..`C15` across callers, `mypy --strict`, `Store` hooks, and KB guard tests.
* src/core/src/zava_forward/core/data_protection.py: Existing 8-class register, 3-task manifest, necessity-exception validator, model-dispatch holds, and in-memory rights clock.
* src/core/tests/test_data_protection.py: Existing 23 unit tests pinning backward-compatible register, dispatch, task payload, rights clock, and projection behavior.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: Requirements `DH-001`..`DH-007`, `PR-001`, `PR-003`, and v0.16.0 RAI processing/retention contract (`MAP-02`).
* docs/reference/research/chat-memory-dpia.md: Canonical indexed KB privacy/DPIA working record guarded by `test_chat_dpia_record.py` and `test_regulatory_privacy.py`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement whole-system data protection inventory, task manifests, attachment dispatch, and rights ledger

* Intent: Extend `src/core/src/zava_forward/core/data_protection.py` with the complete Issue #121 RAI processing/retention inventory, whole-system task necessity manifests, intact attachment dispatch gate, and persisted store/JSON rights-request ledger under strict `mypy`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Expand DataClass inventory, subject populations, whole-system surfaces, and residency posture

* Requirement and evidence: FR-1; research `C1`, `C2`, `C6`, `C10`.
* Expected result: `DATA_CLASSES` covers `fixture_resident` (`constructed`) plus all 9 `actual` classes (`staff_identity`, `tenant_identity`, `review_record`, `future_real_resident`, `raw_document`, `prompt_output`, `audit_ledger`, `telemetry`, `provider_retained_copy`) with explicit `subject_population` and `processing_surfaces`, and `register_report(env)` reports `subject_populations`, `whole_system_coverage`, and `hosting_region_vs_inference_residency` (`uk_hosting_does_not_prove_uk_inference_residency: True`) without echoing reference values.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Expand whole-system TASKS manifest and enforce non-sufficiency of user permission and intact attachment gates

* Requirement and evidence: FR-2, FR-3; research `C2`, `C3`, `C4`, `C15`.
* Expected result: `TASKS` covers `rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`, `look_at_attachment`, `intake_summary`, and `case_brief` with `purpose`, `audience`, `permitted_fields` (and `fields` alias), `prohibited`, and `necessity`; `validate_task_payload` and `model_dispatch` enforce `user_permission_establishes_necessity=False`; `dispatch_attachment_to_model` and `model_dispatch` reject intact material even with `storage_permission_granted=True` unless human non-synthetic `reviewed_redacted` (`redaction_reviewer_id` + `redaction_review_id`) or non-synthetic `scoped_necessity_ref` / `necessity_exception` is provided.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Implement persisted Store-backed and JSON-serializable RightsRequestLedger workflow

* Requirement and evidence: FR-4, NFR-1; research `C2`, `C9`, `C14`, `C15`; critique `PC-001`.
* Expected result: `RightsRequestLedger`, `record_rights_request`, `log_rights_action`, `answer_rights_request`, and polymorphic `rights_status` persist requests across `Store` and `SqlStore` (`"rights_requests"` registered in `SqlStore.DOCS` and `SqlStore.MERGE_PRESERVED_DOCS`, lock-scoped dynamic access, atomic `audit`/`save` ordering, `subject_key`-free metadata-only `.audit()`) and atomic JSON files, enforce timezone-aware receipt and 1-month deadlines, record `locate`/`export`/`erase` action logs, and keep `local_deleted` strictly separate from `provider_erasure_confirmed=False`.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Add focused unit tests for inventory, manifests, attachment dispatch, and rights persistence

* Intent: Prove every Issue #121 behavioral contract and negative boundary in `src/core/tests/test_data_protection.py` while preserving all 23 existing unit tests.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add inventory, residency, task-manifest, attachment-dispatch, and persisted rights tests

* Requirement and evidence: FR-1..FR-4, NFR-1, NFR-2; research `C9`, `C13`, `C15`.
* Expected result: `src/core/tests/test_data_protection.py` retains all existing tests (`none` removed) and adds <=18 focused semantic and boundary tests proving subject-population and residency separation, 9 actual data/processing classes, 7-task manifest necessity validation with `user_permission_granted=True`, `storage_permission_granted=True` intact-attachment denial vs valid `reviewed_redacted` / `scoped_necessity_ref`, and `Store`/JSON persisted rights lifecycle with 1-month deadline and `local_deleted` vs `provider_erasure_confirmed=False` separation.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Synchronize documentation, run focused validation, and prepare frozen local commit

* Intent: Update `src/core/README.md` and knowledge-base records, verify all focused lint/type/unit/doc-guard checks pass, and configure repository-local privacy-safe Git identity for the post-Review single clean commit on `feat/core-121-data-protection-controls`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Update core README and knowledge-base privacy synthesis, index, and log

* Requirement and evidence: User Objective 2; research `C7`, `C8`, `C11`, `C12`.
* Expected result: `src/core/README.md` (`### Data protection register and dispatch gate (#121)`), `docs/reference/research/chat-memory-dpia.md` (new dated `#121` H2 section, preserving guarded `#163` and `#217` sections), `docs/reference/README.md`, and `docs/reference/log.md` accurately describe the implemented controls and remaining DPO/Legal gates.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Run focused validation suite and configure Git identity for frozen local commit

* Requirement and evidence: NFR-1, NFR-2, Caller Validation Tier; research `C9`, `C11`, `C12`, `C13`.
* Expected result: `ruff check`, `ruff format --check`, `(cd src/core && python3 -m mypy)`, and worktree-isolated `unittest` runs (`test_data_protection*.py`, `test_chat_dpia_record.py`, `test_regulatory_privacy.py`, `test_ai_dispatch_marker.py`) exit `0`; repository-local privacy-safe Git identity (`{id}+{login}@users.noreply.github.com`) is configured on `feat/core-121-data-protection-controls` ready for the single post-Review frozen commit containing all code, docs, and `.copilot-tracking/` artifacts without pushing.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md

## Dependencies

* Existing `zava_forward.core.doc_controls.scan_status` and `Store` persistence contract (`data`, `lock`, `save`, `audit`): used via structural `Protocol` typing so `data_protection.py` stays pure stdlib + core without new packages or SQL DDL.
* External human DPO and Legal governance approvals (`DH-001`..`DH-007`): intentionally out-of-band; keep `dpo_reviewed=False` and `Refs #121`.

## Critique Disposition

Single-pass `rpi-plan-critique` executed in `.copilot-tracking/reviews/2026-11-15/data-protection-controls-121-plan-critique.md` (`Verdict: Revise`, 4 `planner-direct` findings, 0 user decisions required). All four findings are adopted directly in this finalized plan and phase details:

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| 2026-11-15 / PC-001 [High] | adopted | Added `src/core/src/zava_forward/core/sqlstore.py` (`SqlStore.DOCS` + `MERGE_PRESERVED_DOCS` registration for `"rights_requests"` with zero SQL DDL), lock-scoped dynamic `store.data["rights_requests"]` access, `hasattr(store, "db")` atomic `audit`-before-`save` ordering, `subject_key`-free audit details, `"id"` + `"request_id"` fields, polymorphic helper target support, `SqlStore` reopen tests (`P02-T01`), and `ruff check` coverage (`P03-T02`). |
| 2026-11-15 / PC-002 [High] | adopted | Updated `P01-T02` and `P02-T01` to include `"read_document"` in `TASKS`, align `SPECIAL_FIELDS` with `regulatory_privacy.SPECIAL_CATEGORY_FIELDS`, deny empty `not kept` payloads and safely validate `int` (rejecting `bool`) vs `str` limits in `validate_task_payload`, validate `task in TASKS` ahead of `c.kind == "constructed"` in `model_dispatch`, and enforce optional `payload` checks in `model_dispatch` regardless of `user_permission_granted=True`. |
| 2026-11-15 / PC-003 [Medium] | adopted | Updated `P01-T02` and `P02-T01` to enforce strict fail-closed precedence (no `OR` rescue when `derivative == CONSTRUCTED_DERIVATIVE`, reviewer/review IDs are invalid, or `necessity_exception` is invalid), case-insensitive `.upper().startswith("SYNTH-")`, unconditional `user_permission_establishes_necessity=False` and `storage_approves_ai_dispatch=False` keys on every dispatch return path, and kwarg forwarding in `dispatch_hold` and `document_model_hold`. |
| 2026-11-15 / PC-004 [Low] | adopted | Standardized on `HOSTING_REGION_VS_INFERENCE_RESIDENCY`, ordered defaulted `subject_population` and `processing_surfaces` fields cleanly on `DataClass`, and distinguished `tenant_identity` (`current_tenant_identity` signed-in tenant/representative account claims) from `future_real_resident` (`future_real_resident` household/case personal data). |

## Follow-Up Items

* Obtain named DPO confirmation of lawful basis per data class and Article 17(3) audit data position, plus Legal retention schedule and `DH-006` processor/transfer approval before any real personal data processing (`Refs #121`; owner: DPO and Legal).
* Expose authenticated DPO/intake HTTP routes over `RightsRequestLedger` in `src/api` once `D8` intake role and identity-verification procedures are ratified in `docs/reference/research/chat-memory-dpia.md` (outside immediate `src/core` slice; owner: platform engineering after DPO `D8` decision).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/data-protection-controls-121-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none

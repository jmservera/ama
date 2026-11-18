<!-- markdownlint-disable-file -->
# Review: Issue #121 Whole-System Data Protection, Retention, Derivative Dispatch, and Rights-Request Controls

## Scope and Evidence

* Task ID: issue-121-data-protection-controls
* Review date: 2026-11-15
* Review scope: full task (P01, P02, P03)
* Assessed boundary: Deterministic local engineering, unit-testing, and documentation slice for Issue #121 (`Refs #121`) across `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/tests/test_data_protection.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, and `docs/reference/log.md` under the focused validation tier.
* Plan: .copilot-tracking/plans/2026-11-15/data-protection-controls-121-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/data-protection-controls-121-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/data-protection-controls-121-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/data-protection-controls-121-research.md, focused `ruff`/`mypy`/`unittest` execution results, KB guard tests, and independent bounded `rubber-duck` lens check.

## Opening Review State

* Interpreted review goal: Verify that every planned requirement, critique disposition (`PC-001`..`PC-004`), documentation update, and focused validation gate for Issue #121 (`Refs #121`) is completely, accurately, and safely delivered without scope creep, regressions, or premature governance claims.
* Review scope: full task (P01, P01-T01, P01-T02, P01-T03, P02, P02-T01, P03, P03-T01, P03-T02)
* Evidence readiness: Ready; plan markers, phase details, critique dispositions, and changes record are reconciled.
* Acceptance basis: User Objective & Scope 1..3, FR-1..FR-4, NFR-1..NFR-2, AC-1..AC-6, and adopted critique dispositions `PC-001`..`PC-004`.
* First comparison boundary: Compare `P01`..`P03` plan/detail commitments and `PC-001`..`PC-004` resolutions against workspace source/doc diffs and focused validation results.
* Active read-only boundaries: Write access limited strictly to `.copilot-tracking/reviews/2026-11-15/data-protection-controls-121-review.md`; no source or prior tracking mutations.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass assessment on 2026-11-15 across reconciled `P01`..`P03` artifacts, `PC-001`..`PC-004` critique dispositions, workspace source and documentation diffs, focused validation runs, KB/API regression checks, and bounded read-only `rubber-duck` inspection.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| P01 (P01-T01, P01-T02, P01-T03) | Whole-system inventory, task manifests, derivative dispatch, and rights ledger | Reconciled | All 10 `DATA_CLASSES`, `SUBJECT_POPULATIONS`, `WHOLE_SYSTEM_SURFACES`, `HOSTING_REGION_VS_INFERENCE_RESIDENCY`, 10-task `TASKS` manifest, fail-closed attachment dispatch, and `Store`/`SqlStore`/JSON `RightsRequestLedger` match plan and phase details. |
| P02 (P02-T01) | Focused unit test coverage | Reconciled | All 23 baseline tests preserved (`0` removals) and 9 strictly typed test methods added (`32` total, within `<= 18` addition ceiling) covering every behavioral requirement and `PC-001`..`PC-004` boundary. |
| P03 (P03-T01, P03-T02) | Documentation sync, focused validation, and Git identity setup | Reconciled | `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, and `docs/reference/log.md` updated cleanly; focused validation suite and repo-local privacy-safe Git identity verified. |
| Follow-Up Items | External DPO/Legal sign-offs and future `src/api` DPO intake routes | Reconciled | Preserved outside active `Pxx` / `Pxx-Txx` completion claims in both plan and changes record (`dpo_reviewed=False`, `Refs #121`). |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| P01-T01 | `src/core/src/zava_forward/core/data_protection.py` | Separated `fixture_resident` (`constructed`) from 9 `actual` classes across `SUBJECT_POPULATIONS` and `WHOLE_SYSTEM_SURFACES`, adding `HOSTING_REGION_VS_INFERENCE_RESIDENCY` (`uk_hosting_does_not_prove_uk_inference_residency: True`) and enriched `register_report`. | Symbol and diff inspection; zero secret/reference echoing. | `ruff`, `mypy --strict`, `WholeSystemInventoryAndNecessityTests` passed. | Reconciled |
| P01-T02 | `src/core/src/zava_forward/core/data_protection.py` | Expanded `TASKS` across 10 tasks with `permitted_fields` + `fields` alias, aligned `SPECIAL_FIELDS`, hardened `validate_task_payload` (empty/bool-int rejection), and enforced `user_permission_establishes_necessity=False` and fail-closed `storage_approves_ai_dispatch=False` in `model_dispatch`, `dispatch_attachment_to_model`, `dispatch_hold`, and `document_model_hold`. | Symbol and diff inspection; no `OR` fallback rescue on invalid derivative/exception inputs. | `ruff`, `mypy --strict`, `WholeSystemInventoryAndNecessityTests` and `IntactAttachmentDispatchControlTests` passed. | Reconciled |
| P01-T03 | `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/sqlstore.py` | Added `RightsRequestLedger`, `record_rights_request`, `log_rights_action`, `answer_rights_request`, and polymorphic `rights_status` persisted across `Store`, `SqlStore` (`"rights_requests"` in `DOCS` + `MERGE_PRESERVED_DOCS`), and JSON files with 1-month deadlines, non-synthetic human actor checks, `subject_key`-free audit details, and `local_deleted` vs `provider_erasure_confirmed=False`. | Symbol and diff inspection; zero new SQL DDL. | `ruff`, `mypy --strict`, `RightsRequestLedgerPersistenceTests` (`Store`, `SqlStore` reopen, JSON roundtrip) passed. | Reconciled |
| P02-T01 | `src/core/tests/test_data_protection.py` | Added 9 focused unit test methods across 3 test classes without removing or altering any of the 23 existing tests. | Test diff and execution log (`32` tests run). | `ruff check`, `ruff format --check`, `mypy --strict`, `unittest -v` passed. | Reconciled |
| P03-T01 | `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/README.md`, `docs/reference/log.md` | Documented whole-system inventory, derivative dispatch, and persisted rights ledger; preserved guarded `#163`/`#217` sections and `dpo_reviewed=False`. | Clean ASCII diff (`0` `.copilot-tracking` refs, `0` em dashes). | `test_chat_dpia_record.py` and `test_regulatory_privacy.py` passed. | Reconciled |
| P03-T02 | Repository-local Git config and focused check targets | Executed focused validation tier and configured repo-local privacy-safe Git email (`8036360+jmservera@users.noreply.github.com`). | Command exit codes `0` and verified `git config user.email`. | Full focused tier + API caller regression tests passed. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| P03-T02 | Clarified that `P03-T02` executes focused validation and repo-local Git identity setup prior to `rpi-review`, while the single frozen `git commit` executes immediately after `rpi-review` writes its review artifact and finalizes RPI session state. | User prompt instruction to run the full RPI loop through `rpi-review` and commit all changes and `.copilot-tracking/` artifacts cleanly in a frozen local commit without pushing. | Synchronized `P03` / `P03-T02` in `.copilot-tracking/plans/2026-11-15/data-protection-controls-121-plan.md`, `.copilot-tracking/details/2026-11-15/data-protection-controls-121-phase-details.md`, and `.copilot-tracking/changes/2026-11-15/data-protection-controls-121-changes.md`. | Not needed; immediately relevant current-state update preserving confirmed user intent (`PC-001`..`PC-004` unaffected). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All 4 `planner-direct` findings (`PC-001`..`PC-004`) in `.copilot-tracking/reviews/2026-11-15/data-protection-controls-121-plan-critique.md` were adopted in planning and verified in the delivered code and unit tests (`SqlStore.DOCS` + `MERGE_PRESERVED_DOCS`, `"read_document"` + strict `int`/`not kept` payload checks, fail-closed attachment precedence without `OR` rescue, and `HOSTING_REGION_VS_INFERENCE_RESIDENCY` + `tenant_identity` separation).
* Material revisions: None; only the non-divergent `P03-T02` commit-sequencing clarification above occurred during implementation.
* Dependent-work pause assessment: No pause required; execution followed dependency order `P01` -> `P02` -> `P03`.
* Justification assessment: Supported by repository and caller constraints (capturing all RPI artifacts in one clean commit without rewriting history).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Named DPO confirmation of per-class lawful basis and Article 17(3) audit data position, plus Legal retention schedule and `DH-006` processor/transfer sign-off (`Refs #121`) | Requires qualified human DPO and Legal governance authority (`DH-001`, `DH-002`, `DH-006`, `DH-007`), which code cannot fabricate. | Named DPO and Legal owner (Juan Manuel Servera in exercise governance). | Open external governance prerequisite; routed as distinct follow-up (`Refs #121` preserved, `dpo_reviewed=False`). |
| Authenticated DPO/intake HTTP endpoints over `RightsRequestLedger` in `src/api` once `D8` intake role and identity-verification procedures are ratified | Depends on open DPO decision `D8` in `docs/reference/research/chat-memory-dpia.md` and extends into `src/api` routes outside `src/core`. | Platform engineering after DPO `D8` ratification. | Open future slice; routed as distinct follow-up (incorporating `RV-001` HTTP/multi-writer boundary hardening). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Future HTTP and multi-writer boundary hardening for `RightsRequestLedger` (`DocumentStateStore` recovery and opaque-slug enforcement)

* Related scope: Follow-Up Items (future `src/api` HTTP exposure of `P01-T03`)
* Evidence: `src/core/src/zava_forward/core/data_protection.py` (`RightsRequestLedger._commit_unlocked`, `record_request`, `log_action`, `answer_request`), `src/core/src/zava_forward/core/sqlstore.py` (`SqlStore.save`), and `src/core/src/zava_forward/core/aftercare_store.py` (`DocumentStateStore`). Within `src/core`, `SqlStore.save()` already invokes `_discard()` on `ConflictError`/`GateError`/`PermissionError`, `store.lock` serializes in-process writes, and `subject_key` is excluded from `audit_detail`. When untrusted HTTP callers or concurrent standalone file writers are introduced in `src/api`, wrapping `SqlStore` writes in `DocumentStateStore`-style unconfirmed-write recovery, using `NamedTemporaryFile` per file flush, and restricting `request_id`/`target_scope`/`outcome` to strict opaque ASCII slugs (`^[A-Za-z0-9._:-]+$`) will harden the external boundary.
* Impact: Non-blocking for the deterministic `src/core` engineering slice (`P01`..`P03` conformant); prevents caller-supplied freeform identifiers from carrying embedded personal data into audit strings or leaving unconfirmed state if exposed over concurrent HTTP routes later.
* Destination: follow_up
* Smallest useful next action: Include strict opaque-slug regex checks, `NamedTemporaryFile` atomic swaps, and `DocumentStateStore`-style SQL failure recovery when exposing authenticated DPO/intake HTTP routes over `RightsRequestLedger`, or as an optional `src/core` hardening follow-up.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| RV-001 | distinct follow-up | Platform engineering (before or alongside `src/api` DPO intake HTTP route exposure) | Non-blocking boundary hardening outside active `src/core` slice acceptance criteria |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Future boundary hardening (`RV-001`): Enforce strict opaque-slug regexes on `request_id`/`target_scope`/`outcome`, unique `NamedTemporaryFile` flushes on standalone path ledgers, and `DocumentStateStore`-style generic SQL failure recovery before exposing `RightsRequestLedger` to concurrent HTTP routes in `src/api`.
* External human governance sign-offs (`Refs #121`): Named DPO lawful-basis/DPIA/Article 17(3) confirmation and Legal retention/transfer (`DH-006`) approvals remain open external gates (`dpo_reviewed=False`).

## Blockers and Remaining Work

* Blockers: none for the deterministic local engineering and documentation slice (`Refs #121` human DPO/Legal approvals remain external issue-closure prerequisites, as explicitly scoped by the caller).
* Remaining active work: none (`P01`..`P03` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m ruff check src/core/src/zava_forward/core/data_protection.py src/core/src/zava_forward/core/sqlstore.py src/core/tests/test_data_protection.py` | Modified `src/core` production and test files | Passed | `All checks passed!` (exit 0) |
| `python3 -m ruff format --check src/core/src/zava_forward/core/data_protection.py src/core/tests/test_data_protection.py` | Modified `data_protection` source and test files | Passed | `2 files already formatted` (exit 0) |
| `(cd src/core && python3 -m mypy)` | Full `src/core` package (`strict = true` on `data_protection` and tests) | Passed | `Success: no issues found in 369 source files` (exit 0) |
| `PYTHONPATH=src/core/src:src/core/tests TMPDIR=/dev/shm python3 -m unittest discover -s src/core/tests -p "test_data_protection*.py" -v` | `src/core/tests/test_data_protection.py` | Passed | `Ran 32 tests in 0.064s - OK` (23 baseline + 9 new tests, exit 0) |
| `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests TMPDIR=/dev/shm python3 -m unittest src/core/tests/test_chat_dpia_record.py src/core/tests/test_regulatory_privacy.py src/core/tests/test_ai_dispatch_marker.py -q` | KB DPIA doc guards and AI dispatch marker regressions | Passed | `Ran 32 tests in 0.241s - OK` (exit 0) |
| `PYTHONPATH=src/api/src:src/api/tests:src/core/src:src/core/tests:src/agents/src:src/agents/tests TMPDIR=/dev/shm python3 -m unittest src/api/tests/test_ai_tasks.py src/api/tests/test_role_endpoint_inventory.py -q` | `src/api` `/api/data-protection` and AI task endpoint callers | Passed | Exit 0 across API endpoint callers |
| Full Docker/SQL/browser RPI gate (`tools/rpi-checks.py --all`) | Repository-wide full gate | Skipped | Explicitly excluded by caller instruction (`Run focused validation only (do NOT run the full Docker/SQL/browser gate)`). |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every active-scope functional and non-functional requirement (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`), acceptance criterion (`AC-1`..`AC-6`), documentation/KB sync requirement, and adopted critique disposition (`PC-001`..`PC-004`) is completely implemented and verified by passing lint, format, strict `mypy`, unit, KB guard, and API caller checks, with zero active-scope defects and honest preservation of open human DPO/Legal gates (`Refs #121`, `dpo_reviewed=False`). One non-blocking `Low` future boundary-hardening item (`RV-001`) is routed cleanly to distinct follow-up work.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Platform engineering (`RV-001` opaque-slug/SQL-recovery hardening alongside `src/api` DPO intake routes) and DPO/Legal (`Refs #121` human sign-offs) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`ruff check`, `ruff format --check`, `mypy` across 369 files, 32 `test_data_protection` tests, 32 KB/dispatch guard tests, API caller regressions); full Docker/SQL/browser gate skipped per caller instruction.
* Blockers: none


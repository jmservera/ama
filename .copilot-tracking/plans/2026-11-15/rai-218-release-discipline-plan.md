<!-- markdownlint-disable-file -->
# RPI Plan: Epic #218 Responsible AI Release, Challenge and Incident Control

## Task Metadata

* Task ID: issue-218-rai-release-discipline
* Task slug: rai-218-release-discipline
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/rai-218-release-discipline-plan-critique.md

## Executive Summary

This plan delivers the executable Responsible AI (RAI) control-plane enforcement, requirement traceability, and separated readiness reporting for GitHub Epic #218 across `src/core` and `src/api`. It introduces `src/core/src/zava_forward/core/rai_control_plane.py` and integrates it with the release admission, audit ledger, governance, and status-reporting paths so that live AI task activation is deterministically blocked and audited without named human approval (`OQ-017`), all 15 RAI epic requirements map machine-readably to verifiable tests or explicit deferrals, and operators can inspect `rai_exercise_acceptance` separately from `real_ai_delivery_gate`.

### User Decisions and Requirements Highlights

* **Deterministic `OQ-017` live activation gate with audit emission**: Any attempt to activate a live AI task without both a non-empty named human `approved_by` and a non-empty `named_approval_id` is rejected with `OQ-017` and emits a tamper-evident audit record even when the SQL release write rolls back.
* **Complete 15-requirement machine-readable traceability**: `FR-051` to `FR-054`, `NFR-014`, `AC-069` to `AC-073`, `OQ-017` to `OQ-019`, `RULE-024`, and `RULE-020` each resolve to concrete passing acceptance/unit test targets in the repository and, where live authority, fairness sign-off, or Legal/DPO screening remains open, an explicit structured deferral.
* **Separated `rai_exercise_acceptance` and `real_ai_delivery_gate` sections**: Both `src/core` readiness/live reports and `src/api` status payloads emit distinct `rai_exercise_acceptance` and `real_ai_delivery_gate` sections so offline or disabled-AI modes verify RAI safeguards without masquerading as a passing live-model cut-over gate.
* **Focused validation and frozen local commit**: Validate with `unittest`, `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check` on `src/core` and `src/api` without running `tools/rpi-checks.py`, then commit locally on `feat/rai-218-release-discipline` without pushing or opening a PR.

### What You May Not Know

* `GET /api/ai/report` has an existing regression test (`src/api/tests/test_heldout_eval_api.py`) asserting the exact top-level key set `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}`, and `src/api/tests/test_role_endpoint_inventory.py` enforces an exact server route inventory. Emitting `rai_exercise_acceptance` and `real_ai_delivery_gate` inside `report["live"]` (`store.ai_live_report`) as well as on `GET /api/governance` (`store.governance_view`), `GET /api/assistants` (`assistants.registry`), and `store.rai_readiness_report()` satisfies both `src/core` and `src/api` callers cleanly without breaking existing contract tests.
* In `src/core/src/zava_forward/core/assistants.py`, `record_release` runs inside a SQL transaction that rolls back on `PermissionError` or `ValueError`, and `SqlStore.audit()` buffers to thread-local `pending` when called inside `with store.lock:`. To ensure rejected live activation attempts leave durable audit evidence across both JSON `Store` and `SqlStore`, rejection handling commits immediately via `store._audit_immediate` on SQL stores (or `with store.lock:` + `store.audit` on JSON stores) and commits its `live-activation-rejected` event outside the rolled-back `assistant_releases` insert.

### Unresolved Decisions or Blockers

* None for implementation scope. Live organizational appointments (`OQ-017`), representative fairness/threshold approvals (`OQ-018`), Legal/DPO automated-decision/EU AI Act screening (`OQ-019`), and live phase release sign-off (`RULE-020`) remain explicit owner deferrals recorded in the traceability table rather than fabricated in software.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing dated artifacts under `.copilot-tracking/` (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `changes/2026-11-15/`, `reviews/2026-11-15/`, and `reviews/logs/2026-11-15/`) for issue #218.
* Work in `/home/azureuser/source/ama-demo-wt/feat-218-rai-release` on branch `feat/rai-218-release-discipline` targeting base branch `feat/demo-164-chat-grounding-provenance-0900` (PR #1641).
* Enforce that no live activation of an AI task succeeds without named human approval (`OQ-017`): inspect/implement `src/core/src/zava_forward/core/rai_control_plane.py` and release/assistant governance paths so any attempt to activate a live AI task without a non-empty named human approver (`approved_by` and `named_approval_id`) is deterministically rejected (`OQ-017`) with audit record emission.
* Provide a machine-readable requirement-to-acceptance traceability table/helper covering `FR-051` to `FR-054`, `NFR-014`, `AC-069` to `AC-073`, `OQ-017` to `OQ-019`, `RULE-024`, and `RULE-020`, mapping each to its passing unit/acceptance test or explicit live/owner deferral.
* Ensure the exercise acceptance / RAI readiness report across `src/core` and `src/api` status/readiness payloads emits a distinct `rai_exercise_acceptance` section separated from `real_ai_delivery_gate` so operators verify RAI controls independently of live model cut-over (docs/case_study_48_addendum.md).
* Use the focused validation tier (`src/core` and `src/api` unit tests + `mypy` + `ruff check` + `ruff format --isolated --line-length 100 --check`) and do NOT run `tools/rpi-checks.py`.
* Commit all code changes and `.copilot-tracking/` RPI artifacts on `feat/rai-218-release-discipline` with trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing or opening a pull request.

## Goals

* Enforce deterministic fail-closed `OQ-017` named-human approval (`approved_by` and `named_approval_id`) and durable audit emission across both direct control-plane live activation and SQL/HTTP live release recording.
* Publish an authoritative, machine-verifiable requirement-to-acceptance and deferral traceability structure in `src/core` covering all 15 Epic #218 requirements, rules, acceptance criteria, and open questions.
* Expose distinct, side-by-side `rai_exercise_acceptance` and `real_ai_delivery_gate` readiness sections in `src/core` and `src/api` status/readiness payloads while preserving all existing endpoint schemas and role boundaries.

## Scope and Non-Goals

### In Scope

* Creating `src/core/src/zava_forward/core/rai_control_plane.py` with `OQ-017` live activation validation/execution + audit emission, 15-item requirement traceability table/helpers, and separated `rai_exercise_acceptance` / `real_ai_delivery_gate` reporting.
* Integrating `rai_control_plane` with `rai_release.py`, `assistant_release.py`, `assistants.py`, `ai_tasks.py`, `governance.py`, `store.py`, `src/core/tests/release_support.py`, and `src/api/src/zava_forward/api/server.py`.
* Concise component documentation updates in `src/core/README.md` and `src/api/README.md`.
* Focused unit tests in `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py`, plus full `src/core` and `src/api` unit, type, lint, and format checks.

### Non-Goals

* Running `tools/rpi-checks.py`, browser Playwright harnesses, or hosted Azure deployments.
* Modifying frontend web files under `src/api/src/zava_forward/api/web/`, Bicep templates under `infra/`, or GitHub Actions workflows.
* Fabricating live organizational appointments (`OQ-017`), live fairness clearance (`OQ-018`), or Legal/DPO sign-off (`OQ-019`).
* Pushing to `origin` or opening/updating a GitHub pull request.

## Functional Requirements

* **FR-PLAN-01 (`OQ-017` live activation gate and audit)**: `rai_control_plane.activate_live_task`, `assistant_release.record` (when `evidence_class == "actual"` or `live=True`), and `assistants.record_release` (`POST /api/assistants/releases`) must reject any live AI task activation lacking a non-empty named human `approved_by` (rejecting blank, non-human/system/agent/bot/AI, and placeholder/fictional/unapproved tokens) or lacking a non-empty `named_approval_id` (rejecting blank, placeholder, unknown, or system tokens), or targeting an unregistered/disabled task, citing `OQ-017` and emitting an audit entry (`rai_live_activation_rejected` on `store.audit` plus committed `live-activation-rejected` on SQL `assistant_events` when SQL is active).
  * Observable acceptance criteria: Unit and API tests verify deterministic `OQ-017` rejection and audit record emission across missing, blank, system/bot, placeholder, unappointed, and disabled-task inputs, while `store.verify_audit()` remains True.
* **FR-PLAN-02 (Machine-readable 15-requirement traceability)**: `rai_control_plane.requirement_traceability()` and `traceability_summary()` must return deterministic machine-readable records covering `FR-051`, `FR-052`, `FR-053`, `FR-054`, `NFR-014`, `AC-069`, `AC-070`, `AC-071`, `AC-072`, `AC-073`, `OQ-017`, `OQ-018`, `OQ-019`, `RULE-024`, and `RULE-020`, with each entry pointing to workspace-relative repository test targets (`file::ClassName.test_method`) and/or an explicit structured live/owner deferral.
  * Observable acceptance criteria: Unit tests verify exact ID coverage, zero untraced entries, callable existence across `src/core/tests` (via `importlib` + AST) and `src/api/tests` (via repository-root `ast.parse` in `src/core` tests so isolated `PYTHONPATH=src:tests` and `test_dependency_rule.py` stay clean, plus `importlib` in `src/api` tests), and explicit owner/question deferral fields for live-gated items.
* **FR-PLAN-03 (Separated `rai_exercise_acceptance` vs `real_ai_delivery_gate` payloads)**: `rai_control_plane.exercise_acceptance_report`, `store.rai_readiness_report`, `store.ai_live_report` (`GET /api/ai/report` `live`), `store.governance_view` (`GET /api/governance`), and `assistants.registry` (`GET /api/assistants`) must emit distinct `rai_exercise_acceptance` and `real_ai_delivery_gate` sections where offline/workflow-only/disabled assistance keeps `real_ai_delivery_gate["passed"] == False` while `rai_exercise_acceptance` independently evaluates local RAI controls.
  * Observable acceptance criteria: Core and API unit tests verify both distinct sections exist, `rai_exercise_acceptance["passed"]` is True when local RAI controls hold, `real_ai_delivery_gate["passed"]` remains False when AI is unconfigured, `ZF_AI=off`, or live approvals are absent, and `GET /api/ai/report` preserves its 5 top-level keys.

## Non-Functional Requirements

* **NFR-PLAN-01 (Tamper-evident audit integrity and rollback safety)**
  * Objective threshold or evaluation condition: 100% of rejected live activation attempts append a hash-chained `store.audit` entry whose chain passes `store.verify_audit()`, and SQL `assistant_releases` retains zero active rows from a rejected call.
  * Operating condition or verification approach: Tested under both JSON `Store` and SQLite `SqlStore` / `Assistants` HTTP server fixtures.
  * Observable acceptance criteria: `store.verify_audit()` returns `True` and `assistant_releases` contains no unapproved `actual` row after rejected activation attempts.
* **NFR-PLAN-02 (Static typing, lint, formatting, and zero-regression compatibility)**
  * Objective threshold or evaluation condition: Zero errors from `mypy`, `ruff check`, `ruff format --isolated --line-length 100 --check`, and `unittest discover` across `src/core` and `src/api`.
  * Operating condition or verification approach: Run package-level checks directly in `src/core` and `src/api` without `tools/rpi-checks.py`.
  * Observable acceptance criteria: All existing and newly added `src/core` and `src/api` tests, `mypy`, and `ruff` checks exit 0.

## Acceptance Criteria

* Attempting to activate any live AI task (via `rai_control_plane.activate_live_task`, `assistant_release.record` with `evidence_class="actual"`, or `POST /api/assistants/releases` with `evidence_class="actual"`) without both a non-empty named human `approved_by` and a non-empty `named_approval_id` is deterministically rejected with `OQ-017` and emits a verifiable audit record.
* `rai_control_plane.requirement_traceability()` covers `FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, `OQ-017`..`OQ-019`, `RULE-024`, and `RULE-020` (all 15 IDs), and every entry traces to verified passing unit/acceptance test callables and/or an explicit recorded live/owner deferral.
* `src/core` (`exercise_acceptance_report`, `store.rai_readiness_report`, `store.ai_live_report`, `store.governance_view`, `assistants.registry`) and `src/api` (`GET /api/ai/report`, `GET /api/governance`, `GET /api/assistants`) emit a distinct `rai_exercise_acceptance` section separated from `real_ai_delivery_gate`, and disabling assistance or running offline never reports `real_ai_delivery_gate["passed"] == True`.
* Focused validation (`unittest`, `mypy`, `ruff check`, `ruff format --isolated --line-length 100 --check` on `src/core` and `src/api`) passes cleanly and all changes plus `.copilot-tracking/` artifacts are committed locally on `feat/rai-218-release-discipline` without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/rai-218-release-discipline-plan.md                                                                    |
| Phase details                    | .copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md                                                         |
| Latest critique                  | .copilot-tracking/reviews/2026-11-15/rai-218-release-discipline-plan-critique.md (`Revise`; `PC-001` through `PC-005` resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/rai-218-release-discipline-research.md                                                             |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/rai-218-release-discipline-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and implementation-ready (`ready`)                                                                                              |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to Implement (`P01-T01`)                                                         |

## Sources

* .copilot-tracking/research/2026-11-15/rai-218-release-discipline-research.md: Primary Cycle 1 (`C1`..`C18`) research mapping PRD/BRD specs, release/audit code paths, and contrarian test-compatibility boundaries.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: Authoritative definitions of `FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, and `OQ-017`..`OQ-019`.
* docs/brds/agentic-retrofit-programme-brd.md: Authoritative definitions of `RULE-020` and `RULE-024`.
* docs/case_study_48_addendum.md: Specification requiring exercise acceptance to report RAI checks separately from the real-AI delivery gate so disabled assistance never masquerades as a passing real-AI delivery gate.
* src/core/src/zava_forward/core/rai_release.py, src/core/src/zava_forward/core/assistant_release.py, src/core/src/zava_forward/core/assistants.py, src/core/src/zava_forward/core/store.py, and src/api/src/zava_forward/api/server.py: Existing release, audit, and HTTP status/report modules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement Core RAI Control Plane, OQ-017 Gate, and Traceability

* Intent: Introduce `rai_control_plane.py` and wire `OQ-017` live named-approval enforcement, rejection audit emission, 15-requirement traceability, and separated readiness sections into `src/core`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Author `src/core/src/zava_forward/core/rai_control_plane.py`

* Requirement and evidence: `FR-PLAN-01`, `FR-PLAN-02`, `FR-PLAN-03`, `NFR-PLAN-01`; research evidence `C1`..`C14`
* Expected result: New module providing `LiveActivationApprovalError` (`OQ-017`), `validate_live_task_approval`, `activate_live_task` (with deterministic `store.audit` + SQL event emission on rejection and recording), `REQUIREMENT_TRACEABILITY` / `requirement_traceability` / `traceability_summary` covering all 15 IDs, and `exercise_acceptance_report` emitting distinct `rai_exercise_acceptance` and `real_ai_delivery_gate` sections.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Integrate `rai_control_plane` across `rai_release.py`, `assistant_release.py`, `assistants.py`, `ai_tasks.py`, `governance.py`, `store.py`, and `release_support.py`

* Requirement and evidence: `FR-PLAN-01`, `FR-PLAN-03`, `NFR-PLAN-01`, `NFR-PLAN-02`; research evidence `C5`..`C9`, `C14`..`C17`
* Expected result: `assistant_release.record` and `assistants.record_release` enforce `approved_by` + `named_approval_id` + live threshold approvals on `actual`/live releases and emit `store.audit` + committed `assistant_events` records on rejection; `rai_release.missing_binding` validates `approved_by`/`named_approval_id` when present on live records; `store.rai_readiness_report`, `ai_tasks.live_report`, `governance.governance_view`, and `assistants.registry` emit separated `rai_exercise_acceptance` and `real_ai_delivery_gate`; `release_support.fixture(..., cls="actual")` supplies synthetic `approved_by` and `named_approval_id`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Wire API Readiness Payloads and Component Documentation

* Intent: Ensure `src/api` HTTP endpoints surface live-SQL-aware separated `rai_exercise_acceptance` and `real_ai_delivery_gate` sections compatibly and update `src/core` / `src/api` READMEs.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Wire `assistants` service context into `GET /api/ai/report` and `GET /api/governance` in `server.py` and document in `src/core/README.md` and `src/api/README.md`

* Requirement and evidence: `FR-PLAN-01`, `FR-PLAN-03`, `NFR-PLAN-02`; research evidence `C17`, `C18`
* Expected result: `GET /api/ai/report` (`live`), `GET /api/governance`, and `GET /api/assistants` expose SQL-aware `rai_exercise_acceptance` and `real_ai_delivery_gate` sections while preserving the exact 5 top-level keys of `GET /api/ai/report` and existing server route inventories; `src/core/README.md` and `src/api/README.md` document the new Epic #218 control-plane contract.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Unit Tests and Validation

* Intent: Prove all three Epic #218 acceptance criteria with focused unit tests in `src/core` and `src/api` and pass `unittest`, `mypy`, `ruff check`, and `ruff format --check`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add focused unit tests in `src/core/tests/test_rai_control_plane_218.py` and `src/api/tests/test_rai_release_readiness_api_218.py`

* Requirement and evidence: `FR-PLAN-01`, `FR-PLAN-02`, `FR-PLAN-03`, `NFR-PLAN-01`; locked test budget (0 removals, max 2 new test files, <= 20 focused test methods)
* Expected result: Comprehensive unit and HTTP API tests proving `OQ-017` rejection + audit record emission, 15-requirement traceability with dynamic test-target resolution + recorded deferrals, and separated `rai_exercise_acceptance` vs `real_ai_delivery_gate` across offline, `ZF_AI=off`, unapproved-SQL, and named-human-approved states.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Run focused-tier validation on `src/core` and `src/api`

* Requirement and evidence: `NFR-PLAN-02`; caller validation constraint (no `tools/rpi-checks.py`)
* Expected result: Clean exit 0 for `src/core` and `src/api` `unittest discover`, `mypy`, `ruff check`, and `ruff format --isolated --line-length 100 --check`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md

## Dependencies

* Existing child-issue modules in `src/core` (`rai_release.py`, `assistant_release.py`, `challenges.py`, `continuity.py`, `restart_authority.py`, `cohort_eval.py`, `human_review_effectiveness.py`, `monitoring_coverage.py`, `regulatory_privacy.py`, `governance.py`): Provide the underlying controls referenced by the 15-requirement traceability table and `rai_exercise_acceptance` checks.
* Existing API contract tests (`src/api/tests/test_heldout_eval_api.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/api/tests/test_list_export_inventory.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`): Constrain payload placement and bare-dict `missing_binding` compatibility.

## Critique Disposition

Single final-candidate critique completed in .copilot-tracking/reviews/2026-11-15/rai-218-release-discipline-plan-critique.md with verdict `Revise` and five direct planner-owned technical findings (`PC-001` through `PC-005`), all applied in one coherent batch below with zero unresolved user questions.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [Critical]: `SqlStore.audit()` inside `with store.lock:` buffers to `self.local.pending` without committing | Applied directly | Updated Executive Summary, `P01-T01`, and `P03-T01` so SQL-backed immediate audit persistence calls `store._audit_immediate(...)` directly (bypassing `self.local.pending` buffering) while JSON `Store` acquires `with store.lock:` before `store.audit(...)`, with explicit `sql_store.audit_entries()` + `sql_store.verify_audit()` test coverage. |
| Run 1 `PC-002` [High]: Nested `BEGIN IMMEDIATE` self-deadlock, missing `read_only()`, and omitted `not self.sql` / `?assessment=...` paths | Applied directly | Updated `P01-T01`, `P01-T02`, and `P02-T01` so `exercise_acceptance_report` inspects SQL release state strictly read-only under `with assistant_release.read_only():` via caller-supplied `db` or read-only `store.assistant_connection()` (never opening a nested `BEGIN IMMEDIATE`), `Assistants.registry()` attaches readiness sections on both `not self.sql` and SQL paths, `governance_view` merges outside `with self.lock:`, and `server.py` forwards `assistants_service=app.assistants` on both `/api/governance` paths. |
| Run 1 `PC-003` [High]: Non-existent `monitoring_coverage` helper, `"legacy:"` prefix lookup, and pre-`OQ-017` check ordering | Applied directly | Updated `P01-T01` and `P01-T02` to use `monitoring_coverage.check_monitoring_declaration(..., task_enabled=True, live=True)["missing"]`, normalize `removeprefix("legacy:")` before `ai_registry.get(...)`, and evaluate live `OQ-017` intent (`evidence_class == "actual"` or `bool(body.get("live"))`) ahead of `task not in task_ids` / `not self.sql` while leaving `constructed-fixture` errors untouched. |
| Run 1 `PC-004` [High]: Cross-package `src/api/tests` imports fail isolated `src/core` `PYTHONPATH=src:tests` and `test_dependency_rule.py` | Applied directly | Updated `FR-PLAN-02`, `P01-T01`, and `P03-T01` so traceability descriptors store workspace-relative test paths plus class/method names, verified via `ast.parse` in `src/core` without importing `zava_forward.api` or `zava_forward.agents` and additionally imported in `src/api/tests`. |
| Run 1 `PC-005` [Medium]: New `src/core` files run under `mypy` `strict = true` against untyped migrated `core` modules | Applied directly | Updated `P01-T01` and `P03-T01` to preserve `pyproject.toml` untouched, annotate all new functions/tests completely, and bind untyped migrated `core` modules through `Any`-typed aliases or `Protocol` boundaries. |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/rai-218-release-discipline-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None

<!-- markdownlint-disable-file -->
# RPI Plan: Issue #104 Cross-Capability Bounded AI Enforcement and Verification

## Task Metadata

* Task ID: issue-104-bounded-ai-invariants
* Task slug: issue-104-bounded-ai
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-104-bounded-ai-plan-critique.md

## Executive Summary

This plan delivers explicit cross-capability runtime enforcement and exhaustive acceptance verification across `src/core` and `src/agents` for the two engineering invariants of Issue #104 (`Epic: Bounded AI assistance with human review`):

1. AI never approves, executes, ranks, or mutates controlled records.
2. No registered AI capability is enabled beyond the exercise without finite, owner-approved call, token, and budget limits (and an owned alert).

Codebase research (`C1`–`C20`) confirmed that `zava_forward.core.ai_registry.tasks()` enumerates all 13 registered AI capabilities (`5` proposal-only assistants, `6` retained tasks, `chat-case-conversation`, and `aftercare-concern-pack`), and uncovered four runtime edge bypasses plus missing cross-capability verification in `src/core` and `src/agents`. The plan introduces a strictly typed canonical enforcement and audit module (`zava_forward.core.bounded_ai`), closes all four runtime edge bypasses across `src/core` and `src/agents`, and delivers parameterized 13-capability invariant verification suites in both `src/core/tests/test_epic104_bounded_ai_invariants.py` and `src/agents/tests/test_epic104_bounded_ai_invariants.py`.

### User Decisions and Requirements Highlights

* Execute the full RPI loop continuously without pausing (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) on branch `feat/demo-104-bounded-ai` (stacked child of `feat/demo-164-chat-grounding-provenance-0900`, PR #1641).
* Enforce and verify both Issue #104 invariants across every registered AI capability in `src/core` and `src/agents`.
* Validate under the Focused tier (`src/core` and `src/agents` unit tests, `ruff check`, `ruff format --check`, and `mypy`), explicitly excluding `tools/rpi-checks.py`.
* Commit all code changes and `.copilot-tracking/` artifacts locally with `Refs #104` and the Copilot co-author trailer, without pushing.

### What You May Not Know

* Registered-but-disabled capabilities (`aftercare-concern-pack` and `chat-case-conversation` outside the synthetic demo switch) currently satisfy `ai_registry.is_registered(task)` because `is_registered` checks metadata completeness rather than `enabled`; `Ai.run` and `Ai.look_at` need an explicit `is_dispatch_enabled` guard to fail closed when `self.gate` is absent (`C2`, `C5`, `C6`).
* Direct `ChatModel.__call__` invocations without an outer `ChatPanel` context currently leave `ai_consumption.CURRENT` unset, causing `Ai._request` to fall back to `capability="evidence"` rather than `"chat-case-conversation"` (`C5`, `C13`).
* `Consumption.authorize` before `Consumption.price(..., synthetic=False)` and non-human/placeholder owner strings (`"system"`, `"agent"`, `"copilot"`, `"unknown"`, `"unapproved"`) in `Consumption._require_bounds`, `chat_eval.call_authorization`, and `heldout_batch.authorization_problems` currently bypass `rai_release.named_human` (`C9`–`C12`).
* `src/core/pyproject.toml` excludes legacy migrated files (`ai.py`, `ai_registry.py`, `assistants.py`, `store.py`) from `ruff format` and `mypy` strict errors while enforcing `mypy --strict`, `ruff check`, and `ruff format --check` on all new `src/core` modules and tests (`C19`); typing untyped legacy module imports via explicit `Any` boundaries keeps `pyproject.toml` untouched.

### Unresolved Decisions or Blockers

* None. Open decision OD-51 (live Azure OpenAI pricing, spend caps, and named accountable individuals) remains intentionally unassigned owner policy, keeping every capability fail-closed beyond exercise mode by default.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop continuously in a single run (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) without stopping after any phase summary, writing dated artifacts under `.copilot-tracking/`.
* Work in `/home/azureuser/source/ama-demo-wt/feat-104-bounded-ai` on branch `feat/demo-104-bounded-ai` targeting `feat/demo-164-chat-grounding-provenance-0900` (PR #1641).
* Deliver an explicit cross-capability enforcement and acceptance verification suite for Issue #104's two engineering invariants:
  * `AI never approves, executes, ranks or mutates controlled records`
  * `No registered AI capability is enabled beyond the exercise without finite, owner-approved call, token and budget limits`
* Verify across `src/core` and `src/agents` that every registered AI capability is read-only/propose-only with respect to controlled records and cannot be enabled beyond exercise mode without finite, owner-approved call, token, and budget limits.
* Use the Focused validation tier (`src/core` and `src/agents` unit tests, `ruff check`, `ruff format --check`, `mypy`) and do NOT run `tools/rpi-checks.py`.
* Commit all changes and `.copilot-tracking/` artifacts locally using privacy-safe GitHub noreply email, `Refs #104` (not `Closes #104`, as Epic #104 has broader human/epic items), and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing.

## Goals

* Provide one canonical, strictly typed cross-capability enforcement and audit contract (`zava_forward.core.bounded_ai`) covering all 13 registered AI capabilities across `src/core` and `src/agents`.
* Close all discovered runtime bypasses in `src/core` (`ai_registry.py`, `ai.py`, `ai_consumption.py`) and `src/agents` (`chat.py`, `chat_eval.py`, `heldout_batch.py`) so disabled tasks cannot dispatch, chat calls always carry `chat-case-conversation` consumption context, out-of-order billable pricing cannot pair with unbounded authorities, and non-human or placeholder strings cannot approve non-exercise limits.
* Prove both Issue #104 invariants exhaustively across every registered capability via repeatable unit/acceptance suites in `src/core/tests/` and `src/agents/tests/`.

## Scope and Non-Goals

### In Scope

* New cross-capability enforcement and audit module `src/core/src/zava_forward/core/bounded_ai.py`.
* Surgical enforcement hardening in `src/core/src/zava_forward/core/ai_registry.py`, `src/core/src/zava_forward/core/ai.py`, `src/core/src/zava_forward/core/ai_consumption.py`, `src/agents/src/zava_forward/agents/chat.py`, `src/agents/src/zava_forward/agents/chat_eval.py`, and `src/agents/src/zava_forward/agents/heldout_batch.py`.
* New core acceptance suite `src/core/tests/test_epic104_bounded_ai_invariants.py` and expanded agents acceptance suite `src/agents/tests/test_epic104_bounded_ai_invariants.py`.
* Focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`) across `src/core` and `src/agents`, RPI review artifact, and local commit with `Refs #104`.

### Non-Goals

* Modifying `pyproject.toml`, `requirements*.txt`, `Dockerfile`s, workflows, `src/api`, `src/orchestrator`, or `src/importer`.
* Running `tools/rpi-checks.py` or browser harnesses.
* Inventing live Azure OpenAI pricing, operational budgets, or named human approvals for open decision OD-51.
* Pushing commits or opening/updating remote pull requests.

## Functional Requirements

* FR-1: Canonical capability dispatch, live-authority human check, and consumption identity (`ai_registry.py`, `ai.py`)
  * Observable acceptance criteria: `ai_registry.is_dispatch_enabled(task_id, env)` returns `False` for unregistered tasks and for `enabled=False` tasks (`aftercare-concern-pack`, and `chat-case-conversation` unless `demo_activation_honoured(task_id, env)` holds); `ai_registry.authorizes_live(task_id, env)` (outside the synthetic demo switch) requires `rai_release.named_human` on `accountable_individual` and every `authority` holder plus `rai_release.named` on `delegation`; `ai_registry.consumption_capability(task_id)` validates registration and maps task IDs to canonical kebab-case consumption capability names (`Ai.run` and `Ai.look_at` use it when constructing `CallContext`); `Ai.run` and `Ai.look_at` (immediately after scalar input bounds, before `ai_prompts.render` or `self.configured`) fail closed to `source="template", model=None, validated=True` with zero provider calls whenever a task is unregistered or not dispatch-enabled.
* FR-2: Non-exercise human-approved finite call, token, budget, and owned-alert enforcement (`ai_consumption.py`, `agents/chat_eval.py`, `agents/heldout_batch.py`, `agents/chat.py`)
  * Observable acceptance criteria: `Consumption.authorize` rejects blank `authority`, `owner`, or `evidence` unconditionally, validates `_require_bounds` with `rai_release.named_human(owner)`, `rai_release.named(alert)`, and `rai_release.named_human(alert_owner)` plus positive `calls`, `tokens`, and `amount` whenever the referenced price is non-synthetic or alert metadata is supplied, omits `"alert"` on synthetic exercise authorities when `alert=None`, `Consumption.price(..., synthetic=False)` raises `ValueError` at write time if any existing referencing authority lacks `alert`, `alert_owner`, or positive `calls`/`tokens`/`amount`, and `Consumption.non_exercise_status(...)` exposes read-only verification of unexpired authority, unexpired `synthetic is False` price (`retrieved <= now`, matching `model`), `alert`, `alert_owner`, `max_calls >= 1`, `max_depth >= 1`, positive budgets, and currency compatibility; `chat_eval.call_authorization` and `heldout_batch.authorization_problems` reject non-human or placeholder owners via `rai_release.named_human`; `ChatModel.__call__` binds a `CallContext` for `chat-case-conversation` when `ai_consumption.CURRENT.get()` is `None`.
* FR-3: Cross-capability invariant enforcement and audit API (`bounded_ai.py`)
  * Observable acceptance criteria: `zava_forward.core.bounded_ai` exposes `EXPECTED_CAPABILITIES` (all 13 registered capabilities), partitioned controlled-record snapshots (`snapshot_controlled_records` + `assert_controlled_records_unchanged`) separating strictly invariant case/ranking/aftercare fields from capability-scoped `funding_draft` and `read_document` workspace slots, `enforce_proposal_only(task_id, payload)` rejecting `approved=True`, forbidden approval/execution/override claims, or controlled-record mutation keys, `verify_non_exercise_enablement(task_id, ..., task_entry=None)` (supporting optional `task_entry` for controlled test harnesses while defaulting to `ai_registry.get(task_id)`) failing closed with explicit reasons unless named-human registry live authority (excluding demo-only activation), live `rai_release` contract/binding (`named_human` `accountable_owner` and approver), and `Consumption.non_exercise_status(...)` all pass, and `audit_registered_capabilities(env=None)` returning a deterministic cross-capability audit report.
* FR-4: Cross-capability acceptance verification suites (`src/core/tests/test_epic104_bounded_ai_invariants.py`, `src/agents/tests/test_epic104_bounded_ai_invariants.py`)
  * Observable acceptance criteria: Automated tests in both `src/core` and `src/agents` iterate over all 13 registered capabilities (`5` assistants, `6` retained tasks, `chat-case-conversation`, `aftercare-concern-pack`) and verify (a) read-only/propose-only non-mutation of controlled case records, stage/closure, resident consent/decisions, hazards, signoffs, grants, procurement, finance, quality, aftercare concerns/closures, and deterministic ranking even under adversarial model replies and post-review actions, and (b) fail-closed denial beyond exercise mode whenever finite call, token, or budget limits, billable pricing, owned alerts, or named human approvals are absent, zero, expired, exhausted, non-human, or registered out of order.

## Non-Functional Requirements

* NFR-1: ADR 0006 package dependency isolation
  * Objective threshold or evaluation condition: Zero forbidden cross-project imports (`core` imports stdlib/internal `core` only; `agents` imports `core` and never SQL/blob clients or `api`).
  * Operating condition or verification approach, if needed: Verified via `src/core/tests/test_dependency_rule.py` and `src/agents/tests/test_dependency_rule.py`.
  * Observable acceptance criteria: Dependency-rule tests pass in both `src/core` and `src/agents`.
* NFR-2: Static type safety and lint/format cleanliness
  * Objective threshold or evaluation condition: Zero `mypy`, `ruff check`, and `ruff format --check` errors in `src/core` and `src/agents` without modifying `pyproject.toml` exclusion lists.
  * Operating condition or verification approach, if needed: Run `ruff check .`, `ruff format --check .`, and `mypy` from `src/core` and `src/agents`.
  * Observable acceptance criteria: All static checks exit 0.
* NFR-3: Backward compatibility and bounded test budget
  * Objective threshold or evaluation condition: Exact test removals = `none`; maximum new test files = `1` (`src/core/tests/test_epic104_bounded_ai_invariants.py`, <= 20 focused test methods using `subTest` parameterization across the 13 capabilities); maximum added test methods in `src/agents/tests/test_epic104_bounded_ai_invariants.py` = `<= 12`; canonical targets only (`none` generated files).
  * Operating condition or verification approach, if needed: Full `python -m unittest discover -s tests` passes in both `src/core` and `src/agents`.
  * Observable acceptance criteria: All existing and new unit tests pass with zero removed tests.

## Acceptance Criteria

* AC-1: Every registered AI capability in `ai_registry.tasks()` (all 13 capabilities) is verified across `src/core` and `src/agents` to be read-only/propose-only with respect to controlled records—unable to approve, execute, rank, or mutate controlled records (`cases` stage/closed/resident/hazards/signoffs/grants/procurement/finance/quality, deterministic `_ranking()`, and aftercare `concerns`/`closures`).
* AC-2: Every registered AI capability in `ai_registry.tasks()` (all 13 capabilities) fails closed beyond exercise mode unless finite, named-human-approved call, token, and budget limits (plus an owned alert and valid live release/authority) are configured, and halts deterministically upon call, token, or money exhaustion.
* AC-3: `Ai.run` and `Ai.look_at` refuse provider dispatch for disabled or unregistered capabilities; direct `ChatModel` calls bind `chat-case-conversation` consumption context; `Consumption`, `chat_eval`, and `heldout_batch` reject non-human/placeholder owners and price-after-unbounded-authority bypasses.
* AC-4: Focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`) passes cleanly in both `src/core` and `src/agents` without running `tools/rpi-checks.py`.
* AC-5: All source, test, and `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `changes`, `reviews`, `rpi-sessions`) are committed locally on `feat/demo-104-bounded-ai` with `Refs #104` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and not pushed.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md                                                                          |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md                                                               |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-104-bounded-ai-plan-critique.md with Revise verdict resolved (`PC-001`–`PC-005` applied) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-104-bounded-ai-research.md                                                                   |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-104-bounded-ai-changes.md is created or continued by implementation as its evidence record    |
| Planning execution and readiness | Complete and Ready for implementation (`PC-001`–`PC-005` resolved directly by planner)                                                   |
| Continuation context             | Confirmed automatic RPI Agent parent continues automatically to `rpi-implement` once critique disposition is recorded                    |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-104-bounded-ai-research.md`: Cycle 1 evidence (`C1`–`C20`) mapping all 13 capabilities, controlled-record boundaries, non-exercise gates, and the 5 contrarian gaps.
* `src/README.md`: ADR 0006 package dependency rule, venv setup, and Focused validation commands for `src/core` and `src/agents`.
* `docs/case_study_48_original.md` and `docs/case_study_48_addendum.md`: Bounded agentic architecture, human approval gates, and resident consent constraints.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Bounded-AI Enforcement and Cross-Capability Contract

* Intent: Close `src/core` dispatch and non-exercise authorization gaps and deliver `zava_forward.core.bounded_ai` as the canonical cross-capability invariant enforcement and audit module.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Enforce capability dispatch-enabled state in `ai_registry` and `Ai`

* Requirement and evidence: FR-1, AC-3 (`C1`, `C2`, `C5`, `C6`)
* Expected result: `ai_registry.is_dispatch_enabled` and `ai_registry.consumption_capability` exist; `Ai.run` fails closed to `source="template"` when `not ai_registry.is_dispatch_enabled(task)`; `Ai.look_at` fails closed to `source="template"` when `"read_document"` is unregistered or not dispatch-enabled.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Harden `Consumption` non-exercise owner and price-ordering bounds

* Requirement and evidence: FR-2, AC-2, AC-3 (`C9`, `C10`)
* Expected result: `Consumption.authorize` rejects blank `authority`/`owner`/`evidence`, enforces `rai_release.named_human` on `owner` and `alert_owner` (and `rai_release.named` on `alert`) whenever price is non-synthetic or alert metadata is provided while omitting `"alert"` on synthetic authorities with `alert=None`, and `Consumption.price(..., synthetic=False)` raises `ValueError` if any pre-existing referencing authority lacks `alert`, `alert_owner`, or positive `calls`/`tokens`/`amount`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Create `zava_forward.core.bounded_ai` cross-capability enforcement and audit module

* Requirement and evidence: FR-3, NFR-1, NFR-2, AC-1, AC-2 (`C1`–`C10`, `C15`–`C19`)
* Expected result: `src/core/src/zava_forward/core/bounded_ai.py` implements strictly typed 13-capability inventory verification, controlled-record snapshot/immutability assertions (`Store` cases, deterministic `ranking`, aftercare `concerns`/`closures`), `enforce_proposal_only`, `verify_non_exercise_enablement`, and `audit_registered_capabilities`, passing `mypy --strict` and `ruff`.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Agents Capability Attribution and Named-Human Authorization Hardening

* Intent: Ensure `zava_forward.agents` preserves `chat-case-conversation` capability attribution on direct `ChatModel` calls and enforces named-human owner approval across actual-model evaluation gates.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Bind `CHAT_TASK` consumption context in `ChatModel.__call__`

* Requirement and evidence: FR-2, AC-3 (`C5`, `C13`)
* Expected result: When `ai_consumption.CURRENT.get()` is `None`, `ChatModel.__call__` wraps `self.worker.provider_call(...)` in `call_context(CallContext(..., CHAT_TASK, ...))`, preventing fallback to `"evidence"` while preserving outer `ChatPanel` context when present.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Enforce `rai_release.named_human` in `chat_eval` and `heldout_batch`

* Requirement and evidence: FR-2, AC-2, AC-3 (`C10`, `C11`, `C12`)
* Expected result: `chat_eval.call_authorization` rejects non-human or placeholder `authorised_by` values (`"no named owner authorisation"`), and `heldout_batch.authorization_problems` rejects non-human or placeholder `approved_by` values while retaining `"approved_by missing"` for blank/missing inputs.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Cross-Capability Acceptance Verification Suites and Focused Validation

* Intent: Prove Issue #104's two invariants across all 13 registered capabilities in both `src/core/tests` and `src/agents/tests`, pass focused `unittest` / `ruff` / `mypy` validation, and prepare clean review and local commit state.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add `src/core/tests/test_epic104_bounded_ai_invariants.py`

* Requirement and evidence: FR-4, NFR-2, NFR-3, AC-1, AC-2, AC-3 (`C1`–`C10`, `C15`–`C20`)
* Expected result: New strictly typed core test module exercises `bounded_ai` and all 13 registered capabilities across `Store`, SQLite `Assistants` (`invoke -> claim -> issue_permit -> complete -> review`), `ChatPanel`, `AftercareRegister`, `Ai.run`/`Ai.look_at`, `rai_release`, and `Consumption` (both invariants, hostile outputs, disabled-task refusal, price-ordering and non-human owner refusal, and exhaustion holds).
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Expand `src/agents/tests/test_epic104_bounded_ai_invariants.py` and run focused validation

* Requirement and evidence: FR-4, NFR-1, NFR-2, NFR-3, AC-1, AC-2, AC-3, AC-4 (`C11`–`C14`, `C18`–`C20`)
* Expected result: Expanded agents invariant suite verifies full 13-capability alignment with `bounded_ai.audit_registered_capabilities()`, direct `ChatModel` `CHAT_TASK` consumption metering and live-price denial, `AgentWorker` + `Store` cross-capability controlled-record immutability, and `named_human` enforcement across `Consumption`, `chat_eval`, and `heldout_batch`; `unittest`, `ruff check`, `ruff format --check`, and `mypy` exit 0 in both `src/core` and `src/agents`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md

## Dependencies

* `zava-forward-core` editable install before running `src/core` and `src/agents` checks: `src/agents` depends on `zava_forward.core` per ADR 0006.
* Existing formatting/typing boundaries in `src/core/pyproject.toml` and `src/agents/pyproject.toml`: keep legacy excluded core modules (`ai.py`, `ai_registry.py`) surgical and `ruff check`-clean, and keep `ai_consumption.py`, `bounded_ai.py`, `agents/*.py`, and test modules compliant with `ruff check`, `ruff format --check`, and `mypy --strict`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [High]    | resolved    | Added `rai_release.named_human` checks on registry/release owners, optional `task_entry` harness seam on `verify_non_exercise_enablement`, and public `Consumption.non_exercise_status(...)` helper (`FR-1`–`FR-3`, `P01-T01`–`P01-T03`). |
| Run 1 `PC-002` [High]    | resolved    | Removed `/tmp/zf-104-venv` instructions from `P03-T02`; validation uses workspace-local gitignored `.venv` verified with `git status --short`. |
| Run 1 `PC-003` [Medium]  | resolved    | Added explicit `: Any` boundary-alias requirement in `P03-T01` for untyped legacy `core` classes/modules under `mypy --strict` without touching `src/core/pyproject.toml`. |
| Run 1 `PC-004` [Medium]  | resolved    | Partitioned `snapshot_controlled_records` into strictly invariant controlled digests vs. `funding_draft` and `read_document` workspace-slot digests in `P01-T03`. |
| Run 1 `PC-005` [Low]     | resolved    | Placed `Ai.look_at` registration/enabled guard at function entry (after `export_fields.scalars`, before `ai_prompts.render` and `self.configured`) and wired `ai_registry.consumption_capability` in `Ai.run` and `Ai.look_at` (`P01-T01`). |
| Residual risk (`OD-51`)  | accepted with risk | Open decision OD-51 (live Azure OpenAI pricing, spend caps, and named accountable individuals) remains owner-owned policy outside software scope; all 13 capabilities default to `non_exercise_enabled == False`. |

## Follow-Up Items

* Optional future `src/api` startup diagnostic exposing `bounded_ai.audit_registered_capabilities()` on an operator health/readiness surface: outside immediate `src/core` + `src/agents` scope; tracked for a later #104 API slice.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-104-bounded-ai-changes.md
* Ready phase or task: All planned phases and tasks (`P01`, `P02`, `P03`) completed and reconciled for `rpi-review`
* Remaining provisional question or blocker: none

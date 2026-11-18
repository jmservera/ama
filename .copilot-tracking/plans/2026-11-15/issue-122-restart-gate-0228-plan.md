<!-- markdownlint-disable-file -->
# RPI Plan: Issue #122 Local RAI Incident, Restart Gate, Suspension Fallback, and SQL Old-Image Exclusion

## Task Metadata

* Task ID: issue-122-restart-gate-0228
* Task slug: issue-122-restart-gate-0228
* Planning status: Ready for implementation (single-pass critique PC-001..PC-007 applied)
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-plan-critique.md

## Executive Summary

This plan delivers the remaining local software-enforceable RAI Incident and Restart controls and verification suites for Issue #122 across `src/core` and `src/api` on branch `feat/platform-122-restart-gate-0228` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`). It hardens corrective-evidence and distinct-human-approval restart gating against placeholder claims, rejected/consumed test-claim replay, and view-only principals; verifies end-to-end availability of manual case progression, accessible digital/non-digital resident challenge, and independent statutory hazard response while AI is suspended; and adds database-enforced `continuity-gate-v1` SQL triggers plus independent SQL connection, concurrent barrier race, and multi-process worker restart tests covering `queued`, `leased`, and `ready` proposals as well as old-image restarts.

### User Decisions and Requirements Highlights

* Deliver all three local RAI Incident and Restart acceptance criteria in `src/core` and `src/api` without introducing a separate governance service or claiming live human authorization.
* Write dated RPI artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews`).
* Run focused unit tests in `src/core` and `src/api`, `ruff check`, `ruff format --check`, and `mypy`.
* Commit locally with `Refs #122` and the required Copilot co-author trailer without pushing, leaving `git status --short` empty.

### What You May Not Know

* **Database-level old-image exclusion without breaking existing corruption fixtures**: Existing tests (`src/api/tests/test_operator_suspension.py` and `src/core/tests/test_seed_merge.py`) intentionally write malformed JSON directly to `meta WHERE key='continuity'` and `assistant_tasks.body` to verify fail-closed reader handling. Enforcing `continuity-gate-v1` via normalized `continuity_gate_state` and `continuity_open_holds` tables plus SQLite/T-SQL triggers on `assistant_attempts` (`gate_version`, `send_gate_version`, `capability`) physically blocks pre-gate worker/server images from reserving or dispatching calls in SQL while preserving 100% compatibility with those corruption fixtures.
* **Non-code Issue #122 governance boundaries remain open and honest**: Constructed restart (`evidence_class="constructed-fixture"`) keeps `actual_hold=True` for live `Ai` because real OD-35 / OQ-017 restart authority appointment, witnessed live operational drills, immutable external Azure ledger-head storage, and accessibility sign-off remain owner activities outside code. That is why `Refs #122` (never a closing keyword) is mandatory.

### Unresolved Decisions or Blockers

* None within local `src/core` and `src/api` scope. External governance items on Issue #122 remain tracked as follow-ups outside this local slice.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop (`research`, `plan`, `critique`, `implement`, `review`) in `/home/azureuser/source/ama-demo-wt/feat-122-restart-gate` on branch `feat/platform-122-restart-gate-0228` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) for Issue #122 (`Service continuity, versioning, exportability and integration`).
* Deliver Criterion 1 in `src/core` and `src/api`: corrective evidence and distinct authorized human approval gate restart; replayed, stale, self-approved, or unauthorized restart fails.
* Deliver Criterion 2 in `src/core` and `src/api`: manual case work, accessible challenge, and independent hazard response remain available during suspension.
* Deliver Criterion 3 in `src/core` and `src/api`: independent SQL connection, concurrent suspend/review, race, and restart tests cover queued, leased, and ready proposals and old-image restart.
* Write dated RPI artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews`).
* Run focused unit tests in `src/core` and `src/api` (plus baseline guard tests if web/routes change), `ruff check`, `ruff format --check`, and `mypy`.
* Commit locally with `Refs #122` and trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, do not push, and leave a clean frozen worktree (`git status --short` empty).

## Goals

* Ensure AI restart after suspension requires substantive (non-placeholder, non-replayed) corrective test evidence and approval by a distinct OID-bound human manager holding trusted `ai_restart` capability, failing closed on every replayed, superseded, stale, self-approved, view-only, password-authenticated, or unauthorized attempt.
* Prove and preserve uninterrupted manual case progression, accessible digital and staffed non-digital resident challenge (including correction propagation without retaliation, inferred refusal, or hazard-clock interference), and statutory hazard response during task-scope suspension, release-wide (`all`) suspension, and continuity gate-version mismatch.
* Enforce fail-closed old-image restart exclusion at both the SQL engine boundary (SQLite and T-SQL triggers on `continuity_gate_state` and `assistant_attempts`) and the runtime protocol/release/epoch boundary, verified across independent SQL connections, concurrent suspend/review/dispatch barriers, and separate worker OS processes covering `queued`, `leased`, and `ready` proposals.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/restart_authority.py` and `src/core/src/zava_forward/core/continuity.py` corrective-evidence validation, corrective-claim anti-replay, `view_only` refusal, approver `actor` OID snapshot recording, and `GATE_VERSION` state helpers.
* `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, and `src/core/src/zava_forward/core/assistants.py` normalized `continuity_gate_state` and `continuity_open_holds` SQL tables, monotonic/gate-enforcement SQLite and T-SQL triggers on `continuity_gate_state` and `assistant_attempts`, and fail-closed gate-version mismatch checks.
* Strictly typed unit, HTTP (`TrustedProxyProvider` and `PasswordProvider`), suspension-availability, concurrent multi-connection race, and multi-process old-image restart tests in `src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py`.
* Directly related documentation updates in `src/core/README.md` and `src/api/README.md`.

### Non-Goals

* Adding a separate governance service, external deployment controller, or dependency-manifest package changes.
* Fabricating live OD-35 / OQ-017 human restart authority delegation, witnessed live operational drills, external immutable Azure head storage, live Azure SQL environment runs, or accessibility sign-off.
* Modifying web UI assets or HTTP route tables (existing `/api/continuity/*`, `/api/assistants/*`, and `/api/cases/*` routes remain stable).
* Pushing commits to any remote or closing Issue #122.

## Functional Requirements

* FR-1 (Substantive corrective evidence and anti-replay): `restart_propose` and `restart_decide` validate `corrective_evidence` and `test_id` using prose-safe placeholder/unavailability/chat-memory checks (rejecting empty/oversized inputs, exact placeholder tokens, leading `pending`/`tbd`/`todo`/`tbc`/`placeholder`/`unavailable` prefixes, chat-memory citations, and self/automatic-approval claims without false-positiving on domain prose or `test_id="constructed"`), and reject casefolded (`test_id.strip().casefold()`) reuse of any `test_id` previously rejected by `"Keep suspended"` on the suspension, attached to another open suspension's active `proposal`, or consumed by a committed `"Restart"` decision in the continuity register.
  * Observable acceptance criteria: Placeholder, `"Unavailable..."`, chat-memory, Keep-suspended-replayed, concurrently open, and previously Restart-consumed corrective claims fail closed with `ValueError` or `PermissionError` and append `ai_restart_propose_denied` / `ai_restart_decide_denied` audit records without mutating suspension status.
* FR-2 (Distinct authorized human approval and HTTP route enforcement): `suspend`, `restart_propose`, and `restart_decide` refuse `view_only` principals; `restart_decide` records the approver's `actor` snapshot (`email`, `name`, `code`, `oid`) and fails closed on password-route requests, missing `ZavaForward.AIRestart` (`ai_restart`), `ZavaForward.ApplicationAdmin` view-only principals, suspender/proposer/OID-alias self-approval, stale `epoch`, mismatched/superseded `proposal_digest`, candidate release/binding drift, mismatched `authority_ref`, automatic flags, and replayed decisions.
  * Observable acceptance criteria: Core and HTTP (`TrustedProxyProvider` / `PasswordProvider`) tests verify 200 on distinct OID-bound `ZavaForward.AIRestart` approval; store-dispatched negative cases return 400/403 with `ai_restart_propose_denied` / `ai_restart_decide_denied` audit rows, while outer HTTP RBAC `view_only` (`ApplicationAdmin`) rejection returns 403 before reaching the store (and writes `ai_restart_*_denied` when invoked directly on Core `Store`).
* FR-3 (Manual work, accessible challenge, and hazard independence during suspension): During active task-scope suspension, `all`-scope suspension, and SQL `gate_version` mismatch, staff can execute manual case updates/advances, open/update/escalate/resolve accessible resident challenges across `Digital`, `Phone`, `Letter`, and `In person` channels (plus `ChallengeRegister` `digital` and `staff_recorded` `phone`/`in_person`/`paper`/`assisted_visit` and immediate `hazard_concern` referral), reject suspended AI suggestions/proposals, and complete statutory hazard lifecycles (`raise_hazard` through `release_hazard`).
  * Observable acceptance criteria: Challenge `"Correction recorded"` marks dependent AI priority suggestions `stale=True` (`priority_correction=1`) during suspension while `assert_no_adverse_challenge_effects` preserves consent, case stage/priority, and statutory hazard clocks unchanged.
* FR-4 (SQL-enforced old-image exclusion and proposal-state race safety): `SqlStore`, `MssqlStore`, and `Assistants` maintain `continuity_gate_state` (`id=1, gate_version='continuity-gate-v1', epoch`) and `continuity_open_holds` (`scope, incident_id, epoch`) with SQLite and T-SQL triggers on `continuity_gate_state` and `assistant_attempts` (`capability`, `gate_version`, `send_gate_version`) so pre-gate images cannot reserve or send provider calls and cannot regress `epoch`, while `queued` (`pending`), `leased`, and `ready` proposals remain non-actionable or quarantined across concurrent suspend/review races and old-image worker restarts.
  * Observable acceptance criteria: Pre-gate SQL `INSERT`/`UPDATE` on `assistant_attempts`, open-hold reservation/send writes, and `epoch` regression fail at the SQL trigger layer; independent SQL connection, threaded barrier, and `subprocess` worker tests verify zero unauthorized provider calls and non-actionable/quarantined handling across `queued`, `leased`, and `ready` proposals.

## Non-Functional Requirements

* NFR-1 (Transactional atomicity and dialect parity): Continuity gate state and open holds commit in the exact same SQL transaction as `meta ('continuity')`, using dialect-portable DDL/triggers across SQLite (`sqlstore.py`, `assistants.py`) and T-SQL (`mssqlstore.py`, `assistants.py`).
  * Objective threshold or evaluation condition: Zero uncommitted partial state on simulated writer faults or `ConflictError`; both SQLite live execution and T-SQL generated DDL/trigger assertions pass.
  * Operating condition or verification approach, if needed: Verified via multi-connection SQLite transactions, `subprocess` workers, and `MssqlStore` / `Assistants(mssql=True)` SQL inspection tests.
  * Observable acceptance criteria: All existing corruption/rollback tests (`test_operator_suspension.py`, `test_seed_merge.py`, `test_continuity_epoch_export.py`, `test_assistant_restart_non_replenishment.py`) and new SQL trigger/race tests pass.
* NFR-2 (Type, lint, format, and test-budget discipline): All new and modified code conforms to repository `ruff`, SQL portability (`SharedSqlIsPortableTests`), and strict `mypy` gates without modifying dependency manifests or removing existing regression tests.
  * Objective threshold or evaluation condition: Exact test removals = `none`; maximum new test files = `2` (`src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py`, <= 25 focused test methods total, plus MSSQL teardown table registration in `src/api/tests/test_mssqlstore.py` and `src/api/tests/test_assistants.py`); `ruff check`, `ruff format --check`, and `mypy` exit 0 in `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Run in workspace-local editable venv `.venv-122-local` (never `/tmp`) and remove `.venv-122-local` before final git status check.
  * Observable acceptance criteria: Zero lint, format, mypy, SQL portability, or unit-test failures across `src/core` and `src/api`, and `git status --short` is empty after local commit.

## Acceptance Criteria

* AC-1: Corrective evidence and distinct authorized human approval gate restart; replayed (post-Restart, post-Keep-suspended, or consumed `test_id`), stale (`epoch`, superseded `proposal_digest`, or drifted serving candidate), placeholder/unavailable, self-approved (suspender, proposer, or same-OID roster alias), view-only (`ApplicationAdmin`), password-route, or unauthorized restart fails closed across core and HTTP endpoints.
* AC-2: Manual case work (`log_call`, `set_decision`, `advance`), accessible resident challenge (`Digital`, `Phone`, `Letter`, `In person` + `staff_recorded` `phone`/`in_person`/`paper`/`assisted_visit`, update, escalation to distinct owner, resolution with correction propagation and `hazard_concern` referral, zero retaliation/refusal/hazard delay), AI proposal rejection, and statutory hazard response (`raise_hazard` through `release_hazard`) succeed and persist across independent SQL connections while AI is suspended.
* AC-3: SQLite and T-SQL `continuity-gate-v1` schema/triggers and independent SQL connection, concurrent barrier suspend/review/dispatch race, and `subprocess` worker restart tests cover `queued`, `leased` (live completion quarantine, permit denial, expired-lease reclaim, and `permitted`-marker `blocked-reclaim`), and `ready` proposals plus old-image restart (both pre-gate SQL write exclusion and older model/prompt/release worker restart).
* AC-4: `src/core/README.md` and `src/api/README.md` accurately document the SQL old-image gate and remaining non-code Issue #122 boundaries; dated RPI tracking artifacts are complete and reconciled; unit tests, `ruff check`, `ruff format --check`, and `mypy` pass; and the branch is committed locally with `Refs #122` and clean `git status --short`.

## Test Ownership, Canonical Targets, and Budget Lock

* Canonical production targets (hand-authored, zero generated code):
  * `src/core/src/zava_forward/core/restart_authority.py`
  * `src/core/src/zava_forward/core/continuity.py`
  * `src/core/src/zava_forward/core/sqlstore.py`
  * `src/core/src/zava_forward/core/mssqlstore.py`
  * `src/core/src/zava_forward/core/assistants.py`
  * `src/core/README.md`
  * `src/api/README.md`
* Generated targets: `none`.
* Test ownership and budget:
  * Exact test removals: `none` (existing suites in `src/core/tests/` and `src/api/tests/` remain intact as regression guards).
  * Existing MSSQL test harness teardown updates (zero new test methods): `src/api/tests/test_mssqlstore.py` and `src/api/tests/test_assistants.py` drop `continuity_open_holds`, `continuity_gate_state`, and new gate triggers during disposable SQL Server teardown.
  * Maximum test additions: `2` new strictly typed test modules (`src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py`, capped at <= 25 focused semantic test methods combined, using `: Any` boundary aliases for untyped Core/fixture symbols).
  * Semantic vs regression split: Existing `test_continuity.py`, `test_continuity_epoch_export.py`, `test_operator_suspension.py`, `test_operator_suspension_drill.py`, `test_assistant_restart_non_replenishment.py`, `test_seed_merge.py`, `test_mssqlstore.py`, and `test_resident_decisions.py` cover baseline regression; the two new modules test newly introduced behavioral invariants (placeholder/replay corrective-claim rejection, HTTP `TrustedProxyProvider` restart matrix, suspension-time accessible challenge + correction + statutory hazard independence, NULL-safe SQL trigger pre-gate/epoch-rollback/open-hold enforcement, and concurrent/subprocess `queued`/`leased`/`ready` + old-image restart races).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md                                                                   |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md                                                        |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-plan-critique.md (`Revise` -> all `PC-001`..`PC-007` applied)     |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md                                                            |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete; implementation-ready                                                                                                           |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to `rpi-implement`                                                               |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md`: Cycle 1 Wider, Deeper, and Contrarian findings (`C1`-`C18`) establishing exact code anchors and contrarian fixture constraints.
* `src/core/src/zava_forward/core/continuity.py` and `src/core/src/zava_forward/core/restart_authority.py`: Existing suspension, snapshot, corrective proposal, RULE-024 human restart authority, and export contracts.
* `src/core/src/zava_forward/core/assistants.py`, `src/core/src/zava_forward/core/sqlstore.py`, and `src/core/src/zava_forward/core/mssqlstore.py`: Durable SQL assistant lifecycle, `assistant_attempts` reservation/send fencing, SQLite WAL transactions, and T-SQL schema/trigger patterns.
* `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/challenges.py`, and `src/api/src/zava_forward/api/server.py`: Accessible challenge workflow, safeguard checks, statutory hazard routes, and `/api/continuity/*` HTTP handlers.
* `src/core/README.md` and `src/api/README.md`: Canonical component documentation and Issue #122 non-operative custody/authority disclosures.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden Restart Gate Corrective Evidence, Anti-Replay, and Identity Controls

* Intent: Close placeholder corrective-evidence, rejected/consumed claim replay, view-only principal, and approver OID snapshot gaps in `restart_authority.py` and `continuity.py`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add substantive corrective-evidence validator in `restart_authority.py`

* Requirement and evidence: FR-1, AC-1; research `C2`, `C4`.
* Expected result: `validate_corrective_evidence` rejects empty/oversized text, chat-memory references, `"Unavailable..."` prefixes, and placeholder strings without echoing raw input, while accepting valid concise test claims and identifiers.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce corrective-claim anti-replay, `view_only` refusal, and approver `actor` snapshot in `continuity.py`

* Requirement and evidence: FR-1, FR-2, AC-1; research `C2`, `C3`, `C15`.
* Expected result: `suspend`, `restart_propose`, and `restart_decide` reject `view_only` principals; `restart_propose` and `restart_decide` enforce `validate_corrective_evidence`, reject Keep-suspended-replayed `(test_id, corrective_evidence)` pairs and previously Restart-consumed `test_id` values, and record `actor` (`email`, `name`, `code`, `oid`) on decision records.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Enforce SQL Continuity Gate Protocol and Old-Image Exclusion Triggers

* Intent: Add normalized `continuity_gate_state` and `continuity_open_holds` SQL tables and database triggers across SQLite and T-SQL so pre-gate or gate-mismatched images cannot reserve/send assistant calls or regress continuity epochs.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Persist `continuity_gate_state` and `continuity_open_holds` with monotonic SQLite/T-SQL triggers in `continuity.py`, `sqlstore.py`, and `mssqlstore.py`

* Requirement and evidence: FR-4, NFR-1, AC-3; research `C1`, `C8`, `C9`, `C10`, `C16`, `C17`, `C18`.
* Expected result: `continuity.GATE_VERSION = "continuity-gate-v1"` and normalized SQL state/open-hold rows are created and synchronized atomically with `continuity` writes in `SqlStore` and `MssqlStore`, protected against delete/epoch regression by SQL triggers, and checked fail-closed by `SqlStore.continuity_suspension` without breaking raw `meta ('continuity')` corruption fixtures.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Enforce `continuity-gate-v1` and open-hold SQL triggers on `assistant_attempts` in `assistants.py`

* Requirement and evidence: FR-4, NFR-1, AC-3; research `C5`, `C6`, `C7`, `C10`, `C16`.
* Expected result: `Assistants.migrate()` adds `capability`, `gate_version`, and `send_gate_version` columns plus SQLite and T-SQL triggers on `assistant_attempts` that abort pre-gate `'reserved'` / `'sending'` writes and open-hold dispatches; `_reserve`, `_fence_in`, and `disabled` stamp and check `continuity.GATE_VERSION`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Author Core, HTTP, Suspension-Fallback, Concurrency, and Old-Image Restart Tests

* Intent: Verify Criteria 1, 2, and 3 across `src/core` and `src/api` with deterministic unit, HTTP, multi-connection barrier, and `subprocess` old-image restart tests.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add `src/core/tests/test_restart_gate_sql_fences.py` for core restart, suspension availability, and SQL trigger/T-SQL invariants

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2, AC-1, AC-2, AC-3; research `C2`-`C13`, `C16`.
* Expected result: Strictly typed `src/core` test module verifies placeholder/replay corrective-claim rejection, suspension-time manual/accessible-challenge/hazard availability (including gate-version mismatch), SQLite trigger rejection of pre-gate `assistant_attempts` writes and epoch rollback, and T-SQL DDL/trigger parity.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Add `src/api/tests/test_continuity_restart_gate.py` for HTTP `TrustedProxyProvider`, suspension fallback, concurrent races, and subprocess old-image restart

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2, AC-1, AC-2, AC-3; research `C3`, `C5`-`C9`, `C11`-`C15`.
* Expected result: Strictly typed `src/api` test module verifies the HTTP `TrustedProxyProvider` / `PasswordProvider` restart gate matrix, HTTP manual/accessible-challenge/hazard availability while `all` AI work is suspended, concurrent barrier `suspend` vs `review`/`claim`/`fence_send`/`complete_result` across independent SQL connections, and `subprocess` old-image restart across `queued`, `leased` (including `permitted`-marker `blocked-reclaim`), and `ready` proposals.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Update Component Documentation and Execute Validation Gate

* Intent: Align `src/core/README.md` and `src/api/README.md` with the implemented SQL continuity gate and run full project unit, lint, format, and type-check suites.
* Dependencies: P01, P02, P03.

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Document SQL `continuity-gate-v1` old-image exclusion and corrective-claim anti-replay in `src/core/README.md` and `src/api/README.md`

* Requirement and evidence: AC-4; research `C16`.
* Expected result: `src/core/README.md` and `src/api/README.md` accurately describe SQL `continuity-gate-v1` enforcement and anti-replay rules while keeping OD-35/OQ-017, witnessed drill, immutable external head custody, and accessibility acceptance explicitly marked unestablished.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md

<!-- rpi:task id=P04-T02 -->
#### [x] P04-T02: Run `src/core` and `src/api` test suites, `ruff check`, `ruff format --check`, and `mypy`, and reconcile RPI artifacts

* Requirement and evidence: NFR-2, AC-4.
* Expected result: Focused and full unit suites in `src/core` and `src/api` (plus regression guard `tools/rename-zava-tests.py` if applicable), `ruff check`, `ruff format --check`, and `mypy` pass with zero errors; temporary venv is cleaned up before final Review/commit.
* Detail section: P04-T02 in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md

## Dependencies

* `zava_forward.core` editable package -> `zava_forward.api`: `src/api` imports `continuity`, `restart_authority`, `sqlstore`, `mssqlstore`, and `assistants` directly from `src/core`, so P01 and P02 precede P03-T02.
* Existing legacy module lint/format exclusions in `src/core/pyproject.toml`: `continuity.py`, `assistants.py`, `sqlstore.py`, and `mssqlstore.py` are in ADR 0006 format-exclude lists, whereas `restart_authority.py` and both new test modules are subject to full strict `ruff check`, `ruff format --check`, and `mypy --strict`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique `PC-001` (Critical) | Applied (`planner-direct`) | Replaced scalar `!=` trigger subqueries with NULL-safe fail-closed `NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = ...)`, specified separate SQLite (`BEFORE ... RAISE(ABORT, ...)`) and set-based T-SQL (`INSTEAD OF DELETE` + `AFTER INSERT, UPDATE` over `inserted`/`deleted` with `THROW`) triggers, and matched `NVARCHAR(...) COLLATE Latin1_General_100_BIN2` collations across `mssqlstore.py` and `assistants.py`. |
| Single-pass critique `PC-002` (High) | Applied (`planner-direct`) | Replaced raw `INSERT OR IGNORE` seeding with portable `INSERT INTO continuity_gate_state ... SELECT ... WHERE NOT EXISTS (...)` so `SharedSqlIsPortableTests` passes, and added `continuity_open_holds`, `continuity_gate_state`, and gate triggers to `src/api/tests/test_mssqlstore.py` and `src/api/tests/test_assistants.py` MSSQL teardown lists. |
| Single-pass critique `PC-003` (High) | Applied (`planner-direct`) | Removed `/tmp` paths in favor of workspace-local `.venv-122-local` (deleted before final `git status --short` check), and added explicit worktree `PYTHONPATH` propagation + `timeout=15` to `subprocess.run` old-image worker tests in `P03-T02`. |
| Single-pass critique `PC-004` (High) | Applied (`planner-direct`) | Moved `continuity_gate_state.gate_version` check directly into `Assistants.suspended(db, capability)` and `SqlStore.continuity_suspension` (returning a complete synthetic hold dict handled by `continuity.reason_text`), added JSON-safe monotonic `safe_epoch = max(current_sql_epoch, parsed_epoch)` clamping in `continuity.gate_sync_rows`, and wired sync into `SqlStore._migrate`, `_seed`, `merge_seed(apply=True)`, `_proc_write`, and `Assistants.migrate()`. |
| Single-pass critique `PC-005` (Medium) | Applied (`planner-direct`) | Specified prose-safe placeholder patterns in `validate_corrective_evidence` (preserving valid prose and `test_id="constructed"`), enforced re-validation in `restart_decide("Restart")`, normalized `.strip().casefold()` anti-replay across Keep-suspended, concurrently open, and Restarted suspensions, and guarded `(self.local if hasattr(self, "db") else self).incident_validation`. |
| Single-pass critique `PC-006` (Medium) | Applied (`planner-direct`) | Distinguished outer HTTP `do_POST` `view_only` `403` (`ApplicationAdmin`) from store-level `ai_restart_*_denied` audits and mapped each negative subtest to its exact HTTP route (`/api/continuity/restart-propose` vs `/api/continuity/restart-decide`). |
| Single-pass critique `PC-007` (Medium) | Applied (`planner-direct`) | Specified `: Any` boundary aliases for untyped Core/fixture symbols and complete strict annotations in `test_restart_gate_sql_fences.py` and `test_continuity_restart_gate.py` so `mypy` passes with zero `pyproject.toml` edits. |
| Residual risk (non-local SQL Server & human drills) | Accepted | Local SQLite trigger execution and offline T-SQL DDL/portability assertions run locally; live `ZF_TEST_MSSQL=1` execution and human-witnessed Azure deployment drills (`OD-35` / `RULE-020`) remain external (`Refs #122`). |

## Follow-Up Items

* Execute an owner-witnessed continuity/restart drill and record appointed human restart authority (`OQ-017` / `OD-35` / `RULE-020`) once Zava North Homes governance sign-off exists; outside immediate scope because human delegation and witness participation cannot be fabricated in code (Owner: Programme Sponsor / Building Safety).
* Configure immutable external Azure ledger-head storage and execute an owned Azure SQL continuity/restart drill; outside immediate scope because live Azure resource provisioning and custody approvals remain open on Issue #122 (Owner: Platform / Data Governance).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None

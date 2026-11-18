---
title: "RPI Plan: PR #1797 c2 Cross-PR Continuity SQL Gate Fix (Refs #81)"
description: "Implementation plan for PR #1797 c2 Assistants.challenge() continuity SQL gate remediation across src/core and src/api"
ms.date: 2026-11-15
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: safety-81-exercise-gates-c2
* Task slug: safety-81-exercise-gates
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/safety-81-exercise-gates-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/safety-81-exercise-gates-plan-critique.md

## Executive Summary

This `c2` child plan resolves the sole cross-PR CI failure on `PR #1797` (`feat/safety-81-exercise-gates` at `1be969f61`, targeting `feat/demo-164-chat-grounding-provenance-0900` / `PR #1641`) for `#81`. Commit `1be969f61` passed `8/10` CI jobs and all `#81` safety/consent exercise tests, failing 1 test in `src-core` (`test_challenge_no_retaliation_220`) and 1 test in `src-api` (`test_challenge_no_retaliation_api_220`) with `sqlite3.IntegrityError: continuity SQL gate mismatch` at `src/core/src/zava_forward/core/assistants.py:4064`. That interaction arose on the parent branch between PR `#1796` (`#220`) and PR `#1787` (`#122`): `Assistants.challenge()` increments `revision=revision+1` on a `'ready'` row without stamping `review_gate_version` and `reviewed_revision=revision+1` required by `#122`'s `assistant_tasks_gate_update` trigger. Updating `Assistants.challenge()` to match `Assistants.review()` (`assistants.py:3638-3641`) resolves both failures without weakening `#122` old-image SQL write fences or affecting `#81` or `#220` governance semantics, verified under the Focused tier and committed locally on `feat/safety-81-exercise-gates` without pushing.

### User Decisions and Requirements Highlights

* Continue the RPI loop on `feat/safety-81-exercise-gates` (`PR #1797`) for the `c2` cross-PR (`#122` / `#220`) fix in `Assistants.challenge()` (`src/core/src/zava_forward/core/assistants.py` around line `4064`).
* Stamp `review_gate_version=?, reviewed_revision=revision+1, revision=revision+1` using `continuity.GATE_VERSION` in `Assistants.challenge()`.
* Run Focused validation across `src/core` (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`), `src/api` (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`), and `python3 tools/rename-zava-tests.py`.
* Record `c2` rework in `.copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/safety-81-exercise-gates-review.md`, and commit cleanly on `feat/safety-81-exercise-gates` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.

### What You May Not Know

* `reviewed_revision` and `review_gate_version` are write-only SQL trigger fence columns (`assistant_tasks_gate_insert` and `assistant_tasks_gate_update`); `Assistants._row()` never selects them, so updating `reviewed_revision=revision+1` in `Assistants.challenge()` never marks an unreviewed proposal as verified or accepted in Python or API responses (`C4`).
* In the workspace, the `#81` core test module is named `src/core/tests/test_safety_consent_exercise_scenarios_81.py` (rather than `test_safety_consent_exercise_gates_81.py`), and `#81` has no `src/api/tests/test_safety_consent_exercise_gates_81_api.py` file (`C8`). Focused validation therefore executes `tests/test_challenge_no_retaliation_220.py`, `tests/test_restart_gate_sql_fences.py`, and `tests/test_safety_consent_exercise_scenarios_81.py` in `src/core`, and `tests/test_challenge_no_retaliation_api_220.py`, `tests/test_continuity_restart_gate.py`, and `tests/test_content_standard.py` in `src/api`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Continue the RPI loop in `/home/azureuser/source/ama-demo-wt/feat-81-safety-consent-gates` on branch `feat/safety-81-exercise-gates` (`PR #1797` targeting `feat/demo-164-chat-grounding-provenance-0900`) (user prompt).
* Update `Assistants.challenge()` in `src/core/src/zava_forward/core/assistants.py` to execute `UPDATE assistant_tasks SET body=?,state=?,review_gate_version=?,reviewed_revision=revision+1,revision=revision+1 WHERE id=? AND revision=?` with `(canonical(stored), state, continuity.GATE_VERSION, tid, revision)` (user prompt; research `C2`, `C3`, `C5`).
* Run Focused validation (`unittest`, `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/api`, plus `python3 tools/rename-zava-tests.py`) (user prompt; research `C8`).
* Record `c2` rework in `.copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/safety-81-exercise-gates-review.md`, and commit cleanly on `feat/safety-81-exercise-gates` with privacy-safe noreply email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (user prompt; `.github/copilot-instructions.md`).

## Goals

* Eliminate the `sqlite3.IntegrityError: continuity SQL gate mismatch` failure in `Assistants.challenge()` across both `src-core` (`#220` unit/integration suite) and `src-api` (`#220` HTTP endpoint suite).
* Preserve `#122` SQLite and MSSQL `assistant_tasks_gate_update` and `assistant_tasks_hold_update` old-image and suspension write fences intact.
* Preserve `#81` exercise-scenario safety and resident consent gate invariants and full `ruff` / `mypy` / `rename-zava-tests` conformance across `src/core` and `src/api`.
* Deliver a complete dated `safety-81-exercise-gates` RPI evidence set and a clean unpushed local commit on `feat/safety-81-exercise-gates`.

## Scope and Non-Goals

### In Scope

* Canonical Python target: `src/core/src/zava_forward/core/assistants.py` (`Assistants.challenge()` `UPDATE assistant_tasks` statement); generated targets: `none`.
* Test ownership lock: existing suites `src/core/tests/test_challenge_no_retaliation_220.py`, `src/core/tests/test_restart_gate_sql_fences.py`, `src/core/tests/test_safety_consent_exercise_scenarios_81.py`, `src/api/tests/test_challenge_no_retaliation_api_220.py`, `src/api/tests/test_continuity_restart_gate.py`, and `src/api/tests/test_content_standard.py`; exact test removals: `none`; maximum test additions: `0` (existing `#220` core and HTTP tests already reproduce the exact failure pre-fix and assert the complete `open` -> `update` -> `escalate` -> `resolve` -> `reopen` lifecycle post-fix).
* Focused validation: `unittest`, `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` and `src/api`, plus `python3 tools/rename-zava-tests.py`.
* Dated `2026-11-15` `safety-81-exercise-gates` RPI tracking artifacts under `.copilot-tracking/` and a single clean local commit atop `1be969f61` on `feat/safety-81-exercise-gates`.

### Non-Goals

* Modifying SQL DDL, `SQLITE_ATTEMPT_TRIGGERS`, or `MSSQL_ATTEMPT_TRIGGERS` in `assistants.py`.
* Modifying `safety_consent_exercise_gate.py`, `gates.py`, `resident_decisions.py`, `src/api/checks/`, or `src/api/src/zava_forward/api/web/`.
* Rebasing, amending `1be969f61`, or pushing to `origin`.

## Functional Requirements

* FR-1: Continuity SQL gate version and revision stamping in `Assistants.challenge()`.
  * Observable acceptance criteria: `Assistants.challenge()` updates `assistant_tasks` with `SET body=?,state=?,review_gate_version=?,reviewed_revision=revision+1,revision=revision+1 WHERE id=? AND revision=?` passing `continuity.GATE_VERSION`, and `AssistantsProposalChallengeNoRetaliationTests` (`src/core`) and `ChallengeNoRetaliationApi220Tests` (`src/api`) both pass `100%`.
* FR-2: Complete `c2` RPI evidence record and clean unpushed local commit.
  * Observable acceptance criteria: `.copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/safety-81-exercise-gates-review.md`, and companion `safety-81-exercise-gates` RPI artifacts are reconciled and committed with `src/core/src/zava_forward/core/assistants.py` on `feat/safety-81-exercise-gates` (`Refs #81`, `Refs #122`, `Refs #220`, `Co-authored-by` trailer), with `git status --short` empty and zero remote pushes.

## Non-Functional Requirements

* NFR-1: Continuity SQL trigger fence preservation (semantic coverage).
  * Objective threshold or evaluation condition: Un-gated `UPDATE assistant_tasks` statements without `review_gate_version` and `reviewed_revision=revision+1` continue to fail closed with `continuity SQL gate mismatch`, and suspended capabilities continue to fail closed with `continuity scope is suspended`.
  * Operating condition or verification approach, if needed: Verified via `src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py`.
  * Observable acceptance criteria: All `#122` SQL fence and HTTP restart gate tests pass with zero regressions.
* NFR-2: Focused lint, formatting, static-type, and `#81` regression parity (regression coverage).
  * Objective threshold or evaluation condition: `ruff check .`, `ruff format --check .`, and `mypy` report `0` issues across `src/core` (`363` source files) and `src/api` (`300` source files); `test_safety_consent_exercise_scenarios_81.py` (`8` tests), `test_content_standard.py` (`29` tests), and `tools/rename-zava-tests.py` (`25` tests) pass with `0` failures.
  * Operating condition or verification approach, if needed: Run inside `src/core`, `src/api`, and repository root matching `.github/workflows/src-ci.yml`.
  * Observable acceptance criteria: Every check exits `0`.

## Acceptance Criteria

* `Assistants.challenge()` in `src/core/src/zava_forward/core/assistants.py` updates `review_gate_version=?` (`continuity.GATE_VERSION`) and `reviewed_revision=revision+1` alongside `revision=revision+1`.
* `tests/test_challenge_no_retaliation_220.py`, `tests/test_restart_gate_sql_fences.py`, and `tests/test_safety_consent_exercise_scenarios_81.py` pass in `src/core`.
* `tests/test_challenge_no_retaliation_api_220.py`, `tests/test_continuity_restart_gate.py`, and `tests/test_content_standard.py` pass in `src/api`.
* `python3 -m ruff check . && python3 -m ruff format --check .` and `mypy` exit `0` in both `src/core` and `src/api`, and `python3 tools/rename-zava-tests.py` exits `0`.
* `.copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/safety-81-exercise-gates-review.md` (plus state, research, plan, details, critique) are reconciled and committed locally on `feat/safety-81-exercise-gates` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and `git status --short` empty, without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                    |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/safety-81-exercise-gates-plan.md                                                           |
| Phase details                    | .copilot-tracking/details/2026-11-15/safety-81-exercise-gates-phase-details.md                                                |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/safety-81-exercise-gates-plan-critique.md (`Pass`, `PC-001` applied)               |
| Relevant research                | .copilot-tracking/research/2026-11-15/safety-81-exercise-gates-research.md                                                    |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md is created by implementation as its evidence record  |
| Planning execution and readiness | Complete; Ready for implementation                                                                                            |
| Continuation context             | Active confirmed automatic RPI Agent parent continues to `Implement` after critique gate passes                               |

## Sources

* `.copilot-tracking/research/2026-11-15/safety-81-exercise-gates-research.md`: Cycle 1 evidence (`C1`-`C8`) reproducing `assistants.py:4064` failure, auditing `reviewed_revision` and all `UPDATE assistant_tasks` sites, and verifying test module paths.
* `src/core/src/zava_forward/core/assistants.py`: `SQLITE_ATTEMPT_TRIGGERS` (`1054-1065`), `MSSQL_ATTEMPT_TRIGGERS` (`1096-1108`), `Assistants.review()` (`3638-3641`), and `Assistants.challenge()` (`4064-4067`).
* `src/core/tests/test_challenge_no_retaliation_220.py` and `src/api/tests/test_challenge_no_retaliation_api_220.py`: `#220` unit and loopback HTTP tests reproducing the failure.
* `src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py`: `#122` SQL trigger fence and restart authority tests.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Continuity SQL Gate Stamp in `Assistants.challenge()`

* Intent: Align `Assistants.challenge()` `UPDATE assistant_tasks` statement in `src/core/src/zava_forward/core/assistants.py` with `#122`'s `assistant_tasks_gate_update` contract (`continuity.GATE_VERSION` and `reviewed_revision=revision+1`).
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update `Assistants.challenge()` `UPDATE assistant_tasks` in `src/core/src/zava_forward/core/assistants.py`

* Requirement and evidence: FR-1, NFR-1 (`C2`, `C3`, `C4`, `C5`, `C6`, `C7`)
* Expected result: `Assistants.challenge()` executes `UPDATE assistant_tasks SET body=?,state=?,review_gate_version=?,reviewed_revision=revision+1,revision=revision+1 WHERE id=? AND revision=?` with `(canonical(stored), state, continuity.GATE_VERSION, tid, revision)`, formatted cleanly to `src/core` `line-length = 100`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/safety-81-exercise-gates-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Cross-Package Validation and Local Git Identity Check

* Intent: Verify `#220`, `#122`, and `#81` unit/HTTP suites, package-local `ruff check .`, `ruff format --check .`, `mypy`, and `tools/rename-zava-tests.py`, and confirm local noreply git identity ahead of post-Review commit closeout.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run Focused `src/core`, `src/api`, and migration validation suites and verify local git identity

* Requirement and evidence: FR-2, NFR-1, NFR-2 (`C7`, `C8`; `.github/copilot-instructions.md`)
* Expected result: `test_challenge_no_retaliation_220.py`, `test_restart_gate_sql_fences.py`, and `test_safety_consent_exercise_scenarios_81.py` pass in `src/core`; `test_challenge_no_retaliation_api_220.py`, `test_continuity_restart_gate.py`, and `test_content_standard.py` pass in `src/api`; `ruff check .`, `ruff format --check .`, and `mypy` exit `0` in both `src/core` and `src/api`; `python3 tools/rename-zava-tests.py` exits `0`; local `user.email` is confirmed as `8036360+jmservera@users.noreply.github.com`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/safety-81-exercise-gates-phase-details.md

## Dependencies

* `src/core` (`pyproject.toml` `line-length = 100`) and `src/api` (`pyproject.toml` `line-length = 100`, `[tool.ruff.format] exclude`).
* `gh api user` / repository-local `git config --local user.email` (`8036360+jmservera@users.noreply.github.com`).

## Critique Disposition

Single-pass `rpi-plan-critique` completed with verdict `Pass` (`0` Critical, `0` High, `0` Medium, `1` Low).

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `2026-11-15` `PC-001` (Low: `src/core/pyproject.toml` excludes `assistants.py` from `ruff format`, so do not pass `assistants.py` directly to `ruff format`; edit surgically and run directory-scoped `ruff check . && ruff format --check .`) | Applied | Updated `P01-T01` in `safety-81-exercise-gates-phase-details.md` to forbid running `ruff format` directly on `assistants.py` and keep the surgical edit cleanly wrapped under `<= 100` columns. |
| Residual risk: remote PR `#1797` stays at `1be969f61` until coordinator push | Accepted | Explicit caller `exclude` control forbids pushing from this worktree; frozen local HEAD commit leaves exact `10/10`-ready code and `c2` tracking trail for coordinator push. |

## Follow-Up Items

* None inside `c2` scope; pushing frozen local HEAD on `feat/safety-81-exercise-gates` to `origin` (`PR #1797`) and parent epic `#81` non-exercise criteria remain post-Review follow-ups.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md
* Ready phase or task: `P01` and `P02` (`Planning status: Ready`)
* Remaining provisional question or blocker: None

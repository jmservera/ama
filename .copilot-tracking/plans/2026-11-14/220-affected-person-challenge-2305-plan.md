---
title: RPI Plan - 220-affected-person-challenge-2305
description: Implementation plan for Issue 220 affected-person challenge non-retaliation, non-refusal, and non-delayed hazard response controls and tests in src/core
ms.date: 2026-11-14
---

<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: issue-220-criterion-5-affected-person-challenge-2305
* Task slug: 220-affected-person-challenge-2305
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md
* Plan critique: .copilot-tracking/critiques/2026-11-14/220-affected-person-challenge-2305-critique.md

## Executive Summary

This plan delivers the locally verifiable `src/core` controls and deterministic unit tests for Issue #220 criterion 5 (`No retaliation, inferred refusal or delayed hazard response`) across both the store-independent `ChallengeRegister` (`zava_forward.core.challenges`) and the store-backed case workflow (`zava_forward.core.resident_decisions`). It extends both challenge surfaces to support all four required target kinds (`source`, `policy`, `proposal`, and `human_decision`) as well as challenge updates and escalations alongside recording and terminal resolution, adds fail-closed safeguard enforcement rejecting adverse/retaliatory/refusal/hazard-delay mutations, and proves zero retaliation penalties, zero inferred resident refusals, and zero statutory/safety hazard clock or emergency response delays across `ChallengeRegister`, JSON `Store`, SQLite `SqlStore`, `taskqueues`, and `ranking`.

### User Decisions and Requirements Highlights

* Deliver `No retaliation, inferred refusal or delayed hazard response` in `src/core` when an affected person submits or updates a challenge or correction request against a source, policy, proposal version, or human decision (caller prompt; Issue #220).
* Verify deterministically in `src/core/tests/test_issue_220_challenge_route.py` (alongside existing `test_challenges.py`) that recording, escalating, or resolving an affected-person challenge/correction request never triggers retaliation flags/penalties, never records an inferred resident refusal, and never delays or pauses any statutory/safety hazard clock or emergency response (caller prompt).
* Run only targeted `src/core` validation (`mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*challenge*.py' -v`), commit cleanly on `feat/ai-220-affected-person-challenge-2305` with the Copilot trailer, and do not push (caller prompt).

### What You May Not Know

* Escalating or updating an open challenge that carries an active `hazard_referral` (`status="referred_on_receipt"`) must preserve the original `received_on` date while transferring `to` ownership on escalation; resetting `received_on` would mask referral ageing in `hazard_referrals_overdue(today, max_days)`.
* `_res_challenge_resolve` in `resident_decisions.py` previously hardcoded `version=2`; updating it to `record["version"] + 1` keeps direct open-to-resolve flows at `version=2` while preserving monotonic optimistic concurrency when updates or escalations precede resolution.
* Live operational non-retaliation audits, resident/staff comprehension studies, and an owner-approved `max_days` threshold remain separate human governance gates outside unit code, so the commit uses `Refs #220` rather than claiming human operational gates are closed.

### Unresolved Decisions or Blockers

* None for `src/core` implementation.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Complete the full RPI loop (`research/`, `plans/`, `changes/`, `reviews/`) dated `2026-11-14` on branch `feat/ai-220-affected-person-challenge-2305` (target branch `feat/demo-164-chat-grounding-provenance-0900`).
* Deliver `No retaliation, inferred refusal or delayed hazard response` in `src/core` when an affected person submits or updates a challenge or correction request against a source, policy, proposal version, or human decision (Issue #220, PRD FR-052/AC-071/FR-043, Case Study 48 Addendum).
* Create deterministic unit tests in `src/core/tests/test_issue_220_challenge_route.py` verifying that recording, updating, escalating, or resolving an affected-person challenge/correction request never triggers retaliation flags/penalties, never records an inferred resident refusal, and never delays or pauses any statutory/safety hazard clock or emergency response.
* Run only targeted checks in `src/core` (`python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*challenge*.py' -v`); never run un-scoped `unittest discover -s tests` without `-p`.
* Leave `pyproject.toml` untouched (focused tier; avoid manifest modifications), commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push.

## Goals

* Support all four challenge target kinds (`source`, `policy`, `proposal`, and `human_decision`) and the full non-retaliatory lifecycle (`record`, `update`, `review`, `escalate`, `resolve`) in `src/core`.
* Enforce fail-closed safeguard invariants guaranteeing that challenge submission, update, escalation, and resolution never introduce retaliation flags/penalties, never infer resident refusals, and never delay or pause statutory/safety hazard clocks or emergency responses.
* Prove those invariants deterministically across both `ChallengeRegister` and `Store`/`SqlStore` (with `taskqueues` hazard clocks, `hazard` emergency events, `resident_decisions` measure consent/refusal state, and `ranking` deterministic order) in `src/core/tests/test_issue_220_challenge_route.py`.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/challenges.py`: `"human_decision"` in `SUBJECT_KINDS`, `"escalated"` in `STATUSES`, `update(...)`, `escalate(...)`, closed adverse-key input validation (`ChallengeSafeguardError`, `FORBIDDEN_ADVERSE_FIELDS`), explicit `safeguards` guarantee view fields, and pure case-state invariant verifier `assert_no_adverse_challenge_effects(before_case, after_case)`.
* `src/core/src/zava_forward/core/resident_decisions.py`: `target_kind == "human_decision"` dependency binding and exact staleness derivation, `challenge_update` and `challenge_escalate` resident actions, monotonic `version = record["version"] + 1` on resolution, and active `assert_no_adverse_challenge_effects` check around case challenge writes.
* `src/core/tests/test_issue_220_challenge_route.py`: deterministic unit tests covering all target kinds, channels, lifecycle verbs (`record`, `update`, `escalate`, `resolve`), and safeguard invariants across `ChallengeRegister`, JSON `Store`, and SQLite `SqlStore`.
* `src/core/README.md`: accurate documentation of the new `src/core` challenge route capabilities, tests, and remaining human acceptance boundaries.

### Non-Goals

* Web UI (`src/api/src/zava_forward/api/web/panels.js`) or HTTP route changes outside `src/core`.
* Infrastructure, Bicep, Dockerfile, workflow, or `pyproject.toml` edits.
* Claiming live human operational acceptance or pushing commits to remote.

## Functional Requirements

* FR-1: `ChallengeRegister` shall accept challenges and correction requests against `source`, `policy`, `proposal`, and `human_decision` versions via both `digital` and `staff_recorded` non-digital channels (`phone`, `in_person`, `paper`, `assisted_visit`), and shall mark only exact transitive dependents stale when resolved as `corrected`.
  * Observable acceptance criteria: Recording and correcting a `"human_decision"` (or `source`/`policy`/`proposal`) challenge stales only transitive dependents of that exact `(kind, id, version)` tuple while preserving prior versions and unrelated items.
* FR-2: `ChallengeRegister.update(...)` shall allow digital and staff-recorded non-digital updates on unresolved challenges (`received`, `under_review`, `escalated`), preserving the opening statement, appending immutable update records, optionally updating `next_update` and `explanations`, immediately referring newly raised `hazard_concern=True` items without resetting `received_on` on already-open hazard referrals, and rejecting updates to resolved challenges.
  * Observable acceptance criteria: Updating an open challenge preserves `statement`, appends to `updates` and `history`, keeps any prior unhanded `hazard_referral["received_on"]` unchanged so `hazard_referrals_overdue` age is never shortened, and raises `ValueError` on resolved challenges.
* FR-3: `ChallengeRegister.escalate(...)` shall escalate an unresolved challenge to a different named human owner with a recorded reason and `next_update` commitment, transitioning status to `"escalated"` while preserving any active `hazard_referral` (`status="referred_on_receipt"` and original `received_on`) without delay or reset.
  * Observable acceptance criteria: Escalating to the same owner or on a resolved challenge raises `ValueError`; escalating to a new human owner updates `owner`, sets `status == "escalated"`, transfers `hazard_referral["to"]` while preserving `originally_referred_to` and `received_on`, and keeps the referral listed in `hazard_referrals()`.
* FR-4: `challenges.py` shall fail closed (`ChallengeSafeguardError` / `ValueError`) if adverse/retaliatory, inferred-refusal, or hazard-delay fields (`FORBIDDEN_ADVERSE_FIELDS`) are injected into challenge inputs, and shall expose `assert_no_adverse_challenge_effects(before_case, after_case)` verifying zero retaliation/penalty/closure mutations, zero inferred resident refusals, and zero statutory/safety hazard clock or hold delays.
  * Observable acceptance criteria: Passing any forbidden key in challenge inputs or introducing any retaliation flag, priority penalty, inferred refusal (`Declined`/`Paused`/`Withdrawn`), unrelated closure, or delayed/paused hazard clock between `before_case` and `after_case` raises `ChallengeSafeguardError`.
* FR-5: `Store` and `SqlStore` (`resident_decisions.py`) shall support `target_kind="human_decision"` (requiring a recorded human disposition on the priority suggestion and staling only that exact `decision_version` on `"Correction recorded"`), `challenge_update`, and `challenge_escalate` on `affected_challenges`, with monotonic `version` increments and active `assert_no_adverse_challenge_effects` verification.
  * Observable acceptance criteria: Recording, updating, escalating, and resolving challenges across `source`, `policy`, `proposal`, and `human_decision` on JSON `Store` and SQLite `SqlStore` leaves `ranking.rank`/`sql_key`/`reasons`, `measure_decision_view`/`resident_status`, `case["hazards"]`, emergency audit entries, and `taskqueues.case_view()["hazard_clocks"]` completely unpenalized, un-refused, and un-delayed, while independent emergency `raise_hazard`/`refer_hazard`/`observe_hazard_times` succeed immediately while challenges are open or escalated.

## Non-Functional Requirements

* NFR-1: Static typing and lint conformance in `src/core`.
  * Objective threshold or evaluation condition: Zero errors from `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core` without modifying `pyproject.toml`.
  * Observable acceptance criteria: All three static commands exit 0 across all `src/core` files.
* NFR-2: Deterministic, fast, isolated unit execution.
  * Objective threshold or evaluation condition: Zero wall-clock sleeps, network calls, or shared mutable fixtures; `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*challenge*.py' -v` passes deterministically in under 5 seconds.
  * Observable acceptance criteria: Targeted test discovery runs both `test_challenges.py` and `test_issue_220_challenge_route.py` with 0 failures and 0 skips.

## Acceptance Criteria

* AC-1: Submitting or updating a challenge or correction request against a `source`, `policy`, `proposal`, or `human_decision` works across digital and non-digital routes in both `ChallengeRegister` and `Store`/`SqlStore`, marking only exact versioned dependents stale on correction.
* AC-2: Recording, updating, escalating, or resolving an affected-person challenge/correction request never triggers retaliation flags, sanctions, service/tenancy restrictions, unrelated closures, or priority ranking penalties (`ranking.rank`, `ranking.sql_key`, `ranking.reasons`).
* AC-3: Recording, updating, escalating, or resolving an affected-person challenge/correction request never records or infers a resident refusal (`measure_decisions`, `decision`, `resident_status` remain `"Not recorded"` or their prior explicit resident-recorded value).
* AC-4: Recording, updating, escalating, or resolving an affected-person challenge/correction request never delays, pauses, resets, or alters any statutory/safety hazard clock (`aware_at`, `response_due_at`, `resident_update_due_at`, `elapsed_hours`, `response_state`, `hold`), `hazard_referral` ageing (`received_on`), or immediate emergency hazard intake/referral (`raise_hazard`, `refer_hazard`, `observe_hazard_times`).
* AC-5: Fail-closed safeguard validation (`ChallengeSafeguardError`) actively rejects forbidden adverse/retaliation/refusal/hazard-delay inputs and detects tampered adverse side-effects on case snapshots.
* AC-6: All 4 `.copilot-tracking/` artifacts dated `2026-11-14` exist, `src/core/README.md` is updated, targeted checks pass, and the branch has a clean commit with the Copilot trailer and empty `git status --short`.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-11-14/220-affected-person-challenge-2305-plan.md |
| Phase details | .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md |
| Latest critique | .copilot-tracking/critiques/2026-11-14/220-affected-person-challenge-2305-critique.md (`Revise`; `PC-001` through `PC-003` resolved directly) |
| Relevant research | .copilot-tracking/research/2026-11-14/220-affected-person-challenge-2305-research.md |
| Changes-record role | .copilot-tracking/changes/2026-11-14/220-affected-person-challenge-2305-changes.md (`Complete`; full plan `P01` and `P02` implemented and verified) |
| Planning execution and readiness | Complete; all planned tasks implemented and reconciled for Review |
| Continuation context | Confirmed automatic RPI Agent return |

## Sources

* `.copilot-tracking/research/2026-11-14/220-affected-person-challenge-2305-research.md`: `C1`-`C12` codebase evidence across `challenges.py`, `resident_decisions.py`, `ranking.py`, `hazard.py`, `taskqueues.py`, `sqlstore.py`, and `pyproject.toml`.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: FR-052, AC-071, FR-043 contracts.
* `docs/case_study_48_addendum.md`: Responsible AI Release Position — Meaningful oversight and redress.
* `src/core/README.md`: Existing Issue #220 sections and component test boundaries.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Challenge Route Lifecycle and Non-Retaliation Safeguards

* Intent: Extend `challenges.py` and `resident_decisions.py` with `human_decision` target support, challenge `update` and `escalate` operations, closed adverse-input validation, and deterministic non-retaliation / non-refusal / non-hazard-delay invariant enforcement.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden `zava_forward.core.challenges` lifecycle and safeguard invariants

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4 (`C1`, `C2`, `C6`, `C7`, `C8`)
* Expected result: `ChallengeRegister` supports `SUBJECT_KINDS` including `"human_decision"`, `STATUSES` including `"escalated"`, `update(...)`, `escalate(...)`, closed adverse-key input checks, explicit `safeguards` metadata in `view()`, and `assert_no_adverse_challenge_effects(before_case, after_case)` raising `ChallengeSafeguardError` on any retaliation, inferred refusal, or hazard clock/hold delay.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Extend `zava_forward.core.resident_decisions` store-backed challenges with `human_decision`, `challenge_update`, `challenge_escalate`, and safeguard verification

* Requirement and evidence: FR-1, FR-4, FR-5 (`C4`, `C5`, `C9`, `C12`)
* Expected result: `_dependency` and `priority_challenge_state` support `"human_decision"`, `RESIDENT_ACTIONS` and `FOLLOWUP_ACTIONS` include `"challenge_update"` and `"challenge_escalate"`, `_res_challenge_resolve` increments `version` monotonically (`record["version"] + 1`), and challenge writes verify `assert_no_adverse_challenge_effects` across JSON `Store` and SQLite `SqlStore`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Deterministic Unit Verification, Documentation, and Validation

* Intent: Author `src/core/tests/test_issue_220_challenge_route.py`, update `src/core/README.md`, and pass all targeted static and unit checks cleanly.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Create `src/core/tests/test_issue_220_challenge_route.py` covering submit, update, escalate, and resolve safeguards

* Requirement and evidence: AC-1 through AC-5, NFR-1, NFR-2 (`C1`-`C12`)
* Expected result: Strictly typed deterministic unit test suite verifying `ChallengeRegister`, JSON `Store`, SQLite `SqlStore`, `ranking`, `resident_decisions`, `hazard`, and `taskqueues` across `source`, `policy`, `proposal`, and `human_decision` targets and digital/non-digital channels, proving zero retaliation flags/penalties, zero inferred refusals, zero delayed/paused hazard clocks or emergency responses, and fail-closed `ChallengeSafeguardError` enforcement.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update `src/core/README.md` and run targeted validation suite

* Requirement and evidence: AC-6, NFR-1, NFR-2
* Expected result: `src/core/README.md` documents the expanded Issue #220 `src/core` controls and honest human-gate boundary; `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*challenge*.py' -v` all exit 0.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md

## Dependencies

* Existing `zava-forward-core` editable environment with Python 3.12, `mypy`, and `ruff` (verified working in Research).

## Critique Disposition

Single-pass critique completed in `.copilot-tracking/critiques/2026-11-14/220-affected-person-challenge-2305-critique.md` (`Verdict: Revise`; 0 Critical, 1 High, 1 Medium, 1 Low; no divergent user decision required):

* `PC-001` (High, applied directly): Updated `P01-T01`, `P01-T02`, and `P02-T01` so `assert_no_adverse_challenge_effects` inspects `resident`, `funding`, `wave`, `service_requests`, and `appointments` alongside `closed`, `stage`, `days_in_stage`, `decision`, `measure_decisions`, `resident_reviews`, and `hazards`, recursively scans `after_case` (including nested `affected_challenges`) for `FORBIDDEN_ADVERSE_FIELDS`, enforces non-`affected_challenges` top-level case immutability, and checks `FORBIDDEN_ADVERSE_FIELDS` on `_res_challenge_*` inputs with `ChallengeSafeguardError` before generic `set(body) != fields` validation.
* `PC-002` (Medium, applied directly): Updated `P01-T01` and `P02-T01` so `ChallengeRegister.view(cid)` filters `explanations` inside `rec["updates"]` to `permitted=True` items alongside top-level `rec["explanations"]`, with a test verifying `permitted=False` update notes never appear in `view(cid)`.
* `PC-003` (Low, applied directly): Updated `P01-T01` and `P02-T01` so `ChallengeRegister.update(..., hazard_concern=True)` date-validates non-`None` `received_on` arguments while unconditionally preserving `referral["received_on"]` unchanged on active `referred_on_receipt` referrals whether the existing value is an ISO date string or `None`.

## Follow-Up Items

* Expose `challenge_update`, `challenge_escalate`, and `target_kind="human_decision"` in `src/api/src/zava_forward/api/web/panels.js` in a dedicated web slice under `web-design-guidelines`.
* Obtain live workflow acceptance evidence, resident/staff comprehension sign-off, and an owner-approved `max_days` hazard follow-up threshold before closing Issue #220's operational governance gate.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/220-affected-person-challenge-2305-changes.md
* Ready phase or task: Review (all active `P01` and `P02` tasks completed)
* Remaining provisional question or blocker: none

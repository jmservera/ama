<!-- markdownlint-disable-file -->
# RPI Plan: Issue #1238 Stale Pending Supersession and Retry/Receipt Verification

## Task Metadata

* Task ID: issue-1238
* Task slug: core-1238-stale-pending-2346
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md
* Plan critique: .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-critique.md

## Executive Summary

This plan delivers the final unchecked acceptance criterion of Issue #1238 (`(low F3) Mark a stale Pending attempt superseded`) in `src/core/src/zava_forward/core/resident_decisions.py` after verifying that the first four criteria from the #86 diff review (single outcome-write retry after `Acknowledged`, `receipt_ref` warning logging on write failure, failed-write regression tests, and `reservation_id`-bound lookup instead of `attempts[-1]`) are intact and passing. When an earlier formal-route send's outcome write failed and left its reservation in `"Pending"` (no longer `in_flight`), recording an explicit retry via `service_forward` (`retry_unresolved=True`) will atomically mark any stale `"Pending"` attempt `"Superseded"` (`superseded_from="Pending"`, `superseded_at`, `superseded_by_attempt`) inside the same store transaction that appends the superseding attempt, preserving full audit history, `route_key` idempotency, and late-outcome fencing across JSON and SQLite backends.

### User Decisions and Requirements Highlights

* Deliver AC 5 (low F3) using the module's title-case `"Superseded"` vocabulary when an explicit retry or superseding attempt is recorded after a stale/failed `"Pending"` reservation, while keeping ACs 1-4 verified and intact.
* Preserve full audit history, `route_key` idempotency, and distinct provenance from Owner Decision Q6 (`manual_verified` two-person `service_supersede_authorize` without resending).
* Do not use bulk `del sys.modules[...]` in test files, validate with `mypy`, `ruff check`, `ruff format --check`, and `unittest` in `src/core`, and commit locally on `fix/core-1238-stale-pending-2346` with `Closes #1238` without pushing.

### What You May Not Know

* One existing regression test (`test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend` in `src/core/tests/test_resident_decisions.py`) currently asserts `["Pending", "Acknowledged"]` after `self.forward(retry_unresolved=True)` because F3 had not yet been applied to `_res_service_forward`; updating that post-retry expectation to `["Superseded", "Acknowledged"]` while keeping pre-retry `"Pending"` assertions proves the exact state transition.
* Marking stale `"Pending"` attempts `"Superseded"` at reservation time immediately fences `_res_service_forward_outcome` against delayed outcome writes for the superseded attempt, causing `_record_outcome` to log any unrecorded `receipt_ref` and fail closed rather than mutating a superseded attempt.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI workflow (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) in `/home/azureuser/source/ama-demo-wt/feat-1238-stale-pending-2346` on branch `fix/core-1238-stale-pending-2346` targeting `feat/demo-164-chat-grounding-provenance-0900` (caller brief).
* Verify ACs 1-4 of Issue #1238 in `src/core/src/zava_forward/core/resident_decisions.py` and `src/core/tests/test_resident_decisions.py`: single outcome-write retry after `Acknowledged`, `receipt_ref` warning log when outcome write still fails, failed-write regression test coverage, and safe `reservation_id` lookup instead of `attempts[-1]` after reservation (caller brief; `.copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md`).
* Implement AC 5 (`(low F3) Mark a stale Pending attempt superseded`): mark a stale `"Pending"` attempt as `"Superseded"` when an explicit retry or superseding attempt is recorded after a stale/failed `"Pending"` reservation, preserving full audit history and idempotency invariants, with focused unit tests (caller brief; Issue #1238).
* Preserve Owner Decision Q6 (`manual_verified`, 2026-11-08): age alone never marks `"Pending"` as `"Superseded"` and never authorizes resend; two-person `service_supersede_authorize` (`attempt["supersession"]`) remains distinct from retry-triggered supersession (`src/core/README.md`).
* Write all dated RPI artifacts under `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-14/core-1238-stale-pending-2346*` (caller brief).
* Never use bulk `del sys.modules[...]` in test files (caller brief).
* Validate in `src/core` with `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and the focused `unittest` suite covering `resident_decisions`, then commit cleanly on `fix/core-1238-stale-pending-2346` with `Closes #1238` and the Copilot `Co-authored-by` trailer without pushing (caller brief).

## Goals

* Transition stale `"Pending"` formal-route attempts to `"Superseded"` atomically when an explicit retry (`service_forward` with `retry_unresolved=True` and no active in-flight send) reserves a superseding attempt.
* Preserve complete attempt audit history, stable `route_key` idempotency, late-outcome fencing, retention-deletion scrubbing, and `manual_verified` dual-authorization separation across JSON and SQLite stores.
* Document and regression-test the transition thoroughly while keeping ACs 1-4 verified and passing all `src/core` static-analysis, lint, format, and unit-test checks.

## Scope and Non-Goals

### In Scope

* Atomic stale-`"Pending"`-to-`"Superseded"` transition and audit detail update in `ResidentDecisionMixin._res_service_forward` (`src/core/src/zava_forward/core/resident_decisions.py`).
* Focused unit and regression tests in `src/core/tests/test_resident_decisions.py` (`JsonResidentDecisions` and `SqlResidentDecisions`).
* Directly related documentation update in `src/core/README.md`.
* Full `src/core` validation (`mypy`, `ruff check`, `ruff format --check`, `unittest`) and local commit on `fix/core-1238-stale-pending-2346`.

### Non-Goals

* Modifying `_record_outcome`, `_outcome_recorded`, `_forward` reservation lookup, or `SupersessionBinding` (`#1346` low review follow-ups `RV-1`/`RV-2` are out of scope).
* Changing `complaints_route.STATUSES` (which intentionally restricts receiver-supplied outcomes to `"Unconfigured"`, `"Failed"`, `"Unconfirmed"`, `"Acknowledged"`).
* Using `del sys.modules[...]` in any test file or pushing commits to any remote.

## Functional Requirements

* FR-1: When `ResidentDecisionMixin._res_service_forward` executes with `retry_unresolved=True`, no attempt for `(case_id, req["id"])` is `in_flight`, and all version, route, status, actor-permission/independence, and `resident_request_ref` checks pass, every existing attempt in `route["attempts"]` with `status == "Pending"` transitions in place to `status == "Superseded"` with `superseded_from="Pending"`, `superseded_at=now`, and `superseded_by_attempt=attempt` (matching the new attempt's `reserved_at = now`).
  * Observable acceptance criteria: After a failed outcome write leaves attempt 1 `"Pending"` and an authorized operator invokes `service_forward` with `retry_unresolved=True`, attempt 1 has `status == "Superseded"`, `superseded_from == "Pending"`, ISO timestamp `superseded_at`, and `superseded_by_attempt == 2`, with no `supersession` key added unless previously created by `service_supersede_authorize`.
* FR-2: Prior attempts in `"Unconfirmed"`, `"Failed"`, or already-`"Superseded"` status (including `manual_verified` two-person supersessions) remain unmodified when a subsequent explicit retry reserves a new attempt, and refused or rolled-back `service_forward` calls leave stale `"Pending"` attempts unchanged.
  * Observable acceptance criteria: Retrying after `"Unconfirmed"`, legacy `"Failed"`, `service_supersede_authorize`, or chained stale `"Pending"` attempts never overwrites non-`"Pending"` attempts or earlier `superseded_at`/`superseded_by_attempt` values; omitted `retry_unresolved`, `in_flight` sends, permission/validation failures, and failed `store.save()` calls leave attempt 1 `"Pending"`.
* FR-3: Full audit history, idempotency invariants, late-outcome fencing, and retention-deletion scrubbing hold for retry-superseded attempts.
  * Observable acceptance criteria: Original reservation fields (`attempt`, `reservation_id`, `request_id`, `request_version`, `resident_request_ref`, `requested_by`, `reserved_at`, `reason`) remain intact; envelopes share the same `route_key` as `idempotency_key`; case audit detail records the superseded attempt number(s); late `_record_outcome` / `_res_service_forward_outcome` calls targeting the superseded attempt fail closed (`ResidentCommittedError`) and log `receipt_ref`; `delete_resident_records` removes `resident_request_ref` and `requested_by` while keeping supersession metadata.
* FR-4: ACs 1-4 of Issue #1238 remain intact and verified (`_record_outcome` single retry without resend, `receipt_ref` warning log on persistent or unverified-recovery write failure, failed-write regression tests, and `reservation_id`-bound lookup after reservation).
  * Observable acceptance criteria: Existing unit tests for ACs 1-4 pass across `JsonResidentDecisions` and `SqlResidentDecisions`.

## Non-Functional Requirements

* NFR-1: Static type safety, lint cleanliness, formatting compliance, and test isolation in `src/core`.
  * Objective threshold or evaluation condition: Zero errors from `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -q` in `src/core`, with zero occurrences of bulk `del sys.modules[...]` in `src/core/tests/test_resident_decisions.py`.
  * Operating condition or verification approach, if needed: Execute directly in `src/core` during implementation and review verification.
  * Observable acceptance criteria: All four commands exit `0` and `git diff` confirms clean test isolation.

## Acceptance Criteria

* AC-1: Outcome write is retried once on failure after an `Acknowledged` receipt without contacting the receiver again (verified intact).
* AC-2: `receipt_ref` is logged at `WARNING` level when the outcome write still fails or recovery is unverified (verified intact).
* AC-3: Regression tests cover the failed-write, single-retry, lost-commit reconciliation, and unverified-recovery paths across JSON and SQLite stores (verified intact).
* AC-4: Attempt lookup after reservation binds by `reservation_id` rather than indexing `attempts[-1]` (verified intact).
* AC-5: Recording an explicit retry (`service_forward` with `retry_unresolved=True` when not `in_flight`) after a stale/failed `"Pending"` reservation marks prior `"Pending"` attempt(s) `"Superseded"` (`superseded_from="Pending"`, `superseded_at`, `superseded_by_attempt`), preserves full audit history and `route_key` idempotency, fences late outcome writes, updates `src/core/README.md`, and passes focused unit tests plus `mypy` and `ruff` in `src/core`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-plan.md                                                                  |
| Phase details                    | .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md                                                       |
| Latest critique                  | .copilot-tracking/plans/2026-11-14/core-1238-stale-pending-2346-critique.md with Revise disposition (PC-001 and PC-002 directly resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md                                                           |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/core-1238-stale-pending-2346-changes.md is created by implementation as its evidence record         |
| Planning execution and readiness | Complete; ready for implementation                                                                                                       |
| Continuation context             | Confirmed automatic RPI Agent parent return                                                                                              |

## Sources

* .copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md: Grounded codebase evidence `C1`-`C14` verifying ACs 1-4 and establishing the convergence design for AC 5.
* src/core/src/zava_forward/core/resident_decisions.py: Owns `_forward`, `_record_outcome`, `_outcome_recorded`, `_res_service_forward`, `_res_service_forward_outcome`, `_res_service_supersede_authorize`, and `delete_resident_records`.
* src/core/tests/test_resident_decisions.py: Owns `JsonResidentDecisions` and `SqlResidentDecisions` formal-route forwarding, retry, reservation-binding, and supersession unit tests.
* src/core/README.md: Documents formal-route forwarding, unresolved retry rules, and `Pending` supersession semantics.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Atomic Stale `Pending` Supersession in `_res_service_forward`

* Intent: Transition stale `"Pending"` attempts to `"Superseded"` atomically when an authorized explicit retry reserves a superseding formal-route attempt.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Transition prior `Pending` attempts to `Superseded` in `ResidentDecisionMixin._res_service_forward`

* Requirement and evidence: FR-1, FR-2, FR-3, AC-5; `.copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md` (`C3`, `C10`, `C11`, `C13`)
* Expected result: When `service_forward` with `retry_unresolved=True` reserves attempt `N` after passing all validation, `not in_flight`, actor-identity, and `resident_request_ref` checks, every prior attempt with `status == "Pending"` updates in place to `status="Superseded"`, `superseded_from="Pending"`, `superseded_at=now`, and `superseded_by_attempt=N`, and the audit detail reports superseded attempt number(s).
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Unit Tests and Component Documentation

* Intent: Prove stale `"Pending"` supersession, audit/idempotency preservation, late-outcome fencing, and non-interference across JSON and SQLite stores, and synchronize `src/core/README.md`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update and add focused `resident_decisions` unit tests without `sys.modules` deletion

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, AC-1..AC-5; `.copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md` (`C8`, `C9`, `C12`, `C14`)
* Expected result: `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend` asserts `["Superseded", "Acknowledged"]` post-retry while preserving pre-retry `"Pending"` checks, and focused new tests in `JsonResidentDecisions` (inherited by `SqlResidentDecisions`) cover Complaint + Independent review routes, audit/idempotency field preservation, refused/rolled-back retries, chained stale `Pending` retries, non-`Pending` / `manual_verified` preservation, late-outcome fencing with `receipt_ref` logging, and `delete_resident_records` scrubbing.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update `src/core/README.md` formal-route supersession documentation

* Requirement and evidence: AC-5; `.copilot-tracking/research/2026-11-14/core-1238-stale-pending-2346-research.md` (`C1`, `C10`, `C11`)
* Expected result: Both the unresolved-retry paragraph and the `Pending supersession` paragraph in `src/core/README.md` are synchronized so `Pending`, `Unconfirmed`, `Superseded`, and legacy `Failed` without `not_sent` are listed as unresolved, a failed outcome save stays `Pending` until superseded, and both `service_supersede_authorize` (`manual_verified` two-person supersession without resending) and explicit `service_forward` (`retry_unresolved=True` when not in flight, recording `superseded_by_attempt`) are accurately documented.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: `src/core` Validation Gate

* Intent: Verify type checking, linting, formatting, and unit tests in `src/core`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run `mypy`, `ruff check`, `ruff format --check`, and focused `unittest` suites in `src/core`

* Requirement and evidence: FR-4, NFR-1, AC-1..AC-5
* Expected result: `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest test_resident_decisions test_sqlreads -q` all exit `0` in `src/core`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/core-1238-stale-pending-2346-phase-details.md

## Dependencies

* Existing `src/core` editable/installed environment with `Python 3.12.3`, `mypy`, `ruff`, and standard-library `unittest` + `sqlite3`: verified available locally.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition        | Plan response or residual risk |
|--------------------------|--------------------|--------------------------------|
| Run 1: PC-001 [Low]      | resolved           | Replaced nonexistent `resident_retention_delete` reference with `delete_resident_records` in FR-3, Sources, P02, and P02-T01 |
| Run 1: PC-002 [Low]      | resolved           | Scoped P02-T02 across both the unresolved-retry paragraph and the `Pending supersession` paragraph in `src/core/README.md` so `"stays Pending"` is qualified and `"Superseded"` is included among unresolved statuses |
| Run 1: residual risk     | accepted_with_risk | Per-instance `_IN_FLIGHT` tracking remains single-process as documented in `src/core/README.md`, and `AzureResidentDecisions` remains environment-gated locally while sharing `ResidentDecisionMixin` and `validate_sql` with `SqlResidentDecisions` |

## Follow-Up Items

* `#1346` low review item `RV-1` (`SupersessionBinding._roles` `MappingProxyType` + exact `type(binding) is SupersessionBinding` check): outside Issue #1238 AC 5 surgical scope; retained as ranked post-Review follow-up candidate.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/core-1238-stale-pending-2346-changes.md
* Ready phase or task: All planned phases and tasks completed (P01-P03); ready for Review
* Remaining provisional question or blocker: none

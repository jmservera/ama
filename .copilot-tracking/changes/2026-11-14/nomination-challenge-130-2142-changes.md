---
title: "RPI Changes: nomination-challenge-130-2142"
description: "Implementation changes and verification evidence for Issue 130 locally verifiable controls in src/core"
ms.date: 2026-11-14
---

## Metadata

* Task ID: nomination-challenge-130-2142
* Related plan: .copilot-tracking/plans/2026-11-14/nomination-challenge-130-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`
* All remaining active-plan markers: None
* Status basis: All planned tasks in `P01` and `P02` completed and verified against the mandatory bare `mypy`/`ruff`/`unittest discover` gate plus `src/core` and `src/api` regression suites.

## Execution Summary

Delivered all four locally verifiable acceptance criteria for Issue #130 in `src/core` across both pure domain helpers (`nomination_route.py`) and store-backed JSON `Store` / SQLite `SqlStore` resident workflows (`resident_decisions.py`), with worktree-isolated strict-typed tests (`test_nomination_route.py`, `test_resident_decisions.py`).

## Completed Work

### P01-T01: Store-Independent Nomination, Challenge, Re-Review, and Hazard Controls

* Hardened `src/core/src/zava_forward/core/nomination_route.py` under `mypy --strict`:
  * Unified `HazardRouted` (`HAZARD_INTAKE`, `HAZARD_MESSAGE`, `HAZARD_ROUTING_MESSAGE`) with case-aware `hazard_routing(hazard_concern, case_id=...)` returning `None` only when `hazard_concern is False` and routing `True`, `None`, and any non-`False` value immediately to `/api/cases/{case_id}/hazard-raise` (`issue="#85"`, `route="independent_hazard_intake"`, `queue_item_created=False`, `immediate=True`).
  * Hardened `missing_before_review` and `require_ready_for_review` to reject blank/whitespace strings and role-label owners (`owner["name"].strip().casefold() == owner["role"].strip().casefold()`).
  * Expanded `challenge_trail` to retain `"original_account"` alongside structured `"original"` provenance, competing evidence entries (`version`, `reported_subject_ref`, `account`, `source`, `channel`, `raised_by`, `representative_ref`, `challenge_id`, `challenged_review`, and live `challenge_status`/`challenge_resolution` overlaid from `case["affected_challenges"]`), all human review entries, and `not_decided` boundaries.
  * Implemented fail-closed `parse_node`, `parse_dependencies`, and version-cutoff `re_review_set` backed by `ChallengeRegister.dependents(corrected)`, keeping `automatic_acceptance=False`, `automatic_sanction=False`, `priority_changed=False`, and `consent_changed=False`.

### P01-T02: Store and SqlStore Resident Workflow Integration

* Updated `src/core/src/zava_forward/core/resident_decisions.py`:
  * Re-exported `HAZARD_INTAKE_ROUTE`, `HAZARD_ROUTING_MESSAGE`, and `HazardRouted` from `nomination_route`, and updated `_refuse_hazard` so explicit `hazard_concern=None` (in addition to `True` and non-boolean values) fails closed across `nomination_record`, `nomination_acknowledge`, `nomination_review`, `nomination_correct`, and `challenge_open` with case-specific `route["action"]`.
  * Added `nomination_acknowledge` to `RESIDENT_ACTIONS` and `INTAKE_ACTIONS` (`_res_nomination_acknowledge`) so unready or legacy referrals can record a named registered owner, staff-recorded acknowledgement reference, staffed non-digital route, and next update date (preserving `acknowledgement_history` and `original` account, enforcing `_owner_rights` when an existing owner is `"Known"`, and verifying `challenges.assert_no_retaliation`).
  * Hardened `_res_nomination_review` to reject hazard flags, require `nomination_route.require_ready_for_review(record)` plus a `"Known"` registered owner identity, enforce independent human review (`_require_independent_reviewer`), and verify `challenges.assert_no_retaliation`.
  * Fixed `_raiser` to strip `representative_ref`, evaluate the latest authority per measure across multi-measure cases against all `Communicate`, safe-contact, context-revision, and retention invariants (leaving `authority_for` unchanged), enabled `raised_by`/`representative_ref` on `_res_challenge_open`, and scrubbed `affected_challenges[*]["representative_ref"]` in `delete_resident_records`.
  * Wired optional `dependencies` in `_res_nomination_correct` through `nomination_route.parse_dependencies` and `nomination_route.re_review_set` while keeping the default `correction["re_review"]` structure backward-compatible when `dependencies` is omitted.
  * Delegated `nomination_follow_up` readiness checks to `nomination_route.missing_before_review` and exposed `record["challenge_trail"]` in `followup_view`.

### P02-T01: Worktree-Isolated Bare Verification and Regression Tests

* Updated `src/core/tests/test_nomination_route.py` with conditional worktree path bootstrap (`_bootstrap_worktree_paths` evicting `zava_forward*` only when loaded outside `<worktree>/src`), 4 pure `NominationRoute` unit tests, and 8 store-backed acceptance tests (`JsonNominationChallengeRoute` and `SqlNominationChallengeRoute` covering AC1..AC4).
* Updated `src/core/tests/test_resident_decisions.py` to test `nomination_acknowledge` pre-review completion across JSON and SQLite stores and explicit `hazard_concern=None` routing across intake, correction, review, and challenge actions.

## Implementation-Time Plan and Detail Updates

* Local judgment during `P02-T01`: used `taskqueues.overdue_tasks(..., as_of="2100-01-01T00:00:00Z", handoff=None)` in `test_nomination_route.py` to verify zero nomination queue tasks are added on `HazardRouted`, matching the actual typed `taskqueues` API.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` (309 source files) | Passed | `Success: no issues found in 309 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (256 formatted files) | Passed | `256 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v` | Bare worktree discovery (`NominationRoute`, `JsonNominationChallengeRoute`, `SqlNominationChallengeRoute`) | Passed | `Ran 12 tests in 4.058s — OK` |
| `PYTHONPATH=src:tests:../agents/src python3 -m unittest tests.test_nomination_route tests.test_resident_decisions tests.test_challenges tests.test_hazard_referral tests.test_taskqueues` | `src/core` regression suites | Passed | `Ran 547 tests in 169.435s — OK (skipped=159)` |
| `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest tests.test_nomination_screen tests.test_resident_api` | `src/api` cross-package compatibility | Passed | Exited `0` |

## Pre-Review Reconciliation

* Plan markers and phase details: Synchronized (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01` checked `[x]`).
* Completed-work evidence and handoff prose: Reconciled with `nomination_route.py`, `resident_decisions.py`, `test_nomination_route.py`, and `test_resident_decisions.py`.
* Validation, blockers, remaining work, and follow-up items: All planned validations passed; zero blockers; zero remaining active-plan work.
* Review readiness: Ready

## Blockers

* None

## Remaining Work

* None in active plan scope.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/nomination-challenge-130-2142-plan.md, `## Follow-Up Items`
* Author interactive UI forms in `src/api` for `nomination_record`, `nomination_acknowledge`, `nomination_correct`, and `nomination_review` (owner: web/API slice for `#130`).
* Ratify `OD-41` and `OD-42` operational policy thresholds with housing operations and compliance leads (owner: governance).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`; remaining None
* Validation coverage: Mandatory bare `mypy`/`ruff`/`unittest discover` gate passed (`12/12`), `src/core` resident/challenge/hazard/taskqueue regression suites passed (`547` run, `0` failed), `src/api` nomination/resident API suites passed
* Blockers: None
* Current plan and detail updates: All `P01` and `P02` checklist markers checked `[x]`
* Planning and critique state: Ready (`PC-001`..`PC-005` resolved)
* Follow-up items: UI form authoring in `src/api` and human ratification of `OD-41`/`OD-42`
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent

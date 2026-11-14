<!-- markdownlint-disable-file -->
# RPI Changes: 220-affected-person-challenge-2305

## Metadata

* Task ID: issue-220-criterion-5-affected-person-challenge-2305
* Related plan: .copilot-tracking/plans/2026-11-14/220-affected-person-challenge-2305-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/220-affected-person-challenge-2305-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full_plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02
* All remaining active-plan markers: none
* Status basis: Every task across `P01` and `P02` is implemented, documented, and verified cleanly under the required targeted static and unit checks.

## Execution Summary

Implemented the locally verifiable `src/core` non-retaliation, non-inferred-refusal, and non-delayed-hazard-response controls and deterministic unit tests for Issue #220 across both `zava_forward.core.challenges` (`ChallengeRegister`) and `zava_forward.core.resident_decisions` (`Store` and `SqlStore`), updated `src/core/README.md`, and verified clean execution of `mypy`, `ruff check .`, `ruff format --check .`, and all 28 targeted challenge tests.

## Completed Work

### Store-Independent Challenge Register Lifecycle and Safeguard Invariants

* Related phase or task: P01-T01 (`P01`)
* Files: `src/core/src/zava_forward/core/challenges.py`
* What changed and why: Added `"human_decision"` to `SUBJECT_KINDS` and `"escalated"` to `STATUSES`; implemented `ChallengeRegister.update(...)` (digital and staff-recorded non-digital channels, keeping the opening statement immutable, filtering non-permitted update explanations in `view(cid)`, and unconditionally preserving original `received_on` including `None` on active `referred_on_receipt` hazard referrals) and `ChallengeRegister.escalate(...)` (transferring to a distinct named human owner and preserving active hazard referrals without resetting `received_on`); added `ChallengeSafeguardError`, `FORBIDDEN_ADVERSE_FIELDS`, `SAFEGUARDS`, `reject_adverse_mapping`, and `assert_no_adverse_challenge_effects(before_case, after_case)` enforcing zero retaliation/priority/closure mutations, zero inferred resident refusals, and zero statutory/safety hazard clock or hold delays.
* Completion evidence: `src/core/src/zava_forward/core/challenges.py` diff and 22 passing register/safeguard tests across `test_challenges.py` and `test_issue_220_challenge_route.py`.
* Validation: Passed (`mypy`, `ruff check .`, `ruff format --check .`, `unittest`).

### Store-Backed Affected-Person Challenge Lifecycle and Transactional Safeguards

* Related phase or task: P01-T02 (`P01`)
* Files: `src/core/src/zava_forward/core/resident_decisions.py`
* What changed and why: Added `target_kind == "human_decision"` binding in `_dependency` and exact staleness derivation in `priority_challenge_state` when `resolved_by` is present; registered `"challenge_update"` and `"challenge_escalate"` in `RESIDENT_ACTIONS` and `FOLLOWUP_ACTIONS` so transactional `validate_sql` replay covers SQLite writes; implemented `_res_challenge_update` and `_res_challenge_escalate`; made `_res_challenge_resolve` accept `"Open"` or `"Escalated"` and increment `version = record["version"] + 1` monotonically; added pre-schema `challenges.reject_adverse_mapping` (`ChallengeSafeguardError`) and post-mutation `challenges.assert_no_adverse_challenge_effects(before, c)` across all four `_res_challenge_*` handlers.
* Completion evidence: `src/core/src/zava_forward/core/resident_decisions.py` diff and passing `JsonStoreChallengeSafeguardTests` + `SqlStoreChallengeSafeguardTests`.
* Validation: Passed (`mypy`, `ruff check .`, `unittest`).

### Deterministic Challenge Route Safeguard Unit Suite

* Related phase or task: P02-T01 (`P02`)
* Files: `src/core/tests/test_issue_220_challenge_route.py`
* What changed and why: Created strictly typed deterministic unit test suite covering `ChallengeRegister`, JSON `Store`, and SQLite `SqlStore` across `source`, `policy`, `proposal`, and `human_decision` targets and all digital/non-digital channels through submit, update, escalate, and resolve, proving zero retaliation/ranking penalties (`ranking.rank`, `ranking.sql_key`, `ranking.reasons`, `Store._ranking`), zero inferred refusals (`measure_decision_view`, `resident_status`), zero hazard clock/hold delays (`taskqueues.context` `hazard_clocks`, `raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times`, immediate `Emergency` hazard intake while challenges are escalated), and fail-closed `ChallengeSafeguardError` rejection.
* Completion evidence: 9 new test methods (including JSON and SQLite suites; 28 total tests with `test_challenges.py`) passing in 2.33s.
* Validation: Passed (`mypy` on 328 files, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*challenge*.py' -v`).

### Component Documentation and Targeted Validation

* Related phase or task: P02-T02 (`P02`)
* Files: `src/core/README.md`
* What changed and why: Updated both `#version-bound-affected-person-challenges-220` and `## Affected-person challenge and correction route (#220)` in `src/core/README.md` to document `human_decision` target support, `update`/`escalate` (`challenge_update`/`challenge_escalate`), `ChallengeSafeguardError` / `assert_no_adverse_challenge_effects`, `test_issue_220_challenge_route.py`, and the remaining non-code human operational gates.
* Completion evidence: Clean diff in `src/core/README.md` and 0-exit targeted validation command.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

### Untouched Sensor Consent Compatibility in Case Safeguard Check

* Affected plan area or markers: P01-T01 (`assert_no_adverse_challenge_effects`)
* What changed: Local judgment refinement during P01-T01 ensured `assert_no_adverse_challenge_effects` inspects `after_case["affected_challenges"]` recursively for `FORBIDDEN_ADVERSE_FIELDS` and checks top-level adverse field additions/mutations plus full non-`affected_challenges` top-level case equality, so untouched pre-existing `sensors[...]["consent"]` entries on a home record never cause false positives while any adverse mutation fails closed.
* Why: Code search (`sensor_view.py`, `sensor_consumer.py`) showed legitimate case sensor controls store `"consent"`.
* Triggering evidence: `src/core/src/zava_forward/core/sensor_view.py` and `sensor_consumer.py`.
* User answer or decision: none needed (preserves approved intent and strengthens accuracy).
* Reconciliation performed: Verified by explicit subtest in `test_fail_closed_safeguard_errors_on_adverse_inputs_and_case_tampering`.
* Planning and critique state: not needed; ready.

## Validation Record

| Check | Scope | Status | Evidence or reason |
| --- | --- | --- | --- |
| `python3 -m mypy` | `src/core` (328 files) | Passed | `Success: no issues found in 328 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (275 files) | Passed | `275 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*challenge*.py' -v` | `test_challenges.py` + `test_issue_220_challenge_route.py` | Passed | `Ran 28 tests in 2.327s — OK` |
| Full un-scoped `unittest discover -s tests` | `src/core/tests` | Skipped | Explicitly prohibited by caller instructions (`NEVER run full unittest discover -s tests without -p`) |

## Pre-Review Reconciliation

* Plan markers and phase details: current (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all checked and complete)
* Completed-work evidence and handoff prose: current
* Validation, blockers, remaining work, and follow-up items: current
* Review readiness: ready

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/220-affected-person-challenge-2305-plan.md, `## Follow-Up Items`
* Expose `challenge_update`, `challenge_escalate`, and `target_kind="human_decision"` in `src/api/src/zava_forward/api/web/panels.js` in a dedicated web slice under `web-design-guidelines`.
* Obtain live workflow acceptance evidence, resident/staff comprehension sign-off, and an owner-approved `max_days` hazard follow-up threshold before closing Issue #220's operational governance gate.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full_plan; completed: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02; remaining: none
* Validation coverage: `mypy` (328 files), `ruff check .`, `ruff format --check .`, and targeted challenge unit suite (`28` tests across `test_challenges.py` and `test_issue_220_challenge_route.py`) all passed (`focused` tier)
* Blockers: none
* Current plan and detail updates: local compatibility guard for untouched `sensors[...]["consent"]` recorded
* Planning and critique state: ready (`PC-001` through `PC-003` resolved and verified)
* Follow-up items: `src/api` web panel exposure and human operational governance sign-off
* Review readiness or no-handoff reason: ready for Review
* Continuation owner: parent for confirmed automatic RPI Agent

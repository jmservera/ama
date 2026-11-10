<!-- markdownlint-disable-file -->
# Phase details: issue 1238 outcome persistence retry (recovery 1109)

Plan: [plan](../../plans/2026-11-09/issue-1238-outcome-retry-recovery-1109-plan.md).

## Phase 1: tests first

* File `src/core/tests/test_resident_decisions.py`, class
  `JsonResidentDecisions` near
  `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend`.
* Add helper wrapping `self.store.save` that acts only when the in-memory
  attempt is `Acknowledged` (the outcome write), counting calls: mode `before`
  raises without saving; mode `after` saves then raises `RuntimeError`.
* Success criteria: new tests fail on base source (the first outcome failure
  raises `ResidentCommittedError`); the strengthened exhaustion test fails on
  the missing log and handler count.

## Phase 2: source

* `_forward` calls `_record_outcome(store, user, case_id, outcome)` in place of
  the inline `try`.
* `_record_outcome`: up to two executions of the same `_operation`. Re-raise
  `ResidentCommittedError` unchanged. After a failure without a recorded
  recovery failure note, if `_outcome_recorded` finds the same reservation,
  status and receipt on the attempt, return. If both fail, log one warning with
  exception type, case, request, attempt, status and `repr(receipt_ref)` and
  raise the existing `ResidentCommittedError` message `from` the last error.
* `_outcome_recorded` reads the attempt under `store.lock`.
* Success criteria: no receiver change; no new store API.

## Phase 3: validation

Commands and results are recorded in the changes file and handoff; raw output
stays in the owned external scratch directory.

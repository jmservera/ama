<!-- markdownlint-disable-file -->
# Plan: issue 1238 outcome persistence retry (recovery 1109)

Task `issue-1238-outcome-retry-recovery-1109`. Written 2026-11-09 before any
source edit. Research:
[research](../../research/2026-11-09/issue-1238-outcome-retry-recovery-1109-research.md).
Details: [details](../../details/2026-11-09/issue-1238-outcome-retry-recovery-1109-details.md).

## Objective

Repair acceptance criteria 1 to 3 of issue 1238 in
`src/core/src/zava_forward/core/resident_decisions.py` and its existing test
module, with the receiver submitted once. F2 is already present and is not
claimed. F3 is assessed and not implemented. Use `Refs`, not a closing keyword.

## Phases

* [ ] Phase 1: focused regression tests first, shown failing against base
  source (red).
* [ ] Phase 2: add `_record_outcome` with one bounded retry, reconciliation of
  an already-recorded identical outcome and `receipt_ref` logging.
* [ ] Phase 3: targeted validation on JSON, SQLite and an owned local SQL
  Server, plus module, lint and type profiles.
* [ ] Phase 4: changes record, one post-implementation review, handoff.

## Planned tests (existing `test_resident_decisions.py`, `JsonResidentDecisions`)

The class is inherited by the SQLite and MSSQL classes, so each case runs on
all three stores.

1. Transient failed write succeeds on the one retry: first outcome save raises
   before commit; expect no error, one attempt, status `Acknowledged`, the
   receipt kept, receiver called once, same idempotency key.
2. Ambiguous committed save: real save runs, then raises; expect success
   without a second receiver call, no duplicate attempt, receipt kept.
3. Exhausted retry: strengthen the existing
   `test_forward_outcome_save_failure_leaves_pending_and_blocks_silent_resend`
   to assert the outcome handler ran exactly twice, a warning log carries the
   valid `receipt_ref`, the attempt stays `Pending`, the explicit
   `ResidentCommittedError` is raised, a plain resend is refused, the manual
   `retry_unresolved` path still works and keeps the idempotency key.
   Critique amendment (see [critique](issue-1238-outcome-retry-recovery-1109-critique.md)):
   case 2 simulates a lost commit acknowledgement (real save, then clear
   `persisted` and raise), not a post-COMMIT failure, which is already a
   known-committed error on SQL.
3a. An error carrying a recovery-failure note is not retried or reconciled;
   it logs the receipt and raises the explicit error after one handler run.
4. Existing owner, reviewer, in-flight and reservation tests remain unchanged
   and are rerun.

## Design constraints

* No second `receiver.submit`; same reservation, attempt, outcome, key.
* Retry only non-`ResidentCommittedError` failures; never after a committed
  acknowledgement failure.
* No claim of success when recovery failed (state unknown) and no swallowed
  exception: exhaustion still raises `ResidentCommittedError`.
* No store, schema, API or Quality file change.

## Validation (owner demo targeted)

* Red/green: the three focused tests on JSON.
* Whole `test_resident_decisions` JSON and SQLite; the focused cases on MSSQL
  via an owned loopback SQL Server container under the shared heavy lock with
  one non-queued admission; if unavailable, report blocked.
* `ruff`, `mypy` per the component config; import and diff review.
* Not run: full gate, browser, hosted CI, cloud, real receiver.

## Review-correction cycles

Five total allowed for this loop; none spent; initial implementation is not a
cycle.

<!-- markdownlint-disable-file -->
# Review: issue 1238 outcome persistence retry (recovery 1109)

Original, immutable outcome. Executed once, 2026-11-09 after the
Implement-to-Review transition (22:21:31Z), by an independent read-only
`code-review` subagent against the unstaged diff at base
`a04668ae94b5c2f38e6c55ed789db245e8c71d16`. Review was not repeated.

## Outcome: findings (one Medium, test-only; no production-code defect)

* RV-1, Medium, `src/core/tests/test_resident_decisions.py` (`outcome_save_fault`
  with `committed=True` and the lost-commit test): on the JSON store, `_operation`
  restores the pre-image after the fault, so nothing stays committed and
  `_outcome_recorded` is not exercised; the test would pass on JSON without the
  reconciliation. Only SQLite and SQL Server reach the reconcile path. Suggested
  fix: assert whether the retry write occurred, per store.

Checked and sound per the reviewer: receiver called once before
`_record_outcome`; `_outcome_recorded` matches reservation, status and receipt;
recovery-failure notes block retry; known-committed errors are not retried; the
error is chained and not swallowed; `%r` neutralises newlines in the logged
receipt reference. Minor, not a finding: a non-transient `PermissionError` gets
one harmless second attempt.

## Routing

RV-1 is a test-strength correction, routed to correction cycle 1 of 5 in this
loop (no source defect). Per the one-pass rule there is no second Review; the
correction is verified by its diagnostics, recorded in the changes file.

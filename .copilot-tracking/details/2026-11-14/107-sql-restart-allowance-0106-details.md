<!-- markdownlint-disable-file -->
# Details: Issue #107 SQL restart and independent-connection proof

* Plan: [107-sql-restart-allowance-0106-plan.md](../../plans/2026-11-14/107-sql-restart-allowance-0106-plan.md)

## P1-P2 test design

* `RevocationAndSuspension`: continuity suspension on one store blocks `claim`, `execute`, `invoke` and late `complete` on other and fresh stores with zero provider calls and unchanged controlled records; revoked and suspended releases stay blocked after reopen with default and larger env; an old image cannot reactivate a revoked record; only `record_release` re-enables and never revives the old task.
* `Allowance`: consumed calls persist, stored ceilings do not rise with larger env, token reservation cannot be refilled, three concurrent connections spend a one-call allowance exactly once, and a revoke plus new record does not refund consumption.
* `MaterialMismatch`: constructed prompt, policy, permission, scope and serving-version variations on a separate worker deny dispatch, revoke the record, stay denied after restart, and quarantine a late completion without domain writes.

## P3

* `src/api/pyproject.toml`: add the module to the existing `disallow_untyped_calls = false` override used by typed tests that reuse untyped assistant fixtures.

<!-- markdownlint-disable-file -->
# Changes: Issue #107 SQL restart and independent-connection proof

* Plan: [107-sql-restart-allowance-0106-plan.md](../../plans/2026-11-14/107-sql-restart-allowance-0106-plan.md)
* Base: `f73a48f34` (parent `feat/demo-107-release-attest-race-2315`, PR #1594)

## Added

* `src/api/tests/test_assistant_restart_non_replenishment.py`: 11 tests over real file-backed SQLite with a fresh `SqlStore` and `Assistants` per worker or restart (suspension, revocation, finite call and token allowance, concurrent last-call race, prompt, policy, permission, scope and serving-version mismatch).

## Modified

* `src/api/pyproject.toml`: module added to the existing typed-test mypy override (`disallow_untyped_calls = false`).

## Not changed

* No `src/core` or `src/api/src` production file; no persistence gap found (see research and critique C1).

## Divergence

* The first test draft was written during research probing, before the critique; the critique then led to additions and tighter assertions (recorded in the critique file).

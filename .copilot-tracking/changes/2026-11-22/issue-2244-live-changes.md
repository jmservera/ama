# Changes: issue 2244

Status: implemented.

## Files

* src/core/src/zava_forward/core/mssqlstore.py: `_Conn._begin` retries the `could not take the write lock` failure of `BEGIN IMMEDIATE` with exponential backoff (1 s doubling, cap 30 s, up to 8 attempts) while `MssqlStore._initialize` runs; the flag is cleared afterwards, so runtime writes keep one 15 s attempt. Other errors and the final timeout propagate unchanged.
* src/core/tests/test_mssql_startup_lock.py (new): six regression tests with a fake driver.

Root cause: every start-up step (`_create_schema`, `_migrate`, `_migrate_queues`, `_create_indexes`, `_migrate_recommendations`) takes the global `sp_getapplock` write lock once with a 15 s timeout and no retry, so a long writer makes the constructor raise and the container exit 1.

## Validation

* `PYTHONPATH=src:tests python3 -m unittest test_mssql_startup_lock test_sqlstore test_restart_gate_sql_fences test_sqlqueues -q` in src/core: 51 tests OK.
* `python3 -m mypy` in src/core: 3 errors, all pre-existing (telemetry, device_provision), none in changed files; baseline without the change also 3.
* `ruff check` clean on both files; the new test is ruff-format clean.
* Tier: FULL applies (src change); rpi-checks --all not run here, the coordinator runs the gates. Hosted CI not observed (nothing pushed).

## Residual risk

Worst case start-up now waits about 3.5 min (8 x 15 s lock waits plus 91 s backoff). The Container Apps StartUp probe may still restart a replica before that; the probe window was not changed (no Bicep redeploy). A read-only schema check before taking the lock (issue suggestion) is routed as follow-up.

## Per-criterion table

The issue has no ticked or unticked acceptance checkboxes; criteria are taken from the goal and the issue's suggested fixes.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cause found in src | Proven | Root cause above; code references in the research note |
| Start-up retries with backoff | Proven (unit) | test_lock_timeout_is_retried_with_backoff_then_succeeds, test_backoff_is_capped |
| No exit on a transient lock | Proven (unit) | Retry succeeds after 3 timeouts; the constructor path enables retries (test_store_enables_retries_only_while_initialising) |
| Bounded, errors not masked | Proven (unit) | test_exhausted_retries_raise_the_lock_error, test_other_errors_are_not_retried, test_no_retry_after_start_up |
| Lock holder identified | Unproven | Log Analytics not readable by this client; not needed for the demo |
| Read-only schema check before lock | Unproven | Not implemented; routed follow-up |
| Live proof on ca-cutover-test-demo-api | Unproven | Needs holding the DB app lock and a new image rollout; no image was built or deployed, so the live app still runs the old code |

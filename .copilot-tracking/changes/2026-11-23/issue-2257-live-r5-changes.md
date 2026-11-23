# Issue 2257 r5 changes

Tier: FULL (src changed); only targeted tests, mypy and ruff were run here, the coordinator runs gates.

## Files

* `src/core/src/zava_forward/core/mssqlstore.py`: `driver_sqlstate`.
* `src/core/src/zava_forward/core/assistants.py`: `sqlstate=` in the overlay warning.
* `src/api/tests/test_map_sensors.py`: `test_an_other_overlay_failure_logs_only_the_sqlstate_code`.
* `docs/reference/research/issue-2257-live-r5-2026-11-23.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

* `tests.test_map_sensors`, `tests.test_error_logging`: 34 OK. `mypy` src/api clean; src/core 3 errors pre-existing (identical with changes stashed). `ruff check` clean.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Cause logged (lock tag plus SQLSTATE) | Proven in code and test; unproven live (not deployed) | test above |
| Map retries or recovers without reload | Proven live in r2 (0000055); retry button not deployed, unproven live | r2 note |
| Fresh-session failures gone | Unproven (18 of 18 passed, cannot show zero rate) | r2, r3 notes |
| Billing, DPO or Legal, assistive-technology testing | Not needed for the demo | owner decision 2026-11-18 |

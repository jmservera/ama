# Changes 2244 live r4 (2026-11-23)

Tier FULL (src/core change). `rpi-checks.py --all` not run; the coordinator runs gates. Local commit only, not pushed, not deployed.

## Edits

* `src/core/src/zava_forward/core/sqlstore.py`: `_seed` counts `cases` read-only and skips the write lock when populated.
* `src/core/tests/test_mssql_startup_lock.py`: `test_populated_cases_skip_the_seed_lock` (fails without the change, passes with it).
* Docs: `docs/reference/research/issue-2244-live-r4-2026-11-23.md`, README index, log.

## Validation

* `tests.test_mssql_startup_lock` 18 OK; with `tests.test_sqlstore` 39 OK. `ruff check` and `ruff format --isolated --line-length 100 --check` clean on changed files. `mypy`: 3 errors, all pre-existing (opentelemetry stubs, device_provision), none new.
* Full `src/core` discover: 4204 run, 35 failures and 22 errors, concentrated in `test_device_registry_azure`, `test_telemetry` and `test_discovery_assistant_demo` (Azure SDK and environment; none touch the seed or store). Baseline not re-run on a clean tree.
* Not run: full local gate, hosted CI. Live: read-only `az containerapp revision list`; nothing created.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| C1 retry with backoff | Proven (code, tests; live log run 2) | research r2, r3 |
| C2 skip lock when schema current | Proven live (run 2); seed step now also lock-free (code, test) | research r4 |
| C3 live start without crash-loop | Unproven: needs deployment (owner-gated) | research r3 |
| C4 long writer cannot take the demo down | Unproven live; fewer lock waits at start (code, test) | tests |
| C5 lock holder identified | Unproven: no log names the holder | research r2 |

# Changes 2244 live r2 (2026-11-23)

Tier FULL (src change in `src/core`, startup/SQL path). `rpi-checks.py --all` not run; the coordinator runs gates. Local commit only, not pushed, not deployed.

## Edits

* `src/core/src/zava_forward/core/lawstore.py`: `MssqlDb` sets `startup_retries = LOCK_RETRY_ATTEMPTS - 1` after opening its connection and gains `end_startup()`; `LawStore.__init__` calls it in a `finally` after `RuleCardStore` init and `seed()`. Fixes the law store start-up exiting with code 1 on a write-lock timeout (live evidence: replicas `7vs6x` 07:09:47Z and `pg6mj` 07:18:02Z on revision 0000055).
* `src/core/tests/test_mssql_startup_lock.py`: two tests (`LawStoreStartupRetryTests`).
* Docs: `docs/reference/research/issue-2244-live-r2-2026-11-23.md`, `docs/reference/README.md` index entry, `docs/reference/log.md` entry.

## Validation

* `test_mssql_startup_lock` 17 OK; `test_rulecards`, `test_rule_engine`, `test_source_monitor`, `test_regulatory_output_guard` 85 OK.
* `ruff check` clean on both changed files; `ruff format --isolated --line-length 100` clean on the test file. `lawstore.py` was already non-conformant to that format before this change (baseline check), left unchanged to avoid unrelated churn.
* `mypy` in `src/core`: 3 pre-existing errors (telemetry, device_provision), none in changed files.
* Not run: full `src/core` suite and the complete local gate (coordinator runs gates). No hosted CI (not pushed).
* Live: read-only Azure queries only (revision list, exec file hash, `/healthz`, Log Analytics). No deploy, no drill, nothing created, so nothing to delete.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| C1 retry with backoff on start-up lock timeout | Proven for the SQL store (live `retry 1 of 7`); law store gap fixed in code and unit tests, not deployed | research r2 |
| C2 skip the write lock when schema is current | Proven live (0000055 file md5 equals main). Law store and rule-card seeding still lock by design | research r2 |
| C3 live API starts without crash-loop | Not fully proven: two scale-out replicas on 0000055 exited with code 1 under contention and were restarted; fix not deployed | research r2 |
| C4 long concurrent writer cannot take the demo down | Unproven: probe budget (about 121 s) below worst-case wait (about 211 s); drill and probe change excluded by owner decision | research r2 |
| C5 lock holder identified | Unproven: Log Analytics readable but no line names the holder | research r2 |
| Live revision carries the law store fix | Not proven; deploy is a production change, owner-gated | n/a |

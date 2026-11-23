# Changes 2244 live (2026-11-23)

Tier FULL (src change). `rpi-checks.py --all` not run; the coordinator runs gates.

## Edits

* `src/core/src/zava_forward/core/mssqlstore.py`: read-only fast paths `_schema_current`, `_chat_memory_current`, `_indexes_current` and a `_migrate_queues` override. When every table, guard trigger, column and index already exists, start-up no longer queues for the `zavaforward_write` application lock. Anything missing, or a non-append-only ledger, takes the existing locked path unchanged.
* `src/core/tests/test_mssql_startup_lock.py`: six tests with a fake catalog (no lock when current; locked path when a table, trigger, index or ledger kind is off).

## Validation

* `test_mssql_startup_lock` 12 OK, `test_sqlstore` 21 OK, `test_sensor_analysis_mssql` skipped (no SQL). `ruff check` and `ruff format --isolated --line-length 100` clean on the changed files; `mypy` shows only the 3 pre-existing errors (telemetry, device_provision), none in changed files.
* A full `src/core` discover run finished after 26 min but its pass/fail summary line was cut off by trailing timing output and was not captured; treat the full suite as not evidenced. No hosted CI observed (not pushed).
* No live deployment of this change: the owner decision allows no production changes, so live revisions 0000054/0000026 do not carry it.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| C1 retry with backoff on start-up lock timeout | Proven (code, unit tests; live image identical) | #2273 `_Conn._begin`; live `mssqlstore.py` md5 07d00576e1d5e11e0efb1d86cfc1f92f equals main |
| C2 skip the write lock when schema is current | Proven in code and unit tests for schema, chat memory, indexes, queue columns. Partial: `_migrate` and `_migrate_recommendations` still lock (they repair data) | this change; not live |
| C3 live API starts without crash-loop | Proven only for the steady state: 0000054 Healthy, restartCount 0, `/healthz` 200 x3, no `write lock` in last 300 console lines. Start under contention unproven | research note |
| C4 long concurrent writer cannot take the demo down | Unproven. Worst case start wait (about 211 s) exceeds the StartUp probe (about 121 s); a stress drill is excluded and the probe is a production setting | research note |
| C5 lock holder identified | Unproven; Log Analytics not readable | issue text |
| Live 0000054/0000026 carry this change | Not proven, owner-gated (deploy is a production change) | n/a |

Docs added before the final review-done: docs/reference/research/issue-2244-live-2026-11-23.md, README index entry, log entry.

# Changes 2244 live r4 (2026-11-23)

Tier FULL (src change); `rpi-checks.py --all` not run. Local commit only, not pushed.

## Edits

* `src/core/src/zava_forward/core/lawstore.py`: `MssqlDb._schema_current()` read-only check; start-up skips the write lock when current.
* `src/core/tests/test_mssql_startup_lock.py`: regression tests.
* Docs: `docs/reference/research/issue-2244-live-r4-2026-11-23.md`, README index, log.

## Validation

`tests.test_mssql_startup_lock` 20 OK; law store tests 54 OK; ruff check and format clean; mypy: no lawstore finding (3 pre-existing errors elsewhere). Not run: full gate, hosted CI. Live: none, nothing to delete.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| C1 retry with backoff | Proven | r2, r3, tests |
| C2 skip lock when schema current | Proven (SQL store live run 2; law store unit tests); law store live unproven until deploy | research r4 |
| C3 live start without crash-loop | Unproven: owner-gated deploy | r3 |
| C4 long writer cannot down the demo | Unproven live | r3, tests |
| C5 lock holder identified | Unproven: no log names it | r2 |

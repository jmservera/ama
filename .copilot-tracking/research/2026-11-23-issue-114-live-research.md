# Research: issue 114 durable Azure SQL store with ledger audit (2026-11-23)

Research disposition: executed. Planning Readiness: Ready.

## Intake

* Issue #114 body (read via REST, GraphQL rate limited): all three acceptance criteria are already ticked. Closure waits for the owner tick and the #440 checkpoint (closure audit 11, 2026-11-19).
* There is no unticked criterion. Task becomes re-proof of the three criteria plus one code or test increment.
* Prior evidence: docs/reference/research/sql-ledger-live-2026-11-18.md, sql-ledger-live-r2-2026-11-18.md, ledger-verification/, issue-115-ledger-digest-live-2026-11-22.md.
* Open gaps named by those notes: deployed image lacked `verify_ledger_before_reliance`; live data holds one calendar year; native ledger verification after restore was permission blocked.

## Code survey

* `verify_ledger_before_reliance` lives only in `src/core/src/zava_forward/core/store.py`; no non-test caller outside the Store classes.
* Tests: `src/core/tests/test_recovery.py` (file and SQLite stores) and `src/core/tests/test_sqlstore.py` (multi-year, head mismatch, MssqlStore inheritance).

## Evidence plan

Live probes are recorded in the changes record and the research note under docs/reference/research/.

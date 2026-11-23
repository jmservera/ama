# Research 2244 live r4 (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

## Prior coverage

r1 to r3 covered the SQL store retry (C1), the SQL store read-only schema check (C2, live in run 2), the law store retry, and the StartUp probe window. Read: r2/r3 research and changes.

## New angle

`lawstore.MssqlDb.__init__` (law store, started by the API at every boot) takes `BEGIN IMMEDIATE` (the global `zavaforward_write` applock) unconditionally to run `IF OBJECT_ID IS NULL` DDL, even when all tables and guard triggers or ledger tables exist. C2 ("skip the write lock when the schema is already current") is therefore unmet for the law store: any long writer still delays every start up to the retry budget (211 s) and can exhaust it. Fix: a read-only current-schema check (tables, ledger kind or append-only triggers) before the locked path, mirroring `MssqlStore._schema_current`.

## Criteria status entering this run

* C1 retry: proven (code, tests). C2: proven for SQL store, unproven for law store (this run). C3, C4, C5: owner-gated or unprovable (r2, r3). Live Azure is not needed: the live demo database already holds the law tables; the change is proven by unit tests with a fake connection. Deploy is owner-gated.

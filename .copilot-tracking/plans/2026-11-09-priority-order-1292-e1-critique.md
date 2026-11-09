<!-- markdownlint-disable-file -->
# Critique: issue 1292 extension E1 plan (2026-11-09)

Executed once on the final candidate plan and details by the RPI agent (self-critique against the coordinator findings, the code and the constraints). Verdict: `revise`. Compatible findings applied directly below; no finding conflicts with a confirmed decision; no significant or divergent issue needs a user decision.

## Findings and dispositions

1. Zero count. Producer evidence (`_backfill_zero_ordinals` writes `len(keyed)` only when rows exist) shows no zero-count state, so rejecting 0 is not a loss of a documented semantic. Disposition: applied; the research and README text must state this evidence rather than assert it.
2. Absence detection. `_meta_value` cannot separate absent from present, so a direct `SELECT` is required; NULL is impossible (`value NOT NULL`). Disposition: applied in details Phase 1.
3. SQL Server dialect risk. Some edge tests build legacy tables with SQLite-only DDL (for example `TEXT PRIMARY KEY`) and `FlakyDb` injects `sqlite3.OperationalError`. Running the classes on SQL Server may fail for fixture dialect reasons, not production defects. Disposition: use the existing `legacy_ddl()` helper where raw DDL appears, or skip a single named test with a recorded reason only when the test is SQLite-structural by construction. Wholesale class skips are not allowed; every skip is listed in the changes record. A production failure found on SQL Server is a stop condition, not a waiver.
4. Lock timeout duration. The real `BEGIN` waits 15 s. Patching `mssqlstore.BEGIN` to a shorter `@LockTimeout` keeps the real driver, server and lock; it is not a fake. Disposition: applied; the test asserts the real timeout error and `@@TRANCOUNT` from the server.
5. UI latch scope. `checkHistory` is panel-closure state, so a remount (workspace reload) clears it, which is the intended recovery. `pending` must also stop double-click repeats of the POST. Disposition: applied.
6. Test honesty. The HTTP test must reach the shipped `app.js` `api()` through a response that came from the real server, not a hand-written body. Disposition: applied (real `ThreadingHTTPServer` then Node with the captured status and JSON).
7. Scope control. Do not alter the already-reviewed `act()` path, server handler, or ordinal logic. Disposition: applied.
8. Assertion integrity. New tests only add; no existing assertion changes; the `MssqlPriorityOrder` refactor to a shared mixin must be behaviour-identical. Disposition: applied; the class count and test names are compared before and after.

No further critique pass is run for this task.

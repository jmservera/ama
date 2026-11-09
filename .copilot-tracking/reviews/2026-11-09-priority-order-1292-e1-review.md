<!-- markdownlint-disable-file -->
# Review: issue 1292 extension E1 (2026-11-09)

Review executed once by the authoring RPI agent after implementation (self review; independent exact-head review remains mandatory and is not claimed). Outcome: `partial`, not conformant: the selected SQL Server proof is missing. Plan: [plan](../plans/2026-11-09-priority-order-1292-e1-plan.md). Changes: [changes](../changes/2026-11-09-priority-order-1292-e1-changes.md).

## Assessed

* F1 High, malformed `rec_order_legacy`: code reads present vs absent, requires an object with a positive integer `rows`, else whole range suspect. SQLite matrix covers invalid JSON, empty text, `{}`, `[]`, `null`, bare number, missing, negative, zero, string, bool and float counts with positive legacy ordinals: ordinals preserved, latest unresolved, `order_confirmed`/`actionable`/`relied_on` false, accept and edit refused. Verified by a local run (142 tests, OK).
* F2 Medium, committed creation repeat: `ask` is guarded by `pending` and the `checkHistory` latch, `mutationNeedsHistory` applied; no creation control after a committed, uncertain or transport outcome; an ordinary refusal stays retryable. Test uses a real HTTP 409 `committed` response from the shipped server. Verified (31 tests, OK).
* UI against the fetched web-interface-guidelines (this change adds one `role="status"` text note, no new controls, no styling): no rule violated; Fluent, text states and manual routes preserved.
* C2/C4 real SQL edge, lock-timeout `BEGIN` on a second connection, `@@TRANCOUNT`: tests are written and selected but NOT executed.

## Findings

* R1 High (blocks independent publication): the selected SQL Server tests did not run. The only prior full run (`e1-sql-run2`) failed; `e1-sql-run3` was interrupted by the coordinator; the single admission attempt was refused by another lane's lock holder. No SQL skip is a pass.
* R2 Medium: `MssqlLegacyEdges.test_large_legacy_backfill_is_linear_and_survives_concurrent_openers` is skipped with a recorded reason (concurrent first opens race on `CREATE INDEX ix_recs_seq`). That is an unproven claim of a pre-existing SQL Server bootstrap defect and a weakened SQL coverage point; the critique treats a SQL production failure as a stop condition. Route: separate follow-up with a SQL reproduction, not waived.
* R3 Low: `ZF_RESIDENT_MSSQL` classes show as skipped (65) locally; this is not SQL evidence.

## Routing

Resume condition: when `/tmp/ama-rpi-heavy.lock` is free, run once with `flock -n` into a new `e1-sql-admission-<unique>` directory from a clean committed head, then rerun review for the SQL outcome via the coordinator's independent reviewer. No Implement transition in this task.

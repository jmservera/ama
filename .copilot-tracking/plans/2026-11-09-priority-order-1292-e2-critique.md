<!-- markdownlint-disable-file -->
# Critique: issue 1292 extension E2 (2026-11-09)

Executed once on the final candidate plan. Verdict: `proceed with revisions`; compatible findings applied directly; no confirmed user decision conflicted.

* C1 Scope: the defect is pre-existing bootstrap code, so a reader could call it unrelated. Basis for coupling: the SQL reproduction shows the concurrent-open guarantee tested by this issue's backfill fails on this index step, and the owner conditionally authorized exactly this case. Revision applied: the fix touches only `_create_indexes`; no refactor of `_create_schema`, `_indexes` or the other bootstrap steps.
* C2 Transaction semantics: DDL inside `BEGIN TRAN` holds the applock for the index build; on a large table this extends the write-lock hold. Accepted: index creation runs once, and the existing 15 s `@LockTimeout` makes a waiter fail closed rather than hang. The large-backfill test asserts the 20 s bound.
* C3 Order: `_migrate_chat_memory` commits its own transaction, so the index transaction must start after it, not nest in it. Applied in the details.
* C4 Weakening risk: removing the skip must not change the test body or thresholds. Applied; the test is not edited.
* C5 Evidence: a pass on SQLite is not SQL evidence. The plan requires a new owned SQL Server run on the final head.

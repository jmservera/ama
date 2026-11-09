<!-- markdownlint-disable-file -->
# Review: issue 1292 extension E2 and E1 SQL validation (2026-11-09)

Review executed once by the authoring RPI agent after implementation (self review; independent exact-head review remains mandatory and is not claimed). Outcome: `conformant for the selected owned-SQL and local tier`; whole-issue and live criteria remain unproven (below). Plan: [plan](../plans/2026-11-09-priority-order-1292-e2-plan.md). Changes: [changes](../changes/2026-11-09-priority-order-1292-e2-changes.md). The original E1 review ([E1 review](2026-11-09-priority-order-1292-e1-review.md)) and the C2/C4 and adverse reviews are preserved unchanged; this review supersedes none of them.

## Assessed against the E1 open findings

* R1 High (SQL proof missing): resolved for the selected tier. Actual owned SQL Server 2022 runs: `test_priority_order` 142 tests OK with zero skips on `a20472734` (includes C0 absent versus malformed `rec_order_legacy` and legitimate zero semantics, C2/C4 edge classes, real `BEGIN` lock timeout with a second connection and `@@TRANCOUNT`, failed-`BEGIN` recovery); `MssqlResidentControls` 91 OK on the byte-identical `mssqlstore.py`. SQLite-only and fake-driver tests were not counted as SQL proof.
* R2 Medium (skipped concurrent-open test): reproduced on SQL (`ix_recs_seq` already exists), root cause in `_create_indexes` (non-atomic check-then-create outside the write lock), fixed, skip removed, test passes on SQL. A latent test defect (`_Cursor` not iterable) surfaced and was fixed without weakening any assertion.
* R3 Low (opt-in skips are not evidence): unchanged; the 158 and 365 opt-in skips in local runs are not SQL evidence.

## Remaining risks and unproven criteria

* Hosted CI on the exact head, independent exact-head review and human approval: not performed.
* Live and whole-issue criteria: nothing here was run against Azure SQL or a deployed environment, so any acceptance criterion that requires the live UI path with a real SQL reload in a deployed system, or the whole-issue closure, is unproven. Use `Refs #1292`, not `Closes`.
* `_create_indexes` now holds the write lock while indexes build; large production tables lengthen that hold (bounded by the 15 s lock timeout, waiters fail closed). Not measured on Azure SQL.
* Resident SQL phase was not re-run on `a20472734`; identity of `mssqlstore.py` is the basis.

## Routing

No Implement transition inside this task. Next: coordinator independent exact-head review of `a20472734` plus records commit, then hosted CI. Budget: E2 consumed (second of five), three remain.

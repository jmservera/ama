---
title: Issue 1292 priority recommendation creation order plan critique
description: Single independent critique of the final plan and its direct dispositions
ms.date: 2026-11-08
---

## Execution

Critique executed once (independent read-only rubber-duck agent) on 2026-11-08 against the plan and details committed in the first RPI commit. Verdict: Revise. It is not repeated for this task. No finding conflicts with a confirmed user decision, so all compatible findings were applied directly; no user decision is required.

## Findings and dispositions

* C-1 Blocking, applied. A local insert is cached before the post-commit `_sync`, so a concurrent older commit appended afterwards would sort after it despite the query order. Disposition: keep an id-to-ordinal map and stably sort the whole cached list by ordinal after every recommendation load and after save; add an interleaved-writer regression (details, SQL cache reconciliation and case 6).
* C-2 Blocking, applied. The `recommendations` table is created in the `INDEXES` script, after migration. Disposition: run `_migrate_recommendations` after `_create_indexes`, create the new index from the migration through a dialect hook, and add a fresh-initialisation case (case 7).
* C-3 Blocking, applied. Backfill changed neither `seq` nor `rowversion`, so a running reader could keep a stale order. Disposition: backfilled rows and `meta.seq` take one new `seq`; add a long-lived reader case. Pre-fix readers stay out of scope and the rolling-deployment limit stays documented.
* C-4 Non-blocking, applied. The legacy MSSQL fixture cannot simply drop the new column, and the deployment may use ledger tables. Disposition: build the legacy fixture by dropping and recreating the table with the pre-fix DDL; the ledger migration path already exists in `_add_column_default`; record ledger execution as unproven unless the native database is ledger-enabled.
* C-5 Blocking as stated, accepted as a completion gate. Native SQL Server evidence and the PR are acceptance conditions. The coordinator instruction for this task defers native SQL and publication, so they are carried as explicit PENDING completion gates in the plan, issue record and handoff, never as accepted residual risk or a claimed pass.

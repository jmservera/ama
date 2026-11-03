---
title: Issue 114 round 1 research
ms.date: 2026-11-03
---

Disposition: executed (repository inspection, merged PR review).

## Already delivered (do not redo)

* PR #262: per-year ledger digests and verification, loadcheck harness, recovery and deletion register (DH-005), local tests.
* PR #403: loadcheck evidence contract hardened (invalid workloads and worker failures cannot report success).
* `MssqlStore` subclasses `SqlStore`; year digest code is store-agnostic (`Store.verify_ledger_by_year`).

## Acceptance criteria status

* Per-year audit and digest verification: proven locally on SQLite by `src/core/tests/test_recovery.py`; not run against Azure SQL. Unmet for reliance.
* Measured load, latency and cost: only local SQLite numbers exist; Azure run and cost need Azure access. Unmet.
* Backup, restore and deletion re-application on Azure SQL: only SQLite drill exists. Unmet.

## Gap found

`ledger.verify_years` raised on a malformed digest and `read_year_digests` raised on a corrupt file; a digest dir with every file removed reported intact with no hint that nothing was sealed.

Planning Readiness: Ready. Slice: fail-closed digest handling, no Azure dependency.

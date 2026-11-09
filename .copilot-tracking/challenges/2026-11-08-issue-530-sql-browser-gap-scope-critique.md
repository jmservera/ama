---
title: Issue 530 actual SQL and employee browser gap scope critique
ms.date: 2026-11-08
---

* Execution: one independent read-only rubber-duck pass (agent `critique-gapscope`) before any code. Verdict: Proceed with changes. Not repeated.

## Findings and dispositions

* F1 Blocking, applied: the inherited `ChatDemoMeterOnSqlStore.kinds()` iterates a cursor, and the `MssqlStore` cursor is not iterable (`test_continuity.py:349`, `mssqlstore.py:120`). The MSSQL meter class overrides `kinds()` and the order-dependent seed test using `fetchall()` and order-independent comparison.
* F2 Blocking, applied: the required-SQL-tests proof parses each exact verbose header and its bounded result region (same line or the following status line before the next header), rejects duplicates, failures and missing headers, and resolves required names through the class MRO (inherited methods count). Regressions cover interleaving, duplicate, failure and missing cases.
* F3 Non-blocking, applied: the chat browser command and results copy run inside the existing `try/finally` in `Runner.browser()` so the `.venv` marker cleanup still happens on failure.

## Verified by critique

* Roster reads are live SQL on `MssqlStore`; fixture staff seeding is supported.
* Import modules rather than `TestCase` classes to avoid duplicate discovery.
* Skip reason `needs a SQL Server (ZF_TEST_MSSQL=1)` is allowed; browser scratch, safety path, timeout and copied-results approach match existing mechanics; command sorting keeps intra-group order.
* No scope violation found (no workflow, production or schema change).

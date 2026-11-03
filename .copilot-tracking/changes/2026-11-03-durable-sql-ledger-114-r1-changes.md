---
title: Issue 114 round 1 changes
ms.date: 2026-11-03
---

* Year digest verification fails closed on bad digest files; report lists sealed years.
* Validation run: `tests.test_recovery` (14 OK), orchestrator `tests.test_digest_blob` (23 OK), ruff check clean, mypy (cache /tmp/mypy-114) clean on ledger module.
* Not run: complete gate, full suites, Azure SQL, SQL Server container tests, benchmarks. `ruff format --check` flags ledger.py, as it did before this change.
* Unmet: all three issue criteria remain unmet (no Azure evidence). Use Refs #114.

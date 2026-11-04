---
title: Issue 190 retained-store scenario details
ms.date: 2026-11-04
---

* Test file: `src/core/tests/test_retrofit_scenarios_retained_store.py` (SQLite only; skipped on SQL Server).
* Setup: fixture store, constructed `cases` rows for the scenario homes, one control per scenario sensor, a 28-day exercise policy.
* Assertions: every row accepted; retained signal equals the pure signal; sufficiency SUFFICIENT; priority effect NONE; no review task candidate; exercise label kept; declined consent gives DECLINED; partial or unmapped data is not SUFFICIENT.

---
title: Issue 74 round 1 changes
ms.date: 2026-11-03
---

## Added

* src/core/src/zava_forward/core/home_case.py
* src/core/tests/test_home_case.py

## Modified

* src/core/src/zava_forward/core/store.py (two delegating methods)
* src/core/src/zava_forward/core/sqlstore.py (`schemes` in DOCS)
* src/core/README.md (Versioned home case section)

## Validation run

* test_home_case (7), test_buildings (9), test_seed_merge (21), test_change_provenance (13): OK.
* ruff check and format check on new files: clean. mypy on new files: clean.

## Not run

Complete local gate, full suites, API and browser checks, MSSQL store, benchmarks. SQL touched, so the coordinator runs the gate.

## Divergences

None. A first test draft used the wrong fixture case IDs and the register was not persisted in SQL; both fixed.

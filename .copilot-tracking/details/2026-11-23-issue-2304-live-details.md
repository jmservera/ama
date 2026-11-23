---
title: Issue 2304 plan details
ms.date: 2026-11-23
---

# Details

## Phase 2

`ForecastReads(db, mssql, budget)` wraps the read connection. `execute` serves the schedule slot, task by id (existence, state and attempts, body) and the adoption page from bulk reads; short-circuits per-home sensor reads and consent index reads for homes absent from a distinct-home read; memoises other SELECTs; passes everything else through. `check()` raises `ForecastTimeout` after the 10 s budget. `Assistants.forecast` uses it and checks the budget per case. `server.py` maps `ForecastTimeout` to 503.

## Phase 3

`ForecastStatements` in `src/api/tests/test_assistants.py`: statement count equal for the seed set and the seed set plus 40 open cases with larger forecast totals; a spent budget raises `ForecastTimeout`. Existing forecast tests, ruff, mypy.

## Phase 4

Deployment of the demo API app from the branch if the existing build path is usable within the owner's authority; otherwise record why the live re-check is unproven.

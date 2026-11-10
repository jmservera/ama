---
title: Issue 1384 main adoption changes
description: Changes record for the main adoption, prospective until implementation finishes
ms.date: 2026-11-10
ms.topic: reference
---

## Status

* Completed: merge staged and validated; see Actual outcome below. Plan: `.copilot-tracking/details/2026-11-10-workspace-oracles-main-adoption-1384-1110-details.md`.
* Base: original frozen candidate `3f1fa4810a79b8689aaa8d8e167aa6470b262420` plus the tracking-only commit that holds this record; adopting `origin/main` `111847191d1fde5e8ea18c30c999e99f33721aff`.

## Actual outcome (completed before implement-done)

* Ran `git merge --no-ff --no-commit origin/main`: one conflict, `src/api/checks/workspace_scripts_browser_check.py`, resolved by keeping both sides (imports `partial` and `monotonic`; constants `TERMINAL`, `REVISIT`, `ROUTE_DELIVERY_DEADLINE_S`). Staged, not yet committed (235 files staged from main plus the candidate).
* No oracle, loader, delay or retry-policy change. `workbench_browser_check.py` sha256 equals main's (`9a975543...`), so no manifest recipe update.
* Evidence dir: `ROOT/checks-1384-main-adoption-1110/` (00 non-heavy; 01/02 units; 10 whole browser runs; 11, 12 chat reruns).
* Results: ruff check pass; ruff format 139 formatted; mypy 220 files pass; node --check pass; `tests.test_workspace_scripts` 10 OK (includes the Node-VM loader test); `tests.test_workspace_paging` 12 OK only with `tests` on PYTHONPATH.
* Whole `workspace_scripts_browser_check`: exit 0. Whole `employee_workspace_browser_check`: exit 0. Lock holder before: none; flock -n, one execution each.
* `employee_chat_browser_check`: exit 1 in `10-*` and `11-*` with ModuleNotFoundError at import (`regulatory_fixture`, then `test_regulatory_chat_api`), before any check ran: my PYTHONPATH omitted test helper dirs. Third execution `12-*` with corrected PYTHONPATH (`.:tests:../core/tests:../agents/tests`): exit 0. Disclosed deviation: 3 executions of this check, 2 import-only failures preserved; scripts and workspace checks ran once.
* Original baseline `sign_out` empty failure stays UNKNOWN; earlier original reds are not called green.

## Registered touched paths (declared before implement-start)

* Hand-resolved: `src/api/checks/workspace_scripts_browser_check.py` (two additive merge hunks only).
* Taken unchanged from main by the ordinary merge (not hand edited): the 7-commit main delta, including `src/api/checks/workbench_browser_check.py`, `src/api/src/zava_forward/api/web/app.js`, other checkers and tests, and `.copilot-tracking` files of other issues.
* Not touched: `workbench-manifest.json`, the scenario manifest (its `recipe` hash was already updated by main for the same `workbench_browser_check.py`), production loader, delays, auth, API, policy.

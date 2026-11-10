---
title: Issue 1384 main adoption changes
description: Changes record for the main adoption, prospective until implementation finishes
ms.date: 2026-11-10
ms.topic: reference
---

## Status

* Prospective: no source edit or merge has been made yet. Plan: `.copilot-tracking/details/2026-11-10-workspace-oracles-main-adoption-1384-1110-details.md`.
* Base: original frozen candidate `3f1fa4810a79b8689aaa8d8e167aa6470b262420` plus the tracking-only commit that holds this record; adopting `origin/main` `111847191d1fde5e8ea18c30c999e99f33721aff`.

## Registered touched paths (declared before implement-start)

* Hand-resolved: `src/api/checks/workspace_scripts_browser_check.py` (two additive merge hunks only).
* Taken unchanged from main by the ordinary merge (not hand edited): the 7-commit main delta, including `src/api/checks/workbench_browser_check.py`, `src/api/src/zava_forward/api/web/app.js`, other checkers and tests, and `.copilot-tracking` files of other issues.
* Not touched: `workbench-manifest.json`, the scenario manifest (its `recipe` hash was already updated by main for the same `workbench_browser_check.py`), production loader, delays, auth, API, policy.

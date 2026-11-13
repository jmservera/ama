---
title: Issue 74 criterion 2 evidence-only changes
description: Record of the bounded local fixture check and evidence files for shared-building versus per-home separation; no source or test changes
ms.date: 2026-11-13
---

## Changes

Only the research, plan, critique, changes and review Markdown under `.copilot-tracking/`. No source, test, dependency or infrastructure edit.

## Check actually run

* Origin: this worktree, base 1f870ec92. System-wide pip distributions resolve to another checkout (`/home/azureuser/source/ama`) and were not used.
* `python3 -m venv /tmp/c2venv.G5vg/v` then `pip install --no-deps -e src/core -e src/agents -e src/api` (exit 0). Import path verified to the worktree `src/core`. No PYTHONPATH, no uv.
* From `src/core/tests` with `ZF_DATA=/tmp/c2venv.G5vg/zf.json` (temporary, private data untouched): `python -m unittest test_home_case.HomeCaseTests.test_shared_building_id_never_transfers_evidence_between_homes test_buildings.BuildingTests.test_shared_view_keeps_home_evidence_allocations_and_approvals_home test_buildings.BuildingTests.test_cost_visibility_and_role_denial`. Result: Ran 3 tests, OK (the displayed exit was from `tail`; unittest reported OK).
* Order deviation: ran before the critique (see critique file).

## Limitations

Core-level only. No API HTTP, browser, SQL server, Docker, cloud or full gate. Dependencies and holds rows were empty in the fixture. Not criterion 2 acceptance; criterion not ticked.

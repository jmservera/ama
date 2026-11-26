---
title: Issue 1288 live r15 changes
description: Changes record with the per-criterion proven or unproven table
ms.date: 2026-11-26
---

## Changes

* src/core/src/zava_forward/core/assistants.py: new `Assistants.open_suspension` honours `continuity.demo_owner_override()`; `suspended()` and two task-view sites use it. Real defect: live proposals for the five demo homes showed SUS-1 hold despite the owner override.
* src/api/tests/test_continuity.py: new test, fails on base, passes with the change.
* docs/reference/research/issue-1288-live-r15-quality-sensor-evidence-2026-11-26.md, docs/reference/README.md, docs/reference/log.md.
* Azure: finite allowance set (revision 0000080) and removed (0000081, Healthy). No resource created; no role, network, key or budget change.

## Tier

FULL tier applies (src changed). Local checks run: 274 targeted tests OK (83 skipped: SQL Server and browser prerequisites), ruff check, src/api mypy clean; src/core mypy 3 pre-existing errors; assistants.py ruff-format drift pre-exists. `rpi-checks.py --all` not run (coordinator gate). Commit stays local.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 read model | Ticked (carried) | r12 live and earlier |
| 2 UI context | Ticked (carried) | r12 live and earlier |
| 3 snapshot consumes identical IDs | Proven locally, unproven live | mock provider tests; no live model request |
| 4 proactive deduplicated bounded flag | Unproven live | release in force, allowance set; blocked by assistants SUS-1 hold (defect fixed in source, not deployed: registry private); tokens 0 |
| 5 employee sees finding and attribution | Proven locally, unproven live | no live output |
| 6 explicit unavailable states | Proven locally and seen live | disabled/suspended with manual route |
| 7 focused tests | Proven as local engineering evidence | 274 tests, fixtures |
| 8 live walkthrough | Unproven | model leg not reached |
| 9 existing controls intact | Ticked (carried) | unchanged; the override stays demo-only and keeps records open |

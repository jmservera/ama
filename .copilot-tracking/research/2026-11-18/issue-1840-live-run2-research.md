---
title: "Research: issue 1840 incomplete old-image completion (live demo run 2)"
description: Evidence for classifying incomplete mismatch/reinvoke completion as INSUFFICIENT
ms.date: 2026-11-18
---

Task: issue-1840-live. Mode: automatic. Refs #1840. Opened before substantive search.

## Opening

Goal: `completed()` in `src/api/checks/old_image_sql_probe.py` must not let the mismatch audit return `VIOLATED` without observed supported completion. Owner decisions of 2026-11-18 apply (synthetic demo, desktop only, live Azure authorised in `ama`, no drills, no production change). The defect sits in an offline fixture-driven judge, so no Azure resource can prove an acceptance criterion.

## Findings

* An earlier run on main (`d2f974c45`) recorded a blocker: pin `510fd90f` was in no reachable ref. That run is preserved on main (`59e5c3c60`).
* The pin exists in the local archive clone `[archive clone]`. `git fetch <clone> 510fd90f...` succeeded, and this branch was re-created from the pin as the issue's child-branch instruction requires (3 commits ahead of main's merge base `1c9ac230b`).
* `completed()` (lines 482-491) only requires non-empty `executed` and `reinvoked` lists and no `error` key. `check_step` already holds the fixed-protocol checks (single record, requested task id, `before` pending, boolean `result`, text `after`, matching reinvoke capability/case and text `state`, no error), but only feeds `weak`.
* `judge` line 682: `mismatch_done = completed(...) and mutated_read` gates the audit of the mismatch release row.

## Planning Readiness

Ready. Disposition `executed`. Fix: factor the execution/reinvoke checks out of `check_step` and make `completed()` reuse them with the requested task id.

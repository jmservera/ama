---
title: "Details: #146 RAI window reconcile and disabled-task owner status"
ms.date: 2026-11-14
task_slug: demo-146-rai-window-reconcile-0003
---

## Phase 1

`reconcile_events(..., prior_event_ids=None)`: validate prior tokens and size (blocked otherwise), seed `seen`, return `count` (distinct total), `new`, `duplicates`, `checkpoint` (sorted ids). Behaviour without a prior is unchanged.

## Phase 2

`disabled_task_status(task)` returns `task`, `state`, `owner_role`, `owner_individual`, `owner_gap`, `reason`; reads only registry fields; withholds sensitive or oversized reasons. `assistants.registry` adds it as `status` on disabled registered tasks.

## Phase 3

Tests for checkpoint replay, bad checkpoint, status owner/gap, withheld reason; API assertion on the disabled chat task.

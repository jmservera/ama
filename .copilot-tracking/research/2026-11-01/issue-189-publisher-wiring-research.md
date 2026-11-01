---
title: Issue 189 publisher wiring research
ms.date: 2026-11-01
task_id: issue-189-publisher-wiring
---

## Disposition

Executed 2026-11-01. Planning Readiness: Ready.

## Evidence

* PR #637 (merged) delivered `synthetic/run_plan.py` (estimate, B1 headroom, owner, limit, alert reference, `RunController`) with tests. No other open PR references #189.
* Its review lists the remaining low finding: `RunController` is not wired into `HubPublisher` in `src/api/src/zava_forward/api/iot_stream.py`, so limits bind only callers that use it.
* `HubPublisher.run` already accepts `pacer` and `budget`; `RunController.start(estimate_path)` refuses without a matching recorded estimate.
* Live Azure budget alert is owned by #146 and cannot be verified offline.

## Remaining slice

Add `HubPublisher.run_controlled` so a publish run requires a recorded estimate, uses the plan budget and controller pacer, and always stops the controller afterwards. Tests in `src/api/tests`.

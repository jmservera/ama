---
title: Issue 189 infra alignment research
ms.date: 2026-11-03
task_id: issue-189-infra-alignment
---

## Research disposition

Reused. Prior merged work: PR 637 (estimate, B1 quota headroom, owner, time limit, alert reference, start/stop/scale-down controller) and PR 707 (publisher wiring, `run_controlled`). Evidence: `.copilot-tracking/*/2026-11-01/issue-189-*`.

## Findings

* Criterion 1 (estimate recorded before any run) and criterion 2 (B1 quota headroom) are implemented and unit tested in `src/core`; `RunController.start` refuses without a recorded, matching estimate.
* Criterion 3: owner, time limit and alert reference are required and enforced. The alert is only a recorded reference and threshold.
* `infra/modules/iothub.bicep` already defines a hub-scoped budget with 80 percent actual and 100 percent forecast notifications; `infra/main.bicep` pins B1, one unit and a 60 allocation. Nothing tied the plan constants to those definitions, so drift would go unnoticed.
* Live budget notification delivery is owned by #146 and #140 deployment; it is not verifiable offline.

## Planning Readiness

Ready. Smallest slice: static drift tests, no infra or security change (focused tier).

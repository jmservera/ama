---
title: Issue 189 infra alignment details
ms.date: 2026-11-03
task_id: issue-189-infra-alignment
---

## Phase 1 details

* File: `src/core/tests/test_run_plan.py`. Parse `param <name> <type> = <default>` from `infra/main.bicep` and the `actual80` block from `infra/modules/iothub.bicep` with regular expressions.
* No new dependency; `INFRA` resolved as `parents[3] / "infra"` like `test_monitoring_coverage.py`.

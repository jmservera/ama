---
title: Issue 111 live demo evidence, 2026-11-19
description: Per-criterion proof status for issue 111 deterministic sensor analysis in the synthetic desktop demo
ms.date: 2026-11-19
---

Refs #111. Scope: synthetic demo, desktop only. No Azure resource was touched or created, because no criterion needs one.

## Criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| Outputs are reproducible from retained readings | Proven (already ticked) | `src/core` `test_sensor_analysis`: 46 tests, OK (11 skipped, 1 expected failure), run 2026-11-19 |
| Thresholds are sourced or labelled exercise values | Proven (already ticked) | `AnalysisPolicy.validate` rejects an unlabelled threshold (`THRESHOLD_LABEL_REQUIRED`); same test run |
| R1 to R3 complete before a derived measure is used beyond an exercise rule | Unproven | See below |

## Why the third criterion cannot be proven for the demo

* [Plan R2](./iot-sensor-analytics-research-plan.md) needs sign-off by a competent building-physics reviewer and Asset. R3 needs agreed miss and false-alert limits. Both are named human approvals; an agent cannot supply them.
* The owner waivers of 2026-11-18 cover billing reconciliation, DPO/Legal approval and person-run assistive-technology testing. They do not waive R2 or R3.
* The code already enforces the safe side of the criterion: a `SOURCED:` threshold raises `RESEARCH_GATE_REQUIRED` without a `ResearchGate`, and a review task needs a named `RuleApproval`. In the demo every measure stays an exercise rule, so the gate is never crossed.
* No source change was made; adding code that fabricated reviewer sign-off would breach the approval boundary.

The criterion stays unticked.

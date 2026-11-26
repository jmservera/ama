---
title: Issue 146 research, live2 pass (2026-11-25)
---

Refs #146. Reuse of [live8 note](../../../docs/reference/research/issue-146-live8-monitoring-2026-11-25.md) as the live baseline (Research disposition: reused, Planning Readiness: Ready).

## Finding

* `infra/scripts/monitoring_live_inventory.py` marks the `job_failure` class `enabled` when any one `alert-job-*-failed` rule is enabled.
* Live state (live8): `job-live-receiver` had 8 Failed of 2742 executions and no rule, while the class could read `enabled` as soon as one other job rule was enabled. Coverage is overstated.
* Source alert names are `alert-${jobName}-failed` (operationalMonitoring.bicep, live-receiver-job.bicep).

## Angle

Add an optional job inventory (`az containerapp job list` names) so the classifier reports `partial` and names jobs with no enabled failure rule. Test-only plus tool change in `infra/scripts`; no `src/` change, focused tier.

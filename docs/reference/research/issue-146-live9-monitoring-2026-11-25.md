---
title: Issue 146 monitoring criteria, live9 classifier pass (2026-11-25)
description: Per-job failure-alert coverage in the live inventory classifier, run against the live demo resource group, with a proven or unproven result per criterion
ms.date: 2026-11-25
ms.topic: reference
---

Refs #146. Builds on the [live8 note](./issue-146-live8-monitoring-2026-11-25.md). Read-only Azure CLI calls on resource group `ama` (names and enabled flags only); no resource created, no credential read.

## Change

`infra/scripts/monitoring_live_inventory.py` took a class as `enabled` when any one rule matched, so one enabled job rule hid jobs without a rule. The new `--jobs` input (`az containerapp job list`) adds `uncovered_jobs` and reports `partial` in that case.

## Live result

Output of the classifier over the live inventory (2026-11-25): coverage `partial`; `job_failure` disabled, `poison_queue` disabled, `ledger_digest` enabled, `iot_ingestion` disabled. Jobs with no enabled failure rule: `job-184-bodyscan`, `job-cutover-test-demo-audit`, `job-cutover-test-demo-load`, `job-cutover-test-demo-orch`, `job-live-receiver`, `job-live-simulator`. This agrees with live8: the job rules are installed but disabled and the receiver has none.

## Criteria

| Criterion | Result | Reason |
| --- | --- | --- |
| Alerts cover job failures, poison queue, ledger digest, IoT ingestion | Unproven | Only ledger digest is enabled; the other three classes are disabled or missing. Enabling needs owner approval |
| Workbook shows availability, errors, latency and cost against budget | Unproven | Deployed workbook is behind source (live8); redeploy is a deployment action not run here |
| Each alert has a runbook entry with an owner | Unproven | Source tests pass, but no person is named (human decision) |
| Dashboard shows metered AI usage beside the Azure cost record with variance | Unproven | Proven for the demo in live8; not re-run here |

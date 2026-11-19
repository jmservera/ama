---
title: Issue 146 live5 research
ms.date: 2026-11-19
---

Refs #146. Synthetic demo, desktop only, resource group `ama`. Read-only.

* Live inventory (az, existing login): 4 metric alerts, 4 scheduled-query alerts, 0 workbooks; identical to [live4](../../docs/reference/research/issue-146-live4-monitoring-2026-11-19.md).
* `infra/modules/operationalMonitoring.bicep` still uses `timeAggregation: 'Maximum'` for the job-failure candidate; the fix and any workbook install are Bicep and redeploy changes.
* Runbook owners are proposed roles; naming people is a human decision.
* Planning readiness: Ready to conclude no buildable criterion.

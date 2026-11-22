# Issue 146 research (2026-11-22): API 5xx, receiver job failures, SQL DTU

Disposition: executed. Planning Readiness: Ready. Scope: repo Bicep and docs only; live use was read-only (resource group ama, demo, desktop).

## Findings

* Live inventory (az monitor, read-only, 2026-11-22 20:20 UTC): API 5xx and API restart metric alerts are enabled for both the `cutover-test` and `cutover-test-demo` prefixes; SQL CPU (`cpu_percent` >85) is the only SQL alert; job-failure and IoT candidates are installed but disabled for `demo-audit`, `demo-orch` and `demo-load`; poison and AI-limit rules are disabled; a workbook now exists (it was absent on 2026-11-19).
* Gap 1, SQL DTU: the database is a DTU tier (Standard, capacity 100, S3) and exposes `dtu_consumption_percent`, `dtu_limit`, `dtu_used`. No alert watches DTU. Hourly maxima over the last 6 hours were 82 to 92 percent while hourly averages were 15.7 to 20.9 percent, so an Average over 15 minutes is the quiet, non-flapping choice.
* Gap 2, receiver job: `job-live-receiver` (template `infra/live-receiver-job.bicep`, a separate deployment) has 61 Failed, 43 Succeeded, 2 Stopped, 1 Running executions in history and no failure alert, because the monitoring module only receives jobs declared in `main.bicep`. The `Executions` metric with a `state` split reported 0 Failed in the last 3 hourly buckets.
* API 5xx: `alert-${applicationPrefix}-api-5xx` exists in `infra/main.bicep` (Requests Total >5, `statusCodeCategory=5xx`) with a runbook entry; the workbook has request error and p95 panels. No change needed; criterion text only needs the documented KQL/metric query for the 5xx view.
* The aggregation fix noted on 2026-11-19 is already in the source (`timeAggregation: 'Total'`, confirmed on the deployed demo-orch rule).
* Coverage register `src/core/.../monitoring_coverage.py` is src; this run does not edit it (FULL tier avoided).

## Acceptance criteria status before this change

Unticked: alerts for job failures, poison, ledger digest, IoT (ledger installed enabled; others disabled or absent); dashboard with availability/errors/latency/cost vs budget (workbook installed, render blocked by private-link query access); runbook per alert with owner (roles proposed, people not named); tokenomics dashboard beside Azure cost (demo proven 2026-11-18, billing reconciliation excluded).

## Evidence boundary

Read-only commands: `az monitor metrics alert list`, `az monitor scheduled-query list`, `az resource list` (workbooks), `az sql db show`, `az monitor metrics list` (DTU and job Executions), `az containerapp job execution list`. No secret, credential or resource was created; nothing to delete.

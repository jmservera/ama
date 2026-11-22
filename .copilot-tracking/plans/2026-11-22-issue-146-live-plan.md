# Issue 146 plan (2026-11-22)

1. `infra/main.bicep`: add `sqlDtu` metric alert (`dtu_consumption_percent` Average >80, 15 min, Sev3), conditional on `sqlTier == 'dtu'`; description names owner and `#sql-dtu`.
2. `infra/live-receiver-job.bicep`: optional `failureAlertActionGroupId`; when set, add `Executions` state=Failed Total >0 rule for the job, runbook `#job-live-receiver`.
3. `infra/monitoring-runbooks.md`: add `### SQL DTU` and `### Job live receiver` entries; add KQL/metric queries for API 5xx, receiver failures and DTU.
4. `infra/tests/test_monitoring_alert_coverage.py`: assert both rules name owner and a valid anchor.
5. Validate: bicep build both files, run infra monitoring tests; research evidence note under `docs/reference/research/`; index and log updates.
Tier: focused (infra and docs, no src, no security control change).

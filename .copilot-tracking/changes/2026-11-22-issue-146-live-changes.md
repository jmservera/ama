# Issue 146 changes (2026-11-22)

Files: infra/main.bicep (sqlDtu alert), infra/live-receiver-job.bicep (optional failure alert), infra/monitoring-runbooks.md (sql-dtu, job-live-receiver, API 5xx queries), infra/tests/test_monitoring_alert_coverage.py, docs/reference/research/issue-146-live5-monitoring-2026-11-22.md, docs/reference/README.md, docs/reference/log.md.
Tier: focused (infra and docs only, no src). Validation: bicep build clean for both templates; infra monitoring tests (31), wiring, network posture, container hosting, demo wiring (54) and src/core monitoring tests (37) pass. No Azure change; hosted CI not observed.

## Per-criterion table

| Criterion | Result | Basis |
| --- | --- | --- |
| Alerts: job failures, poison, ledger digest, IoT | Partly proven | Ledger digest installed and enabled; job, poison and IoT disabled; new receiver and DTU rules source-only; no drill |
| Dashboard: availability, errors, latency, cost vs budget | Unproven | Workbook installed; private-link query access blocks a render from this host |
| Runbook entry with owner per alert | Partly proven | Entries test-enforced with proposed roles; no named person |
| Tokenomics dashboard beside Azure cost | Proven for demo 2026-11-18 | Earlier note; billing reconciliation excluded; not re-run |

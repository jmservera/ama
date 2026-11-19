# Issue 146 research, run 20261119T154738Z

Refs #146. Disposition: reused (docs/reference/research/issue-146-live-triage-2026-11-19.md, written 2026-11-19T15:00Z) plus a fresh read-only re-check at 2026-11-19T15:50Z. Planning Readiness: Ready.

## Fresh inventory (az, resource group ama)

* Metric alerts, all enabled: foundry-throttle, sql-cpu, api-5xx, api-restarts.
* Scheduled-query alerts, all enabled: Key Vault secret-expiry, Key Vault denied-access, ledger-digest-mismatch, ledger-verify-missing.
* No tmp146 resource; zero workbooks installed.
* No job-failure, poison-queue or IoT ingestion alert installed.

## Buildable item check

The only code-shaped item is changing the job-failure rule aggregation from Maximum to Total in infra/modules/operationalMonitoring.bicep. It is infrastructure scope: FULL tier and a redeploy, which the brief says to stop and report rather than guess.

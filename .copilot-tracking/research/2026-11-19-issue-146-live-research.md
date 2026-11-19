# Issue 146 live research, 2026-11-19

Refs #146. Research disposition: executed (fresh read-only Azure check) plus reuse of the 2026-11-18 closure note
(docs/reference/research/issue-146-live3-monitoring-closure-2026-11-18.md).

Planning Readiness: Ready.

## Live inventory (read-only, `az` existing login, resource group `ama`, 2026-11-19 UTC)

* Metric alerts, all enabled: foundry-throttle (Sev2), sql-cpu (Sev3), api-5xx (Sev2), api-restarts (Sev3).
* Scheduled-query alerts, all enabled: Key Vault secret-expiry (Sev2), denied-access (Sev3), ledger-digest-mismatch (Sev1), ledger-verify-missing (Sev1).
* Workbooks in the resource group: none.
* No job-failure, poison-queue or IoT ingestion alert is installed. No `tmp146` leftovers.

## Classification of unticked criteria

| Criterion | Buildable or provable for the demo? |
| --- | --- |
| Alerts cover job failures, poison queue, ledger digest, IoT | Ledger digest proven earlier. Job-failure fix is a Bicep aggregation change (Maximum to Total) in infra/modules/operationalMonitoring.bicep: infrastructure scope, FULL tier, redeploy needed. Out of bounds for this brief. |
| Dashboard/workbook of availability, errors, latency, cost vs budget | Not installed; workspace query is private-link only so render cannot be observed; enabling public query weakens a control. Unproven. |
| Each alert has a runbook entry with an owner | Offline tests pass; owners are proposed roles, naming people is a human decision. |
| Tokenomics dashboard beside Azure cost, variance visible | Proven for the demo on 2026-11-18 (app AI report); cost reconciliation excluded by owner. |

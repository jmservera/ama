---
title: Issue 146 live research (2026-11-26)
ms.date: 2026-11-26
---

Refs #146. Read-only Azure CLI observation, resource group `ama`, 2026-11-26 about 11:07 UTC. Disposition: executed. Planning Readiness: Ready.

## Evidence

* Live inventory through `infra/scripts/monitoring_live_inventory.py`: job_failure `partial` (4 rules enabled; `job-184-bodyscan` and `job-live-simulator` have none), poison_queue enabled, ledger_digest enabled, iot_ingestion enabled. Earlier notes (live7, live9) recorded these as disabled; the estate changed since.
* Every one of the 22 alert rules has one action group; the action group has one email receiver (address not printed).
* 18 of 22 rules carry an owner and runbook anchor in the description. The four without are the legacy `alert-cutover-test-api-5xx`, `-api-restarts`, `-ledger-digest-mismatch`, `-ledger-verify-missing`; the api pair scopes to `ca-cutover-test-api`, a container app that no longer exists (orphaned rule).
* The deployed workbook has every source tile name; all eight data queries execute with exit code 0 against the workspace: ingress 170529 requests, 1449 server errors, p95 4509 ms (7 days); AppRequests and AppAvailabilityResults 0 rows (Insufficient); cost Unknown/Unreconciled; AI usage 75 attributed calls by capability; three AI limit breach rows with owner and runbook.
* Poison alert query executes: 13 `PutMessage` rows in 7 days, none on `agent-tasks-poison`, so no match and no firing proof; a drill is not permitted.
* `infra/monitoring-runbooks.md` still calls the job, IoT, poison and AI rules "disabled candidates", which no longer matches the live estate.

## Decision

No src change is warranted. Defect found: stale runbook status text. Fix in documentation only (focused tier). Enabling/deleting alerts and Portal rendering are outside the authorisation or credentials.

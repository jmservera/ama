---
title: Issue 146 monitoring coverage re-run (demo, 2026-11-18)
description: Live read-only inventory and a throwaway job-failure alert test for the unticked criteria of issue 146 in resource group ama, with gaps stated
ms.date: 2026-11-18
ms.topic: reference
---

Refs #146. Scope: synthetic demo, resource group `ama`, existing Azure CLI login, desktop only. No drills, no Key Vault rotation, no production change, no source change. No credentials, receiver addresses or secrets are recorded. This note extends the [earlier run](./issue-146-live-monitoring-evidence-2026-11-18.md); it does not replace it.

## What exists

Source (`infra/modules/monitoring.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/monitoring-workbook.json`, `infra/monitoring-runbooks.md`):

* Log Analytics, Application Insights, private link scope, action group, four metric alerts and a monthly budget.
* Job-failure, IoT and poison-queue candidate alerts, disabled by default until named-human approval (`candidateAlertsEnabled`).
* A 12-item operations workbook and 20 runbook entries, each with a proposed owner role.

Observed live at 2026-11-18T10:05Z (read-only):

| Kind | Installed |
| --- | --- |
| Metric alerts (enabled) | Foundry throttle (Sev2), SQL CPU (Sev3), API 5xx (Sev2), API restarts (Sev3), plus `alert-109-probe-connectivity` from #109 |
| Scheduled-query alerts (enabled) | ledger digest mismatch (Sev1), ledger verify missing (Sev1), Key Vault secret expiry (Sev2), Key Vault denied access (Sev3) |
| Action group | `ag-cutover-test-ops`, one email receiver |
| Workbooks | none |
| Job-failure, poison-queue, IoT-ingestion alerts | none installed |
| Budgets | list call now returns RBACAccessDenied for this login; earlier-run values (300 and 25 caps) are not re-observed |

The Sev1 digest mismatch alert that fired at 08:18Z was provoked by the forced-mismatch copy test recorded in [digest-verification-alert-live-2026-11-18.md](./digest-verification-alert-live-2026-11-18.md). It is not a tamper signal; this corrects the earlier note's "adverse finding" wording.

## Job-failure alert test (new)

Job `job-cutover-test-ledger-verify` reported Failed executions on metric `Executions` (dimension `state`): 5 in the 07:05Z hour and 6 in the 08:05Z hour. Throwaway rules, severity 3, existing action group, 24-hour window, five-minute frequency:

* `tmp146b-job-failed`, time aggregation Maximum (as in `operationalMonitoring.bicep`): created 10:05Z, no alert after about 12 minutes. Deleted.
* `tmp146c-job-failed`, time aggregation Total: created about 10:12Z; Alerts Management showed it Fired at 10:17:37Z. Deleted.

Interpretation, kept narrow: a metric alert on the real failed-job signal fires on this job when aggregated as Total over 24 hours. The source rule uses Maximum over PT15M and was not tested with that exact shape (no failure fell in a 15-minute window), so whether it would fire is unproven. A candidate follow-up is to test the source shape on a fresh failure before activation; changing the Bicep is infrastructure and needs the full validation tier, so it was not done here.

## Per-criterion result

| Criterion | Status | Evidence and reason |
| --- | --- | --- |
| C1 Alerts cover job failures, poison queue, ledger digest, IoT ingestion | Partly proven | Digest: installed, enabled and fired live. Job failures: a throwaway rule on the live signal fired (Total variant); not installed permanently. IoT: earlier run created and deleted a rule on `d2c.telemetry.ingress.sendThrottle`; no firing provoked. Poison queue: unproven; the storage diagnostic setting has no queue log category and the account blocks this client, and enabling diagnostics is an infrastructure change. |
| C2 Dashboard or workbook shows availability, errors, latency, cost against budget | Unproven | Workbook JSON has 12 items including those panels, and the earlier run deployed and deleted it. No workbook is installed. Workspace and Application Insights query access is private-link only, so rendering cannot be observed from this host; enabling public query would weaken a security control. |
| C3 Each alert has a runbook entry with an owner | Partly proven | 20 "Proposed owner" entries in `infra/monitoring-runbooks.md`; the `infra/tests` suite passes (750 tests, 4 skipped, 325 s). Owners are roles awaiting appointment, not named people. |
| C4 Tokenomics: AI usage by capability beside Azure cost with visible variance | Unproven | Panels exist in the workbook source; same rendering limit as C2, and no Azure cost export table was provisioned. |

The ticked criteria (diagnostic log exclusion, RAI harm monitoring, AI-limit alert ownership, budget as notification) were not re-examined.

## Cleanup and limits

* `az resource list -g ama` shows no `tmp146` names after the run.
* Email delivery to the ops mailbox was not observed; the Alerts Management record is the proof of firing.
* Portal screenshots and Playwright proofs were not taken: no alert or workbook surface is reachable from a signed-in browser session in this environment.

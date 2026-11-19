---
title: Issue 146 monitoring criteria triage (demo, 2026-11-19)
description: Per-criterion proven or unproven status for the unticked acceptance criteria of issue 146 after a fresh read-only live inventory
ms.date: 2026-11-19
ms.topic: reference
---

Refs #146. Synthetic demo, resource group `ama`, desktop only. Read-only Azure CLI inventory at 2026-11-19T15:00Z; no resource created, no secret recorded. Extends [the 2026-11-18 re-run](./issue-146-live-monitoring-rerun-2026-11-18.md).

## Observed

* Enabled metric alerts: Foundry throttle, SQL CPU, API 5xx, API restarts.
* Enabled scheduled-query alerts: Key Vault secret expiry, Key Vault denied access, ledger digest mismatch, ledger verify missing.
* No job-failure, poison-queue or IoT-ingestion alert installed. `az resource list -g ama` shows no `tmp146` resource. The workbook list command needs a `--category` argument and was not rerun.
* Source: `infra/modules/operationalMonitoring.bicep` keeps these candidate alerts disabled until `approvalReference` is set (named-human approval).

## Per-criterion status

| Criterion | Status | Reason |
| --- | --- | --- |
| C1 Alerts for job failures, poison queue, ledger digest, IoT | Partly proven | Digest installed and fired (2026-11-18 forced-mismatch test). Job-failure fired only as a Total-aggregation throwaway; the source Maximum shape did not fire in a 12-minute watch and is unproven. Poison and IoT candidates are disabled pending approval. |
| C2 Workbook for availability, errors, latency, cost | Unproven | Workbook source exists; none installed; query access is private-link only, so rendering cannot be shown from this host. |
| C3 Runbook entry with owner per alert | Partly proven | Entries carry proposed owner roles in `infra/monitoring-runbooks.md`; no named people. |
| T2 AI usage by capability beside Azure cost, variance visible | Unproven | Same rendering limit; no Azure cost export table is provisioned. |

## Decision

The only buildable item, aligning the job-failure rule aggregation to Total, edits `infra/` and so needs the FULL validation tier and a live re-test on a fresh failure. Every other remaining criterion needs human approval or private-link access. No source change was made.

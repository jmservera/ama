---
title: Issue 145 live run 4 audit with retained Azure settings output (demo)
description: Per-criterion proven and unproven table for issue 145 on 2026-11-18, closing the run 3 evidence limits with retained read-only Azure output and separating production-only items
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 145
  - point-in-time restore
  - backup retention
  - recovery objectives
estimated_reading_time: 6
---

## Scope and authority

Refs #145. Synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive Azure billing reconciliation, DPO and Legal approval and person-run assistive technology testing for the demo. This run made read-only Azure calls and Bicep builds only. No source, infrastructure or Azure resource changed, nothing was created, and no credential was read or printed. This note ticks nothing on the issue.

Raw output, server name redacted: [azure_cli_outputs.txt](./issue-145-live-r4-raw-2026-11-18/azure_cli_outputs.txt) and [azure_cli_outputs_2.txt](./issue-145-live-r4-raw-2026-11-18/azure_cli_outputs_2.txt), captured 2026-11-18T16:35Z.

## What this run adds

[Run 3](./issue-145-live-run3-pitr-rerun-2026-11-18.md) listed three observations as "Observed; raw output not retained": the backup and retention settings, the earliest restore date, and the absence of throwaway resources. The retained output now covers them for the state at 16:35Z:

* `retrofit` is Standard S0 (10 DTU), online, backup storage redundancy Local (requested and current), zone redundancy off, created 2026-10-16, earliest restore date 2026-11-04T16:35Z.
* Short-term retention 14 days with a 12-hour differential interval. Long-term retention weekly, monthly and yearly all `PT0S`.
* The server holds `retrofit` and `master` only, so the run 1 and run 3 restore copies are gone. No Container Apps job has `145` in its name. (`tmp146d-failjob` also exists; it belongs to another issue and was not touched.)
* The SQL server has public network access disabled, Entra-only authentication and TLS 1.2.
* Blob store: versioning on, soft delete 30 days, container soft delete 30 days, blob point-in-time restore not configured.
* The demo API revision `ca-cutover-test-demo-api--0000032` runs `ZF_STORE=mssql` with profile `demo`.

The restore duration (about 34 minutes in run 3, about 57 minutes in run 1) is still "Observed; raw output not retained", because no new restore was run. A third restore would repeat the same single-sample observation at about an hour of wall time.

## Repository check of the parameter criterion

* `infra/main.bicep` exposes `sqlTier` (serverless or provisioned), `sqlVCores`, `sqlAutoPauseDelayMinutes`, `zoneRedundant`, `sqlBackupStorageRedundancy` and `sqlBackupRetentionDays`, and passes them to `infra/modules/sql.bicep`, which selects `GP_S_Gen5` or `GP_Gen5` and sets auto-pause only for serverless.
* `infra/parameters/prod.bicepparam` and `infra/main.pilot.example.bicepparam` set `sqlTier` to `provisioned` (ADR 0002 decision 1); sizing, region, zone redundancy and backup redundancy are marked placeholders awaiting owner decisions.
* `az bicep build` of `infra/main.bicep` and `az bicep build-params` of the prod, dev and pilot example parameter files succeed.
* `infra/sql-recovery-runbook.md` records the recovery time objective as "Undecided" with owner Digital owner with Programme owner.
* `src/core/src/zava_forward/core/recovery.py` still reapplies only erasure deletions after a restore. No code re-applies release, suspension or allowance state.

## Per-criterion status

| # | Criterion | Status | Evidence or reason |
| --- | --- | --- | --- |
| C1 | SKU, auto-pause, redundancy are environment parameters, pilot setting recorded | Proven in the repository (ticked on the issue) | Parameters and builds above. Pilot sizing, region and zone are placeholders, so the setting recorded is the tier, not final sizing; that is production-only |
| C2 | Point-in-time restore performed, ledger verification recorded | Proven for the demo, with a limit | Runs 1 and 3: actual restore, application chain intact, restored head equal to source entry 1694. Native `sp_verify_database_ledger` was denied (`VIEW LEDGER CONTENT`); granting it changes a database control and is out of authority |
| C3 | Recovery objectives stated with evidence, or undecided with owner | Proven (ticked on the issue) | Runbook records RTO undecided with owner; restore times and recovery point are samples, not objectives |
| C4 | Backup redundancy and retention match #121 decisions | Unproven, production-only | Settings recorded above; #121 has no approved retention decision (Legal period and DPO position moved to #1906), so there is nothing to match |
| R1 | Actual backup restored with document and audit state | Partly proven | SQL audit and ledger state restored; documents live in blob storage with versioning and soft delete but no blob point-in-time restore, and were not restored |
| R2 | Reconcile versions and counts; reapply tombstones and holds | Partly proven | Counts and chain prefix reconciled in run 3; erasure reapply proven by the #114 drill; no legal hold state exists on the demo |
| R3 | No resurrection of revoked, suspended, erased or spent state | Unproven | Erased content proven by #114. Release, suspension and allowance tables are empty (vacuous) and no reapply code exists. Proof needs seeded revocations before a restore point: seeding the live source is outside authority, and a fix is a `src` change at the FULL tier |
| R4 | DPO and record-owner approvals | Not needed for the demo | Owner decision 2026-11-18; production in #1906 |
| R5 | Independent qualified witness | Unproven, production-only | The phase witness is worker-authored, not an independent qualified person |
| R6 | Disposable restrictions, authorised bounded exercise | Proven | Throwaway copies and jobs were deleted and are absent in the retained output; this run created nothing |
| R7 | SQLite and SQL-shape emulation labelled lower-tier | Proven (ticked on the issue) | Azure-tier evidence here; SQLite regressions stay lower-tier |
| R8 | Publish only hashes, status, counts | Proven (ticked on the issue) | Retained files hold configuration values and names only, server name redacted; no `@` or GUID found |

## Production-only items

C4 (Legal retention and #121 match), R4 (DPO approvals, waived for the demo), R5 (independent qualified witness), final pilot sizing, region and zone choice, and blob point-in-time recovery for production documents.

## Remaining engineering gap

R3 needs a post-restore reconciliation that re-applies release revocation, task suspension and spent allowance, with a test restoring an older backup that holds seeded revocations. That is a `src/core` change and takes the FULL validation tier; it was not attempted here.

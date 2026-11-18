---
title: Live Azure SQL point-in-time restore evidence for issue 145 (demo)
description: Recorded run on 2026-11-18 restoring the demo SQL database to a throwaway copy, verifying the audit ledger chain and reconciling it with the source, with a per-criterion proven/unproven record
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 145
  - point-in-time restore
  - ledger verification
  - recovery objectives
estimated_reading_time: 8
---

## Scope and authority

Refs #145. The target is the synthetic demo only, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). The run read the source database `retrofit` on server `sql-cutover-test-rzsrg` and created one throwaway database. Nothing else was changed. The #114 recovery drill (`drill114src`, `drill114restored`, `job-drill114-erase`) was neither used nor repeated; #114 owns the per-year ledger and erasure re-application evidence, and this note covers only the point-in-time restore itself.

No credential or private record was read or printed. The SQL server has public network access disabled, so the checks ran from a short-lived Container Apps job in the demo environment using the existing managed identity. Only counts, timestamps and audit-chain hashes are recorded below.

## Source configuration (read-only)

| Setting | Value | Source |
| --- | --- | --- |
| Database `retrofit` SKU | Standard, 10 DTU (S0) | `az sql db show` |
| Backup storage redundancy | Local | `az sql db show` |
| Short-term (PITR) retention | 14 days, differential backup every 12 hours | `az sql db str-policy show` |
| Long-term retention | weekly, monthly and yearly all `PT0S` (none) | `az sql db ltr-policy show` |
| Earliest restore date reported | 2026-11-04T08:32:01Z | `az sql db show` |
| Ledger | database ledger on, 64 ledger tables (append-only `audit`, `assistant_events`; updatable tables with history) | SQL probe |
| Zone redundancy | off | `az sql db show` |

## Procedure and results

1. At 2026-11-18T08:32:55Z `az sql db restore --time 2026-11-18T08:17:55Z --service-objective S0 --backup-storage-redundancy Local` started a point-in-time restore of `retrofit` to `retrofit-pitr145`.
2. The new database stayed invisible to ARM reads while it was created, then showed `Restoring` and `Online` at 2026-11-18T09:29:30Z. Wall time from request to online was about 57 minutes for a database holding roughly 1,000 audit rows and 980 cases. The local CLI call was interrupted after 27 minutes; the server-side restore continued, and a second request was rejected with `DatabaseNameInUse`, which confirms the first was still in progress.
3. A throwaway job `job-145-pitr-probe` ran one read-only script per database. It counted rows in every table, replayed the audit hash chain with `zava_forward.core.ledger.verify_entries` and `verify_years`, and compared the audit head with `audit_head`.
4. The restored database and the job were deleted at 2026-11-18T09:33Z. `az sql db list` then showed only `retrofit` and `master`, and no job with `145` in its name remained.

### Restored copy against the source

| Check | Restored `retrofit-pitr145` | Source `retrofit` |
| --- | --- | --- |
| Audit entries | 1003 | 1100 at 08:49Z, 1481 at 09:31Z |
| Last audit entry time | 2026-11-18T08:17:54 | live, still growing |
| Audit chain (app verifier) | intact, 1003 entries | intact, 1100 and 1481 entries |
| `audit_head` row | count 1003, head `cabde033b0fed9399d57710413c10860ab1c7ee904afd456fc2a92a69b4034f8` | count 1481 at 09:31Z |
| Source audit entry number 1003 | hash `cabde033b0fed9399d57710413c10860ab1c7ee904afd456fc2a92a69b4034f8` (2026-11-18T08:17:54) | identical to the restored head |
| `cases`, `chat_thread`, `chat_message`, `sensor_reading`, `sensor_delivery`, `resident_showcase.allowed_case`, `staff`, `meta` | 980, 22, 74, 812, 99, 522, 1, 15 | identical |
| `recommendations` | 131 | 154 at 08:49Z, 171 at 09:31Z (rows added after the restore point) |
| `assistant_events` | 46 | 54 at 08:49Z, 120 at 09:31Z (rows added after the restore point) |
| Ledger tables | 64 | 64 |
| `assistant_allowance`, `assistant_releases`, `assistant_dispatch_gate`, `assistant_tasks`, `chat_memory`, `notice_ack` | 0 each | 0 each |

The restored audit head equals the source's entry 1003 hash, so the restore is an exact prefix of the live chain taken at the requested time (last entry 1 second before the requested 08:17:55). Counts that differ are tables the live demo kept writing to after the restore point.

Limit found: the managed identity lacks `VIEW LEDGER CONTENT`, so `sys.sp_verify_database_ledger` returned a permission error on the restored copy and on the source. The native engine verification did not run. The recorded ledger result is the application hash-chain verification only. Granting the permission would change a database control, which this run was not authorised to do.

## Observed recovery figures

* Restore duration, request to online: about 57 minutes at this size. This is one observation for a small demo database, not a recovery time objective.
* Recovery point achieved: the last audit entry in the restored copy is 1 second before the requested time. This is one observation, not a guarantee; Azure documents log backups roughly every 10 minutes as the nominal RPO and the objective remains recorded as undecided with owners under criterion 3.
* Cost: one S0 database for about 4 minutes online plus the restore period, and one 0.5 vCPU job for about 5 minutes. Both are far below the USD 700 cap and were deleted. Azure billing reconciliation is not needed for the demo.

## Per-criterion status

| # | Criterion | Status | Evidence or reason |
| --- | --- | --- | --- |
| 1 | SKU, auto-pause and redundancy are environment parameters, pilot recorded | Already ticked on the issue | Not re-proven here |
| 2 | A point-in-time restore is performed and the ledger verification result is recorded | Proven for the demo, with a limit | Restore and prefix match above; app hash-chain verification intact; native `sp_verify_database_ledger` not run (permission) |
| 3 | Recovery time and point objectives stated or undecided with owner | Already ticked on the issue | This run adds one observed restore duration and RPO figure as evidence only |
| 4 | Backup storage redundancy and retention match the retention decisions of #121 | Unproven | Current settings are recorded (Local, 14 days, no long-term retention) but #121 now defers the Legal retention period and DPO position to production (#1906), so there is no decision to match on the demo |
| R1 | Restore an actual backup with document/audit state on authorised disposable infrastructure | Partly proven | An actual Azure PITR backup restored to a throwaway database with audit and ledger state, authorised by the owner on 2026-11-18. Document blobs live in a separate store and were not restored or compared |
| R2 | Reconcile versions/counts, history and authority; reapply erasure tombstones and legal holds | Partly proven | Counts and audit prefix reconciled. The erasure register and legal holds were not reapplied: the demo has no erasure or hold state to reapply, and seeding it would alter the live demo database. #114 covers erasure re-application |
| R3 | Restored state does not resurrect revoked permission, suspended proposals, erased content or spent allowance | Unproven | `assistant_allowance`, `assistant_releases` and `assistant_dispatch_gate` hold no rows in source or copy, so a clean result is vacuous. A real test needs seeded revocations, outside this run's authority |
| R4 | DPO/record owners approve retention, hold, audit conflicts and provider-copy handling | Not needed for the demo | Owner decision 2026-11-18; moved to production work (#1906) |
| R5 | Independent qualified owners witness expected and actual results | Unproven | The phase witness log is observational and worker-authored; no independent qualified witness took part. Qualified-owner witness is a production step |
| R6 | Observe disposable restrictions; no pilot/live database targeted; Azure exercise needs separate authorisation and runbook | Proven for the demo | The target was a throwaway copy on the demo server; the source was only read; the owner decision of 2026-11-18 is the authorisation; the plan, details and changes records serve as the bounded runbook |
| R7 | SQLite/SQL-shape emulation labelled lower-tier evidence | Proven | This note is Azure-tier. Earlier SQLite backup-copy regressions stay lower-tier and are not cited as PITR |
| R8 | Publish only permitted hashes, status and counts | Proven | The note holds counts, timestamps and public audit-chain hashes only; no credential, token or private record |

## Residual items for the issue

* Native ledger verification needs `VIEW LEDGER CONTENT` for the verifying identity or an admin-run check; record as a follow-up, not a demo blocker.
* A resurrection test (R3) needs seeded revocation, suspension and allowance state in a throwaway database, restored over a point before and after the change.
* The 57 minute duration is a single small-database sample; sizing the pilot objective is still an owner decision.

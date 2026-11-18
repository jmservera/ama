---
title: Issue 145 live run 3 point-in-time restore rerun (demo)
description: Second live point-in-time restore of the demo SQL database on 2026-11-18 with the raw probe output retained, covering ledger verification, retention, reconciliation and resurrection checks
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 145
  - point-in-time restore
  - ledger verification
  - resurrection
estimated_reading_time: 6
---

## Scope and authority

Refs #145. Synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills of production, no Key Vault rotation, no production change). This run repeats the restore of [run 1](./issue-145-live-pitr-restore-evidence-2026-11-18.md) because run 1 kept no raw output. The source database was only read; the production-like #114 drill resources were not touched. No credential was read or printed. Server, subscription and identity names are redacted.

Raw output: [issue-145-live-r3-raw-probe-2026-11-18.txt](./issue-145-live-r3-raw-probe-2026-11-18.txt) (counts, timestamps and chain hashes only).

## Procedure

1. Restore point 2026-11-18T11:32:36Z; `az sql db restore` to a throwaway database (S0, Local backup redundancy). The copy was online at about 12:22Z, roughly 34 minutes after the request (Observed; raw output not retained; run 1: about 57 minutes; both are single small-database samples, not objectives).
2. A throwaway Container Apps job (existing orchestrator image and managed identity, 0.5 vCPU) ran one read-only script against the copy and the source at 12:30Z.
3. The job and the copy were deleted at 12:31Z. `az sql db list` then showed `retrofit` and `master` only, and no job with `145` in its name remained (Observed; raw output not retained).

## Results

| Check | Restored copy | Source `retrofit` |
| --- | --- | --- |
| Audit entries | 1694, last entry 2026-11-18T11:32:30 (6 seconds before the restore point) | 1770 at 12:30Z, still growing |
| Application hash chain (`verify_entries`, `verify_years`) | intact | intact |
| `audit_head` row | count 1694, head `b54729e8...8b66b01a` | not compared (count moved on) |
| Source audit entry 1694 | hash equals the restored head | n/a |
| Native `sp_verify_database_ledger` | denied, `VIEW LEDGER CONTENT` | denied, same |
| Ledger tables | 64 | 64 |
| Tables with different counts | `audit` 1694 vs 1770, `recommendations` 220 vs 243, three ledger history tables (1628, 25, 1591 vs 1653, 26, 1666) | rows written after the restore point |
| Other tables (60 of 64 incl. `resident_showcase.allowed_case` 522, `assistant_allowance` 0, `assistant_releases` 0, `assistant_dispatch_gate` 0, `chat_memory` 0, `notice_ack` 0) | identical counts | identical |
| `assistant_tasks` | 5 | 5 |

The restored copy is a prefix of the live chain (head hash compared at entry 1694), and every difference is explained by writes after the restore point. The native engine verification still did not run: the identity lacks `VIEW LEDGER CONTENT`, and granting it would change a database control this run was not authorised to change.

## Backup and retention settings (read-only, 2026-11-18T12:31Z)

Standard S0, backup storage redundancy Local, zone redundancy off, short-term retention 14 days with a 12-hour differential interval, long-term retention weekly, monthly and yearly all `PT0S`, earliest restore date 2026-11-04 (Observed; raw output not retained). [Issue 121 evidence](./issue-121-live-data-protection-evidence-2026-11-18.md) records retention as unknown until Legal sets a period and defers it to production (#1906), so there is no approved decision to match; the settings are recorded, not matched.

## Resurrection check

* Release, allowance, dispatch gate, chat memory and notice acknowledgement tables hold zero rows in the source and the copy, so a clean result is vacuous. `assistant_tasks` holds 5 rows in both; their suspension state was not read, so no claim is made about it.
* A point-in-time restore rewinds rows, so a revocation made after the restore point would reappear. No code re-applies release, suspension or allowance after a restore ([run 2 note](./issue-145-live-run2-reverification-2026-11-18.md)). Proving it needs seeded revocations on a database whose restore point precedes them; seeding the live demo source is outside the authority, and a fix needs a `src` change at the full tier.

## Per-criterion status

| # | Criterion | Status | Evidence or reason |
| --- | --- | --- | --- |
| 1 | SKU, auto-pause, redundancy parameters | Ticked on the issue | Not re-proven |
| 2 | Restore performed, ledger verification recorded | Proven for the demo, with a limit | Second restore with raw output retained; application chain intact; native verification denied |
| 3 | RTO and RPO stated or undecided with owner | Ticked on the issue | Second sample of 34 minutes (Observed; raw output not retained) and 6 seconds recovery point, evidence only |
| 4 | Backup redundancy and retention match #121 | Unproven | Settings recorded; #121 has no approved decision to match (production, #1906) |
| R1 | Actual backup restored with document and audit state | Partly proven | SQL audit and ledger state only; blob store has no point-in-time restore and was not restored |
| R2 | Reconcile counts and history; reapply tombstones and holds | Partly proven | Counts and chain prefix reconciled; erasure re-application is #114; no hold state exists on the demo |
| R3 | No resurrection of revoked, suspended, erased or spent state | Unproven | Tables empty (vacuous); no re-apply mechanism; see above |
| R4 | DPO and record-owner approvals | Not needed for the demo | Owner decision 2026-11-18 |
| R5 | Independent qualified witness | Unproven | Phase witness is worker-authored; production step |
| R6 | Disposable restrictions, authorised exercise | Proven | Throwaway copy and job, deleted and confirmed absent (Observed; raw output not retained) |
| R7 | Lower-tier evidence labelled | Proven | Azure-tier here; SQLite regressions stay lower-tier |
| R8 | Publish only hashes, status, counts | Proven | Raw file holds counts, timestamps and chain hashes only |

## Evidence limits

The raw probe file holds only the read-only database probe output. These `az` CLI observations were not saved and are labelled "Observed; raw output not retained":

* The restore time of about 34 minutes (procedure step 1, criterion 3 row).
* The backup and retention settings and the earliest restore date.
* The post-delete `az sql db list` and job absence check (procedure step 3, criterion R6 row).

## Cost and cleanup

One S0 database for about 10 minutes online plus the restore period, and one 0.5 vCPU job for about 2 minutes (estimates, far below USD 700; billing reconciliation is not needed for the demo). Both deleted. Prior state files were not changed.

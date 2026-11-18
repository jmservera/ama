---
title: Issue 145 live run 2 re-verification and criterion status (demo)
description: Read-only re-verification on 2026-11-18 of the demo SQL backup configuration and cleanup, with a code check explaining why restore resurrection cannot be proven on the demo, and the final per-criterion record
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 145
  - point-in-time restore
  - resurrection
  - recovery objectives
estimated_reading_time: 6
---

## Scope

Refs #145. Synthetic demo, desktop only. This run adds to [the first live restore note](./issue-145-live-pitr-restore-evidence-2026-11-18.md), which holds the actual point-in-time restore (about 57 minutes, audit chain intact, restored head equal to the source's entry 1003) and the #114 drill in [sql-ledger-live-2026-11-18.md](./sql-ledger-live-2026-11-18.md). No second restore was run: it would repeat the same observation at about an hour of wall time and the owner decision forbids drills on the live database. This run made read-only Azure calls only and changed nothing. No credential was read or printed.

## Fresh read-only checks (2026-11-18T10:53Z)

The results below come from read-only `az` calls; raw `az` output not retained.

| Check | Result |
| --- | --- |
| Databases on `sql-cutover-test-rzsrg` | `retrofit` (Standard S0, 10 DTU, Online) and `master`; the throwaway `retrofit-pitr145` and the #114 drill databases are absent |
| Container Apps jobs in `ama` | eight standing `job-cutover-test-*` jobs; no job named for 145 or the #114 drill remains |
| Backup storage redundancy | Local, zone redundancy off |
| Short-term retention | 14 days, differential backup every 12 hours |
| Long-term retention | weekly, monthly, yearly `PT0S` (none) |
| Earliest restore date | 2026-11-04T10:53:44Z, so a restore point exists across the full 14 days |
| Blob store `stcutovertestrzsrg` (documents) | soft delete 30 days, versioning on, blob point-in-time restore off |

The blob container listing was blocked by the storage network rules, so only the account-level protection settings were read.

## Why restore resurrection (R3) cannot be proven on the demo

Release status (`assistant_releases`), task suspension and its epoch, and spent allowance (`assistant_allowance`) are rows in the SQL database ([assistant_release.py](../../../src/core/src/zava_forward/core/assistant_release.py), [continuity.py](../../../src/core/src/zava_forward/core/continuity.py)). A point-in-time restore rewinds them with the rest of the database. The #114 drill showed that rewind directly: the restored ledger returned to 602 entries and the erased case came back unredacted until `reapply_deletions` ran. The only reconciliation code is `reapply_deletions` in [recovery.py](../../../src/core/src/zava_forward/core/recovery.py), driven by an erasure register held outside the database. A search of `src/core`, `src/agents` and `src/api` found no equivalent that re-applies a revocation, suspension or spent allowance after a restore. To reproduce the search, run `git grep -nE "reapply_deletions|reconcil|restore" -- src/core src/agents src/api` and read the hits in `src/core`; the result is a search result, not a proof of absence. A drill would therefore be expected to show a revoked or suspended state coming back, which is a product gap, not a proof. Closing it needs a `src` change (an out-of-database register for release, suspension and allowance decisions) and the full validation tier, which this run does not take. The three tables are also empty on the demo, so a restore of the demo alone would be vacuous. Recorded as a finding for follow-up.

## Final per-criterion record

| # | Criterion | Status | Evidence or reason |
| --- | --- | --- | --- |
| 1 | SKU, auto-pause, redundancy parameters | Ticked on the issue | Not re-proven |
| 2 | PITR performed, ledger verification recorded | Proven for the demo, with a limit | First live note: restore to `retrofit-pitr145`, app hash chain intact, prefix head matched. Native `sp_verify_database_ledger` was denied (`VIEW LEDGER CONTENT`) and was not worked around |
| 3 | RTO and RPO stated or undecided with owner | Ticked on the issue | One observed restore time and RPO recorded as evidence only |
| 4 | Backup redundancy and retention match #121 | Unproven | Settings recorded above (Local, 14 days, no long-term). #121 moved the Legal retention period and DPO position to production (#1906), so no decision exists to match |
| R1 | Actual backup restored with document and audit state | Partly proven | SQL audit and ledger state restored. Documents live in blob storage with soft delete and versioning but no blob point-in-time restore, and were not restored |
| R2 | Reconcile counts and history; reapply tombstones and holds | Partly proven | Counts and audit prefix reconciled; erasure re-application proven by #114; no legal hold state exists on the demo |
| R3 | No resurrection of revoked, suspended, erased or spent state | Unproven | Erased content: proven by #114. Release, suspension and allowance: no mechanism exists and tables are empty, see above |
| R4 | DPO and record-owner approvals | Not needed for the demo | Owner decision 2026-11-18, moved to #1906 |
| R5 | Independent qualified witness | Unproven | Production step; the phase witness is worker-authored |
| R6 | Disposable restrictions, authorised bounded exercise | Proven | Throwaway targets only; owner decision is the authorisation; plan, details and changes are the runbook |
| R7 | Lower-tier evidence labelled | Proven | Azure-tier evidence here; SQLite regressions stay lower-tier |
| R8 | Publish only hashes, status, counts | Proven | Only configuration values, counts and public hashes appear |

## Cost and cleanup

This run created no billable resource. The earlier restore and job were deleted and are confirmed absent above.

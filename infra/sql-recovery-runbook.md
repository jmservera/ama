---
title: Azure SQL pilot tier, backup restore and recovery runbook
description: Bounded point-in-time restore and ledger verification procedure with recorded objectives and evidence status (issue 145)
ms.date: 2026-11-01
---

Refs #145. Source: ADR 0002 decision 1, BRD NFR-002 and NFR-004, DH-005.

## Environment parameters

| Parameter | Dev (`main.bicepparam`) | Pilot (`main.pilot.example.bicepparam`) |
| --- | --- | --- |
| `sqlTier` | `serverless` (`GP_S_Gen5`) | `provisioned` (`GP_Gen5`) |
| `sqlAutoPauseDelayMinutes` | 60 (serverless only) | Not applicable; provisioned has no auto-pause |
| `sqlVCores` | 2 (maximum) | 2 placeholder; size from a load result not yet recorded |
| `zoneRedundant` | `false` | Owner decision after the region capability check |
| `sqlBackupStorageRedundancy` | derived (`Local`) | Placeholder; empty follows `zoneRedundant` |
| `sqlBackupRetentionDays` | 14 | 14 placeholder; point-in-time window only |

The pilot file is a non-deployable example; the setting is recorded, not deployed.

## Objectives

| Item | Value | Owner | Evidence |
| --- | --- | --- | --- |
| Recovery time objective | Undecided | Digital owner with Programme owner (NFR-004: owners approve limits before live use) | None; no restore timed |
| Recovery point objective | Undecided | Digital owner with Programme owner | None; platform PITR granularity is not an approved objective |
| Backup retention matching legal retention | Undecided | Legal (#121) | #121 is open; 14 days covers recovery only |

## Procedure (disposable target only)

Requires separate explicit authorization and a disposable server. Never target a pilot or live database.

```bash
az sql db restore --resource-group <rg> --server <server> --name retrofit \
  --dest-name retrofit-restore-<yyyymmdd> --time <UTC ISO 8601 inside retention>
```

Record start and end times, then run as the Entra admin group on the restored copy. Native SQL ledger verification needs digests captured from the source database (automatic digest storage or `sys.sp_generate_database_ledger_digest`) and their storage location metadata, not digest contents. Keep this step blocked until native digests exist for the restore point. The application anchors published by the orchestrator (`count`/`head`) are not native digests; verify them separately against the immutable blob container.

```sql
DECLARE @locations NVARCHAR(MAX) = N'[{"path":"<digest-storage-url>","last_digest_block_id":<id>,"is_current":1}]';
EXEC sp_verify_database_ledger_from_digest_storage @locations;
SELECT COUNT(*) FROM <audit ledger table>;
```

Compare row counts and latest version against the source at the restore point. Reapply erasure tombstones and legal holds, and confirm that revoked permissions, suspended proposals and spent allowance are not resurrected. Delete the copy afterwards. Publish only hashes, status and counts.

## Evidence

| Check | Status | Notes |
| --- | --- | --- |
| Point-in-time restore of an actual backup | Not performed | Blocked: no authorized disposable Azure infrastructure in this change |
| Ledger verification after restore | Not performed | Depends on the restore |
| Timed recovery against objectives | Not performed | Objectives undecided |
| Independent witness and DPO or record-owner approval | Not performed | Required by the RAI restore criteria |
| Parameter contract and Bicep compilation | Passed locally | `infra/tests/test_sql_tier.py`; lower-tier evidence, not a restore |

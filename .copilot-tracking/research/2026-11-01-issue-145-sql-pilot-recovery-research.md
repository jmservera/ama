# Research: issue 145 Azure SQL pilot tier, backup restore and recovery proof (2026-11-01)

Task: issue-145-sql-pilot-recovery. Disposition: executed (focused). Planning Readiness: Ready.

## Evidence

* `infra/modules/sql.bicep` hardcodes `GP_S_Gen5` serverless, `autoPauseDelay: 60`, `minCapacity: 0.5`, a 14 day short-term retention and `requestedBackupStorageRedundancy` derived only from `zoneRedundant`. Ledger is on, Entra-only auth, auditing and threat protection exist.
* `infra/main.bicep` exposes only `zoneRedundant`; no SKU, auto-pause, backup redundancy or retention parameter. `main.pilot.example.bicepparam` is a non-deployable placeholder; `main.bicepparam` and `main.test.bicepparam` are dev.
* ADR 0002 decision 1 (line 446): serverless for dev, provisioned general purpose for pilot; auto-pause causes cold starts so not for pilot. DH-005 requires restore and deletion drills before real data.
* BRD NFR-004: owners approve response and recovery limits before live use. No RTO or RPO value is decided anywhere. NFR-002 requires immutable versions (ledger).
* Issue #121 (retention) is open and unresolved: Legal sets the retention period, so no retention value can be "matched" yet.
* Infra tests are stdlib `unittest` text checks over Bicep in `infra/tests/`; `bicep` CLI is available locally. No Azure subscription or authorized disposable infrastructure is available in this session, so a real PITR cannot be performed.

## Decisions

* Add environment parameters (tier, vCores, auto-pause, backup redundancy, retention days) with unchanged dev defaults; record pilot setting in the pilot example (provisioned, no auto-pause, zone redundancy left as owner decision).
* Add a bounded PITR and ledger verification runbook with a result-recording template; state RTO/RPO as undecided with owner (Digital, per NFR-004); record PITR as not performed (blocked: authorization).
* No pilot or live database is targeted.

## Not in scope

Performing the Azure restore, load results, setting retention (#121), erasure/provider-copy approvals.

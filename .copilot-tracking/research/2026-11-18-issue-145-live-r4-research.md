---
title: Issue 145 live run 4 research (demo SQL tier and restore audit)
ms.date: 2026-11-18
---

Refs #145. Task: issue-145-live. Synthetic demo, desktop only; live Azure authorised (rg ama, cap USD 700, no drills, no Key Vault rotation, no production change). Tier FOCUSED, docs-only unless src changes (then STOP: FULL tier).

## Opening state

* Issue ticks: C1 and C3 and two RAI criteria ticked; C2, C4, R1 to R6 open.
* Prior notes read at open: run 1 restore, run 2 re-verification, run 3 rerun with raw probe, #114 drill, #121 evidence.
* Known evidence limits from run 3: restore duration, backup settings and cleanup were "Observed; raw output not retained".
* Plan of research: retain raw `az` output for those limits; re-check repo parameterisation (C1) against `infra/modules/sql.bicep` and environment parameter files; check blob state and resurrection gap (R3) by code; decide whether a throwaway-copy experiment is feasible.

Research disposition: executed (to be completed below). Planning Readiness: pending.

## Findings (executed 2026-11-18T16:35Z to 16:50Z)

* Raw read-only `az` output retained, server name redacted: `.copilot-tracking/evidence/2026-11-18/issue-145-live-r4/azure_cli_outputs.txt` and `azure_cli_outputs_2.txt`. It closes run 3's "raw output not retained" limits for settings, earliest restore date, and throwaway absence.
* Live: `retrofit` S0 Standard, backup redundancy Local, zone off, short-term retention 14 days, differential 12 h, long-term weekly/monthly/yearly PT0S, earliest restore 2026-11-04, only `retrofit` and `master` on the server, no job named for 145, SQL public access Disabled, Entra-only, TLS 1.2; blob versioning on, soft delete 30 days, no blob PITR; app `ca-cutover-test-demo-api--0000032` with `ZF_STORE=mssql`, profile `demo`.
* C1 repo: `infra/main.bicep` exposes `sqlTier`, `sqlVCores`, `sqlAutoPauseDelayMinutes`, `zoneRedundant`, `sqlBackupStorageRedundancy`, `sqlBackupRetentionDays`; `sql.bicep` branches SKU on `sqlTier`; pilot/prod parameter files set `provisioned` with placeholders for sizing and zone; `az bicep build` of main.bicep and build-params of prod and pilot example succeed.
* C3 repo: `infra/sql-recovery-runbook.md` records RTO "Undecided" with owner (Digital owner with Programme owner).
* R3 code: `src/core/.../recovery.py` still reapplies only erasure deletions after a restore; no release, suspension or allowance re-apply exists. Unchanged since run 2.
* A new restore or throwaway-copy resurrection experiment was considered and not run: a restore repeats runs 1 and 3 (about an hour), and seeding revocations needs either the live source (outside authority) or a src change (FULL tier, out of scope).

Research disposition: executed and reused (runs 1 to 3). Planning Readiness: Ready.

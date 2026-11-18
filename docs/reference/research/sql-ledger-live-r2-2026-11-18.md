---
title: Azure SQL ledger tamper-evidence and per-year verification rerun (demo, issue 114)
description: Second live run for issue 114 on 2026-11-18 covering ledger tamper evidence on live audit data, per-year verification and the native ledger check, with a per-criterion proven/unproven record
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
---

Refs #114. Scope is the synthetic desktop demo in resource group `ama`, database `retrofit` on `sql-cutover-test-rzsrg`, under the owner decisions of 2026-11-18 (live Azure authorised, cap USD 700, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO/Legal approval and person-run assistive-technology testing not needed). This note adds to [sql-ledger-live-2026-11-18.md](./sql-ledger-live-2026-11-18.md), which holds the 30-minute load, latency, cost and point-in-time-restore results; those are not repeated.

## Method

A throwaway Container Apps job `job-114-r2-probe` (orchestrator image already in use, existing user-assigned identity, 0.5 vCPU) ran [probe.py](./sql-ledger-live-r2-2026-11-18/probe.py) once successfully at about 10:57Z (an earlier execution `job-114-r2-probe-2r7mad8` failed with a `KeyError` in the probe itself and is preserved as adverse evidence; the script was then patched). The probe only reads `retrofit`. Tamper steps mutate in-memory copies of the live audit entries. Output is in [probe-job.log](./sql-ledger-live-r2-2026-11-18/probe-job.log). The job was deleted afterwards; `az containerapp job list` shows no job with `114` in its name. No credential, token or private record is recorded.

## Observations

| Check | Result |
| --- | --- |
| Live store class and audit chain | `MssqlStore`; 1,610 audit entries; chain intact; one year (2026) holding 1,610 entries |
| Edit one live entry (copy) | Detected at entry 806, the edited entry: `content does not match its hash` |
| Delete one entry (copy) | Detected at entry 806: `previous hash does not match the entry before it` |
| Swap two entries (copy) | Detected at entry 806: same reason |
| Truncate last 5 entries against a head digest (copy) | Detected: `chain is shorter than the digest` |
| Re-hash a rewritten tail entry (copy) | Chain alone stays intact; against the head digest detected as `chain differs from the digest`, so an external digest is required for tail rewrites |
| Two-year chain of 200 live-shaped entries, 2025 sealed | Intact with the 2025 digest sealed; editing a 2025 entry gives `content does not match its hash` in 2025 only |
| `verify_ledger_before_reliance` on the deployed image | Not present (`has_reliance: false`); the orchestrator image also predates it |
| Native `sp_verify_database_ledger` and `sys.database_ledger_blocks` | Permission denied: `VIEW LEDGER CONTENT` is not held by the identity; not granted (would change a database control) |
| Ledger tables | 64 in `retrofit` (`sys.tables` where `ledger_type <> 0`) |

Local re-run on this branch: `PYTHONPATH=src:tests python3 -m unittest tests.test_recovery tests.test_sqlstore tests.test_ledger_digest_blob` from `src/core` ran 62 tests, OK. The digest container comparison (`digests: 0` in the probe because the job's local digest directory was empty) is covered by [digest-verification-alert-live-2026-11-18.md](./digest-verification-alert-live-2026-11-18.md), not by this run.

## Per-criterion status

| # | Criterion | Status | Evidence or reason |
| --- | --- | --- | --- |
| 1 | Per-year audit and ledger digest verification proven by test before reliance | Proven by tests and on live-shaped data; not proven on the deployed image | 62 local tests pass; live probe shows per-year verification, sealed-year tamper detection and chain tamper detection. The deployed image lacks `verify_ledger_before_reliance`, and live data holds one year, so real yearly sealing of live data did not run. Rolling the image is a deployment change and was not done |
| 2 | Measured load, latency and cost recorded against PRD targets | Proven at demo scale | Earlier note: 30-minute run, all four p95 limits met, cost estimate below USD 0.15; limits recorded there (443 cases, no 500-row import preview or bulk edit) |
| 3 | Backup, restore and deletion re-application tested (DH-005) | Proven at demo scale for point-in-time restore of a throwaway copy and deletion re-application | Earlier note and [issue-145-live-pitr-restore-evidence-2026-11-18.md](./issue-145-live-pitr-restore-evidence-2026-11-18.md) (restore of `retrofit` itself, hash-chain match). Not proven: native ledger verification after restore (permission), geo-restore (local redundancy), production-scale timing |

## Residual items

* Roll the demo API image to main, then run `verify_ledger_before_reliance` with sealing on a database with more than one year of data.
* Grant `VIEW LEDGER CONTENT` to a verifying identity (owner decision) so the native check can run.
* Tamper tests here are in-memory on live entries; a tamper attempt against the real ledger table is blocked by the append-only ledger and was not tried.

## Evidence limits

* The probe output is the retained log; row counts depend on the live demo, which keeps writing.
* Costs are estimates, not billing.

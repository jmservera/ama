---
title: Azure SQL Ledger Load, Restore and Deletion Evidence (Demo)
description: Live evidence for issue 114 on the synthetic desktop demo, run 2026-11-18 under owner authorisation
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

Scope: the synthetic demo only (desktop, 443 synthetic cases), resource group `ama`, app `ca-cutover-test-demo-api`, database `retrofit` on `sql-cutover-test-rzsrg` (Standard S0, 10 DTU, local backup redundancy). Owner decisions of 2026-11-18 authorise live Azure use (cap USD 700, no drills of production, no Key Vault rotation). This is demo evidence, not production reliance. Raw files are in [sql-ledger-live-2026-11-18/](./sql-ledger-live-2026-11-18/). Sign-in used the supplied test account through Playwright (screenshot [workbench-after-signin.png](./sql-ledger-live-2026-11-18/workbench-after-signin.png)); the session cookie was held in a temporary file that was deleted. No credential appears in any artifact.

## Per-criterion result

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1 Per-year audit and ledger digest verification proven by test | Proven by tests on main; not exercised on the deployed image | 62 tests pass (`test_recovery`, `test_sqlstore`, `test_ledger_digest_blob`): per-year verification, sealed digests, tampered and dropped years, pre-reliance gate, MssqlStore inheritance. Live `/api/audit-check` is intact (1,475 entries after the load). The deployed image's `MssqlStore` has no `verify_ledger_before_reliance` (job failed with `AttributeError`), and the live data holds one year, so yearly sealing was not run live. |
| 2 Measured load, latency and cost against PRD targets | Proven at demo scale | below |
| 3 Backup, restore and deletion re-application (DH-005) | Proven for point-in-time restore on the same server | below |

## Criterion 2: load, latency and cost

Method: [live_load.py](./sql-ledger-live-2026-11-18/live_load.py), five concurrent sessions (two also write), 60 s warm-up excluded, 1,800 s window 2026-11-18 07:35:04Z to 08:05:05Z, session mix of case list (50 rows), case detail, dashboard (`/api/progress`) and a call-log write. Result: [live-load-30min.json](./sql-ledger-live-2026-11-18/live-load-30min.json).

| Class | Samples | Errors | p50 s | p95 s | max s | PRD p95 limit s |
| --- | --- | --- | --- | --- | --- | --- |
| list | 6,343 | 0 | 0.174 | 0.276 | 3.69 | 1 |
| detail | 6,344 | 0 | 0.076 | 0.170 | 5.00 | 1 |
| dashboard | 1,269 | 0 | 0.115 | 0.187 | 2.26 | 3 |
| write | 414 | 0 | 0.229 | 0.345 | 3.07 | 2 |

Limits (NFR-002): the run covers the five-session, two-writer, 30-minute shape and the list, detail, dashboard and write limits. It excludes the 500-row import preview (10 s limit) and the 25-case bulk edit, and it ran on 443 cases, not the 60,000-home scale of the offline load check. Maximum single requests exceeded the p95 limits (cold connections and a concurrent database copy); only p95 is the PRD measure. Database DTU averaged 27 to 46 percent per five-minute bucket with two 100 percent peaks at 07:45 and 08:00 ([sql-metrics-load.txt](./sql-ledger-live-2026-11-18/sql-metrics-load.txt)); another worker was restoring a database on the same server at that time, so the peaks are not attributable to this run alone. The app held one replica at about 0.16 vCPU peak.

Cost (estimate, not billing; owner waived billing reconciliation): public retail prices retrieved 2026-11-18 for UK South. S0 is USD 0.605 per day, so the 30-minute window is about USD 0.013. Container Apps active rates are USD 0.000034 per vCPU-second, USD 0.000004 per GiB-second and USD 0.40 per million requests; the upper bound for 0.5 vCPU and 1 GiB for 1,800 s is about USD 0.038 plus USD 0.006 for 14,370 requests. The window therefore costs at most about USD 0.06. The drill databases added about USD 0.07 (two S0 databases, about 2.5 database-hours in total). Total session cost is below USD 0.15 against the USD 700 cap. The run wrote about 414 synthetic call-log rows to the demo ledger.

## Criterion 3: backup, restore and deletion re-application (DH-005)

Method ([drill.py](./sql-ledger-live-2026-11-18/drill.py), run as throwaway Container Apps jobs in the demo environment using the existing API identity and image):

1. `az sql db copy` of `retrofit` to `drill114src` (07:37Z); first restore point appeared 08:07Z.
2. T0 = 08:08:52Z. At 08:09:29Z the erase step wrote the register entry to a throwaway blob container (`drill114`, outside the database) and redacted synthetic case `ZF-2025-0001`: ledger 602 entries, head `c732de95...` before; 603 entries after ([drill-erase-job.log](./sql-ledger-live-2026-11-18/drill-erase-job.log)).
3. `az sql db restore --time 2026-11-18T08:08:52Z` into `drill114restored` completed at about 09:04Z (about 55 minutes, shared server).
4. Restore job output ([drill-restored-job.log](./sql-ledger-live-2026-11-18/drill-restored-job.log)): the restored case was not erased and the ledger was at 602 entries with the same head `c732de95...` (the database really rewound); the register still held 1 entry (it lives outside the database); `reapply_deletions` returned `ZF-2025-0001`; afterwards the case was erased, the ledger was intact at 603 entries and an `erasure_reapplied` audit entry exists.
5. Cleanup: both throwaway databases, the three jobs and the blob container were deleted and verified absent; `retrofit` was never changed by the drill.

Limits: Azure SQL point-in-time restore cannot target another server, so the "throwaway server" form is not possible; the throwaway is a database on the same server, restored from the throwaway copy and not from `retrofit`'s own backups. Backup redundancy is local, so no geo-restore. A restore of `retrofit` itself was not run. The final per-year reliance step of the restore job failed on the deployed image as noted under criterion 1.

## Residual items

* Roll the demo image to main so `MssqlStore.verify_ledger_before_reliance` exists, then run yearly sealing against a database with more than one year of data.
* A credential-file line was printed to the agent session once by mistake while checking file shape. The value is in no repository artifact; rotation is an owner decision (none authorised here).

## Evidence limits

* `sql-metrics-load.txt` has an unlabelled trailing line, and its `cpu_percent` block is identical to the DTU block; do not read it as an independent CPU measurement.
* The "about 0.16 vCPU peak" figure, the "62 tests pass" result and the "verified absent" deletion check have no retained raw output; treat them as unverified observations.
* An `az sql db copy` of `retrofit` started at 07:37Z, inside the 07:35Z to 08:05Z load window, and is a confounder on the maximum latencies.
* The p95 results hold at demo scale (443 cases) only.

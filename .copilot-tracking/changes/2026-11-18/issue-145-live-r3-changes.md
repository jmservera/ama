---
title: Issue 145 live run 3 changes
ms.date: 2026-11-18
---

Refs #145. No `src` change; focused tier (documentation and live evidence). `rpi-checks.py --all` not run.

## Live actions (resource group `ama`)

* One PITR restore to a throwaway database and one throwaway job; both deleted 2026-11-18T12:31Z and confirmed absent. Source read-only; no Key Vault action; no state JSON of earlier runs changed; no credential printed.

## Files

* `docs/reference/research/issue-145-live-run3-pitr-rerun-2026-11-18.md` (note), `docs/reference/research/issue-145-live-r3-raw-probe-2026-11-18.txt` (redacted raw output)
* `docs/reference/README.md`, `docs/reference/log.md`; r3 state file and phase artifacts.

## Per-criterion proven/unproven

| # | Criterion | Status |
| --- | --- | --- |
| 1 | SKU, auto-pause, redundancy parameters | Ticked on the issue |
| 2 | PITR performed, ledger verification recorded | Proven for the demo; native verify denied (`VIEW LEDGER CONTENT`), application chain intact |
| 3 | RTO and RPO | Ticked on the issue; second observation added |
| 4 | Backup redundancy and retention match #121 | Unproven: no approved decision (#1906) |
| R1 | Backup restored with document and audit state | Partly proven (SQL only) |
| R2 | Reconcile; reapply tombstones and holds | Partly proven |
| R3 | No resurrection | Unproven (empty tables, no re-apply mechanism) |
| R4 | DPO approvals | Not needed for the demo |
| R5 | Independent witness | Unproven |
| R6 | Disposable restrictions | Proven |
| R7 | Lower-tier labelled | Proven |
| R8 | Publish only hashes, counts | Proven |

## Validation

Documentation link and diff review; raw file scanned for server, subscription and identity names (none); Azure cleanup listing.

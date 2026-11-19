---
title: Issue 145 live PITR changes
ms.date: 2026-11-18
---

# Changes

* Added `docs/reference/research/issue-145-live-pitr-restore-evidence-2026-11-18.md`; indexed in `docs/reference/README.md`; appended to `docs/reference/log.md`.
* No `src/` change. Validation tier FOCUSED (documentation plus live evidence). `rpi-checks.py --all` not run; mypy, ruff and unit tests not applicable (no executable change).
* Live actions (resource group `ama`): one PITR restore `retrofit-pitr145` (S0, Local), one throwaway job `job-145-pitr-probe`; both deleted 2026-11-18T09:33Z and confirmed absent. Source database read-only. #114 drill resources untouched. No secret read or printed.
* Divergence: first CLI restore call was interrupted at 27 minutes; server-side restore continued (a duplicate request returned `DatabaseNameInUse`). Native `sp_verify_database_ledger` denied (`VIEW LEDGER CONTENT`); not worked around.

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | SKU, auto-pause, redundancy parameters | Already ticked; not re-proven |
| 2 | PITR performed and ledger verification recorded | Proven (app hash chain, prefix hash match); native verify not run |
| 3 | RTO/RPO stated or undecided with owner | Already ticked; one observed duration (about 57 min) and RPO (1 s) added |
| 4 | Backup redundancy and retention match #121 | Unproven: #121 retention deferred to production (#1906) |
| R1 | Actual backup restored with document/audit state | Partly proven: SQL audit/ledger state; document blobs not restored |
| R2 | Reconcile counts, history, authority; reapply tombstones and holds | Partly proven: counts and audit prefix; no erasure or hold state in demo |
| R3 | No resurrection of revoked, suspended, erased or spent state | Unproven: relevant tables empty, result vacuous |
| R4 | DPO/record-owner approvals | Not needed for demo (owner decision, #1906) |
| R5 | Independent qualified witness | Unproven: production step |
| R6 | Disposable restrictions, authorised bounded Azure exercise | Proven |
| R7 | Lower-tier evidence labelled | Proven |
| R8 | Publish only hashes, status, counts | Proven |

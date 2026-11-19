---
title: Issue 145 live run 2 changes
ms.date: 2026-11-18
---

# Changes

* Added `docs/reference/research/issue-145-live-run2-reverification-2026-11-18.md`; indexed in `docs/reference/README.md`; appended to `docs/reference/log.md`.
* No `src/` change, so tier FOCUSED. `rpi-checks.py --all` not run; mypy, ruff and unit tests not applicable (no executable change). Checks run: relative-link existence and diff review.
* Azure actions: read-only calls only (list, show, policy show). No restore, no resource created, no secret read or printed, no Playwright proof (no web surface in scope).
* Divergence: a second live restore was deliberately not run (duplicate observation, "no drills" limit); the first run's restore evidence is cited and preserved. Earlier run artifacts (`issue-145-live-*.md`) are unchanged; the state file path is shared and was rewritten (history in git).

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | SKU, auto-pause, redundancy parameters | Ticked on the issue; not re-proven |
| 2 | PITR performed and ledger verification recorded | Proven for the demo (first run); native `sp_verify_database_ledger` denied, not worked around |
| 3 | RTO/RPO stated or undecided with owner | Ticked on the issue; observed 57 min and 1 s as evidence only |
| 4 | Backup redundancy and retention match #121 | Unproven: settings recorded (Local, 14 days, no LTR); #121 retention deferred to #1906 |
| R1 | Actual backup restored with document and audit state | Partly proven: SQL state; documents not restored (blob soft delete and versioning only) |
| R2 | Reconcile counts, history, authority; reapply tombstones and holds | Partly proven: counts, prefix, erasure re-application (#114); no hold state on demo |
| R3 | No resurrection of revoked, suspended, erased, spent state | Unproven: erased content proven by #114; release, suspension, allowance have no reconcile mechanism and are empty on the demo; needs a `src` change and FULL tier |
| R4 | DPO and record-owner approvals | Not needed for the demo (owner decision; #1906) |
| R5 | Independent qualified witness | Unproven: production step |
| R6 | Disposable restrictions, authorised bounded exercise | Proven |
| R7 | Lower-tier evidence labelled | Proven |
| R8 | Publish only hashes, status, counts | Proven |

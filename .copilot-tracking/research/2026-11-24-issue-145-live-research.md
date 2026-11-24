---
title: Issue 145 live research (2026-11-24)
description: RPI research record for issue 145 backup, restore and recovery proof.
ms.date: 2026-11-24
---

Refs #145. Scope: synthetic demo, desktop only, resource group `ama`. Owner decision 2026-11-18: no drills, no Key Vault rotation, no production change. Research disposition: `executed`. Planning Readiness: `Ready`.

## Read-only Azure evidence (2026-11-24T04:17Z)

| Setting | Value |
| --- | --- |
| Database `retrofit` | Standard, Online, zone redundancy false |
| Backup storage redundancy | Local (requested and current) |
| Earliest restore date | 2026-11-10T04:17Z |
| Short-term retention | 14 days, 12 hour differential |
| Long-term retention | weekly, monthly, yearly all `PT0S` |
| Databases on the server | `retrofit`, `master`; no throwaway restore copy |
| Dropped-database records | 5 (earlier restore copies, already deleted) |

Only `az sql ... show/list` ran. Nothing was created, changed or restored.

## Criteria

* C4 (redundancy and retention match #121): the #121 retention period and DPO position are deferred to production (#1906, owner decision 2026-11-18), so there is no approved decision to match. Unproven, production-only.
* R1, R2 (restore an actual backup, reconcile, reapply): proven earlier by the [2026-11-18 restore evidence](../../docs/reference/research/issue-145-live-pitr-restore-evidence-2026-11-18.md) and run 3. Not repeated: drills are not authorised.
* R4: waived for the demo. R5: needs an independent qualified person; unproven.
* R3 (restore must not resurrect revoked or suspended release, erased content or spent allowance): erasure is covered by `recovery.reapply_deletions`. Release changes are not.

## Defect found (R3, release resurrection)

`assistants.change_release` and the serving-attestation quarantine call `assistant_release.change`, which writes only to SQL (`assistant_releases.status`). A point-in-time restore to before a suspension returns the row to `active`, so dispatch admission would resume for a release a named human had suspended or revoked. `recovery.py` keeps a durable register outside SQL for erasure only, and `reapply_deletions` is the only reapply step. Evidence: `src/core/src/zava_forward/core/assistants.py` (`change_release`, attestation suspension) and `assistant_release.py` (`change`, `admission`).

Material-change revocations (`invalidate_changed`) are re-derived from bound versions on the next assessment, so they need no register. Spent allowance has no outside-SQL record either; a fix needs an owner-approved design, so it stays unproven.

## Fix direction

Reuse the erasure pattern: a write-once register entry in the document backend (case id `_release_changes`) holding release id, status and time only, written before the SQL change, plus `reapply_release_changes(db, now, store)` run after a restore. Revoked outranks suspended; a terminal release is left alone. This is source on a release-authority path, so the FULL tier applies by classification. This worker does not run `rpi-checks.py --all`; the coordinator runs gates.

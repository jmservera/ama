---
title: Issue 122 live research (demo)
ms.date: 2026-11-18
---

Refs #122. Synthetic demo, desktop only, live Azure in resource group `ama` authorised (cap USD 700, no drills, no Key Vault rotation, no production change).

## Opening findings

* Issue lists 3 ticked criteria and 8 RAI restart criteria; only the last (witnessed authorised drill) is unticked. Owner excluded drills.
* Live proof candidates: `GET /api/continuity` and `/api/continuity/export` (server.py), `/api/audit-check`, SQL PITR restore (#145 note, 2026-11-18), release and version reads.
* Disposition: Research executed; Planning Readiness Ready once live reads succeed.

## Live reads (2026-11-18, signed-in employee, read-only)

* `/api/continuity` 200: epoch 0, no suspensions, history_valid true. `/api/audit-check` 200: intact, 1582 entries.
* `/api/continuity/export` 200: format `zf-evidence-export/1`, complete true, ledger 1581 entries, registry 2026-10-15.1, versions.changes empty.
* Planning Readiness: Ready. Drill criterion excluded by owner; restore evidence reused from the #145 note (PITR run earlier the same day).

---
title: Issue 96 r15 export review-history details
description: Phase details for the paused export review-history increment
ms.date: 2026-11-05
---

## Phase 3 design (not started)

* `form_export.py`: add `history` to `BODY_KEYS`; set `history=deepcopy(report["history"])` in the body, in stored order, from the same authorized `_report` after the existing actor and evidence-availability preflight. No new reads, scans or writes. An unavailable-evidence error stays `Unavailable`; other service errors propagate.
* Status fields unchanged: Held, `reviewed` false, Not submitted, Not assessed, notices. The digest is a change detector, not a signature.
* Legacy copies lacking `history` are Invalid via the existing `KeyError` path. Never backfilled. README updated to define this and that history is working field review, not Finance pack approval.

## Tests (existing files, JSON and SQLite fixtures)

* Accept, correct, reject one field plus a sibling: exported history equals the working report history exactly, including rejected prior evidence; the sibling is unchanged; an empty history exports as an empty list.
* Repeated export is identical. A same-value new review event changes the input version and digest; the saved earlier copy is unchanged. A returned nested history object is a detached copy.
* Tamper, reorder, removal and a legacy history-less copy are Invalid, including a legacy copy whose digest was recomputed over the old keys.
* Existing freshness controls remain: a changed bound source affects only its dependent fields.
* Denied or foreign actor discloses no history; unavailable historical evidence returns Unavailable with no write.
* A before and after snapshot of case, holds, sources and audit state shows no mutation.

## Gate

Phase 3 requires a coordinator-consumed checkpoint covering parent head `0472fd5d5625bb610b5ac65ad177026953802830` and the Held export manifest contract, recorded in the cut-over evidence pack with the legacy compatibility disposition.

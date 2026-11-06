---
title: Research for exact-68 replacement preparation (issue 1204)
ms.date: 2026-11-06
---

Task: coordinator-exact68-replacement-prep-1204. Research disposition: executed (bounded, known targets). Planning Readiness: Ready. Mode automatic, tracking and storage only. Existing records stay byte-identical.

## Evidence read

* Retention policy `docs/reference/method/tracking-retention-policy.md`: removal needs an explicit finite selection, a full snapshot (tracked, untracked, ignored, opaque symlink identities) with readback and restore before any prune, no age or glob authority, and root approval.
* Finite manifest SHA-256 643fb9ad14b44cf3e3b4e32d481c5646d8ff1c45f5d4527b259748375b309047: 69 rows, 68 transcripts (288862 bytes) selected, `exit-codes.json` unselected.
* Root verification (session files `1204-1a2-root-preservation-verification-r2.json` and `1204-1a2-root-storage-consumption.md`, read as data, no commands imported): all 7571 members of the frozen 1a2a4182 snapshot verified, exact 68 restored with actual modes, 7503 protected blobs, C 68 exact, B 400 archive-exact, hygiene zero on 468 archived members. Removal not authorized.

## Findings

* The tracked lossless bundle C already holds the exact 68 members; it matches the approved manifest and the f6b2984d blobs.
* Qualifications to carry unchanged: B `h1204-r4/snapshot-out.json` archived 0 bytes versus later 3517 bytes (SHA-256 7639c765...); the r5 script wrote 0600 restores and checked inventory, not actual restored, modes; the four extra names of the earlier 396 scan are unknown; the first root parser attempt failed on the extra action column and was corrected.
* Any new tracked record changes the baseline, so a fresh full snapshot and restore proof is required for this new head before any removal.
* Full-range `git diff --check origin/main..HEAD` remains open until a later authorized replacement.

## Boundaries

No removal, normalization, suppression, gitattributes change, new model batch, third HVE run or upgraded profile claim. Heavy work stays with #188.

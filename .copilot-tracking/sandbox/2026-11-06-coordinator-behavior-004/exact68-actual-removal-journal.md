---
title: Actual exact-68 replacement journal and storage-proof qualification (issue 1204)
ms.date: 2026-11-06
---

This is a NEW record written after the guarded operation. The earlier pending journal (`exact68-pending-journal-and-restore-map.md`) is unchanged and was intent only.

## Actual operation

* Authorization: root, 2026-11-06, finite 68 paths from manifest SHA-256 643fb9ad14b44cf3e3b4e32d481c5646d8ff1c45f5d4527b259748375b309047, excluding `exit-codes.json`.
* Baseline: HEAD 4628e2d9cbe4f81b20dc3f21efb98090e4f25a22, tree ceeb0549019dab908a2a91bf5476faa5c596169b, ignored-clean, agent blob acefb44a4d254ede6d86413343127b763dec42cb.
* Script `/tmp/h1204-r8-remove.py` (SHA-256 9f293462278807bc0fcaec85a1f22e3687cb19950462bb3bff0dc8a6ea7a1ffc), external. Preflight asserted exact HEAD, ignored-clean status, inventory SHA 3b2af74f..., full current membership and hashes equal to the r7 snapshot, selection equal to the manifest and the committed pending journal, C bundle member hashes equal to the originals, regular type, mode and size for each path. Each path was then removed with a single `os.unlink`; no recursive, glob or forced removal.
* External journal: `~/.local/share/ama/tracking-archives/2026-11-06-issue1204-removal-journal-20261106T005314Z/` with `journal.jsonl` (206 lines: preflight, 68 pending, 68 unlinking, 68 removed, post-ok; SHA-256 7a32f731...2b7f) and `result.json` (SHA-256 c4f2e93b...aa7c). External, on a disposable VM, not durable.
* Restore source: archive `tracking-current.tar.gz` (SHA-256 d019f30c6967674c8400d028ccbec1347d7d1968ed2b34666219e4626c9dc214, external), the tracked bundle `raw-selected-68.tar.gz` (SHA-256 a250456ec1a6c40d0740087d0ff5721211ff961e639019524aa649916fbab9b4) and Git commit f6b2984d9dabc181ef784caadcf045bcbb69a24a. Original paths resolve to the bundle member of the same name; restore only into a new empty directory outside the checkout.

## Measured results

* Tracking files 7575 to 7507; logical bytes 90915306 to 90626444; removed 68 files, 288862 bytes.
* Post-removal: the 68 are absent; no other member added or changed; all 7507 remaining tracked blobs equal HEAD; `exit-codes.json` present; source blob unchanged; `git status` shows exactly 68 deletions and no other change.
* The 262 protected `/tmp/h1204` entries (mode, size, SHA-256) and the four backup refs equal the root pre-prune manifest (`1204-protected-external-before-prune.json`).
* Free disk changed by about +0.4 MB (31659360256 to 31659737088 bytes); this removes checkout duplicates only. Git history still holds the blobs, and the archives and bundles add storage.

## Qualifications retained

* Bundle B member `h1204-r4/snapshot-out.json` was archived 0 bytes; its later current external file is 3517 bytes (SHA-256 7639c7654eafc08bede37f2d4b41dadbc02a5ccc85e5fc01aad4beee93b5bcd3). B members match the archive manifest, not all current external versions.
* The r5 script compared inventory modes, not actual restored modes; root and the r7 script verified actual restored modes separately. The r5 claim stands corrected, not erased.
* The four extra names of the earlier 396-file scan remain unknown; the 468-member names-only hygiene scan fixes coverage, not that provenance, and is not certification.
* Behavior report 005 is limited text-emulated, proxy evidence; this storage work is not native-host, whole-profile or operational acceptance.

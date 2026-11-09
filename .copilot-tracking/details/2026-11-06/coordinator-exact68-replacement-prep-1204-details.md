---
title: Details for exact-68 replacement preparation (issue 1204)
ms.date: 2026-11-06
---

## Phase 1 details

* Journal and restore map: `.copilot-tracking/sandbox/2026-11-06-coordinator-behavior-004/exact68-pending-journal-and-restore-map.md`, generated from the tracked C manifest; all 68 rows `pending`, no removal entries.
* Original-path resolution: through the C bundle member of the same name or the f6b2984d9 Git blob; restore only into a new empty external directory with traversal and link refusal; never extract into the checkout.
* Locality: external archives are on a disposable VM; tracked bundles are durable candidate content, not published evidence.

## Phase 2 details

* New unique owner-only directory under `~/.local/share/ama/tracking-archives/`, exclusive create, stream-only.
* Inventory all of `.copilot-tracking` by lstat (types, modes, sizes, SHA-256, no link following); build archive; full member readback; restore the 68 into a new empty scratch and compare actual filesystem modes, hashes, f6b2984d blobs and current bytes; check every unselected tracked blob against HEAD (blob id from `git ls-files -s`), source blob, backup refs and `/tmp/h1204` listing; record head, tree and ignored-inclusive status before and after.
* Outputs and logs external only.

## Phase 3 (not authorized here)

Replacement of the exact 68 with a bundle reference, then final 97-unit repeat, range `git diff --check`, and dedicated Review, each only after root authorization.

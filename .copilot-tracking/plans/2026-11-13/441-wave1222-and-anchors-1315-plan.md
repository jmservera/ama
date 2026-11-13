---
title: 441 Wave-1222 and doc anchors plan
ms.date: 2026-11-13
---

## Plan

* [ ] P1 Repoint PRD:609 and addendum:1510 to `../capstone/history/storage-map-before-reorganization.md#agents-in-the-retrofit-process-2026-10-13` (addendum: `./capstone/history/...`). No ms.date or status change.
* [ ] P2 Octopus or sequential `git merge --no-ff --no-edit` of the 7 child commits; verify 48 blobs byte-identical to child commits.
* [ ] P3 Fix `workspace-fix` to `whitespace-fix` at evidence pack line 8204.
* [ ] P4 Append the Wave-1222 section (7 rows, adverse results kept) to the evidence pack; add index row to reference README; append log entry.
* [ ] P5 Validate: link/anchor check, ASCII check on added text, `git diff --check`. Independent code-review, commit.

Details: see plan; docs-only, no behavioral code so no RED test; Python venv checks are not applicable.

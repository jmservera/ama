---
title: Issue 1231 r19 plan, merge parent79 47de325d
description: Prospective plan for one normal local merge of parent79 47de325d into the child
ms.date: 2026-11-07
---

Details: `.copilot-tracking/details/2026-11-07/issue-1231-r19-parent47de-details.md`. Critique: `.copilot-tracking/challenges/2026-11-07/issue-1231-r19-parent47de-critique.md`.

* [ ] Phase 1: re-verify identities, create `backup/issue-1231-cfc78-pre-r19-merge`.
* [ ] Phase 2: one `git merge --no-ff` of 47de325d; abort only it on conflict.
* [ ] Phase 3: prove parents, incoming raw/mode/blob delta, child blobs unchanged, log additions only.
* [ ] Phase 4: light selectors and static checks, own-source origins, unmasked exits, scratch /mnt/ama-gates/g1231-parent47de-preparation-1107.
* [ ] Phase 5: records, commit, freeze.

Exclusions: FULL, SQL, browser, scanners, images, heavy lock, push, PR update, ticks, parent/main mutation, cleanup.
Follow-up: combined child FULL on exact head and current main, independent review, hosted checks, new parent integration FULL.

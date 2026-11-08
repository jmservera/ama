---
title: Issue 1231 r20 plan, merge parent79 0a8ecd50
description: Prospective plan for one normal local merge of parent79 0a8ecd50 into the child
ms.date: 2026-11-07
---

Details: `.copilot-tracking/details/2026-11-07/issue-1231-r20-parent0a8-details.md`. Critique: `.copilot-tracking/challenges/2026-11-07/issue-1231-r20-parent0a8-critique.md`.

* [ ] Phase 1: re-verify identities; create `backup/issue-1231-120bb-pre-r20-merge`.
* [ ] Phase 2: one `git merge --no-ff` of 0a8ecd50; abort only it on conflict.
* [ ] Phase 3: prove parents, incoming raw/mode/blob delta, child ranking blobs unchanged, log additions only.
* [ ] Phase 4: light checks, own-source origins, per-command .out/.err/.exit files in /mnt/ama-gates/g1231-parent0a8-preparation-1107.
* [ ] Phase 5: records, commit, freeze.

Exclusions: FULL, SQL, browser, Docker, scanners, lock wait, cloud, push, PR update, ticks, parent/main mutation, cleanup.
Follow-up: sole FULL with --lock-timeout 0 on exact head, independent review, hosted checks, new parent integration FULL.

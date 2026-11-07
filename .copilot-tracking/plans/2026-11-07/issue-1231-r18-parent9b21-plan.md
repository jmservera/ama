---
title: Issue 1231 r18 plan, merge parent79 9b21a6a0
description: Prospective plan for one normal local merge of pinned parent79 9b21a6a0 into the child
ms.date: 2026-11-07
---

Research: `.copilot-tracking/research/2026-11-07/issue-1231-r18-parent9b21-research.md`. Details: `.copilot-tracking/details/2026-11-07/issue-1231-r18-parent9b21-details.md`. Critique: `.copilot-tracking/challenges/2026-11-07/issue-1231-r18-parent9b21-critique.md`.

* [ ] Phase 1: Re-verify child 201f2612, parent 9b21a6a0 and clean status; create `backup/issue-1231-201f2-pre-r18-merge` (refuse if it exists). Stop on drift.
* [ ] Phase 2: Recompute dry-run on the planning head; one normal `git merge --no-ff` of 9b21a6a0; abort only this merge on conflict.
* [ ] Phase 3: Prove parents, complete incoming raw/mode/blob delta, child blobs unchanged, log additions only.
* [ ] Phase 4: Run r17 selectors and strict static checks with PYTHONDONTWRITEBYTECODE=1, own-source origins, scratch `/mnt/ama-gates/g1231-parent9b21-preparation-1107`, unmasked exits.
* [ ] Phase 5: Regression only for a demonstrated gap; never weaken tests.
* [ ] Phase 6: Changes, one author Review, state; commit and freeze.

Exclusions: FULL, SQL, browser, scanners, images, provider, push, PR update, ticks, parent/main mutation, cleanup, shared lock.

Follow-Up Items: combined child FULL against the then-current main, independent exact-head review, hosted checks, new parent integration FULL.

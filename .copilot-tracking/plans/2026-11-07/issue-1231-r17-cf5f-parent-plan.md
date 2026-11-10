---
title: Issue 1231 r17 plan, merge parent79 cf5f57a00
description: Prospective plan for one normal local merge of pinned parent79 cf5f57a00 into the child
ms.date: 2026-11-07
---

Research: `.copilot-tracking/research/2026-11-07/issue-1231-r17-cf5f-parent-research.md`. Details: `.copilot-tracking/details/2026-11-07/issue-1231-r17-cf5f-parent-details.md`. Critique: `.copilot-tracking/challenges/2026-11-07/issue-1231-r17-cf5f-parent-critique.md`.

## Objective

One normal `git merge --no-ff` of local cf5f57a00 into the planning head, preserving both ancestries, child source and tests, and the parent's append-only log. No new behaviour, no rebase, no force, no retarget.

## Phases

* [ ] Phase 1: Re-verify start 5f904c29, parent cf5f57a0 tree dd20fdc7, clean status, main 8af3aea6 ancestor. Create backup ref `backup/issue-1231-5f904-pre-r17-merge` (refuse if it exists). Stop on drift.
* [ ] Phase 2: Recompute the dry-run tree on the planning head; require a single line. Merge once; abort only this merge on a conflict and report.
* [ ] Phase 3: Prove parents (planning head, cf5f57a0), incoming raw and mode delta from 87c027a30 matches cf5f57a00 with records separated, child source/test blobs equal to 5f904c29, log.md additions only.
* [ ] Phase 4: Run the r16-derived selectors, Ruff, format, mypy and `git diff --check` with PYTHONDONTWRITEBYTECODE=1, own worktree import origin, new external scratch `/mnt/ama-gates/g1231-cf5f-preparation-1107`. Record exits, stdout/stderr, ran/skipped. pip only after a real missing-dependency failure; never uv.
* [ ] Phase 5: Add a regression only for a demonstrated interaction gap. Never weaken tests.
* [ ] Phase 6: Write changes, one author Review and state (YAML frontmatter), commit and freeze ignored-inclusive clean.

## Exclusions

No FULL, SQL, browser, scanner, image, provider, push, PR update, tick, parent or main mutation, cleanup or lock queue.

## Follow-Up Items

* New combined child FULL against current main, independent exact-head review, hosted checks; a new parent integration FULL before main.

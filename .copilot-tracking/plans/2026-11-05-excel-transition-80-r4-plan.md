---
title: Plan for issue 80 round 4
description: Ordinary merge of pinned main into the checklist CSV child
ms.date: 2026-11-05
---

## Phases

* [x] Phase 1: ordinary `git merge --no-ff` of `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` into the child; no rebase, amend or force.
* [x] Phase 2: light checks only: prove module paths, run the existing export selectors, ruff (no cache) and mypy with external caches, bytecode disabled.
* [x] Phase 3: r4 changes, review and state evidence; commit with the repository-local privacy-safe identity.

Details: [phase details](../details/2026-11-05-excel-transition-80-r4-details.md).

## Critique (one pass, direct)

Verdict: proceed. The delta does not touch child files, so the merge should be clean; both intents are kept by a merge commit. Any conflict stops the merge correction and is recorded, not resolved by guess. No application edit, no web edit, no UI change, so no web-guideline fetch is needed. FULL tier is unchanged: light preparation does not downgrade it, and no heavy gate is attempted while the lock is held. Compatible advice applied; nothing conflicts with confirmed decisions.

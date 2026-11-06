---
title: Issue 80 r14 plan, browser lint docstring correction
description: Plan to wrap the child_env docstring so the FULL browser lint passes
ms.date: 2026-11-06
---

* Research: [r14 research](../research/2026-11-06-excel-transition-80-r14-docstring-lint-research.md). Details: [r14 details](../details/2026-11-06-excel-transition-80-r14-docstring-lint-details.md).

## Phases

* [ ] Phase 1: edit the `child_env()` docstring in `src/api/checks/design_system_browser_check.py` only, as a two-line wrapped docstring of the same meaning.
* [ ] Phase 2: run the gate's recorded lint and format commands with the pinned Ruff 0.17.1 over the three browser-group files with cache disabled; confirm `git diff` touches that docstring only and production, other checks and tests are byte-identical.
* [ ] Phase 3: record changes, author Review, state, then commit in order (implementation, then records), fresh `gh api user` identity, no amend.

## Decisions and limits

* No test for a docstring. No browser, FULL, SQL, Docker or install. Parent ancestry preserved; no push, PR, rebase or retarget.
* One independent plan critique is not requested by the assignment for a one-line documentation change; the Review is author-only and labelled so.

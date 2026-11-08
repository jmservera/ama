---
title: Issue 1231 r28 plan, root stage-cleanup propagation
description: Plan for merging root bb7e044c and reconciling it with the child stage cleanup
ms.date: 2026-11-07
---

Research: `.copilot-tracking/research/2026-11-07/issue-1231-r28-root-stagecleanup-propagation-research.md`. Details: `.copilot-tracking/details/2026-11-07/issue-1231-r28-root-stagecleanup-propagation-details.md`.

* [ ] Phase 1: commit these prospective records; backup ref `backup/issue-1231-4ec4c-pre-r28-merge`.
* [ ] Phase 2: `git merge --no-ff bb7e044c`; resolve the four conflicts keeping the child helper; fix the stage name in adopted root tests.
* [ ] Phase 3: light checks with an own pip venv (no services): core ranking tests, API wiring, assistant release, Ruff check and format on src/core and src/api, mypy on src/core.
* [ ] Phase 4: prove preservation, write changes, one author Review and state; commit and freeze.

## Follow-Up Items

* One rebaseline of root and child on the eventual main, then a fresh FULL (all 17 groups, fresh images, real MSSQL with `MssqlUnleasedRevocation`), then independent exact-head assessment.
* #1258 and #1259 stay with their issues.

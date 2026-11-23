---
title: Issue 2008 live re-proof r3 research
ms.date: 2026-11-23
---

## Scope

Refs #2008. Four unticked criteria. Prior notes (r2, close-out) proved them on API revision 0000054. Azure CLI now shows `ca-cutover-test-demo-api--0000055` (100% traffic, Healthy) and `ca-resident-demo--0000027`, so a fresh proof is possible on the new revision.

## Findings

* Committed workbook `docs/reference/research/demo-workbook/demo-case-list.xlsx` with generator and walkthrough note (2026-11-18 note).
* Live proof script exists at `demo-workbook/evidence-2026-11-23-live/live_xlsx_import_check.py`; only the worktree path and output folder need changing.
* No source gap known; focused tier. No Azure change.

Research disposition: reused plus one live run. Planning Readiness: Ready.

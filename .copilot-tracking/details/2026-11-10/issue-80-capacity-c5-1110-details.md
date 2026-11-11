---
title: Issue 80 capacity C5 details
description: Phase details for the test stub alignment
ms.date: 2026-11-10
---

## Phase 1

* Replace `show = (...nodes) => app.replaceChildren(...nodes);` (test line 435 only) with `show = (...nodes) => app.replaceChildren(...nodes.flat().filter(n => n && n.nodeType));`, copying production `app.js` line 106 semantics.

## Phase 2

* From `src/api`, owned venv, `PYTHONPATH` core/tests, agents/tests, api/tests. Direct exits to evidence files, no pipes.
* Commands: single test; `tests.test_case_journey`; `tests.test_list_export_api`; static modules `test_workspace_paging test_workspace_scripts test_content_standard test_design_system test_ui_support`; `ruff check` and `ruff format --check` on the test file; `node --check` of `ops.js`.

## Phase 3

* One native review after the `implement-done` marker; handoff `handoff-80-c5-casejourney-1110.md`.

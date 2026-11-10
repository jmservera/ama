---
title: Issue 96 r14 plan, approval reference versus field issues
ms.date: 2026-11-05
---

Refs #96. Research: `.copilot-tracking/research/2026-11-05/issue-96-r14-approval-issue-research.md`. Written before any source or test edit.

* [x] Phase 1: add focused tests (JSON and SQLite) for a current-version reference to an Unknown field and to a schema-invalid accepted value; keep an unaffected-field Current control and a plain Held reference; confirm RED at the start head.
* [x] Phase 2: minimal change passing the report's issue field ids into the approval evaluator; GREEN.
* [x] Phase 3: form_dependencies, form_review, form_export, form_staging suites, ruff check/format, mypy with exit capture; commit locally.

No gate, SQL, browser, Docker or cloud work. FULL gate on the new head is owned by the coordinator.

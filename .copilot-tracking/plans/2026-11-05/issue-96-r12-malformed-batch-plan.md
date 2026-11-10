---
title: Issue 96 r12 plan, malformed batch visibility
ms.date: 2026-11-05
---

Refs #96. Research: `.copilot-tracking/research/2026-11-05/issue-96-r12-malformed-batch-research.md`. Written before any source or test edit.

* [x] Phase 1: add a regression to `src/core/tests/test_form_dependencies.py` on both stores (remove only the EPC batch `schema_digest` under the store lock); confirm it fails at the intake head; assert staging and ledger unchanged by the read.
* [x] Phase 2: minimal change in `_proposals` as described in the research; also keep a batch with a different present digest excluded.
* [x] Phase 3: run the form_dependencies, form_review, form_export and form_staging suites, ruff check/format and mypy with exit capture; commit.

Critique: executed none; the change is a three-line conditional with the independent review as external critique. Out of scope: heavy gate, browser, SQL, Docker, API/UI, policy, approvals, other files.

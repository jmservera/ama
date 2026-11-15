---
title: SQL Entra auditing Bicep plan (issue 143)
ms.date: 2026-11-14
---

## Plan

* [x] Add infra/tests/test_sql_entra_auditing_bicep.py with static contract tests (no Bicep change needed).
* [x] Validate with unittest, isolated ruff and mypy using /tmp caches.
* [x] Commit locally; no push or PR.

Critique: executed once; verdict compatible, no Bicep edits required because the module already conforms.

---
title: Issue 135 C5 plan
date: 2026-11-10
---

* [x] Phase 1: add the one `mssql_python` mypy override to `src/importer/pyproject.toml`, mirroring Core. No runtime change.
* [x] Phase 2: validate in the isolated venv (bare mypy, ruff check/format on changed files, unit tests) and in a driver-present venv (mypy, tests); confirm the previous failure by temporarily comparing against HEAD.
* [x] Phase 3: single Review, changes record, state, commit. No push.

Details: [details](../../details/2026-11-10/served-import-refusal-135-c5-details.md). Critique: [critique](../../reviews/plans/2026-11-10/served-import-refusal-135-c5-plan-critique.md).

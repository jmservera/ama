---
title: Plan for issue 80 round 6
description: Denial regression tests for the form-schema CSV
ms.date: 2026-11-05
---

## Phases

* [x] Phase 1: add one focused test in `src/api/tests/test_form_staging_api.py` for administrator, unknown-role and Finance-without-resident-rights callers of `GET /api/form-schemas.csv`.
* [x] Phase 2: run the four relevant API modules together, then Ruff check, format check and mypy with external caches and real exit codes.
* [x] Phase 3: write r6 changes and Review, then state; commit.

Details: [phase details](../details/2026-11-05-excel-transition-80-r6-denials-details.md).

## Critique (one pass, direct)

Verdict: proceed. Assertions are behavioural (status 403, body without catalogue, case or candidate text, store, cases and audit chain unchanged, AI chat patched to raise), so a bypass would fail. Roles come from the real store and login, not a mock of the guards. No admin exception, role grant or core policy change. If a test fails unexpectedly, record it and fix only a minimal guard within this scope. Compatible advice applied; nothing conflicts with confirmed decisions.

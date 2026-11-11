---
title: Issue 80 capacity C5 plan
description: Plan for the test-only stub alignment in test_case_journey
ms.date: 2026-11-10
---

## Objective

Make the test's `show` stub honour the production `show` contract so the valid `null` export children no longer crash the fixture. No app change.

## Phases

* [ ] Phase 1: edit `src/api/tests/test_case_journey.py` line 435 stub to filter `n && n.nodeType` after flattening.
* [ ] Phase 2: targeted checks: the failing test, the whole `tests.test_case_journey`, API list-export 11, static 60, Ruff check and format on the test file, Node syntax on ops.js (unchanged), mypy only if the test file is typed-checked by existing config.
* [ ] Phase 3: native review after implement-done, handoff, commit.

## Stop rules

* If the fix does not turn the test green or reveals a second distinct failure, stop and report; no C6 and no app edit.
* No assertion weakening; no app fallback.

---
title: Issue 153 proposal card formatting and type-check correction research
ms.date: 2026-11-12
task_id: 153-check-correction-1112
---

Continuation of candidate 8d244c3c3 (owner-approved one bounded correction, 2026-11-12). Main is now 5df20e63982165048b3496f7b2792238aaf79128; only `docs/reference/log.md` changed on both sides (append-only, possible trivial conflict, no rebase done).

Original adverse evidence preserved: `ruff format --check` failed on 2 of 3 touched Python files; mypy reported an unused `type: ignore[no-untyped-call]` at `tests/test_case_journey.py:560` because `App.__init__` (`server.py:90`) is unannotated; one axe-enabled browser run timed out at checker line 558 (exit 1) and one later identical probe passed (216 checks, 58 axe scans); cause of the timeout is unproven. Axe `incomplete` (manual contrast) results are not passes.

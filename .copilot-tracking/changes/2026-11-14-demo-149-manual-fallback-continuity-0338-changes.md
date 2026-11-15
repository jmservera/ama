---
title: Epic 149 manual fallback continuity changes
ms.date: 2026-11-14
---

Refs #149. Tier: Focused (test-only).

* Added `src/api/tests/test_epic149_manual_fallback_continuity.py` (10 tests: staff advance and checklist, AI-unavailable copy, server 503 manual routes, resident manual callback and rules fallback, no colour-only cues).
* Validation run from `src/api`: unittest 10 OK; `ruff check` and `ruff format --check` pass; `mypy` clean.
* Not run: full local gate, hosted CI, browser or assistive-technology checks. Not pushed.
* No divergences from plan.

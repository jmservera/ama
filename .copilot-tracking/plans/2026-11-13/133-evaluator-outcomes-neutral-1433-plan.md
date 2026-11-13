---
title: Issue 133 evaluator outcomes and neutral text plan
ms.date: 2026-11-13
---

## Plan

* [ ] Phase 1 RED: tests in `test_aftercare.py` (paraphrase rejection, neutral facts accepted), `test_aftercare_screen.py` (Outcomes column, 7 columns, static string scan).
* [ ] Phase 2: extend `neutral_text` in `aftercare.py` with a paraphrase regex list; keep `BANNED_PHRASES`.
* [ ] Phase 3: add Outcomes column in `aftercare.js` built from `row.concerns[].outcome` using `acLabel`; update caption.
* [ ] Phase 4: run targeted tests, ruff check, ruff format --check, mypy, scenario manifest.

Details: `.copilot-tracking/details/2026-11-13/133-evaluator-outcomes-neutral-1433-details.md`.

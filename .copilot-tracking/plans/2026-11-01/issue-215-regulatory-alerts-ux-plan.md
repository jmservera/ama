---
title: Issue 215 regulatory alerts UX plan
ms.date: 2026-11-01
---

## Plan

1. [x] Add `.regulatory textarea{overflow-x:hidden}` in `src/api/src/zava_forward/api/web/style.css`.
2. [x] Make `checks/regulatory_ux_check.py` fail on unresolved `color-contrast` incompletes when axe runs.
3. [x] Update `src/api/README.md` and `docs/reference/log.md`.
4. [x] Focused validation: 8 regulatory/accessibility unit modules, browser harness with axe, ruff check, ruff format check, mypy.
5. [x] Commit, push, PR with `Refs #215` naming unmet criteria 3 (manual AT) and 5.

## Critique (one pass)

Verdict: acceptable. The harness assertion could break CI where axe produces unrelated incompletes in future; it is scoped to `color-contrast` only, which is the intended regression guard. Overflow-x hidden does not affect vertical scrolling or wrapping.

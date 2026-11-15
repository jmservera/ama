---
title: Issue 215 regulatory UX accessibility audit research
description: Research for the bounded automated accessibility and plain-language evidence audit of issue 215
ms.date: 2026-11-13
---

## Scope

Audit the third unticked criterion of issue #215 (WCAG 2.2 AA: no colour-only status, keyboard operable, plain-language mode) by running the existing local checks, and record honest residuals. Criterion 5 (comprehension tested with staff) stays unmet.

## Evidence found

* `src/api/checks/regulatory_ux_check.py` drives Playwright/Chromium against a constructed local API; `--axe` needs the hash-pinned axe-core 4.10.3 (SHA-256 `880970c0...8bb`).
* `src/api/README.md` ("synthetic design-system CI step") gives the run recipe: `PYTHONPATH=tests:../core/tests:../agents/tests`, `python -m checks.regulatory_ux_check --axe ... --out ...`.
* Unit tests: `test_regulatory_ux_check.py`, `test_accessibility_baseline.py`, `test_content_standard.py` in `src/api/tests`.
* Playwright Chromium is already present in `~/.cache/ms-playwright`.

## Approach

* Venv `/tmp/venv-215-1953` with `pip install -e src/core -e src/agents -e src/api playwright`.
* Fetch axe-core 4.10.3 to an external directory and rely on the script's hash assertion.
* Record exact counts and axe results; state that automated checks do not establish assistive-technology or staff comprehension acceptance.

## Planning Readiness

Ready. Research disposition: executed.

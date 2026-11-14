---
title: Asset executive and board view WCAG changes (#226)
ms.date: 2026-11-14
---

## Changes

* `src/api/src/zava_forward/api/web/role-screens.js`: summary panel and table, textual state labels, section jump nav, focusable section headings.
* `src/api/tests/test_asset_exec_screen_wcag.py`: new conformance tests.

## Validation

* `unittest discover -s tests -p "test_asset*.py"`: 23 passed. `test_accessibility_baseline`: 13 passed.
* `-p "test_*screen*.py"`: 214 run; one error in `test_aftercare_screen` (import of `zava_forward.core.aftercare_intake`), present without these changes.
* mypy and ruff check and format clean in `src/api` using /tmp caches.
* Not run: `tools/rpi-checks.py --all`, browser harness, Docker (focused tier).

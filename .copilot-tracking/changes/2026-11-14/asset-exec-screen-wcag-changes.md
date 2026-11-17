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

## Cycle 1 correction

* `role-screens.js`: `assetPanel` removed; asset panels call `screenPanel("Title", { anchor: "asset-x" }, ...)`.
* `connected_home_browser_check.py`: "Summary in words" added to `EXCLUDED["asset-board"]`.
* `specialist_keyboard_browser_check.py`: "Summary in words" added to `EXPECTED_REGIONS["asset-board"]`.
* Validation in `src/api`: mypy, `ruff check`, `ruff format --check` clean; `test_connected_home_check`, `test_role_screens_conformance`, `test_accessibility_baseline`, `test_asset_exec_screen_wcag`: 46 passed (core/agents source on PYTHONPATH, as the installed package points at another checkout). Browser checks not run.

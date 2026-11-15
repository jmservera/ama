---
title: Changes - correction cycle 2 for alert chat accessibility (#215)
description: Adds the two test module names the review command requires
ms.date: 2026-11-14
ms.topic: reference
---

## Changes

* Rebased onto current `origin/main`; `docs/reference/log.md` earlier entries untouched.
* `src/api/tests/test_regulatory_ux_accessibility.py` and `src/api/tests/test_alert_chat_keyboard_provenance.py`: thin modules re-exporting the existing `test_regulatory_a11y_cues` and `test_home_chat_regulatory_keyboard_provenance` cases so the specified command runs without duplicating tests.

## Validation

* `ruff check`, `ruff format --check` and `mypy`: clean.
* `python3 src/api/checks/regulatory_ux_check.py`: PASS, 21 browser states (axe not supplied).
* The three named modules from `src/api`: 41 tests OK.

## Not done

No push, complete gate or hosted CI. #215 stays open.

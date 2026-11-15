---
title: Changes - #215 non-colour, keyboard and plain-language matrix
description: Test-only additions for the WCAG plain-language criterion
ms.date: 2026-11-14
ms.topic: reference
---

## Changes

* `src/api/tests/test_alert_chat_role_wcag_plain_matrix.py`: new, 25 static checks across role coverage, non-colour cues, plain-language toggle, doubt and no-source states, and live-region roles.
* `src/api/tests/test_alert_chat_accessibility.py`, `src/api/tests/test_alert_chat_keyboard_live.py`: thin re-export modules.
* No change to `chat-widget.js`, `chat.js`, `style.css`, workbench check scripts or `scenario-manifest.json`.

## Validation (Focused tier)

* API modules (matrix, accessibility, keyboard_live, accessibility_baseline): 62 tests OK.
* Core `test_scenario_manifest`, `test_needs_inventory`: 19 tests OK.
* `ruff check`, `ruff format --check`, `mypy`: clean.

## Not done

No browser check re-run (no web source changed), no push, hosted CI or complete gate. #215 stays open; `Refs #215`, stacked on `feat/demo-215-alert-chat-wcag-plain-2220`.

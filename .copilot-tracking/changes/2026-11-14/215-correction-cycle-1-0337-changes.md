---
title: Changes - correction cycle 1 for alert chat accessibility (#215)
description: Fixes for two independent review findings
ms.date: 2026-11-14
ms.topic: reference
---

## Changes

* `docs/reference/log.md`: blank line before the #215 entry, heading date corrected to 2026-11-14, entry now also documents the #1611 keyboard and provenance test.
* `src/api/checks/regulatory_ux_check.py`: adds `src/core/tests`, `src/core/src`, `src/agents/src`, `src/api/src` and `src/api/tests` to `sys.path` when missing so a direct run from the repository root works; `--out` is optional and defaults to a `tempfile.mkdtemp(prefix="reg-ux-check-")` directory, and the evidence path is printed.

## Validation

* `ruff check` and `ruff format --check` on the check script: clean.
* `python3 src/api/checks/regulatory_ux_check.py` from the repository root: PASS, 21 browser states (axe not supplied).
* From `src/api`: `test_regulatory_ux_check`, `test_accessibility_baseline`, `test_home_chat_regulatory_keyboard_provenance` and `test_regulatory_a11y_cues`: 49 tests OK. The requested names `test_regulatory_ux_accessibility` and `test_alert_chat_keyboard_provenance` do not exist; these are the existing equivalents.

## Not done

No push, complete gate or hosted CI. #215 stays open.

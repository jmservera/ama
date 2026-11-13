---
title: Issue 1530 C1 fix changes
description: Change record
ms.date: 2026-11-13
---

## Changes

* `app.js`: `#hz-aware-hint` now ends with `Example: Resident phoned the repairs desk at 09:15 on 13 Nov 2026.`
* `test_safety_panel_ux.py`: asserts `Example:` on `hz-note-hint`, `hz-source-hint` and `hz-aware-hint`.
* `case_view_ux_browser_check.py`: new `populated_safety_panel` (open referred and legacy hazards via route fixture) scans 1280, 390, 320 px and 200% browser zoom (640 px at device scale 2): two cards present, axe 0 violations, no horizontal overflow, no JavaScript errors.
* `src/api/README.md`: documents the added coverage.

## Divergences

* Plan critique PC-1 applied: real zoom state added. An extra state of 200% root text at 320 px was tried and removed: the site header brand link overflows by 3 px there (pre-existing, outside the safety panel). Routed as a follow-up.
* Manifest digest: `scenario-manifest.json` binds only `workbench_browser_check.py` (unchanged), so no digest edit was needed.

## Validation (venv /tmp/venv-1530c1-1713, playwright 1.64.0, ruff 0.17.1, mypy 2.4.0)

* Nine named unittest modules: 113 tests OK.
* `python -m checks.case_view_ux_browser_check --axe` (pinned axe 4.10.3): all PASS.
* `ruff check`, `ruff format --check`, `mypy`, `node --check app.js`: clean.

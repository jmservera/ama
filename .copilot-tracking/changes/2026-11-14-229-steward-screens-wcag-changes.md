---
title: Issue 229 steward and operator screens WCAG slice changes
ms.date: 2026-11-14
---

* `role-screens.js`: added `indicatorRows` and a "State at a glance" panel with written states for lineage freshness, ingestion quarantine, sensor feed health and AI tasks.
* Added `src/api/tests/test_data_steward_screen_wcag.py` (6 tests).
* Validation: new tests, `test_accessibility_baseline` and `test_data_operator_ai_state`, `test_data_operator_screen` pass; mypy, ruff check and ruff format --check clean in `src/api`. Tests ran with a transient PYTHONPATH because editable installs point at another checkout. Browser checks and hosted CI not run; nothing pushed.
* Open: server `/api/exceptions` does not supply `indicators`; keyboard behaviour is static and Node-rendered only. #229 criterion remains unproven (`Refs #229`).

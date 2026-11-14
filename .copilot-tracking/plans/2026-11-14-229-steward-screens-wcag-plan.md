---
title: Issue 229 steward and operator screens WCAG slice plan
ms.date: 2026-11-14
---

* Add a read-only "State at a glance" definition list to the exception register view: lineage freshness, ingestion quarantine, sensor feed health, AI task enabled or disabled.
* Every state is written text prefixed `State:`; absent or unrecognised values read `Unknown`, never healthy. Optional `indicators` contract field; no mutating controls.
* No new `role=status`, no `aria-invalid`; use `dl` so existing table-row tests are unaffected.
* Add `src/api/tests/test_data_steward_screen_wcag.py`; run it with `test_accessibility_baseline` and `test_data_operator_ai_state`; mypy and ruff with /tmp caches in `src/api`.
* Critique (single pass, self): compatible; server does not yet emit `indicators`, so states show Unknown until it does (follow-up).

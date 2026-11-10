---
title: Issue 130 nomination read-only view changes
description: Changes record for the read-only nomination section (issue 130)
ms.date: 2026-11-10
---

## Status

Implementation complete. Single critique already run; Review follows.

## Files changed

* `src/api/src/zava_forward/api/web/panels.js`: new `nominationPanel(c)` (read-only; original and corrected account, source, owner, next update, acknowledgement "Delivery unverified", identity/support/risk with Unknown fallback, current/stale review, missing fields, authorised-empty state).
* `src/api/src/zava_forward/api/web/app.js`: Resident tab composition adds `nominationPanel(c)`.
* `src/api/src/zava_forward/api/web/style.css`: small `.nominations` rules.
* `src/api/tests/test_nomination_screen.py`: node renderer tests (5).
* `src/api/checks/nomination_browser_check.py`: Playwright loopback check.

## Divergences from the plan

* `style.css` was edited; the plan listed two source files. Layout rules only (wrapping, 44px summary, narrow stacking).
* `unknown()` helper also joins arrays so server lists render as text.
* Browser check fixes during normal implementation: record/review/correct actions needed `case_id`; the `Record supplied challenge` text assertion was replaced by `#affected-challenges` attached; the empty-state scan was dropped because the shared target-size helper requires interactive controls, so the empty state is asserted by text only.

## Validation (focused tier)

* `node --check` panels.js, app.js: exit 0.
* Nomination browser check (under `flock -n /tmp/ama-rpi-heavy.lock`): passed, axe 4.10.3, no violations, no non-GET requests while viewing, denied roles see nothing.
* Existing `challenge_browser_check.py`: exit 0.
* API unittest (resident_api, nomination_screen, content_standard, accessibility_baseline, design_system, static_assets, case_journey, resident_service_screen, finance_exposure_screen, error_logging, browser_asset_urls): 120 tests OK, 1 skipped.
* Core `test_resident_decisions`: 371 OK, 132 skipped.
* `ruff check` and `ruff format --check` on new Python: clean. `mypy` from `src/api` over src, tests, checks: no issues in 215 files (API typing only; not Core typing).
* Backend untouched: `git diff --stat -- src/core` is empty; no API, store, schema or SQL change.
* Browser recipe manifest hash: not applicable; no registered manifest references the changed files.

## Limitations

Synthetic SQLite fixture; not SQL Server acceptance. Axe and keyboard automation only; no human assistive technology or WCAG acceptance.

# Changes: resident demo UX redesign, phase 1 (Refs #462)

Plan: [plan](../../plans/2026-11-04/resident-demo-ux-462-plan.md). Phase 1 only; Phase 2 is a separate PR.

## Added

* `src/core/src/zava_forward/core/resident_summary.py`: timeline, documents view, needed-from-you and the rules summary.
* `src/core/tests/test_resident_summary.py` (7 tests).
* `src/api/checks/resident_summary_browser_check.py`: loading-only sign-in, section order, sticky nav, summary consent and fallback, reflow, reduced motion.

## Modified

* `resident_showcase.py`: view adds `stage`, `timeline`, `documents`, `needed`, `summary`.
* Web `index.html`, `demo.css`, `demo.js`: icon-only `Account`, loading-only sign-in, sticky nav, reorganised sections, case summary with optional AI.
* `test_resident_demo_api.py`, `test_resident_demo_script.py` (loading and error-restore scenarios).
* `resident_account_check.py` (name `Account`, icon, 44px target, tooltip), `resident_assistant_browser_check.py` (new sign-in loading text).
* `src/api/README.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Divergences

* No route added, so `test_role_endpoint_inventory.py` is unchanged.
* `resident_demo_browser_check.py` needs live SQL env (`ZF_SQL_PORT`); not run.
* The AI-success summary path is not exercised in a browser (no model); only the rules fallback is.

## Validation

* ruff check, ruff format --check, mypy --cache-dir=/tmp/mypy-462ux: pass.
* Node script tests, resident API tests, core summary tests: pass.
* Browser checks pass: account, assistant, generated-answer, sensors, summary.

## Phase 2: sensors, forecast and stock link (branch feat/resident-demo-sensors-forecast)

* Added `resident_forecast.py` (deterministic 24-hour estimate, `is_stale`) and `test_resident_forecast.py`.
* `resident_showcase.py`: `showcase_view(row, now)` adds `sensors.stale` and `sensors.forecast`; `app.py` passes the app clock.
* `demo.js`/`demo.css`: section `Your home sensors and forecast`, stale badge, dashed forecast line with hollow squares, `Latest stored` divider, forecast table rows.
* `infra/sql/resident-showcase.sql`: one `@stock` expression, `COALESCE(home.stock_id, synthetic_stock_anchor_id)`, replacing five repeated uses. Source-text tests updated; T-SQL not compiled locally.
* `resident_sensors_browser_check.py`: forecast, stale, few-readings and 54-row table assertions.
* Docs: `src/api/README.md`, index and log.

Divergences: `resident_demo_browser_check.py` has no sensor seed and needs SQL, so it is unchanged. Live view apply, sensor tables and extending the backfill (ends 2026-09-30) are not done (Azure, owner-gated).

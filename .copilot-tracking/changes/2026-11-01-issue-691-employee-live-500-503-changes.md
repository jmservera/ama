# Issue 691 changes

Date: 2026-11-01. Plan: `.copilot-tracking/plans/2026-11-01-issue-691-employee-live-500-503-plan.md`.

## Changed

* `src/api/src/zava_forward/api/server.py`: `_send` logs a warning (method, path without query, status) for any status >= 500 and any non-200/304 `/vendor/` response.
* `src/api/src/zava_forward/api/web/chat.js`: `unavailableNote` gives plain wording for 403 (not available for your role) and 503 (not switched on in this environment); Application Administrator no longer requests `/api/assistants` or `/api/chat/regulatory/status`; law-alert 503 reads plainly.
* `src/api/tests/test_employee_live_responses.py`: 5 tests (leaflet GET/HEAD/`?v=`/304/48 concurrent, logging, wording via Node, admin guard).

## Validation (focused tier)

* New tests, `test_workspace_scripts`, `test_static_assets`, `test_chat_panel`, `test_regulatory_chat_api`: pass.
* `ruff check .` and `ruff format --check .` in `src/api`: clean. `mypy`: no new errors (36 pre-existing, missing playwright stubs).
* `test_browser_asset_urls` not run (playwright not installed locally); CI is the evidence.

## Divergences

Leaflet 500 cause is outside the app process (not reproducible; Log Analytics blocked by network perimeter); not claimed fixed.

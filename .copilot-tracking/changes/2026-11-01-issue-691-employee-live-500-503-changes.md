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

## Correction cycle 2026-11-01

* `server.py`: warning moved from `_send` to `send_response`; OPTIONS 501 on a vendor path is now logged (test added).
* `chat.js`: neutral wording for unconfirmed 403/503; role wording only via `roleDenied`; alert fallback shows the server message.
* `test_employee_live_responses.py`: wording tests updated; administrator test now executes the panels with stubs.
* Validation: `ruff check`, `ruff format --check` clean; mypy 9 errors, identical before and after (missing stubs); `test_employee_live_responses` passes; full api discover result recorded in the PR reply.

## Correction cycle 2 2026-11-01

* `server.py`: `send_response` tolerates missing `self.path`/`self.command` and unparseable targets.
* `test_employee_live_responses.py`: `test_malformed_request_lines_still_get_error_responses` sends raw 414, 400 and 501 requests.
* Validation: `ruff check`, `ruff format --check` clean; `mypy src` clean; targeted tests pass.

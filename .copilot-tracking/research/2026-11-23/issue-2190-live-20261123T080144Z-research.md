# Research: issue 2190 late_success race regression test (2026-11-23)

Task: issue-2190-live-20261123T080144Z. Research disposition: executed (code reading) and reused (earlier notes 2026-11-21, 22, 23).

## Findings

* The race: `late_success` in `src/api/checks/employee_chat_browser_check.py` snapshots the page after a route change. The list route (`#/`) reads facets then cases and writes `#workspace-status` ("Perspective: ...", app.js:1004) when the second read ends. `networkidle` can pass in the gap between the reads, so the baseline snapshot raced the render.
* The fix `settle_route` already exists. Its coverage is a recording-double test (`src/api/tests/test_employee_chat_settle.py`) and an AST ordering test (`tools/test_rpi_checks.py:310`). Neither executes a real browser, so neither shows that the wait closes the gap.
* Gap: no deterministic reproduction. Proposal: a Chromium test with a local page whose `#/` route writes the status 900 ms after the hash change, with no network activity (longer than the 500 ms networkidle window). Control: `networkidle` alone returns with the status unset (the race); `settle_route` returns with it set.
* Chromium launches in this environment (Playwright check OK).

## Planning Readiness

Ready.

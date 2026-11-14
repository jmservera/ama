# Research: Epic 149 role workbench heading hierarchy (demo-149-role-workbench-heading-hierarchy-0442)

* Date: 2026-11-14
* Branch: `test/demo-149-role-workbench-heading-hierarchy-0442` (stacked child of the Epic 149 landmark/skip-link branch)
* Issue link: `Refs #149`
* Research disposition: executed
* Planning Readiness: Ready

## Findings

* The API is a standard-library `ThreadingHTTPServer` (`src/api/src/zava_forward/api/server.py`); there is no `TestClient`. `/app` serves a shell and every role view is drawn client-side by `app.js`, `role-screens.js` and siblings, so a raw HTTP fetch cannot see headings, tables or buttons.
* Existing evidence in `tests/test_epic149_landmarks_skip_link_focus_order.py` covers static shell landmarks only. `tests/test_staff_intake_browser.py` shows the Playwright pattern (login via `context.request.post`).
* `tests/role_matrix_fixture.py` `MatrixServer` and `build()` seed one fictional user per staff role plus a contractor (password `zf-test`). Playwright 1.64 and Chromium are installed.
* `/api/me` returns `navigation` per role (9 to 13 views for staff, none beyond the fixed routes for the contractor). The `#/screens` page lists the specialist screens installed for the role.
* Probe of 8 roles x about 25 views (nav, case, handoff, simulator, import, coordinator, each specialist screen with and without a case):
  * Staff `#/` and `#/all` render `h2`/`h3` filter and briefing headings before the page `h1` (H1 not first). Recorded as a shrink-only gap.
  * No skipped levels after the first heading, no empty visible headings, every visible table has a caption and scoped `th`, no visible link or button without a name.
  * A hidden empty `h3` (map panel) and a hidden empty button exist; both are excluded as not rendered.

## Decision

Render in headless Chromium over the real local server; skip cleanly if Playwright or Chromium is absent. Record the list-page heading order as a gap rather than editing production UI (out of scope for a test-only focused change).

## Validation tier

Focused (test-only, no gate tooling, no UI change): unittest, `ruff check`, `ruff format --check`, `mypy` from `src/api`.

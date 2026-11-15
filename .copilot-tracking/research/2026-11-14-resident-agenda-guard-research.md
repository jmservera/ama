# Research: resident demo agenda guard (#1053, #462)

Date: 2026-11-14. Disposition: executed. Planning Readiness: Ready.

* Issue #1053: signed-in page invited synthetic callback booking while `/demo/agenda` returns 503 when no agenda is configured.
* `resident_demo/app.py` `view_for` already exposed `callbacks_available` (#1070) and demo.js hid the form. Gaps: no `agenda_available` key, and the lede gave no upfront notice when unconfigured.
* Tests: `test_resident_callbacks_page.py`, `test_resident_demo_api.py` pin the view key set.
* Environment note: the editable install points to the main checkout; tests for this worktree need `PYTHONPATH` set to the worktree `src/*/src` paths.

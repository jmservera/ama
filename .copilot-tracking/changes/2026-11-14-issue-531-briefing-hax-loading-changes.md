# Changes: issue 531 briefing loading and provenance

* `src/api/src/zava_forward/api/web/app.js`: section `aria-busy`, new loading/refresh status text, provenance `dl`, per-statement basis line.
* `src/api/src/zava_forward/api/web/style.css`: `.briefing-status` min-height, `.briefing-provenance` layout.
* `src/api/tests/test_briefing_loading_provenance.py`: four focused source-level tests.
* Validation: mypy, `ruff check .`, `ruff format --check .` pass. 50 listed unittests pass except `test_connected_home_check` discovery test, which fails identically on the base because the shell `PYTHONPATH` needed for imports leaks `core/tests`. Browser render not run.

## Cycle 1 correction (CI src-api failure on 183a00c36)

* `app.js` line 645: removed the unused `data-briefing-provenance` attribute and renamed class `briefing-provenance` to `briefing-basis` (JS and CSS); `test_content_standard.CopyAudit.test_no_internal_terms_in_web_copy` banned the word `provenance` in it. No test referenced the attribute.
* Review: single-line removal, no behaviour or accessibility impact (the audit also flags the class name, so it was renamed).

## Cycle 2 correction (independent review of 88b39e22c)

* High: `aria-busy` is no longer set on the `.briefing-section` box, which wraps `.briefing-status`; it stays on `.briefing-content` only, so the live region is not suppressed and `loading_briefing_browser_check.py` `!closest('[aria-busy=true]')` holds.
* High: loading status text now starts with `Reading case summaries...` (initial and refresh), keeping `workbench_browser_check.py` and `loading_briefing_browser_check.py` assertions valid.
* Tests: `test_briefing_loading_provenance.py` renamed to `test_briefing_hax_states.py` and updated for both invariants.
* Validation: targeted modules, `ruff check`, `ruff format --check`, `mypy` run in `src/api`; browser checks not run.

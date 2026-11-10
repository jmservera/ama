<!-- markdownlint-disable-file -->
# Changes: issue 230 native browser paging proof

* Status: IMPLEMENTED (initial, previously undelivered). Began as a prospective pending stub before implement-start; completed here.
* Plan: `.copilot-tracking/plans/2026-11-10-issue-230-paging-coverage-1110-plan.md`; details `.copilot-tracking/details/2026-11-10-issue-230-paging-coverage-1110-details.md`.

## Changes

* Added `src/api/checks/programme_paging_browser_check.py`: reuses the existing harness (`design_system_browser_check.main`) and a private checker-local 60-case synthetic fixture wrapper over `role_screens_fixtures.synthetic_data` (shared fixture file untouched). Programme Manager at 1280 and 320 px: real `/api/cases?view=all&limit=50&offset=N` pages (50 and 10), unique labels, page-local scope and total text, keyboard Previous/Next/filter, one constructed intercepted offset=50 GET failure (retained rows, filter status and selected home, visible recovery), retry to page 2, Reset, return to page 1, no writes, no case change, no page errors, no horizontal overflow, concrete module origins and served `role-screens.js` hash.
* Added a short manual entrypoint entry to `src/api/README.md`.

## Adverse history (preserved)

* Baseline passed: 24 Node/unit tests; story 230 browser run (62 PASS, axe skipped).
* Run 1 refused: heavy lock held by #231 (stopped, no queue).
* Runs 2 to 5 failed on initial-checker assertions: wrong "Connected view" text (actual "Selected home"), initial-load GET counted as Previous, off-screen `content-visibility:auto` giving empty `innerText` at 320 px. Fixed in the checker only.
* Run 6 refused: lock busy. Run 7 failed at 320 px (`all_inner_texts` empty, same cause). Run 8 passed (89 PASS); lint/type fixes then run 9 passed (89 PASS) on the final file. Logs: ROOT `phase230-paging-coverage-evidence-1110/`.

## Validation

* Final browser run 9: exit 0, 89 PASS; axe not run (no pinned axe used; this is not a pass for axe).
* Ruff 0.17.1 format and check clean; mypy 2.4.0 clean (from `src/api`).
* Node/unit controls: test_programme_screen 16, test_role_screens 8, test_workbench 5, test_queue_empty_state 7, core test_needs_inventory 11, all OK. Registered recipe `workbench_browser_check.py` untouched: recipe SHA N/A.
* No product, shared fixture, #231/#233 checker, schema, auth or consent change.

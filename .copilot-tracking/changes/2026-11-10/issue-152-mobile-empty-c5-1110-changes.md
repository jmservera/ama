<!-- markdownlint-disable-file -->

# Changes: issue-152-mobile-empty-c5-1110

Status: implementation complete at witness implement-done (this record was completed before that event).

## Source changes

* `src/api/checks/workbench_browser_check.py`: `EMPTY_UNCLIPPED_JS` plus a new failure "empty explanation is clipped vertically" in `own_queue_empty_failures` (own `scrollHeight > clientHeight + 1`, or an overflow-clipping ancestor below body whose box does not contain the element vertically; page scroll allowed). New `mutated_empty_failures` helper applies a constructed test-page mutation and restores the exact original `style` attribute in `finally`. `run_browser` keeps the display:none negative (now through the helper) and adds a `height:12px; overflow:hidden` negative at 320 px that must report the clipping message and then pass after restore. No other assertion, selector or timeout changed.
* `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`: recipe sha256 `f649f27e...` to `9a9755434d071d36f0c5eba479a627892ccccec2cb4042bb7743cf6a594ebfe4` (equals harness bytes). The literal digest was substituted with a one-line sed, a deviation from the manual-edit-tool preference, disclosed here; the diff is one line.
* `src/api/README.md`: correction paragraph (15 empty-queue and 6 populated-queue observations; clipping rejection; second negative). `docs/reference/log.md`: one appended entry. No index change.
* Not touched: app.js, CSS, API, Core logic, roles, accounts, data; C4 records.

## Red before / green after

* Red-before (original, 11:41:24Z, /tmp/c5-red.out/.err, exit 0): unchanged C4 observer on `height:12px; overflow:hidden` returned `[]` (clientHeight 32, scrollHeight 224).
* Green after, served harness from `src/api` `python -m checks.workbench_browser_check` (11:42:39Z, /tmp/c5-browser.out/.err): exit 0, 124 PASS, 0 FAIL, empty stderr; 21 role-width observations (15 empty-queue, 6 populated-queue); hidden negative `failures=['empty explanation is not visible']`; clipped negative `failures=['empty explanation is clipped vertically']`, with the helper passing after restore.

## Other checks (venv /tmp/ama-c4-venv; mypy 2.4.0, ruff 0.17.1, playwright 1.64.0)

* Core test_scenario_manifest, test_needs_inventory, test_generator_coverage (from src/core/tests): exit 0, 35 OK.
* API test_queue_empty_state, test_workbench, test_workbench_live_defaults, test_content_standard (PYTHONPATH=../core/tests:../agents/tests): exit 0, 37 OK.
* mypy (src/api project): exit 0, 217 files. ruff check: exit 0. ruff format --check: exit 0, 138 files.
* Node not run (app.js unchanged). Harness SHA-256 `9a9755434d071d36f0c5eba479a627892ccccec2cb4042bb7743cf6a594ebfe4`.

Limits: constructed mutations on constructed data, not a product defect; no device, assistive-technology or user evidence; not run: full or --changed gate, MSSQL, images, hosted CI, private data.

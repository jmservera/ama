<!-- markdownlint-disable-file -->

# Changes: issue-152-mobile-empty-c4-1110

Plan: .copilot-tracking/plans/2026-11-10/issue-152-mobile-empty-c4-1110-plan.md
Status: implementation complete (witness implement-done recorded when this file held only an opening stub; the content below was written immediately after, changes artifacts are not guarded). 

## Source changes

* `src/api/checks/workbench_browser_check.py`: added `EMPTY_WIDTHS` and `own_queue_empty_failures` (awaits the attached `li.empty`, then checks single visible element, assigned-queue sentence, "unknown", no "declared gap", positive size inside the viewport, no element overflow, no page overflow; nonempty queues must show none). `run_browser` now calls it per non-Contractor role at 320, 390 and 1280 px (1280 last, so later checks see the original viewport), and runs one constructed negative on the first empty-queue role. Existing assertions, selectors and timeouts are unchanged; the replaced block was the 1280-only empty check.
* Constructed negative: a test-page CSSOM mutation (`display:none` on `li.empty` at 320 px), removed immediately, then the helper must pass again. First attempt used an injected style tag, which the page CSP blocks (stderr preserved at /tmp/c4-browser.err, exit 1 on that first run); replaced by the CSSOM mutation. This is a constructed mutation on the test page, not a product bug; product and fixtures are untouched.
* `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`: `recipe` sha256 `56409ec2...` to `f649f27ee9787ab2a897b8d3f2b12e32e3435b86ee6ee27fb89a498b294ff6e7` (literal-byte digest checked by `scenario_manifest.py`).
* `src/api/README.md`: one paragraph for the narrow-width observation and its limits. `docs/reference/log.md`: one appended entry (appended with a shell command, not the edit tool). No index change.
* Not touched: app.js, CSS, API, Core logic, roles, accounts, data.

## Validation (Python 3.12.3, venv /tmp/ama-c4-venv, editable installs from this worktree; mypy 2.4.0, ruff 0.17.1, playwright 1.64.0, Chromium 156.0.8078.4)

| Check | Result |
|---|---|
| Import origins | zava_forward api/core/agents resolve under this worktree `src/*/src` |
| First served harness run | exit 1, 84 PASS then Playwright CSP error on the style-tag negative (own fault, fixed) |
| Final `python -m checks.workbench_browser_check` from src/api | exit 0, 123 PASS, empty stderr; 21 role-width empty checks (7 roles x 3 widths) and the negative PASS with `failures=['empty explanation is not visible']`. Logs /tmp/c4-browser2.out and .err |
| Core `test_scenario_manifest test_needs_inventory test_generator_coverage` (from src/core/tests) | exit 0, 35 tests OK |
| API `tests.test_queue_empty_state tests.test_workbench tests.test_workbench_live_defaults tests.test_content_standard` (PYTHONPATH=../core/tests:../agents/tests) | exit 0, 37 tests OK |
| `mypy` (strict, src/api project) | exit 0, no issues in 217 files |
| `ruff check .` in src/api | exit 0 |
| `ruff format --check .` in src/api | exit 0, 138 files formatted. The explicitly named harness file reports pre-existing reformat hunks at unrelated lines that the project config excludes; the same result occurs on the parent version, so not introduced here |
| Node | not run, app.js unchanged |

Harness SHA-256 `f649f27ee9787ab2a897b8d3f2b12e32e3435b86ee6ee27fb89a498b294ff6e7`.

Limits: constructed widths on constructed data only; no product defect was reproduced; not run: full or --changed gate, MSSQL, images, full API suite, employee browser, human devices, assistive technology, hosted CI. The existing failed API simulator fixture is outside scope and was not exercised.

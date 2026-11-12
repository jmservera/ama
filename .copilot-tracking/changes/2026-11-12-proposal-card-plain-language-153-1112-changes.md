---
title: Issue 153 proposal card plain-language default changes
ms.date: 2026-11-12
task_id: 153-proposal-card-1112
---

## Files changed

* `src/api/src/zava_forward/api/web/assistants.js`: one `details[data-proposal-technical]` ("Suggestion details (technical, for audit and support)") holding the unchanged snapshot and history JSON under labelled headings; `pre` blocks focusable and named; edit field relabelled "Edited proposal (technical JSON format)" with a note.
* `src/api/checks/assistants_browser_check.py`: coupled label updates; new `plain_default_card` regression (desktop and 360 px; 8 new checks).
* `src/api/tests/test_content_standard.py`: one static disclosure-structure test.
* `src/api/tests/test_case_journey.py`: label string only.
* `docs/reference/research/ux/content-standard.md`, `docs/reference/log.md`: documentation.

## Not changed

Server, API, permissions, approval logic, audit data, `ALLOWED` guard exemptions, CSS, dependencies.

## Amendments and divergences

* Plan did not anticipate that the editable install points at another checkout; browser and unit checks were run with explicit `PYTHONPATH` entries for this worktree. A first browser run therefore exercised stale code and failed on the old label; the rerun is the evidence. The first run and the Chromium "Socket path too long" failure from the long worktree cwd (run from `/tmp/zw` instead) are retained here, not hidden.

## Validation

* `test_content_standard`, `test_case_journey`, `test_assistants`, `test_browser_asset_urls`: 180 tests, OK, 58 skipped (existing opt-in/SQL Server skips).
* `assistants_browser_check.py`: 158 checks passed (150 before the new regression on baseline), including the 8 new checks. A logged "law store is not loaded" traceback during the run is existing log noise; the script exits with all checks passing.
* `ruff check` on three changed Python files passed. `ruff format --check` reports reformatting needed for 2 of the 3 files, identical to the base tree (pre-existing); not reformatted to avoid unrelated churn. `mypy tests/test_content_standard.py` clean.
* Not run: full gates, the unrelated suites, SQL Server, assistive-technology or human review.

<!-- markdownlint-disable-file -->
# Changes: issue #232 round 2

* `src/api/src/zava_forward/api/web/role-screens.js`: restored valid JavaScript (missing closing `}` and `});` after data-operator, contractor-job-pack, resident-choice and hazard-triage; `node --check` now passes, it failed on origin/main). Added `summarise`/`summary` to resident-choice and rendered it in the no-home-selected state: page-level table of measure choices (latest version and binding), paused or withdrawn measures, and update commitment (purpose, owner, due, safe route). Failed detail fetches show Unavailable. Read-only, no contact.
* `src/api/tests/test_resident_choice_screen.py`: new node-vm test for the summary.
* `src/api/checks/role_screens_browser_check.py`: scenario 232 asserts the summary region and no contact links.

Validation: tests for resident choice, role screens, design system, accessibility baseline, asset board, finance, procurement, static assets passed; ruff check, ruff format --check, mypy on touched files passed; local Chromium browser check for scenario 232 passed. axe scan not run (CI evidence).

## Correction cycle changes

* `role-screens.js`: queue paused or withdrawn column now lists state, version, scope binding and human-review requirement per measure; queue measure column separates the current answer from the latest recorded version.
* `test_resident_choice_screen.py`: updated queue expectations and added a test for the stale-scope and stop-followed-by-waiting fixtures.

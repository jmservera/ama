<!-- markdownlint-disable-file -->
# RPI Phase Details: Fix Issue 130 src-api CI Failures from Run 43694720253

## Metadata

* Task ID: nomination-api-routes-130-ci-fix
* Task slug: nomination-api-routes-130-ci-fix
* Related plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/nomination-api-routes-130-ci-fix-research.md (`C1`–`C8`, `W1`)

## Phase Index

| Phase ID | Name                                                                                      | Status   | Detail sections        |
|----------|-------------------------------------------------------------------------------------------|----------|------------------------|
| P01      | Fix `panels.js` Node slice guard and `test_nomination_api_routes.py` missing-Chromium skip | complete | P01, P01-T01, P01-T02  |
| P02      | Execute focused-tier validation across `src/api` and `src/core`                           | complete | P02, P02-T01           |

<!-- rpi:phase id=P01 -->
## P01: Fix `panels.js` Node slice guard and `test_nomination_api_routes.py` missing-Chromium skip

### Context

GitHub Actions run `43694720253` (`src-api` job `132752737563`) on `PR #1776` (`feat/ux-130-api-routes`, HEAD `2215209cb`) failed two tests during `python -m unittest discover -s tests -v` (`C1`):
1. `CaseJourney.test_raw_resident_and_challenge_outcomes_exclude_repeat_posts` in `src/api/tests/test_case_journey.py` extracts `"const formFor = " + source.split("  const formFor = ", 1)[1].split("  const staff", 1)[0]` from `src/api/src/zava_forward/api/web/panels.js` and runs it in Node without a `c` binding (`C2`). Commit `2215209cb` placed `const perms = c.nomination_permissions ...` and `const repRefs = ...` between `const formFor` and `const staff` inside `affectedChallengePanel` (`C3`).
2. `NominationApiRoutesTests.test_workbench_keyboard_operability_for_digital_and_non_digital_routes` in `src/api/tests/test_nomination_api_routes.py` called `pw.chromium.launch(headless=True)` during unit discovery before `.github/workflows/src-ci.yml` runs `python -m playwright install --with-deps chromium` (`C4`). Peer tests in `src/api/tests/test_workbench_live_defaults.py` and `src/api/tests/test_browser_asset_urls.py` catch `PlaywrightError` when `"Executable doesn't exist"` is present and skip cleanly (`C5`).

### Intent

Restore clean Node slice evaluation in `panels.js` and clean missing-Chromium skip behavior in `test_nomination_api_routes.py` while retaining full semantic, DOM, accessibility, and local Chromium keyboard coverage.

### Boundaries

* Included: Surgical edits to `affectedChallengePanel` in `src/api/src/zava_forward/api/web/panels.js` and Playwright/Chromium skip handling plus `1` regression test in `src/api/tests/test_nomination_api_routes.py`.
* Excluded: Modifying `src/api/tests/test_case_journey.py`, `.github/workflows/src-ci.yml`, `scenario-manifest.json`, or any API backend route handler; removing any existing test (`exact removals: none`).

### Likely Targets

* `src/api/src/zava_forward/api/web/panels.js`: Reorder `const staff` immediately after `const formFor` and guard `c` via `typeof c !== "undefined" && c` before reading `nomination_permissions` inside `affectedChallengePanel`.
* `src/api/tests/test_nomination_api_routes.py`: Align `_playwright_available()` and `pw.chromium.launch(headless=True)` `PlaywrightError` handling with peer `src/api/tests/` browser tests, and add `1` unit test covering the missing-Chromium skip branch.

### Dependencies

* None.

### Validation Expectations

* `CaseJourney` (`31` tests) and `NominationApiRoutesTests` (`9` tests including the new skip unit test) pass locally with `0` errors and `0` failures.

### Completion Evidence

* Clean diff in `src/api/src/zava_forward/api/web/panels.js` and `src/api/tests/test_nomination_api_routes.py` plus passing test output recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Reorder `staff` declaration and guard `c` in `affectedChallengePanel` (`panels.js`)

#### Context

Inside `affectedChallengePanel(c, id, refresh)` in `src/api/src/zava_forward/api/web/panels.js`, `test_case_journey.py` relies on `"  const staff"` immediately terminating the `"  const formFor = "` slice (`C2`, `C3`). In addition, guarding `typeof c !== "undefined" && c` when computing `perms` ensures no slice evaluation can ever throw `ReferenceError: c is not defined`, and every line in `panels.js` (including comments) is scanned by `test_content_standard.py` and `test_accessibility_baseline.py` (`C6`, `W1`).

#### Intent

Make `formFor` cleanly sliceable by `test_case_journey.py` and guard `c` defensively without altering runtime DOM output, `aria-invalid` counts (`9`), `table` counts (`14`), or plain-language copy.

#### Boundaries

* Included: Moving `const staff = (me.staff || []).filter(...)` immediately after `const formFor = ...` and changing `const perms = ...` to `const caseRecord = typeof c !== "undefined" && c ? c : null; const perms = caseRecord && caseRecord.nomination_permissions && typeof caseRecord.nomination_permissions === "object" ? caseRecord.nomination_permissions : null;` inside `affectedChallengePanel`.
* Excluded: Changing `nominationPanel._routeForm`, altering HTML elements/attributes, or adding comments containing banned words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`).

#### Likely Targets

* `src/api/src/zava_forward/api/web/panels.js`: `affectedChallengePanel` declaration block around `formFor`, `staff`, `perms`, and `repRefs`.

#### Dependencies

* None.

#### Validation Expectations

* Running `src/api/tests/test_case_journey.py` passes all `31` tests, including `test_raw_resident_and_challenge_outcomes_exclude_repeat_posts` across both `challenge === false` and `challenge === true` permutations.

#### Completion Evidence

* Zero `ReferenceError` and `OK` status from `test_case_journey.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Align missing-Chromium `PlaywrightError` skip and add skip unit test in `test_nomination_api_routes.py`

#### Context

In `src/api/tests/test_nomination_api_routes.py`, `_playwright_available()` checks whether `playwright` imports, which returns `True` in hosted `src-api` unit discovery before Chromium is installed (`C4`). Peer tests in `src/api/tests/test_workbench_live_defaults.py` and `src/api/tests/test_browser_asset_urls.py` use `importlib.util.find_spec("playwright") is not None` and catch `from playwright.sync_api import Error as PlaywrightError` around `chromium.launch(headless=True)`, calling `self.skipTest("Chromium is installed by the later browser-check step")` when `"Executable doesn't exist" in str(error)` and re-raising otherwise (`C5`).

#### Intent

Ensure `test_workbench_keyboard_operability_for_digital_and_non_digital_routes` skips cleanly when Chromium is absent in unit-test containers, runs completely when Chromium is installed, re-raises genuine browser launch errors, and has direct unit-test proof of the missing-binary skip behavior while all non-browser HTTP/HTML route/DOM assertions remain unconditional.

#### Boundaries

* Included: Updating `_playwright_available()` to `importlib.util.find_spec("playwright") is not None`, extracting or guarding Chromium launch via `_launch_headless_chromium(self, pw)` (catching `PlaywrightError` when `"Executable doesn't exist" in str(exc)` -> `self.skipTest("Chromium is installed by the later browser-check step")`), and adding `test_keyboard_operability_skips_when_chromium_executable_missing` using `unittest.mock` to verify `SkipTest` on missing executable and re-raise on non-missing `PlaywrightError`.
* Excluded: Weakening or skipping `test_accessible_html_route_fragment_labels_channels_and_live_status` or any HTTP API route test; editing `.github/workflows/src-ci.yml`.

#### Likely Targets

* `src/api/tests/test_nomination_api_routes.py`: `_playwright_available()`, `test_workbench_keyboard_operability_for_digital_and_non_digital_routes`, and `1` focused skip-contract test method on `NominationApiRoutesTests`.

#### Dependencies

* None.

#### Validation Expectations

* `NominationApiRoutesTests` executes all `9` tests locally (including live headless Chromium in `test_workbench_keyboard_operability_for_digital_and_non_digital_routes` and simulated missing-executable `SkipTest` in `test_keyboard_operability_skips_when_chromium_executable_missing`), and `ruff` + `mypy` report `0` issues on `test_nomination_api_routes.py`.

#### Completion Evidence

* Passing `unittest`, `ruff`, and `mypy` runs over `src/api/tests/test_nomination_api_routes.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Execute focused-tier validation across `src/api` and `src/core`

### Context

Owner validation rules classify this targeted two-file CI bugfix under the focused validation tier (`src/README.md` / `.github/copilot-instructions.md`): run all affected unit tests, static accessibility/content guards, `ruff`, `mypy`, and the caller-specified `scenario-manifest` / `needs_inventory` tests. Note that `test_case_journey.py` imports `tests.test_mvp`, which lives at `src/core/tests/test_mvp.py` (`src/core` parent directory provides the `tests` namespace when `src/core` is editable-installed or on `PYTHONPATH`).

### Intent

Confirm zero regressions across every requested and tightly coupled validation check before transitioning to `rpi-review` and local commit.

### Boundaries

* Included: Running `unittest` from `src/api` (matching `.github/workflows/src-ci.yml` working directory) and from repository root (including `src/core` on `PYTHONPATH` plus testing caller's exact command), `python3 -m ruff check src/api`, `(cd src/api && python3 -m ruff format --check .)`, `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`, and `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_scenario_manifest.py src/core/tests/test_needs_inventory.py -q`.
* Excluded: Running external cloud deployment or pushing to remote.

### Likely Targets

* Read-only verification across `src/api/` and `src/core/tests/`; evidence recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md`.

### Dependencies

* P01 (`P01-T01`, `P01-T02`).

### Validation Expectations

* All unit test commands print `OK` with `0` failures and `0` errors; `ruff check`, `ruff format --check`, and `mypy` exit `0`.

### Completion Evidence

* Exact commands, test counts, and exit codes recorded in `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run targeted `unittest`, `ruff`, `mypy`, and `scenario-manifest` validation commands

#### Context

Validates Caller Validation Requirements 1, 2, and 3 plus coupled Epic 149 and nomination screen suites (`C6`, `C7`).

#### Intent

Produce deterministic local proof that the hosted `src-api` failures from run `43694720253` are resolved without collateral regressions.

#### Boundaries

* Included:
  * `(cd src/api && PYTHONPATH=../core:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_case_journey.py tests/test_nomination_api_routes.py tests/test_nomination_screen.py tests/test_content_standard.py tests/test_accessibility_baseline.py tests/test_epic149_form_error_summary_associations.py -q)`
  * `PYTHONPATH=src/core:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_case_journey.py src/api/tests/test_nomination_api_routes.py src/api/tests/test_content_standard.py src/api/tests/test_accessibility_baseline.py -q`
  * `python3 -m ruff check src/api && (cd src/api && python3 -m ruff format --check .)`
  * `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`
  * `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_scenario_manifest.py src/core/tests/test_needs_inventory.py -q`
* Excluded: Modifying unrelated test suites or manifests.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md`: Record command execution and results during `rpi-implement`.

#### Dependencies

* P01-T01 and P01-T02.

#### Validation Expectations

* Every listed command exits `0`.

#### Completion Evidence

* Recorded command outputs and exit codes in the implementation changes artifact.

#### Unresolved Items

* None.

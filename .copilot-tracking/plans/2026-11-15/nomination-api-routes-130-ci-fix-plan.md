<!-- markdownlint-disable-file -->
# RPI Plan: Fix Issue 130 src-api CI Failures from Run 43694720253

## Task Metadata

* Task ID: nomination-api-routes-130-ci-fix
* Task slug: nomination-api-routes-130-ci-fix
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan-critique.md

## Executive Summary

This plan resolves the **two `src-api` CI failures** reported by GitHub Actions run `43694720253` on pull request `#1776` (commit `2215209cb`, Issue `#130` dual-route nomination and plain-language explanation routes). Fixing these two issues restores green unit-test execution in hosted `src-api` CI while preserving every route, DOM, plain-language content, accessibility baseline, and local headless-Chromium keyboard operability check.

### User Decisions and Requirements Highlights

* **Node slice safety in `panels.js`**: Guard `c` with `typeof c !== "undefined" && c` and restore the `formFor`-to-`staff` declaration boundary inside `affectedChallengePanel` in `src/api/src/zava_forward/api/web/panels.js` so `src/api/tests/test_case_journey.py` never throws `ReferenceError: c is not defined` during isolated Node slice evaluation.
* **Missing-Chromium unit-container skip alignment**: Align `src/api/tests/test_nomination_api_routes.py` with the established `src/api/tests/` browser-availability skip pattern when the Chromium binary is absent in the `src-api` unit-test step, while keeping HTTP/HTML route and DOM assertions unconditional and executing full Playwright keyboard checks whenever Chromium is installed.
* **Focused validation and local-only commit**: Run targeted `src/api` unit tests (`test_case_journey.py`, `test_nomination_api_routes.py`, `test_content_standard.py`, `test_accessibility_baseline.py`), `ruff`, `mypy`, and `src/core` scenario-manifest/needs-inventory checks, then commit locally with the Copilot `Co-authored-by` trailer without pushing.

### What You May Not Know

* **Exact hosted CI symbol and branch reconciliation**: Primary inspection of `gh pr view 1776` and `gh run view 43694720253 --log-failed` confirmed that worktree `/home/azureuser/source/ama-demo-wt/feat-130-api-routes` at HEAD `2215209cb` tracks active pull-request branch `feat/ux-130-api-routes` (targeting `feat/demo-233-same-home-tensions-0825` / pull request `#1639`), and that the two failing tests were `CaseJourney.test_raw_resident_and_challenge_outcomes_exclude_repeat_posts` (slicing `affectedChallengePanel` between `const formFor = ` and `const staff`) and `NominationApiRoutesTests.test_workbench_keyboard_operability_for_digital_and_non_digital_routes` (`pw.chromium.launch(headless=True)` raising `BrowserType.launch: Executable doesn't exist`).
* **Why `_playwright_available()` returned `True` in hosted CI**: `.github/workflows/src-ci.yml` installs the Python `playwright` package via `pip install -e ".[dev]"` before `python -m unittest discover -s tests -v`, whereas `python -m playwright install --with-deps chromium` runs only in a subsequent step. Peer tests (`test_workbench_live_defaults.py` and `test_browser_asset_urls.py`) catch `PlaywrightError` when `"Executable doesn't exist"` appears in the launch error and skip cleanly.
* **Module import path when running `test_case_journey.py` from repository root**: `test_case_journey.py` imports `from tests.test_mvp import DATA` (resolved under `src/core/tests/test_mvp.py`). In hosted CI (`working-directory: src/api`), `src/core` is editable-installed and `tests` resolves cleanly; from the repository root, validation runs both the caller's exact `PYTHONPATH` command and the `src/core`-inclusive `PYTHONPATH` / `cd src/api` invocation so `tests.test_mvp` resolves deterministically.
* **Static guards and scenario-manifest hashes**: `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` does not hash `panels.js`, and static guards in `test_accessibility_baseline.py` (`9` `aria-invalid` calls, `14` `table` elements) and `test_content_standard.py` (banned jargon check on every `web/*.js` line including comments) remain intact.

### Unresolved Decisions or Blockers

* No blockers exist for this local CI-fix RPI loop. External human governance items (`OD-41`, `OD-42`, human representative comprehension sign-off) and remote push plus hosted CI re-verification remain owner-controlled follow-ups (`Refs #130`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop in order (`research`, `plan`, `implement`, `review`), recording dated `2026-11-15` artifacts under `.copilot-tracking/` for Issue `#130` (`PR #1776`, HEAD `2215209cb`) in worktree `/home/azureuser/source/ama-demo-wt/feat-130-api-routes` (caller prompt; reconciled to active `PR #1776` branch `feat/ux-130-api-routes` per repository Branch Workflow and research `C8`).
* Fix the `ReferenceError: c is not defined` Node slice failure in `src/api/src/zava_forward/api/web/panels.js` triggered by `src/api/tests/test_case_journey.py` using `typeof c !== "undefined" && c` and preserving slice compatibility (caller prompt; reconciled to `affectedChallengePanel` in research `C1`–`C3`).
* Fix the missing-Chromium failure in `src/api/tests/test_nomination_api_routes.py` by aligning the browser/Playwright skip condition with the existing helper pattern used in peer `src/api/tests/test_*.py` unit tests when Chromium is not installed in the unit-test container, while keeping route and DOM assertions covered (caller prompt; research `C1`, `C4`, `C5`).
* Run targeted validation covering `src/api/tests/test_case_journey.py`, `src/api/tests/test_nomination_api_routes.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_accessibility_baseline.py`, `python3 -m ruff check src/api`, `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`, and `src/core/tests/test_scenario_manifest.py` plus `src/core/tests/test_needs_inventory.py` (caller prompt).
* Commit all changes and `.copilot-tracking/` artifacts locally with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer, do not push, and leave a clean frozen working tree (caller prompt).

## Goals

* Eliminate the `ReferenceError: c is not defined` failure when `src/api/tests/test_case_journey.py` slices and evaluates `formFor` from `src/api/src/zava_forward/api/web/panels.js`.
* Ensure `NominationApiRoutesTests.test_workbench_keyboard_operability_for_digital_and_non_digital_routes` skips cleanly when the Playwright Chromium executable is absent in unit-test containers, runs in full when Chromium is installed, and leaves all HTTP/HTML route and DOM assertions unconditional.
* Prove regression safety across unit tests, static accessibility/content baselines, `ruff`, `mypy`, and synthetic-scenario manifest tests.

## Scope and Non-Goals

### In Scope

* Reordering `const staff` before `const perms` / `const repRefs` and guarding `typeof c !== "undefined" && c` inside `affectedChallengePanel` in `src/api/src/zava_forward/api/web/panels.js`.
* Updating `src/api/tests/test_nomination_api_routes.py` to use `importlib.util.find_spec("playwright")` for module detection, catch `PlaywrightError` on `"Executable doesn't exist"` during `pw.chromium.launch(headless=True)` with `self.skipTest("Chromium is installed by the later browser-check step")`, and add `1` focused unit test verifying the missing-Chromium skip branch.
* Executing focused-tier validation commands and recording dated `2026-11-15` child RPI artifacts (`nomination-api-routes-130-ci-fix-*`) while preserving parent RPI artifacts (`nomination-api-routes-130-*`).

### Non-Goals

* Pushing commits to `origin` or mutating remote PR state.
* Renaming or switching away from `PR #1776`'s active head branch `feat/ux-130-api-routes`.
* Editing `src/api/tests/test_case_journey.py`, `.github/workflows/src-ci.yml`, or `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`.
* Overwriting or deleting historical parent RPI artifacts (`nomination-api-routes-130-*`).

## Functional Requirements

* `affectedChallengePanel` in `src/api/src/zava_forward/api/web/panels.js` must define `const staff` immediately after `const formFor` and guard any reference to `c` in `perms` lookup via `typeof c !== "undefined" && c`.
  * Observable acceptance criteria: `src/api/tests/test_case_journey.py` (`31` tests, including `test_raw_resident_and_challenge_outcomes_exclude_repeat_posts`) passes with `0` failures and `0` errors without modifying `test_case_journey.py`.
* `NominationApiRoutesTests.test_workbench_keyboard_operability_for_digital_and_non_digital_routes` in `src/api/tests/test_nomination_api_routes.py` must skip via `self.skipTest("Chromium is installed by the later browser-check step")` when `pw.chromium.launch(headless=True)` raises `PlaywrightError` containing `"Executable doesn't exist"`, re-raise unexpected `PlaywrightError` failures, and execute completely when Chromium is installed.
  * Observable acceptance criteria: When Chromium is present locally, the keyboard operability test executes and passes; a dedicated unit test simulating `PlaywrightError("BrowserType.launch: Executable doesn't exist ...")` confirms `unittest.SkipTest` is raised cleanly; non-browser route/DOM tests in `NominationApiRoutesTests` run unconditionally.

## Non-Functional Requirements

* Accessibility, plain-language copy, and form-error association baseline preservation across `src/api/src/zava_forward/api/web/panels.js`.
  * Objective threshold or evaluation condition: `setAttribute("aria-invalid", "true")` count stays `9`, `h("table", {}, ...)` count stays `14`, Epic 149 error-summary association checks pass, and `0` banned copy words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) appear anywhere in `web/*.js`.
  * Operating condition or verification approach, if needed: Run `test_accessibility_baseline.py`, `test_content_standard.py`, and `test_epic149_form_error_summary_associations.py`, plus `web-design-guidelines` review in `rpi-review`.
  * Observable acceptance criteria: All three static guard test suites pass with `0` violations.
* Lint, formatting, type-safety, and synthetic-data manifest integrity.
  * Objective threshold or evaluation condition: `0` `ruff check` / `ruff format --check` diagnostics in `src/api`, `0` `mypy` errors in `src/api`, and `0` hash/inventory mismatches in `test_scenario_manifest.py` and `test_needs_inventory.py`.
  * Operating condition or verification approach, if needed: Run `ruff check`, `ruff format --check`, `mypy`, and `src/core` manifest/inventory unit tests.
  * Observable acceptance criteria: Every static analysis and manifest command exits `0`.
* Locked test ownership and change bounds.
  * Objective threshold or evaluation condition: Test removals: `none`. Maximum new test additions: `1` unit test method (`test_keyboard_operability_skips_when_chromium_executable_missing`) in `src/api/tests/test_nomination_api_routes.py`. Canonical production target: `src/api/src/zava_forward/api/web/panels.js`. Generated targets: `none`.
  * Observable acceptance criteria: `git diff --stat` modifies only `src/api/src/zava_forward/api/web/panels.js` and `src/api/tests/test_nomination_api_routes.py` outside `.copilot-tracking/`.

## Acceptance Criteria

* `CaseJourney` in `src/api/tests/test_case_journey.py` passes completely (`OK`), proving semantic and slice-regression compatibility of `nominationPanel._routeForm` and `affectedChallengePanel` (`formFor`).
* `NominationApiRoutesTests` in `src/api/tests/test_nomination_api_routes.py` passes completely (`OK`), covering HTTP/HTML dual-route DOM semantics unconditionally, full headless-Chromium keyboard operability when Chromium is installed, and clean `SkipTest` handling when the Chromium binary is absent.
* `test_content_standard.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_nomination_screen.py`, `test_scenario_manifest.py`, and `test_needs_inventory.py` all pass (`OK`).
* `python3 -m ruff check src/api`, `python3 -m ruff format --check src/api`, and `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` exit `0`.
* No `.copilot-tracking/` paths appear in production code, test files, or commit messages, and the final local commit on `feat/ux-130-api-routes` includes the Copilot `Co-authored-by` trailer with a clean `git status --short` and zero remote push.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan.md                                                              |
| Phase details                    | .copilot-tracking/details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md                                                   |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan-critique.md with Pass disposition (0 PC findings)        |
| Relevant research                | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-ci-fix-research.md                                                       |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md is created by implementation as its evidence record     |
| Planning execution and readiness | Complete and ready for implementation                                                                                                    |
| Continuation context             | Confirmed automatic RPI Agent return; parent advances automatically to rpi-implement                                                     |

## Sources

* `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-ci-fix-research.md`: Primary evidence (`C1`–`C8`, `W1`) reconciling GitHub Actions run `43694720253` logs, `panels.js` slice boundaries, `src-ci.yml` Chromium staging, and static guard invariants.
* `src/api/src/zava_forward/api/web/panels.js`: Production UI panel module containing `nominationPanel._routeForm` and `affectedChallengePanel`.
* `src/api/tests/test_case_journey.py`: Regression test suite slicing `panels.js` between `const formFor = ` and `const staff`.
* `src/api/tests/test_nomination_api_routes.py`: Nomination API, accessible HTML route/DOM, and Playwright keyboard operability test suite.
* `src/api/tests/test_workbench_live_defaults.py` and `src/api/tests/test_browser_asset_urls.py`: Canonical repository `PlaywrightError` `"Executable doesn't exist"` skip pattern in `src-api` unit discovery.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Fix `panels.js` Node slice guard and `test_nomination_api_routes.py` missing-Chromium skip

* Intent: Resolve both `src-api` unit-step failures from GitHub Actions run `43694720253` without weakening route, DOM, or local browser assertions.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Reorder `staff` declaration and guard `c` in `affectedChallengePanel` (`panels.js`)

* Requirement and evidence: Caller Requirement 1 and research `C1`–`C3`, `C6`, `W1`.
* Expected result: `const staff` immediately follows `const formFor` inside `affectedChallengePanel`, `const caseRecord = typeof c !== "undefined" && c ? c : null;` safely guards `nomination_permissions`, and `test_case_journey.py` evaluates the `formFor` slice with zero `ReferenceError`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Align missing-Chromium `PlaywrightError` skip and add skip unit test in `test_nomination_api_routes.py`

* Requirement and evidence: Caller Requirement 2 and research `C1`, `C4`, `C5`.
* Expected result: `_playwright_available()` checks `importlib.util.find_spec("playwright") is not None`, `pw.chromium.launch(headless=True)` skips cleanly with `"Chromium is installed by the later browser-check step"` when `PlaywrightError` reports `"Executable doesn't exist"` (re-raising other errors), and `test_keyboard_operability_skips_when_chromium_executable_missing` verifies that skip contract directly.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Execute focused-tier validation across `src/api` and `src/core`

* Intent: Verify that all unit tests, static accessibility/content guards, linters, type checks, and synthetic-scenario manifest invariants pass cleanly.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run targeted `unittest`, `ruff`, `mypy`, and `scenario-manifest` validation commands

* Requirement and evidence: Caller Validation Requirements 1–3 and research `C6`, `C7`.
* Expected result: All targeted `src/api` and `src/core` unit tests (`test_case_journey.py`, `test_nomination_api_routes.py`, `test_nomination_screen.py`, `test_content_standard.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.md`/`py`, `test_scenario_manifest.py`, `test_needs_inventory.py`), `ruff check`, `ruff format --check`, and `mypy` pass with exit code `0`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md

## Dependencies

* Local Python 3.12 + Node.js runtime and editable/PYTHONPATH access to `src/core`, `src/agents`, and `src/api`: Required to execute `test_case_journey.py` Node VM slices, `test_nomination_api_routes.py` Playwright/ASGI checks, `ruff`, and `mypy`.
* `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-ci-fix-research.md`: Supplies verified root causes (`C1`–`C8`, `W1`) so implementation does not rely on approximate symbol names.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`Pass`, 0 `PC-xxx` findings) | resolved | Candidate verified ready across slice boundaries, Chromium skip parity, locked test bounds, and static baselines; keep `@unittest.skipUnless(_playwright_available(), ...)` on the mock skip test and `gh api user` privacy-safe `user.email` at commit. |

## Follow-Up Items

* Extend `src/api/checks/nomination_browser_check.py` to scan interactive dual-route nomination acknowledgement and correction disclosures with axe-core 4.10.3: Outside immediate CI-bugfix scope; tracked as post-Review ranked follow-up for `#130`.
* Ratify governance open decisions `OD-41` and `OD-42`, complete human representative comprehension sign-off, push `feat/ux-130-api-routes` (`PR #1776`), and obtain hosted CI + independent exact-head review: Outside local no-push execution boundary; owned by human governance and repository owner (`Refs #130`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md
* Ready phase or task: All planned items (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`) complete; ready for `rpi-review`
* Remaining provisional question or blocker: None

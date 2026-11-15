<!-- markdownlint-disable-file -->
# RPI Changes: Fix Issue 130 src-api CI Failures from Run 43694720253

## Metadata

* Task ID: nomination-api-routes-130-ci-fix
* Related plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-ci-fix-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full_plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01
* All remaining active-plan markers: none
* Status basis: Every phase and task in `full_plan` completed and passed all targeted unit, browser-skip, static baseline, linter, type, and manifest validations.

## Execution Summary

Completed `full_plan` implementation (`P01-T01`, `P01-T02`, `P02-T01`) resolving both `src-api` unit-step failures from GitHub Actions run `43694720253` on pull request `#1776` (`feat/ux-130-api-routes`):
1. Restored the `formFor`-to-`staff` slice boundary and added a defensive `typeof c !== "undefined" && c` guard inside `affectedChallengePanel` in `src/api/src/zava_forward/api/web/panels.js`, resolving `CaseJourney.test_raw_resident_and_challenge_outcomes_exclude_repeat_posts`.
2. Updated `_playwright_available()` to `importlib.util.find_spec("playwright") is not None`, added `_launch_headless_chromium()` catching `PlaywrightError` on `"Executable doesn't exist"` via `self.skipTest("Chromium is installed by the later browser-check step")`, and added `test_keyboard_operability_skips_when_chromium_executable_missing` in `src/api/tests/test_nomination_api_routes.py`, resolving `NominationApiRoutesTests.test_workbench_keyboard_operability_for_digital_and_non_digital_routes` in Chromium-less unit containers while preserving live headless Chromium execution when Chromium is installed and unconditional HTTP/HTML route/DOM tests.

## Completed Work

### Guard `c` and restore `formFor`-to-`staff` slice boundary in `affectedChallengePanel`

* Related phase or task: P01, P01-T01
* Files: src/api/src/zava_forward/api/web/panels.js
* What changed and why: Moved `const staff = (me.staff || []).filter(...)` immediately after `const formFor = ...` inside `affectedChallengePanel` and bound `const caseRecord = typeof c !== "undefined" && c ? c : null;` before inspecting `caseRecord.nomination_permissions`, eliminating the `ReferenceError: c is not defined` thrown when `src/api/tests/test_case_journey.py` evaluates `"const formFor = " + source.split("  const formFor = ", 1)[1].split("  const staff", 1)[0]` in Node.
* Completion evidence: `CaseJourney` (`31` tests, including `test_raw_resident_and_challenge_outcomes_exclude_repeat_posts`) passed with `0` errors and `0` failures without modifying `test_case_journey.py`.
* Validation: Passed (`test_case_journey.py`, `test_nomination_screen.py`, `test_content_standard.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`).

### Align missing-Chromium `PlaywrightError` skip and add skip regression test

* Related phase or task: P01, P01-T02
* Files: src/api/tests/test_nomination_api_routes.py
* What changed and why: Replaced try/import `_playwright_available()` with `importlib.util.find_spec("playwright") is not None`, added `_launch_headless_chromium()` to skip with `"Chromium is installed by the later browser-check step"` when `PlaywrightError` contains `"Executable doesn't exist"` (re-raising genuine launch crashes), and added `test_keyboard_operability_skips_when_chromium_executable_missing`.
* Completion evidence: `NominationApiRoutesTests` (`5` tests) passed `5/5` (`skipped=0`) with the local Chromium cache and passed `5/5` (`OK (skipped=1)`) under `PLAYWRIGHT_BROWSERS_PATH=/tmp/empty-playwright-cache-130` (reproducing the hosted `src-api` unit step).
* Validation: Passed (`test_nomination_api_routes.py` with and without Chromium binary, `ruff check`, `ruff format --check`, `mypy`).

### Execute focused-tier validation suites across `src/api`, `src/core`, and `tools`

* Related phase or task: P02, P02-T01
* Files: .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-ci-fix-changes.md
* What changed and why: Executed all requested and coupled unit, static accessibility/content, lint, format, type, synthetic-manifest, and migration regression suites.
* Completion evidence: Every command below exited `0`.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `PYTHONPATH=src/api:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_case_journey.py src/api/tests/test_nomination_api_routes.py src/api/tests/test_content_standard.py src/api/tests/test_accessibility_baseline.py -q` | Repo-root targeted `src/api` unit & static guards (`P02-T01`) | Passed | `Ran 79 tests in 9.137s — OK` (note: `src/api` prepended to `PYTHONPATH` from repo root so `from tests.test_mvp import DATA` in `test_case_journey.py` and `test_nomination_api_routes.py` resolves without relying on shared user site-packages) |
| `(cd src/api && PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_case_journey.py tests/test_nomination_api_routes.py tests/test_content_standard.py tests/test_accessibility_baseline.py -q)` | `src/api` working-directory CI-equivalent unit run (`P02-T01`) | Passed | `Ran 79 tests in 9.218s — OK` (`skipped=0`, live headless Chromium executed) |
| `PYTHONPATH=src/core:src/agents:src/api:src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_case_journey.py src/api/tests/test_nomination_api_routes.py src/api/tests/test_content_standard.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_nomination_screen.py src/api/tests/test_epic149_form_error_summary_associations.py -v` | Extended coupled `src/api` suites (`NominationScreen` + `FormErrorAssociations`) (`P02-T01`) | Passed | `Ran 94 tests in 9.478s — OK` |
| `(cd src/api && PLAYWRIGHT_BROWSERS_PATH=/tmp/empty-playwright-cache-130 PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_nomination_api_routes.py -v)` | Real empty-Chromium-cache hosted CI reproduction (`P01-T02`, `P02-T01`) | Passed | `Ran 5 tests in 3.933s — OK (skipped=1)` with `'Chromium is installed by the later browser-check step'` while all 4 HTTP/DOM/mock tests ran and passed |
| `python3 -m ruff check src/api && (cd src/api && python3 -m ruff format --check .)` | Lint and formatting (`P02-T01`) | Passed | `All checks passed!` and `210 files already formatted` |
| `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` | Static typing (`P02-T01`) | Passed | `Success: no issues found in 294 source files` |
| `PYTHONPATH=src/core:src/core/src:src/core/tests python3 -m unittest src/core/tests/test_scenario_manifest.py src/core/tests/test_needs_inventory.py -q` | Synthetic scenario-manifest & needs-inventory (`P02-T01`) | Passed | `Ran 19 tests in 0.080s — OK` |
| `python3 tools/rename-zava-tests.py` | Naming regression check (`P02-T01`) | Passed | `Ran 25 tests in 0.481s — OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01` checked `[x]` in plan and marked `complete` in phase details).
* Completed-work evidence and handoff prose: Current and synchronized across plan, details, and changes record.
* Validation, blockers, remaining work, and follow-up items: Current (`0` blockers, `none` remaining active markers, `2` follow-ups preserved).
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-ci-fix-plan.md, `## Follow-Up Items`
* Extend `src/api/checks/nomination_browser_check.py` to scan interactive dual-route nomination acknowledgement and correction disclosures with axe-core 4.10.3: Outside immediate CI-bugfix scope; tracked for post-Review selection (`#130`).
* Ratify governance open decisions `OD-41` and `OD-42`, complete human representative comprehension sign-off, push `feat/ux-130-api-routes` (`PR #1776`), and obtain hosted CI + independent exact-head review: Outside local no-push execution boundary; owned by human governance and repository owner (`Refs #130`).

## Return-to-Caller State

* Implementation execution status: Complete (`full_plan`)
* Declared scope and markers: full_plan; completed: P01, P01-T01, P01-T02, P02, P02-T01; remaining: none
* Validation coverage: 94 `src/api` unit/DOM/a11y/copy/browser tests (`OK`), real empty-Chromium-cache skip reproduction (`OK (skipped=1)`), `ruff check` + `ruff format --check` (`0` issues), `mypy` (`294` files, `0` issues), 19 `src/core` manifest/inventory tests (`OK`), 25 `rename-zava-tests.py` tests (`OK`)
* Blockers: None
* Current plan and detail updates: None beyond completion markers
* Planning and critique state: Ready (`Pass` critique with 0 PC findings)
* Follow-up items: Two follow-up items mirrored from plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent

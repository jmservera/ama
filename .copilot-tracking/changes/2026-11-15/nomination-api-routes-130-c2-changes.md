<!-- markdownlint-disable-file -->
# RPI Changes: Rebase Issue 130 Branch and Fix Refusal Feedback Focus-Blur Clearing

## Metadata

* Task ID: nomination-api-routes-130-c2
* Related plan: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full_plan
* Completed scope markers: P01, P01-T01, P02, P02-T01, P02-T02, P03, P03-T01
* All remaining active-plan markers: none
* Status basis: All planned phases and tasks (`P01`, `P02`, `P03`) completed with verified Focused Tier unit, Playwright + axe-core browser, Ruff, and Mypy evidence.

## Execution Summary

Rebased `feat/ux-130-api-routes` (`PR #1776`) cleanly onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, `PR #1639`), scoped the `"change"` invalid-state clearing listener inside `nominationPanel._routeForm` in `src/api/src/zava_forward/api/web/panels.js` exclusively to `<select>` elements (`isSelect: Boolean(options)`), added `test_route_form_blur_change_preserves_refusal_message_while_input_and_select_clear` in `src/api/tests/test_nomination_screen.py`, and passed all Focused Tier checks including end-to-end `case_journey_browser_check.py` (`mutation_reconstruction` `challenge` `refusal`).

## Completed Work

### P01 / P01-T01: Rebase onto Target Parent Branch

* Configured local privacy-safe Git email (`8036360+jmservera@users.noreply.github.com`), fetched `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), and rebased `feat/ux-130-api-routes` cleanly onto `6510b6fbc` (`9b9f72eae` and `11867e8b1` replayed with zero conflicts while preserving all Cycle 1 and Cycle 2 `.copilot-tracking/` artifacts).

### P02 / P02-T01 and P02-T02: Fix `_routeForm` Focus-Blur Clearing and Add Regression Test

* Updated `src/api/src/zava_forward/api/web/panels.js` inside `nominationPanel._routeForm` to record `isSelect: Boolean(options)` on each field descriptor and attach `input.addEventListener("change", clearInvalid)` only when `isSelect` is true, keeping `input.addEventListener("input", clearInvalid)` on all controls. When `bindCaseMutationForm` moves focus to `#challenge-open-feedback` (`status.focus()`) after a `409` refusal, the synchronous blur-triggered `"change"` event on an edited `<input>` or `<textarea>` no longer clears `mutation.message` or `status.textContent`.
* Added `test_route_form_blur_change_preserves_refusal_message_while_input_and_select_clear` in `src/api/tests/test_nomination_screen.py` (formatted with `ruff format`), exercising the real `panelOwned`, `PANEL_SUPPORT`, `bindCaseMutationForm`, and `nominationPanel._routeForm` functions in Node to verify active-element blur `"change"` refusal retention on `<input>`, `"input"` clearing on `<input>`, and `"change"` clearing plus `showWhen` visibility toggling on `<select>`.

### P03 / P03-T01: Focused Tier Validation

* Classified as Focused Tier per caller instructions and repository rules (targeted frontend event-listener bugfix, 1 unit regression test, and parent-branch rebase; no infrastructure, Dockerfile, dependency, workflow, gate, SQL schema, or security-control changes). Executed all planned unit, Playwright + axe-core browser, Ruff, and Mypy checks without invoking `tools/rpi-checks.py`.
* Local Judgment Note: On this Azure Linux VM, `/etc/fonts` maps unaliased `sans-serif` / `Segoe UI` to monospace `Liberation Mono` unless `Liberation Sans` is aliased via `FONTCONFIG_FILE`; passing a temporary `FONTCONFIG_FILE` aliasing `sans-serif`, `system-ui`, and `Segoe UI` to installed proportional `Liberation Sans` matches `ubuntu-latest` hosted CI metrics and lets `case_journey_browser_check.py` complete end-to-end with exit code `0`. Similarly, invoking `src/api` checks and `test_mvp`-importing suites from the repository root includes `src/api:src/core` on `PYTHONPATH` so package-qualified `tests.*` and `checks.*` imports resolve cleanly.

## Implementation-Time Plan and Detail Updates

None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `node --check src/api/src/zava_forward/api/web/panels.js` | P02-T01 | Passed | Exit 0 |
| `src/core/tests` nomination unit discovery (`test_*nomination*.py`) | P03-T01 | Passed | 16 tests passed (exit 0) |
| `src/api/tests` nomination unit discovery (`test_*nomination*.py`) | P03-T01 | Passed | 13 tests passed including new focus-blur regression test (exit 0) |
| `test_resident_api.py`, `test_accessibility_baseline.py`, `test_case_journey.py`, `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`, `test_programme_coordinator_wcag_230.py` | P03-T01 | Passed | All suites passed (exit 0) |
| `src/api/checks/case_journey_browser_check.py` (Playwright + SHA-verified axe-core 4.10.3 + proportional `Liberation Sans` fontconfig) | P03-T01 | Passed | Exit 0 end-to-end including `mutation_reconstruction` (`challenge` `refusal`), 320px/390px/1280px/200% zoom reflow, forced-colours, and fallback checks |
| `src/api/checks/nomination_browser_check.py` (Playwright + SHA-verified axe-core 4.10.3) | P03-T01 | Passed | Exit 0 (`outcome: passed`, 0 axe violations) |
| `python3 -m ruff check src/core src/api && python3 -m ruff format --check src/core src/api` | P03-T01 | Passed | All checks passed; 475 files formatted (exit 0) |
| `(cd src/core && python3 -m mypy) && (cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` | P03-T01 | Passed | 0 issues in 317 `src/core` files and 295 `src/api` files (exit 0) |
| `tools/rpi-checks.py` | Out of scope | Skipped | Explicitly prohibited by caller instructions under Focused Tier |

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c2-plan.md, `## Follow-Up Items`

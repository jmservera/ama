<!-- markdownlint-disable-file -->
# RPI Phase Details: Focused Cycle 2 Correction for Workbench WCAG 2.2 Baseline (#151)

## Metadata

* Task ID: 2026-11-15-wcag-baseline-151-c2
* Task slug: wcag-baseline-151-c2
* Related plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c2-plan.md
* Evidence sources: src/api/tests/test_epic149_landmarks_skip_link_focus_order.py, src/api/tests/test_accessibility_baseline.py, src/api/tests/test_wcag_workbench_baseline_151.py, src/api/tests/test_epic149_form_error_summary_associations.py

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Shrink-Only Skip-Link Baseline Fix, Isolated Formatting, and Focused Validation | completed | P01, P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Shrink-Only Skip-Link Baseline Fix, Isolated Formatting, and Focused Validation

### Context

Cycle 1 (`d15acc57a`) added `<a class="skip-link" href="#welcome-main">Skip to main content</a>` and `<main id="welcome-main" tabindex="-1">` to `src/api/src/zava_forward/api/web/welcome.html` (served at `/`). Independent functional review (`rev-151-wcag`) found that `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` still listed `"/"` in `NO_SKIP_LINK = {"/", "/law.html"}`, causing `SkipLink.test_skip_link_gaps_are_recorded_and_shrink_only` to fail (`AssertionError: True != False : /: update NO_SKIP_LINK`). In addition, `test_accessibility_baseline.py` and `test_wcag_workbench_baseline_151.py` had minor formatting diffs under `python3 -m ruff format --isolated --line-length 100`.

### Intent

Align `NO_SKIP_LINK` with the delivered `/` welcome skip link, format both `#151` test modules under `--isolated --line-length 100` while preserving cross-module test invariants, and prove green execution across all targeted unit, lint, format, and type checks.

### Boundaries

* Included: `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_wcag_workbench_baseline_151.py`, and Cycle 2 `.copilot-tracking/` artifacts.
* Excluded: Web files under `src/api/src/zava_forward/api/web/`, `src/api/pyproject.toml`, historical Cycle 1 `.copilot-tracking/` artifacts, and remote `git push`.

### Likely Targets

* src/api/tests/test_epic149_landmarks_skip_link_focus_order.py: Update `NO_SKIP_LINK = {"/law.html"}`.
* src/api/tests/test_accessibility_baseline.py: Bind the `sites == 9` assertion message to a local variable so `"self.assertEqual(sites, 9,"` remains on a single line under 100 columns, then format with `python3 -m ruff format --isolated --line-length 100`.
* src/api/tests/test_wcag_workbench_baseline_151.py: Format with `python3 -m ruff format --isolated --line-length 100`.

### Dependencies

* None.

### Validation Expectations

* All four caller-specified commands plus `test_epic149_form_error_summary_associations.py`, `ruff format --isolated --line-length 100 --check`, and `mypy` exit `0`.

### Completion Evidence

* Clean diff in the three test files and passing command outputs recorded in `.copilot-tracking/changes/2026-11-15/wcag-baseline-151-c2-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update NO_SKIP_LINK and format #151 baseline test modules

#### Context

1. `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` defines `NO_SKIP_LINK = {"/", "/law.html"}` as a shrink-only set of routes lacking `.skip-link`. Because `welcome.html` (`/`) now renders `.skip-link`, `NO_SKIP_LINK` must shrink to `{"/law.html"}` while `NO_NAV` stays `{"/", "/law.html"}` (`welcome.html` has `<header>` and `<main>`, no `<nav>`).
2. `src/api/tests/test_epic149_form_error_summary_associations.py` asserts `"self.assertEqual(sites, 9," in BASELINE_TEST.read_text()`. Binding `invalid_msg = "new aria-invalid site: audit it and update this check and the record"` before `self.assertEqual(sites, 9, invalid_msg)` keeps that call at 47 columns so `ruff format --isolated --line-length 100` preserves the exact substring on a single line.

#### Intent

Apply the shrink-only `NO_SKIP_LINK` update and run isolated 100-column Ruff formatting across both `#151` test modules without breaking cross-file substring guards.

#### Boundaries

* Included: `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_wcag_workbench_baseline_151.py`.
* Excluded: Adding or removing test cases or changing `src/api/pyproject.toml`.

#### Likely Targets

* src/api/tests/test_epic149_landmarks_skip_link_focus_order.py
* src/api/tests/test_accessibility_baseline.py
* src/api/tests/test_wcag_workbench_baseline_151.py

#### Dependencies

* None.

#### Validation Expectations

* `python3 -m ruff format --isolated --line-length 100 --check src/api/tests/test_accessibility_baseline.py src/api/tests/test_wcag_workbench_baseline_151.py src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` exits `0`.

#### Completion Evidence

* Updated `NO_SKIP_LINK = {"/law.html"}` and clean `--isolated --line-length 100` formatting across all three files.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Execute focused unittest, ruff, and mypy validation

#### Context

Caller specified four validation commands; coupled Epic #149 tests (`test_epic149_*.py`) and `mypy` verify no cross-test or static-typing regressions were introduced.

#### Intent

Run all targeted and coupled checks to confirm zero regressions before Review and local commit.

#### Boundaries

* Included: Local test, lint, format-check, and type-check execution; pre-commit `git status --short` verification that historical Cycle 1 `.copilot-tracking/` files remain untouched.
* Excluded: `git push`.

#### Likely Targets

* Validation commands run against `src/api/tests/` and `src/api/src/`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/api/src python3 -m unittest discover -s src/api/tests -p 'test_epic149_landmarks_skip_link_focus_order.py' -q` (`OK`)
* `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/api/src python3 -m unittest discover -s src/api/tests -p 'test_wcag_workbench_baseline_151.py' -q` (`OK`)
* `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/api/src python3 -m unittest discover -s src/api/tests -p 'test_accessibility_baseline.py' -q` (`OK`)
* `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/api/src python3 -m unittest discover -s src/api/tests -p 'test_epic149_*.py' -q` (`OK`)
* `(cd src/api && python3 -m ruff check src tests)` (`All checks passed!`)
* `(cd src/api && python3 -m mypy src tests/test_epic149_landmarks_skip_link_focus_order.py tests/test_wcag_workbench_baseline_151.py tests/test_accessibility_baseline.py)` (`Success`)

#### Completion Evidence

* Recorded command exit statuses and counts in `.copilot-tracking/changes/2026-11-15/wcag-baseline-151-c2-changes.md`.

#### Unresolved Items

* None.

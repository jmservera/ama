<!-- markdownlint-disable-file -->
# RPI Changes: Issue 231 Cycle 1 Rebase CSS Focus Rule Recovery (PR 1767)

## Metadata

* Task ID: 2026-11-15-retrofit-technical-quality-wcag-231-c1
* Related plan: .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02
* All remaining active-plan markers: none
* Status basis: Every phase and task in declared full-plan scope (P01 and P02) completed with passing focused validation, refreshed Web Interface Guidelines audit, and verified pre-review worktree hygiene.

## Execution Summary

Split the rebase-merged programmatic focus rule in src/api/src/zava_forward/api/web/style.css into two consecutive standalone Fluent 2 focus-token rules (`[tabindex="-1"]:focus` followed by `.screen-record h2[tabindex="-1"]:focus-visible`), restoring byte-for-byte parity with parent commit fe6398197 while preserving Issue #231's heading focus-visible rule. Added one focused regex assertion (`0` removals, `1` addition) in `TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants` within src/api/tests/test_technical_quality_screens_wcag.py to prevent future rebase selector merging. Executed all 10 focused WCAG and baseline unit test modules (`109` tests passing), `ruff check .`, `ruff format --check .` (`207` files formatted), `mypy` (`30` source/test files clean), `python3 tools/rename-zava-tests.py` (`25` tests passing), refreshed Vercel Web Interface Guidelines review (`0` violations), configured local git noreply `user.email` (`8036360+jmservera@users.noreply.github.com`), and verified clean pre-review worktree inventory.

## Completed Work

### Split merged programmatic focus rule in workbench stylesheet

* Related phase or task: P01, P01-T01
* Files: src/api/src/zava_forward/api/web/style.css
* What changed and why: Replaced the single comma-separated rule `[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible { ... }` with standalone `[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` immediately followed by standalone `.screen-record h2[tabindex="-1"]:focus-visible { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` so both sibling Issue #229's `\[tabindex="-1"\]:focus\s*\{\s*outline:` contract and Issue #231's `\.screen-record\s+h2\[tabindex="-1"\]:focus-visible\s*\{` contract match simultaneously with zero CSS cascade change.
* Completion evidence: `git diff -- src/api/src/zava_forward/api/web/style.css` confirms exact two-rule split matching parent fe6398197's standalone `[tabindex="-1"]:focus` rule.
* Validation: Passed (`test_housing_resident_screen_wcag.py`, `test_data_steward_screen_wcag.py`, `test_technical_quality_screens_wcag.py`, `test_accessibility_baseline.py`, and `test_design_system.py` all pass).

### Add standalone programmatic focus regex guard in Issue 231 WCAG tests

* Related phase or task: P01, P01-T02
* Files: src/api/tests/test_technical_quality_screens_wcag.py
* What changed and why: Added `self.assertRegex(CSS, r'\[tabindex="-1"\]:focus\s*\{\s*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)')` inside `TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants` (`0` removals, `1` addition) so Issue #231's own WCAG suite fails immediately if a future rebase merges or drops the standalone `[tabindex="-1"]:focus` rule.
* Completion evidence: `git diff -- src/api/tests/test_technical_quality_screens_wcag.py` confirms single assertion addition with zero `.copilot-tracking/` substrings.
* Validation: Passed (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`, and `tools/rename-zava-tests.py`).

### Run focused WCAG unit tests, static analysis, test-rename check, and Web Interface Guidelines review

* Related phase or task: P02, P02-T01
* Files: .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md
* What changed and why: Ran the complete 10-module focused WCAG/baseline unittest suite (mapping caller alias `test_quality_finance_screen_wcag.py` to `test_technical_quality_screens_wcag.py` plus all finance and data-steward WCAG modules), `ruff check .`, `ruff format --check .`, `mypy`, `python3 tools/rename-zava-tests.py`, and refreshed `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` against `src/api/src/zava_forward/api/web/style.css`.
* Completion evidence: `109` unit tests passed in `3.507s`, `ruff check .` passed, `207` files passed `ruff format --check .`, `mypy` passed on `30` source/test files, `tools/rename-zava-tests.py` passed `25` tests in `0.580s`, and Web Interface Guidelines check passed:

```text
## src/api/src/zava_forward/api/web/style.css

pass
```

* Validation: Passed (all commands exited `0` with zero findings).

### Configure repository-local git noreply identity and verify pre-review worktree hygiene

* Related phase or task: P02, P02-T02
* Files: .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md
* What changed and why: Queried `gh api user` and configured `git config --local user.email "8036360+jmservera@users.noreply.github.com"` (`user.name` verified as `Juan Manuel Servera`), verified `git diff -- src/` contains zero `.copilot-tracking/` substrings, and confirmed `git status --short` lists only expected Cycle 1 source, test, and tracking paths plus modified parent state `.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json`.
* Completion evidence: `git config --local --get user.email` outputs `8036360+jmservera@users.noreply.github.com` and `git status --short` accounts for every modified and untracked Cycle 1 artifact ready for the RPI parent's post-review atomic commit.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

* None

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Focused WCAG and baseline unittest suite | test_technical_quality_screens_wcag.py, test_housing_resident_screen_wcag.py, test_data_steward_screen_wcag.py, test_programme_screen_wcag.py, test_finance_screen_wcag.py, test_finance_grants_screen_wcag.py, test_finance_screens_wcag_225.py, test_accessibility_baseline.py, test_content_standard.py, test_design_system.py | Passed | Ran 109 tests in 3.507s; OK (exit code 0) |
| Ruff lint and format check | src/api (`python3 -m ruff check . && python3 -m ruff format --check .`) | Passed | All checks passed; 207 files already formatted (exit code 0) |
| Mypy strict type check | src/api (`MYPYPATH=../core/src:src python3 -m mypy src tests/test_technical_quality_screens_wcag.py tests/test_housing_resident_screen_wcag.py`) | Passed | Success: no issues found in 30 source files (exit code 0) |
| Test naming check | `python3 tools/rename-zava-tests.py` | Passed | Ran 25 tests in 0.580s; OK (exit code 0) |
| Web Interface Guidelines refresh and audit | src/api/src/zava_forward/api/web/style.css against fetched command.md | Passed | 0 violations (`pass` on standalone Fluent 2 focus-token rules and existing scroll-margin-top rules) |
| Git author identity and diff hygiene | local `.git` config, `git diff -- src/`, `git status --short` | Passed | `8036360+jmservera@users.noreply.github.com` set locally; zero `.copilot-tracking/` substrings in `src/`; worktree inventory clean |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all checked `[x]` in plan and `Complete` in phase details).
* Completed-work evidence and handoff prose: Current and synchronized across plan, phase details, and changes record.
* Validation, blockers, remaining work, and follow-up items: Current (`0` blockers, `0` remaining active-plan markers, `3` deferred follow-up items mirrored cleanly).
* Review readiness: Ready for single-pass `rpi-review`.

## Blockers

* None

## Remaining Work

* None in active plan scope (`P01` and `P02` complete). Following single-pass `rpi-review` artifact and state persistence, the active RPI parent performs the atomic local `git add` and `git commit` (`Refs #231` plus Copilot trailer, no push).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan.md, `## Follow-Up Items`
* Cycle 0 RV-001 and RV-003 (`ensure_ascii=False` in `json.dumps(tree)` inside `src/api/tests/test_technical_quality_screens_wcag.py` and Cycle 0 prose cleanup): Outside immediate surgical CI rebase fix scope; retained for post-Review user selection.
* Cycle 0 RV-002 (extend `qualityAcceptanceGap(r)` in `src/api/src/zava_forward/api/web/app.js` to check `defect.fixed_by` alongside `submitted_by`): Outside immediate CSS rebase regression scope; retained for post-Review user selection.
* External human assistive-technology and role-representative validation (`#151`, `#155`): Requires human NVDA/VoiceOver and zoom walkthrough before Issue #231 closes (`Refs #231` preserved).

## Return-to-Caller State

* Implementation execution status: Complete (full plan)
* Declared scope and markers: full plan; completed P01, P01-T01, P01-T02, P02, P02-T01, P02-T02; remaining none
* Validation coverage: 109 WCAG/baseline unit tests passed, ruff check/format passed, mypy passed (30 files), rename-zava-tests.py passed (25 tests), refreshed Web Interface Guidelines audit passed (0 violations), local git noreply email configured
* Blockers: None
* Current plan and detail updates: None during implementation
* Planning and critique state: Ready (PC-001, PC-002, PC-003 resolved prior to implementation)
* Follow-up items: Cycle 0 RV-001/RV-003, Cycle 0 RV-002, and external AT sign-off (#151, #155)
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)

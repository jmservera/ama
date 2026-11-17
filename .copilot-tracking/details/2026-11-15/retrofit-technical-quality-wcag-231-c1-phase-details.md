<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 231 Cycle 1 Rebase CSS Focus Rule Recovery (PR 1767)

## Metadata

* Task ID: 2026-11-15-retrofit-technical-quality-wcag-231-c1
* Task slug: retrofit-technical-quality-wcag-231-c1
* Related plan: .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-c1-research.md, src/api/src/zava_forward/api/web/style.css, src/api/tests/test_housing_resident_screen_wcag.py, src/api/tests/test_technical_quality_screens_wcag.py, docs/reference/research/ux/wcag-conformance-baseline.md

## Phase Index

| Phase ID | Name                                                                     | Status   | Detail sections        |
|----------|--------------------------------------------------------------------------|----------|------------------------|
| P01      | Restore standalone programmatic focus CSS rule and guard regression      | Complete | P01, P01-T01, P01-T02  |
| P02      | Validate focused WCAG, static-analysis, and repository gates and prepare commit hygiene | Complete | P02, P02-T01, P02-T02  |

<!-- rpi:phase id=P01 -->
## P01: Restore standalone programmatic focus CSS rule and guard regression

### Context

Research evidence (`C3`, `C4`, `C5`, `C6`, `C7`, `W1` in .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-c1-research.md) established that parent commit fe6398197 introduced standalone `[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` in src/api/src/zava_forward/api/web/style.css, and rebase commit db52dfff4 merged `.screen-record h2[tabindex="-1"]:focus-visible` into that same selector list. Sibling Issue #229's `test_workspace_jump_nav_and_click_activation_focus_target_headings` in src/api/tests/test_housing_resident_screen_wcag.py requires `{` immediately after `[tabindex="-1"]:focus`, while Issue #231's `test_focus_ring_and_screen_css_invariants` in src/api/tests/test_technical_quality_screens_wcag.py requires `{` immediately after `.screen-record h2[tabindex="-1"]:focus-visible`.

### Intent

Split the merged focus rule into two consecutive standalone CSS rules with identical Fluent 2 dual-ring focus declarations and lock that standalone invariant in Issue #231's WCAG unit test module.

### Boundaries

* Included: Canonical stylesheet edit in src/api/src/zava_forward/api/web/style.css and `1` focused regex assertion addition (`0` test removals) in src/api/tests/test_technical_quality_screens_wcag.py; `none` generated targets exist.
* Excluded: Edits to sibling test files (`src/api/tests/test_housing_resident_screen_wcag.py`, `src/api/tests/test_data_steward_screen_wcag.py`), `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/index.html`, or unrelated CSS rules.

### Likely Targets

* src/api/src/zava_forward/api/web/style.css: Split the combined programmatic focus selector rule immediately below `.screen-evidence th, .screen-evidence td { font-variant-numeric: tabular-nums; }` into two consecutive standalone rules.
* src/api/tests/test_technical_quality_screens_wcag.py: Add one `self.assertRegex` check for standalone `[tabindex="-1"]:focus` inside `test_focus_ring_and_screen_css_invariants`.

### Dependencies

* None

### Validation Expectations

* Semantic and regression coverage: `test_focus_ring_and_screen_css_invariants` verifies both standalone CSS focus contracts (`[tabindex="-1"]:focus` for programmatic focus targets across pointer/keyboard jump activation and `.screen-record h2[tabindex="-1"]:focus-visible` for Issue #231 record headings) while `test_workspace_jump_nav_and_click_activation_focus_target_headings` in src/api/tests/test_housing_resident_screen_wcag.py verifies sibling #229's jump-link contract.

### Completion Evidence

* Clean diff in src/api/src/zava_forward/api/web/style.css and src/api/tests/test_technical_quality_screens_wcag.py recorded in .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md, with both WCAG test suites passing.

### Unresolved Items

* None

<!-- rpi:task id=P01-T01 -->
### P01-T01: Split merged programmatic focus rule in workbench stylesheet

#### Context

In src/api/src/zava_forward/api/web/style.css, the final rule currently combines `[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible`. Keeping both selectors as separate consecutive rules restores exact line-level parity with parent fe6398197 for `[tabindex="-1"]:focus` while keeping `.screen-record h2[tabindex="-1"]:focus-visible` intact for Issue #231 (`C3`, `C4`, `C5`, `C6`, `C7`, `C8`).

#### Intent

Replace the single comma-merged rule in src/api/src/zava_forward/api/web/style.css with two consecutive standalone rules using the repository's Fluent 2 dual-ring focus tokens (`--focus-w`, `--focus-ink`, `--focus-off`, `--focus`).

#### Boundaries

* Included: Only the merged `[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible` rule at the end of src/api/src/zava_forward/api/web/style.css.
* Excluded: All other selectors, custom properties, `@media` queries, `position:fixed` rules, and `.screen-*` layout rules in src/api/src/zava_forward/api/web/style.css.

#### Likely Targets

* src/api/src/zava_forward/api/web/style.css: Replace merged rule with standalone `[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` and standalone `.screen-record h2[tabindex="-1"]:focus-visible { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }`.

#### Dependencies

* None

#### Validation Expectations

* `git show fe6398197:src/api/src/zava_forward/api/web/style.css` line for `[tabindex="-1"]:focus` matches the restored standalone rule byte-for-byte, and `test_housing_resident_screen_wcag.py`, `test_data_steward_screen_wcag.py`, `test_technical_quality_screens_wcag.py`, `test_accessibility_baseline.py`, and `test_design_system.py` all pass.

#### Completion Evidence

* `git diff src/api/src/zava_forward/api/web/style.css` shows exact two-rule split and passing unit test runs.

#### Unresolved Items

* None

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add standalone programmatic focus regex guard in Issue 231 WCAG tests

#### Context

Issue #231's `TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants` in src/api/tests/test_technical_quality_screens_wcag.py currently checks `:focus-visible{outline:` and `.screen-record h2[tabindex="-1"]:focus-visible\s*\{`, which allowed a rebase merge to place `.screen-record h2[tabindex="-1"]:focus-visible` second after `[tabindex="-1"]:focus,` without failing `#231`'s own test file (`C5`, `C6`).

#### Intent

Add a single `self.assertRegex` assertion in `TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants` verifying `r'\[tabindex="-1"\]:focus\s*\{\s*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)'` so `#231`'s test file catches any future selector re-merging directly.

#### Boundaries

* Included: Maximum `1` assertion addition in `TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants` inside src/api/tests/test_technical_quality_screens_wcag.py; `none` removals; `none` new test classes or files; no `.copilot-tracking/` citations in test code or comments.
* Excluded: Modifying any other test method or sibling test module.

#### Likely Targets

* src/api/tests/test_technical_quality_screens_wcag.py: `TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants`.

#### Dependencies

* P01-T01

#### Validation Expectations

* Semantic vs regression coverage: Guards the standalone `[tabindex="-1"]:focus` CSS contract directly in `#231`'s own WCAG suite (would fail against HEAD db52dfff4 prior to P01-T01 and passes after P01-T01), passes `ruff check`, `ruff format --check`, `mypy`, and `tools/rename-zava-tests.py`.

#### Completion Evidence

* Passing execution of `src/api/tests/test_technical_quality_screens_wcag.py` and clean `ruff`/`mypy` checks on `tests/test_technical_quality_screens_wcag.py`.

#### Unresolved Items

* None

<!-- rpi:phase id=P02 -->
## P02: Validate focused WCAG, static-analysis, and repository gates and prepare commit hygiene

### Context

Caller Required Fix items 4 and 5 require running focused validation across `#231` and sibling WCAG/baseline suites, `ruff`, `mypy`, `tools/rename-zava-tests.py`, and refreshed `web-design-guidelines` checks, configuring repository-local git noreply identity, and verifying worktree hygiene across all Cycle 1 and parent state files (`C1`, `C8`, `W1`, `PC-001`, `PC-003`) so the active RPI parent can freeze one atomic local commit immediately after single-pass read-only `rpi-review` completes.

### Intent

Execute all focused validation checks, reconcile implementation tracking evidence, configure local git noreply `user.email`, and verify pre-review worktree hygiene without circular review dependencies.

### Boundaries

* Included: Running unittest across the 10 verified WCAG and baseline modules in `src/api/tests/`, running `ruff check .`, `ruff format --check .`, and `mypy` in `src/api`, running `python3 tools/rename-zava-tests.py`, refreshing `web-design-guidelines` and auditing changed lines in src/api/src/zava_forward/api/web/style.css in `file:line` format, completing `.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md`, setting local git noreply `user.email`, and auditing `git status --short` across all expected Cycle 1 files plus `.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json`.
* Excluded: Executing `git commit` prematurely before `rpi-review` writes its review log, full repository multi-service test suites unless a focused check fails, `git push`, `git rebase`, or modifying remote PR state.

### Likely Targets

* .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md: Record implementation changes, `web-design-guidelines` `file:line` audit, git identity check, and exact validation evidence.
* .copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-c1-state.json and .copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json: Verified in worktree status for post-review atomic staging by the RPI parent.
* Local `.git` config in /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag: Configure repository-local `{id}+{login}@users.noreply.github.com`.

### Dependencies

* P01

### Validation Expectations

* Unittest command: `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_technical_quality_screens_wcag.py src/api/tests/test_housing_resident_screen_wcag.py src/api/tests/test_data_steward_screen_wcag.py src/api/tests/test_programme_screen_wcag.py src/api/tests/test_finance_screen_wcag.py src/api/tests/test_finance_grants_screen_wcag.py src/api/tests/test_finance_screens_wcag_225.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py src/api/tests/test_design_system.py` exits `0`.
* Lint, format, and type-check command: `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && MYPYPATH=../core/src:src python3 -m mypy src tests/test_technical_quality_screens_wcag.py tests/test_housing_resident_screen_wcag.py)` exits `0`.
* Repository test-naming check: `python3 tools/rename-zava-tests.py` exits `0` with no uncommitted renames left behind.
* Web Interface Guidelines refresh and audit: Fetch current `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (or disclose any retrieval limitation per .github/copilot-instructions.md) and review modified lines in src/api/src/zava_forward/api/web/style.css in `file:line` format (`0` violations).

### Completion Evidence

* Zero-exit outputs for all validation commands, `web-design-guidelines` `file:line` audit result, and verified repository-local noreply `user.email` recorded in `.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md`.

### Unresolved Items

* None

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused WCAG unit tests, ruff, mypy, test-rename, and Web Interface Guidelines validation

#### Context

Research (`C1`, `C8`, `W1`) mapped the caller's shorthand `test_quality_finance_screen_wcag.py` to `#231`'s actual `src/api/tests/test_technical_quality_screens_wcag.py` plus the worktree's finance WCAG modules (`test_finance_screen_wcag.py`, `test_finance_grants_screen_wcag.py`, `test_finance_screens_wcag_225.py`) and `#229`'s `test_data_steward_screen_wcag.py` alongside `test_housing_resident_screen_wcag.py`, `test_programme_screen_wcag.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, and `test_design_system.py`, and `.github/copilot-instructions.md` requires refreshing `web-design-guidelines` with `file:line` audit reporting on modified web files.

#### Intent

Run the complete focused unittest selector list, `ruff check .`, `ruff format --check .`, `mypy`, `python3 tools/rename-zava-tests.py`, and refreshed `web-design-guidelines` `file:line` review of `src/api/src/zava_forward/api/web/style.css` from /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag and record exact pass counts and audit output in `.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md`.

#### Boundaries

* Included: Focused validation commands, refreshed `web-design-guidelines` `file:line` audit on `src/api/src/zava_forward/api/web/style.css`, and changes-record documentation.
* Excluded: Unrelated service suites (`mssql`, `src-orchestrator`, `src-importer`) that already passed in hosted CI job run and have zero changed files.

#### Likely Targets

* .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md: Validation results, `web-design-guidelines` audit, and reconciled completion markers.

#### Dependencies

* P01-T01, P01-T02

#### Validation Expectations

* Every listed test module, linter, formatter, type checker, and test-rename check exits `0`, and `web-design-guidelines` `file:line` review of `src/api/src/zava_forward/api/web/style.css` reports zero violations.

#### Completion Evidence

* Exact test counts, tool exit statuses, and `web-design-guidelines` `file:line` audit recorded in `.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md`.

#### Unresolved Items

* None

<!-- rpi:task id=P02-T02 -->
### P02-T02: Configure repository-local git noreply identity and verify pre-review worktree hygiene

#### Context

Caller Required Fix item 5 and `.github/copilot-instructions.md` require configuring repository-local `{id}+{login}@users.noreply.github.com` via `gh api user`, verifying zero `.copilot-tracking/` citations in production/test code, and ensuring all expected Cycle 1 files plus modified parent state `.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json` are accounted for (`PC-001`). Separating pre-review commit hygiene (`P02-T02`) from the RPI parent's post-`rpi-review` atomic `git commit` keeps `rpi-review` strictly read-only on `plan.md`, `phase-details.md`, and `changes.md` while ensuring `git status --short` ends completely empty after the parent's final commit.

#### Intent

Query `gh api user`, configure `git config --local user.email "{id}+{login}@users.noreply.github.com"` in /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag, verify source/test diffs contain zero `.copilot-tracking/` substrings, and confirm `git status --short` lists only expected Cycle 1 source, test, and tracking files (including `.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json`).

#### Boundaries

* Included: Local `git config --local user.email`, diff hygiene audit, and `git status --short` audit in /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag.
* Excluded: Premature `git commit` before `rpi-review`, `git push`, or any remote GitHub mutation.

#### Likely Targets

* Local `.git` config in /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag and hygiene verification in `.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md`.

#### Dependencies

* P02-T01

#### Validation Expectations

* `git config --local --get user.email` matches `{id}+{login}@users.noreply.github.com`, `git diff -- src/` contains zero `.copilot-tracking` matches, and `git status --short` contains only expected Cycle 1 source/test/tracking paths and `.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json`.

#### Completion Evidence

* Verified local git author email and clean pre-review worktree inventory recorded in `.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md`.

#### Unresolved Items

* None

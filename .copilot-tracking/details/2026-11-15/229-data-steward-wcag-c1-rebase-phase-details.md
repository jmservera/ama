<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #229 Cycle 1 Rebase onto Updated Parent (#1764)

## Metadata

* Task ID: 229-c1-rebase
* Task slug: 229-data-steward-wcag-c1-rebase
* Related plan: .copilot-tracking/plans/2026-11-15/229-data-steward-wcag-c1-rebase-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/229-data-steward-wcag-c1-rebase-research.md, .github/copilot-instructions.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/design-system.md

## Phase Index

| Phase ID | Name                                                                       | Status      | Detail sections          |
|----------|----------------------------------------------------------------------------|-------------|--------------------------|
| P01      | Fetch Upstream Refs and Rebase PR #1764 onto Updated Parent                | Complete    | P01, P01-T01             |
| P02      | Align #229 Row Headers with #232 `screenRecordTable` and Reconcile Docs/Tests | Complete | P02, P02-T01, P02-T02    |
| P03      | Execute Focused Validation Tier, Record Changes, and Freeze Local Commit   | Complete    | P03, P03-T01             |

## Test Ownership, Target Classification, and Coverage Lock

* **Canonical production & doc targets**:
  * `src/api/src/zava_forward/api/web/role-screens.js` (canonical JS role-screens module; zero generated bundle exists because static files are served directly).
  * `docs/reference/log.md` (append-only knowledge-base log).
  * `docs/reference/research/ux/customer-journeys/data.md` (data steward & digital operator journey engineering-evidence note).
* **Generated targets**: `none` (no build/transpile artifact exists for `src/api/src/zava_forward/api/web/`).
* **Applicable test ownership**:
  * `src/api/tests/test_data_steward_screen_wcag.py` (primary semantic WCAG 2.2 unit suite for `#229` + rebase coexistence with `#232`).
  * `src/api/tests/test_exception_register_screen.py` (regression contract suite for `#135`/`#229` exception register read-only rendering and table header scopes).
  * Read-only regression suites executed without modification: `test_housing_resident_screen_wcag.py` (`#232`), `test_programme_screen_wcag.py` (`#230`), `test_same_home_profile_journey_acceptance.py` (`#134`), `test_data_operator_screen.py`, `test_data_operator_ai_state.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_role_screens_conformance.py`, `test_design_system.py`, `test_content_standard.py`.
* **Exact test removals**: `none`.
* **Maximum test additions**: At most `2` focused test methods added/extended in `src/api/tests/test_data_steward_screen_wcag.py` (verifying `<th scope="row">` across register/summary/home tables and `#232` `screenRecordTable`/`stateCue`/`residentJumpNav` coexistence), plus updating the 2-line `th` scope check in `src/api/tests/test_exception_register_screen.py` (`test_tables_use_shared_labelled_pattern`).
* **Semantic vs regression coverage**:
  * *Semantic*: Node VM tree evaluation of `role-screens.js` verifying `thead th[scope="col"]`, `tbody tr > th:first-child[scope="row"]`, `tbody tr > td` data cells, `nav[aria-label]` `a[data-jump]` 1-to-1 `section[tabindex="-1"]` targets, and fail-closed `State:` / `Source state:` cues across `data-operator` and `#232` resident/housing screens.
  * *Regression*: Counted baseline guards (`test_accessibility_baseline`, `test_epic149_form_error_summary_associations`, `test_list_export_inventory`), design-system/content-standard rules, and `#134`/`#230`/`#232` acceptance suites.

<!-- rpi:phase id=P01 -->
## P01: Fetch Upstream Refs and Rebase PR #1764 onto Updated Parent

### Context

PR `#1764` (`feat/ux-229-data-steward-wcag` at `364e87384`) branched from `5536c3907` (`#1755`). Since then, `origin/feat/demo-233-same-home-tensions-0825` advanced through `bcaec70f9` (`#1759` / `#134`), `efe14ef3d` (`#1762` / `#230`), and `321a22960` (`#1763` / `#232`). Read-only `git merge-tree --write-tree` in Research (`C2`–`C5`) confirmed a clean 3-way merge without conflict markers. Note that untracked `.copilot-tracking/` Cycle 1 files exist in the worktree during RPI execution; git rebase preserves untracked non-colliding files automatically, and verifying their presence before and after `git rebase` prevents tracking loss.

### Intent

Configure privacy-safe git commit identity, fetch the latest remote parent and `#135` branch refs, inspect whether any additional commit (such as `#135`) landed on `origin/feat/demo-233-same-home-tensions-0825`, and rebase `feat/ux-229-data-steward-wcag` onto `origin/feat/demo-233-same-home-tensions-0825`.

### Boundaries

* Included: Local `git config --local user.email`, `git fetch origin`, inspection of `origin/feat/demo-233-same-home-tensions-0825` log, and `git rebase origin/feat/demo-233-same-home-tensions-0825`.
* Excluded: Pushing to `origin`, rebasing unrelated worktrees, or modifying upstream commits.

### Likely Targets

* `.git/config` (worktree-local or repo-local user email configuration if not already noreply).
* Branch `feat/ux-229-data-steward-wcag` git history in `/home/azureuser/source/ama-demo-wt/feat-229-data-steward-wcag`.

### Dependencies

* None.

### Validation Expectations

* `git config --get user.email` ends with `@users.noreply.github.com`.
* `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD` exits `0`.
* `git diff origin/feat/demo-233-same-home-tensions-0825..HEAD -- src/api/src/zava_forward/api/web/app.js src/api/src/zava_forward/api/web/style.css src/api/tests/test_housing_resident_screen_wcag.py` produces empty output.

### Completion Evidence

* Rebased commit SHA atop `origin/feat/demo-233-same-home-tensions-0825` recorded in `.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-c1-rebase-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure Git Noreply Identity, Fetch Parent & #135 Refs, and Rebase Branch

#### Context

`.github/copilot-instructions.md` requires setting `user.email` to `{id}+{login}@users.noreply.github.com` from `gh api user` before committing. Also, the caller prompt mentions `git fetch origin feat/demo-233-same-home-tensions-0825 feat/135-exception-feeds-queue-ui-1953`, whereas on `origin` `#135`'s branch is `feat/ux-135-exception-queue-2330` (`C1`). Fetching `feat/demo-233-same-home-tensions-0825` first and checking `git ls-remote --heads origin '*135*'` avoids a non-zero exit if `feat/135-exception-feeds-queue-ui-1953` does not exist while fetching whichever `#135` remote ref exists.

#### Intent

Ensure noreply git identity, fetch current parent and `#135` refs safely, check whether `#135` merged into `origin/feat/demo-233-same-home-tensions-0825`, and rebase `feat/ux-229-data-steward-wcag` onto `origin/feat/demo-233-same-home-tensions-0825`.

#### Boundaries

* Included: `gh api user` check, `git config --local user.email`, `git fetch`, conflict resolution if `#135` merged in the interim (preserving both `#135` and `#229` `docs/reference/log.md` entries), and `git rebase`.
* Excluded: Any `git push`.

#### Likely Targets

* `/home/azureuser/source/ama-demo-wt/feat-229-data-steward-wcag` branch `feat/ux-229-data-steward-wcag`.

#### Dependencies

* None.

#### Validation Expectations

* `git status` shows rebase finished cleanly on `feat/ux-229-data-steward-wcag` with `origin/feat/demo-233-same-home-tensions-0825` as `HEAD~1`.

#### Completion Evidence

* `git log --oneline -n 5` output confirming `HEAD~1` equals `origin/feat/demo-233-same-home-tensions-0825`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Align #229 Row Headers with #232 `screenRecordTable` and Reconcile Docs/Tests

### Context

With `#232` (`321a22960`) present on the rebased base, `screenRecordTable(label, headings, rows, limit = 50)` is available in `src/api/src/zava_forward/api/web/role-screens.js`. Upgrading `#229`'s 8 tables (`exceptionRegisterPanel`'s 2 tables, `data-operator.summary`'s 2 tables with `limit = Infinity`, and `data-operator.render`'s 4 tables) from `screenTable` to `screenRecordTable` gives every stewardship and operator table semantic `<th scope="row">` first-column headers (WCAG 1.3.1) while keeping `#232`'s `screenRecordTable`, `stateCue`, `residentJumpNav`, `ROLE_HASH_SCREENS`, and `[tabindex="-1"]` CSS helpers untouched (`C2`–`C8`, `C11`). Post-rebase `docs/reference/log.md` also requires a single blank line before `#229`'s `## [2026-11-15]` heading (`C12`).

### Intent

Adopt `screenRecordTable` on all 8 `#229` tables in `role-screens.js`, update `test_data_steward_screen_wcag.py` and `test_exception_register_screen.py` to assert row headers and `#232`/`#229` coexistence, and update `docs/reference/log.md` and `docs/reference/research/ux/customer-journeys/data.md`.

### Boundaries

* Included: `src/api/src/zava_forward/api/web/role-screens.js` (`#229` table calls only), `src/api/tests/test_data_steward_screen_wcag.py`, `src/api/tests/test_exception_register_screen.py`, `docs/reference/log.md`, `docs/reference/research/ux/customer-journeys/data.md`.
* Excluded: Editing `#232`, `#230`, or `#134` functions in `role-screens.js`, `app.js`, `style.css`, or deleting any existing test.

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: Switch `#229`'s 8 `screenTable(...)` calls (`"Exception items returned for you"` with `Infinity`, `"Source conflicts with every returned value"` with `Infinity`, `"Source conflicts by home with both values"` with `Infinity`, `"Returns and reopens by home"` with `Infinity`, `"Source conflicts with both values and source details"`, `"Recorded returns and reopens"`, `"Open exceptions and prerequisites"`, `"Recorded stock query events"`) to `screenRecordTable(...)`.
* `src/api/tests/test_data_steward_screen_wcag.py`: Update `test_home_and_summary_tables_are_keyboard_focusable_named_and_scoped` to check `overviewExceptions`, `summary`, and `home` tables for `thead th[scope="col"]` and `tbody tr > th:first-child[scope="row"]`, and add a focused `#232` + `#229` rebase coexistence test verifying `resident-service-issues`, `resident-choice`, and `data-operator` jump nav, `screenRecordTable`, and `stateCue` helpers together.
* `src/api/tests/test_exception_register_screen.py`: Update `test_tables_use_shared_labelled_pattern` so `thead` `<th>` asserts `scope == "col"` and `tbody` row cell 0 asserts `th[scope="row"]`.
* `docs/reference/log.md` & `docs/reference/research/ux/customer-journeys/data.md`: Ensure blank line before `#229`'s `## [2026-11-15]` section and note `th[scope="row"]` row headers via `screenRecordTable`.

### Dependencies

* P01 completed (`screenRecordTable` present from rebased parent `#232`).

### Validation Expectations

* `node --check src/zava_forward/api/web/role-screens.js` exits `0`.
* `PYTHONPATH=../core/src:../agents/src:src python3 -m unittest tests.test_data_steward_screen_wcag tests.test_exception_register_screen tests.test_data_operator_screen tests.test_data_operator_ai_state tests.test_housing_resident_screen_wcag -v` exits `0`.

### Completion Evidence

* Clean `git diff origin/feat/demo-233-same-home-tensions-0825` showing `#232` lines untouched and `#229` tables rendering `<th scope="row">`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Adopt `screenRecordTable` Across #229 Tables and Pin Row-Header & Coexistence Tests

#### Context

Research `C3`, `C6`, `C7`, `C8`, and `C11` confirmed all 8 `#229` tables carry record identifiers in column 0 (`Reference`, `Home`, `Query`, `Recorded`, `Step`, `Event`) and only `test_data_steward_screen_wcag.py` and `test_exception_register_screen.py` asserted `all th == "col"`. Note that `screenRecordTable(label, headings, rows, limit = 50)` defaults `limit` to `50`, whereas BOTH `exceptionRegisterPanel` tables (`"Exception items returned for you"` and `"Source conflicts with every returned value"`) AND BOTH `data-operator.summary` queue tables (`"Source conflicts by home with both values"` and `"Returns and reopens by home"`) explicitly pass `Infinity` so no exception, conflict, or return row is truncated; passing `Infinity` as the 4th argument on all 4 of those `screenRecordTable` calls (`PC-001`) preserves unlimited rendering!

#### Intent

Switch the 8 `#229` `screenTable` calls to `screenRecordTable` (preserving `Infinity` on both `exceptionRegisterPanel` tables and both `summary` tables) and update `test_data_steward_screen_wcag.py` and `test_exception_register_screen.py` to pin row headers and `#232`/`#229` coexistence.

#### Boundaries

* Included: 8 call sites in `role-screens.js`, scope assertions + coexistence test in `test_data_steward_screen_wcag.py`, and `thead`/`tbody` scope split in `test_exception_register_screen.py`.
* Excluded: Changing `screenTable` or `screenRecordTable` definitions, changing table column order or wording, or removing tests.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`
* `src/api/tests/test_data_steward_screen_wcag.py`
* `src/api/tests/test_exception_register_screen.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* All `#229`, `#135`, and `#232` unit suites pass with `<th scope="row">` verified across `overviewExceptions`, `summary`, and `home` views.

#### Completion Evidence

* Passing `unittest` run of `tests.test_data_steward_screen_wcag`, `tests.test_exception_register_screen`, and `tests.test_housing_resident_screen_wcag`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile `docs/reference/log.md` Blank-Line Ordering and `customer-journeys/data.md`

#### Context

Research `C12` demonstrated that rebasing `#229` onto `#134` (`bcaec70f9`) concatenates `## [2026-11-15] update | Issue #229...` directly below `#134`'s paragraph without a blank line. Furthermore, `#229`'s entry in `docs/reference/log.md` and `docs/reference/research/ux/customer-journeys/data.md` should accurately mention `th[scope="row"]` row headers (`screenRecordTable`) alongside jump navigation and textual state labels while preserving upstream entries (`#134`, and `#135` if merged) untouched.

#### Intent

Restore single blank-line separation before `#229`'s `## [2026-11-15]` heading in `docs/reference/log.md` and keep `#229`'s engineering-evidence summary in `docs/reference/log.md` and `docs/reference/research/ux/customer-journeys/data.md` accurate and non-overclaiming.

#### Boundaries

* Included: Blank-line separation and `#229` paragraph refinement in `docs/reference/log.md` and `docs/reference/research/ux/customer-journeys/data.md`.
* Excluded: Editing or reordering any prior entry in `docs/reference/log.md`.

#### Likely Targets

* `docs/reference/log.md`
* `docs/reference/research/ux/customer-journeys/data.md`

#### Dependencies

* P02-T01.

#### Validation Expectations

* Visual/grep verification of `tail -n 30 docs/reference/log.md` confirms clean blank lines around every `## [` heading and intact upstream entries.

#### Completion Evidence

* Clean diff of `docs/reference/log.md` and `docs/reference/research/ux/customer-journeys/data.md`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Execute Focused Validation Tier, Record Changes, and Freeze Local Commit

### Context

The caller specified a Focused validation tier in `src/api` covering 8 `unittest` targets (noting `#1763` named its module `tests.test_housing_resident_screen_wcag`, singular `screen`), `ruff check src tests checks`, `ruff format --check src tests checks`, and `mypy`, followed by committing Cycle 1 rebase artifacts locally with Conventional Commit + Copilot trailer and **not pushing**.

### Intent

Execute all Focused validation checks plus `node --check` and sibling regression tests, reconcile plan/detail markers and `.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-c1-rebase-changes.md`, and record a clean local commit (updated after `rpi-review` writes its final review/state files so `git status` is completely clean and unpushed).

### Boundaries

* Included: Focused `unittest`, `ruff`, `mypy`, `node --check`, `.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-c1-rebase-changes.md`, plan/details checkbox reconciliation, and local `git commit`.
* Excluded: `git push`, unrelated formatting churn, or `.copilot-tracking/` path mentions in commit messages.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-c1-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/229-data-steward-wcag-c1-rebase-plan.md`
* `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-c1-rebase-phase-details.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/229-data-steward-wcag-c1-rebase-state.json`

### Dependencies

* P02.

### Validation Expectations

* `node --check src/zava_forward/api/web/role-screens.js src/zava_forward/api/web/app.js` exits `0`.
* `PYTHONPATH=../core/src:../agents/src:src python3 -m unittest tests.test_data_steward_screen_wcag tests.test_housing_resident_screen_wcag tests.test_accessibility_baseline tests.test_epic149_form_error_summary_associations tests.test_list_export_inventory tests.test_role_screens_conformance tests.test_design_system tests.test_content_standard tests.test_exception_register_screen tests.test_data_operator_screen tests.test_data_operator_ai_state tests.test_programme_screen_wcag tests.test_same_home_profile_journey_acceptance -v` exits `0`.
* `python3 -m ruff check src tests checks` exits `0`.
* `python3 -m ruff format --check src tests checks` exits `0`.
* `python3 -m mypy` exits `0`.

### Completion Evidence

* Zero-exit outputs recorded in `.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-c1-rebase-changes.md`, clean `git status`, and unchanged `origin/feat/ux-229-data-steward-wcag` remote ref.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run Focused Validation Suites, Write Changes Record, and Create Local Commit Candidate

#### Context

All Focused tier checks run offline in `src/api` without reading private datasets. Note that `rpi-research` and `.github/copilot-instructions.md` forbid `.copilot-tracking/` references in commit messages even when `.copilot-tracking/` artifacts are staged in the commit (matching sibling Cycle 1 commits `efe49f0c6` and `01cd17c98`).

#### Intent

Verify all tests, linters, formatters, and static type checks pass, reconcile RPI implementation tracking, and create the local Conventional Commit candidate with `Refs #229` and Copilot trailer without pushing (`PC-002`: after `rpi-review` writes `review.md` and transitions `state.json` to `Follow-up` with zero post-Review production edits, fold those two tracking artifacts into the local Cycle 1 commit via `--amend` so `git status --short` ends completely empty).

#### Boundaries

* Included: Running validation commands in `src/api`, reconciling plan/details/changes/state files, and creating the local commit.
* Excluded: Pushing to `origin` or referencing `.copilot-tracking/` in the commit message.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-c1-rebase-changes.md`
* Local git commit on `feat/ux-229-data-steward-wcag`

#### Dependencies

* P02-T01, P02-T02.

#### Validation Expectations

* All 5 validation commands exit `0`; `git log -1` shows Conventional Commit header, `Refs #229`, Copilot trailer, noreply author email, and zero `.copilot-tracking/` text.

#### Completion Evidence

* Recorded command summaries and commit SHA in `.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-c1-rebase-changes.md`.

#### Unresolved Items

* None.

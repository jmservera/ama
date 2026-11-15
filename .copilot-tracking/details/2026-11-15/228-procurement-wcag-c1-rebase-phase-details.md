<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #228 Cycle 1 Parent Rebase onto Updated Parent (#1639)

## Metadata

* Task ID: issue-228-c1-parent-rebase
* Task slug: 228-procurement-wcag-c1-rebase
* Related plan: .copilot-tracking/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/228-procurement-wcag-c1-rebase-research.md (`C1`–`C12`, `W1`), `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/ops.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_procurement_contractor_screen_wcag.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`

## Phase Index

| Phase ID | Name                                                                              | Status   | Detail sections |
|----------|-----------------------------------------------------------------------------------|----------|-----------------|
| P01      | Git Identity Setup, Parent Rebase, and Route Conflict Resolution                  | Complete | P01, P01-T01    |
| P02      | `screenRecordTable` Row-Header Alignment, Baseline Verification, and Coexistence Tests | Complete | P02, P02-T01    |
| P03      | Focused Tier Validation and Clean Frozen Local Commit                             | Complete | P03, P03-T01    |

<!-- rpi:phase id=P01 -->
## P01: Git Identity Setup, Parent Rebase, and Route Conflict Resolution

### Context

Branch `feat/ux-228-procurement-wcag` currently points at `0486e2ca1` (1 commit ahead of merge-base `5536c3907`), while `origin/feat/demo-233-same-home-tensions-0825` has advanced 5 commits to `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` (`bcaec70f9` `#134`, `efe14ef3d` `#230`, `321a22960` `#232`, `7989f1394` `#135`, `fe6398197` `#229`) (`C1`). Read-only `git merge-tree --write-tree fe6398197 0486e2ca1` identified exactly two conflict hunks (`app.js` `isRoleScreensDestination` and `role-screens.js` `ROLE_HASH_SCREENS`) plus an adjacent auto-merged `hashBase`/`baseHash` duplicate in `app.js` `route()` (`C3`, `C4`).

### Intent

Configure repository-local noreply Git author/committer identity via `gh api user` and rebase `feat/ux-228-procurement-wcag` cleanly onto `fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, preserving all upstream commits and `#228` commits with both routing tables unioned and `route()` normalized to a single `baseHash` binding.

### Boundaries

* Included: `gh api user` local git config (`user.name` / `user.email` noreply), `git fetch origin feat/demo-233-same-home-tensions-0825`, `git rebase fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, conflict resolution in `app.js` and `role-screens.js`, and `baseHash` deduplication in `app.js` `route()`.
* Excluded: Remote pushes, global Git config changes, modifying upstream commit history, or altering unrelated views in `app.js` or `role-screens.js`.

### Likely Targets

* `.git/worktrees/feat-228-procurement-wcag/config` (or repository-local git config): Set privacy-safe `{id}+{login}@users.noreply.github.com`.
* `src/api/src/zava_forward/api/web/app.js`: Resolve `isRoleScreensDestination` with all 7 destinations (`"#/screens"` + 6 `#/role/*` routes) and unify `hashBase`/`baseHash` on `baseHash` inside `route()`.
* `src/api/src/zava_forward/api/web/role-screens.js`: Resolve `ROLE_HASH_SCREENS` with all 6 `#/role/*` screen mappings (`building_safety_lead`, `repairs`, `housing_officer`, `resident_engagement`, `procurement`, `contractor`).

### Dependencies

* None.

### Validation Expectations

* `git merge-base --is-ancestor fe63981978970e38cafed5ebe3d38eb7f9a13cf8 HEAD` exits `0`.
* `node --check src/api/src/zava_forward/api/web/app.js && node --check src/api/src/zava_forward/api/web/role-screens.js && node --check src/api/src/zava_forward/api/web/ops.js` exits `0`.

### Completion Evidence

* Completed rebase onto `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` with zero remaining conflict markers (`git diff --check` clean) and verified JavaScript syntax.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure local noreply Git identity and rebase onto `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` resolving `app.js` and `role-screens.js` conflicts

#### Context

Repository instructions require resolving the authenticated GitHub user via `gh api user` and configuring `{id}+{login}@users.noreply.github.com` locally before rebase/commit operations. During `git rebase fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, untracked `228-procurement-wcag-c1-rebase-*` files under `.copilot-tracking/` have unique filenames that do not collide with any tracked path (`C1`, `C2`). Both conflicts are additive dictionaries/sets of `#/role/*` routes (`C3`, `C4`).

#### Intent

Replay `0486e2ca1` onto `fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, unioning `#232`'s `housing_officer` / `resident_engagement` routes with `#228`'s `procurement` / `contractor` routes alongside `#227`'s `building_safety_lead` / `repairs` routes, and replacing `#228`'s `hashBase` in `app.js` `route()` with a single `const baseHash = hash.split("?")[0];` shared with `#135`'s `#/exceptions` branch.

#### Boundaries

* Included: `app.js` (`isRoleScreensDestination` and `route()`), `role-screens.js` (`ROLE_HASH_SCREENS`), and continuing rebase with Copilot trailer intact.
* Excluded: Changing `#135`'s `exceptionsView`, `#232`'s `resident-service-issues` / `resident-choice`, `#230`'s `programme-queue`, or `#229`'s `data-operator` / `exceptionRegisterPanel`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`: `isRoleScreensDestination` and `route()`.
* `src/api/src/zava_forward/api/web/role-screens.js`: `ROLE_HASH_SCREENS`.

#### Dependencies

* None.

#### Validation Expectations

* `git status` shows rebase finished on `feat/ux-228-procurement-wcag`; `git merge-base --is-ancestor fe63981978970e38cafed5ebe3d38eb7f9a13cf8 HEAD` exits `0`; `git diff --check` exits `0`; `node --check` passes on `app.js`, `ops.js`, and `role-screens.js`.

#### Completion Evidence

* Rebased commit SHA recorded atop `fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, zero conflict markers, and all 6 `#/role/*` entries present in both `app.js` and `role-screens.js`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: `screenRecordTable` Row-Header Alignment, Baseline Verification, and Coexistence Tests

### Context

Upstream `#232` (`321a22960`) added `const screenRecordTable = (label, headings, rows, limit = 50) => screenTable(label, headings, rows, limit, undefined, true);` so first-column record identifiers render as `<th scope="row">`, and `#229` (`fe6398197`) upgraded its specialist tables to `screenRecordTable` (`C5`). Meanwhile `#228`'s `0486e2ca1` upgraded `screenTable`'s default cell formatter to `(value) => screenNodeValue(value)` so DOM badge nodes (`procurementBadge(...)`) render directly in cells, while its 6 tables in `procurement-packages` and `contractor-job-pack` still called `screenTable(...)` (`rowHeader = false`) (`C5`, `C7`). Objective 2 explicitly requires preserving `#228` jump links, row headers (`scope="row"`), and textual state cues alongside upstream `#134/#230/#232/#135/#229`, and Objective 3 requires checking counted assertions in `test_accessibility_baseline.py` and `wcag-conformance-baseline.md` (`C9`, `C10`).

### Intent

Switch all six `#228` tables in `role-screens.js` to `screenRecordTable` (preserving `Infinity` vs default `50` row limits as appropriate — note none of the 6 `#228` tables pass a custom limit today; check whether prerequisite/checklist tables have `<= 6` fixed rows well under `50`), verify WCAG baseline counts remain `sites == 9`, `tables == 14`, `fixed == 2`, and add focused regression assertions in `test_procurement_contractor_screen_wcag.py` for `<th scope="row">` across all 6 `#228` tables and routing coexistence across all 6 `#/role/*` aliases.

### Boundaries

* Included:
  * Switching the 4 `screenTable(...)` calls in `procurement-packages` (`"Packages with period, scope, version and capacity"`, `"Work-order references for the selected home"`, `"Work-order corrections, recorded completion and review for the selected home"`, `` `Unmet prerequisites for ${wording(p.id)}` ``) and the 2 `screenTable(...)` calls in `contractor-job-pack` (`"Your work orders for this home"`, `"Evidence checklist for this job pack"`) to `screenRecordTable(...)` (using `Infinity` on unbounded package/prerequisite/checklist tables only where appropriate or preserving current row limits: `Packages`, `Work-order references`, `Work-order corrections`, and `Your work orders` keep default `50`; `Unmet prerequisites` (5 rows) and `Evidence checklist` (6 rows) keep default `50` as in `0486e2ca1` so existing truncation behavior in `test_procurement_screens.py` is 100% unchanged).
  * Canonical test ownership locked to `src/api/tests/test_procurement_contractor_screen_wcag.py`: exact test removals = `none`; max additions = `<= 2` test methods / subtest expansions; generated test targets = `none`; semantic coverage = `<th scope="row">` on first column of every rendered `tbody tr` and `<th scope="col">` on every `thead th` across `procurement-packages` and `contractor-job-pack`, plus `#/role/housing_officer` (`"Resident service issue queue"`) and `#/role/resident_engagement` (`"Resident choice and update queue"`) added to `test_role_hash_aliases_and_nav_active_mapping` under a `"Resident Liaison Officer"` (`choiceRoles`) session, asserting `shell_sections[1]["attrs"].get("aria-labelledby") == "screen-evidence-heading"` for those two `#232` resident routes while retaining `shell_sections[1]["attrs"].get("aria-label") == "Evidence for C-1"` for `procurement`, `contractor`, `building_safety_lead`, and `repairs` (`PC-001`, zero edits to `#232`'s `roleScreensView`).
  * Confirming `test_accessibility_baseline.py` (`sites == 9`, `tables == 14`, `fixed == 2`) and `wcag-conformance-baseline.md` require zero count edits because `screenRecordTable` delegates to existing `screenTable`.
* Excluded: Modifying `test_procurement_screens.py` (whose `cells()` helper already accepts `td` and `th`, `C8`), modifying sibling `#229/#230/#232/#135/#134` test files, or adding forbidden copy (`'human-approved'` or internal jargon).

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: Replace the 6 `#228` `screenTable(` calls inside `procurement-packages` and `contractor-job-pack` with `screenRecordTable(`.
* `src/api/tests/test_procurement_contractor_screen_wcag.py`: Expand `test_role_hash_aliases_and_nav_active_mapping` to cover all 6 `#/role/*` aliases and add 1 focused test method asserting `thead th[scope="col"]` and `tbody tr > th:first-child[scope="row"]` across all 6 `#228` tables.

### Dependencies

* P01 completed (`screenRecordTable` and `#/role/housing_officer` + `#/role/resident_engagement` present from rebased parent `fe6398197`).

### Validation Expectations

* `tests.test_procurement_contractor_screen_wcag`, `tests.test_procurement_screen_wcag`, `tests.test_procurement_qa_screen_wcag`, `tests.test_procurement_screens`, `tests.test_accessibility_baseline`, and `tests.test_content_standard` all pass.

### Completion Evidence

* All 6 `#228` tables emit `<th scope="row">` on column 0 and `<td>` on remaining columns with DOM badge nodes intact; all 6 `#/role/*` aliases verified in Node VM routing tests; baseline counters confirmed at `9 / 14 / 2`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Upgrade `#228` tables in `role-screens.js` to `screenRecordTable` and pin `scope="row"` + 6-alias coexistence tests

#### Context

In `role-screens.js`, `procurement-packages` renders 4 tables whose column 0 identifies the record (`Package`, `Work order`, `Work order`, `Prerequisite`) and `contractor-job-pack` renders 2 tables whose column 0 identifies the record (`Work order and version`, `Evidence item`) (`C7`). Upgrading those 6 calls from `screenTable(...)` to `screenRecordTable(...)` emits `<th scope="row">` on column 0 while passing `cell = undefined`, which defaults in `screenTable` to `(value) => screenNodeValue(value)` (`C5`), keeping every `procurementBadge(...)` DOM span intact in columns `1..N`.

#### Intent

Update the 6 table calls in `role-screens.js` to `screenRecordTable(...)`, extend `test_role_hash_aliases_and_nav_active_mapping` in `test_procurement_contractor_screen_wcag.py` with `("#/role/housing_officer?case=C-1", rlo_session, "Resident service issue queue")` and `("#/role/resident_engagement?case=C-1", rlo_session, "Resident choice and update queue")` using `"Resident Liaison Officer"` (`choiceRoles`) and asserting `shell_sections[1]["attrs"].get("aria-labelledby") == "screen-evidence-heading"` on those two resident routes versus `shell_sections[1]["attrs"].get("aria-label") == "Evidence for C-1"` on the other four routes (`PC-001`), and add `test_procurement_and_contractor_tables_use_col_and_row_header_scopes` verifying all 6 rendered tables (`4` on `procurement-packages` with 1 package + 1 order, `2` on `contractor-job-pack` with 1 order) emit `th[scope="col"]` headers and `th[scope="row"]` first-column body cells.

#### Boundaries

* Included: `src/api/src/zava_forward/api/web/role-screens.js` (6 call sites in `procurement-packages` and `contractor-job-pack`) and `src/api/tests/test_procurement_contractor_screen_wcag.py` (1 updated alias tuple + 1 new row-header scope test method; 0 removals).
* Excluded: Changing row-limit thresholds (`50`), altering badge wording, or touching `wcag-conformance-baseline.md` unless `test_accessibility_baseline.py` reports a count shift (research proved counts stay `9 / 14 / 2`, `C9`).

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`
* `src/api/tests/test_procurement_contractor_screen_wcag.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* Targeted Node VM unit tests in `test_procurement_contractor_screen_wcag.py`, `test_procurement_screens.py`, `test_accessibility_baseline.py`, and `test_content_standard.py` exit `0`.

#### Completion Evidence

* Passing unit test output confirming `6` tables (`4` + `2`) with `th[scope="col"]` and `th[scope="row"]` and `6` `#/role/*` hash aliases resolving cleanly.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Tier Validation and Clean Frozen Local Commit

### Context

Because upstream `fe6398197` added/updated `src/core` modules (`profile_journey_contract.py` in `#134` and `exception_feeds.py`, `exception_queue.py`, `exception_register.py` in `#135`), running `src/api` tests against stale pre-rebase site-packages could fail or mask regressions (`C11`). Invoking `/usr/bin/python3` directly inside `src/api` with `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src` preserves user-site runtime/linter packages (`aiohttp`, `ruff`, `mypy`) while guaranteeing exact working-tree imports from `src/core`, `src/agents`, and `src/api` without `uv` or `/tmp` isolation hazards (`PC-002`; `--system-site-packages` remains available if any `pip` venv fallback is ever needed).

### Intent

Execute the complete Focused Tier check suite (`node --check`, `/usr/bin/python3 -m ruff check`, `/usr/bin/python3 -m ruff format --check`, `/usr/bin/python3 -m mypy`, and the combined `unittest` matrix covering `#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline`, `test_content_standard`, and `test_role_screens_conformance`) without `uv`, record `.copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md`, commit all rebased code, test updates, and implementation-phase tracking artifacts cleanly so `git status --short` is empty entering `rpi-review`, and follow `rpi-review` with a clean tracking commit recording `reviews/logs` and `rpi-sessions` without pushing (`PC-002`).

### Boundaries

* Included:
  * Primary `/usr/bin/python3` runner inside `src/api` with `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests` (matching `unittest discover -s tests` for bare sibling imports in `tests/`; `--system-site-packages` `pip` venv fallback if ever needed; never `uv`).
  * `node --check` on `app.js`, `ops.js`, `role-screens.js`.
  * `/usr/bin/python3 -m ruff check src tests checks`, `/usr/bin/python3 -m ruff format --check src tests checks`, and `/usr/bin/python3 -m mypy` inside `src/api`.
  * `/usr/bin/python3 -m unittest` run inside `src/api` covering:
    * `#228`: `tests.test_procurement_contractor_screen_wcag`, `tests.test_procurement_screen_wcag`, `tests.test_procurement_qa_screen_wcag`, `tests.test_procurement_screens`
    * `#229`: `tests.test_data_steward_screen_wcag`, `tests.test_exception_register_screen`
    * `#230`: `tests.test_programme_screen_wcag`
    * `#232`: `tests.test_housing_resident_screen_wcag`
    * `#135`: `tests.test_exception_queue_ui`, `tests.test_epic149_form_error_summary_associations`, `tests.test_list_export_inventory`
    * `#134`: `tests.test_same_home_profile_journey_acceptance`
    * Shared UX guards: `tests.test_accessibility_baseline`, `tests.test_content_standard`, `tests.test_role_screens_conformance`, `tests.test_design_system`
  * Writing `.copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md` and committing all rebased changes + implementation-phase dated `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`) locally on `feat/ux-228-procurement-wcag` with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer and zero `.copilot-tracking/` references in commit messages so `git status --short` is empty entering `rpi-review` (with `reviews/logs` + `rpi-sessions` committed cleanly after `rpi-review`).
* Excluded: `uv`, full `tools/rpi-checks.py --all` gate, amending reviewed code after `rpi-review`, and `git push`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md`
* Local branch `feat/ux-228-procurement-wcag` commit history

### Dependencies

* P02.

### Validation Expectations

* Zero-exit across `node --check`, `ruff check`, `ruff format --check`, `mypy`, and all 16 targeted `unittest` modules; `git status --short` empty entering `rpi-review` and again after final post-review tracking commit; `origin/feat/ux-228-procurement-wcag` unchanged.

### Completion Evidence

* Exact command outputs and test counts recorded in `.copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md`, clean pre-review `git status --short`, and verified commit trailer/ancestry.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run Focused Tier checks (`node --check`, `ruff`, `mypy`, and 6-issue `unittest` matrix) via `/usr/bin/python3` + `PYTHONPATH` without `uv` and commit pre-review implementation candidate

#### Context

All six issues (`#228`, `#229`, `#230`, `#232`, `#135`, `#134`) share `role-screens.js` and/or `app.js`. Running their dedicated test suites together in one `/usr/bin/python3 -m unittest` invocation inside `src/api` with `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src` directly proves that the rebased candidate preserves every upstream slice alongside `#228` while retaining user-site `aiohttp`, `ruff`, and `mypy` (`PC-002`).

#### Intent

Run all Focused Tier static checks and the 16-module `unittest` suite via `/usr/bin/python3` + `PYTHONPATH`, reconcile plan and detail checkboxes/statuses, author `.copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md`, and commit all rebased code, test updates, and implementation-phase `.copilot-tracking/` artifacts cleanly with the Copilot trailer so `git status --short` is empty entering `rpi-review` (leaving `reviews/logs` and `rpi-sessions` for the final post-`rpi-review` tracking commit without pushing).

#### Boundaries

* Included: Static checks, 16-module `unittest` execution, RPI tracking reconciliation, and pre-review local implementation commit with Copilot trailer.
* Excluded: `uv`, remote push, or modifying unrelated files.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan.md`
* `.copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md`

#### Dependencies

* P02-T01.

#### Validation Expectations

* `ruff check`, `ruff format --check`, `mypy`, `node --check`, and all 16 `unittest` modules exit `0`; `git status --short` is empty entering `rpi-review`.

#### Completion Evidence

* Recorded validation table in `228-procurement-wcag-c1-rebase-changes.md` and clean pre-review commit atop rebased `feat/ux-228-procurement-wcag`.

#### Unresolved Items

* None.

<!-- markdownlint-disable-file -->
# RPI Plan: Issue #228 Cycle 1 Parent Rebase onto Updated Parent (#1639)

## Task Metadata

* Task ID: issue-228-c1-parent-rebase
* Task slug: 228-procurement-wcag-c1-rebase
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan-critique.md

## Executive Summary

This plan rebases PR `#1765` (Issue `#228`, branch `feat/ux-228-procurement-wcag`, currently `0486e2ca1`) onto the updated parent branch `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, which merged `#1759`/`#134`, `#1762`/`#230`, `#1763`/`#232`, `#1757`/`#135`, and `#1764`/`#229`). It resolves the two `#/role/*` hash-routing conflicts in `app.js` and `role-screens.js`, unifies the duplicate `hashBase`/`baseHash` variable in `app.js` `route()`, upgrades all six `#228` procurement and contractor tables in `role-screens.js` to `#232`'s shared `screenRecordTable` helper (`<th scope="row">`), verifies WCAG baseline counters (`sites == 9`, `tables == 14`, `fixed == 2`) and plain-language content-standard rules, runs Focused Tier validation (`ruff`, `mypy`, `node --check`, and targeted `unittest` suites across all six issues without `uv`), and produces a clean local commit with the Copilot trailer without pushing.

### User Decisions and Requirements Highlights

* Rebase `feat/ux-228-procurement-wcag` onto `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`) preserving every upstream merged slice (`#134`, `#230`, `#232`, `#135`, `#229`) and every `#228` accessibility feature.
* Preserve `#228` keyboard jump links (`role="navigation"`, `a[data-jump]`), row headers (`scope="row"`), and non-colour textual state cues (`procurementBadge` / `stateCue`).
* Reconcile counted WCAG baseline assertions only if combined file counts shift, and ensure `test_content_standard.py` passes with zero forbidden terms (never `'human-approved'`).
* Validate at the Focused Tier using `/usr/bin/python3` or a `/tmp` `pip` virtualenv (no `uv`), commit all rebased changes and `.copilot-tracking/` artifacts locally with the Copilot trailer, and do not push.

### What You May Not Know

* Wave 3 contrarian research showed that commit `0486e2ca1` (authored before `#232` merged) rendered `#228`'s six tables via `screenTable(...)` (`<td>` in column 0), whereas `#232` introduced `screenRecordTable` (`<th scope="row">`) and `#229` adopted it across its tables (`C5`, `C7`, `C8`). Switching `#228`'s six tables in `role-screens.js` to `screenRecordTable` emits `<th scope="row">` while keeping `screenNodeValue` DOM status badges intact.
* Upstream `#135` already incremented `test_accessibility_baseline.py` and `wcag-conformance-baseline.md` to `9` `aria-invalid` sites and `14` `h("table", {},` literals (`C9`, `C10`). Because `#228` reuses `screenTable`/`screenRecordTable` and adds zero `aria-invalid` or `position:fixed` sites, those counts remain `9`, `14`, and `2` after rebase.
* Upstream `#134` and `#135` added new `src/core` modules (`profile_journey_contract.py`, `exception_feeds.py`, `exception_queue.py`, `exception_register.py`), so unit tests in `src/api` must run with updated local `src/core` on `PYTHONPATH` (or freshly installed via `pip` in `/tmp` venv) rather than stale pre-rebase distributions (`C11`, `C12`).

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Fetch `origin/feat/demo-233-same-home-tensions-0825` and rebase `feat/ux-228-procurement-wcag` (`0486e2ca1`) onto `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`) in `/home/azureuser/source/ama-demo-wt/feat-228-procurement-wcag` (user prompt Objective 1; `C1`).
* Preserve all upstream merged changes from PRs `#1759` (`#134`), `#1762` (`#230`), `#1763` (`#232`), `#1757` (`#135`), and `#1764` (`#229`) alongside all `#228` procurement/supplier/contractor WCAG 2.2 jump links, row headers (`scope="row"`), and textual state cues (user prompt Objective 2; `C3`–`C8`).
* Verify and reconcile any counted accessibility baseline assertions in `src/api/tests/test_accessibility_baseline.py` and `docs/reference/research/ux/wcag-conformance-baseline.md` against the combined post-rebase files (user prompt Objective 3; `C9`, `C10`).
* Pass `src/api/tests/test_content_standard.py` and never use forbidden phrases such as `'human-approved'` or internal jargon in visible copy (user prompt Objective 4; `C12`).
* Run Focused Tier validation inside `src/api` (`ruff check`, `ruff format --check`, `mypy`, and targeted `unittest` suites covering `#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline.py`, and `test_content_standard.py`) using `/usr/bin/python3` or a `/tmp` virtualenv with `pip` only and no `uv` (user prompt Validation Tier).
* Commit all rebased changes and dated `2026-11-15` `.copilot-tracking/` artifacts on `feat/ux-228-procurement-wcag` with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer and a privacy-safe local GitHub noreply email, leaving `git status --short` empty without pushing to `origin` (user prompt + `.github/copilot-instructions.md`).

## Goals

* Rebase `feat/ux-228-procurement-wcag` cleanly atop `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` with zero dropped hunks from `#134`, `#230`, `#232`, `#135`, `#229`, or `#228`.
* Align `#228`'s procurement and contractor tables in `role-screens.js` with `#232`/`#229`'s `screenRecordTable` (`<th scope="row">`) convention while keeping non-colour DOM status badges, jump links, and vulnerability redaction intact.
* Prove cross-slice coexistence and accessibility/content compliance under Focused Tier checks and freeze a clean local commit candidate ready for coordinator exact-head review.

## Scope and Non-Goals

### In Scope

* Git rebase of `feat/ux-228-procurement-wcag` onto `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`).
* Conflict resolution and route cleanup in `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/role-screens.js`.
* Upgrading the six `#228` tables in `src/api/src/zava_forward/api/web/role-screens.js` (`procurement-packages` x4, `contractor-job-pack` x2) from `screenTable` to `screenRecordTable` (`<th scope="row">`).
* Extending `src/api/tests/test_procurement_contractor_screen_wcag.py` with focused assertions for `<th scope="row">` row headers across all six `#228` tables and coexistence of all six `#/role/*` hash aliases.
* Focused Tier static analysis (`ruff check`, `ruff format --check`, `mypy`, `node --check`) and `unittest` execution across `#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline.py`, and `test_content_standard.py`.
* Dated `2026-11-15` `.copilot-tracking/` artifacts and local commit with Copilot trailer on `feat/ux-228-procurement-wcag`.

### Non-Goals

* Pushing `feat/ux-228-procurement-wcag` to `origin` or modifying pull request state on GitHub.
* Using `uv` or mutating global Python/Git configuration.
* Altering unrelated backend, infrastructure, or sibling screen logic from `#134`, `#230`, `#232`, `#135`, or `#229`.
* Claiming WCAG 2.2 AA conformance acceptance (`#151`) or live perspective walkthrough acceptance (`#155`).

## Functional Requirements

* FR-01: Branch `feat/ux-228-procurement-wcag` rebases directly onto `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` (`origin/feat/demo-233-same-home-tensions-0825`), preserving all six `#/role/*` destinations (`building_safety_lead`, `repairs`, `housing_officer`, `resident_engagement`, `procurement`, `contractor`) in `app.js` `isRoleScreensDestination` and `role-screens.js` `ROLE_HASH_SCREENS`, and unifying `route()` hash normalization on `baseHash` (`C1`, `C3`, `C4`).
  * Observable acceptance criteria: `git merge-base --is-ancestor fe63981978970e38cafed5ebe3d38eb7f9a13cf8 HEAD` exits `0`, and Node VM route tests resolve all six `#/role/*` aliases to `#/screens` active navigation, their target `h1` headings, and their screen-specific evidence shell landmark (`aria-labelledby="screen-evidence-heading"` for `#232`'s two resident routes under a `Resident Liaison Officer` session and `aria-label="Evidence for C-1"` for the other four routes).
* FR-02: All `#228` procurement, supplier, and contractor views (`procurement-packages`, `contractor-job-pack`, `contractorListView`, `contractorCaseView`, and `workOrdersCard`) preserve keyboard jump links (`nav[role="navigation"]`, `a[data-jump]`, focusable `tabindex="-1"` target headings), non-colour textual state badges (`data-state-cue`), vulnerability redaction, and `<th scope="row">` record headers across all six `#228` tables in `role-screens.js` via `screenRecordTable` (`C5`, `C7`, `C8`, `W1`).
  * Observable acceptance criteria: Every table in `procurement-packages` (4 tables) and `contractor-job-pack` (2 tables) renders `thead th[scope="col"]` and `tbody tr > th:first-child[scope="row"]` alongside intact `data-state-cue` badges and jump-link focus behavior in `test_procurement_contractor_screen_wcag.py` and `test_procurement_screens.py`.
* FR-03: Combined web assets and UX documentation satisfy counted WCAG 2.2 baseline invariants (`sites == 9`, `tables == 14`, `fixed == 2`) and plain-language content-standard checks without introducing `'human-approved'` or banned internal terms (`C9`, `C10`, `C12`).
  * Observable acceptance criteria: `tests.test_accessibility_baseline`, `tests.test_content_standard`, and `tests.test_role_screens_conformance` pass with zero failures.
* FR-04: Upstream `#134`, `#135`, `#229`, `#230`, and `#232` functionality and tests remain regression-free alongside `#228` (`C1`, `C11`).
  * Observable acceptance criteria: Targeted `src/api` `unittest` run covering `#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline`, and `test_content_standard` passes completely.

## Non-Functional Requirements

* NFR-01: Static type safety, formatting, linting, and JavaScript syntax validity across `src/api`.
  * Objective threshold or evaluation condition: Zero diagnostics from `ruff check`, `ruff format --check`, `mypy`, and `node --check` on modified web scripts, plus pairwise disjoint top-level JS declarations across `app.js`, `ops.js`, and `role-screens.js` (`C6`).
  * Operating condition or verification approach, if needed: Executed inside `src/api` primarily via `/usr/bin/python3` with `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src` (or `--system-site-packages` `pip` venv fallback if ever needed; never `uv`).
  * Observable acceptance criteria: All four static commands exit `0` and `test_top_level_identifiers_disjoint_and_no_sys_modules_deletion` passes.
* NFR-02: Test discipline and frozen local branch hygiene.
  * Objective threshold or evaluation condition: Exact test removals = `none`; maximum new test methods/blocks added = `<= 2` in canonical target `src/api/tests/test_procurement_contractor_screen_wcag.py` (no generated test files, no `sys.modules` deletion); `P03-T01` commits all rebased code, test updates, and implementation-phase tracking artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`) cleanly before `rpi-review`, and post-`rpi-review` closeout records `reviews/logs` and `rpi-sessions` in a clean tracking commit using repository-local GitHub noreply email and Copilot trailer with `git status --short` empty and remote untouched.
  * Operating condition or verification approach, if needed: Verified via `git diff`, `git status --short`, `git log -2`, and `git rev-parse origin/feat/ux-228-procurement-wcag` unchanged.
  * Observable acceptance criteria: Working tree clean (`git status --short` empty) both entering `rpi-review` and at final closeout, `HEAD` is descendant of `fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, and zero `.copilot-tracking/` references appear in production code, tests, docs, or commit messages.

## Acceptance Criteria

* AC-01: `feat/ux-228-procurement-wcag` has `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` as an ancestor and preserves all upstream `#134`, `#230`, `#232`, `#135`, and `#229` commits cleanly.
* AC-02: `app.js` `isRoleScreensDestination` and `role-screens.js` `ROLE_HASH_SCREENS` include all six `#/role/*` routes (`building_safety_lead`, `repairs`, `housing_officer`, `resident_engagement`, `procurement`, `contractor`), and `app.js` `route()` uses a single `baseHash` binding.
* AC-03: All six `#228` tables in `role-screens.js` (`procurement-packages` x4, `contractor-job-pack` x2) use `screenRecordTable` so column 0 emits `<th scope="row">` while preserving `procurementBadge` textual state cues, jump navigation, and vulnerability redaction.
* AC-04: `test_accessibility_baseline.py` (`sites == 9`, `tables == 14`, `fixed == 2`) and `test_content_standard.py` (zero banned terms, zero `'human-approved'`) pass against the combined rebased codebase.
* AC-05: Focused Tier checks (`node --check`, `ruff check`, `ruff format --check`, `mypy`, and targeted `unittest` suites covering `#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline`, and `test_content_standard`) pass using `pip`/python3 without `uv`.
* AC-06: All rebased changes and dated `2026-11-15` `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`) are committed locally on `feat/ux-228-procurement-wcag` with the Copilot trailer and privacy-safe noreply email, `git status --short` is empty, and nothing is pushed.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan.md                                                          |
| Phase details                    | .copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md                                               |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan-critique.md with Revise disposition resolved directly (`PC-001`, `PC-002`) |
| Relevant research                | .copilot-tracking/research/2026-11-15/228-procurement-wcag-c1-rebase-research.md                                                   |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for `rpi-implement`                                                                                             |
| Continuation context             | Confirmed automatic RPI Agent parent return                                                                                        |

## Sources

* `.copilot-tracking/research/2026-11-15/228-procurement-wcag-c1-rebase-research.md`: Primary three-wave research artifact (`C1`–`C12`, `W1`) establishing exact conflict hunks, `screenRecordTable` row-header alignment, baseline counters, and sibling test module inventory.
* `src/api/src/zava_forward/api/web/app.js` & `src/api/src/zava_forward/api/web/role-screens.js`: Conflict and semantic reconciliation targets (`isRoleScreensDestination`, `route()`, `ROLE_HASH_SCREENS`, `procurement-packages`, `contractor-job-pack`).
* `src/api/src/zava_forward/api/web/ops.js`: `#228` work-order badges and `#contractor-work-orders-heading` target carried forward across rebase.
* `src/api/tests/test_procurement_contractor_screen_wcag.py`: Canonical `#228` WCAG 2.2 unit test suite (test ownership target; removals: `none`; max additions: `<= 2` methods/blocks; generated targets: `none`).
* `src/api/tests/test_accessibility_baseline.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, & `src/api/tests/test_content_standard.py`: Static WCAG 2.2 inventory and plain-language content-standard guards.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Git Identity Setup, Parent Rebase, and Route Conflict Resolution

* Intent: Configure repository-local privacy-safe Git identity, rebase `feat/ux-228-procurement-wcag` (`0486e2ca1`) onto `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`), resolve both `#/role/*` routing conflicts, and unify `baseHash` in `app.js` `route()`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Configure local noreply Git identity and rebase onto `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` resolving `app.js` and `role-screens.js` conflicts

* Requirement and evidence: FR-01, NFR-02; `.copilot-tracking/research/2026-11-15/228-procurement-wcag-c1-rebase-research.md` (`C1`–`C4`, `C6`)
* Expected result: `feat/ux-228-procurement-wcag` sits cleanly atop `fe63981978970e38cafed5ebe3d38eb7f9a13cf8` with all six `#/role/*` entries preserved in `isRoleScreensDestination` and `ROLE_HASH_SCREENS`, a single `baseHash` binding in `app.js` `route()`, and `ops.js` / `#228` commit history cleanly replayed.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: `screenRecordTable` Row-Header Alignment, Baseline Verification, and Coexistence Tests

* Intent: Upgrade all six `#228` tables in `role-screens.js` (`procurement-packages` x4, `contractor-job-pack` x2) to `screenRecordTable` (`<th scope="row">`), verify WCAG baseline counts (`9 / 14 / 2`) and content-standard invariants, and pin row-header + 6-alias coexistence assertions in `test_procurement_contractor_screen_wcag.py`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Upgrade `#228` tables in `role-screens.js` to `screenRecordTable` and pin `scope="row"` + 6-alias coexistence tests

* Requirement and evidence: FR-01, FR-02, FR-03, NFR-02; `.copilot-tracking/research/2026-11-15/228-procurement-wcag-c1-rebase-research.md` (`C5`, `C7`, `C8`, `C9`, `C10`, `C12`, `W1`); `PC-001`
* Expected result: All six tables in `procurement-packages` and `contractor-job-pack` render `<th scope="row">` on column 0 while preserving DOM `procurementBadge` cues, `test_procurement_contractor_screen_wcag.py` pins `scope="row"` and all six `#/role/*` hash aliases using `"Resident Liaison Officer"` (`choiceRoles`) and `#232`'s `aria-labelledby="screen-evidence-heading"` shell assertion on the two resident routes (zero test removals, `<= 2` focused test additions, zero edits to `#232`'s `roleScreensView`), and `test_accessibility_baseline.py` / `wcag-conformance-baseline.md` remain exact at `9 / 14 / 2`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Tier Validation and Clean Frozen Local Commit

* Intent: Execute all Focused Tier linters, type checks, JS syntax checks, and sibling unit test suites (`#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline`, `test_content_standard`) inside `src/api` primarily using `/usr/bin/python3` with `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests` (no `uv`), commit all rebased code and implementation-phase tracking artifacts cleanly before `rpi-review`, and follow `rpi-review` with a clean tracking commit recording `reviews/logs` and `rpi-sessions` without pushing.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run Focused Tier checks (`node --check`, `ruff`, `mypy`, and 6-issue `unittest` matrix) via `/usr/bin/python3` + `PYTHONPATH` without `uv` and commit pre-review implementation candidate

* Requirement and evidence: FR-03, FR-04, NFR-01, NFR-02; `.copilot-tracking/research/2026-11-15/228-procurement-wcag-c1-rebase-research.md` (`C6`, `C9`–`C12`); `PC-002`
* Expected result: `node --check`, `/usr/bin/python3 -m ruff check src tests checks`, `/usr/bin/python3 -m ruff format --check src tests checks`, `/usr/bin/python3 -m mypy`, and `/usr/bin/python3 -m unittest ...` (with `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests`) exit `0`, and all rebased changes plus implementation-phase `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`, `rpi-sessions`) are committed locally with the Copilot trailer and empty `git status --short` entering `rpi-review` (with `reviews/logs` and `rpi-sessions` committed cleanly immediately after `rpi-review` without pushing).
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md

## Dependencies

* `origin/feat/demo-233-same-home-tensions-0825` at `fe63981978970e38cafed5ebe3d38eb7f9a13cf8`: Required rebase target containing merged PRs `#1759` (`#134`), `#1762` (`#230`), `#1763` (`#232`), `#1757` (`#135`), and `#1764` (`#229`).
* Node.js (`/usr/bin/node`), Python 3.12 (`/usr/bin/python3`), `pip`, `ruff`, and `mypy`: Required local Focused Tier execution tools without `uv`.
* Local `src/core` and `src/agents` distributions / source paths: Required so `src/api` tests import updated `profile_journey_contract.py` (`#134`) and `exception_*` modules (`#135`) plus `src/core/tests/dataset.py`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass `PC-001` (`[High]`: `#232` resident routes use `choiceRoles` and `aria-labelledby="screen-evidence-heading"`) | resolved | Updated `FR-01`, `P02`, and `P02-T01` so the two added `#232` route tuples in `test_role_hash_aliases_and_nav_active_mapping` use a `"Resident Liaison Officer"` session (`choiceRoles`), assert `"Resident service issue queue"` and `"Resident choice and update queue"` `h1` headings, and assert `shell_sections[1]["attrs"].get("aria-labelledby") == "screen-evidence-heading"` for those two resident routes while keeping `aria-label == "Evidence for C-1"` for the other four routes (zero edits to `#232`'s `roleScreensView`). |
| Single-pass `PC-002` (`[Medium]`: isolated `/tmp` venv lacks user-site `aiohttp`/`ruff`/`mypy`, and pre- vs post-review commit split) | resolved | Updated `NFR-01`, `NFR-02`, `P03`, and `P03-T01` to make `/usr/bin/python3` inside `src/api` with `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src` the primary Focused Tier runner (with `--system-site-packages` if any venv fallback is needed), and split commit hygiene cleanly into `P03-T01` pre-review implementation commit (`git status --short` empty entering `rpi-review`) plus post-`rpi-review` tracking commit (`reviews/logs` + `rpi-sessions`, leaving `git status --short` empty without amending reviewed code or pushing). |

## Follow-Up Items

* Execute Chromium Playwright + axe runtime checks (`src/api/checks/specialist_keyboard_browser_check.py`) across `#/role/procurement` and `#/role/contractor` when a browser-tier validation gate runs (`owner: follow-up UX browser check`; outside Focused Tier rebase scope).
* Complete human assistive-technology testing (`#151`) and participant perspective walkthroughs (`#155`) before claiming WCAG 2.2 AA conformance acceptance or ticking human criteria on `#228` (`owner: #151 / #155`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md
* Ready phase or task: P01 (`P01-T01`)
* Remaining provisional question or blocker: none

<!-- markdownlint-disable-file -->
# Review: Issue #228 Cycle 1 Parent Rebase onto Updated Parent (#1639)

## Scope and Evidence

* Task ID: issue-228-c1-parent-rebase
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: Rebase of `feat/ux-228-procurement-wcag` (`0486e2ca1` -> `e9f74e39c`, `6efa815aa`) onto `origin/feat/demo-233-same-home-tensions-0825` (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8`, incorporating merged PRs `#1759` (`#134`), `#1762` (`#230`), `#1763` (`#232`), `#1757` (`#135`), and `#1764` (`#229`)), routing conflict reconciliation in `app.js` and `role-screens.js`, `screenRecordTable` (`<th scope="row">`) alignment across all six `#228` specialist tables, WCAG baseline count verification (`9 / 14 / 2`), plain-language content-standard preservation, Focused Tier static/unit validation without `uv`, and refreshed Web Interface Guidelines compliance.
* Plan: .copilot-tracking/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/228-procurement-wcag-c1-rebase-research.md (`C1`–`C12`, `W1`), full branch diff `fe63981978970e38cafed5ebe3d38eb7f9a13cf8..6efa815aa` across `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/ops.js`, `src/api/src/zava_forward/api/web/role-screens.js`, and `src/api/tests/test_procurement_contractor_screen_wcag.py`, Focused Tier check outputs, and refreshed Vercel Web Interface Guidelines (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`).

## Opening Review State

* Interpreted review goal: Verify once against concrete git, code, test, and refreshed Web Interface Guidelines evidence that the rebased `feat/ux-228-procurement-wcag` branch preserves all five upstream merged PRs (`#134`, `#230`, `#232`, `#135`, `#229`) alongside `#228`'s WCAG 2.2 jump links, `<th scope="row">` row headers, and textual state cues, passes Focused Tier checks without `uv`, and respects all governance, baseline, and plain-language invariants.
* Review scope: full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready — `research`, `plan`, `phase-details`, `plan-critique`, and `changes` artifacts are reconciled, and `git status --short` was empty at review intake (`6efa815aa`).
* Acceptance basis: `FR-01`–`FR-04`, `NFR-01`–`NFR-02`, `AC-01`–`AC-06`, resolved critique items `PC-001` and `PC-002`, WCAG baseline (`docs/reference/research/ux/wcag-conformance-baseline.md`), plain-language content standard (`docs/reference/research/ux/content-standard.md`), and live Web Interface Guidelines.
* First comparison boundary: Compare `fe63981978970e38cafed5ebe3d38eb7f9a13cf8..6efa815aa` against `P01`–`P03` expectations without mutating production or planning files.
* Active read-only boundaries: Create only `.copilot-tracking/reviews/logs/2026-11-15/228-procurement-wcag-c1-rebase-review.md` during Review.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass inspection on 2026-11-15 over `fe63981978970e38cafed5ebe3d38eb7f9a13cf8..6efa815aa`, verifying ancestry, conflict resolutions, `screenRecordTable` row-header rendering, 6-alias `#/role/*` routing coexistence, baseline counters (`9 / 14 / 2`), commit metadata/trailers, Focused Tier check outputs (`183` unit tests `OK`), and refreshed Web Interface Guidelines rules.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Parent Rebase and `#/role/*` Routing Reconciliation | Reconciled | `e9f74e39c` sits cleanly atop `fe63981978970e38cafed5ebe3d38eb7f9a13cf8`; all 6 `#/role/*` destinations unioned in `app.js` and `role-screens.js`; `baseHash` deduplicated in `app.js` `route()`. |
| `P02`, `P02-T01` | `screenRecordTable` Row-Header Alignment and Coexistence Tests | Reconciled | All 6 `#228` tables (`procurement-packages` x4, `contractor-job-pack` x2) upgraded to `screenRecordTable` (`<th scope="row">`) in `6efa815aa`; `PC-001` honored in `test_procurement_contractor_screen_wcag.py`; baseline counts unchanged (`9 / 14 / 2`). |
| `P03`, `P03-T01` | Focused Tier Static Analysis, 6-Issue Unit Test Matrix, and Clean Local Commit | Reconciled | `node --check` (x3), `ruff check`, `ruff format --check` (206 files), `mypy` (291 files), and 16-module `unittest` (`183` tests `OK`) executed via `/usr/bin/python3` without `uv`; `:tests` `PYTHONPATH` update reconciled across plan, details, and changes. |
| `## Follow-Up Items` | Opt-in Playwright + axe browser check; human `#151` / `#155` validation | Reconciled | Preserved outside active `P01`–`P03` completion claims and mirrored accurately in `changes`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01` | `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/ops.js` | Rebased `0486e2ca1` (`-> e9f74e39c`) onto `fe6398197`, unioned all 6 `#/role/*` routes (`building_safety_lead`, `repairs`, `housing_officer`, `resident_engagement`, `procurement`, `contractor`), deduplicated `baseHash` in `app.js` `route()`, and preserved `ops.js` work-order badges/jump target. | `git merge-base --is-ancestor fe63981978970e38cafed5ebe3d38eb7f9a13cf8 HEAD` exited `0`; `git diff --check` clean. | Passed (`node --check` x3; `test_role_hash_aliases_and_nav_active_mapping`). | Reconciled |
| `P02`, `P02-T01` | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_procurement_contractor_screen_wcag.py` | Upgraded all 6 `#228` specialist tables to `screenRecordTable` (`<th scope="row">` on column 0 with `screenNodeValue` DOM badge preservation), extended `test_role_hash_aliases_and_nav_active_mapping` to all 6 `#/role/*` routes using `"Resident Liaison Officer"` (`choiceRoles`) and `#232`'s `aria-labelledby="screen-evidence-heading"` shell assertion (`PC-001`), and added `test_procurement_and_contractor_tables_use_col_and_row_header_scopes`. | Commit `6efa815aa`; `0` test removals; `1` new test method (`<= 2` cap honored); `0` edits to `#232`'s `roleScreensView`; `test_accessibility_baseline.py` / `wcag-conformance-baseline.md` exact at `9 / 14 / 2`. | Passed (`tests.test_procurement_contractor_screen_wcag`, `tests.test_procurement_screens`, `tests.test_accessibility_baseline`, `tests.test_content_standard`). | Reconciled |
| `P03`, `P03-T01` | `.copilot-tracking/changes/2026-11-15/228-procurement-wcag-c1-rebase-changes.md`, `.copilot-tracking/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan.md`, `.copilot-tracking/details/2026-11-15/228-procurement-wcag-c1-rebase-phase-details.md` | Executed full Focused Tier checks inside `src/api` via `/usr/bin/python3` without `uv` and committed clean pre-review candidate with privacy-safe noreply identity and Copilot trailer (`PC-002`). | Commit `6efa815aa` with noreply email `8036360+jmservera@users.noreply.github.com`, Copilot trailer, and zero `.copilot-tracking/` text in commit messages. | Passed (`183` unit tests `OK` across 16 modules). | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P03`, `P03-T01` | Appended `:tests` to `PYTHONPATH` (`PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests`) so explicit dotted `tests.*` `unittest` module invocation matches `unittest discover -s tests` for bare sibling imports (`from test_procurement_screens import ...`). | Triggered by `test_procurement_screen_wcag.py` bare sibling import; no user decision required because it preserves the approved `/usr/bin/python3` runner without touching sibling tests. | Updated `P03` and `P03-T01` in `228-procurement-wcag-c1-rebase-plan.md`, `228-procurement-wcag-c1-rebase-phase-details.md`, and `228-procurement-wcag-c1-rebase-changes.md`. | Ready (`PC-001` and `PC-002` preserved; no second critique needed). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Both findings from `.copilot-tracking/reviews/plans/2026-11-15/228-procurement-wcag-c1-rebase-plan-critique.md` (`PC-001` High and `PC-002` Medium) were directly resolved in planning and faithfully honored during implementation (`Resident Liaison Officer` session + `aria-labelledby="screen-evidence-heading"` for `#232` resident routes; `/usr/bin/python3` + `PYTHONPATH` runner without `uv` + clean pre-review commit before `rpi-review`).
* Material revisions: None — the `:tests` `PYTHONPATH` addition is an ordinary local current-state detail alignment matching `unittest discover -s tests`.
* Dependent-work pause assessment: No early resumption or dependency-order violation occurred (`P01` -> `P02` -> `P03` executed strictly in order).
* Justification assessment: Fully supported by empirical command and test output.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Opt-in Chromium Playwright + axe runtime check (`src/api/checks/specialist_keyboard_browser_check.py`) across `#/role/procurement` and `#/role/contractor` | Task explicitly scoped validation to the Focused Tier (`ruff`, `mypy`, `node --check`, and `src/api` unit tests). | UX browser-tier validation follow-up | Open distinct follow-up route |
| Human assistive-technology (`#151`) and live participant perspective walkthrough (`#155`) validation | Engineering unit/DOM checks cannot substitute for human accessibility or usability sign-off (`docs/reference/research/ux/wcag-conformance-baseline.md`). | Human accessibility/UX leads (`#151`, `#155`) | Open distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Web Interface Guidelines Compliance (`web-design-guidelines` Fresh Fetch)

Refreshed rules from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before reviewing changed web files (`fe63981978970e38cafed5ebe3d38eb7f9a13cf8..6efa815aa`):

```text
## src/api/src/zava_forward/api/web/app.js

✓ pass

## src/api/src/zava_forward/api/web/ops.js

✓ pass

## src/api/src/zava_forward/api/web/role-screens.js

✓ pass
```

Verified semantic `<nav role="navigation">`, `<a href="#...">` navigation links, hierarchical `<h1>`/`<h2>` headings with `tabindex="-1"` programmatic focus targets, `<table>` with `<caption>`, `<th scope="col">`, and `<th scope="row">`, keyboard-scrollable `.table-scroll` regions (`tabindex="0"`), URL query-parameter deep linking (`#/role/*?case=...`), explicit empty-state messages, `Intl.DateTimeFormat` / `Intl.NumberFormat` usage, non-colour textual state cues (`data-state-cue`), vulnerability redaction, and absence of forbidden phrases (`'human-approved'`) or banned internal jargon.

## Findings

No material or minor defects, decision gaps, or evidence gaps were found across `P01`, `P02`, or `P03` (`0 Critical, 0 High, 0 Medium, 0 Low`).

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | none | No corrective RPI stage required | Implementation is conformant across `P01`–`P03` |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Opt-in Chromium Playwright + axe runtime check (`src/api/checks/specialist_keyboard_browser_check.py`) across `#/role/procurement` and `#/role/contractor` when browser-tier checks run.
* Human assistive-technology (`#151`) and participant perspective walkthrough (`#155`) sign-off before claiming WCAG 2.2 AA conformance acceptance.

## Blockers and Remaining Work

* Blockers: None for the Cycle 1 rebase engineering scope (human `#151`/`#155` validation remains tracked separately before WCAG acceptance claims).
* Remaining active work: None (`P01`, `P01-T01`, `P02`, `P02-T01`, `P03`, `P03-T01` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `git merge-base --is-ancestor fe63981978970e38cafed5ebe3d38eb7f9a13cf8 HEAD` | `feat/ux-228-procurement-wcag` | Passed | Confirmed clean ancestry atop updated parent `#1639` (`fe6398197`) |
| `node --check src/zava_forward/api/web/app.js && node --check src/zava_forward/api/web/ops.js && node --check src/zava_forward/api/web/role-screens.js` | `src/api` web scripts | Passed | Exited `0` across all three scripts |
| `/usr/bin/python3 -m ruff check src tests checks` | `src/api` | Passed | `All checks passed!` |
| `/usr/bin/python3 -m ruff format --check src tests checks` | `src/api` (`206` files) | Passed | `206 files already formatted` |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src /usr/bin/python3 -m mypy` | `src/api` (`291` source files) | Passed | `Success: no issues found in 291 source files` |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests /usr/bin/python3 -m unittest` (16 modules) | `#228`, `#229`, `#230`, `#232`, `#135`, `#134`, `test_accessibility_baseline`, `test_content_standard`, `test_role_screens_conformance`, `test_design_system` | Passed | `Ran 183 tests in 18.256s — OK` |
| `specialist_keyboard_browser_check.py` | Opt-in Chromium Playwright + axe check | Skipped | Outside Focused Tier scope; routed to distinct follow-up |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every user requirement (`1`–`4`), functional/non-functional requirement (`FR-01`–`FR-04`, `NFR-01`–`NFR-02`), acceptance criterion (`AC-01`–`AC-06`), and resolved plan-critique disposition (`PC-001`, `PC-002`) is satisfied with verified git ancestry, `screenRecordTable` `<th scope="row">` parity, unchanged `9 / 14 / 2` accessibility baseline counts, passing plain-language content-standard checks, `183` passing unit tests across all six sibling slices without `uv`, and refreshed Web Interface Guidelines compliance.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Optional browser-tier `specialist_keyboard_browser_check.py` run and human `#151`/`#155` validation |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused Tier complete (`node --check` x3, `ruff check`, `ruff format --check` on 206 files, `mypy` on 291 files, and `unittest` 183 tests across 16 modules)
* Blockers: None

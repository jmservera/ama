<!-- markdownlint-disable-file -->
# Review: Programme Coordinator WCAG 2.2 Verification and Screen Enhancements (#230)

## Scope and Evidence

* Task ID: 2026-11-15-programme-coordinator-wcag-230
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Requirements `FR-01` through `FR-04`, `NFR-01`, `NFR-02`, acceptance criteria `AC-01` through `AC-05`, critique dispositions `PC-001` through `PC-005`, Focused validation suites across `src/api` and `src/core`, refreshed `web-design-guidelines` compliance across changed web assets (`role-screens.js`, `app.js`, `style.css`), and the automated-vs-human assistive-technology boundary (`#151`, `#155`, `Refs #230`).
* Plan: .copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/programme-coordinator-wcag-230-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/programme-coordinator-wcag-230-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/programme-coordinator-wcag-230-research.md; `src/api/src/zava_forward/api/web/role-screens.js`; `src/api/src/zava_forward/api/web/app.js`; `src/api/src/zava_forward/api/web/style.css`; `src/api/tests/test_programme_screen_wcag.py`; `src/api/tests/test_programme_coordinator_wcag_230.py`; refreshed `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`.

## Opening Review State

* Interpreted review goal: Verify once, from committed/staged source and test evidence, whether `#230` WCAG 2.2 AA route aliases, row headers, keyboard section-jump navigation, `aria-describedby` associations, and Fluent 2 tri-state non-colour cues satisfy `FR-01` through `FR-04`, `NFR-01`, `NFR-02`, and `PC-001` through `PC-005` without mutating counted or manifest guards or claiming human assistive-technology sign-off.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; research, critique-reconciled plan, phase details, and changes record are complete and internally consistent.
* Acceptance basis: `FR-01`..`FR-04`, `NFR-01`..`NFR-02`, `AC-01`..`AC-05`, critique dispositions `PC-001`..`PC-005`, AMA WCAG 2.2 AA baseline (`docs/reference/research/ux/wcag-conformance-baseline.md`), AMA plain-language content standard (`docs/reference/research/ux/content-standard.md`), and refreshed `web-design-guidelines`.
* First comparison boundary: Compare `P01`, `P02`, and `P03` completed work in `role-screens.js`, `app.js`, `style.css`, `test_programme_screen_wcag.py`, and `test_programme_coordinator_wcag_230.py` against plan requirements and `PC-001`..`PC-005`, keeping human screen-reader / lived-experience sign-off outside automated engineering acceptance (`#151`, `#155`).
* Active read-only boundaries: This stage writes only `.copilot-tracking/reviews/logs/2026-11-15/programme-coordinator-wcag-230-review.md` and does not modify source files, tests, plan, phase details, critique, research, or changes records.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass full-task comparison on `2026-11-15` across all RPI artifacts, changed web and test files, Focused validation runs (`345` specialist-screen/WCAG tests, `166` baseline/content/coordinator/manifest tests, `node --check`, `ruff check`, `ruff format --check`, `mypy`), and refreshed `web-design-guidelines`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `### P01: Programme Queue and Role Route Alias WCAG 2.2 Enhancements (P01-T01, P01-T02)` | Reconciled | `#/role/programme_manager` and `#/role/retrofit_coordinator` route aliases, `<th scope="row">` across all 3 `programme-queue` tables, `#programme-scope` `aria-describedby`, `data-jump-target`, and Fluent 2 `.flag` / `.status-line.wait` + `data-state-cue` indicators match `FR-01`, `FR-02`, `AC-01`, `AC-02`, and `PC-005`. |
| `P02` (`P02-T01`) | `### P02: Coordinator Flow (#/coordinator) Keyboard Jump Navigation and Non-Colour State Cues (P02-T01)` | Reconciled | `contractorJumpLinks` 7-section jump nav (including `#map-title`), unique `.table-scroll` landmarks and single `aria-labelledby` on `summary`, `#co-filter-error` and `#co-cutoff-note` `aria-describedby` wiring, tri-state (`Unknown != 0`) heatmap and `Selected records` non-colour state cues, and `style.css` focus-visible/inset-border rules match `FR-03`, `FR-04`, `AC-03`, and `PC-001`..`PC-004`. |
| `P03` (`P03-T01`, `P03-T02`) | `### P03: Focused WCAG 2.2 Conformance Tests and Regression Verification (P03-T01, P03-T02)` | Reconciled | `test_programme_screen_wcag.py` updated (`1` existing test file) and `test_programme_coordinator_wcag_230.py` added (`1` new test file, `0` removals) with Focused validation passing and `P03-T02` boundary reconciled so post-review commit/rebase closes cleanly with empty `git status --short`. |
| `## Follow-Up Items` | `## Follow-Up Items` (manual AT validation under `#151`, `#155`) | Reconciled | Preserved outside active `P01`–`P03` engineering claims; commit uses `Refs #230` rather than `Closes #230`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js` | Wired `#/role/programme_manager` and `#/role/retrofit_coordinator` into `ROLE_HASH_SCREENS` and `isRoleScreensDestination` for lazy loading, active nav highlighting, query preservation, and role denial alerts | Verified in `test_role_hash_route_aliases_script_loading_and_rbac` | Passed (`test_programme_coordinator_wcag_230`, `test_workspace_scripts`) | Reconciled |
| `P01-T02` | `src/api/src/zava_forward/api/web/role-screens.js` | Enabled `<th scope="row">` across all 3 `programme-queue` tables, linked `#programme-scope` via `aria-describedby`, added `data-jump-target`, and wrapped states in Fluent 2 `.flag` / `.flag.danger` / `.status-line.wait` + `data-state-cue` without altering copy or write-free boundaries | Verified in `test_programme_queue_row_headers_scope_descriptions_jump_targets_and_state_cues` and `test_programme_screen_wcag.py` | Passed (`test_programme_screen`, `test_programme_screen_wcag`, `test_programme_coordinator_wcag_230`) | Reconciled |
| `P02-T01` | `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/style.css` | Added 7-target `contractorJumpLinks` jump nav (including `#map-title`), unique landmark labels, `#co-filter-error` & `#co-cutoff-note` `aria-describedby` + change clearing, tri-state (`Unknown != 0`) heatmap & `Selected records` `.flag` cues, inset border on `.heat-present`, and `.coordinator h2[tabindex="-1"]:focus-visible` ring | Verified in `test_coordinator_view_jump_navigation_landmarks_and_focus_delegation`, `test_coordinator_view_filter_descriptions_error_recovery_and_tristate_cues`, and `test_css_focus_ring_and_heatmap_non_colour_contracts` | Passed (`test_programme_coordinator_wcag_230`, `test_coordinator_api`, `test_map_fullscreen`, `test_technical_quality_screens_wcag`, `test_accessibility_baseline`, `test_content_standard`) | Reconciled |
| `P03-T01` | `src/api/tests/test_programme_screen_wcag.py`, `src/api/tests/test_programme_coordinator_wcag_230.py` | Updated row-header `scope` assertion in `test_programme_screen_wcag.py` and authored isolated subprocess Node VM WCAG 2.2 suite `test_programme_coordinator_wcag_230.py` | `14` tests across both modules run in `<1s` with zero `sys.modules` mutation | Passed (`unittest`, `ruff check`, `ruff format --check`, `mypy`) | Reconciled |
| `P03-T02` | `src/api/tests/*`, `src/core/tests/*` | Executed Focused unit, WCAG, specialist-screen, content-standard, scenario-manifest, syntax, lint, and static-typing checks | Recorded in `.copilot-tracking/changes/2026-11-15/programme-coordinator-wcag-230-changes.md` (`## Validation Record`) | Passed (`345` screen tests + `166` Focused baseline/manifest tests + `node --check` + `ruff` + `mypy`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P03-T02` in plan and phase details | Scoped `P03-T02` to Focused validation execution during `rpi-implement` while sequencing the single local Git commit and rebase (`AC-05`) immediately after `rpi-review` persists its review log and `Follow-up` state JSON | Immediately relevant lifecycle ordering requirement so `git status --short` ends empty after `rpi-review` writes canonical tracking files; preserves user's confirmed single-commit instruction | Reconciled across `.copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md`, `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md`, and `.copilot-tracking/changes/2026-11-15/programme-coordinator-wcag-230-changes.md` | Not needed (preserves approved scope, acceptance criteria, and `PC-001`..`PC-005` dispositions) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five findings (`PC-001` CSS selector ordering, `PC-002` unique `.table-scroll` landmarks + `#map-title` 7th jump link + single `aria-labelledby` on `summary`, `PC-003` tri-state `Unknown != 0` visible `.flag` cues + `.heat-present` inset border, `PC-004` `contractorJumpLinks` `.screen-links` reuse, `PC-005` omitting static `role="status"` on `programmeFunnel`) were applied directly in planning and verified in implementation and tests.
* Material revisions: None; no discovery altered requirements, architecture, acceptance criteria, or user-confirmed decisions.
* Dependent-work pause assessment: No dependent work required pausing; `P01`, `P02`, and `P03` executed in dependency order.
* Justification assessment: Supported by direct code, CSS, and isolated Node VM test evidence.

## Web Interface Guidelines Compliance (`file:line`)

Refreshed `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before review; AMA Fluent 2, WCAG 2.2 AA, plain-ASCII, and sentence-case rules (`docs/reference/research/ux/design-system.md`, `wcag-conformance-baseline.md`, `content-standard.md`) take precedence where generic typography guidance prefers Title Case or Unicode ellipses.

```text
## src/api/src/zava_forward/api/web/role-screens.js

✓ pass

## src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:2716 - pre-existing ASCII "..." in "Loading coordinator counts..." intentionally retained per AMA plain-ASCII Markdown/content rule

## src/api/src/zava_forward/api/web/style.css

✓ pass
```

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Manual assistive-technology, screen-reader, and lived-experience validation across `programme-queue` (`#/role/programme_manager`, `#/role/retrofit_coordinator`) and `#/coordinator` (`#151`, `#155`) | Requires human assistive-technology testing and user-research sessions that automated engineering checks cannot fabricate per `docs/reference/research/ux/wcag-conformance-baseline.md` | Human accessibility / UX reviewer under `#151` and `#155` before changing `Refs #230` to `Closes #230` | Open distinct follow-up route (not an implementation defect) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Human assistive-technology and lived-experience validation remains open before closing `#230`

* Related scope: Plan `## Follow-Up Items` (`#230`, `#151`, `#155`)
* Evidence: `docs/reference/research/ux/wcag-conformance-baseline.md`; `src/api/tests/test_programme_coordinator_wcag_230.py`
* Impact: Automated Node VM and static CSS/HTML checks prove engineered WCAG 2.2 AA semantics, keyboard focus delegation, `aria-describedby` wiring, and tri-state non-colour cues, but repository policy rightly forbids claiming accessibility acceptance or closing `#230` until human assistive-technology verification completes.
* Destination: Distinct follow-up item (`#151` / `#155`)
* Smallest useful next action: Keep commit linkage as `Refs #230` and run human screen-reader and keyboard walkthroughs on `#/role/programme_manager`, `#/role/retrofit_coordinator`, and `#/coordinator` under `#151` and `#155`.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | Distinct follow-up (`#151`, `#155`) | Human accessibility / UX reviewer executes live screen-reader and keyboard acceptance walkthroughs before closing `#230` | Non-blocking human validation boundary outside automated engineering implementation |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Execute manual assistive-technology and lived-experience acceptance checks on `programme-queue` (`#/role/programme_manager`, `#/role/retrofit_coordinator`) and `#/coordinator` under `#151` and `#155` before closing `#230`.

## Blockers and Remaining Work

* Blockers: None for engineered `#230` implementation and local branch closeout (`Refs #230`); human AT validation remains a governance prerequisite for closing `#230`.
* Remaining active work: None in `P01`, `P02`, or `P03` (local single-commit and rebase onto `origin/feat/demo-233-same-home-tensions-0825` executes immediately at task closeout).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `node --check web/role-screens.js && node --check web/app.js` | Changed JavaScript modules | Passed | Zero syntax errors |
| `python3 -m unittest test_programme_screen test_programme_screen_wcag test_programme_coordinator_wcag_230` | `#230` functional & WCAG 2.2 suites (`src/api`) | Passed | `38` tests passed (`OK`) |
| `python3 -m unittest discover -s tests -p 'test_*screen*.py' -q` | All `37` specialist-screen & WCAG suites (`src/api`) | Passed | `345` tests passed in `26.9s` (`OK`) |
| `python3 -m unittest test_accessibility_baseline test_content_standard test_coordinator_api test_map_fullscreen test_workspace_scripts test_epic149_form_error_summary_associations test_epic149_role_workbench_heading_hierarchy test_dependency_rule` | Static WCAG/copy baselines, coordinator API, map split & dependency rule (`src/api`) | Passed | All passed (`OK`; `test_accessibility_baseline.py` and `test_content_standard.py` untouched) |
| `python3 -m unittest test_scenario_manifest test_needs_inventory test_dependency_rule` | Synthetic scenario manifest, needs inventory & dependency rule (`src/core`) | Passed | All passed (`OK`; `scenario-manifest.json` recipe SHA inputs untouched) |
| `ruff check . && ruff format --check tests/test_programme_screen_wcag.py tests/test_programme_coordinator_wcag_230.py` | Lint & formatting (`src/api`) | Passed | `All checks passed!`; `2 files already formatted` |
| `MYPYPATH=src:../core/src:../agents/src mypy src tests/test_programme_screen_wcag.py tests/test_programme_coordinator_wcag_230.py` | Static typing (`src/api`) | Passed | `Success: no issues found in 30 source files` |
| `python3 tools/rpi-checks.py` | Repository-wide full local gate | Skipped | Explicitly out of scope under Focused validation tier (`#1294` and caller instructions) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every engineered requirement (`FR-01`..`FR-04`, `NFR-01`, `NFR-02`), acceptance criterion (`AC-01`..`AC-04`, with `AC-05` commit/rebase ready for closeout), and critique disposition (`PC-001`..`PC-005`) is implemented, reconciled across canonical RPI artifacts, and proven by isolated automated tests, linters, and static type checks while preserving all counted baselines, scenario-manifest hashes, and human AT boundaries (`RV-001` routed as distinct non-blocking follow-up work under `#151`/`#155`).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up (`#151`, `#155`) | Human accessibility / UX reviewer runs assistive-technology walkthroughs before closing `#230` |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused validation passed (`345` specialist-screen/WCAG tests, `166` baseline/content/coordinator/manifest tests, `node --check`, `ruff check`, `ruff format --check`, `mypy`); full gate skipped by Focused tier classification
* Blockers: None

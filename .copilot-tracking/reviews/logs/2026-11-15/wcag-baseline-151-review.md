<!-- markdownlint-disable-file -->
# Review: WCAG 2.2 Conformance Baseline for the Workbench (#151)

## Scope and Evidence

* Task ID: 2026-11-15-wcag-baseline-151
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Issue `#151` and `#119` workbench accessible equivalents (`app.js`, `progress.js`, `ops.js`, `panels.js`, `role-screens.js`, `welcome.html`, `style.css`), deterministic static and Node-VM verification suites (`test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`), structured eight-dimension WCAG 2.2 AA audit and accessible-equivalents inventory (`wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`), Focused-tier validation results, and Web Interface Guidelines compliance across changed web files.
* Plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/wcag-baseline-151-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/wcag-baseline-151-research.md; refreshed Web Interface Guidelines (`command.md`); Focused validation outputs (`ruff`, `mypy`, `node --check`, `src/core` and `src/api` `unittest` runs, `tools/rename-zava-tests.py`).

## Opening Review State

* Interpreted review goal: Verify that the completed `#151` / `#119` implementation, deterministic tests, and knowledge-base documentation satisfy all approved plan requirements, critique dispositions (`PC-001` through `PC-005`), repository guard invariants, and Web Interface Guidelines rules without claiming unperformed human assistive-technology acceptance.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan, phase details, one-pass plan critique, changes log, research artifact, git diff, and focused validation outputs are complete and reconciled.
* Acceptance basis: Issue `#151` acceptance criteria (structured 8-dimension WCAG 2.2 AA audit; accessible equivalents for maps, charts, and tables `#119`), `FR-1` through `FR-6`, `NFR-1` through `NFR-4`, resolved critique items `PC-001` through `PC-005`, and Web Interface Guidelines compliance.
* First comparison boundary: Plan-to-change reconciliation across `P01`, `P02`, `P03`, and `## Follow-Up Items`, excluding live human screen-reader/zoom walkthroughs (`#155`).
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/wcag-baseline-151-review.md` and RPI session state; production code, tests, docs, plan, details, critique, and changes record remain read-only.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed one post-implementation review on `2026-11-15` across the reconciled plan, phase details, plan critique, changes log, git diff, refreshed Web Interface Guidelines (`command.md`), and Focused-tier validation outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| `P01-T01` | Overview Chart, Leaflet Map, and Progress Meter Accessible Equivalents | Reconciled | `bars()`, `mapPanel()` / `renderList()`, and `ProgressViews` `chart()` match approved requirements and `PC-001` / `PC-005` critique dispositions |
| `P01-T02` | Captions, Row Headers, and Focusable Scroll Regions Across All 15 Script-Built Table Builders | Reconciled | All 15 `h("table", {},` builders across `web/*.js` carry `.table-scroll` (`role="region"`, `tabindex`, `aria-label`), `<caption>`, `<th scope="col">`, and `<th scope="row">`, including `role-screens.js` `screenTable` `rowHeader = true` (`PC-002`, `PC-003`) |
| `P01-T03` | Target-Size Minimums, Welcome Skip Link, and Tokenized Contrast | Reconciled | `welcome.html` `.skip-link` alignment and `style.css` 24px/40px target-size and `var(--muted)` rules match reconciled plan/details (`PC-005`) |
| `P02-T01` | Deterministic Automated Baseline and Accessible-Equivalent Tests | Reconciled | `test_accessibility_baseline.py` (`15` tables, 3 HTML files, 8 target-size selectors, `sites == 9`) and `test_wcag_workbench_baseline_151.py` (zero `@unittest.skip`) created and passing prior to `P03` (`PC-004`) |
| `P03-T01`, `P03-T02` | Structured Eight-Dimension WCAG 2.2 AA Audit and Knowledge Base Update + Focused Validation | Reconciled | `wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md` updated with all 8 dimensions, widget/table register, recorded gaps (`/law.html`), non-conformance boundaries, and passing Focused validation |
| `## Follow-Up Items` | Manual assistive-technology/zoom walkthroughs + owner confirmation `O-1`; CI live-browser harness (`#155`); standalone `/law.html` skip-link slice | Reconciled | Preserved outside active `P01`-`P03` claims and routed as distinct follow-up work |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| `P01-T01` | `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/progress.js` | Disambiguated `bars()` disclosure summaries, wrapped `bars()` tables in `.table-scroll`, added empty-state row, added synchronized `[data-maplist-empty]` sibling in `mapPanel()`, and added series-qualified `aria-label` on `ProgressViews` `<meter>` elements | Diff and Node-VM DOM tests | Passed (`node --check`, `test_wcag_workbench_baseline_151.py`, `test_content_standard.py`) | Reconciled |
| `P01-T02` | `src/api/src/zava_forward/api/web/ops.js`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js` | Brought all 15 script-built table builders to `.table-scroll` + `<caption>` + `<th scope="col">` + `<th scope="row">` parity | Diff, static regex inventory (`15`), and Node-VM table checks | Passed (`node --check`, `test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`, 18 `test_*wcag*.py` suites) | Reconciled |
| `P01-T03` | `src/api/src/zava_forward/api/web/style.css`, `src/api/src/zava_forward/api/web/welcome.html` | Added `.skip-link` + `<main id="welcome-main" tabindex="-1">` on `welcome.html`, enforced `>= 1.5rem` (`24px`) and `2.5rem` (`40px`) target sizes, and tokenized `.focus dt` to `var(--muted)` | Diff and static CSS/HTML assertions | Passed (`test_design_system.py`, `test_static_assets.py`, `test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`) | Reconciled |
| `P02-T01` | `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_wcag_workbench_baseline_151.py` | Updated baseline static assertions (`15` tables, `law.html`, 8 target-size selectors) and added 6-method deterministic Node-VM + static verification module | Runnable test modules with zero `@unittest.skip` | Passed (`ruff check`, `mypy`, `unittest`: 20 tests across both modules) | Reconciled |
| `P03-T01`, `P03-T02` | `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md` | Authored structured 8-dimension WCAG 2.2 AA audit, complete visual-widget and 15-table accessible-equivalents inventory, recorded gaps, and KB index/log entries; executed Focused validation | Diff and traceability/evidence guards | Passed (`test_epic149_*.py`, `test_screen_design_traceability.py`, `tools/rename-zava-tests.py`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| `P01-T03` | Added `<a class="skip-link" href="#welcome-main">Skip to main content</a>` and `id="welcome-main" tabindex="-1"` on `<main>` in `welcome.html` so both in-scope workbench HTML pages (`index.html` and `welcome.html`) expose consistent WCAG 2.4.1 bypass links | `welcome.html` lacked `.skip-link` while `wcag-conformance-baseline.md` scopes the target to signed-in screens plus the welcome page; ordinary local current-state update requiring no user escalation | Updated `P01-T03` in `.copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md`, `.copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md`, and `.copilot-tracking/changes/2026-11-15/wcag-baseline-151-changes.md` | Not needed; preserves approved `#151` WCAG 2.4.1 scope and `PC-001`..`PC-005` critique resolutions | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five critique findings (`PC-001` through `PC-005`) have `resolved` dispositions in `## Critique Disposition` and are verified in the delivered code, tests, and documentation.
* Material revisions: None. The single implementation-time update (`welcome.html` `.skip-link`) is an immediately relevant current-state alignment within `P01-T03` that preserves approved scope and acceptance criteria.
* Dependent-work pause assessment: No pause was needed; `P01`, `P02`, and `P03` executed strictly in dependency order (`P02` created `test_wcag_workbench_baseline_151.py` before `P03` cited it in `wcag-conformance-baseline.md`).
* Justification assessment: Supported by repository source, Node-VM DOM execution, and passing Focused validation checks.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Manual assistive-technology and browser zoom walkthroughs (NVDA, JAWS, VoiceOver, TalkBack, 200% zoom, 400% reflow) and owner confirmation `O-1` (`#151`, `#155`, `#619`) | Requires human testers with real screen readers and repository owner target sign-off; engineering checks cannot establish assistive-technology acceptance | Repository owner and human UX/accessibility testers | Open; routed as distinct human/governance follow-up outside active `P01`-`P03` completion |
| Rendered axe-core / Playwright accessibility runtime config (`a11y-runtime.config.json`) in hosted CI (`#155`) | Tracked separately under issue `#155` outside the Focused `#151` baseline slice | Future engineering slice on `#155` | Open; routed as distinct engineering follow-up |
| Standalone `/law.html` `.skip-link` and polite status region | `/law.html` is a standalone local legal-snapshot viewer outside signed-in workbench scope and honestly documented under `## Recorded gaps` | Optional future UX slice if `/law.html` enters workbench conformance scope | Open; routed as distinct non-blocking follow-up |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Web Interface Guidelines Compliance Audit (Changed Web Files)

Refreshed rules from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and audited all 7 changed web files (`welcome.html`, `style.css`, `app.js`, `progress.js`, `ops.js`, `panels.js`, `role-screens.js`). Zero WCAG 2.2 AA regressions or anti-patterns were introduced; minor pre-existing polish notes outside `#151` scope are recorded below in `file:line` format:

```text
## src/api/src/zava_forward/api/web/welcome.html

src/api/src/zava_forward/api/web/welcome.html:6 - pre-existing: missing <meta name="theme-color"> matching --bg (changed skip-link/main landmark lines 10,15 pass)

## src/api/src/zava_forward/api/web/style.css

src/api/src/zava_forward/api/web/style.css:271 - pre-existing: numeric table cells omit global font-variant-numeric: tabular-nums (changed target-size/contrast rules lines 54,105,250,275,315 pass)

## src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:2440 - pre-existing: bars() formats integer count via String(d.n) rather than Intl.NumberFormat (changed disclosure/scroll/empty-state lines 2436-2441, 2523, 2588-2591, 2907, 2911, 2934-2937 pass)

## src/api/src/zava_forward/api/web/progress.js

✓ pass

## src/api/src/zava_forward/api/web/ops.js

src/api/src/zava_forward/api/web/ops.js:42 - pre-existing: sensorTable renders raw UTC ISO timestamp and numeric readings rather than Intl.* formatters (changed .table-scroll/caption/row-header lines 38-43, 478 pass)

## src/api/src/zava_forward/api/web/panels.js

✓ pass

## src/api/src/zava_forward/api/web/role-screens.js

✓ pass
```

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Pre-existing typography and locale formatting polish opportunities in untouched workbench table cells and welcome head

* Related scope: Follow-up outside `P01`-`P03`
* Evidence: `src/api/src/zava_forward/api/web/welcome.html`, `src/api/src/zava_forward/api/web/style.css`, `src/api/src/zava_forward/api/web/app.js`, and `src/api/src/zava_forward/api/web/ops.js` (recorded in the Web Interface Guidelines audit above).
* Impact: Does not affect WCAG 2.2 AA conformance baseline, keyboard operation, accessible equivalents, or screen-reader semantics, but adding `font-variant-numeric: tabular-nums` on numeric columns, `Intl.NumberFormat("en-GB")` in `bars()`, and `<meta name="theme-color">` on HTML entrypoints would improve visual number alignment and browser chrome theming in a future design-system polish pass.
* Destination: follow-up
* Smallest useful next action: Track as an optional Fluent 2 design-system polish item alongside `#150` / `#155` without altering `#151` baseline scope.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| `RV-001` | Distinct follow-up item | Future Fluent 2 web polish slice (`#150` / `#155`) | Non-blocking pre-existing Web Interface Guidelines polish outside `#151` WCAG 2.2 baseline scope |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Human assistive-technology and browser zoom walkthroughs (`NVDA`, `VoiceOver`, `200%` text resize, `400%` reflow) plus owner confirmation `O-1` remain required before closing `#151` or claiming WCAG 2.2 AA conformance (`Refs #151, #119`).
* Optional standalone `/law.html` `.skip-link` and polite status region if `/law.html` is brought into workbench conformance scope.
* Optional Web Interface Guidelines polish (`RV-001`: `tabular-nums`, `Intl.NumberFormat` in `bars()`, `<meta name="theme-color">`).

## Blockers and Remaining Work

* Blockers: none for the `#151` engineering baseline slice (human assistive-technology walkthroughs and owner confirmation `O-1` remain explicit open issue gates, so the commit and PR must use `Refs #151, #119` rather than `Closes #151`).
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| `ruff check src/core src/api` | `src/core` and `src/api` Python sources and tests | Passed | `All checks passed!` |
| `mypy` (`src/core` `src` + `tests`; `src/api` `src` + `test_accessibility_baseline.py` + `test_wcag_workbench_baseline_151.py`) | Static type checking | Passed | `0` issues across `317` files in `src/core` and `30` files in `src/api` |
| `node --check src/api/src/zava_forward/api/web/*.js` | All 16 workbench JavaScript files | Passed | Exit `0` on all 16 scripts |
| `unittest` in `src/core` (`test_scenario_manifest.py`, `test_needs_inventory.py`, `test_live_doc_links.py`) | Core manifest hashes, needs inventory, and live doc links | Passed | `19` targeted tests passed (`0.143s`); `3,382` non-Azure-SDK core tests passed |
| `unittest` in `src/api` (`test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`, `test_epic149_*.py`, `test_design_system.py`, `test_content_standard.py`, `test_finance_exposure_screen.py`, `test_progress_dashboard.py`, `test_role_screens*.py`, `test_static_assets.py`, and all 18 `test_*wcag*.py` modules) | Static + Node-VM WCAG 2.2 baseline, accessible equivalents, UX traceability, and role-screen suites | Passed | `270` UX/baseline/guard tests (`40.6s`) + `142` `*wcag*.py` tests (`10.9s`) passed with `0` failures |
| `python3 tools/rename-zava-tests.py` | Zava North Homes naming guard | Passed | `25` tests passed (`0.629s`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned phase and task (`P01`, `P02`, `P03`) and both targeted `#151` engineering deliverables (complete accessible equivalents for workbench maps, charts, `<meter>` stacks, and all 15 script-built table builders; structured eight-dimension WCAG 2.2 AA workbench audit in `wcag-conformance-baseline.md` backed by deterministic static and Node-VM tests) are complete, verified, and reconciled with zero defects, while human assistive-technology testing and owner target confirmation remain honestly preserved as open non-conformance gates (`Refs #151, #119`).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | Distinct follow-up items (`RV-001`, `#155` live AT/CI harness, standalone `/law.html` skip link, owner confirmation `O-1`) | Select at RPI post-Review checkpoint or leave for human/owner gate execution |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `ruff check`, `mypy`, `node --check`, `src/core` unit tests, `src/api` accessibility/WCAG/UX/traceability unit tests, and `tools/rename-zava-tests.py` all passed
* Blockers: none


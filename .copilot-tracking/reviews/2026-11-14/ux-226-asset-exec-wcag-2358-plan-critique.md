<!-- markdownlint-disable-file -->
# RPI Plan Critique: Asset Executive and Board Views WCAG 2.2 Accessibility & Keyboard Navigation

## Metadata

* Task ID: 2026-11-14-ux-226-asset-exec-wcag-2358
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/ux-226-asset-exec-wcag-2358-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the local WCAG 2.2 accessibility, keyboard jump navigation, and explicit non-colour textual state meaning slice for Issue #226 on the asset-board screen mirroring PR #1715 (#225), including role="navigation", aria-label, keyboard jump links, and textual state labels; preserve workbench.py and scenario-manifest.json recipe SHA invariants; avoid bulk del sys.modules[...] in tests; validate in src/api with mypy, ruff check, ruff format --check, and focused unittest suites; record dated RPI artifacts under .copilot-tracking/*/{2026-11-14}/ux-226-asset-exec-wcag-2358* and commit locally on feat/ux-226-asset-exec-wcag-2358 with Refs #226 without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/ux-226-asset-exec-wcag-2358-research.md, .copilot-tracking/plans/2026-11-14/ux-226-asset-exec-wcag-2358-plan.md, .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md, src/api/src/zava_forward/api/web/role-screens.js, src/api/src/zava_forward/api/web/style.css, src/api/src/zava_forward/api/web/app.js, src/api/src/zava_forward/api/web/index.html, src/api/pyproject.toml, src/api/tests/test_asset_board_screen.py, src/api/tests/test_asset_exec_screen_wcag.py, src/api/tests/test_finance_screens_wcag_225.py, src/api/tests/test_finance_grants_screens.py, src/api/tests/test_finance_screen_wcag.py, src/api/tests/test_finance_grants_screen_wcag.py, src/api/tests/test_role_screens_conformance.py, src/api/tests/test_content_standard.py, src/api/tests/test_connected_home_check.py, src/api/tests/test_safety_screen_wcag_keyboard.py, src/api/tests/test_accessibility_baseline.py, src/api/tests/test_design_system.py, src/api/checks/connected_home_browser_check.py, src/api/checks/specialist_keyboard_browser_check.py, src/api/checks/role_screens_browser_check.py, docs/reference/research/ux/wcag-conformance-baseline.md, and docs/reference/research/ux/design-system.md.
* Decisions, dependencies, and acceptance criteria considered: FR-01 through FR-04, NFR-01 through NFR-02, AC-01 through AC-05, P01-T01 through P02-T02, research claims C1 through C12 and W1, plain-language copy bans, connected-home panel title and span invariants, global identifier uniqueness against app.js, and non-conformance-claim guardrails (Refs #226 because manual NVDA+Firefox and VoiceOver+Safari acceptance remains external).
* Assessment boundary: Evaluates plan accuracy, DOM/CSS/JS invariants, cross-screen side effects, static analysis rules, unit test compatibility, and browser-check script contracts from the supplied repository files. Does not execute live human assistive-technology testing or external hosted CI.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-01 / AC-01 / P01-T01 | Partial | 10-section assetSections jump bar, role="navigation", aria-label="Sections of this view", Go to labels, btn alt styling, data-jump / data-jump-target attributes, and anchor-backed screenPanel landmarks are sound and preserve connected_home_browser_check.py panel titles, test_content_standard.py banned-word rules, and read-only tag constraints; however, P01-T01's proposed scrollIntoView and window.matchMedia change to the shared click handler breaks two existing unit suites (PC-001). |
| FR-02 / AC-02 / P01-T01 | Partial | All 10 panels receive section id, aria-labelledby, and h2 tabindex="-1", and existing table-scroll regions keep role="region", tabindex="0", and expected specialist_keyboard_browser_check.py labels; shared delegated click handler changes need correction per PC-001. |
| FR-03 / AC-03 / P01-T02 | Partial | Stock conflict status cues, AI report status cues, Overall AI cost per accepted outcome cue, and preserved Evidence class == Unknown / Loaded invariants satisfy test_asset_board_screen.py and connected_home_browser_check.py substring checks, but assetReconciliationCues mishandles missing reconciliation and double-prefixes matched values (PC-002), the Eligibility value change breaks checks/role_screens_browser_check.py Story 226 exact inner_text() assertion (PC-003), and shared assetCost blast radius on Finance screens lacks test coverage in P02-T02 (PC-004). |
| FR-04 / AC-04 / P01-T03 | Partial | btn alt target sizing (2.5rem / 40px) and scroll-margin-top clearance pass RoleScreenConformance no-motion rules and class checks, but P01-T03 relies on a false C5 premise that .top is position: sticky in style.css and introduces a literal 4.5rem length instead of a Fluent spacing token (PC-005). |
| NFR-01 | Covered | Zero edits target workbench.py or the four SHA-locked recipe files in scenario-manifest.json (workbench-manifest.json, workbench_browser_check.py, dataset.py, test_workbench.py), and tests avoid bulk del sys.modules[...]. |
| NFR-02 / AC-05 / P02-T01 / P02-T02 | Partial | Typed unittest harness design aligns with strict mypy and ruff rules in src/api/pyproject.toml, but P02-T01/P02-T02 inherit PC-001 through PC-005 and omit Finance screen suites that exercise shared assetCost(report). |
| Research C1-C3, C6-C12, W1 | Covered | Anchor contract in screenPanel, existing test_asset_board_screen.py and test_asset_exec_screen_wcag.py invariants, connected_home_browser_check.py panel_span regexes, specialist_keyboard_browser_check.py region list, and SHA-locked file boundaries are accurately reflected. |
| Research C4, C5 | Partial | C4 mis-cites stateCue at line 421 instead of line 836 and misses stateCue's prefix: detail formatting and undefined lookup behavior (PC-002); C5 inaccurately claims .top is position: sticky in style.css (PC-005). |

## Verdict

* Verdict: Revise
* Rationale: Three High-severity defects and one Medium cross-screen test gap in P01 and P02 would break existing unit and browser checks if implemented verbatim: (1) adding window.matchMedia and scrollIntoView inside the shared a[data-jump] click listener breaks both test_asset_exec_screen_wcag.py exact source assertions and test_finance_screens_wcag_225.py's Node VM sandbox; (2) stateCue(assetReconciliationCues, m.reconciliation) returns "Action needed: Unknown" when reconciliation is omitted and double-prefixes matched values ("State: Unreconciled: unreconciled"); and (3) replacing ["Eligibility", "Unknown"] breaks Story "226" exact multi-line inner_text() assertions in src/api/checks/role_screens_browser_check.py. All five findings are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: P01-T01 shared click-listener edit breaks test_asset_exec_screen_wcag.py and test_finance_screens_wcag_225.py

* Related IDs: FR-01, FR-02, NFR-02, AC-01, AC-02, AC-05, P01-T01, P02-T01, P02-T02
* Evidence: .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md (lines 95-98); src/api/src/zava_forward/api/web/role-screens.js (lines 267-273); src/api/tests/test_asset_exec_screen_wcag.py (lines 60-63); src/api/tests/test_finance_screens_wcag_225.py (lines 51-61, 91-94).
* Concern: P01-T01 instructs updating the global delegated a[data-jump] click handler in src/api/src/zava_forward/api/web/role-screens.js to call scrollIntoView({ behavior: window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ? "auto" : "smooth", block: "start" }) (or scrollIntoView?.({ block: "start" })) alongside focus(). First, test_finance_screens_wcag_225.py executes that shared click listener in a Node vm.createContext sandbox where window is undefined (throwing ReferenceError: window is not defined) and mock jump targets only implement { focus() { ... } } without scrollIntoView. Second, test_asset_exec_screen_wcag.py line 63 asserts the exact consecutive source substring self.assertIn("event.preventDefault();\n    document.getElementById", source), which fails if any target variable binding or scrollIntoView statement is placed before document.getElementById. Third, native HTMLElement.focus() already scrolls focused headings into view while honoring CSS scroll-margin-top and avoiding smooth-scroll motion under the repository reduced-motion baseline.
* Impact: Implementing P01-T01 as specified causes immediate regression failures in test_asset_exec_screen_wcag.py and test_finance_screens_wcag_225.py, violating AC-05 and NFR-02.
* Smallest useful change: Revise P01-T01 and P02-T01 to keep the shared click handler body as const link = event.target?.closest?.("a[data-jump]"); if (!link) return; followed by the exact lines event.preventDefault(); and document.getElementById(link.getAttribute("data-jump"))?.focus(); with no window.matchMedia reference and no scrollIntoView call, relying on native focus scrolling and P01-T03's CSS scroll-margin-top.
* Action owner: planning_parent
* Exact resolving evidence: Updated P01-T01 and P02-T01 in .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md removing window.matchMedia and scrollIntoView from the delegated click handler and explicitly preserving the consecutive "event.preventDefault();\n    document.getElementById" substring and { focus() } VM mock compatibility.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: assetReconciliationCues mislabels missing reconciliation as Action needed, duplicates State prefixes, and sits above stateCue declaration

* Related IDs: FR-03, AC-03, P01-T02, P02-T01, C4
* Evidence: .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md (lines 124-130, 141-144); .copilot-tracking/plans/2026-11-14/ux-226-asset-exec-wcag-2358-plan.md (line 80); src/api/src/zava_forward/api/web/role-screens.js (lines 221-251, 836-839, 1390-1393); src/api/tests/test_asset_board_screen.py (lines 276, 345).
* Concern: stateCue in src/api/src/zava_forward/api/web/role-screens.js (line 836, mis-cited as line 421 in C4) is defined as `${Object.hasOwn(table, status) ? table[status] : "Action needed"}: ${screenValue(detail)}`. Passing raw m.reconciliation with assetReconciliationCues = { reconciled: "State: Reconciled", unreconciled: "State: Unreconciled", Unknown: "State: Unknown" } has three defects: (1) when m.reconciliation is undefined, null, or "" (as in test_asset_board_screen.py line 345 consumption: {}), Object.hasOwn(table, undefined) evaluates false, dead-coding the Unknown entry and rendering "Action needed: Unknown" instead of an Unknown state; (2) when m.reconciliation is "unreconciled" or "reconciled", stateCue appends ": " + detail, rendering redundant double-colon strings "State: Unreconciled: unreconciled" and "State: Reconciled: reconciled"; and (3) const stateCue is currently declared at line 836 below assetUsage (line 221).
* Impact: Omitted reconciliation evidence is misreported as "Action needed: Unknown" rather than Unknown (violating FR-03 and AC-03), matched values emit malformed duplicated state prefixes, and P02-T01 assertions expecting a State: Unknown prefix on missing reconciliation will fail.
* Smallest useful change: Hoist const stateCue to the shared non-colour state helper section near line 52 of src/api/src/zava_forward/api/web/role-screens.js, normalize const rec = screenValue(m.reconciliation) before lookup, and align assetReconciliationCues with stateCue's prefix: detail format (for example { reconciled: "Recorded", unreconciled: "Action needed", Unknown: "State" } yielding "Recorded: reconciled", "Action needed: unreconciled", and "State: Unknown", or { reconciled: "State", unreconciled: "State", Unknown: "State" } yielding "State: reconciled", "State: unreconciled", and "State: Unknown").
* Action owner: planning_parent
* Exact resolving evidence: Updated FR-03 in .copilot-tracking/plans/2026-11-14/ux-226-asset-exec-wcag-2358-plan.md and P01-T02 / P02-T01 in .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md specifying hoisted stateCue, screenValue(m.reconciliation) normalization, and exact non-duplicated output strings for reconciled, unreconciled, and undefined/null inputs.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Changing Eligibility value breaks Story 226 exact inner_text() check in checks/role_screens_browser_check.py

* Related IDs: FR-03, NFR-02, AC-03, AC-05, P01-T02, P02-T02
* Evidence: src/api/checks/role_screens_browser_check.py (lines 74-93, specifically line 82); src/api/src/zava_forward/api/web/role-screens.js (lines 331-334); .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md (line 138); src/api/checks/scenario-manifest.json.
* Concern: src/api/checks/role_screens_browser_check.py defines SCENARIOS["226"] for "Asset and board view" and asserts exact rendered Chromium inner_text() substring "Eligibility\nUnknown\nResolution owner\nResident Liaison Officer Example". P01-T02 replaces ["Eligibility", "Unknown"] with ["Eligibility", assetState("Unknown", "This page cannot confirm eligibility.")] while excluding src/api/checks/role_screens_browser_check.py from modified files. Note that scenario-manifest.json SHA-locks only workbench-manifest.json, workbench_browser_check.py, dataset.py, and test_workbench.py, not role_screens_browser_check.py.
* Impact: Running python3 -m checks.role_screens_browser_check 226 fails immediately on Story 226 exact evidence because Chromium inner_text() renders "Eligibility\nState: Unknown. This page cannot confirm eligibility.\nResolution owner\nResident Liaison Officer Example".
* Smallest useful change: Either (a) include src/api/checks/role_screens_browser_check.py line 82 in P01-T02 and P02-T02 so SCENARIOS["226"] expects "Eligibility\nState: Unknown. This page cannot confirm eligibility.\nResolution owner\nResident Liaison Officer Example" (verifying mypy still passes on checks/), or (b) add a separate row ["Eligibility state", assetState("Unknown", "This page cannot confirm eligibility.")] immediately before ["Eligibility", "Unknown"] so the contiguous "Eligibility\nUnknown\nResolution owner\nResident Liaison Officer Example" lines stay intact without touching checks/role_screens_browser_check.py.
* Action owner: planning_parent
* Exact resolving evidence: Updated .copilot-tracking/plans/2026-11-14/ux-226-asset-exec-wcag-2358-plan.md and .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md (P01-T02 and P02-T02) either updating src/api/checks/role_screens_browser_check.py line 82 in lockstep or preserving the contiguous Eligibility / Unknown / Resolution owner rows alongside a dedicated state row.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Shared assetCost(report) mutation affects Finance screens without documented substring invariants or Finance test coverage in P02-T02

* Related IDs: FR-03, NFR-02, AC-05, P01-T02, P02-T02
* Evidence: src/api/src/zava_forward/api/web/role-screens.js (lines 201-217, 1574, 1595, 1894); src/api/tests/test_finance_grants_screens.py (lines 259-275); .copilot-tracking/plans/2026-11-14/ux-226-asset-exec-wcag-2358-plan.md (lines 67, 117); .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md (lines 234-243).
* Concern: assetCost(report) is called directly by financeEconomicsPanel(report) at src/api/src/zava_forward/api/web/role-screens.js line 1574 on both finance-invoices and finance-funding. test_finance_grants_screens.py (lines 259-275) asserts substrings "Unknown. No finance-defensible value" and "The AI report could not be loaded, so every AI figure below is Unknown" and absence of "GBP" on failed loads. The plan's Boundaries claim unrelated role screens are untouched, and P02-T02 only runs test_finance_screens_wcag_225, omitting test_finance_grants_screens, test_finance_screen_wcag, and test_finance_grants_screen_wcag.
* Impact: Any slight wording variation in assetCost(report) during P01-T02 implementation can silently regress Finance and Grants unit tests that are excluded from P02-T02's focused unittest selector.
* Smallest useful change: Note in P01-T02 that assetCost(report) is shared with financeEconomicsPanel and must retain exact substrings "Unavailable. The AI report could not be loaded", "so every AI figure below is Unknown", "Loaded", and "Unknown. No finance-defensible value", and add test_finance_grants_screens, test_finance_screen_wcag, and test_finance_grants_screen_wcag to the focused unittest command in P02-T02.
* Action owner: planning_parent
* Exact resolving evidence: Updated P01-T02 notes and P02-T02 validation selector list in .copilot-tracking/plans/2026-11-14/ux-226-asset-exec-wcag-2358-plan.md and .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md including test_finance_grants_screens, test_finance_screen_wcag, and test_finance_grants_screen_wcag.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: P01-T03 states an inaccurate sticky .top CSS premise and uses a literal rem length instead of a design-system spacing token

* Related IDs: FR-04, AC-04, P01-T03, P02-T01, C5, W1
* Evidence: .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md (lines 162-176); .copilot-tracking/research/2026-11-14/ux-226-asset-exec-wcag-2358-research.md (line 48, C5); src/api/src/zava_forward/api/web/style.css (lines 41, 51, 90, 277, 306, 326, 371-377); docs/reference/research/ux/design-system.md (line 104).
* Concern: P01-T03 (following C5) states that .top in style.css has position: sticky; top: 0; z-index: 1000 and sets scroll-margin-top: 4.5rem on .screen-record[id], .screen-evidence h2[tabindex="-1"]. In src/api/src/zava_forward/api/web/style.css, .top is static (only .side at line 306 is sticky), existing heading anchor rules in style.css (.case-section-title at line 277) and progress.css use Fluent spacing tokens (var(--sp-4) and var(--sp-5)), and docs/reference/research/ux/design-system.md line 104 specifies that new CSS rules must use tokens rather than literal lengths.
* Impact: If P02-T01 asserts sticky positioning on .top based on P01-T03's context note, the test will fail immediately; literal 4.5rem also diverges from the design-system token convention in style.css.
* Smallest useful change: Correct the P01-T03 context note to remove the nonexistent sticky .top claim, use a spacing token such as scroll-margin-top: var(--sp-5); (or var(--sp-4), matching .case-section-title in style.css), and ensure P02-T01 asserts only the .screen-record[id] / .screen-evidence h2[tabindex="-1"] scroll-margin-top token rule without asserting position: sticky on .top.
* Action owner: planning_parent
* Exact resolving evidence: Updated P01-T03 and P02-T01 in .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md and FR-04 / AC-04 in .copilot-tracking/plans/2026-11-14/ux-226-asset-exec-wcag-2358-plan.md using a Fluent spacing token for scroll-margin-top and removing the false sticky .top premise.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Strong alignment with repository guardrails: preserves exact screenPanel titles required by src/api/checks/connected_home_browser_check.py and src/api/tests/test_connected_home_check.py, avoids banned internal terms enforced by src/api/tests/test_content_standard.py, preserves read-only control bans and global scope uniqueness against app.js (test_safety_screen_wcag_keyboard.py), keeps all four scenario-manifest.json SHA-locked files untouched, and forbids bulk del sys.modules[...] test pollution.
* Properly maintains Refs #226 commit linkage without claiming full WCAG 2.2 conformance because manual assistive-technology verification (NVDA+Firefox and VoiceOver+Safari) remains an external human gate in docs/reference/research/ux/wcag-conformance-baseline.md.

## Questions or Blocking Evidence Gaps

* None. All five findings are resolvable directly from existing repository source and test files by the planning parent without user input.

## Limitations

* This critique statically verified all referenced web assets, Python unit suites, and Playwright check contracts from repository source; it did not execute live browser or assistive-technology sessions during this read-only planning critique pass.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise .copilot-tracking/plans/2026-11-14/ux-226-asset-exec-wcag-2358-plan.md and .copilot-tracking/details/2026-11-14/ux-226-asset-exec-wcag-2358-phase-details.md to resolve PC-001 through PC-005 (keep the consecutive preventDefault/getElementById?.focus() click handler without window.matchMedia/scrollIntoView, hoist stateCue and normalize screenValue(m.reconciliation) with non-duplicated cue labels, reconcile Eligibility with checks/role_screens_browser_check.py Story 226, add Finance regression suites for shared assetCost, and use a spacing token for scroll-margin-top), then finalize the plan for implementation without another critique pass.
* User response required: No

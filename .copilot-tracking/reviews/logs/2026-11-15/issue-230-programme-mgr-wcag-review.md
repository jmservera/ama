<!-- markdownlint-disable-file -->
# Review: Issue #230 Programme Manager and Coordinator Screens WCAG 2.2 Compliance

## Scope and Evidence

* Task ID: 2026-11-15-issue-230-programme-mgr-wcag
* Review date: 2026-11-15
* Review scope: Full task (`P01` and `P02`: `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Remaining unchecked acceptance criterion on GitHub issue #230 (`Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation`) across `programme-queue` (`overview()` and `render()`) in `src/api/src/zava_forward/api/web/role-screens.js`, unit/accessibility tests in `src/api/tests/test_programme_screen.py` and `src/api/tests/test_programme_screen_wcag.py`, Focused Tier validation (`unittest`, `mypy`, `ruff`, local Chromium Playwright harnesses, and fresh `web-design-guidelines` `command.md` review), and all four already-delivered #230 acceptance criteria.
* Plan: .copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-230-programme-mgr-wcag-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-230-programme-mgr-wcag-research.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/design-system.md, docs/reference/research/ux/content-standard.md, Git diff of `src/api/`, Focused Tier test/type/lint outputs, real Chromium 156.0.8078.4 execution of `checks/programme_paging_browser_check.py`, `checks/role_screens_browser_check.py 230`, `checks/connected_home_browser_check.py`, and `checks/specialist_keyboard_browser_check.py` (`walk_screen` + 8 jump links), and fresh `web_fetch` of `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`.

## Opening Review State

* Interpreted review goal: Verify once with concrete repository, runtime, and browser evidence whether the completed implementation satisfies `FR-01`–`FR-05`, `NFR-01`–`NFR-02`, `AC-01`–`AC-05`, all four `PC-001`–`PC-004` critique dispositions, and Repository Web Development Guidance without regressing the four previously delivered issue #230 criteria or overclaiming human/AT conformance (#155).
* Review scope: Full task (`P01` and `P02`)
* Evidence readiness: Ready; research, plan (`ready` with `[x]` reconciled markers), phase details (`complete`), plan critique (`PC-001`–`PC-004`), changes record (`Complete`), clean `src/api/` Git diff, and Focused Tier command outputs are all present and current.
* Acceptance basis: `FR-01`–`FR-05`, `NFR-01`–`NFR-02`, `AC-01`–`AC-05`, `PC-001`–`PC-004` critique dispositions, `docs/reference/research/ux/wcag-conformance-baseline.md` (#151), `docs/reference/research/ux/design-system.md` (#150), `docs/reference/research/ux/content-standard.md` (#153), and fresh `web-design-guidelines` `command.md`.
* First comparison boundary: Plan-to-change reconciliation across `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`, and `## Follow-Up Items`, excluding live human assistive-technology sign-off (#155) and remote GitHub Actions CI (push prohibited by user instruction).
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/issue-230-programme-mgr-wcag-review.md` (plus RPI Agent session state transition) and does not mutate source code, tests, plan, phase details, critique, research, or changes records.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full boundary comparison on 2026-11-15 across all five RPI artifacts, exact Git diff (`src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_programme_screen.py`, `src/api/tests/test_programme_screen_wcag.py`), Focused Tier unit/conformance/type/lint runs, real Chromium 156 browser harnesses, and fresh `command.md` `file:line` audit (`src/api/src/zava_forward/api/web/role-screens.js`: `✓ pass`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01 (P01-T01, P01-T02): programme-queue WCAG 2.2 Keyboard Jump Navigation and Textual State Labels` | Reconciled | `[x]` checked in plan, `complete` in phase details; `programmeJumpNav` (`<nav class="screen-links" aria-label="...">` + `a[data-jump]`), disjoint `screenJumpTarget` (`tabindex="-1"`), `"aria-live": "polite"` queue statuses, and explicit non-colour state prefixes match reconciled plan and details. |
| `P02` (`P02-T01`, `P02-T02`) | `P02 (P02-T01, P02-T02): WCAG 2.2 Unit/Accessibility Tests and Focused Tier Validation` | Reconciled | `[x]` checked in plan, `complete` in phase details; 2 obsolete `button == 4` assertions updated in `test_programme_screen.py`, 6 focused semantic tests added alongside 3 retained tests in `test_programme_screen_wcag.py` (9 total), and Focused Tier validation recorded in `changes.md`. |
| `## Follow-Up Items` | `#155` live assistive-technology (NVDA/JAWS/VoiceOver) and user walkthrough validation | Reconciled | Preserved outside active `P01`/`P02` claims in both `plan.md` and `changes.md`; commit uses `Refs #230` rather than a closing keyword. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/src/zava_forward/api/web/role-screens.js` | Added `programmeJumpNav`, `programmeOverviewSections` (4 disjoint overview targets), and `programmeSections` (4 disjoint connected-home targets); wired `<nav aria-label="..." class="screen-links">` + `a[data-jump]` + `screenJumpTarget` (`tabindex="-1"`) across `overview()` and `render()`; preserved ``screenPanel(`Connected view for ${c.id}`, ...)`` around sibling `#programme-summary` and `#programme-steps`; removed `programmeJump` and `<div role="group">` jump `<button>`s. | Clean diff in `role-screens.js`; zero `<button>` tags in `render()`; zero `tabindex` inside `journeyStageMap(c)`. | `test_programme_screen_wcag.py`, `test_programme_screen.py`, `test_role_screens_conformance.py`, `test_role_screens_stage_map_focus.py`, `test_connected_home_check.py`, `test_atlas_tensions_checker.py`, Chromium `programme_paging_browser_check`, `connected_home_browser_check`, and `specialist_keyboard_browser_check` + 8 jump links all passed. | Reconciled |
| `P01-T02` | `src/api/src/zava_forward/api/web/role-screens.js` | Added `"aria-live": "polite"` to `#programme-filter-status` and `#programme-page-status`; added explicit non-colour textual state prefixes in `programmeRow()` (`State: Returned. ...`, `State: Not returned. Handoff state: ...`, `State: Not returned`), `programmeFunnel()` (`State: Unknown. ...`, `State: Recorded stage history (not a pass). ...`), and `render()` (`State: Warning. No blocker is recorded...`). | Clean diff in `role-screens.js`; raw step-table cells and existing substrings preserved; zero banned glossary words. | `test_programme_screen.py`, `test_programme_screen_wcag.py`, `test_content_standard.py`, and Chromium `role_screens_browser_check 230` passed. | Reconciled |
| `P02-T01` | `src/api/tests/test_programme_screen.py`, `src/api/tests/test_programme_screen_wcag.py` | Replaced 2 obsolete `button == 4` assertions on read-only `render()` with `assertNotIn("button", tags(node))`; upgraded `SCRIPT` in `test_programme_screen_wcag.py` to wire document `click` delegation and `overview()` + `render()` execution; retained `test_existing_state_cells_are_unchanged` and added 6 semantic tests (9 total). | Clean diff across both test modules within the `<= 10` added-method cap and `0` file deletions. | `unittest` (`Ran 33 tests in 2.925s - OK`), `mypy` (`Success: no issues found in 285 source files`), `ruff check` + `ruff format --check` passed. | Reconciled |
| `P02-T02` | `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md`, `.copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md`, `.copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md` | Executed Focused Tier unit, conformance, browser, `mypy`, `ruff`, and fresh `command.md` `file:line` checks, recorded validation outputs and disclosures, and reconciled plan/detail markers. | Complete changes log and reconciled plan/details. | All executed checks exited `0`; unrun `axe` (`ZF_AXE_JS` unset) and unpushed hosted CI honestly disclosed. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `FR-01`, `FR-02`, `AC-01`, `P01-T01` | Used `programmeJumpNav` (`<nav class="screen-links" aria-label="...">` with `a[data-jump]`, matching `asset-board` #226 and `safety_repairs` #227) and placed the connected-home jump `<nav>` inside ``screenPanel(`Connected view for ${c.id}`, ...)`` right after the intro paragraph so ``Connected view for ZF-1`` stays inside Chromium's initial `content-visibility: auto` layout margin (`top < 2250px` at `1280x900`). | Real Chromium 156 execution of `checks/role_screens_browser_check.py 230` (`style.css` `.screen-record { content-visibility: auto }`); local engineering judgment preserving user intent (`<nav aria-label>` jump links, `tabindex="-1"` targets, delegated `a[data-jump]`, zero edits to `checks/*.py`). | Reconciled `FR-01`, `FR-02`, `AC-01`, `P01-T01` in `plan.md` and `phase-details.md`, and recorded rationale in `changes.md`. | Not needed (immediately relevant local refinement preserving approved architecture, scope, and `PC-001`–`PC-004` dispositions). | Reconciled |
| `FR-04`, `P01-T02` | Used `"State: Recorded stage history (not a pass)."` in `programmeFunnel()` rather than `"not a readiness pass"` to avoid introducing `"readiness"` copy while preserving `"not a pass"` for `test_programme_screen.py`. | Existing `test_programme_screen.py` substring contract and non-readiness boundary (`role_screens_browser_check.py 230`); local engineering judgment. | Reconciled `FR-04` and `P01-T02` across `plan.md`, `phase-details.md`, and `changes.md`. | Not needed (preserves `FR-04` and `AC-03` intent directly). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four critique findings from `.copilot-tracking/reviews/plans/2026-11-15/issue-230-programme-mgr-wcag-plan-critique.md` (`PC-001` preserving ``Connected view for ${c.id}`` around sibling `#programme-summary` and `#programme-steps` + running `test_connected_home_check.py` / `test_atlas_tensions_checker.py`; `PC-002` adding explicit `"aria-live": "polite"` on `#programme-filter-status` and `#programme-page-status`; `PC-003` accurately wiring `SCRIPT` delegation and retaining `test_existing_state_cells_are_unchanged`; `PC-004` loading `web-design-guidelines` + `redesign-existing-projects`, performing fresh `command.md` `file:line` review, and running/disclosing local browser checks and Focused Tier status) were resolved in planning and verified in implementation.
* Material revisions: None. Both implementation-time refinements stayed within the approved 3-file boundary and preserved every requirement and critique disposition without requiring re-planning.
* Dependent-work pause assessment: No dependent work required pausing; execution proceeded in strict `P01-T01` -> `P01-T02` -> `P02-T01` -> `P02-T02` order.
* Justification assessment: Supported by direct unit, conformance, static-analysis, and real-Chromium browser check evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live assistive-technology (NVDA/JAWS/VoiceOver) and user walkthrough validation across specialist screens (#155) | Per `docs/reference/research/ux/wcag-conformance-baseline.md`, automated DOM/keyboard checks cannot substitute for human assistive-technology walkthroughs tracked separately under #155. | Designated accessibility / UX human reviewer under issue #155 (plus pinned local `ZF_AXE_JS` axe 4.10.3 scan when running full UX sign-off). | Open as distinct follow-up work outside active `P01`/`P02` scope; commit uses `Refs #230` accordingly. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No implementation defects, decision gaps, or material evidence gaps were identified across `P01` and `P02`. One non-blocking residual follow-up boundary is recorded below so engineering verification is never conflated with human assistive-technology acceptance or hosted CI execution.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Human assistive-technology walkthrough (#155), pinned `ZF_AXE_JS` scan, and remote hosted CI remain post-commit / external steps

* Related scope: Plan `## Follow-Up Items` and `AC-05` external verification boundary
* Evidence: .copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md, docs/reference/research/ux/wcag-conformance-baseline.md, `checks/role_screens_browser_check.py 230` output (`PARTIAL: axe scan skipped for 4 views (ZF_AXE_JS unset)`), and user prompt instruction (`Do NOT push; leave a clean frozen local commit`).
* Impact: Engineering VDOM, `mypy`, `ruff`, and real-Chromium Playwright checks prove the code-level WCAG 2.2 keyboard jump navigation and textual state contract, while pinned `ZF_AXE_JS` scan, remote hosted CI (post-push), and human screen-reader/zoom sign-off (#155) remain required before closing issue #230 on `main`.
* Destination: follow-up
* Smallest useful next action: Keep `Refs #230` on the local commit; when ready to publish a PR, push `feat/ux-230-programme-mgr-wcag` to observe hosted CI and complete the pinned `ZF_AXE_JS` + #155 assistive-technology walkthrough before closing #230.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| RV-001 | follow-up | Branch owner / human accessibility reviewer (#155) when publishing PR and completing AT sign-off | Non-blocking external / human verification boundary outside this unpushed engineering task |

Later implementation of a routed finding does not require another Review.

## Residual Work

* RV-001: Post-push hosted CI observation, pinned `ZF_AXE_JS` axe 4.10.3 browser scan, and human assistive-technology walkthrough (#155) remain distinct follow-up steps outside this local engineering task.

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest discover -s tests -p "test_*programme*.py" -q` | `src/api/tests/test_programme_screen.py` + `src/api/tests/test_programme_screen_wcag.py` | Passed | `Ran 33 tests in 2.925s - OK` |
| `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest tests.test_accessibility_baseline tests.test_role_screens tests.test_role_screens_conformance tests.test_role_screens_connected_journey tests.test_role_screens_same_home_identity tests.test_role_screens_stage_map_focus tests.test_role_screens_tensions_same_home tests.test_specialist_keyboard_check tests.test_connected_home_check tests.test_atlas_tensions_checker tests.test_design_system tests.test_content_standard -q` | 12 cross-cutting repository conformance suites in `src/api` | Passed | `Ran 133 tests in 1.810s - OK (skipped=3)` |
| `python3 -m mypy` | `src/api` strict typing across `src` and `tests` | Passed | `Success: no issues found in 285 source files` |
| `python3 -m ruff check src tests && python3 -m ruff format --check src tests` | `src/api` lint and formatting | Passed | `All checks passed!` and `200 files already formatted` |
| `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m checks.programme_paging_browser_check` | Real Chromium 156.0.8078.4 (`1280px` and `320px`) | Passed | Pager Tab reachability (`5 <= 6`), boundary focus handoff, scope filter/reset, read-only connected view, and reflow all `PASS` |
| `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m checks.role_screens_browser_check 230` | Real Chromium 156.0.8078.4 (`pam@example.test` + `coordinator@example.test`, `320px`/`390px`/`1280px`) | Passed (axe skipped) | All queue accountability, keyboard filter/reset, 5 independent textual step states, non-readiness, reflow, and read-only checks `PASS`; `ZF_AXE_JS` unset skipped axe scan honestly |
| `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m checks.connected_home_browser_check` | Real Chromium 156.0.8078.4 cross-role connected-home journey | Passed | `programme-queue` (`ZF-1` and `ZF-2`) and cross-role connected-home invariants all `PASS` |
| `specialist_keyboard_browser_check.walk_screen` + 8 `a[data-jump]` links | Real Chromium 156.0.8078.4 (`Retrofit Programme Manager`, `Retrofit Coordinator`, `Programme Support Officer`) | Passed | Full keyboard walk plus measured focus ring, `Enter` target focus (`document.activeElement.id`), and SPA hash route preservation across all 8 jump links |
| Fresh `web_fetch` of `web-design-guidelines` `command.md` `file:line` review | `src/api/src/zava_forward/api/web/role-screens.js` | Passed | `✓ pass` (0 `file:line` findings) |
| Hosted GitHub Actions CI | Remote PR / branch workflows | Skipped | Explicitly skipped per caller instruction (`Do NOT push; leave a clean frozen local commit`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: All planned phases and tasks (`P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`), functional and non-functional requirements (`FR-01`–`FR-05`, `NFR-01`–`NFR-02`), acceptance criteria (`AC-01`–`AC-05`), and critique dispositions (`PC-001`–`PC-004`) are satisfied and reconciled with passing unit, conformance, strict-typing, lint/format, real-Chromium Playwright, and Web Interface Guidelines evidence, while keeping human assistive-technology acceptance (#155) and unpushed hosted CI explicitly bounded under `RV-001`.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | No implementation defects found |
| Decision gap or invalid assumption | none | No planning or decision gaps found |
| Material evidence gap | none | No research gaps found |
| Non-blocking residual work | distinct follow-up (`RV-001`) | Complete #155 human AT walkthrough, pinned `ZF_AXE_JS` axe scan, and post-push hosted CI check before closing #230 |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused Tier passed (`test_*programme*.py` 33/33, 12 conformance suites 133/133, `mypy` 285 files, `ruff check` + `ruff format --check`, real Chromium 156 `programme_paging_browser_check`, `role_screens_browser_check 230` [with `ZF_AXE_JS` unset disclosed], `connected_home_browser_check`, `specialist_keyboard_browser_check` `programme-queue` + 8 jump links, and fresh `command.md` `file:line` review); remote hosted CI skipped because push is prohibited
* Blockers: none

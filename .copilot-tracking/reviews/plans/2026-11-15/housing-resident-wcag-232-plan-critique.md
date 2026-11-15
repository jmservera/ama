<!-- markdownlint-disable-file -->
# RPI Plan Critique: Housing Officer and Resident Engagement WCAG 2.2 AA Baseline (#232)

## Metadata

* Task ID: 2026-11-15-housing-resident-wcag-232
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Focused-tier engineering WCAG 2.2 AA baseline (#151) delivery for issue #232 on branch `feat/ux-232-resident-wcag` targeting parent integration branch `origin/feat/demo-233-same-home-tensions-0825` (PR #1639), covering keyboard jump navigation, row headers, programmatic focus, `aria-live` status announcements, and explicit plain-language textual state cues across neighbourhood housing officer, contact-centre, and resident engagement staff screens (`src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/panels.js`, and `src/api/tests/test_housing_resident_wcag_232.py`), preserving `test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_resident_api.py`, and `specialist_keyboard_browser_check.py`, followed by post-review noreply commit with exact subject `feat(ux): add WCAG 2.2 keyboard jump nav, row headers and state cues for housing and resident screens (Refs #232)`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, clean fetch/rebase onto `origin/feat/demo-233-same-home-tensions-0825`, and clean working tree without pushing.
* Research and evidence considered: `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md`, `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md`, `.copilot-tracking/research/2026-11-15/housing-resident-wcag-232-research.md`, `.copilot-tracking/rpi-sessions/2026-11-15/housing-resident-wcag-232-state.json`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/src/zava_forward/api/web/style.css`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_resident_api.py`, `src/api/tests/test_role_screens.py`, `src/api/tests/test_role_screens_conformance.py`, `src/api/tests/test_housing_resident_screen_wcag.py`, `src/api/tests/test_case_journey.py`, and `src/api/checks/specialist_keyboard_browser_check.py`.
* Decisions, dependencies, and acceptance criteria considered: `FR-1` through `FR-5`, `NFR-1` through `NFR-5`, `AC-1` through `AC-5`, `C1` through `C20`, and phases `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), and `P03` (`P03-T01`, `P03-T02`).
* Assessment boundary: Evaluates technical credibility, static/behavioral test compatibility, scope alignment, and delivery closeout accuracy against the supplied repository code and test contracts. Does not execute live assistive-technology user sessions, which remain explicitly out of scope per issue #151 governance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1, AC-1, P01-T01 | Partial | Contact-centre route alias and `Object.hasOwn` lookup are grounded (`app.js:349,370,428`, `role-screens.js:91`), but direct `isRoleScreensDestination` query-suffix handling needs uniform normalization (`PC-004`). |
| FR-2, AC-2, C4, P01-T02 | Partial | `roleScreensView()` status transitions preserve `specialist_keyboard_browser_check.py:67` settled text, but file-wide `role="status"` claims conflict with 6 out-of-scope specialist-screen nodes in `role-screens.js` and the empty-screen chooser message (`PC-002`). |
| FR-3, AC-3, P01-T02 | Covered | Keyboard `a[data-jump]` focus transfer (`tabIndex = -1`, `focus({ preventScroll: true })`, `scrollIntoView`) matches `role-screens.js:150-169,304-311` and preserves the 2-`setTimeout` conformance guard (`test_role_screens_conformance.py:124`). |
| FR-4, AC-4, C12-C17, P02-T01, P02-T02 | Partial | `actForm` slugged IDs, `.table-scroll` region wrapper, and `<th scope="row">` preserve `test_accessibility_baseline.py:72,87,96`, `test_content_standard.py:19`, and `test_case_journey.py:698` (`PC-004`), but service-request cue wording risks breaking `test_resident_api.py:907` (`PC-001`). |
| FR-5, P03-T01, P03-T02 | Partial | `test_housing_resident_wcag_232.py` covers `FR-1`..`FR-4`, but `P03` omits the contiguous `Response: <status>. Owner: <name>.` regression assertion and `ZF_RESIDENT_BROWSER=1` skip awareness for `test_resident_api.py:857` (`PC-001`). |
| AC-5, Post-review git closeout | Partial | Plan `User Decisions and Requirements` and `AC-5` omit the caller-mandated exact commit subject and clean fetch/rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`PC-003`). |

## Verdict

* Verdict: Revise
* Rationale: Phase decomposition, file ownership, and core WCAG baseline invariants (`aria-invalid` count `9`, `h("table", {}, ...)` count `14`, zero bare `<th>`, `setTimeout` count `2`, `api()` request guard, and banned-jargon avoidance) are well-grounded, but four direct planner corrections (`PC-001` through `PC-004`) are needed before implementation to prevent breaking `test_resident_api.py:907`, colliding with out-of-scope `role="status"` nodes in `role-screens.js`, or missing the caller's post-review rebase and commit-title contract.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Service-request state cue rule omits contiguous `Response: <status>. Owner: <name>.` contract and browser-gated `test_resident_api.py` coverage

* Related IDs: FR-4, AC-4, C16, P02, P02-T02, P03, P03-T01, P03-T02
* Evidence: `src/api/src/zava_forward/api/web/panels.js:257-267`; `src/api/tests/test_resident_api.py:857-916`; `.copilot-tracking/research/2026-11-15/housing-resident-wcag-232-research.md:141`; `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md:71,119,206`; `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md:176,185,199,225,272`
* Concern: `panels.js:257` renders ``Response: ${r.status}. Owner: ${named(r.status_owner)}. Status date: ...``, and `test_resident_api.py:907` explicitly waits for `page.get_by_text("Response: Open. Owner: Rex Coordinator.", exact=False)` alongside `"Response: Closed."` (`875`), `"Remedy: Open."` (`876`), `f"Remedy: {status}."` (`882`), `"Response: Open."` (`890`), and `"Response: Resolved."` (`916`). Plan `What You May Not Know`, `FR-4`, and `P02-T02` require preserving only `"Response: <status>."` and `"Remedy: <status>."`, while cited research `C16` (`housing-resident-wcag-232-research.md:141`) proposes `Response: ${r.status} (${panelServiceCue(r.status)}).`, which breaks both `"Response: Closed."` and `"Response: Open. Owner: Rex Coordinator."`. Even inserting a cue sentence between `"Response: ${r.status}."` and `"Owner: ..."` breaks line `907`. In addition, `ResidentPortalPlaywrightTests` (`test_resident_api.py:857`) is skipped unless `ZF_RESIDENT_BROWSER=1` is set, and Phase Details `P03` line `225` omits `test_resident_api.py` from its coupled suite summary.
* Impact: Implementing `P02-T02` from `FR-4` and `C16` can break `ResidentPortalPlaywrightTests` at `test_resident_api.py:875-916` while a default `unittest` run without `ZF_RESIDENT_BROWSER=1` silently skips the browser test and reports green.
* Smallest useful change: Specify in Plan (`What You May Not Know`, `FR-4`, `P02-T02`) and Phase Details (`P02-T02`) that `residentPanel` places the plain-language state cue outside the contiguous `"Response: ${r.status}. Owner: ${named(r.status_owner)}."` and `"Remedy: ${remedyStatus}. Owner: ..."` substrings (for example, prepending ``State: ${cue}. Response: ${r.status}. Owner: ${named(r.status_owner)}...``). Add a direct Node VM assertion for `"Response: Open. Owner: ..."` and `"Remedy: Open."` in `P03-T01` (`src/api/tests/test_housing_resident_wcag_232.py`), list `src/api/tests/test_resident_api.py` in Phase Details `P03` Validation Expectations, and run `ZF_RESIDENT_BROWSER=1` in `P03-T02` when Playwright Chromium is available (disclosing explicitly if browser prerequisites prevent it).
* Action owner: planner
* Exact resolving evidence: `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md` (`What You May Not Know`, `FR-4`, `P02-T02`, `P03-T01`) and `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md` (`P02-T02`, `P03`, `P03-T01`, `P03-T02`) preserve the exact contiguous `"Response: ${r.status}. Owner: ${named(r.status_owner)}."` contract required by `src/api/tests/test_resident_api.py:907` and cover `ZF_RESIDENT_BROWSER=1` execution/disclosure.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: File-wide `role="status"` `aria-live="polite"` requirement in `role-screens.js` conflicts with 6 out-of-scope specialist-screen nodes and empty-chooser state

* Related IDs: FR-2, AC-2, C4, P01, P01-T02, P03-T01
* Evidence: `src/api/src/zava_forward/api/web/role-screens.js:51,122-145,789,905,1411,1488,1502,1706`; `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md:103,111,183`; `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md:42,99,119`
* Concern: Plan `FR-2` (`line 111`), Plan `P01-T02` (`line 183`), and Phase Details `P01-T02` Validation Expectations (`line 119`) state that every `role="status"` node in `role-screens.js` carries `aria-live="polite"`, while Phase Details `P01` Likely Targets (`line 42`, citing `line 34` instead of `role-screens.js:51`) and `P01-T02` Context (`line 99`) list only the 3 shared-host nodes (`screenTable` truncation at `role-screens.js:51`, loading at `role-screens.js:129`, and queue count at `role-screens.js:145`). `role-screens.js` contains 6 additional `role: "status"` nodes without `"aria-live": "polite"` inside out-of-scope specialist screens (`technical-queue` at `789`, `quality-queue` at `905`, `programme-exceptions` at `1411,1488,1502`, and `funding-evidence` at `1706`), which Plan `Scope and Non-Goals` (`line 103`) forbids editing. In addition, `roleScreensView()` at `role-screens.js:122-128` renders `"No specialist screens are installed for your role on this branch. Use your existing work list."` when `installed.length === 0`, whereas `FR-2` specifies announcing `${role}. Specialist screens. Choose a screen.` unconditionally, and async `#workspace-status` writes around `await api(...)` need `signal.aborted` protection so superseded routes do not clobber `#workspace-status`.
* Impact: `P03-T01` will either fail a literal file-wide `role-screens.js` `role="status"` check on lines `789,905,1411,1488,1502,1706` or push the implementer to modify 4 out-of-scope specialist screens in violation of `Non-Goals`; unentitled roles on `#/screens` would also hear `"Choose a screen."` when zero screens exist.
* Smallest useful change: Scope `FR-2`, `P01-T02`, and `P03-T01` to the shared specialist-screen host (`role-screens.js:51,129,145`) and the `#232` screens (`resident-choice`, `resident-service-issues`), correct the `screenTable` line reference to `role-screens.js:51`, branch the `!screen` `#workspace-status` announcement on `installed.length` (for example, `Choose a screen.` vs `No specialist screens installed.`), and guard `workspaceStatus` updates with `!signal.aborted`.
* Action owner: planner
* Exact resolving evidence: `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md` (`FR-2`, `P01-T02`) and `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md` (`P01`, `P01-T02`, `P03-T01`) align `role="status"` assertions to `role-screens.js:51,129,145` and rendered `#232` screens, branch `!screen` status text on `installed.length`, and guard aborted transitions.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Plan closeout criteria omit caller-mandated commit subject and rebase onto `origin/feat/demo-233-same-home-tensions-0825`

* Related IDs: AC-5, P03, P03-T02
* Evidence: Caller `Post-review git requirement`; `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md:86,138`; `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md:260-278`
* Concern: The caller explicitly requires committing with exact subject `feat(ux): add WCAG 2.2 keyboard jump nav, row headers and state cues for housing and resident screens (Refs #232)` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, then fetching and rebasing cleanly onto `origin/feat/demo-233-same-home-tensions-0825` without pushing. Plan `User Decisions and Requirements` (`line 86`) and `AC-5` (`line 138`) capture local noreply commit, `Refs #232`, trailer, clean `git status --short`, and no push, but omit both the exact commit subject and the fetch/rebase step. Because repository workflow rules prohibit rebasing unless explicitly requested, downstream implementation/closeout stages will not rebase onto `origin/feat/demo-233-same-home-tensions-0825` unless the plan records that requirement.
* Impact: Post-review closeout risks using a non-matching commit title and leaving `feat/ux-232-resident-wcag` un-rebased against `origin/feat/demo-233-same-home-tensions-0825` (or skipping post-rebase verification if the parent branch moved).
* Smallest useful change: Record the exact commit subject `feat(ux): add WCAG 2.2 keyboard jump nav, row headers and state cues for housing and resident screens (Refs #232)` and post-review `git fetch origin feat/demo-233-same-home-tensions-0825` + clean `git rebase origin/feat/demo-233-same-home-tensions-0825` (re-running targeted tests if rebase changes `HEAD`'s parent) in Plan `User Decisions and Requirements`, `AC-5`, and Phase Details `P03-T02`.
* Action owner: planner
* Exact resolving evidence: `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md` (`User Decisions and Requirements`, `AC-5`) and `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md` (`P03-T02`) specify the exact commit title and fetch/rebase onto `origin/feat/demo-233-same-home-tensions-0825`.
* Decision route: Direct planner correction (explicitly decided by caller requirements; no user decision required).

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: `isRoleScreensDestination` query-suffix normalization in `app.js` and `test_case_journey.py` string-slice anchors in `panels.js` are implicit

* Related IDs: FR-1, FR-4, P01-T01, P02-T01, P02-T02
* Evidence: `src/api/src/zava_forward/api/web/app.js:349,370-376,428,442`; `src/api/src/zava_forward/api/web/panels.js:17,43,190-213`; `src/api/tests/test_case_journey.py:698-706,990`; `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md:179,197`; `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md:39,86,147-165`
* Concern: `app.js:370-376` currently checks `destination === ...` without stripping `?query` because internal callers (`app.js:349,428,442`) pre-split `hash.split("?")[0]`, whereas `P01-T01` (`housing-resident-wcag-232-plan.md:179` and `housing-resident-wcag-232-phase-details.md:39,86`) requires direct calls with query strings (`#/role/contact_centre?...`) to return `true`. Handling `?` only for `#/role/contact_centre` would leave `#/role/housing_officer?...` and `#/role/resident_engagement?...` inconsistent under direct helper tests. Separately, `test_case_journey.py:698-706` extracts code from `panels.js` via exact substring splits (`"function bindCaseMutationForm"`, `"function actForm"`, `"  const residentForm = "`, `"  const serviceForm"`, `"  const formFor = "`, `"  const staff"`) and concatenates `ops.js + panels.js` (`line 990`).
* Impact: Ad-hoc query checks in `isRoleScreensDestination` or top-level helper placement/anchor reformatting in `panels.js` can break `P03-T01` route assertions or `test_case_journey.py` VM slices.
* Smallest useful change: Note in `P01-T01` that `isRoleScreensDestination(raw)` strips `?query` first (`const destination = String(raw || "").split("?")[0];`) across all role routes, and note in `P02-T01` / `P02-T02` to keep slug/cue helpers scoped inside `actForm` and `residentPanel` while preserving `test_case_journey.py`'s exact function/const split anchors in `panels.js`.
* Action owner: planner
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md` (`P01-T01`, `P02-T01`, `P02-T02`) specifies `split("?")[0]` normalization in `isRoleScreensDestination` and local helper scoping that preserves `src/api/tests/test_case_journey.py:698-706,990` anchors.
* Decision route: Direct planner correction (no user decision required).

## Strengths and Residual Risk

* Strong static-guard grounding: The plan accurately accounts for `test_accessibility_baseline.py` (`aria-invalid` count `9`, `h("table", {}, ...)` count `14`, zero bare `<th>`, `position:fixed` count `2`), `test_content_standard.py` banned vocabulary (`m.flag === "Proceed"` instead of `"Hold"` at `panels.js:171`), `test_role_screens.py` `request_findings()` and design-system class checks (`.screen-links` already documented in `style.css:35-38`), and `test_role_screens_conformance.py` `timer_findings()` (`setTimeout` count `2`).
* Clean phase isolation: `P01` (`app.js`, `role-screens.js`), `P02` (`panels.js`), and `P03` (`test_housing_resident_wcag_232.py` + validation) have non-overlapping file ownership and preserve human/resident approval and consent boundaries (`NFR-5`).
* Accepted residual risk: `specialist_keyboard_browser_check.py:55` lists `"resident-service-issues"` in `NO_REGION_GAPS`, while parent branch `feat/demo-233-same-home-tensions-0825` already added `redressRoutePanel` (`Routes to ask` table at `role-screens.js:2114`). Keeping `specialist_keyboard_browser_check.py` untouched under Focused tier while adding zero tables to `resident-choice` or `resident-service-issues` and preserving settled `expected_status()` (`role-screens.js:180`) avoids unauthorized gate-tool modification and is properly tracked as a `#233` parent-branch follow-up.

## Questions or Blocking Evidence Gaps

* None. All four findings are direct planner corrections fully resolved by supplied codebase contracts and caller instructions.

## Limitations

* Static, Node VM, and Playwright DOM checks verify programmatic semantics, focus transfer, live-region text, and non-colour text cues, which per `docs/reference/research/ux/wcag-conformance-baseline.md` do not substitute for assistive-technology and resident/staff acceptance testing under issue #151.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planner
* Smallest next action: Apply direct planner revisions for `PC-001` through `PC-004` to `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md` and `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md`, then finalize the plan for `rpi-implement` without another critique pass.
* User response required: No

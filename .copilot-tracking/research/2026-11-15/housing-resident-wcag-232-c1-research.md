<!-- markdownlint-disable-file -->

# Task Research: housing-resident-wcag-232-c1

| Field              | Value                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                              |
| Researcher / agent | RPI Agent (`rpi-research`)                                                              |
| Status             | Complete                                                                                |
| Artifact path      | .copilot-tracking/research/2026-11-15/housing-resident-wcag-232-c1-research.md          |

## Research Brief

* What to research: Three-way rebase and WCAG 2.2 AA compatibility between `feat/ux-232-resident-wcag` (`HEAD` `cffec920a`, parent `184b828e1`, merge-base `a1d0be5f6`) and the updated `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, which merged PR #1784 for Issue #230), across `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/src/zava_forward/api/web/style.css`, and all coupled WCAG/baseline/content unit suites.
* Why it matters: `origin/feat/demo-233-same-home-tensions-0825` advanced by commit `6510b6fbc` (#230 programme/coordinator WCAG 2.2 AA conformance), creating a three-way merge conflict on `PR #1786` (`feat/ux-232-resident-wcag`). Both #230 and #232 route aliases, jump targets, landmarks, row headers, live announcements, and non-colour textual state cues must coexist cleanly without breaking any counted baseline or cross-screen WCAG invariant.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases of the Cycle 1 (`c1`) automatic RPI loop for Issue #232 (`PR #1786`).
* Scope: `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/src/zava_forward/api/web/style.css`, `src/api/checks/case_journey_browser_check.py`, `src/api/tests/test_housing_resident_wcag_232.py`, `src/api/tests/test_programme_coordinator_wcag_230.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_procurement_contractor_screen_wcag.py`, and `.copilot-tracking/` Cycle 1 (`c1`) + parent changes cross-reference artifacts.
* Non-goals: Running `git push`; altering #230 coordinator/programme semantics or #232 resident/housing boundaries; adding resident contact triggers or role simulators; rewriting Cycle 0 critique or review verdicts.
* Criteria: Clean rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`); 100% preservation of #230 (`#/role/programme_manager`, `#/role/retrofit_coordinator`, `programme-shared-queue`, `programme-funnel` ["Lifecycle and funnel"], `programmeCell`, `programmeQueue`, `programmeFunnel`, `programmeStepCell`, `programmeJumpNav`, `coordinatorView` + `mapPanel` landmarks/cues) and #232 (`#/role/contact_centre`, `resident-choice`, `resident-service-issues`, `residentPanel` / `#/my-home` & `#/case/<id>?tab=resident`, `#workspace-status` `announce()`, `screen-queue` / `screen-evidence` landmarks and `data-state-cue` spans, inline `document.getElementById` jump focus); green focused validation (`unittest`, `ruff check`, `mypy`) and clean frozen commit without pushing.
* Requested outputs: Three-way conflict analysis, cross-suite invariant check, convergence recommendation, and Planning Readiness for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                             | Value                                                                                                                                                                     |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)              | Q1–Q5 covering branch divergence, exact conflict hunks in `app.js` and `role-screens.js`, #230 vs #232 identifier/DOM invariants, baseline guards, and commit/artifact rules |
| Codebase scope                    | `src/api/`, `docs/reference/research/ux/`, `.copilot-tracking/`                                                                                                           |
| External scope                    | Vercel Web Interface Guidelines (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`)                                                |
| Initial internal candidate areas  | `src/api/src/zava_forward/api/web/{app.js,role-screens.js,panels.js,style.css}`, `src/api/tests/test_*wcag*.py`, `src/api/tests/test_{accessibility_baseline,content_standard}.py` |
| Initial external candidate areas  | Vercel Web Interface Guidelines (`command.md`)                                                                                                                            |
| Research posture                  | focused                                                                                                                                                                   |
| Posture provenance                | default (bounded internal rebase and conflict-resolution task with named target branch, files, and validation commands)                                                   |
| Explicit limits / deadline        | Non-interactive CLI run; Focused validation tier; leave clean frozen commit with Copilot trailer; do NOT run `git push`                                                   |
| Posture-specific completion basis | Complete three-way inspection of every commit between merge-base `a1d0be5f6`, upstream `6510b6fbc`, and local `cffec920a`, plus verification of all coupled test contracts |
| Edits allowed during research?    | no, research-only (only `git fetch` remote-tracking update and `.copilot-tracking/` Cycle 1 research/state writes)                                                        |
| Resolved evidence root            | `.copilot-tracking/`                                                                                                                                                      |
| Known constraints / excluded sources | Preserve Fluent 2 tokens, WCAG 2.2 baseline (#151), plain-language content standard (#153), counted baseline guards, original Cycle 0 critique/review outcomes, and `Refs #232` |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                                         | Scoped authority or output contract                                              | Selected / skipped reason                                                        |
|---------------------|-----------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and tracking paths         | Enforces AMA repo rules, privacy-safe git email, Focused tier, `Refs #232`       | Selected: mandatory repository instruction                                       |
| Skill               | `rpi-research`                    | Phase skill for Research in RPI Agent                        | Governs three-wave research artifact and readiness handoff                       | Selected: active RPI phase contract                                              |
| Skill               | `accessibility`                   | Matches WCAG 2.2 AA cross-screen verification (#230 + #232)  | Supplies WCAG 2.2 / ARIA APG criteria across merged role screens                 | Selected: loaded at intake                                                       |
| Skill               | `web-design-guidelines`           | Required by AMA Web Development Guidance before web edits    | Supplies fetched Vercel Web Interface Guidelines rules (`file:line` review)      | Selected: loaded and fetched at intake                                           |
| Skill               | `redesign-existing-projects`      | Required by AMA Web Development Guidance for existing-app UX | Targeted audit within existing vanilla JS/CSS stack without visual overhaul      | Selected: loaded at intake; constrained by Fluent 2, WCAG, and content standards |
| Skill               | `design-taste-frontend`           | Public marketing/landing page art direction                  | Explicitly "Not for dashboards or app screens"                                   | Skipped: internal staff/resident casework demonstrator                           |
| Research specialist | `hve-core-all:rpi-researcher`     | General delegated research lane                              | Bounded lane artifact under `.copilot-tracking/research/subagents/`              | Skipped (inline preferred): exact 2-commit vs 1-commit merge-tree fits direct inspection |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                    | Answers / unanswered | Resulting decision or selected further research                                     |
|------------------|----------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit rebase target, conflict guidance, validation commands, and no-push constraint | Not applicable | Proceed in confirmed automatic mode with `focused` posture and inline three-wave inspection |
| Direction change | None encountered during Cycle 1                                                                          | Not applicable       | Maintain caller scope and boundaries                                                |
| Convergence      | All Q1–Q5 questions resolved from read-only `git merge-tree` and commit diffs                            | Not applicable       | Converged on Selected Recommendation Option B; Planning Readiness = `Ready`         |

## Scope and Success Criteria

* Scope: Rebase `feat/ux-232-resident-wcag` (`184b828e1` + `cffec920a`) onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), resolve overlaps in `app.js` and `role-screens.js`, verify combined #230 + #232 WCAG/baseline/copy test suites, and record Cycle 1 RPI artifacts cleanly.
* Assumptions:
  * Caller prompt's shorthand labels (`programme-shared-queue`, `programme-lifecycle-funnel`, `housing-resident-queue`, `resident-service-issues`, `resident-my-home`) refer to the concrete repository anchors and screen/panel surfaces introduced or guarded by #230 and #232 — verified in Wave 1 and Wave 2 below.
* Success criteria:
  * Every divergent file and hunk between `a1d0be5f6..6510b6fbc` and `a1d0be5f6..cffec920a` is catalogued with exact `C#` `path:line` evidence.
  * Every potential cross-suite interaction (`test_housing_resident_wcag_232.py`, `test_programme_coordinator_wcag_230.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_procurement_contractor_screen_wcag.py`, `test_asset_exec_screen_wcag.py`, `test_technical_quality_screens_wcag.py`) is checked before editing.
  * Research remains strictly read-only on repository source files.

## Task Research Requests

* Explicit requests:
  1. Fetch `origin/feat/demo-233-same-home-tensions-0825` and rebase `feat/ux-232-resident-wcag` onto it.
  2. Resolve conflicts in `role-screens.js` (and any other conflicted file, notably `app.js`) preserving both #230 and #232 changes.
  3. Run focused validation (`unittest` across 5 suites, `ruff check`, `mypy`).
  4. Update `.copilot-tracking/` research, plan/details, changes, and review artifacts for the rebased head.
  5. Leave a clean Conventional Commit with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and do NOT push.
* Inferred research questions:
  * Does `git merge-tree` show conflicts only in `role-screens.js`, or also in `app.js`?
  * Do `#230`'s new `style.css` rules, `app.js` coordinator changes, or `role-screens.js` `screenTable(..., rowHeader=true)` / `data-state-cue` additions alter any counted baseline or regex guard in `#232` or peer WCAG tests?

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Rebase `feat/ux-232-resident-wcag` onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) preserving #230 + #232 | Caller intake | Bounds implementation to rebase conflict resolution, cross-branch regression check, and RPI tracking |
| exclude                                                  | Do NOT run `git push`; do NOT rewrite Cycle 0 critique/review verdicts                                  | Caller intake + AMA instructions | Keeps publication gated for coordinator review and preserves historical Cycle 0 RPI gates |

## Research Questions

|  # | Sub-question                                                                                                                                              | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | What is the exact commit divergence between `feat/ux-232-resident-wcag` and `origin/feat/demo-233-same-home-tensions-0825`, and which files conflict?      | breadth                                  | H        | answered |
| Q2 | How do `app.js` and `role-screens.js` hunks in `#230` (`6510b6fbc`) and `#232` (`184b828e1`, `cffec920a`) interact line-by-line?                          | depth                                    | H        | answered |
| Q3 | How do the caller-named identifiers map to concrete DOM IDs, screen registrations, and test assertions in `#230` and `#232`?                              | depth                                    | H        | answered |
| Q4 | Could `#230` + `#232` combined break any counted baseline (`test_accessibility_baseline.py`), copy check (`test_content_standard.py`), or peer WCAG suite? | depth                                    | H        | answered |
| Q5 | Should the two local `#232` commits (`184b828e1` + `cffec920a`) stay separate or be squashed/topped cleanly with Cycle 1 tracking so history is atomic?   | straightforward                          | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed:
  * `.copilot-tracking/research/2026-11-15/housing-resident-wcag-232-research.md`
  * `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md`
  * `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`
  * `.copilot-tracking/reviews/logs/2026-11-15/housing-resident-wcag-232-review.md`
  * `.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-c1-state.json`
* Reused (verified) findings:
  * Cycle 0 `#232` implementation (`184b828e1`) and post-check fixup (`cffec920a`) already passed Focused validation, Playwright + pinned `axe-core 4.10.3`, `ruff`, `mypy`, and `rename-zava-tests.py` on merge-base `a1d0be5f6`.
  * Repository convention (`a1d0be5f6` `#231`) records post-review rebase/fixup iterations as a child `*-c1` RPI loop (`parent_task` pointing to Cycle 0) so original critique/review gates remain immutable.
* Superseded / stale:
  * `origin/feat/demo-233-same-home-tensions-0825` moved forward from `a1d0be5f6` to `6510b6fbc` (`PR #1784`, `#230`); all overlap claims were verified fresh via `git fetch` and read-only `git merge-tree`.

## Cycle 1 Execution

### Wave 1 — Wider (Breadth Discovery)

* **C1 (`git merge-base` / commit topology)**: `git fetch origin feat/demo-233-same-home-tensions-0825` updated the remote-tracking ref to `6510b6fbc38533a16b9492cacd3ab7e7331c1610` (`feat(ux): complete WCAG 2.2 keyboard and state-cue conformance for programme coordinator screens (Refs #230) (#1784)`). The merge base with local `HEAD` (`cffec920ab32dd3e9132e872692710de1f3199b2`) is `a1d0be5f611eeb1f3b5bb88f996bb9448a6e72b0` (`#231` `PR #1767`). Upstream has 1 commit (`6510b6fbc`) touching 5 code/test files (`app.js`, `role-screens.js`, `style.css`, `test_programme_coordinator_wcag_230.py`, `test_programme_screen_wcag.py`) plus `.copilot-tracking/*230*`; local has 2 commits (`184b828e1`, `cffec920a`) touching 6 code/test files (`app.js`, `role-screens.js`, `panels.js`, `case_journey_browser_check.py`, `test_housing_resident_wcag_232.py`, `test_procurement_contractor_screen_wcag.py`) plus `.copilot-tracking/*housing-resident-wcag-232*`.
* **C2 (`src/api/src/zava_forward/api/web/app.js:370-380`)**: Read-only `git merge-tree a1d0be5f6 6510b6fbc cffec920a` surfaced a direct conflict in `isRoleScreensDestination(destination)`: `#230` kept `destination === ...` and appended `#/role/programme_manager` and `#/role/retrofit_coordinator`, whereas `#232` normalized `const target = String(destination || "").split("?")[0];` and inserted `#/role/contact_centre`.
* **C3 (`src/api/src/zava_forward/api/web/role-screens.js:92-102`)**: Both branches edited `ROLE_HASH_SCREENS`: `#232` inserted `"#/role/contact_centre": "resident-service-issues"` at line 96, while `#230` appended `"#/role/programme_manager": "programme-queue"` and `"#/role/retrofit_coordinator": "programme-queue"` after `"#/role/contractor": "contractor-job-pack"`.
* **W1 (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`, retrieved 2026-11-15)**: Re-verified Web Interface Guidelines rules governing semantic `<nav>`, `aria-label` / `aria-labelledby` landmarks, `aria-live="polite"` status regions, programmatic focus management without layout shift, visible `:focus-visible` rings, and keyboard-operable scroll containers.

### Wave 2 — Deeper (Line-by-Line Contract & Identifier Verification)

* **C4 (`src/api/src/zava_forward/api/web/role-screens.js:49-185, 317-326`)**: Every `#232` change in `role-screens.js` outside `ROLE_HASH_SCREENS` sits in shared host functions above line 330:
  * `screenTable` (`role-screens.js:52`): `rows.length > limit && h("p", { role: "status", "aria-live": "polite" }, ...)`.
  * `roleScreensView` (`role-screens.js:105-148`): `!signal.aborted`-guarded `announce(text)` helper updating `#workspace-status` on invalid-page, unavailable-screen, chooser, loading (`aria-live="polite"`), and record-mismatch paths, while preserving settled `#workspace-status` wording.
  * `roleScreensView` landmarks (`role-screens.js:154-179`): `isResidentRoleScreen` (`resident-choice` or `resident-service-issues`) sets `id="screen-queue"` + `tabindex="-1"` on `#screen-queue-heading`, `aria-live="polite"` on the queue count `role="status"` node, `id="screen-evidence"` alongside preserved `class="screen-evidence"` and `aria-label="Evidence for ${c.id}"`, `<h2 id="screen-evidence-heading" tabindex="-1">`, and `span[data-state-cue="scope"]`.
  * Jump delegation (`role-screens.js:323-324`): `cffec920a` restored the two-line `document.getElementById(link.getAttribute("data-jump"))?.focus?.();` and `...?.scrollIntoView?.({ block: "start" });` pattern pinned by `src/api/tests/test_asset_exec_screen_wcag.py`.
* **C5 (`src/api/src/zava_forward/api/web/role-screens.js:444-533, 676-740` in `6510b6fbc`)**: Every `#230` change in `role-screens.js` outside `ROLE_HASH_SCREENS` sits inside the programme-queue block (lines 444–740):
  * `programmeCell` tri-state `span.flag` (`data-state-cue`: `"returned"`, `"handoff"`, `"not-returned"`), `programmeQueue` `#programme-scope` `aria-describedby="programme-page-status programme-filter-status"` and `screenTable(..., true)` row headers.
  * `programmeFunnel` `data-state-cue="unknown"` / `"stage-history"` and `screenRecordTable("Lifecycle and funnel by stage", ...)` inside `screenJumpTarget("programme-funnel", screenPanel("Lifecycle and funnel", ...))` paired with `screenJumpTarget("programme-shared-queue", ...)`.
  * `programmeStepCell`, `programmeJumpNav` (`data-jump-target: id`), `programmeOverviewSections` (`programme-shared-queue`, `programme-funnel` ["Lifecycle and funnel"]), and `programme-steps` `screenTable(..., 50, programmeStepCell, true)`.
* **C6 (`src/api/src/zava_forward/api/web/role-screens.js:1016-1091, 2195-2245` & `src/api/src/zava_forward/api/web/panels.js:24-45, 290-395`)**: Confirmed exact repository identifiers corresponding to the caller's summary terms: `#230` uses `programme-shared-queue` and `programme-funnel` ("Lifecycle and funnel"); `#232` uses `resident-choice` (housing/resident choice & update queue), `resident-service-issues` (wired to `#/role/housing_officer` and `#/role/contact_centre`), and `residentPanel` / `#/my-home` (`panels.js` & `app.js`), plus `#workspace-status` announcements and `section#screen-evidence` landmarks/cues.
* **C7 (`src/api/src/zava_forward/api/web/app.js:2530-2860` & `src/api/src/zava_forward/api/web/style.css:374-390` in `6510b6fbc`)**: `#230`'s `mapPanel` (`aria-labelledby="map-title"`), `coordinatorView` jump nav/tri-state cues, and `style.css` `.coordinator h2[tabindex="-1"]:focus-visible, .screen-record h2[tabindex="-1"]:focus-visible` + `.coordinator .heat-present` rules do not touch `#232`'s lines and preserve standalone `[tabindex="-1"]:focus` in `style.css`.

### Wave 3 — Contrarian (Cross-Branch Failure Modes & Alternative Histories)

* **C8 (`src/api/tests/test_programme_coordinator_wcag_230.py:763-918`)**: Checked whether `#232`'s `roleScreensView` `announce()`, `aria-live="polite"`, or `isRoleScreensDestination` `split("?")[0]` normalization breaks `#230`'s tests:
  * In `test_role_hash_route_aliases_script_loading_and_rbac`, `#230` tests `#/role/programme_manager` and `#/role/retrofit_coordinator?case=C-1&scope=all`. Normalizing `const target = String(destination || "").split("?")[0];` in `isRoleScreensDestination` handles both bare and query-bearing hashes (`target === "#/role/programme_manager" || target === "#/role/retrofit_coordinator"`), even when `isRoleScreensDestination` is called directly with a query string!
  * `#230` asserts `ok_badges == []` and checks `cues` (`data-state-cue` elements) on `programme-queue`: `#232`'s `span[data-state-cue="scope"]` on `selected` is gated by `isResidentRoleScreen` (`screen.id === "resident-choice" || screen.id === "resident-service-issues"`), so `programme-queue` does NOT receive `data-state-cue="scope"` (which contains `"State: Confirmed - single-home record scope."` and would otherwise have collided with `#230`'s `assertNotIn(cue_attr, {"pass", "ready", "confirmed"})`!). That `isResidentRoleScreen` gate prevents a subtle cross-screen test failure!
* **C9 (`src/api/tests/test_accessibility_baseline.py` & `src/api/tests/test_content_standard.py`)**: Checked whether `#230` + `#232` combined changes any counted baseline invariant:
  * `#230` modified `const table = (title, headers, rows, headingId) => ...` in `app.js` in-place without adding a new `h("table", {}, ...)` call, keeping total `h("table", {}, ...)` across `app.js` + `panels.js` at `14`, `aria-invalid` at `9`, bare `h("th", {}` at `0`, and `position:fixed` at `2`.
  * Neither branch adds banned jargon under `test_content_standard.py`.
* **C10 (`src/api/tests/test_housing_resident_wcag_232.py:735-775`)**: Checked whether `test_housing_resident_wcag_232.py` asserts an exact key list on `ROLE_HASH_SCREENS`: it tests targeted `isRoleScreensDestination` calls rather than freezing dict length, and we can add a cross-branch regression assertion verifying that `#/role/programme_manager`, `#/role/retrofit_coordinator`, `#/role/housing_officer`, `#/role/contact_centre`, and `#/role/resident_engagement` all resolve `isRoleScreensDestination(...) === true` (with and without query strings) and coexist in `ROLE_HASH_SCREENS`.

## Synthesis by Research Question

* **Q1 (Divergence & Conflicts)**: `feat/ux-232-resident-wcag` (`184b828e1`, `cffec920a`) and `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) diverge at `a1d0be5f6`. Only `app.js` (`isRoleScreensDestination`) has a three-way git conflict, and `role-screens.js` (`ROLE_HASH_SCREENS`) has an adjacent dict insertion requiring careful verification (`C1`–`C3`).
* **Q2 (Line-by-Line Merge)**: Merging `isRoleScreensDestination(destination)` in `app.js` using `const target = String(destination || "").split("?")[0];` across all 10 destinations (`#/screens` + 9 `#/role/*` aliases including `contact_centre`, `programme_manager`, `retrofit_coordinator`) and merging all 9 `#/role/*` entries in `ROLE_HASH_SCREENS` in `role-screens.js` preserves 100% of both branches' hunks (`C2`–`C5`, `C7`).
* **Q3 (Identifier Mapping)**: Verified every #230 (`programme-shared-queue`, `programme-funnel` ["Lifecycle and funnel"], `#/role/programme_manager`, `#/role/retrofit_coordinator`) and #232 (`resident-choice`, `resident-service-issues`, `residentPanel` / `#/my-home`, `#/role/contact_centre`, `#workspace-status`, `section#screen-evidence`) surface (`C4`–`C6`).
* **Q4 (Cross-Suite Invariants)**: `isResidentRoleScreen` cleanly isolates `data-state-cue="scope"` from `programme-queue`, and counted table/ARIA/CSS/content-standard baselines remain exact (`C8`, `C9`).
* **Q5 (Commit Lineage & Tracking)**: Replaying `184b828e1` and `cffec920a` onto `6510b6fbc` via `git rebase origin/feat/demo-233-same-home-tensions-0825` (resolving `app.js` / `role-screens.js` during rebase) and recording the Cycle 1 (`housing-resident-wcag-232-c1-*`) RPI artifacts, cross-branch regression assertion in `test_housing_resident_wcag_232.py`, and Cycle 0 `housing-resident-wcag-232-changes.md` rebase addendum in a clean Conventional Commit on top preserves rebased commit provenance and immutable Cycle 0 critique/review artifacts (`C1`, `C10`).

## Alternatives Considered and Convergence Recommendation

| Option | Summary                                                                                                                                                              | Pros                                                                                   | Cons / Rejection or selection rationale                                                                                     |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| A      | Merge `origin/feat/demo-233-same-home-tensions-0825` into `feat/ux-232-resident-wcag` with `git merge`.                                                              | Single merge commit.                                                                   | **Rejected**: Violates explicit caller Step 1 (`rebase feat/ux-232-resident-wcag onto origin/feat/demo-233-same-home-tensions-0825`). |
| B      | **Selected**: Rebase `feat/ux-232-resident-wcag` onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), union-merge `isRoleScreensDestination` (`split("?")[0]` + all 10 routes) in `app.js` and `ROLE_HASH_SCREENS` (all 9 `#/role/*` routes) in `role-screens.js` while keeping all `#230` and `#232` hunks intact, add a cross-branch `#230`+`#232` route/cue coexistence check in `test_housing_resident_wcag_232.py`, run focused validation, and commit Cycle 1 RPI artifacts cleanly without pushing. | Satisfies every caller step, preserves Cycle 0 critique/review immutability, and locks `#230`+`#232` coexistence with automated tests. | **Selected**: Clean linear history on `6510b6fbc` with zero regressions (`C1`–`C10`, `W1`).                                 |
| C      | Overwrite Cycle 0 `housing-resident-wcag-232-plan-critique.md` and `housing-resident-wcag-232-review.md` in place instead of recording Cycle 1 (`c1`) artifacts.     | Fewer files in `.copilot-tracking/`.                                                   | **Rejected**: Violates AMA Repository Instructions (`Preserve original critique/Review outcomes`) and RPI one-pass gate contract. |

## Risks, Constraints, and Current Decisions

* **Confirmed decisions**:
  * Rebase `feat/ux-232-resident-wcag` onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`).
  * Preserve `const target = String(destination || "").split("?")[0];` in `app.js` `isRoleScreensDestination` across `#/screens` and all 9 `#/role/*` aliases (`building_safety_lead`, `repairs`, `housing_officer`, `contact_centre`, `resident_engagement`, `procurement`, `contractor`, `programme_manager`, `retrofit_coordinator`).
  * Preserve all 9 `#/role/*` entries in `role-screens.js` `ROLE_HASH_SCREENS`, all `#230` programme hunks (`programme-shared-queue`, `programme-funnel` ["Lifecycle and funnel"], `programmeCell`, `programmeQueue`, `programmeFunnel`, `programmeStepCell`, `programmeJumpNav`), and all `#232` resident/host hunks (`screenTable` `aria-live`, `roleScreensView` `announce()`, `#screen-queue`, `section#screen-evidence`, `data-state-cue="scope"`, inline two-line `document.getElementById` jump listener).
  * Record Cycle 1 (`housing-resident-wcag-232-c1-*`) RPI artifacts plus a concise rebase addendum in `housing-resident-wcag-232-changes.md`, configure local privacy-safe Git email from `gh api user`, commit with Conventional Commit + `Refs #232` + Copilot trailer, and do NOT run `git push`.
* **Open blockers**: None.

## Further Research and Follow-Up Candidates

1. Align `NO_REGION_GAPS` for `resident-service-issues` (`Routes to ask` region from `#86`) in `src/api/checks/specialist_keyboard_browser_check.py` in a dedicated full-tier gate-tool PR (`#1294`).
2. Complete human assistive-technology (`NVDA`/`JAWS`/`VoiceOver`) and `360px` mobile walkthroughs across `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` before closing Issue #232 (`#151`, `#155`).

## Research Disposition and Planning Readiness

* Research execution status: Complete (1 full Wider -> Deeper -> Contrarian cycle executed under `focused` posture; all Q1–Q5 claims verified directly against `6510b6fbc` and `cffec920a`).
* Research disposition: `executed`
* Output mode supports planning: Yes (`convergence`)
* Planning Readiness: `Ready`

## Artifact Self-Check

* [x] Research Brief, Parameters, Extension Registry, Participation, Scope, Direction Controls, Questions, and Prior Knowledge Gate recorded.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order.
* [x] Every codebase claim cites a `C#` reference and external rule check cites `W1` with URL and retrieval date.
* [x] Alternatives A, B, and C recorded with evidence-based selection of Option B.
* [x] Zero repository source/test files modified during Research.
* [x] Research disposition (`executed`) and Planning Readiness (`Ready`) explicitly recorded.

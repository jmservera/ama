<!-- markdownlint-disable-file -->

# Task Research: programme-coordinator-wcag-230

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                 |
| Researcher / agent | RPI Agent (`rpi-research`)                                                 |
| Status             | Complete                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/programme-coordinator-wcag-230-research.md |
| Research disposition | executed                                                                 |
| Planning Readiness | Ready                                                                      |

## Research Brief

* What to research: Current WCAG 2.2 baseline (#151) textual state meaning, non-colour status signals, `aria-label`/`aria-describedby` associations, table row headers (`screenRecordTable`), hash route aliases, and keyboard jump/focus navigation across the programme manager, planner, and retrofit coordinator screens (`programme_manager`, `retrofit_coordinator`) in `src/api/src/zava_forward/api/web/` (plus any `static/` alias check) and `src/api/tests/`, comparing against `#231` (`a1d0be5f6`) and `#228` (`538462eba`) on `feat/demo-233-same-home-tensions-0825` as well as earlier `#230` slice `efe14ef3d`.
* Why it matters: Issue `#230` (`Programme manager and coordinator screens`) has one remaining unchecked engineering criterion (`Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation`). Earlier commit `efe14ef3d` landed before `#228` and `#231` established stronger cross-screen WCAG patterns (`screenRecordTable` `<th scope="row">`, `#/role/*` route aliases, `Object.hasOwn`-safe textual state helpers, `status-line ok` banners, standalone focus-visible rules, and comprehensive focused conformance tests), and we must verify both `programme_manager` and `retrofit_coordinator` surfaces across `role-screens.js`, `app.js`, `ops.js`, `panels.js`, `index.html`, and `style.css` without breaking counted accessibility/content-standard/manifest guards.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` in this automatic RPI loop, plus PR reviewers checking `#230` against parent branch `feat/demo-233-same-home-tensions-0825`.
* Scope: `src/api/src/zava_forward/api/web/` (and verification of `src/api/src/zava_forward/api/static/`), `src/api/tests/`, `src/api/checks/`, `src/core/tests/test_scenario_manifest.py`, `src/core/tests/test_needs_inventory.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, `docs/reference/research/ux/customer-journeys/programme.md`.
* Non-goals: Claiming human assistive-technology or screen-reader acceptance (#155/#151 manual checks remain human-owned so commit uses `Refs #230`, not `Closes #230`), running `tools/rpi-checks.py`, pushing to remote, or performing visual redesigns outside Fluent 2 tokens and WCAG 2.2 baseline semantics.
* Criteria: Every `programme_manager` and `retrofit_coordinator` surface has explicit non-colour textual state meaning, semantic headings/tables/live regions/labels, and keyboard jump/focus navigation matching `#231` and `#228`; all counted guards in `test_accessibility_baseline.py`, `test_content_standard.py`, `test_scenario_manifest.py`, and `test_needs_inventory.py` remain green; focused test module `src/api/tests/test_programme_coordinator_wcag_230.py` exercises textual state meaning, non-colour status cues, and keyboard navigation.
* Requested outputs: Converged implementation recommendation for `rpi-plan` with exact `path:line` evidence and guard impact inventory.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                      |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q6 covering `#231`/`#228` patterns, `programme_manager` and `retrofit_coordinator` gaps after `efe14ef3d`, counted guards, and recipe SHA impact |
| Codebase scope                   | `src/api/src/zava_forward/api/`, `src/api/tests/`, `src/api/checks/`, `src/core/tests/`, `docs/reference/research/ux/`                     |
| External scope                   | Vercel Web Interface Guidelines (`command.md`) as required by repository Web Development Guidance                                          |
| Initial internal candidate areas | `src/api/src/zava_forward/api/web/role-screens.js`, `app.js`, `index.html`, `style.css`, `ops.js`, `panels.js`, `src/api/tests/test_programme_screen_wcag.py`, `test_technical_quality_screens_wcag.py`, `test_procurement_contractor_screen_wcag.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `src/core/tests/test_scenario_manifest.py` |
| Initial external candidate areas | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                                    |
| Research posture                 | balanced                                                                                                                                   |
| Posture provenance               | default (bounded internal task with adjacent cross-screen/guard interactions across `app.js`, `role-screens.js`, and `src/core` manifests) |
| Explicit limits / deadline       | Focused validation tier only; do NOT run `tools/rpi-checks.py`; do NOT `git push`                                                          |
| Posture-specific completion basis | balanced scope coverage and adequate evidence across all `programme_manager`/`retrofit_coordinator` views and counted test/manifest guards  |
| Edits allowed during research?   | no, research-only                                                                                                                          |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                       |
| Known constraints / excluded sources | Preserve Fluent 2 tokens, plain-language glossary (banned words in core flow), counted `aria-invalid`/table/fixed-position guards, and scenario recipe SHA |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and evidence paths | Enforces Fluent 2, WCAG 2.2 baseline (#151), content standard (#153), focused validation tier, `Refs #230` honesty | Selected: mandatory repository contract |
| Skill               | `rpi-research`                   | Active phase skill for Research                   | Three-wave research artifact and readiness contract | Selected: active RPI phase |
| Skill               | `web-design-guidelines`          | Repository Web Development Guidance mandatory skill | Fetched `command.md` rules for web edits and `file:line` review | Selected: loaded and fetched at intake |
| Skill               | `accessibility`                  | Domain match on WCAG 2.2 AA and ARIA APG          | WCAG 2.2 success criteria mapping (1.3.1, 1.4.1, 2.1.1, 2.4.1, 2.4.3, 2.4.6, 2.4.7, 4.1.2, 4.1.3) | Selected: loaded for WCAG criterion verification |
| Skill               | `redesign-existing-projects`     | Repository Web Development Guidance existing-app skill | Scan-diagnose-fix discipline subordinated to Fluent 2 and WCAG baseline | Selected: loaded per repo web guidance; visual overhaul rules subordinated to Fluent 2 constraint |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered specialist for independent lanes  | Delegated subagent lane markdown             | Skipped: tightly coupled single-app JS/Python guard trace is faster and higher-precision inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller scope, branch, parent tip, test path, validation command, and commit rules | N/A (non-interactive) | Proceed autonomously in confirmed automatic RPI mode with `balanced` posture and `convergence` output mode |
| Direction change | Verified counted static/DOM/browser guards (`test_accessibility_baseline.py`, `test_content_standard.py`, `test_map_fullscreen.py`, `role_screens_browser_check.py`, `specialist_keyboard_browser_check.py`) | None | Scoped enhancements to preserve all exact counted sites (`9` `aria-invalid`, `14` `h("table", {},`, `2` `position:fixed`), exact `Evidence for {case}` region label, and `\nasync function coordinatorView()` boundary |
| Convergence      | Cycle 1 evidence answered Q1-Q6 with zero unresolved blockers | None | Selected unified WCAG 2.2 enhancement across `role-screens.js`, `app.js`, `style.css`, `test_programme_screen_wcag.py`, and `test_programme_coordinator_wcag_230.py`; `Planning Readiness: Ready` |

## Scope and Success Criteria

* Scope: All UI surfaces and routes serving `programme_manager` (including planner/funnel/shared queue/connected same-home view and `#/role/programme` / `programme-queue`) and `retrofit_coordinator` (coordinator workbench queue, overview/funnel, case view, handoff/coordination panels, and specialist screen links/routes), plus `src/api/tests/test_programme_coordinator_wcag_230.py` and existing WCAG/content/manifest regression suites.
* Assumptions:
  * Prompt references `src/api/src/zava_forward/api/static/`, which in the migrated `src/api` layout may correspond to `src/api/src/zava_forward/api/web/` (to verify via `glob`).
  * Earlier commit `efe14ef3d` partially addressed `programme-queue` in `role-screens.js`, leaving gaps relative to `#228` and `#231` (such as `screenRecordTable` `<th scope="row">`, route aliases, coordinator/programme workbench views, or `aria-label`/`aria-describedby` wiring) that must be verified directly from current `HEAD` (`a1d0be5f6`).
* Success criteria:
  * Every research question is answered with exact `path:line` codebase evidence.
  * Evidence is grounded in actual code, docs, and test execution.
  * Findings, decisions, and readiness claims cite Evidence Log IDs (`C#`, `W#`).
  * Alternatives are compared with trade-offs and one convergence recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Inspect `programme_manager`, planner, and `retrofit_coordinator` screens and tests, specifically how `#231` and `#228` proved WCAG 2.2 baseline textual state meaning, non-colour badges, `aria-label`/`aria-describedby` associations, and keyboard navigation on `feat/demo-233-same-home-tensions-0825`.
  2. Identify needed WCAG 2.2 baseline textual state meaning and keyboard navigation improvements on the programme manager and coordinator screens plus requirements for `src/api/tests/test_programme_coordinator_wcag_230.py`.
  3. Check counted accessibility/content-standard guards (`test_accessibility_baseline.py`, `test_content_standard.py`) and `scenario-manifest.json` recipe SHA checks (`test_scenario_manifest.py`, `test_needs_inventory.py`).
* Inferred research questions:
  * How does `efe14ef3d` (`test_programme_screen_wcag.py` and `programme-queue`) compare with the later `#228` (`538462eba`) and `#231` (`a1d0be5f6`) standards?
  * Which screens/routes belong to `programme_manager` vs `retrofit_coordinator` across `role-screens.js`, `app.js`, `panels.js`, `ops.js`, and `index.html`?
  * Which files are hashed by `scenario-manifest.json` or guarded by exact counts in `test_accessibility_baseline.py`, `test_content_standard.py`, `role_screens_browser_check.py`, `specialist_keyboard_browser_check.py`, and `atlas_tensions_browser_check.py`?
* Caller constraints and non-goals: Focused validation tier only; do not run `tools/rpi-checks.py`; do not `git push`; commit with `Refs #230`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Focused validation tier; exclude `tools/rpi-checks.py` and `git push` | Caller prompt / Intake | Keep validation scoped to targeted unit/accessibility/content/core manifest suites, ruff, mypy, and local checks |
| add                                                      | Deliver `src/api/tests/test_programme_coordinator_wcag_230.py` alongside screen WCAG improvements | Caller prompt / Intake | Must design new dedicated test module without breaking existing `test_programme_screen_wcag.py` |
| add                                                      | Preserve counted guards and `scenario-manifest.json` recipe SHA integrity | Caller prompt / Intake | Wave 2 and Wave 3 must verify every static count and SHA recipe input |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status   |
|---:|------------------|------------------------------------------|-----------|----------|
| Q1 | Where do web static assets live (`web/` vs `static/`), and which screens, routes, and role profiles implement `programme_manager`, planner, and `retrofit_coordinator` journeys? | breadth | H | answered |
| Q2 | What exact WCAG 2.2 patterns did `#231` (`a1d0be5f6`) and `#228` (`538462eba`) establish for jump navigation, focus delegation, row headers (`screenRecordTable`), non-colour status badges/lines, `aria-label`/`aria-describedby` associations, and `#/role/*` routing? | depth | H | answered |
| Q3 | What did earlier `#230` commit `efe14ef3d` already add to `programme-queue`, and what WCAG 2.2 textual state meaning, `aria-label`/`aria-describedby`, table row-header, route-alias, or keyboard-navigation gaps remain across `programme_manager` and `retrofit_coordinator` screens? | depth | H | answered |
| Q4 | What exact counted guards exist in `test_accessibility_baseline.py`, `test_content_standard.py`, and browser check harnesses (`role_screens_browser_check.py`, `specialist_keyboard_browser_check.py`, `atlas_tensions_browser_check.py`)? | depth | H | answered |
| Q5 | Does modifying `index.html`, `app.js`, `role-screens.js`, or `style.css` affect `scenario-manifest.json` recipe SHA in `src/core/tests/test_scenario_manifest.py` and `src/core/tests/test_needs_inventory.py`? | straightforward | H | answered |
| Q6 | What test cases and harness pattern (e.g., Node VM / DOM / static contract without `sys.modules` pollution) should `src/api/tests/test_programme_coordinator_wcag_230.py` use so all suites run cleanly together? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed:
  * `.copilot-tracking/rpi-sessions/2026-11-15/issue-230-programme-mgr-wcag-state.json`
  * `.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json`
  * `docs/reference/research/ux/wcag-conformance-baseline.md`
  * `docs/reference/research/ux/design-system.md`
  * `docs/reference/research/ux/content-standard.md`
* Reused (verified) findings:
  * Commit `efe14ef3d` already added `programmeJumpNav` and `screenJumpTarget` to `programme-queue` in `role-screens.js` and updated `test_programme_screen_wcag.py`, while later commits `538462eba` (#228) and `a1d0be5f6` (#231) introduced `screenRecordTable` (`<th scope="row">`), `#/role/*` hash aliases in `app.js`, standalone `[tabindex="-1"]` focus-visible rules in `style.css`, `Object.hasOwn`-safe state maps, and `status-line ok` banners.
  * `wcag-conformance-baseline.md` confirms counted static inventories: 9 `aria-invalid` sites and 14 regex-counted workbench tables, and manual AT/human checks remain `Not run` (#151, #155).
* Superseded / stale:
  * Pre-`538462eba`/`a1d0be5f6` assumptions in `issue-230-programme-mgr-wcag-research.md` predated `#/role/*` route aliases, `screenRecordTable` row-header standardization across specialist screens, and `#135` exception-queue counted-inventory bumps; all line numbers and screen states must be re-verified on `a1d0be5f6`.

## Cycle 1 Execution

### Wave 1: Wider (Surface Discovery and Role Route Mapping)

* Executed inline across `src/api/src/zava_forward/api/`, `src/api/tests/`, `src/api/checks/`, `src/core/tests/`, and `docs/reference/research/ux/` (fallback rationale: tightly coupled JS/Python contract trace in one package).
* Web asset root (`Q1`): Shipped static assets live in `src/api/src/zava_forward/api/web/` (`app.js`, `role-screens.js`, `ops.js`, `panels.js`, `style.css`, `index.html`); no `static/` directory exists (`C1`).
* Programme manager, planner, and coordinator surfaces (`Q1`):
  * Specialist screen `programme-queue` (`Programme queue and connected home view`) in `role-screens.js:682-727` serves `Retrofit Programme Manager`, `Programme Support Officer` (`screenManagers`), and `Retrofit Coordinator` (`C2`).
  * Coordinator workbench route `#/coordinator` (`coordinatorView()` in `app.js:2705-2829`) renders the coordinator population filter form, denominator/coverage summary, count definitions disclosure, current-case heatmap, lifecycle funnel, record-selection status card, map panel, and selected-records table (`C3`).
  * Adjacent programme/coordinator workbench views `#/handoff-waiting` (`handoffWaitingView()` in `app.js:882-925`) and `#/capacity` (`capacityView()` in `ops.js:373-525`) already include scoped captions, `<th scope="col">` / `<th scope="row">` headers, live regions, and `aria-describedby` wiring (`C4`, `C5`).
  * Role hash aliases `ROLE_HASH_SCREENS` (`role-screens.js:92-99`) and `isRoleScreensDestination` (`app.js:370-378`) map six `#/role/*` routes (`building_safety_lead`, `repairs`, `housing_officer`, `resident_engagement`, `procurement`, `contractor`) into `roleScreensView()`, omitting `#/role/programme_manager` and `#/role/retrofit_coordinator` (`C6`, `C7`).

### Wave 2: Deeper (Gap Audit Against `#228`, `#231`, WCAG 2.2 Baseline, and Web Guidelines)

* Sibling WCAG patterns from `#228` (`538462eba`) and `#231` (`a1d0be5f6`) (`Q2`, `W1`):
  * `screenRecordTable` / `screenTable(..., rowHeader = true)` (`role-screens.js:48-55`, `76`) emits `<th scope="row">` on the record-identifying first column without adding a new `h("table", {}, ...)` call literal (`C8`).
  * Delegated `a[data-jump]` click listeners in both `role-screens.js:306-315` and `app.js:2390-2400` prevent hash routing (`preventDefault()`) and move focus + `scrollIntoView({ block: "start" })` to `tabindex="-1"` section/heading targets styled by `[tabindex="-1"]:focus` and `h2[tabindex="-1"]:focus-visible` in `style.css:374-375` (`C9`, `C10`).
  * Non-colour status cues combine explicit plain-text prefixes (`State: ...`, `Action needed: ...`, `Warning: ...`) with Fluent 2 `.flag`, `.flag.danger`, and `.status-line.wait` CSS glyphs/borders (`style.css:324-327`) plus `data-state-cue` attributes (`C10`, `C11`).
* Concrete `#230` gaps remaining after `efe14ef3d` (`Q3`):
  1. Missing `#/role/programme_manager` and `#/role/retrofit_coordinator` hash route aliases in `ROLE_HASH_SCREENS` (`role-screens.js:92-99`) and `isRoleScreensDestination` (`app.js:370-378`) (`C6`, `C7`).
  2. Missing `<th scope="row">` row headers across all three `programme-queue` data tables in `role-screens.js`: `Shared queue: returned and handed-off work` (`line 463`, needs `rowHeader = true` as 6th arg to `screenTable` so custom `programmeCell` still formats columns), `Lifecycle and funnel by stage` (`line 516`, `screenRecordTable`), and `Same-home step states` (`line 721`, `screenTable` with `rowHeader = true` + badge cell formatter) (`C2`, `C8`).
  3. Missing `aria-describedby="programme-page-status programme-filter-status"` on `#programme-scope` `<select>` (`role-screens.js:457`), missing `data-jump-target` attribute parity on `programmeJumpNav` links (`role-screens.js:669`), and missing Fluent 2 `.flag` / `.flag.danger` / `.status-line.wait` + `data-state-cue` non-colour visual/DOM cues on queue return/handoff cells (`line 444`), funnel state banners (`lines 514-515`), unblocked connected-home warning banner (`line 715`), and `Same-home step states` `State` cells (`line 721`) (`C2`).
  4. On `#/coordinator` (`coordinatorView()` in `app.js:2705-2829`):
     * Zero keyboard section-jump navigation across its six primary sections (`Choose the current case population`, `Denominator and coverage`, `Heatmap of current cases`, `Lifecycle funnel: current and observed cases`, `Record selection`, `Selected records`), and section `<h2>` headings lack `id`, `tabindex="-1"`, and parent `aria-labelledby` wiring (`C3`).
     * Filter form lacks `id="co-filter-error"` + `aria-describedby` association on required selects (`co-view`, `co-group_by`) and lacks `id="co-cutoff-note"` + `aria-describedby` association on temporal cutoff inputs (`co-as_of`, `co-start`) (`C3`).
     * Heatmap `.heat-present` cells (`app.js:2792`) highlight non-zero case counts via background tint (`style.css:99`) without a `data-state-cue` attribute or explicit `(present)` / `(none recorded)` screen-reader state cue on the count link, and `Selected records` `Can move on` cells (`app.js:2808`) render bare strings (`"Cannot move on"` / `"No current stop recorded"`) without non-colour `.flag.danger` / `.flag` status badges, `data-state-cue`, or explicit `Action needed:` / `State:` prefixes (`C3`, `C10`).

### Wave 3: Contrarian (Counted Guards, String Split Boundaries, and Existing Test Invariants)

* Checked every potential regression vector against existing static, Node VM, and Playwright harnesses (`Q4`, `Q5`, `Q6`):
  1. Counted `aria-invalid` guard (`test_accessibility_baseline.py:85-98` and `test_epic149_form_error_summary_associations.py:18-105`): pins `sites == 9` for `setAttribute("aria-invalid", "true")`. Contrarian finding: adding `aria-describedby="co-filter-error"` to `co-view` and `co-group_by` in `coordinatorView()` WITHOUT adding a 10th `setAttribute("aria-invalid", "true")` call improves error announcement while keeping both counted-site tests green (`C12`, `C13`).
  2. Counted `h("table", {},` guard (`test_accessibility_baseline.py:139-155`): pins `tables == 14` and forbids unscoped `h("th", {}`. Contrarian finding: using `screenRecordTable` and `screenTable(..., true)` in `role-screens.js` and enhancing the existing `table` helper in `coordinatorView()` adds zero `h("table", {},` sites (`C12`).
  3. Plain-language banned-word guard (`test_content_standard.py:14-60`): scans all `web/*.js` and `web/*.html` with case-insensitive `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b`. Contrarian finding: no new comment, identifier, `id`, `data-state-cue`, or string in `app.js` or `role-screens.js` may contain standalone word-bounded `gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, or `envelope(s)` (`C14`).
  4. Source-split guard in `test_map_fullscreen.py:9-11`: splits `app.js` on literal `"\nasync function coordinatorView()"`. Contrarian finding: all new coordinator helpers must live inside `coordinatorView()` so the boundary immediately after `mapPanel` stays byte-identical (`C15`).
  5. Browser region-name & text guards in `role_screens_browser_check.py:646-663` and `specialist_keyboard_browser_check.py:47`:
     * `role_screens_browser_check.py:646` locates `get_by_role("region", name="Evidence for ZF-1", exact=True)` and asserts `\bready\b` does not appear in `region.inner_text()`, while `rows.nth(index).locator("th, td")` already accepts `<th scope="row">` (`C16`). Therefore `roleScreensView()` must preserve `aria-label: "Evidence for ${c.id}"` on `.screen-evidence` for `programme-queue` and never introduce the word `"ready"`.
     * `specialist_keyboard_browser_check.py:47` pins `EXPECTED_REGIONS["programme-queue"] = ("Same-home step states",)`. Keep that exact table label (`C17`).
  6. Existing `test_programme_screen_wcag.py` assertions (`lines 221-376`):
     * Pins exact `nav["attrs"]` (`{"aria-label": ..., "class": "screen-links"}`), exact 4 overview jump IDs + 4 connected-home jump IDs (`len(jump_labels) == 8`), exact `text(td)` values (`"Blocked: evidence missing"`, `"State: Returned. Missing survey"`, etc.), and at line `373` previously checked `all(h["attrs"].get("scope") == "col" for h in headers)` because row headers were absent in `efe14ef3d`. Wrapping cell text in `h("span", { class: ..., "data-state-cue": ... }, value)` preserves `text(td)` in both `test_programme_screen.py` and `test_programme_screen_wcag.py`, and updating `test_programme_screen_wcag.py:373` to verify `<th scope="col">` in `thead` and `<th scope="row">` in `tbody` aligns it with `screenRecordTable` (`C18`).
  7. Scenario manifest SHA guard (`test_scenario_manifest.py` and `test_needs_inventory.py`) (`Q5`): `scenario-manifest.json` hashes only `src/api/checks/workbench-manifest.json`, `src/api/checks/workbench_browser_check.py`, `src/core/tests/dataset.py`, and `src/api/tests/test_workbench.py`; editing `web/*.js`, `web/*.css`, and `src/api/tests/test_programme*.py` has zero SHA impact (`C19`).

## Parent Cycle Synthesis and Convergence

* Cycle 1 covered all `programme_manager` and `retrofit_coordinator` surfaces and contrarian test guards with zero open uncertainties; no Cycle 2 is needed under the `balanced` posture.
* Alternatives evaluated:
  1. Minimal route-alias + test-only patch (leave `programme-queue` without `<th scope="row">` and leave `#/coordinator` without jump links or non-colour cues): Rejected because `#/coordinator` is the primary coordinator flow view (`app.js:2705`) and lacks keyboard section-jump links, required-field error `aria-describedby`, and non-colour cues on `.heat-present` and `Can move on` cells (`C3`), while `programme-queue` tables lack `<th scope="row">` row headers established in `#228`/`#231` (`C2`, `C8`).
  2. Full `isResidentRoleScreen`-style wrapper rewrite on `programme-queue`: Rejected by Wave 3 contrarian evidence because changing `.screen-evidence` from `aria-label="Evidence for ${c.id}"` to `aria-labelledby="screen-evidence-heading"` would break `role_screens_browser_check.py:646`, and adding a second `<nav>` inside `overview()`/`render()` would break `len(navs) == 1` in `test_programme_screen_wcag.py:243` (`C16`, `C18`).
  3. Selected Convergence Recommendation:
     * Wire `#/role/programme_manager` and `#/role/retrofit_coordinator` -> `"programme-queue"` in `ROLE_HASH_SCREENS` (`role-screens.js`) and `isRoleScreensDestination` (`app.js`), preserving `Evidence for ${c.id}` region naming.
     * Upgrade all three `programme-queue` tables in `role-screens.js` to emit `<th scope="row">` first-column headers (`rowHeader = true` / `screenRecordTable`), wire `aria-describedby="programme-page-status programme-filter-status"` on `#programme-scope`, add `data-jump-target` on `programmeJumpNav` links, and add Fluent 2 `.flag` / `.flag.danger` / `.status-line.wait` + `data-state-cue` non-colour cues on queue return/handoff cells, funnel state banners, unblocked warning banner, and `Same-home step states` state cells while keeping exact rendered text strings and updating `test_programme_screen_wcag.py` row-header assertion (`C2`, `C18`).
     * Upgrade `coordinatorView()` (`#/coordinator` in `app.js` + `.coordinator h2[tabindex="-1"]:focus-visible` in `style.css`) with a keyboard section-jump `<nav class="screen-links">` (`a[data-jump]`), programmatic-focus `<h2 id="..." tabindex="-1">` headings with section `aria-labelledby`, `aria-describedby` associations on `co-view`/`co-group_by` (`co-filter-error`) and `co-as_of`/`co-start` (`co-cutoff-note`) without touching counted `aria-invalid` sites, and non-colour textual state cues + `.flag` / `.flag.danger` badges + `data-state-cue` on heatmap `.heat-present` cells and `Selected records` `Can move on` cells (`C3`, `C10`, `C12`, `C15`).
     * Deliver comprehensive Node VM + DOM/route conformance suite `src/api/tests/test_programme_coordinator_wcag_230.py` verifying `#/role/programme_manager` and `#/role/retrofit_coordinator` routing/RBAC/script-loader contracts, `programme-queue` row headers/non-colour cues/`aria-describedby`/jump focus/pager focus handoff, and `#/coordinator` section-jump focus, `aria-describedby` associations, heatmap & `Selected records` non-colour state cues, and plain-language safety (`Q6`).

## Evidence Log

| ID  | Source (`path:line` or URL + retrieval date) | Evidence summary |
|-----|----------------------------------------------|------------------|
| C1  | `src/api/src/zava_forward/api/web/index.html:1-45` | Shipped web assets reside under `src/api/src/zava_forward/api/web/` (`index.html`, `app.js`, `role-screens.js`, `ops.js`, `panels.js`, `style.css`). |
| C2  | `src/api/src/zava_forward/api/web/role-screens.js:396-727` | `programme-queue` serves `Retrofit Programme Manager`, `Programme Support Officer`, and `Retrofit Coordinator`; currently omits `rowHeader = true` on its 3 tables, `aria-describedby` on `#programme-scope`, `data-jump-target` on `programmeJumpNav` links, and `.flag`/`.status-line`/`data-state-cue` wrappers. |
| C3  | `src/api/src/zava_forward/api/web/app.js:2705-2829` | `coordinatorView()` (`#/coordinator`) lacks section jump navigation, focusable `h2[tabindex="-1"]` section targets, `aria-describedby` on filter error and cutoff hints, and non-colour cues on `.heat-present` and `Can move on` cells. |
| C4  | `src/api/src/zava_forward/api/web/app.js:882-925` | `handoffWaitingView()` (`#/handoff-waiting`) already provides `<th scope="col">`, `<th scope="row">`, caption, live status/alert regions, and explicit `"Escalated: unaccepted handoff"` / `"Action needed"` state text. |
| C5  | `src/api/src/zava_forward/api/web/ops.js:373-525` | `capacityView()` (`#/capacity`) already wires `aria-describedby="capacity-version-error"`, live status region, scoped table headers, and accessible control names. |
| C6  | `src/api/src/zava_forward/api/web/role-screens.js:92-108` | `ROLE_HASH_SCREENS` maps six `#/role/*` routes to specialist screen IDs and omits `#/role/programme_manager` and `#/role/retrofit_coordinator`. |
| C7  | `src/api/src/zava_forward/api/web/app.js:370-455` | `isRoleScreensDestination(destination)` gates lazy `/role-screens.js` loading, `#/screens` active nav highlighting, and `roleScreensView()` dispatch. |
| C8  | `src/api/src/zava_forward/api/web/role-screens.js:48-77` | `screenTable` supports `rowHeader = false` (6th arg) and `screenRecordTable` wraps it with `rowHeader = true` to emit `<th scope="row">` on column 0 without adding a table literal. |
| C9  | `src/api/src/zava_forward/api/web/app.js:2390-2400` | Global `document.addEventListener("click", ...)` handles `a[data-jump]` across all workbench routes (including `#/coordinator`), preventing route change and focusing + scrolling the target ID. |
| C10 | `src/api/src/zava_forward/api/web/style.css:98-100,324-327,374-375` | Defines `.coordinator .heat-present` tint, `.flag.danger` / `.status-line.wait` non-colour CSS glyphs, and `[tabindex="-1"]:focus` + `.screen-record h2[tabindex="-1"]:focus-visible` two-tone focus rings. |
| C11 | `src/api/src/zava_forward/api/web/role-screens.js:1735-1790` | `#228` (`procurement-packages` / `contractor-job-pack`) pairs plain-language state prefixes with `.flag` / `.status-line.wait` and `data-state-cue`. |
| C12 | `src/api/tests/test_accessibility_baseline.py:85-155` | Enforces exact counted baselines: `9` `setAttribute("aria-invalid", "true")` sites, `2` `position:fixed` rules, `14` `h("table", {},` sites, and zero unscoped `h("th", {}`. |
| C13 | `src/api/tests/test_epic149_form_error_summary_associations.py:18-105` | Maps the exact 9 counted `aria-invalid` sites one-for-one. |
| C14 | `src/api/tests/test_content_standard.py:14-60` | Rejects word-bounded `gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, and `envelope(s)` anywhere in `web/*.js` and `web/*.html` outside `ALLOWED`. |
| C15 | `src/api/tests/test_map_fullscreen.py:9-11,100` | Splits `app.js` on literal `"\nasync function coordinatorView()"` and requires `#coordinator-records` on `.table-scroll` of `Selected records`. |
| C16 | `src/api/checks/role_screens_browser_check.py:645-663` | Requires `get_by_role("region", name="Evidence for ZF-1", exact=True)` and absence of `\bready\b` in `programme-queue` connected-home region text. |
| C17 | `src/api/checks/specialist_keyboard_browser_check.py:47` | Pins `EXPECTED_REGIONS["programme-queue"] = ("Same-home step states",)`. |
| C18 | `src/api/tests/test_programme_screen_wcag.py:221-376` | Asserts `programmeJumpNav` `attrs`, 8 jump targets, exact `text(td)` state strings, and `th` `scope` attributes across the 3 `programme-queue` tables. |
| C19 | `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:1-90` | Hashes only `workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, and `test_workbench.py`; web/test edits for `#230` preserve recipe SHA. |
| W1  | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (retrieved 2026-11-15) | Enforces visible `:focus-visible` rings, semantic links/buttons/headings/tables, `scroll-margin-top` on anchors, `aria-live="polite"` status regions, and non-colour status signals. |

## Open Questions, Risks, and Further Research

* Residual boundary (non-blocking for engineering slice): Manual screen-reader, keyboard assistive-technology, and user-validation checks remain tracked under `#151` and `#155`, so the commit and future PR must cite `Refs #230` rather than claiming full closure of `#230`.
* Deferred follow-ups:
  1. Run live Playwright browser checks (`role_screens_browser_check.py`, `specialist_keyboard_browser_check.py`, `atlas_tensions_browser_check.py`) against a seeded local server when full browser/AT sign-off is executed for `#151`/`#155`.

## Readiness and Self-Check

* Research disposition: `executed`
* Planning Readiness: `Ready`
* Self-check:
  * [x] Wider, Deeper, and Contrarian waves completed in order.
  * [x] Every research question Q1-Q6 answered with `C#` and `W#` citations.
  * [x] Read-only research constraint respected (zero production source files modified).
  * [x] Ready for parent `RPI Agent` transition to `Plan`.


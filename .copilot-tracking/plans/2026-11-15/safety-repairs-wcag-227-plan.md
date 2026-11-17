<!-- markdownlint-disable-file -->
# RPI Plan: Issue #227 Building Safety Lead and Repairs Hazard Screens WCAG 2.2

## Task Metadata

* Task ID: 2026-11-15-safety-repairs-wcag-227
* Task slug: safety-repairs-wcag-227
* Planning status: Ready for implementation
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/safety-repairs-wcag-227-plan-critique.md

## Executive Summary

This plan completes the remaining engineering accessibility work for GitHub issue #227 on the Building Safety Lead (`safety-lead`, `#/role/building_safety_lead`) and Repairs / Hazard Triage (`hazard-triage`, `#/role/repairs`) specialist screens. Both screens display life-safety hazard referrals, separate `sent`/`received`/`accepted` handoff timestamps, pending-receipt follow-up ownership, response clocks, and scoped retrofit stop-work and release evidence. Making every section reachable by keyboard jump navigation, every state explicit in plain words first, and every link and status flag distinguishable without relying on colour prevents safety escalation or stop-work states from being missed by keyboard, low-vision, forced-colours, or screen-reader users.

### User Decisions and Requirements Highlights

* Execute the full RPI loop in order (`rpi-research` -> `rpi-plan` -> `rpi-plan-critique` -> `rpi-implement` -> `rpi-review`) on branch `feat/ux-227-safety-repairs-wcag-0006` targeting `feat/demo-233-same-home-tensions-0825`, writing all dated 2026-11-15 artifacts under `.copilot-tracking/`.
* Deliver WCAG 2.2 baseline (#151) keyboard jump navigation, textual state labels, and non-colour status signals on `#/role/building_safety_lead` (`safety-lead`) and `#/role/repairs` (`hazard-triage`) while preserving all five previously checked #227 acceptance criteria (read-only boundary, separate `sent`/`received`/`accepted` referral states, pending-receipt follow-up owner, scoped pause/release evidence, Fluent 2 components, and no role simulator).
* Run the Focused validation tier (`mypy`, `ruff check .`, `ruff format --check .`, and targeted unit tests in `src/api` including `tests/test_role_screens.py` and `tests/test_accessibility_baseline.py`), then commit all code, tests, and `.copilot-tracking/` artifacts cleanly with the Copilot `Co-authored-by` trailer without pushing.

### What You May Not Know

* Earlier commit `a1bfc1748` left `hazardJump` as the **only remaining `<a href="#" onclick=...>` inline handler** in `src/api/src/zava_forward/api/web/role-screens.js`; migrating it to real `#hazard-...-heading` fragments and `data-jump` click delegation lets us remove the last `href: "#"` inline-onclick carve-out in `src/api/tests/test_role_screens_conformance.py`.
* Global `nav a` styling in `src/api/src/zava_forward/api/web/style.css` currently strips underlines from `<nav class="screen-links">` links and leaves them below the WCAG 2.2 2.5.8 24x24 CSS px target height at rest; fixing `.screen-links a` benefits both safety jump links and specialist screen navigation links without introducing motion on `.screen-*` selectors.
* `CopyAudit` (`src/api/tests/test_content_standard.py`) bans `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` across every line of served JS/HTML except exact allowlisted expressions (`h.hold`, `x.hold`), and `SafetyScreens` (`src/api/tests/test_safety_screens.py`) pins `<td>` column counts equal to `<th scope="col">` headers plus zero `<button>` elements. All state-label additions are designed to preserve 100% of existing substring and structural contracts.
* Automated unit, conformance, and CSS checks prove the engineering WCAG 2.2 baseline, but repository policy (`docs/reference/research/ux/wcag-conformance-baseline.md`) reserves full WCAG conformance and issue closure for human assistive-technology and named safety-role sign-off (#155, #156), so commits reference `Refs #227`.

### Unresolved Decisions or Blockers

* None for engineering implementation. Human assistive-technology and named safety-role validation (#151, #155, #156) remains a tracked post-implementation follow-up item outside automated execution.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`rpi-research` -> `rpi-plan` -> `rpi-plan-critique` -> `rpi-implement` -> `rpi-review`) for GitHub issue #227 ("Building safety lead and repairs hazard screens (`#/role/building_safety_lead`, `#/role/repairs`): WCAG 2.2 keyboard jump nav, text state labels, and non-colour status signals") in worktree `/home/azureuser/source/ama-demo-wt/feat-227-safety-repairs-wcag-0006` on branch `feat/ux-227-safety-repairs-wcag-0006` targeting `feat/demo-233-same-home-tensions-0825` (caller prompt; `/tmp/issue-227.md`).
* Read `/tmp/issue-227.md` first and preserve all five already-checked #227 criteria: separate `sent`/`received`/`accepted` referral timestamps, named follow-up owner for pending receipt/acceptance, scoped retrofit pause and human release evidence, strict read-only human-authority boundary (zero write controls or silent defaults), and Fluent 2 components with no role-switching simulator (`/tmp/issue-227.md`; `C4`, `C13`, `C19`).
* Write all required dated RPI artifacts under `.copilot-tracking/` (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `changes/2026-11-15/`, `reviews/2026-11-15/`, plus canonical `reviews/plans/2026-11-15/` for plan critique and `rpi-sessions/2026-11-15/` for RPI Agent state) (caller prompt).
* Apply AMA Web Development Guidance: preserve Fluent 2 tokens (`#150`), WCAG 2.2 AA engineering baseline (`#151`), and plain British English content standard (`#153`), and verify changed web files against refreshed Web Interface Guidelines (`command.md`) reporting `file:line` findings (`C1`–`C3`, `W1`).
* Validate under the Focused tier (`mypy`, `ruff check .`, `ruff format --check .`, and targeted unit tests in `src/api` including `tests/test_role_screens.py` and `tests/test_accessibility_baseline.py`) (caller prompt).
* Commit all changes and `.copilot-tracking/` artifacts cleanly with privacy-safe repository-local Git email (`gh api user` -> `{id}+{login}@users.noreply.github.com`) and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push (caller prompt; AMA Branch and Pull Request Workflow).

## Goals

* Deliver native, delegated keyboard jump navigation (`<nav aria-label="Sections on this screen" class="screen-links">` with real `#hazard-...-heading` anchors and `data-jump` focus/scroll delegation) across both selected-home (`hazardScreen`) and cross-home summary (`hazardQueue.summary`) views of `safety-lead` and `hazard-triage`.
* Ensure every referral timestamp, escalation state, follow-up ownership status, response clock, safety clock, urgency value, cross-home anomaly row, and scoped stop-work/release indicator leads with explicit plain-language state words (`Confirmed:`, `Waiting:`, `Action needed:`, `Unknown:`, `State:`, `Stop-work indicator:`) backed by `Object.hasOwn`-safe lookups and corrupt-timestamp guards.
* Guarantee non-colour link and status differentiation plus WCAG 2.2 2.5.8 target sizing in `style.css` (`.screen-links a` persistent underline + `1.5rem` min-height; `.flag` and `.flag.danger` borders) without adding transitions or animations to `.screen-*` rules.
* Support direct hash navigation to `#/role/building_safety_lead` (`safety-lead`) and `#/role/repairs` (`hazard-triage`) alongside canonical `#/screens?screen=...` URLs while preserving query parameters (`case`, `page`) and strict `me.user.role` access checks.
* Lock regressions with focused unit and conformance assertions and verify clean Focused-tier validation before creating a single clean post-review local Git commit.

## Scope and Non-Goals

### In Scope

* `src/api/src/zava_forward/api/web/role-screens.js`: `ROLE_HASH_SCREENS` alias resolution in `roleScreensView` (plus deduplicating the unselected `overview` VDOM reference), optional `scrollIntoView` in shared `a[data-jump]` delegation, `hazardJump`/`screenPanel` landmark anchors, cross-home summary jump nav, explicit non-colour state cue guidance copy, and word-first `Object.hasOwn`-safe state helpers across `hazardScreen` and `hazardQueue.summary`.
* `src/api/src/zava_forward/api/web/app.js`: `isRoleScreensDestination` support for `#/role/building_safety_lead` and `#/role/repairs` in `missingWorkspaceScripts` and `route()` without modifying script-retry invariants or introducing global-scope identifier collisions.
* `src/api/src/zava_forward/api/web/style.css`: non-colour underline and `1.5rem` (24px) minimum target height on `.screen-links a`, `scroll-margin-top: var(--sp-4)` on `.screen-record h2` heading anchors, and `1px solid` borders on `.flag` / `.flag.danger`.
* `src/api/tests/test_safety_screen_wcag_keyboard.py`, `src/api/tests/test_role_screens_conformance.py`, and `src/api/checks/safety_screens_browser_check.py`: updated delegated jump-link behavioral test, prototype-key and corrupt-timestamp state tests, cross-home summary jump/state tests, CSS non-colour/target-size assertions, `#/role/...` route alias permission/render tests, removal of the legacy `'h("a", { href: "#",' ` inline-onclick exemption, and `content-visibility: auto`-aware real-browser + pinned axe-core 4.10.3 verification in `safety_screens_browser_check.py`.
* Dated RPI tracking artifacts under `.copilot-tracking/{research,plans,details,changes,reviews,rpi-sessions}/2026-11-15/` and `.copilot-tracking/reviews/plans/2026-11-15/`.

### Non-Goals

* Adding write actions, forms, buttons, role-switching simulators, backend API endpoints, or database schema changes.
* Converting safety tables from `screenTable` (`<td>` body cells) to `screenRecordTable` (`<th scope="row">`), which is refuted by `test_safety_screens.py:131-133` (`C13`).
* Claiming human assistive-technology conformance (#155) or closing #227 before human sign-off (`C1`), or pushing commits to `origin`.

## Functional Requirements

* `FR-01` (Delegated keyboard jump navigation and section landmarks): Both per-home (`hazardScreen`) and cross-home (`hazardQueue.summary`) views of `safety-lead` and `hazard-triage` render `<nav aria-label="Sections on this screen" class="screen-links">` containing native `<a href="#hazard-...-heading" data-jump="hazard-...-heading" data-jump-target="hazard-...-heading">` links paired 1:1 with `screenPanel` `<section id="hazard-..." aria-labelledby="hazard-...-heading">` and `<h2 id="hazard-...-heading" tabindex="-1">` landmarks, delegating click activation to the shared `a[data-jump]` handler (`preventDefault()`, `focus()`, optional `scrollIntoView({ block: "start" })`) with zero inline `onclick` attributes and zero `href="#"` links (`C7`, `C8`, `C9`, `C14`, `W1`).
  * Observable acceptance criteria: `AC-01`, `AC-05`.
* `FR-02` (Permission-preserving `#/role/building_safety_lead` and `#/role/repairs` route aliases): `app.js` loads `/role-screens.js` and dispatches `roleScreensView()` when the route path is `#/screens`, `#/role/building_safety_lead`, or `#/role/repairs`, and `roleScreensView()` resolves `#/role/building_safety_lead` to `safety-lead` and `#/role/repairs` to `hazard-triage` (preserving `?case=` and `?page=` parameters when no explicit `?screen=` overrides it) while strictly enforcing `screen.roles.includes(me.user.role)` and rendering `"Screen unavailable"` for unauthorized roles (`C10`, `C11`, `C19`, `C20`).
  * Observable acceptance criteria: `AC-02`.
* `FR-03` (Word-first, prototype-safe textual state labels and non-colour cue guidance): Every state-bearing cell in `hazardScreen` and `hazardQueue.summary` (`hazardStep`, `hazardSafetyClock`, `hazardFollowUp`, `hazardEscalationState`, `hazardClock`, `hazardHold`, cross-home `pause`, reported observation `urgency:`, and cross-home `Unavailable`/`Unknown`/`Mismatch` rows) leads with explicit plain-language state words (`Confirmed:`, `Waiting:`, `Action needed:`, `Unknown:`, `State:`, `Stop-work indicator:`), guards prototype properties with `Object.hasOwn` and invalid date strings against `"Recorded Unknown"` / `"Service responded Unknown"`, includes prose guidance stating that states are written in words first so colour is never the only signal, and preserves all existing safety-screen substrings and `CopyAudit` rules (`C3`, `C6`, `C13`, `C15`, `C17`, `C18`).
  * Observable acceptance criteria: `AC-03`, `AC-05`.
* `FR-04` (Non-colour link/badge CSS signals and 24px target height): `.screen-links a` in `style.css` retains `text-decoration: underline` at rest with `display: inline-flex; align-items: center; min-height: 1.5rem; padding: var(--sp-1) var(--sp-2)` so links and `aria-current="page"` thicker underlines are distinguishable without colour and meet WCAG 2.2 2.5.8 24px minimum height, while `.flag` and `.flag.danger` carry `1px solid` borders for non-colour and `forced-colors` boundary contrast (`C1`, `C2`, `C12`, `C19`).
  * Observable acceptance criteria: `AC-04`, `AC-05`.

## Non-Functional Requirements

* `NFR-01` (Read-only, plain-language, design-system, and conformance invariants):
  * Objective threshold or evaluation condition: Zero `<button>`, `<form>`, `<input>`, `<select>`, or `<textarea>` tags in `safety-lead` or `hazard-triage`; zero banned `CopyAudit` words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`); zero undocumented CSS classes; zero `animation` or `transition` declarations in `.screen-*` selectors; `h("table", {}, ...)` call count across `WEB/*.js` unchanged at `13`; zero top-level identifier collisions between `app.js` and `role-screens.js`; `checks/script_retry.py` invariants in `app.js` preserved (`C13`–`C20`).
  * Operating condition or verification approach: Verified via `test_safety_screens.py`, `test_safety_screen_wcag_keyboard.py`, `test_role_screens_conformance.py`, `test_role_screens.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_design_system.py`, and `test_workspace_scripts.py`.
  * Observable acceptance criteria: `AC-05`, `AC-06`.
* `NFR-02` (Focused-tier static, runtime, Web Interface Guidelines, and single-commit hygiene):
  * Objective threshold or evaluation condition: `mypy`, `ruff check .`, `ruff format --check .`, `node --check`, and targeted `src/api` unit suites exit `0`; refreshed Web Interface Guidelines (`command.md`) `file:line` review reports zero open violations on modified web files; zero `.copilot-tracking/` references appear in production code, tests, comments, or commit message; one clean local Git commit is created after `rpi-review` writes `.copilot-tracking/reviews/2026-11-15/safety-repairs-wcag-227-review.md`, with privacy-safe repository-local `user.email` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and `git status --short` is clean without pushing.
  * Observable acceptance criteria: `AC-06`, `AC-07`.

## Acceptance Criteria

* `AC-01`: `safety-lead` and `hazard-triage` render `<nav aria-label="Sections on this screen" class="screen-links">` jump links using real `#hazard-...-heading` `href` fragments and `data-jump` delegation (zero `onclick:` on `<a>`, zero `href="#"`) targeting focusable `<h2 id="hazard-...-heading" tabindex="-1">` headings inside `<section id="hazard-..." aria-labelledby="hazard-...-heading">` landmarks on both per-home and cross-home views, and clicking a jump link in Node VM calls `preventDefault()`, focuses the matching heading, calls optional `scrollIntoView({ block: "start" })`, and tolerates missing targets cleanly.
* `AC-02`: Navigating to `#/role/building_safety_lead` or `#/role/repairs` (with or without `?case=...&page=...`) loads `/role-screens.js`, renders `safety-lead` or `hazard-triage` respectively when `me.user.role` is authorized, and renders the `"Screen unavailable"` alert without switching or simulating roles when `me.user.role` is unauthorized.
* `AC-03`: Per-home and cross-home cells in `safety-lead` and `hazard-triage` lead with plain-language textual state cues (`Confirmed:`, `Waiting:`, `Action needed:`, `Unknown:`, `State:`, `Stop-work indicator:`), include explicit `urgency:` labels and non-colour cue key prose, reject `Object.prototype` keys such as `constructor` via `Object.hasOwn`, guard unparseable date strings against `"Recorded Unknown"` / `"Service responded Unknown"`, and keep all existing `test_safety_screens.py` assertions passing.
* `AC-04`: `style.css` gives `.screen-links a` persistent `text-decoration: underline` and `min-height: 1.5rem` (24px) flex alignment without `.screen-*` transitions/animations, and gives `.flag` and `.flag.danger` explicit `1px solid` borders alongside existing `.flag.danger:before` symbol and contrast tokens.
* `AC-05`: `test_role_screens_conformance.py` passes with the `'h("a", { href: "#",' ` inline-onclick carve-out removed and forbids `href: "#"` in `role-screens.js`, and `test_safety_screen_wcag_keyboard.py` covers delegated `data-jump` focus/scroll, `#/role/...` route aliases, `Object.hasOwn` prototype safety, corrupt timestamps, cross-home summary jump/state labels, and `.screen-links a` / `.flag` CSS rules within the locked test bounds.
* `AC-06`: Focused-tier validation in `src/api` (`python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, `node --check`, and targeted unit suites including `test_safety_screens.py`, `test_safety_screen_wcag_keyboard.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_design_system.py`, `test_asset_exec_screen_wcag.py`, `test_finance_screens_wcag_225.py`, and `test_workspace_scripts.py`) exits `0`, and refreshed Web Interface Guidelines `file:line` audit reports pass.
* `AC-07`: All dated 2026-11-15 RPI artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews`, and `rpi-sessions`) are reconciled and committed in a single clean local commit after `rpi-review` using privacy-safe `git config --local user.email "{id}+{login}@users.noreply.github.com"`, `Refs #227`, and the Copilot `Co-authored-by` trailer, with no push to remote.

## Locked Test Ownership and Bounds

* Canonical modified test files: `src/api/tests/test_safety_screen_wcag_keyboard.py` and `src/api/tests/test_role_screens_conformance.py`.
* New test files created: `none` (`0`).
* Test removals: `none` (`0` test classes or methods deleted; `test_jump_button_moves_focus_and_tolerates_missing_target` in `test_safety_screen_wcag_keyboard.py` is updated in place from `.attrs.onclick` invocation to shared `a[data-jump]` delegated click dispatch).
* Maximum net new test methods added: `5` (in `src/api/tests/test_safety_screen_wcag_keyboard.py`, importing sibling symbols via canonical `from test_safety_screens import ...` to satisfy `pyproject.toml` `mypy --strict` and `ruff`).
* Canonical production targets: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, and `src/api/src/zava_forward/api/web/style.css` (generated targets: `none`).
* Semantic-versus-regression coverage:
  * Behavioral / semantic tests: Node VM delegated `a[data-jump]` click dispatch against rendered VDOM heading targets (verifying `preventDefault`, `focus`, `scrollIntoView`, and missing-target safety); Node VM route dispatch for `#/role/building_safety_lead` and `#/role/repairs` across authorized and unauthorized roles; VDOM evaluation of word-first state cues, cross-home summary `Stop-work indicator:` labels, `Object.hasOwn` prototype-key rejection (`constructor`), and corrupt timestamp handling.
  * Structural / regression guards: `RoleScreenConformance` removal of `'h("a", { href: "#",' ` exemption + `assertNotIn('href: "#"', source)`, `.screen-links a` underline + `min-height: 1.5rem` and `.flag` border assertions, and unchanged cross-suite regressions (`test_safety_screens.py`, `test_role_screens.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_design_system.py`, `test_asset_exec_screen_wcag.py`, `test_workspace_scripts.py`).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/safety-repairs-wcag-227-plan.md                                                                       |
| Phase details                    | .copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md                                                            |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/safety-repairs-wcag-227-plan-critique.md with Revise disposition (PC-001 through PC-004 all resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/safety-repairs-wcag-227-research.md                                                                |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/safety-repairs-wcag-227-changes.md is created by implementation as its evidence record              |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                       |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to rpi-implement                                                                 |

## Sources

* `/tmp/issue-227.md`: Acceptance criteria and open WCAG 2.2 baseline (#151) scope for #227.
* `.copilot-tracking/research/2026-11-15/safety-repairs-wcag-227-research.md`: Cycle 1 Wider, Deeper, and Contrarian findings (`C1`–`C20`, `W1`) and converged Option A design.
* `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, `docs/reference/research/ux/customer-journeys/safety.md`: Governing WCAG 2.2 AA, Fluent 2, plain-language, and safety journey rules.
* `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/style.css`: Web workspace implementation targets.
* `src/api/tests/test_safety_screens.py`, `src/api/tests/test_safety_screen_wcag_keyboard.py`, `src/api/tests/test_role_screens.py`, `src/api/tests/test_role_screens_conformance.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_design_system.py`, `src/api/tests/test_asset_exec_screen_wcag.py`, `src/api/tests/test_workspace_scripts.py`: Constraining test contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Upgrade safety/hazard WCAG 2.2 jump navigation, textual state labels, non-colour CSS signals, and `#/role/...` route aliases

* Intent: Deliver complete WCAG 2.2 AA engineering support across `role-screens.js`, `app.js`, and `style.css` for `safety-lead` (`#/role/building_safety_lead`) and `hazard-triage` (`#/role/repairs`) without violating read-only, plain-language, or cross-screen invariants.
* Dependencies: Completed research `.copilot-tracking/research/2026-11-15/safety-repairs-wcag-227-research.md` (`C1`–`C20`, `W1`) and pre-edit Web Interface Guidelines fetch (`W1`).

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Migrate `hazardPanel`/`hazardJump` to `screenPanel` landmarks and `data-jump` delegation, add cross-home jump nav, and wire `#/role/...` aliases

* Requirement and evidence: `FR-01`, `FR-02`, `NFR-01`; research `C7`–`C11`, `C14`, `C18`–`C20`, `W1`.
* Expected result: `hazardPanel` delegates to `screenPanel(title, { anchor: "hazard-" + key }, ...)` with `<section id>` and `<h2 id tabindex="-1">`; `hazardJump` emits `<a href="#hazard-${key}-heading" data-jump="hazard-${key}-heading" data-jump-target="hazard-${key}-heading">` with zero inline `onclick`; shared `a[data-jump]` delegation preserves the exact `event.preventDefault();\n    document.getElementById` prefix while adding optional `scrollIntoView?.({ block: "start" })`; `hazardQueue.summary` renders section jump nav + `screenPanel` landmark; `app.js` and `role-screens.js` resolve `#/role/building_safety_lead` -> `safety-lead` and `#/role/repairs` -> `hazard-triage` with full `me.user.role` permission enforcement.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Standardize word-first, `Object.hasOwn`-safe textual state labels and non-colour cue keys across `hazardScreen` and `hazardQueue.summary`

* Requirement and evidence: `FR-03`, `NFR-01`; research `C3`, `C4`, `C6`, `C13`, `C15`–`C18`.
* Expected result: Every state cell in `hazardScreen` and `hazardQueue.summary` (`hazardStep`, `hazardSafetyClock`, `hazardFollowUp`, `hazardEscalationState`, `hazardClock`, `hazardHold`, cross-home `pause`, `urgency:`, and cross-home `Unavailable`/`Unknown`/`Mismatch` rows) leads with explicit state words (`Confirmed:`, `Waiting:`, `Action needed:`, `Unknown:`, `State:`, `Stop-work indicator:`), guards prototype properties via `Object.hasOwn` and unparseable date strings, adds explicit non-colour words-first cue prose on both views, uses zero banned `CopyAudit` words, and preserves every existing substring contract.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Enforce non-colour link underlines, 24px minimum target height on `.screen-links a`, and non-colour borders on `.flag` / `.flag.danger`

* Requirement and evidence: `FR-04`, `NFR-01`; research `C1`, `C2`, `C12`, `C19`.
* Expected result: `src/api/src/zava_forward/api/web/style.css` sets `display: inline-flex; align-items: center; min-height: 1.5rem; padding-inline: var(--sp-1); text-decoration: underline;` on `.screen-links a` (preserving `aria-current="page"` bold weight + thicker underline and `:focus-visible` two-tone ring with zero motion on `.screen-*`), `scroll-margin-top: var(--sp-4)` on `.screen-record h2`, and `border: 1px solid var(--soft-line)` on `.flag` plus `border-color: var(--warn)` on `.flag.danger`.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Update WCAG and conformance tests, execute Focused-tier validation, and prepare post-review commit

* Intent: Lock all new WCAG 2.2 keyboard, state-cue, CSS, and `#/role/...` routing behaviors in automated tests, verify zero regressions across static/unit/browser/guideline checks, reconcile tracking artifacts, and sequence a single clean local commit immediately after `rpi-review`.
* Dependencies: `P01` (`P01-T01`, `P01-T02`, `P01-T03`).

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update `test_safety_screen_wcag_keyboard.py`, tighten `test_role_screens_conformance.py`, and align `safety_screens_browser_check.py` within locked bounds

* Requirement and evidence: `FR-01`–`FR-04`, `NFR-01`, `AC-01`–`AC-05`; research `C13`–`C19`.
* Expected result: `test_role_screens_conformance.py` drops the `'h("a", { href: "#",' ` inline-onclick carve-out and asserts `href: "#"` is absent from `role-screens.js`; `test_safety_screen_wcag_keyboard.py` updates `test_jump_button_moves_focus_and_tolerates_missing_target` to test delegated `a[data-jump]` click dispatch against rendered VDOM headings and adds `3` focused methods (`<= 5` max) covering `#/role/building_safety_lead` & `#/role/repairs` route dispatch/permissions, `Object.hasOwn` prototype-key & corrupt-timestamp safety, cross-home summary jump nav & `Stop-work indicator:` labels, and `.screen-links a` / `.flag` CSS rules; `checks/safety_screens_browser_check.py` renders `content-visibility: auto` panels during text/axe inspection and verifies `#/role/...` navigation, `>= 24px` underlined jump links, and keyboard `Enter` heading focus in Chromium.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Run Focused-tier validation, record refreshed Web Interface Guidelines `file:line` check, and reconcile artifacts for `rpi-review` and post-review local commit

* Requirement and evidence: `NFR-01`, `NFR-02`, `AC-06`, `AC-07`; caller prompt and AMA repository instructions.
* Expected result: `mypy`, `ruff check .`, `ruff format --check .`, `node --check`, and targeted `src/api` unit suites pass cleanly using worktree-local `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src`; refreshed Web Interface Guidelines `file:line` audit of `role-screens.js`, `app.js`, and `style.css` passes and is recorded in `.copilot-tracking/changes/2026-11-15/safety-repairs-wcag-227-changes.md`; plan and phase-detail checkboxes/statuses are reconciled before `rpi-review`, with the single local `git commit` (privacy-safe `gh api user` noreply email, `Refs #227`, Copilot trailer, no push) executed immediately after `rpi-review` writes `.copilot-tracking/reviews/2026-11-15/safety-repairs-wcag-227-review.md`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md

## Dependencies

* `node` CLI runtime on `PATH`: Required by Node VM VDOM and global-scope unit tests in `src/api/tests/`.
* Worktree-local Python packages (`src/core`, `src/agents`, `src/api`) and linters (`mypy`, `ruff`): Required for Focused-tier validation in `src/api`.
* `gh api user` authentication: Required before local `git commit` to configure repository-local `user.email` as `{id}+{login}@users.noreply.github.com`.

## Critique Disposition

One-pass critique executed in `.copilot-tracking/reviews/plans/2026-11-15/safety-repairs-wcag-227-plan-critique.md` (`Verdict: Revise`; `0 Critical`, `1 High`, `2 Medium`, `1 Low`; all owned by `planning_parent` with `Direct planner correction`). All four findings were applied directly before implementation without repeating critique.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High] (`P01-T02` symbols, `h.state`, `h.hold` `CopyAudit`, full release decision strings, `hazardPanel("boundary", ...)`) | Resolved | Updated `P01-T02` in `.copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md` to call `screenStamp`, read `h?.state` and `h.clock_text \|\| h.escalation_clock`, retain exact `(h && h.hold) \|\| {}` / `(x && x.hold) \|\| {}` with `Object.hasOwn(..., "status")`, preserve full `Scope`/`Decided by`/`Reason`/`Evidence`/no-decision strings in `hazardHold`, split cross-home `Released` deterministically with 13-cell sentinel rows, and place cue-key prose inside `hazardPanel("boundary", ...)`. |
| `PC-002` [Medium] (`P01-T01` `?.focus?.()` and `roleScreensView()` local names) | Resolved | Updated `P01-T01` in `.copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md` to invoke `?.focus?.()` (tolerating plain `{}` targets while keeping the pinned `event.preventDefault();\n    document.getElementById` substring) and bind `const id = query.get("screen") \|\| aliasScreen;` using `roleScreensView()`'s actual `query`, `id`, `installed`, and `screen` variables. |
| `PC-003` [Medium] (`P02-T01` `test_safety_screens` exports, exact method name, and `ruff` `E402`-clean import pattern) | Resolved | Updated `P02-T01` in `.copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md` to reference actual `test_safety_screens` exports (`SAFE`, `SENDER`, `SCRIPT`, `WEB`, `find_all`, `hazard`, `run`, `string_leaves`, `tags`), update `test_sections_are_headed_landmarks_with_keyboard_jump_links` in place, and use `if TYPE_CHECKING:` + `importlib.import_module("test_safety_screens")`. |
| `PC-004` [Low] (`P01-T03` base `.screen-links a` font-weight vs `aria-current="page"`) | Resolved | Updated `P01-T03` in `.copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md` to omit `font-weight: 600` from base `.screen-links a` so `.screen-links a[aria-current="page"]` retains both bold weight (`600`) and thicker underline (`.2em`). |

## Follow-Up Items

* Human assistive-technology and named safety-role user validation (#151, #155, #156) for `safety-lead` and `hazard-triage`: Outside automated CLI scope because repository accessibility governance (`docs/reference/research/ux/wcag-conformance-baseline.md`) requires manual screen-reader, magnification, and named safety-role walkthroughs before claiming full WCAG 2.2 AA conformance or closing #227. Owner: Human UX / Building Safety Lead reviewer.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/safety-repairs-wcag-227-changes.md
* Ready phase or task: P01 (`P01-T01`, `P01-T02`, `P01-T03`)
* Remaining provisional question or blocker: None

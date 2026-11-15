<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #227 Building Safety Lead and Repairs Hazard Screens WCAG 2.2

## Metadata

* Task ID: 2026-11-15-safety-repairs-wcag-227
* Task slug: safety-repairs-wcag-227
* Related plan: .copilot-tracking/plans/2026-11-15/safety-repairs-wcag-227-plan.md
* Evidence sources: /tmp/issue-227.md, .copilot-tracking/research/2026-11-15/safety-repairs-wcag-227-research.md (C1-C20, W1)

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Upgrade safety/hazard WCAG 2.2 jump navigation, textual state labels, non-colour CSS signals, and `#/role/...` route aliases | Ready | P01, P01-T01, P01-T02, P01-T03 |
| P02 | Update WCAG and conformance tests, execute Focused-tier validation, and prepare post-review commit | Ready | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Upgrade safety/hazard WCAG 2.2 jump navigation, textual state labels, non-colour CSS signals, and `#/role/...` route aliases

### Context

Research (`C6`–`C12`) identified four engineering WCAG 2.2 Level AA gaps across `safety-lead` ("Building safety referral queue") and `hazard-triage` ("Repairs and hazard triage"):
1. `hazardJump` renders `<a href="#" onclick="...">` instead of real `#hazard-${key}-heading` fragment targets using the shared `a[data-jump]` click delegation, `hazardPanel` omits `<section id>`, and cross-home `hazardQueue.summary` has no section jump navigation.
2. Direct navigation to `#/role/building_safety_lead` and `#/role/repairs` (as named in issue #227 context) is unhandled in `app.js` and `role-screens.js`.
3. Multiple state, follow-up, escalation, clock, urgency, and cross-home pause/anomaly cells omit lead plain-language state words (`Confirmed:`, `Waiting:`, `Action needed:`, `Unknown:`, `State:`, `Stop-work indicator:`) or `Object.hasOwn` / corrupt-date guards, and neither view includes the explicit words-first non-colour cue key shown on sibling WCAG-upgraded screens.
4. `nav a` in `style.css` strips underlines from `.screen-links a` and leaves jump/screen links below the WCAG 2.2 2.5.8 24px (`1.5rem`) target height, while `.flag` and `.flag.danger` lack `1px solid` borders for non-colour and `forced-colors` contrast.

### Intent

Upgrade `role-screens.js`, `app.js`, and `style.css` so both safety and repairs hazard screens satisfy the WCAG 2.2 AA engineering baseline (#151), Fluent 2 inventory (#150), plain-language standard (#153), and Web Interface Guidelines (`W1`) with zero regressions to read-only, table-structure, or global-scope contracts.

### Boundaries

* Included: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, and `src/api/src/zava_forward/api/web/style.css`.
* Excluded: Backend API routes, database projections, write controls (`<button>`, `<form>`, `<input>`, `<select>`, `<textarea>`), `screenRecordTable` `<th scope="row">` conversion (forbidden by `test_safety_screens.py:131-133`), undocumented CSS classes, `.screen-*` animations/transitions, and role-switching simulators.

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: `ROLE_HASH_SCREENS` + `roleScreensView`, shared `a[data-jump]` click listener, `hazardStep`–`hazardQueue` helpers and renderers.
* `src/api/src/zava_forward/api/web/app.js`: `isRoleScreensDestination` helper used by `missingWorkspaceScripts` and `route()`.
* `src/api/src/zava_forward/api/web/style.css`: `.flag`, `.flag.danger`, and `.screen-links a` rules.

### Dependencies

* None beyond completed Cycle 1 research (`C1`–`C20`, `W1`).

### Validation Expectations

* `node --check` passes on both `role-screens.js` and `app.js`.
* All existing safety, role-screen, accessibility, content-standard, design-system, and workspace-script unit suites pass without breaking pinned substrings or structural counts.

### Completion Evidence

* Clean working-tree diff across `role-screens.js`, `app.js`, and `style.css` satisfying `FR-01` through `FR-04` and `NFR-01`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Migrate `hazardPanel`/`hazardJump` to `screenPanel` landmarks and `data-jump` delegation, add cross-home jump nav, and wire `#/role/...` aliases

#### Context

* `hazardPanel` (`role-screens.js`) currently builds `h("section", { class: "card screen-record", "aria-labelledby": id }, h("h2", { id, tabindex: "-1" }, title), ...)` without `id: "hazard-" + key`, whereas `screenPanel(title, { anchor: "hazard-" + key }, ...)` builds `<section id="hazard-${key}" class="card screen-record" aria-labelledby="hazard-${key}-heading">` with `<h2 id="hazard-${key}-heading" tabindex="-1">`.
* `hazardJump` currently renders `<a href="#" onclick="...">` instead of `href: "#hazard-" + key + "-heading"`, `"data-jump": "hazard-" + key + "-heading"`, and `"data-jump-target": "hazard-" + key + "-heading"`.
* `test_asset_exec_screen_wcag.py` (`C14`) asserts the exact substring `'event.preventDefault();\n    document.getElementById'` in the shared `a[data-jump]` listener in `role-screens.js`, while `test_finance_screens_wcag_225.py` mocks `focus()` on targets that do not implement `scrollIntoView`. Keeping `event.preventDefault();\n    document.getElementById(link.getAttribute("data-jump"))?.focus();` intact and adding `document.getElementById(link.getAttribute("data-jump"))?.scrollIntoView?.({ block: "start" });` on the next line satisfies both suites and smooth keyboard/click viewport scrolling.
* `app.js` (`C10`, `C20`) checks `destination === "#/screens"` in `missingWorkspaceScripts` and `p === "#/screens"` in `route()`, and `test_role_screens.py` asserts `source.index("return await roleScreensView()") < source.index("return await (m ? contractorCaseView")`, while `RoleScreensGlobalScope` (`C16`) forbids top-level identifier collisions between `app.js` and `role-screens.js`.

#### Intent

Eliminate dead `href="#"` and inline `onclick` in `hazardJump`, give every safety section (per-home and cross-home summary) an anchored `screenPanel` landmark and delegated `a[data-jump]` jump link, and resolve `#/role/building_safety_lead` and `#/role/repairs` cleanly under `me.user.role` permissions.

#### Boundaries

* Included:
  * In `role-screens.js`:
    * Define `const ROLE_HASH_SCREENS = { "#/role/building_safety_lead": "safety-lead", "#/role/repairs": "hazard-triage" };` and update `roleScreensView()` to parse `const [routePath, rawQuery = ""] = (location.hash || "#/screens").split("?");`, `const query = new URLSearchParams(rawQuery);`, `const aliasScreen = Object.hasOwn(ROLE_HASH_SCREENS, routePath) ? ROLE_HASH_SCREENS[routePath] : null;`, and `const id = query.get("screen") || aliasScreen;` so authorized roles render the target screen (preserving `menu` `aria-current="page"` and `screenHref(id, ...)` home/pagination/reset links) and unauthorized roles hit `if (id && !screen)` and see `"Screen unavailable"`.
    * In the shared `document.addEventListener("click", ...)` handler for `a[data-jump]`, retain the exact `event.preventDefault();\n    document.getElementById` prefix pinned by `test_asset_exec_screen_wcag.py` with optional-call `?.focus?.()`: `event.preventDefault();\n    document.getElementById(link.getAttribute("data-jump"))?.focus?.();\n    document.getElementById(link.getAttribute("data-jump"))?.scrollIntoView?.({ block: "start" });`.
    * Implement `hazardPanel(key, title, ...children)` via `return screenPanel(title, { anchor: \`hazard-${key}\` }, ...children);`.
    * Implement `hazardJump(sections)` to emit `h("nav", { "aria-label": "Sections on this screen", class: "screen-links" }, sections.map(([key, title]) => { const id = \`hazard-${key}-heading\`; return h("a", { href: \`#${id}\`, "data-jump": id, "data-jump-target": id }, \`Go to ${title}\`); }))`.
    * Update `hazardQueue.summary(entries)` to wrap `hazardJump([["page-summary", "Hazard referrals across this page of homes"]])` and `hazardPanel("page-summary", "Hazard referrals across this page of homes", ...)` inside `h("div", {}, ...)`.
  * In `app.js`:
    * Place `function isRoleScreensDestination(destination) { return destination === "#/screens" || destination === "#/role/building_safety_lead" || destination === "#/role/repairs"; }` immediately after `function missingWorkspaceScripts` (before `async function requireWorkspaceScripts` and `const defaultListState`) so both `test_workspace_scripts.py` slices (`STARTUP_RETRY_DELAYS`..`missingWorkspaceScripts` and `STARTUP_RETRY_DELAYS`..`defaultListState`) include the exact declarations they expect without top-level collisions against `role-screens.js`.
    * In `missingWorkspaceScripts(hash, caseRoute)`, compute `const screensRoute = isRoleScreensDestination(destination);`, update the `/ops.js` Contractor check from `destination !== "#/screens"` to `!screensRoute`, and update the `/role-screens.js` check from `destination === "#/screens"` to `screensRoute`.
    * In `route()`, map `isRoleScreensDestination(hash.split("?")[0])` to `"#/screens"` when computing `active` nav link highlight and change `if (hash.split("?")[0] === "#/screens") return await roleScreensView();` to `if (isRoleScreensDestination(hash.split("?")[0])) return await roleScreensView();` (preserving `source.index("return await roleScreensView()") < source.index("return await (m ? contractorCaseView")` in `test_role_screens.py`).
* Excluded: Changing `SCRIPT_RETRY_DELAYS`, `return workspaceScriptLoads.get(path);`, `if (outcome !== "error") break;`, or adding any role-switching parameter.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`
* `src/api/src/zava_forward/api/web/app.js`

#### Dependencies

* Check `src/api/tests/test_workspace_scripts.py` before editing `missingWorkspaceScripts` in `app.js` so exact expected return arrays for every role and route remain aligned.

#### Validation Expectations

* `node --check` passes on `app.js` and `role-screens.js`; `test_workspace_scripts.py`, `test_role_screens.py`, `test_asset_exec_screen_wcag.py`, and `test_finance_screens_wcag_225.py` pass.

#### Completion Evidence

* Zero `href: "#"` or `<a>` inline `onclick:` in `role-screens.js`; `#/role/building_safety_lead` and `#/role/repairs` route to `roleScreensView()` under `me.user.role` enforcement.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Standardize word-first, `Object.hasOwn`-safe textual state labels and non-colour cue keys across `hazardScreen` and `hazardQueue.summary`

#### Context

* `CopyAudit` (`C15`) forbids `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` on any line of `role-screens.js` except exact allowlisted property reads (`h.hold`, `x.hold`).
* `test_safety_screens.py` (`C13`), `safety_screens_browser_check.py` (`C17`), and `specialist_keyboard_browser_check.py` (`C18`) pin table captions (`"Hazard referrals for this home"`, `"Scoped pause and release evidence"`, `"Hazard referrals across this page of homes"`), `<td>` == `<th>` column counts (`screenTable`), SA-007 >50 rows, and exact status substrings.
* Sibling WCAG tests (`test_assessor_screen_wcag.py`, `test_procurement_screen_wcag.py`) verify that `Object.prototype` keys such as `"constructor"` never resolve to truthy prototype functions when mapping states.

#### Intent

Ensure every state cell in per-home and cross-home safety tables starts with clear, screen-reader-friendly state words (`Confirmed:`, `Waiting:`, `Action needed:`, `Unknown:`, `State:`, `Stop-work indicator:`), rejects prototype pollution via `Object.hasOwn`, guards corrupt date strings, and explains the words-first cue system in plain British English.

#### Boundaries

* Included:
  * `hazardStep(stamp)`: return `"State: Not recorded"` when falsy; format via `const formatted = screenStamp(stamp);` and return `` `Unknown: Timestamp not readable (${screenValue(stamp)})` `` when `formatted === "Unknown"`, otherwise `` `State: Recorded ${formatted}` ``.
  * `hazardSafetyClock(h)`: read `const clock = h.clock_text || h.escalation_clock;` and return `` `State: ${clock}` `` when truthy, otherwise `"Unknown: Clock not supplied"`.
  * `hazardFollowUp(h)`: preserve exact existing branches (`h.accepted_at`, `h.received_at`, `h.sent_at`, `h.referred`, default) and actor formatting (`hazardActor(...)`, `screenValue(h.owner)`), prepending `"Confirmed: "` on `h.accepted_at` and `"Action needed: "` on the four pending/legacy/unsent branches.
  * `HAZARD_ESCALATION_CUES` + `hazardEscalationState(h)`: classify `{ Accepted: "Confirmed", Sent: "Action needed", Received: "Action needed", Referred: "Action needed", Open: "Action needed", Escalated: "Action needed" }` from `h?.state` via `Object.hasOwn(HAZARD_ESCALATION_CUES, raw)` (default `"Unknown"`), returning `"Unknown: Escalation state: Unknown"` when `screenValue(h?.state) === "Unknown"` and `` `${cue}: Escalation state: ${raw}` `` otherwise.
  * `hazardClock(h)`: when `h.responded_at` is truthy, check `const formatted = screenStamp(h.responded_at);` and return `` `Unknown: Service responded (${screenValue(h.responded_at)}; timestamp not readable)` `` if `"Unknown"`, else `` `Confirmed: Service responded ${formatted}` ``; return `"Unknown: Service response clock: no due time recorded"` when `!h.response_due_at`; return `` `Unknown: Service response clock: due time not readable (${screenValue(h.response_due_at)})` `` when `Number.isNaN(due)`; otherwise return `` `${late ? "Action needed: Overdue" : "Waiting: Awaiting"} service response. Due ${screenStamp(h.response_due_at)}. Recorded by the service, not set here` ``.
  * `hazardHold(h)`: read `const pause = (h && h.hold) || {};` (preserving exact `h.hold` for `CopyAudit`), `const status = Object.hasOwn(pause, "status") ? screenValue(pause.status) : "Unknown";`, `const decision = Object.hasOwn(pause, "decision") ? pause.decision : null;`, and `const scope = \`${screenValue(pause.scope)} ${screenValue(pause.case_id)} only\`;`. When `status !== "Released"`, prepend `${status === "Active" ? "Action needed" : "Unknown"}: ` onto `Stop-work indicator: ${status === "Active" ? "retrofit work is paused" : "pause status " + status}. Scope: ${scope}. Release needs an authorised human decision.`. When `status === "Released"`, prepend `"Confirmed: "` when `decision` is truthy (`Confirmed: Stop-work indicator: released. Scope: ${scope}. Decided by ${hazardActor(decision.actor)} at ${screenStamp(decision.at)}. Reason: ${screenValue(decision.reason)}. Evidence: ${screenValue(decision.evidence)}`) and `"Action needed: "` when `decision` is absent (`Action needed: Stop-work indicator: released. Scope: ${scope}. No authoritative decision evidence is recorded; do not rely on this release.`).
  * Reported observation & urgency cell in both `hazardScreen` and `hazardQueue.summary`: `` `${screenValue(x.category)}, urgency: ${screenValue(x.priority)}` ``.
  * Cross-home `pause(x)` and 13-column anomaly rows in `hazardQueue.summary`: read `const pauseObj = (x && x.hold) || {};` (exact `x.hold` for `CopyAudit`), `const status = Object.hasOwn(pauseObj, "status") ? screenValue(pauseObj.status) : "Unknown";`, and `const hasDecision = Boolean(Object.hasOwn(pauseObj, "decision") && pauseObj.decision);`. Return `"Action needed: Stop-work indicator: Active (retrofit work paused)"` when `status === "Active"`; when `status === "Released"`, return `"Confirmed: Stop-work indicator: Released (decision recorded; open the home to inspect)"` if `hasDecision` is true and `"Action needed: Stop-work indicator: Released. Release decision evidence: open the home"` if `hasDecision` is false; otherwise return `` `Unknown: Stop-work indicator: ${status}` ``. Keep `const flag = (cells) => [...cells, ...Array(11).fill("Unavailable")];` (13 `<td>` cells total) with `"Unknown: Unavailable. Open the home to check."`, `"Unknown: Unknown. Hazard list not supplied. Open the home to check."`, and `"Action needed: Mismatch. The list flags a hazard but the case returns none. Open the home to check."`.
  * Add the plain-language cue-key sentence inside `hazardPanel("boundary", "Evidence and checks", ...)` in `hazardScreen` (preserving the exact 4 panels `boundary`, `queue`, `restart`, `act`) and inside `hazardPanel("page-summary", "Hazard referrals across this page of homes", ...)` in `hazardQueue.summary`: `"Every referral, clock, and stop-work state is written as words first (Confirmed, Waiting, Action needed, State, or Unknown), so colour is never the only signal."`
* Excluded: Altering table captions, column counts, `screenTable` `<td>` tags, or using any `CopyAudit` banned word.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`

#### Dependencies

* `P01-T01` (`hazardPanel` and `hazardQueue.summary` structure).

#### Validation Expectations

* `test_safety_screens.py` and `test_content_standard.py` pass with zero substring or vocabulary failures.

#### Completion Evidence

* Every status/clock/pause/urgency cell in `hazardScreen` and `hazardQueue.summary` leads with explicit textual state meaning and handles missing, corrupt, and `Object.prototype` inputs safely.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Enforce non-colour link underlines, 24px minimum target height on `.screen-links a`, and non-colour borders on `.flag` / `.flag.danger`

#### Context

* `style.css` (`C12`) defines `nav a { ... text-decoration: none; padding: .2rem .1rem; }`, which strips underlines from `<nav class="screen-links"><a>` at rest so links differ from body copy by colour alone (`--brand-d` vs `--ink`) and fall below the 24x24 CSS px (`1.5rem`) WCAG 2.2 2.5.8 target size. It also prevents `a[aria-current="page"]` (`text-decoration-thickness: .2em`) from rendering a thicker underline until hovered.
* `.flag` and `.flag.danger` (`style.css`) lack borders, weakening pill boundaries when backgrounds are stripped or overridden.
* `test_role_screens_conformance.py` (`C19`) forbids `animation` and `transition` inside any `.screen-*` rule in `style.css`.

#### Intent

Ensure `.screen-links a` links and `.flag` / `.flag.danger` badges satisfy WCAG 2.2 1.4.1 (Use of Color), 1.4.11 (Non-text Contrast / forced-colors resilience), and 2.5.8 (Target Size Minimum, 24x24 CSS px) using existing Fluent 2 spacing and colour tokens.

#### Boundaries

* Included:
  * Update `.screen-links a` in `src/api/src/zava_forward/api/web/style.css` to `display: inline-flex; align-items: center; min-height: 1.5rem; padding: var(--sp-1) var(--sp-2); color: var(--brand-d); text-decoration: underline; text-underline-offset: .16em;` (omitting `font-weight: 600` on base links so `.screen-links a[aria-current="page"]` retains both `font-weight: 600` and `text-decoration-thickness: .2em`, with zero `transition` or `animation` properties).
  * Update `.flag` in `src/api/src/zava_forward/api/web/style.css` to add `border: 1px solid var(--soft-line);` and `.flag.danger` to add `border-color: var(--warn);` while preserving existing background, foreground, and `.flag.danger:before { content: "\26A0 "; }` rules.
* Excluded: Inventing new CSS class names or adding motion to `.screen-*`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/style.css`

#### Dependencies

* None.

#### Validation Expectations

* `test_accessibility_baseline.py`, `test_design_system.py`, and `test_role_screens_conformance.py` pass.

#### Completion Evidence

* `.screen-links a` has persistent underline and `min-height: 1.5rem`; `.flag` and `.flag.danger` carry explicit borders; zero motion on `.screen-*`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Update WCAG and conformance tests, execute Focused-tier validation, and prepare post-review commit

### Context

`test_safety_screen_wcag_keyboard.py` (`C16`) currently invokes `links[1].attrs.onclick(...)` directly, which becomes obsolete when `hazardJump` moves to `data-jump` delegation, and does not yet cover `#/role/building_safety_lead` / `#/role/repairs` route aliases, cross-home summary jump nav and `Stop-work indicator:` labels, `Object.hasOwn` prototype-key safety, corrupt timestamps, or `.screen-links a` / `.flag` CSS rules. Meanwhile `test_role_screens_conformance.py` (`C19`) still contains the legacy `'h("a", { href: "#",' ` inline-onclick carve-out that existed solely for `hazardJump`.

### Intent

Update focused tests within locked bounds, run the full Focused-tier validation suite (`mypy`, `ruff check .`, `ruff format --check .`, `node --check`, and targeted `src/api` unit suites), refresh and record the Web Interface Guidelines `file:line` review, reconcile plan/detail markers, and execute a single clean local commit immediately after `rpi-review`.

### Boundaries

* Included: `src/api/tests/test_safety_screen_wcag_keyboard.py`, `src/api/tests/test_role_screens_conformance.py`, `src/api/checks/safety_screens_browser_check.py`, `.copilot-tracking/changes/2026-11-15/safety-repairs-wcag-227-changes.md`, and plan/details status reconciliation.
* Excluded: Adding new test files, deleting existing test methods, adding `tests/__init__.py`, referencing `.copilot-tracking/` in code/tests/commit messages, amending commits without permission, or pushing to remote.

### Likely Targets

* `src/api/tests/test_safety_screen_wcag_keyboard.py`
* `src/api/tests/test_role_screens_conformance.py`
* `src/api/checks/safety_screens_browser_check.py`
* `.copilot-tracking/changes/2026-11-15/safety-repairs-wcag-227-changes.md`

### Dependencies

* `P01` complete (`P01-T01`, `P01-T02`, `P01-T03`).

### Validation Expectations

* From `src/api`:
  * `python3 -m mypy` -> `Success: no issues found`
  * `python3 -m ruff check .` -> `All checks passed!`
  * `python3 -m ruff format --check .` -> formatted cleanly
  * `node --check src/zava_forward/api/web/role-screens.js && node --check src/zava_forward/api/web/app.js` -> exit `0`
  * `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests python3 -m unittest tests/test_safety_screens.py tests/test_safety_screen_wcag_keyboard.py tests/test_role_screens.py tests/test_role_screens_conformance.py tests/test_accessibility_baseline.py tests/test_content_standard.py tests/test_design_system.py tests/test_asset_exec_screen_wcag.py tests/test_finance_screens_wcag_225.py tests/test_workspace_scripts.py -v` -> exit `0`
  * Also verify discovery without `:tests` in `PYTHONPATH`: `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest discover -s tests -p 'test_*screen*.py' -q` -> exit `0`.

### Completion Evidence

* Passing Focused-tier command outputs and refreshed Web Interface Guidelines `file:line` audit recorded in `.copilot-tracking/changes/2026-11-15/safety-repairs-wcag-227-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update `test_safety_screen_wcag_keyboard.py` and tighten `test_role_screens_conformance.py` within locked bounds

#### Context

* `src/api/pyproject.toml` configures `mypy` with `strict = true`, `mypy_path = ["src", "tests", "../core/src", "../core/tests"]`, and `explicit_package_bases = true`, and enables `ruff` `E`/`F`/`I`/`B`/`UP`. `src/api/tests/test_safety_screen_wcag_keyboard.py` currently imports `SAFE, SCRIPT, WEB, find_all, hazard, run, string_leaves` from `test_safety_screens` (which also exports `SENDER`, `VIEW_SCRIPT`, and `tags`). Using `if TYPE_CHECKING:` static imports paired with runtime `sys.path` setup + `importlib.import_module("test_safety_screens")` (matching `test_finance_screens_wcag_225.py`) ensures `mypy --strict`, `ruff check .` (zero `E402`), `unittest discover -s tests`, and `:tests`-less `python3 -m unittest tests/test_safety_screen_wcag_keyboard.py` all succeed cleanly.

#### Intent

Provide behavioral and structural regression tests for every #227 WCAG 2.2 requirement within the locked bounds (`0` new files, `0` deletions, `<= 5` net new methods).

#### Boundaries

* Included:
  * In `src/api/tests/test_role_screens_conformance.py`: change `if "onclick:" in line and 'h("a", { href: "#",' not in line:` to `if "onclick:" in line:` and add `self.assertNotIn('href: "#"', source)`.
  * In `src/api/tests/test_safety_screen_wcag_keyboard.py`:
    * Use `if TYPE_CHECKING:` static imports + runtime `importlib.import_module("test_safety_screens")` helper for `SAFE`, `SENDER`, `SCRIPT`, `WEB`, `find_all`, `hazard`, `run`, `string_leaves`, `tags` so `:tests`-less CLI execution, `mypy --strict`, and `ruff` all pass.
    * Update `SafetyScreenWcagKeyboard.test_sections_are_headed_landmarks_with_keyboard_jump_links` in place (`0` deletions) to assert every jump `<a>` carries `href == f"#{target}"`, `data-jump == target`, `data-jump-target == target`, no `onclick` attribute, and matching `<section id>` + `<h2 id tabindex="-1">` on BOTH per-home (`tree`, 4 sections) and cross-home (`summary`, 1 section) renders.
    * Update `RoleScreensGlobalScope.test_jump_button_moves_focus_and_tolerates_missing_target` in place to register/capture `document.addEventListener("click", ...)` in Node VM, build click events whose `target.closest("a[data-jump]")` resolves rendered safety jump links, and verify `preventDefault()`, `focus()`, `scrollIntoView({ block: "start" })`, tolerance when `scrollIntoView` is omitted on a target, and tolerance when `getElementById` returns `null`.
    * Add up to 4 focused test methods (well under the `5` max bound):
      1. `test_state_labels_guard_prototype_keys_and_corrupt_timestamps`: verifies word-first prefixes (`Confirmed:`, `Waiting:`, `Action needed:`, `Unknown:`, `State:`, `Stop-work indicator:`), `urgency:` labels, words-first cue prose, `status: "constructor"` / `hold: { status: "constructor" }` resolving to `"Unknown: ..."`, and corrupt `sent_at` / `responded_at` timestamps never producing `"Recorded Unknown"` or `"Service responded Unknown"`.
      2. `test_cross_home_summary_surfaces_word_first_pause_and_anomaly_states`: verifies cross-home `hazardQueue.summary` renders `Stop-work indicator:` text cues across active, released (with and without recorded decision), unknown, and prototype pause states plus `Unavailable`, `Unknown`, and `Mismatch` rows.
      3. `test_role_route_aliases_resolve_safety_and_repairs_with_role_enforcement`: executes `app.js` + `role-screens.js` routing in Node VM for `#/role/building_safety_lead`, `#/role/building_safety_lead?case=C-1`, and `#/role/repairs` across authorized (`Building Safety Liaison`, `Resident Liaison Officer`) and unauthorized (`Contractor`, cross-role `Resident Liaison Officer` on `#/role/building_safety_lead`) roles, proving `isRoleScreensDestination` and `ROLE_HASH_SCREENS` enforce `me.user.role` and render `"Screen unavailable"` when unauthorized.
      4. `test_screen_links_and_flags_have_non_colour_css_and_target_size`: inspects `style.css` to verify `.screen-links a` retains `text-decoration: underline` and `min-height: 1.5rem` (24px) with zero `transition`/`animation`, and `.flag` / `.flag.danger` declare explicit borders alongside `.flag.danger:before`.
* Excluded: Exceeding `5` net new test methods, deleting any existing test method, or creating new test files.

#### Likely Targets

* `src/api/tests/test_safety_screen_wcag_keyboard.py`
* `src/api/tests/test_role_screens_conformance.py`

#### Dependencies

* `P01-T01`, `P01-T02`, `P01-T03`.

#### Validation Expectations

* Both modified test files pass `mypy`, `ruff check`, `ruff format --check`, `:tests`-less direct `unittest`, and `unittest discover -s tests`.

#### Completion Evidence

* All new and updated assertions pass and fail if any `P01` fix is reverted.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Run Focused-tier validation, record refreshed Web Interface Guidelines `file:line` check, and reconcile artifacts for `rpi-review` and post-review local commit

#### Context

* AMA Web Development Guidance requires refreshing `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before review and auditing modified web files (`role-screens.js`, `app.js`, `style.css`) against all fetched rules in `file:line` format.
* AMA Branch and Pull Request Workflow requires resolving the authenticated GitHub user via `gh api user`, setting repository-local `git config --local user.email "{id}+{login}@users.noreply.github.com"`, never amending commits without permission, and never pushing when the caller specifies `Do not push`.
* Because `.copilot-tracking/reviews/2026-11-15/safety-repairs-wcag-227-review.md` and the final post-Review `Follow-up` state in `.copilot-tracking/rpi-sessions/2026-11-15/safety-repairs-wcag-227-state.json` are written during `rpi-review`, the single local `git commit` must execute after `rpi-review` finishes so every 2026-11-15 RPI artifact is included in one clean commit without `--amend`.

#### Intent

Complete Focused-tier validation, record complete implementation evidence in `.copilot-tracking/changes/2026-11-15/safety-repairs-wcag-227-changes.md`, reconcile plan and phase-detail checkboxes before `rpi-review`, and execute the single clean local Git commit after `rpi-review` transitions state to `Follow-up`.

#### Boundaries

* Included: Running `mypy`, `ruff check .`, `ruff format --check .`, `node --check`, targeted `unittest` suites, optional Playwright safety browser check if browser prerequisites are installed (truthfully disclosing skip/pass status), refreshed Web Interface Guidelines `file:line` audit, writing `.copilot-tracking/changes/2026-11-15/safety-repairs-wcag-227-changes.md`, reconciling `P01`/`P02` checkboxes, and post-`rpi-review` local commit.
* Excluded: `git push`, `git commit --amend`, or `.copilot-tracking/` paths in commit messages.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/safety-repairs-wcag-227-changes.md`
* `.copilot-tracking/plans/2026-11-15/safety-repairs-wcag-227-plan.md`
* `.copilot-tracking/details/2026-11-15/safety-repairs-wcag-227-phase-details.md`

#### Dependencies

* `P02-T01`.

#### Validation Expectations

* Zero errors across `mypy`, `ruff check .`, `ruff format --check .`, `node --check`, and targeted `src/api` unit suites; `git log -1` after `rpi-review` shows privacy-safe noreply author/committer email, `Refs #227`, and Copilot trailer; `git status --short` is empty.

#### Completion Evidence

* Reconciled changes log, review artifact, session state, and clean `git status --short` on `feat/ux-227-safety-repairs-wcag-0006`.

#### Unresolved Items

* None.

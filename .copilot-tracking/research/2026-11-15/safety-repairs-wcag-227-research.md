<!-- markdownlint-disable-file -->

# Task Research: safety-repairs-wcag-227

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                 |
| Researcher / agent | rpi-research (under RPI Agent automatic mode)                              |
| Status             | Complete                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/safety-repairs-wcag-227-research.md  |

## Research Brief

* What to research: Current implementation, gaps, conformance guardrails, and WCAG 2.2 baseline requirements for the Building Safety Lead (`#/role/building_safety_lead`) and Repairs and Hazard Triage (`#/role/repairs`) role screens in `src/api`, focusing on keyboard section jump navigation, textual state meaning, non-colour status signals, semantic structure, and authority/SA-007 guardrails for GitHub issue #227.
* Why it matters: Five of six engineering criteria in issue #227 are recorded as delivered, leaving the WCAG 2.2 baseline (#151) criterion ("Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation") open while preserving referral queue provenance, pending-receipt follow-up, release decision evidence, read-only hazard/clock/authorisation boundaries, SA-007 visibility, and Fluent 2 design system components (#150) without role simulator controls.
* Audience or intended use: Downstream `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases in this confirmed automatic RPI session, plus PR reviewers checking #227 acceptance evidence.
* Scope: `src/api/src/zava_forward/api/web/role-screens.js`, related shell/CSS/DOM files in `src/api/src/zava_forward/api/web/`, existing role-screen and accessibility unit/conformance tests in `src/api/tests/`, UX research/baseline docs (`docs/reference/research/ux/`), PRD journey contract (`docs/prds/zava-forward-retrofit-programme-demonstrator.md`), and Web Interface Guidelines.
* Non-goals: Modifying backend hazard classification, clock computation, hazard closure, or work authorisation authority; introducing a role simulator in user views; unrelated visual overhauls or framework changes; claiming human assistive-technology or hosted CI sign-off from local engineering tests alone; pushing to remote.
* Criteria: Every claim grounded in `path:line` or external `URL + retrieval date`; preserve all already-checked #227 criteria and `RoleScreenConformance` / `test_role_screens.py` / `test_accessibility_baseline.py` invariants; satisfy Fluent 2 design system, WCAG 2.2 AA baseline, plain-language content standard, and Web Interface Guidelines.
* Requested outputs: Converged implementation recommendation with exact screen/helper/CSS/test touchpoints, rejected alternatives, risk analysis, and `Planning Readiness` assessment.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                   |
|----------------------------------|-------------------------------------------------------------------------|
| Research question(s)             | How do `#/role/building_safety_lead` and `#/role/repairs` currently render navigation, landmarks/headings, status badges/pills, referral states, holds/releases, and interactive controls, and what exact changes and tests satisfy #227's WCAG 2.2 keyboard jump nav, text state labels, and non-colour status signals without regressing safety/authority/conformance rules? |
| Codebase scope                   | `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `docs/reference/research/ux/`, `docs/prds/` |
| External scope                   | Vercel Web Interface Guidelines (`raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`) per repository web development guidance |
| Initial internal candidate areas | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/styles.css`, `src/api/src/zava_forward/api/web/index.html`, `src/api/tests/test_role_screens.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_finance_screens_wcag_225.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, `docs/reference/research/ux/customer-journeys/safety.md` |
| Initial external candidate areas | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` |
| Research posture                 | balanced                                                                |
| Posture provenance               | default (bounded UX/accessibility task with named routes, sibling #225 precedent, and adjacent conformance/CSS/delegation interactions to verify) |
| Explicit limits / deadline       | Focused validation tier specified by caller; non-interactive CLI execution; do not push to remote |
| Posture-specific completion basis | balanced scope coverage and adequate evidence across target screens, shared helpers, conformance tests, UX standards, and external Web Interface Guidelines |
| Edits allowed during research?   | no, research-only                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                    |
| Known constraints / excluded sources | Preserve read-only safety boundaries (no hazard classification, clock setting, closure, or work authorisation in UI), SA-007 non-hiding of hazards/safeguarding, no inline `onclick` violating conformance rules, no `.copilot-tracking/` citations in code/tests/commits |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | Repository custom instructions (`applyTo: "**"`) | Matches all repository and tracking paths | Enforces case study/KB orientation, Fluent 2 + WCAG 2.2 + plain-language standards, Web Interface Guidelines fetch, focused validation tier, and branch/commit rules | Selected: mandatory repository governance |
| Skill               | `rpi-research`                   | Explicit first phase of caller's RPI loop         | Owns three-wave research artifact and readiness handoff | Selected: active RPI phase skill |
| Skill               | `accessibility`                  | Matches WCAG 2.2, ARIA APG, non-colour status, and keyboard navigation scope | Supplies WCAG 2.2 / ARIA APG criteria mapping | Selected: loaded at intake for WCAG 2.2 reference alignment |
| Skill               | `redesign-existing-projects`     | Required by repository Web Development Guidance for existing-app UX improvements | Supplies audit checklist constrained by owner Fluent 2 / WCAG baseline rules | Selected: loaded per repository web guidance (subordinate to Fluent 2 and WCAG baseline) |
| Skill               | `web-design-guidelines`          | Required by repository Web Development Guidance before web edits and reviews | Requires fetching latest `command.md` rules and reviewing changed web files | Selected: loaded per repository web guidance |
| Skill               | `design-taste-frontend`          | Public landing/marketing pages only ("Not for dashboards or app screens") | Public-page art direction | Skipped: explicitly excluded for app screens by both skill description and repository instructions |
| Research specialist | `hve-core-all:rpi-researcher`    | General delegated research lane worker            | Writes bounded lane artifact under `.copilot-tracking/research/subagents/` | Skipped (inline preferred): target codebase scope is tightly coupled within `src/api` and UX docs, inspectable directly with lower latency and higher precision |
| Research specialist | `Housing Building Safety Lead` / `Neighbourhood Housing Officer` | Domain role-profile agents for eliciting company hypotheses | Role-bounded Q&A grounded in case study and company profile | Skipped: #227 scope is WCAG 2.2 engineering implementation against already-documented `safety.md`, `wcag-conformance-baseline.md`, and PRD contracts |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller brief, target routes (`#/role/building_safety_lead`, `#/role/repairs`), issue spec (`/tmp/issue-227.md`), validation tier, and commit instructions. | No interaction available or needed | Proceed in `balanced` posture and `convergence` mode across all three waves |
| Direction change | Cycle 1 Wave 2 & Wave 3 discovery of `#/role/...` route shorthand vs `#/screens?screen=...` canonical routes and legacy `<a href="#" onclick>` in `hazardJump` | N/A | Keep canonical `#/screens?screen=safety-lead` and `#/screens?screen=hazard-triage` intact while supporting `#/role/building_safety_lead` and `#/role/repairs` as permission-preserving hash aliases, and migrate `hazardJump` to `data-jump` delegation |
| Convergence      | Cycle 1 parent synthesis complete across all 3 waves        | N/A                       | Selected converged Option A; `Research disposition: executed`; `Planning Readiness: Ready` |

## Scope and Success Criteria

* Scope: `#/role/building_safety_lead` and `#/role/repairs` rendering, helpers, keyboard navigation, focus handling, textual state labels, non-colour status signals, styling, and unit/conformance tests in `src/api`.
* Assumptions:
  * Sibling UX WCAG work (such as #225 in commit `d6f863e34`, and any other role-screen WCAG PRs on this branch) established shared helpers like `screenJumpNav` or status badge patterns in `role-screens.js` — must verify actual current code rather than assuming.
  * Existing conformance tests in `src/api/tests/` enforce strict rules on markup, inline handlers, read-only controls, and SA-007 visibility — must inspect every relevant test file.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one converged recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Run `rpi-research` for GitHub issue #227 (`#/role/building_safety_lead`, `#/role/repairs`: WCAG 2.2 keyboard jump nav, text state labels, and non-colour status signals), reading `/tmp/issue-227.md` first and writing dated research under `.copilot-tracking/research/2026-11-15/`.
* Inferred research questions: Identify exact gaps between current `building_safety_lead` / `repairs` screens and the WCAG 2.2 baseline (#151) + sibling WCAG patterns (#225, etc.); verify delegated keyboard/click focus mechanics; verify status badge/pill textual prefixes and non-colour indicators across all badges, queue rows, holds, releases, and empty/fallback states; verify strict conformance and safety boundary tests.
* Caller constraints and non-goals: Focused validation tier (`mypy`, `ruff check .`, `ruff format --check .`, targeted `src/api` unit tests); commit locally with Copilot trailer; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Target `#/role/building_safety_lead` and `#/role/repairs` WCAG 2.2 keyboard jump nav, text state labels, and non-colour status signals under Focused validation tier | Caller intake prompt | Scopes code/test changes to safety and repairs role screens and shared helpers where needed without breaking sibling screens |
| exclude                                                  | Do not push to remote; do not weaken read-only hazard/clock/closure/authorisation boundaries, SA-007 non-hiding, or no-role-simulator rules | Caller intake prompt & `/tmp/issue-227.md` | Constrains implementation and contrarian alternatives |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status   |
|---:|------------------|------------------------------------------|-----------|----------|
| Q1 | What UX, regulatory-literacy, WCAG 2.2 (#151), Fluent 2 (#150), plain-language, and PRD contracts govern `#/role/building_safety_lead` and `#/role/repairs`? | breadth | H | answered |
| Q2 | How are `building_safety_lead` and `repairs` currently implemented in `role-screens.js`, `app.js`, `index.html`, and `styles.css`, and how do sibling WCAG-upgraded role screens (e.g., #225 finance/grants or others) implement jump nav, text state labels, and non-colour signals? | depth | H | answered |
| Q3 | Which badges, pills, referral states (`sent`, `received`, `accepted`, pending receipt), hold/release banners, tables/lists, landmarks, headings, and interactive elements on `building_safety_lead` and `repairs` lack explicit text state prefixes, non-colour visual cues, ARIA/table semantics, or keyboard jump/focus support? | depth | H | answered |
| Q4 | What existing unit, conformance, VDOM/JS harness, and accessibility baseline tests constrain `role-screens.js` (e.g. inline handlers, `screenPanel` counts/IDs, read-only rules, SA-007, link hashes, axe/baseline rules), and what could break if jump nav or text prefixes are added naively? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `/tmp/issue-227.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/research/sector/housing-association-primer.md`, `.copilot-tracking/rpi-sessions/2026-11-14/issue-225-c2-conformance-fix-state.json`.
* Reused (verified) findings: Issue #227 has 5/6 criteria checked; the open engineering criterion is WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation. Commit `d6f863e34` (#225) and commit `29c2e0755` (#228) confirmed that role-screen jump links converge on real `#...` anchor fragments with `data-jump` click delegation (`role-screens.js:268-275`) rather than dead `href="#"` inline `onclick` handlers.
* Superseded / stale: Earlier partial safety-screen commit `a1bfc1748` (#1680) left `hazardJump` on `<a href="#" onclick=...>` without `data-jump` delegation, omitted section `id` attributes on `hazardPanel`, left `hazardQueue.summary` without jump links or `Stop-work indicator:` pause labels, left multiple state cells without lead word-first state cues or `Object.hasOwn` prototype safety, left `.screen-links a` without non-colour underlines or 24px target height in `style.css`, and left `#/role/building_safety_lead` and `#/role/repairs` unrouted in `app.js`.

## Cycle 1 Execution

### Wave 1 — Wider (Standards, Contracts, and Surface Mapping)

* Executed inline across issue #227, UX standards, PRD contracts, and external Web Interface Guidelines:
  * `/tmp/issue-227.md` confirms five delivered acceptance criteria (referral queue awareness/source/destination/separate `sent`/`received`/`accepted` states; pending-receipt follow-up owner; scoped retrofit pause and release decision evidence; read-only authority boundary; Fluent 2 components with no role simulator) and one open criterion: "Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation."
  * `docs/reference/research/ux/wcag-conformance-baseline.md:21-98` (C1) establishes WCAG 2.2 Level AA as the engineering target, requiring non-colour state signals (1.4.1), programmatic headings/landmarks/tables (1.3.1), keyboard reachability and bypass/jump paths without traps (2.1.1, 2.4.1), visible two-tone focus indicators and unobscured focus (2.4.7, 2.4.11), and 24x24 CSS px minimum target size (2.5.8), while explicitly prohibiting claims of full WCAG conformance until manual assistive-technology validation (#155).
  * `docs/reference/research/ux/design-system.md:45-168` (C2) and `docs/reference/research/ux/content-standard.md:18-92` (C3) mandate Fluent 2 tokens, documented component classes only (`.card`, `.screen-record`, `.screen-links`, `.table-scroll`, `.empty`, `.blocked`, `.flag`, `.flag.danger`, `.btn`, `.alt`, `.row`), plain British English, and strict avoidance of banned internal vocabulary (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) in visible copy.
  * `docs/reference/research/ux/customer-journeys/safety.md:1-145` (C4) and `docs/reference/research/ux/screen-design-traceability.md:49-50` (C5) map #227 to registered screens `safety-lead` ("Building safety referral queue") and `hazard-triage` ("Repairs and hazard triage"), preserving SA-007 (never hiding or truncating hazard or safeguarding items past 50 rows) and read-only human-authority boundaries.
  * External Vercel Web Interface Guidelines (`command.md`, retrieved 2026-11-15, W1) require semantic `<a href="#...">` navigation links (never dead `href="#"`), `:focus-visible` outlines, `tabular-nums` for tabular comparisons, explicit `aria-label` on landmarks, and keyboard-operable scroll/section navigation.

### Wave 2 — Deeper (Implementation, Sibling Precedents, and Gap Audit)

* Inspected `src/api/src/zava_forward/api/web/role-screens.js`, `app.js`, `style.css`, and sibling WCAG commits (`d6f863e34`, `29c2e0755`, `8627074ca`, `5a350916d`):
  * **Target screens (`role-screens.js:965-1071`, C6)**: `safety-lead` (roles: `Building Safety Liaison`, `Retrofit Programme Manager`, `Programme Support Officer`) and `hazard-triage` (roles: `Retrofit Coordinator`, `Resident Liaison Officer`, `Quality Inspector`) share `hazardScreen(intro)` for selected-home evidence and `hazardQueue` (`summarise`/`summary`) for the cross-home queue when no home is selected.
  * **Gap 1 — Legacy `href="#"` + inline `onclick` in `hazardJump` and missing section `id` (`role-screens.js:998-1007`, C7)**:
    * `hazardJump` builds `<a href="#" onclick="...">Go to ${title}</a>` instead of pointing `href` to `#hazard-${key}-heading` and delegating via `"data-jump": "hazard-${key}-heading"` and `"data-jump-target": "hazard-${key}-heading"` to the shared click listener at `role-screens.js:268-275` (C8).
    * `hazardPanel` duplicates `screenPanel` (`role-screens.js:21-27`, C9) while omitting `id: "hazard-${key}"` on the `<section>` element. Using `screenPanel(title, { anchor: "hazard-" + key }, ...children)` supplies `section#hazard-${key}[aria-labelledby="hazard-${key}-heading"]` and `h2#hazard-${key}-heading[tabindex=-1]`.
    * `hazardQueue.summary` (`role-screens.js:1036-1057`, C6) currently has no keyboard jump navigation or anchored landmark when viewing the cross-home hazard summary (`!c`).
  * **Gap 2 — Direct hash route aliases `#/role/building_safety_lead` and `#/role/repairs` (`app.js:347-360,442`, C10; `role-screens.js:99-115`, C11)**:
    * Specialist screens canonically mount at `#/screens?screen=safety-lead` and `#/screens?screen=hazard-triage`. Navigating directly to `#/role/building_safety_lead` or `#/role/repairs` (with optional `?case=...&page=...`) currently skips loading `/role-screens.js` in `missingWorkspaceScripts` (`app.js:358`) and falls through `route()` (`app.js:442`) to `listView("mine")`.
    * Normalising/routing `#/role/building_safety_lead` -> `safety-lead` and `#/role/repairs` -> `hazard-triage` in `app.js` and `role-screens.js` resolves both direct hash routes while strictly enforcing `me.user.role` membership in `screen.roles` (rendering `"Screen unavailable"` for non-permitted roles and never switching or simulating roles).
  * **Gap 3 — Non-colour link styling, target size, and badge borders (`style.css:149-150,235,364-367`, C12)**:
    * Global `nav a` (`style.css:235`) sets `text-decoration: none; padding: .2rem .1rem;`. Inside `<nav class="screen-links">`, `.screen-links a` (`style.css:365`) overrides only `color: var(--brand-d)`, leaving jump links and specialist screen links distinguished by colour alone at rest (WCAG 1.4.1), leaving `aria-current="page"` (`text-decoration-thickness: .2em`) without an active underline line at rest, and leaving pointer height below the 24px (`1.5rem`) WCAG 2.5.8 minimum.
    * `.flag` and `.flag.danger` (`style.css:149-150`) have background fills without borders; adding `border: 1px solid var(--soft-line)` on `.flag` and `border-color: var(--warn)` on `.flag.danger` (alongside existing `.flag.danger:before` warning symbol at `style.css:329`) ensures non-colour and `forced-colors` boundary differentiation.
  * **Gap 4 — Incomplete word-first state cues and prototype safety across per-home and cross-home tables (`role-screens.js:965-1056`, C6)**:
    * Cross-home `pause(x)` (`role-screens.js:1037-1041`) emits bare `Active`, `Unknown`, or `Released...` instead of `Stop-work indicator: ...` with `Object.hasOwn`-safe status handling.
    * `hazardFollowUp(h)` (`role-screens.js:968-973`) omits lead word-first state prefixes (`Confirmed:` for accepted scope vs `Action needed:` for pending acceptance, pending receipt, unverified legacy referral, or unsent referral).
    * `hazardClock(h)` (`role-screens.js:975-982`) omits lead state prefixes (`Confirmed:`, `Action needed:`, `Waiting:`, `Unknown:`) and does not guard unparseable `responded_at` dates.
    * `hazardStep(stamp)` (`role-screens.js:965`) omits `State:` prefixes and renders `"Recorded Unknown"` when a non-empty timestamp string is unparseable instead of `"State: Unreadable timestamp (...)"`.
    * `hazardEscalationState(h)` (`role-screens.js:974`) does not classify recorded states via `Object.hasOwn` (`Confirmed` / `Waiting` / `Action needed` / `Unknown` paired with `Escalation state: ...`), which sibling screens (`test_assessor_screen_wcag.py:63`, `test_procurement_screen_wcag.py:92`) require so prototype keys like `constructor` are never treated as verified states.
    * Reported observation and urgency (`${screenValue(x.category)}, ${screenValue(x.priority)}`) relies on comma position rather than explicit `urgency: ${screenValue(x.priority)}`.
    * `hazardSafetyClock(h)` (`role-screens.js:966`) and cross-home sentinel rows (`Unavailable`, `Unknown`, `Mismatch` at `role-screens.js:1042-1046`) lack explicit `State:` / `Unknown:` / `Action needed:` prefixes, and both views lack a prose cue key stating that every state is written as words first so colour is never the only signal.

### Wave 3 — Contrarian (Counter-Evidence, Guardrail Traps, and Fragility Checks)

* Challenged each candidate change against existing static, unit, and browser checks to uncover hidden regressions before planning:
  1. **Contrarian check on `<th scope="row">` (`screenRecordTable` vs `screenTable`)**: Sibling resident screens use `screenRecordTable` (`rowHeader = true`), so we tested whether `hazardScreen` and `hazardQueue` should also switch column 0 from `<td>` to `<th scope="row">`. **Counter-evidence (`test_safety_screens.py:131-133`, C13)**: `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` explicitly asserts `all(t["attrs"] == {"scope": "col"} for t in heads)` and `len(find_all(row, "td")) == len(heads)` for every body row in both `tree` and `summary`. Switching to `<th scope="row">` would fail both assertions. Conclusion: retain `screenTable` (`<td>` body cells matching `<th>` column headers).
  2. **Contrarian check on refactoring shared `a[data-jump]` click delegation (`role-screens.js:268-275`)**: Tested refactoring `document.getElementById(link.getAttribute("data-jump"))?.focus()` into a local variable `const target = ...`. **Counter-evidence (`test_asset_exec_screen_wcag.py:67`, C14)**: `AssetExecScreenWcag.test_jump_links_do_not_navigate_the_hash_router` asserts the exact substring `"event.preventDefault();\n    document.getElementById"` in `role-screens.js`, and `test_finance_screens_wcag_225.py:94` mocks `focus()` without `scrollIntoView()`. Conclusion: keep `"event.preventDefault();\n    document.getElementById(link.getAttribute(\"data-jump\"))?.focus?.();"` on that exact line and chain optional `document.getElementById(link.getAttribute("data-jump"))?.scrollIntoView?.({ block: "start" });` immediately beneath it so both `test_asset_exec_screen_wcag.py`, `test_finance_screens_wcag_225.py`, and scroll-into-view expectations pass.
  3. **Contrarian check on `CopyAudit` banned terms (`test_content_standard.py:15-42`, C15)**: `CopyAudit.test_no_internal_terms_in_web_copy` scans every line of `role-screens.js` and `app.js` for `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` after stripping only exact `ALLOWED` substrings (`h.hold`, `x.hold`, etc.). Even an identifier like `holdCues` or a string mentioning `"Retrofit hold released"` in JS source would fail CI (as happened in historical commit `a1bfc1748` cycle 1). Conclusion: never introduce any banned term in JS identifiers, strings, or comments; use `pause` / `stop-work` / `restart` wording and match released states without writing the word `hold` in `role-screens.js`.
  4. **Contrarian check on substring contracts in `test_safety_screens.py` (C13), `test_safety_screen_wcag_keyboard.py` (C16), `safety_screens_browser_check.py` (C17), and `specialist_keyboard_browser_check.py` (C18)**:
     * `specialist_keyboard_browser_check.py:42-47` pins `EXPECTED_REGIONS["hazard-triage"] = ("Hazard referrals for this home", "Scoped pause and release evidence")` and `EXPECTED_REGIONS["safety-lead"] = ("Hazard referrals for this home", "Scoped pause and release evidence")` plus `HANDOFF_TEXT` and `ENDPOINT_TEXT`. Table captions MUST remain unchanged.
     * `test_safety_screens.py` and `safety_screens_browser_check.py` assert substrings `"Pending receipt. Follow-up owner:"`, `"Pending acceptance. Follow-up owner:"`, `"owns the accepted scope"`, `"Legacy referral with no recorded send time"`, `"No referral sent."`, `"Not recorded"`, `"Recorded"`, `"Active"`, `"Released. Release decision evidence: open the home"`, `"Unavailable. Open the home to check."`, `"Unknown. Hazard list not supplied"`, and `"Mismatch. The list flags a hazard"`. Prepending word-first state cues (`Confirmed: `, `Action needed: `, `Waiting: `, `Unknown: `, `State: `, `Stop-work indicator: `) preserves 100% of existing substring assertions while making every cell lead with explicit state words.
  5. **Contrarian check on `RoleScreenConformance` (`test_role_screens_conformance.py:65-102`, C19) and `RoleScreensGlobalScope` (`test_safety_screen_wcag_keyboard.py:103-107`, C16)**:
     * Zero `<button>`, `<form>`, `<input>`, `<select>`, or `<textarea>` elements may appear in `safety-lead` or `hazard-triage`.
     * Zero new CSS classes may be used unless defined in `style.css` AND documented in `design-system.md` (`test_safety_screens.py:276-288`, `test_design_system.py:86-93`). Reusing `.screen-links`, `.card`, `.screen-record`, `.table-scroll`, `.empty` avoids inventing undocumented classes.
     * Zero `.screen-*` CSS rules may include `animation` or `transition` (`test_role_screens_conformance.py:97-100`).
     * Zero top-level identifiers in `role-screens.js` may collide with `app.js`, and `app.js` changes must not alter `SCRIPT_RETRY_DELAYS` or `missingWorkspaceScripts` retry invariants (`checks/script_retry.py`, C20).

## Evidence Log

| ID  | Source / Location | Summary of verified evidence |
|-----|-------------------|------------------------------|
| C1  | `docs/reference/research/ux/wcag-conformance-baseline.md:21-98` | WCAG 2.2 AA target criteria (1.3.1, 1.4.1, 1.4.3, 1.4.11, 2.1.1, 2.4.1, 2.4.7, 2.4.11, 2.5.8, 4.1.2) and explicit rule that automated checks do not claim human AT conformance (#155). |
| C2  | `docs/reference/research/ux/design-system.md:45-168` | Fluent 2 token mapping, approved component inventory (`.screen-links`, `.screen-record`, `.table-scroll`, `.flag.danger`, etc.), and responsive widths (1280px, 768px, 360px, 320px). |
| C3  | `docs/reference/research/ux/content-standard.md:18-92` | Plain British English standard, banned internal jargon (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), and `Why it is blocked / Owner / Next action` structure. |
| C4  | `docs/reference/research/ux/customer-journeys/safety.md:1-145` | Building Safety Lead and Repairs/Hazard Triage journeys, SA-007 non-hiding requirement, separate `sent`/`received`/`accepted` states, and human-only pause release authority. |
| C5  | `docs/reference/research/ux/screen-design-traceability.md:49-50` | Traces issue #227 to `safety-lead` and `hazard-triage` screens and `test_safety_screens.py::SafetyScreens::test_roles_are_scoped`. |
| C6  | `src/api/src/zava_forward/api/web/role-screens.js:965-1071` | Current implementation of `hazardStep`, `hazardSafetyClock`, `hazardOwner`, `hazardFollowUp`, `hazardEscalationState`, `hazardClock`, `hazardHold`, `hazardScreen`, `hazardQueue`, and `registerRoleScreen` for `safety-lead` and `hazard-triage`. |
| C7  | `src/api/src/zava_forward/api/web/role-screens.js:998-1007` | Legacy `hazardPanel` (missing `<section id>`) and `hazardJump` (`href: "#"` with inline `onclick` instead of real `#hazard-...-heading` anchors and `data-jump` delegation). |
| C8  | `src/api/src/zava_forward/api/web/role-screens.js:268-275` | Shared document click listener intercepting `a[data-jump]` with `event.preventDefault()` and programmatic focus without triggering hash-router navigation. |
| C9  | `src/api/src/zava_forward/api/web/role-screens.js:21-32,838-842,1338-1344` | Shared `screenPanel` (`{ anchor }` option emitting `<section id aria-labelledby>` + `<h2 id tabindex=-1>`), `stateCue` (`Object.hasOwn`-safe prefix helper), `residentJumpNav`, and `procurementJumpNav`. |
| C10 | `src/api/src/zava_forward/api/web/app.js:347-360,425-465` | `missingWorkspaceScripts` and `route()` currently recognise `#/screens` for `roleScreensView()`, leaving `#/role/building_safety_lead` and `#/role/repairs` unhandled. |
| C11 | `src/api/src/zava_forward/api/web/role-screens.js:99-167` | `roleScreensView()` parses `?screen=...&case=...&page=...`, enforces `screen.roles.includes(me.user.role)`, updates `workspaceStatus`, and renders `overview` + `selected`. |
| C12 | `src/api/src/zava_forward/api/web/style.css:149-150,235,329,364-371` | `nav a` removes underline; `.screen-links a` sets only `color: var(--brand-d)` without underline or 24px (`1.5rem`) min-height; `.flag` / `.flag.danger` lack borders for forced-colors/non-colour boundaries. |
| C13 | `src/api/tests/test_safety_screens.py:119-301` | Pins `td` count == `th[scope=col]` count, SA-007 >50 rows, zero write controls, substring contracts across per-home and cross-home views, and CSS/design-system class membership. |
| C14 | `src/api/tests/test_asset_exec_screen_wcag.py:64-68` | Pins exact source substring `'closest?.("a[data-jump]")'` and `'event.preventDefault();\n    document.getElementById'` in `role-screens.js`. |
| C15 | `src/api/tests/test_content_standard.py:15-56` | `CopyAudit` bans `gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope` across all served JS/HTML lines except exact `ALLOWED` expressions. |
| C16 | `src/api/tests/test_safety_screen_wcag_keyboard.py:13-114` | Existing safety WCAG/keyboard tests plus `RoleScreensGlobalScope` top-level collision check and jump-focus test (currently invoking `.attrs.onclick` directly). |
| C17 | `src/api/checks/safety_screens_browser_check.py:19-135` | Browser and optional pinned axe-core 4.10.3 checks pinning `EXPECTED` and `QUEUE_EXPECTED` substrings, table region `aria-label`s, and zero write controls. |
| C18 | `src/api/checks/specialist_keyboard_browser_check.py:42-50` | Pins `EXPECTED_REGIONS["safety-lead"]` and `EXPECTED_REGIONS["hazard-triage"]` table captions (`"Hazard referrals for this home"`, `"Scoped pause and release evidence"`). |
| C19 | `src/api/tests/test_role_screens_conformance.py:58-120` | Enforces no role-simulator terms, documented CSS classes, native interactive controls, no inline styles/colours, and zero motion/transitions on `.screen-*` rules. |
| C20 | `src/api/checks/script_retry.py:21-90` | Pins `SCRIPT_RETRY_DELAYS`, `MEMO_RETURN`, and `STOP_ON_NON_ERROR` structure in `app.js`. |
| W1  | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (retrieved 2026-11-15) | Web Interface Guidelines requiring real `<a href="#...">` navigation targets (no dead `href="#"`), visible `:focus-visible` rings, semantic landmarks, and `tabular-nums` in tables. |

## Synthesis and Options Comparison

### Alternatives Evaluated

1. **Option A (Selected — Converged `data-jump` Landmarks, Complete Word-First State Labels, Non-Colour Link/Badge Styling, and Permission-Safe `#/role/...` Route Aliases)**:
   * Replace `hazardPanel` with `screenPanel(title, { anchor: "hazard-" + key }, ...)` and update `hazardJump` to render `<a href="#hazard-${key}-heading" data-jump="hazard-${key}-heading" data-jump-target="hazard-${key}-heading">Go to ${title}</a>` using the shared `a[data-jump]` click delegation (adding optional `scrollIntoView?.({ block: "start" })` while preserving the `test_asset_exec_screen_wcag.py:67` substring). Remove the obsolete `'h("a", { href: "#",' ` inline-onclick carve-out in `test_role_screens_conformance.py:78` if no `<a href="#">` inline handlers remain in `role-screens.js`.
   * Add keyboard section jump navigation and an anchored section landmark (`hazard-page-summary`) to `hazardQueue.summary` when viewing the cross-home summary with no home selected.
   * Standardize word-first, `Object.hasOwn`-safe textual state labels across both `hazardScreen` and `hazardQueue.summary` (`hazardStep`, `hazardSafetyClock`, `hazardFollowUp`, `hazardEscalationState`, `hazardClock`, `hazardHold`, cross-home `pause`, `urgency: ...`, and cross-home `Unavailable`/`Unknown`/`Mismatch` rows) plus explicit non-colour cue guidance sentences, while preserving every existing substring and banned-word (`CopyAudit`) contract.
   * Upgrade `.screen-links a` in `style.css` to keep persistent `text-decoration: underline`, `display: inline-flex; align-items: center; min-height: 1.5rem; padding: var(--sp-1) var(--sp-2)` (WCAG 1.4.1 & 2.5.8, zero motion), and add `1px solid` borders to `.flag` and `.flag.danger` for non-colour / `forced-colors` distinction.
   * Support `#/role/building_safety_lead` (-> `safety-lead`) and `#/role/repairs` (-> `hazard-triage`) hash route aliases in `app.js` and `role-screens.js` (preserving `?case=` and `?page=` query parameters and enforcing `me.user.role` permissions without any role simulator).
   * Update `test_safety_screen_wcag_keyboard.py` (testing delegated `a[data-jump]` clicks, prototype-key safety, corrupt timestamps, cross-home summary state labels and jump nav, non-colour `.screen-links a` / `.flag` CSS rules, and `#/role/building_safety_lead` & `#/role/repairs` route resolution).
2. **Option B (Rejected — Switch hazard tables to `screenRecordTable` with `<th scope="row">`)**:
   * Rejected because `test_safety_screens.py:131-133` (C13) explicitly asserts `all(t["attrs"] == {"scope": "col"} for t in heads)` and `len(find_all(row, "td")) == len(heads)`. Changing column 0 to `<th scope="row">` breaks established safety-table alignment tests without adding clarity beyond explicit `H-1` / `C-1 H-1` item labels.
3. **Option C (Rejected — Use `<button>` jump controls like `programme-queue`)**:
   * Rejected because `test_safety_screens.py:258,270` (C13), `test_safety_screen_wcag_keyboard.py:55` (C16), and `safety_screens_browser_check.py:72,118` (C17) strictly forbid `<button>` elements anywhere in `safety-lead` and `hazard-triage` to guarantee read-only presentation. Native `<a href="#...">` jump links satisfy both read-only invariants and Web Interface Guidelines (W1).

## Decisions, Risks, and Readiness

* **Confirmed / Parent-Synthesized Decisions**:
  * Use native `<a href="#hazard-${key}-heading" data-jump="hazard-${key}-heading" data-jump-target="hazard-${key}-heading">` jump links with shared `a[data-jump]` delegation and `screenPanel(..., { anchor })` landmarks on both per-home and cross-home views (C7, C8, C9, C14, W1).
  * Lead every state, clock, follow-up, referral timestamp, urgency, and stop-work cell in `hazardScreen` and `hazardQueue.summary` with plain-language state words (`Confirmed:`, `Waiting:`, `Action needed:`, `Unknown:`, `State:`, `Stop-work indicator:`) using `Object.hasOwn` lookups and zero banned `CopyAudit` words (C3, C6, C13, C15, C17).
  * Fix `.screen-links a` underline + `1.5rem` (24px) target height and `.flag` / `.flag.danger` borders in `style.css` without adding motion to `.screen-*` selectors (C1, C12, C19).
  * Route `#/role/building_safety_lead` and `#/role/repairs` to `safety-lead` and `hazard-triage` under existing `me.user.role` enforcement (C10, C11, C19).
  * Reference issue as `Refs #227` (not `Closes #227`) because manual assistive-technology and named safety-role human validation (#151, #155, #156) cannot be satisfied by automated engineering checks alone (C1, C5).
* **Residual Risks and Open Items**:
  * Automated VDOM, Node VM, and CSS token/contrast tests verify engineering structure, delegated keyboard/click focus, target-size rules, and textual state labels, but do not replace manual screen-reader/keyboard user validation tracked under #155.
  * No Cycle 2 is required under `balanced` posture because every research question (Q1–Q4) and contrarian check is backed by direct `path:line` evidence and no material uncertainty remains.
* **Research Disposition**: `executed`
* **Planning Readiness**: `Ready`

## Artifact Self-Check

* [x] Brief, parameters, extension registry, participation, scope, direction controls, questions, and prior-knowledge gate recorded
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order before synthesis
* [x] Every codebase claim cites a `C#` ID with `path:line` and external rules cite `W1` with URL and retrieval date
* [x] Converged recommendation and rejected alternatives documented with evidence-backed rationale
* [x] Research-only constraint honored (zero source or test files modified during `rpi-research`)
* [x] `Research disposition: executed` and `Planning Readiness: Ready` recorded


---
description: "Primary evidence artifact for Issue #159 conversational assistant panel keyboard operability, focus management, and screen-reader live-region verification"
---
<!-- markdownlint-disable-file -->

# Task Research: issue-159-assistant-a11y

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                 |
| Researcher / agent | rpi-research (RPI Agent)                                                   |
| Status             | Complete                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md |

## Research Brief

* What to research: Current implementation and test coverage of the workbench conversational assistant panel (`src/api/src/zava_forward/api/web/`) for keyboard operability, focus management, and screen-reader live-region (`aria-live="polite"`, `role="status"`, `role="log"`) message announcement, plus how `docs/reference/research/ux/` records assistive-technology / screen-reader and keyboard verification and distinguishes automated/emulated evidence from human AT sign-off.
* Why it matters: GitHub Issue #159 (`Conversational assistant experience in the workbench`) has one remaining unticked acceptance criterion (`Panel is keyboard operable, screen-reader tested, and announces new messages`). Delivering and proving the executable/verification slice requires grounded evidence of existing DOM/JS behavior, browser/accessibility test harnesses, counted guard tests, and UX knowledge-base conventions.
* Audience or intended use: Downstream `rpi-plan`, `rpi-implement`, and `rpi-review` phases delivering `src/api/tests/test_assistant_panel_a11y_159.py`, any minimal isolated web fix if needed, and the UX verification record in `docs/reference/research/ux/`.
* Scope: `src/api/src/zava_forward/api/web/` (chat/assistant/widget/index/CSS modules), `src/api/tests/` and `src/api/checks/` (assistant, chat, accessibility baseline, content standard, AT record checks), `docs/reference/research/ux/` (`wcag-conformance-baseline.md`, `content-standard.md`, `design-system.md`, and related AT/chat records), `docs/reference/README.md`, `docs/reference/log.md`, and prior `.copilot-tracking/` artifacts for Issue #159.
* Non-goals: Pushing to remote, altering `role-screens.js` or `panels.js` unless strictly required and minimal, claiming human assistive-technology sign-off without human execution if repository policy separates automated/headless AT-tree/live-region verification from named human AT testing, or changing AI provider/tokenomics logic.
* Criteria: Every codebase claim carries a `C#` ID with `path:line`; external guidelines/references carry `W#` IDs with URL and retrieval date; three waves (Wider, Deeper, Contrarian) complete before synthesis.
* Requested outputs: Converged recommendation for `src/api/tests/test_assistant_panel_a11y_159.py`, minimal web edit determination, and `docs/reference/research/ux/` verification documentation.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                               |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How does the workbench conversational assistant implement keyboard operability, focus management, and screen-reader live announcements, what gaps (if any) exist, how do existing tests/checks validate them, and how should verification be recorded in `docs/reference/research/ux/`? |
| Codebase scope                   | `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `src/api/checks/`, `docs/reference/research/ux/`, `docs/reference/`          |
| External scope                   | Web Interface Guidelines (`vercel-labs/web-interface-guidelines`) when web files are reviewed or touched                            |
| Initial internal candidate areas | `chat.js`, `chat-widget.js`, `assistants.js`, `index.html`, `chat-widget.css`, `style.css`, `test_chat_panel.py`, `test_chat_widget_focus.py`, `test_alert_chat_keyboard_live.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `wcag-conformance-baseline.md` |
| Initial external candidate areas | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                            |
| Research posture                 | focused                                                                                                                             |
| Posture provenance               | caller-specified (bounded internal task with named target paths, test module, and Focused validation tier)                          |
| Explicit limits / deadline       | Avoid edits to `role-screens.js` / `panels.js` if already satisfied (or keep minimal/isolated); do not push                         |
| Posture-specific completion basis| focused scope and materiality: all target assistant web modules, existing chat/a11y tests, counted baseline guards, and UX record conventions verified |
| Edits allowed during research?   | no, research-only                                                                                                                   |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Respect AMA evidence honesty rules (do not conflate automated browser/ARIA/Playwright/CDP accessibility-tree or live-region checks with human AT user sign-off where baseline docs distinguish them); preserve `test_accessibility_baseline.py` and `test_content_standard.py` invariants |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                            | Scoped authority or output contract                                          | Selected / skipped reason                                                       |
|---------------------|---------------------------------------|-----------------------------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` repository-wide AMA instructions                | Enforces Focused validation tier, UX/WCAG/content standards, KB log rules    | Selected: governs web, UX, KB, git, and evidence boundaries                     |
| Skill               | `rpi-research`                        | Phase skill for Research                                        | Owns three-wave primary research artifact and readiness contract             | Selected: active RPI phase skill                                                |
| Skill               | `accessibility`                       | Matches WCAG 2.2, ARIA APG, live-region, and keyboard scope     | Supplies WCAG 2.2 / ARIA APG live-region, dialog/disclosure, keyboard rules  | Selected: directly informs criterion 6 verification                             |
| Skill               | `web-design-guidelines`               | Required by AMA Web Development Guidance before web edits/review| Supplies external UI/a11y review checklist (`file:line` audit)               | Selected: loaded and fetched in case web edits or UI review apply               |
| Skill               | `redesign-existing-projects`          | Existing-app visual redesign skill                              | Governs visual redesigns                                                     | Skipped: no visual redesign requested; task is a11y verification and minimal fix|
| Research specialist | `hve-core-all:rpi-researcher`         | General delegated research lane worker                          | Writes lane evidence under `.copilot-tracking/research/subagents/`           | Skipped (inline): tightly coupled, bounded set of local files (<15 direct reads)|

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                           |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller prompt specifying Issue #159 criterion 6, target files, and commands. | N/A (non-interactive)| Proceed in `focused` posture with convergence output mode; no intake prompt needed.       |
| Direction change | None at intake.                                                                                                        | N/A                  | Retain caller boundaries (prefer test + UX doc only if web panel already satisfies rules).|
| Convergence      | Cycle 1 answered Q1-Q4 with contrarian verification; zero web JS/CSS defects found, so no user fork is needed. | N/A (converged)      | Deliver `src/api/tests/test_assistant_panel_a11y_159.py` (Node VM + headless Chromium CDP AXTree/live-region/keyboard checks) + `docs/reference/research/ux/wcag-conformance-baseline.md` & `docs/reference/log.md` updates without touching `role-screens.js`, `panels.js`, `chat.js`, or `chat-widget.js`. |

## Scope and Success Criteria

* Scope: Workbench conversational assistant UI (`src/api/src/zava_forward/api/web/`), assistant/chat/accessibility tests (`src/api/tests/`, `src/api/checks/`), and UX accessibility verification documentation (`docs/reference/research/ux/`, `docs/reference/README.md`, `docs/reference/log.md`).
* Assumptions:
  * The workbench conversational assistant lives in `chat.js` / `chat-widget.js` / `assistants.js` / `index.html` (to be verified in Wave 1).
  * Headless Chromium / Playwright or DOM harnesses may already exist in `src/api/checks/` and `src/api/tests/` (to be verified in Wave 1 & 2).
* Success criteria:
  * Every research question is answered with `path:line` `C#` evidence.
  * Exact DOM roles, `aria-live` / `role="status"` / `role="log"` attributes, keyboard handlers, and focus transitions of the conversational assistant panel are mapped.
  * Any bug or accessibility gap in the panel (if present) vs already-satisfied behavior is proven with contrarian checks.
  * Baseline guard tests (`test_accessibility_baseline.py`, `test_content_standard.py`, `test_ux_design_traceability.py`, etc.) are checked so new tests/docs do not break invariants.

## Task Research Requests

* Explicit requests:
  * Inspect conversational assistant panel in `src/api/src/zava_forward/api/web/` and existing assistant tests in `src/api/tests/`.
  * Determine whether web files already satisfy keyboard operability, live-region message announcement, and focus management (avoiding edits to `role-screens.js` / `panels.js` if satisfied, or keeping any edit minimal and isolated).
  * Design `src/api/tests/test_assistant_panel_a11y_159.py` and UX verification documentation under `docs/reference/research/ux/`.
* Inferred research questions:
  * How do existing browser/accessibility tests in `src/api/tests/` (such as `test_chat_panel.py`, `test_chat_widget_focus.py`, `test_alert_chat_keyboard_live.py`, `test_regulatory_at_record_check.py`) run under `python3 -m unittest`?
  * How does `docs/reference/research/ux/wcag-conformance-baseline.md` (and any companion UX doc) record Issue #159 conversational assistant keyboard and screen-reader verification, and how is automated screen-reader/accessibility-tree/live-region testing framed truthfully under repository rules?
* Caller constraints and non-goals: Focused validation tier; commit locally with Copilot trailer; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Avoid edits to `role-screens.js` / `panels.js` if already satisfied, or keep any edit minimal/isolated  | Caller prompt       | Wave 2 & 3 verify whether existing web panel already satisfies all a11y criteria   |
| exclude                                                  | Do not push branch to remote                                                                            | Caller prompt       | Local commit only after verification and RPI review                                |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type            | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | Which web files implement the Issue #159 workbench conversational assistant panel, and what are its exact DOM landmarks, ARIA live regions, keyboard bindings, and focus transitions? | depth           | H        | answered |
| Q2 | What do existing assistant/chat/accessibility tests and browser checks in `src/api/tests/` and `src/api/checks/` already verify, and what headless/DOM harness do they use? | breadth         | H        | answered |
| Q3 | Do any keyboard, focus-management, or live-region announcement gaps remain in the conversational assistant panel (including error/fallback/empty/multi-turn/toggle states)? | depth           | H        | answered |
| Q4 | How do `docs/reference/research/ux/` documents and guard tests (`test_accessibility_baseline.py`, `test_content_standard.py`, etc.) structure and enforce screen-reader and keyboard verification records? | straightforward | H        | answered |

## Cycle 1 — Three-Wave Execution Log

### Wave 1 — Wider (Inline Breadth Inspection)

* Scope covered: `src/api/src/zava_forward/api/web/` (`index.html`, `chat-widget.js`, `chat.js`, `assistants.js`, `chat-widget.css`, `app.js`), `src/api/tests/` (`test_chat_*.py`, `test_assistant*.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_epic149_ux_evidence_results.py`, `test_screen_design_traceability.py`, `test_production_ux_acceptance_protocol.py`), `src/api/checks/` (`employee_chat_browser_check.py`, `chat_widget_browser_check.py`), and `docs/reference/research/ux/` (`wcag-conformance-baseline.md`, `production-ux-acceptance-protocol.md`, `screen-design-traceability.md`, `design-system.md`).
* Inline disposition: Tightly coupled internal surface (<15 direct file reads); inline execution preserved cross-file line invariants without worker serialization overhead.
* Breadth findings:
  * The Issue #159 workbench conversational assistant experience consists of two linked surfaces: (a) the persistent/dockable `Employee assistant` dialog (`employeeChat` in `chat.js` backed by `ChatWidget.create` in `chat-widget.js` and `#employee-chat-launcher` in `index.html`) and (b) the optional in-case assistant disclosure (`chatCasePanel(id)` in `chat.js`, mounted on the `"AI assistance"` tab `#case-panel-ai` in `app.js`, which opens `employeeChat`, dispatches `Request proposal: ...` actions to independent review, and embeds `#regulatory-chat`).
  * Existing chat tests cover backend isolation, tokenomics, static regex source assertions (`test_home_chat_regulatory_keyboard_provenance.py`), Node-VM focus-lifecycle checks (`test_chat_widget_focus.py`), and an opt-in `ZF_BROWSER_TESTS=1` partial browser test in `test_chat_panel.py`.

### Wave 2 — Deeper (DOM, ARIA Live-Region, Keyboard, and Focus Contract)

* Prioritized deep inspection of `chat-widget.js`, `chat.js`, `index.html`, `chat-widget.css`, `wcag-conformance-baseline.md`, and `src/api/pyproject.toml`:
  * Launcher & dialog semantics (`C1`, `C2`): `#employee-chat-launcher` (`<button type="button" aria-label="Chat" hidden>`) is decorated with `aria-haspopup="dialog"`, `aria-expanded="false"|"true"`, and `aria-controls="employee-chat"`. `#employee-chat` is `<section id="employee-chat" role="dialog" aria-labelledby="employee-chat-title">` with `<h2 id="employee-chat-title" tabindex="-1">Employee assistant</h2>` and `<button type="button" class="chat-widget-close">Close chat</button>`.
  * Live regions (`C2`, `C3`, `C4`):
    1. Conversation log: `<div class="chat-widget-log" role="log" aria-live="polite" aria-relevant="additions" aria-label="Employee assistant conversation" tabindex="0">` — keyboard-reachable (`tabindex="0"`) and appends `<article class="chat-widget-message chat-widget-user|chat-widget-assistant">` nodes carrying speaker (`You` / `Assistant`), persistent non-colour `Outcome: <answer|withheld|refused|workflow-only help>`, source-of-answer attribution label, reply paragraph, usage/skill detail, and keyboard-operable `<details><summary>Sources (N)</summary>...</details>`.
    2. Turn status region: `<p role="status" aria-live="polite" aria-atomic="true" class="chat-widget-status">` — announces `"Loading skills."`, `"Choose a skill or ask a general work question."`, `"Asking the assistant."`, and outcome-specific completion messages via `statusFor(kind)` (`"Answer added. Check the sources before relying on it."`, `"Reply withheld. Check the case card for recorded facts."`, `"Request refused. A person must take that action in the workflow."`, `"Workflow-only help added. No assistant answer was given. Check the case card for recorded facts."`).
    3. Error alert region: `<p id="employee-chat-error" role="alert" aria-live="polite" aria-atomic="true" class="chat-widget-error" tabindex="-1">` — linked to `#employee-chat-question` via `aria-describedby` (`"employee-chat-entry-warning chat-privacy employee-chat-error"` plus `"chat-demo-disclaimer"` when demo mode is active), unhidden and populated on blank submit (`"Type a question first."`) or transport/API failure (`"Chat unavailable: ... Owner: application support. Next action: ..."`).
    4. In-case `#chat-panel` status & workspace status (`C1`, `C4`): `chatCasePanel(id)` maintains `<p role="status">` announcing `"Requesting a proposal for independent review."` -> `"Proposal requested. Find it in the proposals panel and the review queue."` (or role-denied / failure note with `Owner:` and `Next action:`), while `deny()` on `401`/`403`/`404` announces `"Chat access ended. Reopen from a record you can see, or sign in again."` in `#workspace-status` (`role="status" aria-live="polite" aria-atomic="true"`).
  * Keyboard operability & focus management (`C2`, `C3`):
    * `open()` unhides `#employee-chat`, sets `aria-expanded="true"`, syncs dock visibility, and focuses `#employee-chat-title`.
    * `hide(returnFocus = true)` (invoked by `Close chat` button and `Escape` `keydown` handler) hides `#employee-chat`, unhides `#employee-chat-launcher` BEFORE calling `launcher.focus()` (preventing hidden-launcher focus failure when docked), and sets `aria-expanded="false"`.
    * Composer `<textarea id="employee-chat-question">`: `Enter` without `Shift` (when `!event.isComposing && event.keyCode !== 229` and `!send.disabled`) calls `form.requestSubmit()`; `Shift+Enter` preserves multi-line editing without submitting.
    * `busy(true)` moves focus from `send` to `input` BEFORE setting `send.disabled = true` (`if (value && document.activeElement === send && !root.hidden) input.focus();`), sets `form.setAttribute("aria-busy", "true"|"false")`, and never drops focus to `document.body`.
    * `stayOpen: true` + `externalFocus` / `revealBeside` preserves non-modal case comparison when focus leaves `#employee-chat` and scrolls obscured focused elements clear of the floating or docked panel (WCAG 2.4.11).
    * Size/dock controls (`Chat size` `<details>`): native `<button aria-pressed="false|true">Dock to right edge</button>` and labeled `<input type="range">` width/height sliders work via keyboard `Enter`/`Space` and arrow keys while disabling the height slider when docked.
    * Session/access loss (`deny()`): checks `ui.root.contains(document.activeElement)` before disposal and moves focus to `#app` (`<main id="app" tabindex="-1">`) so focus is never lost.

### Wave 3 — Contrarian (Edge-Case, Guidelines, CI, and Guard Verification)

* Challenged whether any subtle defect required modifying `chat.js`, `chat-widget.js`, `role-screens.js`, or `panels.js`, and checked how CI executes `src/api/tests`:
  1. Checked `chat.js` and `chat-widget.js` against the freshly fetched Vercel Web Interface Guidelines (`W1`) and W3C WCAG 2.2 / ARIA APG Dialog, Disclosure, and Live Region patterns (`W2`, `W3`): all interactive controls are native `<button>`, `<summary>`, `<textarea>`, `<select>`, and `<input type="range">` with programmatic labels, `autocomplete="off"`, explicit error `Owner:` / `Next action:` text, `:focus-visible` two-tone rings (`C6`), `prefers-reduced-motion` zeroed transitions (`C5`), and polite live-region announcements without focus theft.
  2. Checked whether changing `hide()` or `status` markup in `chat-widget.js` / `chat.js` was warranted: `test_home_chat_regulatory_keyboard_provenance.py` (`C9`) explicitly pins exact substrings in `chat-widget.js` (`if (returnFocus && active) launcher.focus()`, `role: "log", "aria-live": "polite"`, `tabindex: "0"`) and `chat.js` (`const status = h("p", { role: "status" });`), and `test_accessibility_baseline.py` (`C10`) pins exact repository-wide counts (`9` `aria-invalid` sites, `2` `position:fixed` rules, `14` script-built tables) while `test_content_standard.py` (`C11`) bans internal terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) across `web/*.js` and `web/*.html`. Because the conversational assistant panel already satisfies all keyboard, live-region, and focus-management criteria cleanly, **zero edits to `web/*.js` or `web/*.css` are needed**, eliminating regression risk on `role-screens.js`, `panels.js`, and pinned source guards.
  3. Checked `.github/workflows/src-ci.yml` (`C13`) and `src/api/pyproject.toml` (`C14`) for CI test execution hazards:
     * In `src-ci.yml`, `python -m unittest discover -s tests -v` runs BEFORE `python -m playwright install --with-deps chromium`, AND `ruff check . && ruff format --check .` + `mypy` (`strict = true` on `tests/`) run immediately after!
     * On this machine, Playwright 1.64.0 and headless Chromium `156.0.8078.4` are already installed and functional, whereas no desktop screen reader (`orca`, `espeak`, `spd-say`, NVDA, VoiceOver) is installed (`C12`).
     * Therefore, `src/api/tests/test_assistant_panel_a11y_159.py` must:
       1. Always execute deterministic **Node `vm` + live Python `ChatPanel`/`App` integration tests** during standard `unittest` discovery (zero browser binary dependency, <0.5s runtime) proving full keyboard operability, dynamic `aria-live="polite"` / `role="status"` / `role="log"` / `role="alert"` message-announcement transitions across all outcomes, and focus-management invariants; AND
       2. Execute **live headless Chromium Playwright + CDP `Accessibility.getFullAXTree` + `MutationObserver` live-region & real keyboard traversal tests** whenever Playwright and the Chromium binary are installed (skipping cleanly via `skipTest` ONLY when `playwright` or the Chromium executable is absent in the pre-browser CI step, matching `test_chat_widget_layout.py`, `C8`, while noting `test_epic149_ux_evidence_results.py` checks `skipTest` only on modules listed in its `SURFACES` dict).
       3. Conform strictly to `ruff check`, `ruff format --check` (`line-length = 100`), and `mypy --strict`.
  4. Checked UX documentation guards (`C10`, `C12`, `test_production_ux_acceptance_protocol.py`, `test_epic149_ux_evidence_results.py`):
     * `production-ux-acceptance-protocol.md` human-record tables MUST keep `"Not run"` unless a named human tester and date exist; never fabricate human tester entries.
     * `wcag-conformance-baseline.md` MUST preserve `"WCAG 2.2"`, `"pending owner confirmation"`, `"we do not claim conformance"`, `"Automated checks are not conformance evidence"`, and the role names, and MUST NOT claim `"fully conforms"` or `"is WCAG 2.2 AA compliant"`.
     * Recording the dated (`2026-11-15`) Issue #159 conversational assistant keyboard, focus-management, CDP Accessibility Tree, and live-region announcement verification in `docs/reference/research/ux/wcag-conformance-baseline.md` (with matching index refresh in `docs/reference/README.md` and append-only entry in `docs/reference/log.md`) satisfies both the caller's instruction and AMA evidence-honesty rules by explicitly distinguishing rendered Chromium accessibility-tree + live-region + keyboard engineering verification on synthetic data from named human desktop NVDA/VoiceOver sessions (#151, #155, #619).

### Parent Synthesis & Re-entry Decision

* All four research questions (`Q1`-`Q4`) are answered with verified `path:line` codebase citations (`C1`-`C14`) and external standard/guideline citations (`W1`-`W3`).
* Contrarian checks confirmed zero web implementation defects and uncovered two critical engineering constraints (`src-ci.yml` pre-Chromium unit-test ordering + `ruff format --check` / `mypy --strict`, and UX guard assertions on `wcag-conformance-baseline.md`).
* No unresolved material uncertainty remains; a second research cycle would be redundant under the `focused` posture.
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`

## Evidence Log

### Codebase Evidence (`C#`)

| ID  | Location                                                                 | Verified fact                                                                                                                                                             |
|-----|--------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `src/api/src/zava_forward/api/web/index.html:43-46`                      | Workbench shell defines `<p id="workspace-status" role="status" aria-live="polite" aria-atomic="true">`, `<main id="app" tabindex="-1">`, and `<button id="employee-chat-launcher" type="button" aria-label="Chat" hidden>`. |
| C2  | `src/api/src/zava_forward/api/web/chat-widget.js:27-237`                 | `ChatWidget.create` builds `section[role="dialog"][aria-labelledby]`, `h2[tabindex="-1"]`, `div[role="log"][aria-live="polite"][aria-relevant="additions"][tabindex="0"]`, `p[role="status"][aria-live="polite"][aria-atomic="true"]`, `p[role="alert"][aria-live="polite"][aria-atomic="true"]`, `Enter`/`Shift+Enter` IME-safe keydown, `Escape` / `Close chat` focus-returning `hide()`, `busy()` focus retention before `send.disabled = true`, `Chat size` dock/range controls, and `revealBeside` unobscured focus handling. |
| C3  | `src/api/src/zava_forward/api/web/chat.js:20-232`                        | `employeeChat` wires role gating, `statusFor(kind)` (`answer`, `withheld`/`abstain`, `refused`, `fallback`), persistent `Outcome:` text and `attribution(answer)` labels, `aria-describedby` (`employee-chat-entry-warning`, `chat-privacy`, `employee-chat-error`, optional `chat-demo-disclaimer`), blank-input `ui.fail("Type a question first.")` + `ui.focusInput()`, and `deny()` focus handoff to `#app` with `#workspace-status` announcement. |
| C4  | `src/api/src/zava_forward/api/web/chat.js:237-272`                       | `chatCasePanel(id)` renders `<details class="card" id="chat-panel">` with `<summary>Ask the assistant about this case (optional)</summary>`, `"Open chat"` `<button type="button">`, `"Request proposal: ..."` buttons, polite `<p role="status">` transition messages, and nested `regulatoryChatPanel(id)` (`#regulatory-chat`). |
| C5  | `src/api/src/zava_forward/api/web/chat-widget.css:1-95`                  | Scopes the two repository-approved `position:fixed` rules (`#employee-chat-launcher` and `#employee-chat`), sticky composer tools, responsive/docked sizing, and `@media (prefers-reduced-motion: reduce)` transition suppression. |
| C6  | `src/api/src/zava_forward/api/web/app.js:1186-1205`                      | Mounts `chatCasePanel(id)` inside the `"AI assistance"` tab panel (`#case-panel-ai`) of `caseView`. |
| C7  | `src/api/tests/test_chat_widget_focus.py:1-95`                           | Executes `chat-widget.js` and `chat.js` inside Node `vm` to test focus transitions during async admission, busy states, and route/session teardown. |
| C8  | `src/api/tests/test_chat_widget_layout.py:21-47`                         | Demonstrates the CI-safe Playwright pattern inside `src/api/tests/`: runs real Chromium when installed and skips cleanly only when `playwright` or the Chromium executable is absent in the pre-browser unit-test step. |
| C9  | `src/api/tests/test_home_chat_regulatory_keyboard_provenance.py:50-125`  | Pins exact source substrings in `chat-widget.js` and `chat.js` for `hide()`, `open()`, `Enter` without `Shift`, live-region attributes, `busy()` focus guard, and source attribution cues. |
| C10 | `src/api/tests/test_accessibility_baseline.py:85-182`                    | Enforces `9` `aria-invalid` sites, `2` `position:fixed` rules, `14` script-built tables, two-tone `:focus-visible`, and required non-conformance wording in `wcag-conformance-baseline.md`. |
| C11 | `src/api/tests/test_content_standard.py:1-120`                           | Audits every served `web/*.js` and `web/*.html` file against banned internal terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), exact AI suggestion labelling, and `Owner:` / `Next action:` guidance. |
| C12 | `docs/reference/research/ux/wcag-conformance-baseline.md:45-295`         | Canonical workbench WCAG 2.2 audit and check coverage record; documents headless Linux host limits (Playwright Chromium available, no NVDA/VoiceOver/Orca/audio hardware) and requires separating automated engineering verification from human assistive-technology acceptance (#151, #155, #619). |
| C13 | `.github/workflows/src-ci.yml:78-115`                                    | Runs `python -m unittest discover -s tests -v`, `ruff check . && ruff format --check .`, and `mypy` before installing Chromium for browser checks. |
| C14 | `src/api/pyproject.toml:27-75`                                           | Enforces `ruff` (`line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`, format check) and `mypy` (`strict = true` across `src`, `tests`, `checks`) for all new test modules not on the legacy ignore list. |

### External Evidence (`W#`)

| ID | Source                                                                                   | Retrieved / Referenced | Key applicable rule                                                                                                                                          |
|----|------------------------------------------------------------------------------------------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| W1 | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` | 2026-11-15             | Native `<button>`/`<label>`/`aria-label`, `:focus-visible` outlines, `aria-live="polite"` for async updates/validation, `autocomplete="off"`, unobscured focus, `prefers-reduced-motion`, and actionable error copy. |
| W2 | `https://www.w3.org/TR/WCAG22/` (via `accessibility` skill `wcag-22.md`)                 | 2026-11-15             | SC 2.1.1 Keyboard, SC 2.1.2 No Keyboard Trap, SC 2.4.3 Focus Order, SC 2.4.7 Focus Visible, SC 2.4.11 Focus Not Obscured (Minimum), SC 3.3.1 Error Identification, SC 4.1.2 Name, Role, Value, SC 4.1.3 Status Messages. |
| W3 | `https://www.w3.org/WAI/ARIA/apg/` (via `accessibility` skill `aria-apg.md`)             | 2026-11-15             | Dialog (`role="dialog"`, `aria-labelledby`, `Escape` dismiss returning focus), Disclosure (`<details>`/`<summary>`, `aria-expanded`), and Notification Live Regions (`role="log"`, `role="status"`, `role="alert"`). |

## Converged Recommendation and Alternatives

### Selected Recommendation

1. **Keep `web/*.js`, `web/*.css`, and `web/*.html` unchanged** (zero edits to `role-screens.js`, `panels.js`, `chat.js`, or `chat-widget.js`), because Wave 2 and Wave 3 proved the conversational assistant panel (`#employee-chat`, `#employee-chat-launcher`, and `#chat-panel`) already satisfies keyboard operability, focus management, and polite screen-reader live-region announcements while preserving all pinned guard counts.
2. **Add `src/api/tests/test_assistant_panel_a11y_159.py`** (`mypy --strict` and `ruff` clean) with two complementary verification layers:
   * **Layer A — Always-on Node `vm` + Real Python `ChatPanel` Integration Suite**: Runs unconditionally in every `unittest` run (<0.5s, zero browser binary dependency) against the real `chat-widget.js`, `chat.js`, and backend `ChatPanel` / `ChatIsolation` responses (`answer`, `withheld`, `refused`, `fallback` workflow-only help, blank-question validation, transport failure, `#chat-panel` `Open chat` + `Request proposal` status announcements, `Enter` vs `Shift+Enter` vs IME composition `isComposing`/`229`, `Send`-focused `busy(true)` focus preservation, `Dock to right edge` + `Escape`/`Close chat` focus return, stay-open `revealBeside` unobscured scroll, and `401`/`403` `deny()` focus handoff to `#app` + `#workspace-status`).
   * **Layer B — Rendered Headless Chromium Playwright + CDP Accessibility Tree (`Accessibility.getFullAXTree`) + Live-Region `MutationObserver` Suite**: Serves the real workbench (`App` + `Store` on `127.0.0.1:0` with synthetic data, skipping cleanly only if Playwright or the Chromium binary is absent in a pre-browser CI step) and executes keyboard-only navigation (`Enter`, `Space`, `Tab`, `Shift+Tab`, `Shift+Enter`, `ArrowRight`, `Escape`) from both `#employee-chat-launcher` and `#case-panel-ai`'s `#chat-panel` (`summary` -> `Open chat` / `Request proposal`), inspects the browser's computed CDP Accessibility Tree (`dialog`, `log`, `status`, `alert`, `button`, `textbox`, `combobox`, `slider`, accessible names, `live="polite"`, `atomic`, `relevant`, `expanded`, `pressed`, `busy`, `describedby`), and captures real DOM live-region mutation announcements across user prompt submission, cited answer, refusal, blank-input alert, transport alert, and proposal request without focus loss or console/page errors.
3. **Record the verification in `docs/reference/research/ux/wcag-conformance-baseline.md`** (plus refresh the index description in `docs/reference/README.md` and append an entry to `docs/reference/log.md`), documenting the exact `2026-11-15` Issue #159 keyboard, focus-management, CDP Accessibility Tree, and live-region announcement checks while explicitly preserving the repository's non-conformance and human desktop NVDA/VoiceOver boundary (#151, #155, #619).

### Alternatives Considered and Rejected

* **Alternative A — Edit `chat-widget.js` or `chat.js` to add redundant ARIA attributes**: Rejected because `#employee-chat`'s `log`, `status`, and `error` elements already carry explicit `role="log" aria-live="polite" aria-relevant="additions"`, `role="status" aria-live="polite" aria-atomic="true"`, and `role="alert" aria-live="polite" aria-atomic="true"`, and `test_home_chat_regulatory_keyboard_provenance.py` pins exact source snippets in both files (`C9`).
* **Alternative B — Gate all new Issue #159 tests behind `ZF_BROWSER_TESTS=1`**: Rejected because the caller's Focused validation command (`python3 -m unittest src/api/tests/test_assistant_panel_a11y_159.py ... -q`) does not set `ZF_BROWSER_TESTS=1`; gating the entire module behind `ZF_BROWSER_TESTS=1` would skip the tests during the required validation run! Combining unconditional Node `vm` + backend integration tests with automatic Chromium execution when the Chromium binary is installed (as on this host) ensures full execution under the exact caller command while remaining safe in pre-Chromium CI steps (`C8`, `C13`).
* **Alternative C — Populate `Not run` cells in `production-ux-acceptance-protocol.md` or `Manual check record` with automated Chromium results**: Rejected because `test_production_ux_acceptance_protocol.py` and `test_epic149_ux_evidence_results.py` enforce that those human-owned record cells remain `"Not run"` until a named human assistive-technology tester runs NVDA/Firefox and VoiceOver/Safari (`C12`).

## Risks, Constraints, and Further Research

* **Strict typing & formatting**: `src/api/pyproject.toml` runs `mypy` in `strict = true` mode and `ruff check` + `ruff format --check` (`line-length = 100`) over `tests/`. All helpers in `test_assistant_panel_a11y_159.py` must carry explicit type annotations and clean formatting (`C14`).
* **Open human gate (separate follow-up / owner boundary)**: Named human desktop screen-reader sessions (NVDA with Firefox on Windows, VoiceOver with Safari on macOS) under `#151`, `#155`, and `#619` remain human-owned external activities that cannot be fabricated on a headless Linux host (`C12`).

## Handoff Summary

* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Active decisions**: Zero web source edits; create `src/api/tests/test_assistant_panel_a11y_159.py` (Node VM + live `ChatPanel` + headless Chromium Playwright/CDP AXTree/live-region/keyboard verification); document verification truthfully in `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
* **Evidence IDs**: `C1`-`C14`, `W1`-`W3`.
* **Blockers**: None for automated engineering delivery and Focused-tier validation; named human NVDA/VoiceOver sign-off (#151/#155/#619) remains explicitly distinguished in documentation.

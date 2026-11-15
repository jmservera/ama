<!-- markdownlint-disable-file -->
# RPI Plan: Issue #159 Conversational Assistant Keyboard Operability and Live-Region Accessibility Verification

## Task Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y
* Task slug: issue-159-assistant-a11y
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-plan-critique.md

## Executive Summary

This plan delivers the executable engineering proof and UX verification record for GitHub Issue #159 (`Conversational assistant experience in the workbench`), targeting the unticked acceptance criterion `Panel is keyboard operable, screen-reader tested, and announces new messages`. Focused three-wave research (`C1`–`C14`, `W1`–`W3`) verified that `src/api/src/zava_forward/api/web/chat-widget.js`, `chat.js`, `chat-widget.css`, and `index.html` already implement native keyboard operability, predictable focus retention/return, unobscured stay-open focus behavior, and polite ARIA live-region announcements (`role="log" aria-live="polite" aria-relevant="additions"`, `role="status" aria-live="polite" aria-atomic="true"`, and `role="alert" aria-live="polite" aria-atomic="true"`). Rather than introducing risky web edits, the plan adds a strictly typed, dual-layer verification module `src/api/tests/test_assistant_panel_a11y_159.py` (always-on Node `vm` + real Python `ChatPanel` integration plus rendered headless Chromium Playwright + CDP `Accessibility.getFullAXTree` + `MutationObserver` live-region verification) and records the verification and its explicit human assistive-technology boundary in `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md`.

### User Decisions and Requirements Highlights

* Add focused test module `src/api/tests/test_assistant_panel_a11y_159.py` verifying keyboard operability, screen-reader live-region (`aria-live="polite"` / `role="status"` / `role="log"`) message announcement, and focus management while avoiding edits to `role-screens.js` / `panels.js` (and keeping web JS untouched since already satisfied).
* Record the keyboard and screen-reader/live-region verification in `docs/reference/research/ux/` and update knowledge-base tracking (`docs/reference/README.md`, `docs/reference/log.md`).
* Validate at the Focused tier (`unittest`, `ruff check`, and `mypy`) on branch `feat/ux-159-assistant-a11y` and commit locally with the Copilot trailer without pushing.

### What You May Not Know

* In `.github/workflows/src-ci.yml`, `python -m unittest discover -s tests -v` runs before `python -m playwright install --with-deps chromium`, while `src/api/pyproject.toml` enforces `mypy --strict`, `ruff check`, and `ruff format --check` across `tests/`. Structuring `test_assistant_panel_a11y_159.py` with both an unconditional Node `vm` + `ChatPanel` test class and an automatic Playwright Chromium + CDP AXTree test class (which skips only if Playwright or the Chromium executable is absent) guarantees full execution on developer/gate hosts without breaking pre-Chromium CI unit discovery.
* Guard tests in `test_accessibility_baseline.py`, `test_production_ux_acceptance_protocol.py`, and `test_epic149_ux_evidence_results.py` enforce that automated browser/AXTree results are never entered into human-tester `Not run` cells or framed as WCAG 2.2 AA conformance; our `wcag-conformance-baseline.md` entry records the exact automated accessibility-tree, live-region, and keyboard verification while keeping human desktop NVDA/VoiceOver runs explicitly separate (#151, #155, #619).

### Unresolved Decisions or Blockers

* None for implementation and Focused-tier validation. Named human desktop screen-reader runs (NVDA with Firefox, VoiceOver with Safari) remain external human-owned gates (#151, #155, #619) and are recorded transparently as a follow-up item rather than fabricated.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (research, plan, implement, review), writing dated `2026-11-15` artifacts under `.copilot-tracking/` for Issue #159 (`Conversational assistant experience in the workbench`) on branch `feat/ux-159-assistant-a11y` (worktree `/home/azureuser/source/ama-demo-wt/feat-159-assistant-a11y`, based on PR #1639).
* Target the unticked acceptance criterion `- [ ] Panel is keyboard operable, screen-reader tested, and announces new messages`.
* Inspect `src/api/src/zava_forward/api/web/` and `src/api/tests/`, avoiding edits to `role-screens.js` / `panels.js` if already satisfied (or keeping any edit minimal and isolated); research confirmed zero web source edits are needed (`C1`–`C6`, `C9`–`C11`).
* Add `src/api/tests/test_assistant_panel_a11y_159.py` verifying keyboard operability, screen-reader live-region (`aria-live="polite"` / `role="status"` / `role="log"`) message announcement, and focus management.
* Record the screen-reader/keyboard verification in `docs/reference/research/ux/` (`wcag-conformance-baseline.md`, plus KB index/log rules in `.github/copilot-instructions.md`).
* Validation tier classification and basis: **Focused tier** — adds one focused accessibility test module (`src/api/tests/test_assistant_panel_a11y_159.py`) and updates UX knowledge-base documentation (`docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`); modifies zero production web/API/agent/core modules, workflows, gate tools, SQL schemas, dependencies, or Dockerfiles.
* Run Focused-tier validation:
  * `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_assistant_panel_a11y_159.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py -q`
  * `python3 -m ruff check src/api` (plus `ruff format --check src/api` per `src-ci.yml`)
  * `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`
* Commit all changes and `.copilot-tracking/` artifacts locally (after `rpi-review` completes so review and final state artifacts are included) using repo-local `{id}+{login}@users.noreply.github.com` resolved via `gh api user`, `Refs #159` (never a closing keyword because human desktop NVDA/VoiceOver assistive-technology sessions remain open), and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do NOT push.

## Goals

* Prove end-to-end keyboard operability, deterministic focus management, computed accessibility-tree exposition, and dynamic polite live-region message announcements for the workbench conversational assistant (`#employee-chat`, `#employee-chat-launcher`, and `#chat-panel`) in `src/api/tests/test_assistant_panel_a11y_159.py`.
* Preserve zero regressions across existing web modules (`role-screens.js`, `panels.js`, `chat.js`, `chat-widget.js`) and repository accessibility/content guard counts.
* Record the dated `2026-11-15` Issue #159 verification accurately in `docs/reference/research/ux/wcag-conformance-baseline.md` (with `docs/reference/README.md` and `docs/reference/log.md` synchronized), maintaining strict separation between automated browser accessibility-tree/live-region proof and named human desktop screen-reader testing.

## Scope and Non-Goals

### In Scope

* Creating `src/api/tests/test_assistant_panel_a11y_159.py` with:
  * Deterministic Node `vm` + real Python `ChatPanel` integration tests covering keyboard interactions, focus lifecycle, and live-region announcements across all turn outcomes (`answer`, `withheld`, `refused`, `fallback`, validation alert, transport alert, `#chat-panel` proposal request status, and session-loss `deny()` handoff).
  * Rendered headless Chromium Playwright + CDP `Accessibility.getFullAXTree` + `MutationObserver` live-region and keyboard-only traversal tests against a live synthetic loopback `App` server.
* Updating `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md` to record the Issue #159 verification and its evidence boundaries.
* Running Focused-tier `unittest`, `ruff`, and `mypy` checks and committing locally with all `2026-11-15` `.copilot-tracking/` artifacts.

### Non-Goals

* Editing `role-screens.js`, `panels.js`, `chat.js`, `chat-widget.js`, or CSS files (verified unnecessary in Research `C1`–`C11`).
* Fabricating named human NVDA/VoiceOver tester entries in `production-ux-acceptance-protocol.md` or `Manual check record` tables, or claiming full WCAG 2.2 AA conformance.
* Pushing commits to `origin` or opening/updating a remote pull request.

## Functional Requirements

* FR-01: Verify keyboard-only launcher, disclosure, composer, skill-selection, resize/dock, sources-disclosure, proposal-request, and close/dismiss flows without mouse clicks where keyboard keys govern activation.
  * Observable acceptance criteria: `test_assistant_panel_a11y_159.py` exercises `Enter` and `Space` on `#employee-chat-launcher`, `<summary>` and `"Open chat"` / `"Request proposal: ..."` inside `#chat-panel`, `"About this chat"` and `"Chat size"` disclosures, `"Dock to right edge"` (`aria-pressed` toggle), width/height `<input type="range">` arrow-key adjustments, `Tab` / `Shift+Tab` traversal including `role="log"[tabindex="0"]` and `Sources (N)` `<summary>`, `Shift+Enter` newline insertion without submitting, `Enter` submission (with IME `isComposing` / `keyCode === 229` non-submit guard), and `Escape` / `"Close chat"` dismissal.
* FR-02: Verify screen-reader live-region structure, computed accessibility-tree properties, and dynamic message announcements across every conversational turn outcome.
  * Observable acceptance criteria: Both Node `vm` and Chromium CDP `Accessibility.getFullAXTree` + `MutationObserver` confirm `role="dialog"` (`aria-labelledby="employee-chat-title"`), `role="log"` (`aria-live="polite"`, `aria-relevant="additions"`, accessible name `"Employee assistant conversation"`), `role="status"` (`aria-live="polite"`, `aria-atomic="true"`), and `role="alert"` (`aria-live="polite"`, `aria-atomic="true"`), and observe the exact announcement transitions for skill loading, ready state, in-flight `"Asking the assistant."`, appended `You` and `Assistant` articles with non-colour `Outcome:` and source attribution, completion status messages (`answer`, `withheld`, `refused`, `fallback`), blank-question and transport `role="alert"` messages, `#chat-panel` proposal `role="status"` updates, and `#workspace-status` access-revoked announcement.
* FR-03: Verify focus management across open, submit, busy, stay-open external focus, docked close, error, and access-revocation states.
  * Observable acceptance criteria: Opening `#employee-chat` focuses `#employee-chat-title`; blank submit focuses `#employee-chat-question`; submitting while `Send` has focus moves focus to `#employee-chat-question` before `send.disabled = true` so `document.activeElement` never falls back to `document.body`; arriving replies do not steal focus when the user inspects `role="log"`, `Sources (N)`, or an outside page control; focusing an obscured page control triggers `revealBeside` scroll clearance; `Escape` or `"Close chat"` (floating or docked) unhides `#employee-chat-launcher` and restores focus to it with `aria-expanded="false"`; and `401`/`403` access denial moves focus from `#employee-chat` to `#app`.
* FR-04: Record the verification and its evidence boundaries in `docs/reference/research/ux/`.
  * Observable acceptance criteria: `docs/reference/research/ux/wcag-conformance-baseline.md` documents the `2026-11-15` Issue #159 conversational assistant keyboard, focus-management, CDP Accessibility Tree, and live-region verification (`src/api/tests/test_assistant_panel_a11y_159.py`), `docs/reference/README.md` and `docs/reference/log.md` are updated consistently, and all baseline/protocol guard tests pass.

## Non-Functional Requirements

* NFR-01: Static analysis, formatting, and strict type safety in `src/api`.
  * Objective threshold or evaluation condition: Zero diagnostics from `python3 -m ruff check src/api`, `python3 -m ruff format --check src/api`, and `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`.
  * Operating condition or verification approach, if needed: Evaluated directly against `src/api/pyproject.toml` (`strict = true`, `line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`).
  * Observable acceptance criteria: All three commands exit `0` with zero warnings or errors.
* NFR-02: Deterministic offline execution and CI pre-Chromium compatibility.
  * Objective threshold or evaluation condition: Zero external network calls (non-loopback browser requests aborted); Node `vm` + Python `ChatPanel` tests always execute in standard `unittest`; Chromium Playwright + CDP AXTree tests execute automatically whenever Playwright and Chromium exist on the host and only `skipTest` if the browser executable is not yet installed.
  * Operating condition or verification approach, if needed: Local loopback `ThreadingHTTPServer` bound to `127.0.0.1:0` with synthetic store data from `test_mvp.DATA`.
  * Observable acceptance criteria: Target `unittest` suite completes deterministically in <15 seconds with zero network dependency and zero page/console errors.

## Acceptance Criteria

* AC-1: `src/api/tests/test_assistant_panel_a11y_159.py` exists, contains semantic behavioral checks (no tautological source-regex restatements), and passes both its Node `vm` + backend `ChatPanel` test class and its live headless Chromium Playwright + CDP `Accessibility.getFullAXTree` + `MutationObserver` test class on this host.
* AC-2: Zero modifications are made to `role-screens.js`, `panels.js`, `chat.js`, `chat-widget.js`, or CSS files, and all pinned baseline/content guards (`test_accessibility_baseline.py`, `test_content_standard.py`, `test_home_chat_regulatory_keyboard_provenance.py`, `test_chat_widget_focus.py`, `test_production_ux_acceptance_protocol.py`, `test_epic149_ux_evidence_results.py`, `test_screen_design_traceability.py`) pass.
* AC-3: `docs/reference/research/ux/wcag-conformance-baseline.md` (including its `Keyboard`, `Name, role, value`, `Status messages`, and `2.4.11` `Focus not obscured` notes plus a dedicated `2026-11-15` `#159` section), `docs/reference/README.md`, and `docs/reference/log.md` record the Issue #159 verification accurately without claiming WCAG 2.2 AA conformance or fabricating human tester entries, and contain zero `.copilot-tracking/` references.
* AC-4: `ruff check src/api`, `ruff format --check src/api`, and `mypy` (`src/api`) pass with exit code `0`, Focused-tier classification and basis are recorded, repo-local `user.email` is configured from `gh api user` (`{id}+{login}@users.noreply.github.com`), and all deliverables plus `2026-11-15` `.copilot-tracking/` artifacts (including post-implementation review and state JSON) are committed locally on `feat/ux-159-assistant-a11y` using `Refs #159` (no closing keywords) and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing.

## Test Ownership and Coverage Lock

* Canonical target added: `src/api/tests/test_assistant_panel_a11y_159.py` (maximum new files: `1`; production web files modified: `0`; exact test removals: `none`).
* Semantic behavioral coverage owned by `test_assistant_panel_a11y_159.py`:
  1. `AssistantPanelNodeA11y159Tests` (unconditional Node `vm` + real Python `ChatPanel` / `ChatIsolation` integration): semantic execution of keyboard events (`Enter`, `Shift+Enter`, IME `isComposing`/`229`, `Escape`), focus transitions (`open`, `busy`, `Send`-focused submit, blank-input error, docked `hide`, `revealBeside` scroll clearance, `401`/`403` `deny()`), and live-region announcement sequences across real backend `answer`, `refused`, `withheld`, and `fallback` payloads plus `#chat-panel` proposal requests.
  2. `AssistantPanelBrowserA11y159Tests` (headless Chromium Playwright + CDP `Accessibility.getFullAXTree` + `MutationObserver` against loopback `App`): rendered keyboard-only journey from `#employee-chat-launcher` and `#case-panel-ai` `#chat-panel`, computed browser accessibility-tree roles/names/live-region properties, and captured DOM live-region mutation announcements across multi-turn prompts, cited answers, refusals, alerts, disclosures, dock/resize controls, and Escape focus restoration.
* Existing regression suites preserved unchanged: `test_accessibility_baseline.py`, `test_content_standard.py`, `test_chat_widget_focus.py`, `test_home_chat_regulatory_keyboard_provenance.py`, `test_chat_panel.py`, `test_production_ux_acceptance_protocol.py`, `test_epic149_ux_evidence_results.py`, `test_screen_design_traceability.py`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-plan.md                                                                      |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-phase-details.md                                                           |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-plan-critique.md with Revise verdict; PC-001, PC-002, and PC-003 resolved directly |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md (`Research disposition: executed`, `Planning Readiness: Ready`)|
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-changes.md is created by implementation as its evidence record             |
| Planning execution and readiness | Complete and Ready for implementation after resolving one-pass critique findings PC-001 through PC-003                                   |
| Continuation context             | Active automatic RPI Agent parent continues directly to `rpi-implement`                                                                  |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md`: Grounded `C1`–`C14` and `W1`–`W3` evidence establishing zero web defects, dual-layer Node-VM + Chromium CDP AXTree test design, CI pre-Chromium constraints, and UX documentation guardrails.
* `src/api/src/zava_forward/api/web/chat-widget.js` and `src/api/src/zava_forward/api/web/chat.js`: Canonical conversational assistant dialog, composer, live regions, focus lifecycle, and `#chat-panel` disclosure implementation.
* `docs/reference/research/ux/wcag-conformance-baseline.md` and `.github/copilot-instructions.md`: Canonical UX audit record, evidence-honesty rules, Focused validation tier contract, and knowledge-base index/log requirements.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Conversational Assistant Keyboard, Focus, and Live-Region Verification Suite

* Intent: Deliver `src/api/tests/test_assistant_panel_a11y_159.py` proving keyboard operability, focus management, computed accessibility-tree exposition, and dynamic polite live-region announcements across Node `vm` + backend `ChatPanel` and rendered headless Chromium.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement Node VM + Real Python ChatPanel Keyboard, Focus, and Live-Region Suite

* Requirement and evidence: FR-01, FR-02, FR-03, NFR-01, NFR-02 (`C2`–`C4`, `C7`, `C13`, `C14`)
* Expected result: `AssistantPanelNodeA11y159Tests` in `src/api/tests/test_assistant_panel_a11y_159.py` runs unconditionally under `unittest` and verifies keyboard shortcuts (`Enter`, `Shift+Enter`, IME `isComposing`/`229`, `Escape`), focus preservation/return (`open`, `Send`-focused `busy(true)`, blank-question alert, docked `hide()`, `revealBeside` scroll clearance, `401`/`403` `deny()` to `#app`), `#chat-panel` `Open chat` + `Request proposal` status announcements, and real backend `ChatPanel` turn announcements across `answer`, `withheld`, `refused`, and `fallback`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement Rendered Chromium Playwright + CDP Accessibility Tree and Live-Region Mutation Suite

* Requirement and evidence: FR-01, FR-02, FR-03, NFR-01, NFR-02 (`C1`–`C6`, `C8`, `C13`, `W1`–`W3`)
* Expected result: `AssistantPanelBrowserA11y159Tests` in `src/api/tests/test_assistant_panel_a11y_159.py` serves the real `App` on loopback with synthetic data, drives keyboard-only traversal (`Enter`, `Space`, `Tab`, `Shift+Tab`, `Shift+Enter`, `ArrowRight`, `Escape`) across `#employee-chat-launcher`, `#employee-chat`, and `#case-panel-ai`'s `#chat-panel`, inspects CDP `Accessibility.getFullAXTree` roles/names/live properties, and asserts `MutationObserver`-captured live-region announcements (`role="log"`, `role="status"`, `role="alert"`) with zero console/page errors.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: UX Verification Record, Guard Reconciliation, and Focused Validation

* Intent: Record the Issue #159 conversational assistant keyboard and screen-reader/live-region verification in `docs/reference/research/ux/`, synchronize the knowledge-base index and log, pass all Focused-tier checks, and prepare clean local commit artifacts.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Record Issue #159 Keyboard and Live-Region Verification in UX Knowledge Base

* Requirement and evidence: FR-04, AC-3 (`C10`, `C12`, `.github/copilot-instructions.md`)
* Expected result: `docs/reference/research/ux/wcag-conformance-baseline.md` records a dated `2026-11-15` Issue #159 conversational assistant keyboard, focus-management, CDP Accessibility Tree, and live-region announcement verification section and audit note; `docs/reference/README.md` and `docs/reference/log.md` are updated consistently; human-tester `Not run` cells and non-conformance wording remain intact.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Execute Focused Validation Suite and Regression Guards

* Requirement and evidence: NFR-01, NFR-02, AC-1, AC-2, AC-3, AC-4 (`C10`–`C14`)
* Expected result: Exact caller `unittest` command, related UX/chat guard tests, `python3 -m ruff check src/api`, `python3 -m ruff format --check src/api`, and `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` all exit `0`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-phase-details.md

## Dependencies

* Local Node.js runtime (`node`) and Python 3.12 editable environment (`src/core`, `src/agents`, `src/api`): present and verified during Research.
* Local Playwright 1.64.0 and Chromium `156.0.8078.4`: present and verified on this host (`C8`); test skips gracefully only in environments where the Chromium binary has not yet been installed (`C13`).

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 — `PC-001` (High)  | Resolved    | Updated `P01-T01` and `P01-T02` to derive valid `Retrofit Coordinator` staff and case fixtures dynamically from `test_mvp.DATA`, reset/isolate non-case launcher checks before opening case-scoped `#employee-chat` on `#/case/<case_id>?tab=ai` (avoiding `chat.js` singleton reuse of `caseId === ""`), and execute both a case-grounded cited answer (`Sources (N)` with `N >= 1`) and a refused action prompt (`"Approve this case"`) in Chromium. |
| Run 1 — `PC-002` (Medium)| Resolved    | Updated `P01-T01` and `P01-T02` to include non-auth `500`/transport failure `role="alert"` verification (`"Chat unavailable: ... Owner: application support. Next action: ..."`), `Space` launcher activation alongside `Enter`, arrow-key adjustment on both `#employee-chat-width` (`--chat-width`) and `#employee-chat-height` (`--chat-height`), child selector `#chat-panel > p[role="status"]`, and `hidden` attribute observation in `window.__a11yLiveEvents`. |
| Run 1 — `PC-003` (Low)   | Resolved    | Recorded explicit Focused-tier classification and basis, aligned the `2.4.11` (`Focus not obscured`) audit row note in `P02-T01`, and specified repo-local noreply `user.email` (`gh api user`), `Refs #159` non-closing commit wording, and post-`rpi-review` local commit capture without pushing in `AC-4` and `P02-T02`. |

## Follow-Up Items

* Execute named human desktop assistive-technology and zoom sessions (NVDA with Firefox on Windows, VoiceOver with Safari on macOS, 200% text resize and 400% zoom) for the conversational assistant widget and single case view under Issues #151, #155, and #619. Outside immediate automated scope because no desktop screen reader or human tester session exists on this headless Linux host (`C12`); owned by the UX human acceptance programme.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None

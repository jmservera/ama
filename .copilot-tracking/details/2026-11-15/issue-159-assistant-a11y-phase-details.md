<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #159 Conversational Assistant Keyboard Operability and Live-Region Accessibility Verification

## Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y
* Task slug: issue-159-assistant-a11y
* Related plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md (`C1`–`C14`, `W1`–`W3`)

## Phase Index

| Phase ID | Name                                                                      | Status | Detail sections        |
|----------|---------------------------------------------------------------------------|--------|------------------------|
| P01      | Conversational Assistant Keyboard, Focus, and Live-Region Verification Suite | Ready  | P01, P01-T01, P01-T02  |
| P02      | UX Verification Record, Guard Reconciliation, and Focused Validation      | Ready  | P02, P02-T01, P02-T02  |

<!-- rpi:phase id=P01 -->
## P01: Conversational Assistant Keyboard, Focus, and Live-Region Verification Suite

### Context

Research (`C1`–`C9`) established that `src/api/src/zava_forward/api/web/chat-widget.js`, `chat.js`, `chat-widget.css`, and `index.html` already implement the complete keyboard, focus-management, and live-region announcement contract for Issue #159, while existing tests split between static substring guards (`test_home_chat_regulatory_keyboard_provenance.py`), async Node-VM focus checks (`test_chat_widget_focus.py`), and an opt-in `ZF_BROWSER_TESTS=1` partial check (`test_chat_panel.py`). Meanwhile, `.github/workflows/src-ci.yml` (`C13`) runs `python -m unittest discover -s tests -v`, `ruff check . && ruff format --check .`, and `mypy` (`strict = true`, `C14`) prior to installing Chromium.

### Intent

Create `src/api/tests/test_assistant_panel_a11y_159.py` as a self-contained, strictly typed `unittest` module proving keyboard operability, screen-reader live-region (`aria-live="polite"`, `role="status"`, `role="log"`, `role="alert"`) announcements, computed accessibility-tree semantics, and focus management without altering web JS/CSS files.

### Boundaries

* Included: `src/api/tests/test_assistant_panel_a11y_159.py` containing both an unconditional Node `vm` + real Python `ChatPanel` integration test class and a live loopback Chromium Playwright + CDP `Accessibility.getFullAXTree` + `MutationObserver` test class.
* Excluded: Edits to `role-screens.js`, `panels.js`, `chat.js`, `chat-widget.js`, `style.css`, or `chat-widget.css`; `.copilot-tracking/` path strings inside Python source/docstrings/comments.

### Likely Targets

* `src/api/tests/test_assistant_panel_a11y_159.py`: New focused accessibility verification test module for Issue #159.

### Dependencies

* None (`node`, `zava_forward` packages, `playwright`, and headless Chromium are already installed).

### Validation Expectations

* `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_assistant_panel_a11y_159.py -v` runs both test classes on this host with 0 failures and 0 skips.
* Clean pass under `ruff check`, `ruff format --check`, and `mypy`.

### Completion Evidence

* Passing test output showing both `AssistantPanelNodeA11y159Tests` and `AssistantPanelBrowserA11y159Tests` executed and passed.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement Node VM + Real Python ChatPanel Keyboard, Focus, and Live-Region Suite

#### Context

`chat-widget.js` (`C2`) and `chat.js` (`C3`, `C4`) run cleanly in Node's `node:vm` module (`C7`) and consume JSON payloads produced by the real Python `ChatPanel` + `ChatIsolation` (`src/api/src/zava_forward/api/` / `zava_forward.agents`). Testing the real JS scripts fed by real Python `ChatPanel` turn responses guarantees that backend response shapes (`kind`, `reply`, `label`, `answer_source`, `workflow_only`, `citations`, `consumption`) drive exact live-region DOM transitions in every `unittest` run, even before Chromium is installed in CI (`C13`).

#### Intent

Implement `AssistantPanelNodeA11y159Tests` inside `src/api/tests/test_assistant_panel_a11y_159.py` to verify semantic runtime behavior of keyboard handlers, live-region announcements, and focus management across `employeeChat` and `chatCasePanel`.

#### Boundaries

* Included:
  * Selecting a valid `Retrofit Coordinator` staff record and case ID dynamically from `test_mvp.DATA` at test setup (avoiding hardcoded fixture assumptions) and generating real backend `ChatPanel` turn payloads on synthetic `Store` data for:
    1. Deterministic case-grounded `answer` (`kind == "answer"`, citations present),
    2. Action/mutation `refused` (`"Approve this case"`, `kind == "refused"`),
    3. Unverified/ungrounded `withheld` (when generative reply lacks valid citation, `kind == "withheld"`),
    4. Model-unavailable `fallback` (`kind == "fallback"`, `workflow_only is True`).
  * Feeding those real payloads into `chat-widget.js` + `chat.js` inside `node:vm` with a live-region mutation recorder tracking every write and `hidden`-state reveal across `[role="log"]` (`aria-live="polite"`, `aria-relevant="additions"`), `p[role="status"]` (`aria-live="polite"`, `aria-atomic="true"`), `p[role="alert"]` (`aria-live="polite"`, `aria-atomic="true"`), `#chat-panel > p[role="status"]` (direct child selector disambiguated from nested `#regulatory-chat > p[role="status"]`), and `#workspace-status`.
  * Verifying keyboard and focus invariants:
    * Launcher toggle (`aria-haspopup="dialog"`, `aria-controls="employee-chat"`, `aria-expanded` `"false"` -> `"true"` -> `"false"`), initial focus on `#employee-chat-title` (`tabindex="-1"`).
    * `Enter` submits when not Shift/IME-composing; `Shift+Enter` and IME (`isComposing: true` or `keyCode: 229`) do not submit.
    * Blank submit triggers `#employee-chat-error` (`"Type a question first."`, `hidden == false`) and returns focus to `#employee-chat-question`.
    * Non-auth server/transport failure (`status == 500` during ask) unhides `#employee-chat-error` (`role="alert"`) with `"Chat unavailable: ... Owner: application support. Next action: try again or continue with the ordinary workflow."`, restores `busy(false)`, and preserves the user's draft text.
    * Submitting while focus is on `Send` moves focus to `#employee-chat-question` before `send.disabled = true` (`form[aria-busy="true"]`), preventing focus drop.
    * Appended `You` and `Assistant` `<article>` items in `role="log"` include `Outcome:` text, source attribution label, and keyboard-operable `<details><summary>Sources (N)</summary>...</details>`, while `role="status"` announces `"Loading skills."` -> `"Choose a skill or ask a general work question."` -> `"Asking the assistant."` -> exact `statusFor(kind)` completion text for `answer`, `withheld`, `refused`, and `fallback`.
    * Focus stays untouched when the user focuses `role="log"`, `Sources (N)` `<summary>`, or an outside control during reply arrival, and `externalFocus` calls `window.scrollBy` via `revealBeside` when an outside focused element overlaps the floating or docked panel.
    * Docking (`Dock to right edge` `aria-pressed="true"`, height slider disabled, launcher hidden) followed by `Escape` or `Close chat` unhides `#employee-chat-launcher` before focusing it.
    * `#chat-panel` (`chatCasePanel(case_id)`): `"Open chat"` opens `#employee-chat` and focuses `#employee-chat-title`; `"Request proposal: ..."` announces `"Requesting a proposal for independent review."` then `"Proposal requested. Find it in the proposals panel and the review queue."` in `#chat-panel > p[role="status"]`.
    * Access loss (`403` during ask while focus is inside `#employee-chat`) disposes `#employee-chat`, announces `"Chat access ended. Reopen from a record you can see, or sign in again."` in `#workspace-status`, and moves focus to `#app`.
* Excluded: Regex assertions that merely re-read static JS source lines already covered by `test_home_chat_regulatory_keyboard_provenance.py`.

#### Likely Targets

* `src/api/tests/test_assistant_panel_a11y_159.py`

#### Dependencies

* None.

#### Validation Expectations

* Runs in <1 second without Playwright/Chromium and passes under strict `mypy` and `ruff`.

#### Completion Evidence

* Passing `AssistantPanelNodeA11y159Tests` test methods covering keyboard operability, all live-region outcomes, and all focus-management transitions.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Implement Rendered Chromium Playwright + CDP Accessibility Tree and Live-Region Mutation Suite

#### Context

On hosts with Playwright and Chromium installed (verified as Chromium `156.0.8078.4` on this machine, `C8`), launching the real `App` (`ThreadingHTTPServer` on `127.0.0.1:0` with synthetic `Store` data) lets us inspect the browser's actual computed Accessibility Tree via Chrome DevTools Protocol (`context.new_cdp_session(page)` -> `Accessibility.getFullAXTree`) alongside real `page.keyboard` events and a DOM `MutationObserver` attached to every live region (`[aria-live], [role="log"], [role="status"], [role="alert"]`). To remain safe in `src-ci.yml`'s pre-Chromium unit-test step (`C13`), `setUpClass` checks `importlib.util.find_spec("playwright")` and catches missing browser executable errors (`"Executable doesn't exist"`) via `cls.skipTest(...)` (`C8`).

#### Intent

Implement `AssistantPanelBrowserA11y159Tests` in `src/api/tests/test_assistant_panel_a11y_159.py` to prove rendered keyboard operability, computed screen-reader accessibility-tree semantics, focus visibility/retention, and live-region announcements in a real browser engine.

#### Boundaries

* Included:
  * Isolated loopback `ThreadingHTTPServer` serving `App(Store(...), "zf-test")` on synthetic data (`test_mvp.DATA`), selecting a `Retrofit Coordinator` staff email and valid `case_id` dynamically from `test_mvp.DATA`, aborting all non-loopback requests, and recording `pageerror` / console errors (asserting none).
  * Signing in as the `Retrofit Coordinator` staff member, installing a `window.__a11yLiveEvents` `MutationObserver` across `document.body` (`childList: true, characterData: true, subtree: true, attributes: true, attributeFilter: ["hidden"]`) that captures every live-region child addition, text change, and `hidden` removal (`id`, `role`, `ariaLive`, `ariaAtomic`, `ariaRelevant`, `text`).
  * Keyboard-only verification (`page.keyboard.press`, no mouse clicks on tested assistant controls), structured to respect `employeeChat` singleton lifecycle across non-case and case-scoped routes:
    1. Non-case launcher `Enter` and `Space` activation + resize/dock/Escape: focusing `#employee-chat-launcher` and pressing `Enter` -> verifying focus lands on `<h2 id="employee-chat-title">Employee assistant</h2>`, computed two-tone `:focus-visible` outline style is active on interactive controls, and `aria-expanded="true"`; pressing `Escape` -> verifying focus returns to `#employee-chat-launcher` (`aria-expanded="false"`); pressing `Space` on `#employee-chat-launcher` -> verifying `#employee-chat` reopens with focus on `#employee-chat-title`.
    2. Navigating via `Tab` through `"Close chat"`, `"About this chat"` (`Space` to expand), and `"Chat size"` (`Enter` to expand -> `Tab` to `"Dock to right edge"` -> `Tab` to width slider `#employee-chat-width` -> `ArrowRight` increments `--chat-width` -> `Tab` to height slider `#employee-chat-height` -> `ArrowRight` increments `--chat-height` while undocked -> `Shift+Tab` back to `"Dock to right edge"` -> `Space` toggles `aria-pressed="true"` and disables `#employee-chat-height` -> pressing `Escape` while docked hides `#employee-chat`, unhides `#employee-chat-launcher`, sets `aria-expanded="false"`, and focuses `#employee-chat-launcher`).
    3. Case-scoped assistant walkthrough on `#/case/<case_id>?tab=ai` (resetting/navigating cleanly so `employeeChat` binds `caseId === <case_id>`): focusing `#chat-panel > summary` (`"Ask the assistant about this case (optional)"`), pressing `Enter` to expand, tabbing to `"Request proposal: ..."` and pressing `Enter` -> verifying direct child `#chat-panel > p[role="status"]` announces `"Proposal requested. Find it in the proposals panel and the review queue."` in `window.__a11yLiveEvents`, then Shift+Tabbing to `"Open chat"` and pressing `Enter` -> verifying `#employee-chat` opens with `"Context: case <case_id>"` and focus on `#employee-chat-title`.
    4. Querying CDP `Accessibility.getFullAXTree` while case-scoped `#employee-chat` is open -> verifying the browser exposes `dialog` named `"Employee assistant"`, `log` named `"Employee assistant conversation"` (`live="polite"`, `relevant` containing `"additions"`), `status` (`live="polite"`, `atomic=true`), `textbox` named `"Your work question"` (with computed `description` including the entry/privacy warning), `combobox` named `"Agent skill"`, and `button` controls (`"Close chat"`, `"Send"`).
    5. Tabbing through `role="log"` (`tabindex="0"` receives keyboard focus), `"Your work question"` textarea, `"Agent skill"` select (`ArrowDown` / keyboard selection), and `"Send"`; performing a blank submit with `Enter` in `"Your work question"` -> `#employee-chat-error` (`role="alert"`, `live="polite"`, `atomic=true` in CDP AXTree) unhides and announces `"Type a question first."` in `window.__a11yLiveEvents` while focus remains on `#employee-chat-question`.
    6. Multi-line `Shift+Enter`, case-cited answer, `Send`-focused refusal turn, and transport `role="alert"`: typing `"Case check:"`, pressing `Shift+Enter`, typing `"What is the current stage?"` -> verifying no premature submit occurred on `Shift+Enter`, pressing `Enter` (backed by deterministic case-cited answer route/backend) -> verifying `window.__a11yLiveEvents` records `"Asking the assistant."`, appended `You` and `Assistant` log items with `Sources (` (`N >= 1`), and `"Answer added. Check the sources before relying on it."` while focus stays on `#employee-chat-question`; Shift+Tabbing to `Sources (` `<summary>` and pressing `Enter` to expand cited case facts via keyboard; then submitting `"Approve this case"` via `Tab` to `Send` + `Enter` -> verifying `busy(true)` moves focus back to `#employee-chat-question` (never `BODY`) and live regions announce `"Outcome: refused"` + `"Request refused. A person must take that action in the workflow."`; then routing one ask to HTTP `500` and pressing `Enter` -> verifying `#employee-chat-error` (`role="alert"`) announces `"Chat unavailable: ... Owner: application support. Next action: ..."` while preserving the unsent draft; finally pressing `Escape` to restore focus to `#employee-chat-launcher`.
* Excluded: External CDN scripts or network access; modifying `SURFACES` in `test_epic149_ux_evidence_results.py` (which forbids `skipTest` inside its pinned static-surface list).

#### Likely Targets

* `src/api/tests/test_assistant_panel_a11y_159.py`

#### Dependencies

* P01-T01 (shares module setup and synthetic store helpers).

#### Validation Expectations

* Executes end-to-end against headless Chromium on this host with 0 errors and passes `mypy --strict` and `ruff`.

#### Completion Evidence

* Passing `AssistantPanelBrowserA11y159Tests` run confirming CDP AXTree roles/names/live properties, `MutationObserver` live-region announcements, and keyboard-only focus transitions.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: UX Verification Record, Guard Reconciliation, and Focused Validation

### Context

The caller requires recording the Issue #159 screen-reader/keyboard verification in `docs/reference/research/ux/`, while repository rules (`.github/copilot-instructions.md`) require updating `docs/reference/README.md` and appending an entry to `docs/reference/log.md` whenever a knowledge-base file materially changes, and guard tests (`C10`, `C12`) enforce strict honesty boundaries between automated browser/AXTree verification and named human screen-reader acceptance (#151, #155, #619).

### Intent

Document the dated `2026-11-15` Issue #159 verification in `docs/reference/research/ux/wcag-conformance-baseline.md` (plus `docs/reference/README.md` and `docs/reference/log.md`) and run all Focused-tier test, lint, format, and type-check validations.

### Boundaries

* Included: `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`, and running Focused-tier validation commands.
* Excluded: Touching `Not run` rows in `Manual check record` or `production-ux-acceptance-protocol.md`; claiming WCAG 2.2 AA conformance; placing `.copilot-tracking/` links inside `docs/` or `src/`.

### Likely Targets

* `docs/reference/research/ux/wcag-conformance-baseline.md`: Add `2026-11-15` audit notes (`Keyboard`, `Name, role, value`, `Status messages`, and `2.4.11` `Focus not obscured` `revealBeside` clearance check while keeping 400% zoom manual testing open) and a dedicated `## Conversational assistant panel keyboard and live-region check (2026-11-15, #159)` section recording the Node-VM + headless Chromium CDP Accessibility Tree + `MutationObserver` live-region and keyboard verification and the open human desktop NVDA/VoiceOver boundary.
* `docs/reference/README.md`: Refresh the `wcag-conformance-baseline.md` summary cell to note the `2026-11-15` `#159` conversational assistant keyboard and live-region engineering check.
* `docs/reference/log.md`: Append a `## [2026-11-15] update | Issue #159 conversational assistant keyboard, focus and live-region verification (Refs #159)` entry at EOF without editing prior entries.

### Dependencies

* P01

### Validation Expectations

* `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_assistant_panel_a11y_159.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py -q`
* Additional UX/chat regression checks: `test_chat_widget_focus.py`, `test_home_chat_regulatory_keyboard_provenance.py`, `test_production_ux_acceptance_protocol.py`, `test_epic149_ux_evidence_results.py`, `test_screen_design_traceability.py`, `test_ux_design_traceability.py`.
* `python3 -m ruff check src/api && python3 -m ruff format --check src/api`
* `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`

### Completion Evidence

* Zero-exit outputs from all validation commands and clean `git diff` review of Markdown links, ASCII punctuation, list markers (`*`), and guard phrases.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Record Issue #159 Keyboard and Live-Region Verification in UX Knowledge Base

#### Context

`wcag-conformance-baseline.md` (`C12`) is the canonical workbench accessibility record guarded by `test_accessibility_baseline.py` (`C10`) and `test_epic149_ux_evidence_results.py`.

#### Intent

Record the `2026-11-15` Issue #159 conversational assistant keyboard operability, focus-management, CDP Accessibility Tree, and live-region announcement verification truthfully in `wcag-conformance-baseline.md`, refresh `docs/reference/README.md`, and append to `docs/reference/log.md`.

#### Boundaries

* Included: Plain ASCII Markdown using `*` bullets, no em dashes, no bolded-prefix list items, relative KB links, explicit module reference `src/api/tests/test_assistant_panel_a11y_159.py`, exact verified behaviors, and explicit separation from human desktop NVDA/VoiceOver testing (#151, #155, #619).
* Excluded: Modifying `Not run` cells in human-record tables; prohibited phrases (`fully conforms`, `is WCAG 2.2 AA compliant`, `conforms to WCAG`); `.copilot-tracking/` references.

#### Likely Targets

* `docs/reference/research/ux/wcag-conformance-baseline.md`
* `docs/reference/README.md`
* `docs/reference/log.md`

#### Dependencies

* P01-T01, P01-T02

#### Validation Expectations

* `test_accessibility_baseline.py`, `test_production_ux_acceptance_protocol.py`, `test_epic149_ux_evidence_results.py`, `test_screen_design_traceability.py`, and `test_ux_design_traceability.py` all pass.

#### Completion Evidence

* Updated Markdown sections verified by diff and guard tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Execute Focused Validation Suite and Regression Guards

#### Context

Caller instructions and AMA Focused-tier rules require running the targeted unit tests, `ruff`, and `mypy` before review and local commit.

#### Intent

Execute the exact caller validation commands plus formatting and UX/chat regression guards, confirming zero regressions.

#### Boundaries

* Included: `unittest`, `ruff check`, `ruff format --check`, `mypy`, recording the Focused-tier classification basis (focused accessibility test + UX KB documentation slice; zero production web/API/SQL/infra/workflow/dependency/Dockerfile changes) in `.copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-changes.md`, configuring repo-local `git config --local user.email` from `gh api user` (`{id}+{login}@users.noreply.github.com`), and committing all deliverables plus `2026-11-15` `.copilot-tracking/` artifacts (after `rpi-review` completes) with `Refs #159` (never any closing keyword) and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
* Excluded: Pushing to remote, mutating git global config, or using closing keywords for Issue #159.

#### Likely Targets

* Validation execution recorded in `.copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-changes.md` during Implement.

#### Dependencies

* P01, P02-T01

#### Validation Expectations

* Exit code `0` across every command, with both Node `vm` and Chromium browser test classes executing on this host.

#### Completion Evidence

* Recorded command outputs and test counts in the implementation changes artifact.

#### Unresolved Items

* None.

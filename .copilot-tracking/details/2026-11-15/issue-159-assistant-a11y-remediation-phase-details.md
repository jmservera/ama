<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #159 Conversational Assistant Accessibility Review Remediation (`RV-001`–`RV-003`)

* Task ID: 2026-11-15-issue-159-assistant-a11y-remediation
* Task slug: issue-159-assistant-a11y-remediation
* Parent task: 2026-11-15-issue-159-assistant-a11y
* Plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan.md

<!-- rpi:phase id=P01 -->
## P01: Remediate Test Hermeticity, Scoped Browser Assertions, and UX Baseline Accuracy (`RV-001`–`RV-003`)

* Phase goal: Resolve `RV-001`, `RV-002`, and `RV-003` from `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-review.md` without touching production web assets.
* Dependencies: None.
* Disjoint write boundary: `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md`.

<!-- rpi:task id=P01-T01 phase=P01 -->
### P01-T01: Test Hermeticity and Scoped Browser/AXTree Assertions (`src/api/tests/test_assistant_panel_a11y_159.py`)

* Context and evidence:
  * `App.__init__` in `src/api/src/zava_forward/api/server.py` calls `simulation_lane.Lane.open(os.environ, ...)`, reading `ZF_SIM_STORE` and `ZF_SIM_KEY_FILE` (`src/core/src/zava_forward/core/simulation_lane.py`). Setting both to `""` in `APPROVED_CHAT_ENV` ensures `self.app.simulation` stays `None` (`not-configured`), and `_SyntheticWorkbenchHarness.close()` defensively closes any `close` callable on `self.app.simulation` if present (`RV-003`).
  * In `AssistantPanelNodeA11y159Tests`: test both `401` and `403` `deny()` access-loss responses against `chat.js` so `401`/`403` focus recovery to `#app` and `#workspace-status` announcement (`"Chat access ended. Reopen from a record you can see, or sign in again."`) are both directly proven.
  * In `AssistantPanelBrowserA11y159Tests`:
    * Whitelist `"chat-http:401:"` alongside `"chat-http:403:"` and `"chat-http:500:"` for `/api/chat/ask` in `_open_authenticated_page`.
    * `test_browser_launcher_keyboard_resize_dock_and_escape_focus`:
      * Activate `Close chat` via `Enter` key (`panel` hides, `aria-expanded == "false"`, focus returns to `#employee-chat-launcher`), then re-open via `Space`.
      * Exercise rendered `revealBeside` overlap scroll clearance in Chromium:
        * While `#employee-chat` is open and undocked (floating bottom-right), reset scroll to `(0, 0)`, inject an in-viewport `position: absolute` focusable button positioned inside `#employee-chat`'s current `getBoundingClientRect()` plus a tall spacer below the fold so vertical scrolling has room, call `el.focus({ preventScroll: true })` (which dispatches `focusin` without browser native pre-scroll so `revealBeside` alone drives `window.scrollBy`), and assert `window.scrollY > 0` and reduced/cleared overlap (then clean up and reset scroll).
        * While `#employee-chat` is docked (`chat-widget-docked`), reset scroll to `(0, 0)`, inject an in-viewport `position: absolute` focusable button positioned inside docked `#employee-chat`'s horizontal bounds plus a wide horizontal spacer so `scrollX` has room, call `el.focus({ preventScroll: true })`, and assert `window.scrollX > 0` (then clean up and reset scroll).
    * `test_browser_case_assistant_axtree_live_announcements_and_keyboard_turns`:
      * Scope CDP AXTree `status` (captured while `.chat-widget-status` is non-empty, since `.chat-widget-status:empty` is `display: none`) and `alert` lookups to descendants of the `Employee assistant` `dialog` AX node by indexing ALL `ax_nodes` (including `ignored` wrapper nodes) by `nodeId` and walking `childIds` recursively from `dialog_ax["nodeId"]`.
      * After pressing `Shift+Enter` between `"Case check:"` and `"What stage is this case at?"`, assert `"\n" in question.input_value()` in addition to `article.count() == 0`.
      * Focus `#employee-chat-skill` (`<select>`), press `ArrowDown` to select a permitted non-`general` skill (asserting `skill_select.input_value() != "general"`), press `Shift+Tab` back to `#employee-chat-question`, type a short question and press `Enter` to submit, and verify the new assistant article renders `f"Skill: {selected_skill}."`.
      * Exercise `403` `chat.js` `deny()` (`#employee-chat` hides, focus moves to `#app`, `#workspace-status` announces `"Chat access ended. Reopen from a record you can see, or sign in again."`), then re-open `#employee-chat` and exercise `401` `app.js` session-expiry interception (`login("Your session has ended. Sign in again.")` renders a sign-in `role="alert"` and moves focus to `#app`).
* Completion expectations:
  * All tests in `src/api/tests/test_assistant_panel_a11y_159.py` pass with 0 skips on this host, `mypy --strict` passes with zero `# type: ignore`, and `ruff check` + `ruff format --check` pass.

<!-- rpi:task id=P01-T02 phase=P01 -->
### P01-T02: UX Baseline Accuracy, `log.md` Hygiene, and Focused Validation

* Context and evidence:
  * Update `docs/reference/research/ux/wcag-conformance-baseline.md`:
    * Replace `resize preset (S, M, L aria-pressed)` with accurate control wording: `Dock to right edge` (`aria-pressed`), width and height range sliders (`#employee-chat-width`, `#employee-chat-height`), keyboard `Close chat`, and keyboard skill `<select>` selection (`#employee-chat-skill`).
    * Confirm every scenario mentioned in the `Audit` rows (`Keyboard`, `Name, role, value`, `Status messages`, `Focus not obscured`) and `## Conversational assistant panel keyboard and live-region check (2026-11-15, #159)` corresponds 1-for-1 to assertions in `src/api/tests/test_assistant_panel_a11y_159.py`.
  * Remove the extra trailing blank line at EOF in `docs/reference/log.md`.
  * Run validation commands:
    * `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_assistant_panel_a11y_159.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py -q`
    * `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_ux_design_traceability.py src/api/tests/test_screen_design_traceability.py src/api/tests/test_epic149_ux_evidence_results.py src/api/tests/test_production_ux_acceptance_protocol.py src/api/tests/test_chat_panel.py src/api/tests/test_chat_widget_focus.py src/api/tests/test_home_chat_regulatory_keyboard_provenance.py src/core/tests/test_live_doc_links.py -q`
    * `python3 -m ruff check src/api && python3 -m ruff format --check src/api`
    * `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`
    * `git --no-pager diff --check`
* Completion expectations:
  * Every command above exits `0` with zero errors or whitespace warnings.

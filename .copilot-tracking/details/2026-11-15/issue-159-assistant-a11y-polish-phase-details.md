<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #159 Conversational Assistant Accessibility Final Precision Polish (`RV-001`–`RV-002`)

* Task ID: 2026-11-15-issue-159-assistant-a11y-polish
* Task slug: issue-159-assistant-a11y-polish
* Parent task: 2026-11-15-issue-159-assistant-a11y-remediation
* Plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md

<!-- rpi:phase id=P01 -->
## P01: Final Test-to-Baseline Parity and Resource/EOF Hygiene (`RV-001`–`RV-002`)

<!-- rpi:task id=P01-T01 phase=P01 -->
### P01-T01: `src/api/tests/test_assistant_panel_a11y_159.py` Precision Assertions and Cleanup Guard

* Wrap `_SyntheticWorkbenchHarness.__init__` after `self.root = Path(...)`, `self.store: Any = None`, `self.app: Any = None` in `try: ... except BaseException: self.close(); raise`, updating `close()` to guard `if self.app is not None:` and `if self.store is not None:`.
* In `LIVE_OBSERVER_INIT_SCRIPT`, when `added.nodeType === 1`, also scan `added.querySelectorAll('[aria-live], [role="status"], [role="alert"], [role="log"]')` so mounted container subtrees (including `app.js`'s `401` login `<p class="err" role="alert">`) are captured (`PC-002`).
* In `test_browser_launcher_keyboard_resize_dock_and_escape_focus`:
  * Open a CDP session (`page.context.new_cdp_session(page)`):
    * Before opening, verify the launcher `button` AX node (`name == "Chat"`) exposes `expanded is False`.
    * After opening `#employee-chat` and expanding `Chat size` (`<summary>`), verify launcher `button` `"Chat"` exposes `expanded is True`, `DisclosureTriangle` `"Chat size"` exposes `expanded is True`, and `Dock to right edge` `button` inside `_dialog_ax_subtree` exposes `pressed == "false"`.
    * Verify zero keyboard focus trap in both directions (`PC-003`): from `Close chat`, `Shift+Tab` moves focus outside `#employee-chat` to `#employee-chat-launcher` and another `Shift+Tab` moves focus inside `#app`; from `Send`, `Tab` moves focus outside `#employee-chat` (`!panel.contains(document.activeElement)`) and wraps to `.skip-link`.
    * After toggling `Dock to right edge` via `Space`, inspect `_dialog_ax_subtree` again and verify `Dock to right edge` `button` exposes `pressed == "true"`.
* In `test_browser_case_assistant_axtree_live_announcements_and_keyboard_turns`:
  * Verify `log_props.get("relevant") == "additions"`.
  * After `ArrowDown` on `#employee-chat-skill` (`selected_skill != "general"`) and `Shift+Tab` back to `#employee-chat-question`, type `"Summarise next steps for this case."` and press `Enter` directly from `#employee-chat-question` (`article` count advances to `4`, `f"Skill: {selected_skill}."` appears in `role="log"`, focus remains on `#employee-chat-question`).
  * Then type `"Approve this case."`, `Tab` twice to `Send`, and press `Enter` on `Send` (`article` count advances to `6`, `"Outcome: refused"` appears in `role="log"`, focus moves back to `#employee-chat-question`).
  * After both the `403` `deny()` flow and the `401` `app.js` session-expiry flow finish, re-read `window.__a11yLiveEvents` and assert that `MutationObserver` recorded `"Chat access ended. Reopen from a record you can see, or sign in again."` on `#workspace-status` (`id == "workspace-status"`) and `"Your session has ended. Sign in again."` on `role="alert"`.

<!-- rpi:task id=P01-T02 phase=P01 -->
### P01-T02: `wcag-conformance-baseline.md` Parity, `log.md` EOF Newline, and Validation

* Update `docs/reference/research/ux/wcag-conformance-baseline.md` so Node-VM `Shift+Enter` non-submit (`!defaultPrevented`) + `scrollBy` delta vs Chromium `Shift+Enter` newline insertion + bounding-box `revealBeside` clearance, CDP `expanded` / `pressed` / `relevant: "additions"`, and forward/backward no-trap `Tab` exit match `test_assistant_panel_a11y_159.py` 1-for-1.
* Restore a single trailing `\n` at EOF in `docs/reference/log.md` and ensure single-`\n` EOF across current tracking files without modifying historical critique/review content.
* Re-run caller `unittest`, UX/traceability/chat regression `unittest`, `ruff check`, `ruff format --check`, `mypy`, `git --no-pager diff --check`, and `git --no-pager diff --cached --check`.

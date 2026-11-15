<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #159 Conversational Assistant Accessibility Closeout (`RV-001`)

## Task Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y-closeout
* Task slug: issue-159-assistant-a11y-closeout
* Parent task: 2026-11-15-issue-159-assistant-a11y-polish
* Plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-closeout-plan.md

<!-- rpi:phase id=P01 status=completed -->
## P01: Resolve `RV-001` in `src/api/tests/test_assistant_panel_a11y_159.py`

<!-- rpi:task id=P01-T01 phase=P01 status=completed -->
### P01-T01: Harden `_SyntheticWorkbenchHarness.close()`, `NODE_A11Y_HARNESS` `Enter` Submit, and Pre-Open `Chat size` CDP `expanded` Assertion

* Context:
  * Resolves `RV-001` from `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-polish-review.md`.
* Expected adjustments in `src/api/tests/test_assistant_panel_a11y_159.py`:
  1. Wrap `_SyntheticWorkbenchHarness.close()` with `try ... finally` blocks around `sim_close()`, `self.app.assistants.stop()`, `self.store.db.close()`, and `shutil.rmtree(self.root, ignore_errors=True)`.
  2. In `NODE_A11Y_HARNESS` `requestSubmit()`, record `this._lastSubmit = this.onsubmit ? this.onsubmit({ preventDefault() {} }) : undefined; return this._lastSubmit;`. In the 4-turn loop (`answer`, `refused`, `withheld`, `fallback`), when `mode === "send"` invoke `formEl.requestSubmit()`, and when `mode !== "send"` set `formEl._lastSubmit = undefined; const enterSub = input.dispatchEvent("keydown", { key: "Enter" }); assert.equal(enterSub.prevented, true); const askTask = formEl._lastSubmit; assert.ok(askTask);`. Also assert `env.liveMutations` recorded `role === "log"`, `role === "status"`, and `role === "alert"` entries.
  3. In `test_browser_launcher_keyboard_resize_dock_and_escape_focus`, before pressing `Enter` on `"Chat size"`, query `_dialog_ax_subtree` and assert `self._ax_props(size_ax_closed[0]).get("expanded") is False` on `DisclosureTriangle` `"Chat size"`, keeping the post-`Enter` `expanded is True` check right after.
* Completion expectations:
  * `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_assistant_panel_a11y_159.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py -q` exits `0`.
  * `python3 -m ruff check src/api`, `python3 -m ruff format --check src/api`, `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`, and `git --no-pager diff --check` exit `0`.

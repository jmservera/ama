<!-- markdownlint-disable-file -->
# RPI Plan: Issue #159 Conversational Assistant Accessibility Closeout (`RV-001`)

## Task Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y-closeout
* Task slug: issue-159-assistant-a11y-closeout
* Parent task: 2026-11-15-issue-159-assistant-a11y-polish
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-closeout-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-closeout-plan-critique.md

## Executive Summary

This micro-closeout resolves the sole `Low` finding (`RV-001`) from `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-polish-review.md` in `src/api/tests/test_assistant_panel_a11y_159.py`: asserting pre-open `expanded == False` on `Chat size` before `Enter` expands it, dispatching `keydown` `{ key: "Enter" }` for non-`send` turns in `NODE_A11Y_HARNESS`, and hardening `_SyntheticWorkbenchHarness.close()` with nested `try/finally` blocks.

### User Decisions and Requirements Highlights

* Zero production web edits; preserve all historical critique and review records untouched.
* Focused-tier validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `git --no-pager diff --check`), followed by `Conformant` `rpi-review` and local `Refs #159` commit without pushing.

### What You May Not Know

* Recording `this._lastSubmit` inside `NODE_A11Y_HARNESS` `requestSubmit()` lets `input.dispatchEvent("keydown", { key: "Enter" })` drive `chat.js`'s real `keydown` listener while awaiting the resulting async submission deterministically.

### Unresolved Decisions or Blockers

* None.

## Sources

* .copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-polish-review.md
* src/api/tests/test_assistant_panel_a11y_159.py
* docs/reference/research/ux/wcag-conformance-baseline.md

## User Decisions and Requirements

* Resolve `RV-001` in `src/api/tests/test_assistant_panel_a11y_159.py` under Focused-tier validation.
* Test ownership lock:
  * Canonical edited file: `src/api/tests/test_assistant_panel_a11y_159.py`.
  * Exact removals: `none`.
  * Maximum new source/test files: `0`.

## Goals

* Close `RV-001` cleanly in `src/api/tests/test_assistant_panel_a11y_159.py`.

## Scope and Non-Goals

### In Scope

* Updating `_SyntheticWorkbenchHarness.close()`, `NODE_A11Y_HARNESS` non-`send` `Enter` turn dispatch, and pre-open `Chat size` `expanded == False` assertion in `src/api/tests/test_assistant_panel_a11y_159.py`.

### Non-Goals

* Modifying any production web/API/core/agent code or historical critique/review records.

## Functional Requirements

* FR-01: Resolve `RV-001` in `src/api/tests/test_assistant_panel_a11y_159.py`.
  * Observable acceptance criteria:
    * `_SyntheticWorkbenchHarness.close()` uses nested `try/finally` blocks so `sim_close()`, `self.app.assistants.stop()`, `self.store.db.close()`, and `shutil.rmtree(self.root, ignore_errors=True)` each execute even if an earlier step raises.
    * In `NODE_A11Y_HARNESS`, `requestSubmit()` stores `this._lastSubmit`, and non-`send` turns in `test_widget_keyboard_focus_and_live_region_lifecycle_with_real_payloads` clear `formEl._lastSubmit = undefined`, submit via `input.dispatchEvent("keydown", { key: "Enter" })` (`prevented === true`), and assert `assert.ok(askTask)` rather than calling `formEl.requestSubmit()` directly, while asserting `env.liveMutations` captured `role="log"`, `role="status"`, and `role="alert"` entries.
    * In `test_browser_launcher_keyboard_resize_dock_and_escape_focus`, CDP `Accessibility.getFullAXTree` asserts `expanded is False` on `DisclosureTriangle` `"Chat size"` before pressing `Enter` and `expanded is True` after pressing `Enter`.

## Non-Functional Requirements

* NFR-01: Pass `mypy`, `ruff check src/api`, `ruff format --check src/api`, Focused `unittest` suites, and `git --no-pager diff --check` with single-newline EOF across all files.

## Acceptance Criteria

* AC-01: `RV-001` is resolved and verified by Focused validation with zero lint, type, test, or whitespace issues.

## Phase Checklist

<!-- rpi:phase id=P01 status=completed -->
### [x] P01: Resolve `RV-001` in `src/api/tests/test_assistant_panel_a11y_159.py`

* Dependencies: None

<!-- rpi:task id=P01-T01 phase=P01 status=completed -->
* [x] P01-T01: Harden `_SyntheticWorkbenchHarness.close()` with `try/finally`, use `keydown` `Enter` (`formEl._lastSubmit = undefined` + `assert.ok(askTask)`) + `env.liveMutations` checks in `NODE_A11Y_HARNESS`, assert pre-open `Chat size` `expanded is False` in Chromium CDP AXTree, and run Focused validation.

## Critique Disposition

* Critique artifact: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-closeout-plan-critique.md
* Critique verdict: Revise (applied directly by planning parent; finalized without repeating critique)
* `PC-001` [Low] (`planning_parent`, applied directly): Replaced `env.liveEvents` with `env.liveMutations` (`createDomEnv()` property name) and added `formEl._lastSubmit = undefined` + `assert.ok(askTask)` before non-`send` `Enter` `keydown` dispatch.

## Follow-Up Items

* Optional Full-tier `.github/workflows/src-ci.yml` post-Chromium test step.
* Named human desktop screen-reader and zoom acceptance under Issues #151, #155, and #619 (`docs/reference/research/ux/production-ux-acceptance-protocol.md`).

## Handoff

* Changes record path: .copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-closeout-changes.md

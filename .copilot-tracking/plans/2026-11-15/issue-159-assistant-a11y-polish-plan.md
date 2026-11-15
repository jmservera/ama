<!-- markdownlint-disable-file -->
# RPI Plan: Issue #159 Conversational Assistant Accessibility Final Precision Polish (`RV-001`–`RV-002`)

## Task Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y-polish
* Task slug: issue-159-assistant-a11y-polish
* Parent task: 2026-11-15-issue-159-assistant-a11y-remediation
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-polish-plan-critique.md

## Executive Summary

This final precision polish resolves `RV-001` and `RV-002` from `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-remediation-review.md` so every statement in `docs/reference/research/ux/wcag-conformance-baseline.md` has an exact 1-for-1 assertion in `src/api/tests/test_assistant_panel_a11y_159.py`, `_SyntheticWorkbenchHarness.__init__` cleans up partial initialization safely, and all tracked and newly created files pass `git diff --cached --check` with single EOF newlines.

### User Decisions and Requirements Highlights

* Zero edits to production web files (`src/api/src/zava_forward/api/web/*`).
* Exact 1-for-1 parity between `wcag-conformance-baseline.md` prose and `test_assistant_panel_a11y_159.py` assertions.
* Focused-tier validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `git diff --cached --check`) followed by clean `rpi-review` and local `Refs #159` commit without pushing.

### What You May Not Know

* Chromium CDP `Accessibility.getFullAXTree` exposes `expanded` on `#employee-chat-launcher` (role `button`) and `<summary>` disclosures, and exposes `pressed` (`"false"` / `"true"`) on `Dock to right edge` (`aria-pressed`), allowing direct CDP AXTree verification alongside DOM `aria-expanded` / `aria-pressed` checks.
* Because `#employee-chat` is a stay-open non-modal panel (`stayOpen: true`, no `aria-modal="true"`), pressing `Tab` from `Send` moves focus out of `#employee-chat` into the underlying page without trapping keyboard users.

### Unresolved Decisions or Blockers

* None.

## Sources

* .copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-remediation-review.md
* src/api/tests/test_assistant_panel_a11y_159.py
* docs/reference/research/ux/wcag-conformance-baseline.md
* docs/reference/log.md

## User Decisions and Requirements

* Resolve `RV-001` and `RV-002` from `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-remediation-review.md` while preserving all historical critique and review records untouched.
* Validation tier: **Focused tier** (test-only and UX-doc edits; zero production, workflow, SQL, dependency, or Dockerfile edits).
* Test ownership lock:
  * Canonical edited files: `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md` (plus trailing-whitespace cleanup on current untracked `.copilot-tracking/` files only without altering historical critique/review verdicts or findings). Note: historical critique and review files remain untouched.
  * Exact removals: `none`.
  * Maximum new source/test files: `0`.

## Goals

* Achieve exact 1-for-1 correspondence between `docs/reference/research/ux/wcag-conformance-baseline.md` claims and `src/api/tests/test_assistant_panel_a11y_159.py` assertions (`RV-001`).
* Guard `_SyntheticWorkbenchHarness.__init__` partial-failure cleanup and ensure clean EOF formatting across deliverables (`RV-002`).

## Scope and Non-Goals

### In Scope

* Updating `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, and `docs/reference/log.md`.
* Running Focused-tier validation checks and checking EOF newline / whitespace hygiene.

### Non-Goals

* Modifying any production web/API/core/agent file or historical critique/review artifacts.

## Functional Requirements

* FR-01: Complete CDP `expanded`/`pressed`/`relevant`, forward/backward no-keyboard-trap `Tab`-exit, descendant-aware post-`403`/`401` `MutationObserver` read, `#employee-chat-question` `Enter` skill-turn submit + separate `Send` `Enter` submit, and exact `wcag-conformance-baseline.md` wording (`RV-001`, `PC-001`–`PC-003`).
  * Observable acceptance criteria:
    * `test_browser_launcher_keyboard_resize_dock_and_escape_focus` inspects CDP `Accessibility.getFullAXTree` to verify `expanded` (`False` when closed, `True` when open) on `#employee-chat-launcher` (`button` `"Chat"`), `expanded` (`True` when open) on `DisclosureTriangle` `"Chat size"`, and `pressed` (`"false"` before toggle, `"true"` after toggle) on `Dock to right edge` once `Chat size` is open; and proves zero focus trap in both directions (`Shift+Tab` from `Close chat` moves focus out of `#employee-chat` to `#employee-chat-launcher` and `#app`, and `Tab` past `Send` exits `#employee-chat` and wraps to `.skip-link`).
    * `LIVE_OBSERVER_INIT_SCRIPT` scans live-region descendants inside `addedNodes` (`added.querySelectorAll(...)`) so mounted container subtrees such as `app.js`'s `401` sign-in card are captured; `test_browser_case_assistant_axtree_live_announcements_and_keyboard_turns` asserts exact `log_props["relevant"] == "additions"`, submits the `ArrowDown` skill-selection turn via `Enter` directly from `#employee-chat-question` AND exercises `Enter` on `Send` on a separate refusal turn, and re-reads `window.__a11yLiveEvents` after the `403` and `401` flows to verify both `#workspace-status` `"Chat access ended..."` and `role="alert"` `"Your session has ended..."`.
    * `docs/reference/research/ux/wcag-conformance-baseline.md` matches every control, CDP property (`relevant: "additions"`), and Node-VM vs Chromium scenario 1-for-1.
* FR-02: Partial-init resource cleanup and single-newline EOF / staged whitespace hygiene (`RV-002`, `PC-004`).
  * Observable acceptance criteria: `_SyntheticWorkbenchHarness.__init__` cleans up `self.app`, `self.store`, and `self.root` inside `except BaseException:` before re-raising; `docs/reference/log.md` and all modified/created files end with a single `\n`; `git --no-pager diff --check` and `git --no-pager diff --cached --check` exit `0`.

## Non-Functional Requirements

* NFR-01: Pass `mypy --strict`, `ruff check src/api`, and `ruff format --check src/api`.

## Acceptance Criteria

* AC-01: `RV-001` and `RV-002` are fully resolved and verified by Focused-tier validation (`unittest`, `ruff`, `mypy`, `git --no-pager diff --check`, `git --no-pager diff --cached --check`, and single-`\n` EOF verification).

## Phase Checklist

<!-- rpi:phase id=P01 status=completed -->
### [x] P01: Final Test-to-Baseline Parity and Resource/EOF Hygiene (`RV-001`–`RV-002`)

* Dependencies: None

<!-- rpi:task id=P01-T01 phase=P01 status=completed -->
* [x] P01-T01: Add `_SyntheticWorkbenchHarness.__init__` partial-init cleanup, CDP `expanded`/`pressed` assertions, no-trap `Tab`-exit past `Send`, `#employee-chat-question` `Enter` skill submit + separate `Send` `Enter` refusal submit, and post-`403`/`401` `MutationObserver` assertions in `src/api/tests/test_assistant_panel_a11y_159.py`.
<!-- rpi:task id=P01-T02 phase=P01 status=completed -->
* [x] P01-T02: Align `docs/reference/research/ux/wcag-conformance-baseline.md` wording 1-for-1 with `test_assistant_panel_a11y_159.py`, restore single trailing `\n` on `docs/reference/log.md`, and run all Focused-tier + UX guard validations.

## Critique Disposition

* Critique artifact: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-polish-plan-critique.md
* Critique verdict: Revise (applied directly by planning parent; finalized without repeating critique)
* `PC-001` [High] (`planning_parent`, applied directly): Corrected launcher accessible name to `"Chat"` (`aria-label="Chat"`), checked `Dock to right edge` CDP `pressed` (`"false"` -> `"true"` tristate string) after opening `Chat size` `<details>`, checked boolean `expanded` on `"Chat"` launcher and `"Chat size"` `DisclosureTriangle`, and asserted exact `relevant == "additions"`.
* `PC-002` [High] (`planning_parent`, applied directly): Extended `LIVE_OBSERVER_INIT_SCRIPT` to scan live-region descendants inside `addedNodes` (`added.querySelectorAll(...)`) so mounted `401` sign-in `role="alert"` subtrees are recorded.
* `PC-003` [Medium] (`planning_parent`, applied directly): Specified both backward `Shift+Tab` exit (`Close chat` -> `#employee-chat-launcher` -> `#app`) and forward `Tab` exit past `Send` (wrapping to `.skip-link`).
* `PC-004` [Low] (`planning_parent`, applied directly): Added `git --no-pager diff --cached --check` and single-`\n` EOF checks to `FR-02`, `AC-01`, and `P01-T02`.

## Follow-Up Items

* Optional Full-tier `.github/workflows/src-ci.yml` post-Chromium test step.
* Named human desktop screen-reader and zoom acceptance under Issues #151, #155, and #619 (`docs/reference/research/ux/production-ux-acceptance-protocol.md`).

## Handoff

* Changes record path: .copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-polish-changes.md

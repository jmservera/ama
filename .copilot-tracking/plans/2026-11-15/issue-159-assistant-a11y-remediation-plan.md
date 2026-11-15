<!-- markdownlint-disable-file -->
# RPI Plan: Issue #159 Conversational Assistant Accessibility Review Remediation (`RV-001`–`RV-003`)

## Task Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y-remediation
* Task slug: issue-159-assistant-a11y-remediation
* Parent task: 2026-11-15-issue-159-assistant-a11y
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-remediation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan-critique.md

## Executive Summary

This child remediation plan resolves the three `rpi-implement` defects (`RV-001`, `RV-002`, and `RV-003`) identified by the parent post-implementation review (`.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-review.md`) prior to creating the local branch commit on `feat/ux-159-assistant-a11y`. It tightens `src/api/tests/test_assistant_panel_a11y_159.py` (clearing ambient simulation-lane environment variables, closing any simulation handle on teardown, adding `401` alongside `403` `deny()`, exercising keyboard `Close chat`, keyboard `#employee-chat-skill` selection, explicit `Shift+Enter` newline verification, rendered Chromium `revealBeside` scroll clearance, and dialog-subtree CDP AXTree scoping), aligns `docs/reference/research/ux/wcag-conformance-baseline.md` strictly with actual `chat-widget.js` controls and tested scenarios, removes the trailing EOF blank line in `docs/reference/log.md`, re-runs Focused-tier validation plus `test_ux_design_traceability.py` and `git diff --check`, and creates the local `Refs #159` commit after remediation review.

### User Decisions and Requirements Highlights

* Preserve zero edits to production web assets (`src/api/src/zava_forward/api/web/*`).
* Ensure every claim in `docs/reference/research/ux/wcag-conformance-baseline.md` matches actual widget controls and executed assertions in `src/api/tests/test_assistant_panel_a11y_159.py`.
* Run Focused-tier validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `test_ux_design_traceability.py`, and `git diff --check`) and commit all deliverables and `.copilot-tracking/` artifacts locally with `Refs #159` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.

### What You May Not Know

* `App(self.store, LOCAL_PASSWORD)` invokes `simulation_lane.Lane.open(os.environ, ...)`, which inspects `ZF_SIM_STORE` and `ZF_SIM_KEY_FILE`; explicitly clearing both in `APPROVED_CHAT_ENV` and closing `self.app.simulation` if present makes `_SyntheticWorkbenchHarness` immune to ambient developer/gate shell state.
* In Chromium CDP `Accessibility.getFullAXTree`, every AX node exposes `childIds` (or `parentId`), enabling exact subtree filtering from the `Employee assistant` `dialog` AX node so `status` and `alert` assertions cannot accidentally match `#workspace-status` or other page regions.

### Unresolved Decisions or Blockers

* None.

## Sources

* .copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md
* .copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-review.md
* src/api/src/zava_forward/api/web/chat-widget.js
* src/api/src/zava_forward/api/server.py
* src/api/tests/test_assistant_panel_a11y_159.py
* docs/reference/research/ux/wcag-conformance-baseline.md

## User Decisions and Requirements

* Remediate parent review findings `RV-001`, `RV-002`, and `RV-003` from `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-review.md` while preserving parent critique and review records unchanged as historical RPI evidence.
* Keep production web modules (`role-screens.js`, `panels.js`, `chat.js`, `chat-widget.js`, CSS) completely untouched.
* Validation tier classification: **Focused tier** — test-only and UX-documentation updates (`src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md`) with zero production, workflow, gate, SQL, dependency, or Dockerfile changes.
* Test ownership lock:
  * Canonical edited files: `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md`.
  * Exact removals: `none`.
  * Maximum new test/source file additions: `0` (in-place refinement of `src/api/tests/test_assistant_panel_a11y_159.py`).
  * Semantic vs regression coverage: semantic behavioral assertions in `test_assistant_panel_a11y_159.py`; regression guard suites in `test_accessibility_baseline.py`, `test_content_standard.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`, `test_epic149_ux_evidence_results.py`, and `test_live_doc_links.py`.
* Commit locally after remediation review using repo-local `{id}+{login}@users.noreply.github.com` from `gh api user`, `Refs #159`, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, with zero `.copilot-tracking/` paths in the commit message. Do NOT push.

## Goals

* Resolve `RV-002` and `RV-003` in `src/api/tests/test_assistant_panel_a11y_159.py` so both Node-VM and headless Chromium tests hermetically isolate environment variables and verify every documented keyboard, focus, scroll-clearance, session-loss (`401` and `403`), and dialog-scoped AXTree behavior.
* Resolve `RV-001` in `docs/reference/research/ux/wcag-conformance-baseline.md` and `docs/reference/log.md` so every documented control and check matches `chat-widget.js` and `test_assistant_panel_a11y_159.py` verbatim and `git diff --check` exits `0`.
* Pass all Focused-tier validation checks and record clean `rpi-review` conformance before creating the local Git commit.

## Scope and Non-Goals

### In Scope

* Updating `src/api/tests/test_assistant_panel_a11y_159.py` for `RV-002` and `RV-003`.
* Updating `docs/reference/research/ux/wcag-conformance-baseline.md` and `docs/reference/log.md` for `RV-001`.
* Re-running Focused-tier validation commands (`unittest`, `test_ux_design_traceability.py`, `ruff check`, `ruff format --check`, `mypy`, `git diff --check`).

### Non-Goals

* Modifying any production web, API, agent, core, or `.github/workflows/` file.
* Pushing to `origin` or claiming human desktop screen-reader execution.

## Functional Requirements

* FR-01: Hermetic simulation-store isolation and resource teardown (`RV-003`).
  * Observable acceptance criteria: `APPROVED_CHAT_ENV` sets `ZF_SIM_STORE: ""` and `ZF_SIM_KEY_FILE: ""`; `_SyntheticWorkbenchHarness.close()` closes `self.app.simulation` if non-`None`.
* FR-02: Complete Chromium keyboard, scroll-clearance, `401`+`403` auth/access-loss, and dialog-subtree AXTree assertions (`RV-002`, `PC-001`, `PC-002`).
  * Observable acceptance criteria: `AssistantPanelNodeA11y159Tests` verifies both `401` and `403` `chat.js` `deny()` recovery (`#employee-chat` hides, focus moves to `#app`, `#workspace-status` announces `"Chat access ended. Reopen from a record you can see, or sign in again."`); `AssistantPanelBrowserA11y159Tests` exercises keyboard `Close chat` activation (`Enter` closes `#employee-chat` and restores focus to `#employee-chat-launcher`), rendered `revealBeside` scroll clearance in Chromium (in-viewport `position: absolute` focus target behind floating `#employee-chat` advances `window.scrollY > 0` and behind docked `#employee-chat` advances `window.scrollX > 0`), keyboard `#employee-chat-skill` change via `ArrowDown` to a non-`general` permitted skill followed by `Shift+Tab` to `#employee-chat-question` and `Enter` submit with `Skill:` attribution verified in the assistant article, explicit `"\n" in question.input_value()` after `Shift+Enter`, both `403` `deny()` (`#workspace-status` `"Chat access ended. Reopen from a record you can see, or sign in again."` + focus `#app`) and `401` `app.js` session-expiry recovery (sign-in `role="alert"` `"Your session has ended. Sign in again."` + focus `#app`, whitelisting `"chat-http:401:"`), and `dialog`-subtree scoping of CDP AXTree `status` (while non-empty) and `alert` nodes via full-tree `childIds` traversal (traversing `ignored` intermediate wrappers).
* FR-03: Exact UX documentation alignment and whitespace hygiene (`RV-001`).
  * Observable acceptance criteria: `docs/reference/research/ux/wcag-conformance-baseline.md` contains zero references to nonexistent `S`/`M`/`L` resize presets, describes only controls and scenarios actually present in `chat-widget.js` and tested in `test_assistant_panel_a11y_159.py`, and `git --no-pager diff --check` exits `0` across all modified files including `docs/reference/log.md`.

## Non-Functional Requirements

* NFR-01: Pass `mypy` (`--strict`), `ruff check src/api`, and `ruff format --check src/api` (`<= 100` character lines, zero `# type: ignore`).
* NFR-02: Preserve all UX guard assertions (`test_accessibility_baseline.py`, `test_content_standard.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`, `test_epic149_ux_evidence_results.py`, `test_live_doc_links.py`).

## Acceptance Criteria

* AC-01: `RV-001`, `RV-002`, and `RV-003` are fully resolved in `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, and `docs/reference/log.md` with zero production web edits.
* AC-02: Caller `unittest` command, `test_ux_design_traceability.py` + UX/chat/doc regression suites, `ruff check src/api`, `ruff format --check src/api`, `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`, and `git --no-pager diff --check` all exit `0`.

## Phase Checklist

<!-- rpi:phase id=P01 status=completed -->
### [x] P01: Remediate Test Hermeticity, Scoped Browser Assertions, and UX Baseline Accuracy (`RV-001`–`RV-003`)

* Dependencies: None
* Execution posture: Primary implementation agent executes `P01-T01` then `P01-T02` sequentially (`P01-T02` depends on exact scenario parity from `P01-T01`).

<!-- rpi:task id=P01-T01 phase=P01 status=completed -->
* [x] P01-T01: Harden `_SyntheticWorkbenchHarness` env isolation (`ZF_SIM_STORE`, `ZF_SIM_KEY_FILE`), add `401` + `403` `deny()` coverage, and add keyboard `Close chat`, keyboard `#employee-chat-skill` change, explicit `Shift+Enter` `"\n"` assertion, Chromium `revealBeside` scroll clearance, and dialog-subtree CDP AXTree scoping in `src/api/tests/test_assistant_panel_a11y_159.py` (`RV-002`, `RV-003`).
<!-- rpi:task id=P01-T02 phase=P01 status=completed -->
* [x] P01-T02: Align `docs/reference/research/ux/wcag-conformance-baseline.md` with actual `chat-widget.js` controls and `test_assistant_panel_a11y_159.py` assertions, fix `docs/reference/log.md` EOF whitespace (`RV-001`), and run all Focused-tier + traceability + `git diff --check` validations.

## Critique Disposition

* Critique artifact: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan-critique.md
* Critique verdict: Revise (applied directly by planning parent; finalized without repeating critique)
* `PC-001` [High] (`planning_parent`, applied directly): Corrected exact `#workspace-status` `403` copy (`"Chat access ended. Reopen from a record you can see, or sign in again."`), distinguished Chromium `app.js` `401` interception (`login("Your session has ended. Sign in again.")` rendering a sign-in `role="alert"` and focusing `#app`) from `403` `chat.js` `deny()` (while testing both `401` and `403` in Node-VM `deny()` and both `403` and `401` in Chromium), and added `"chat-http:401:"` to `_open_authenticated_page`'s expected error whitelist.
* `PC-002` [Medium] (`planning_parent`, applied directly): Specified `ArrowDown` on `#employee-chat-skill` followed by `Shift+Tab` to `#employee-chat-question` + `Enter` submit (since `<select>` `Enter` does not submit forms in Chromium), specified in-viewport `position: absolute` target placement with scrollable document extent for deterministic `revealBeside` `scrollY`/`scrollX` checks, and required full-AXTree `childIds` traversal (including `ignored` wrapper nodes) while `.chat-widget-status` is non-empty.

## Follow-Up Items

* Optional Full-tier CI workflow enhancement (`RV-004`): invoke `AssistantPanelBrowserA11y159Tests` after `playwright install chromium` in `.github/workflows/src-ci.yml` in a dedicated workflow PR with a Full-tier gate receipt.
* Named human desktop screen-reader and zoom acceptance (`NVDA` + `Firefox`, `VoiceOver` + `Safari`, `200%`/`400%` zoom) under Issues #151, #155, and #619 (`docs/reference/research/ux/production-ux-acceptance-protocol.md`).

## Handoff

* Changes record path: .copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-remediation-changes.md
* Post-review local commit step: After child `rpi-review` completes conformantly and child/parent RPI session state records are finalized, configure repo-local `user.email` via `gh api user` (`{id}+{login}@users.noreply.github.com`) and commit all branch deliverables and `.copilot-tracking/` artifacts locally (`Refs #159`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, zero `.copilot-tracking/` strings in the commit message) without pushing.

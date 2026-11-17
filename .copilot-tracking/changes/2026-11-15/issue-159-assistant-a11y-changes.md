<!-- markdownlint-disable-file -->
# RPI Changes: Issue #159 Conversational Assistant Panel Accessibility Verification

## Metadata

* Task ID: issue-159-assistant-a11y
* Related plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: All planned tasks (`P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`) completed with verified test, lint, type-check, and UX documentation guard evidence; zero production web files modified.
* Approved write boundary: `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`, and `.copilot-tracking/` `2026-11-15` artifacts (`src/api/src/zava_forward/api/web/*` untouched).
* Validation tier classification and basis: **Focused tier** — adds one focused accessibility test module (`src/api/tests/test_assistant_panel_a11y_159.py`) and updates UX knowledge-base documentation (`docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`); modifies zero production web/API/agent/core modules, workflows, gate tools, SQL schemas, dependencies, or Dockerfiles.

## Execution Summary

Delivered `src/api/tests/test_assistant_panel_a11y_159.py` with dual-layer verification (`AssistantPanelNodeA11y159Tests` + `AssistantPanelBrowserA11y159Tests`), recorded the dated `2026-11-15` Issue #159 verification boundary in `docs/reference/research/ux/wcag-conformance-baseline.md` alongside `docs/reference/README.md` and `docs/reference/log.md`, and verified all Focused-tier unit, browser, lint, formatting, strict `mypy`, and UX/documentation regression checks with zero production web edits.

## Completed Work

### P01: Conversational Assistant Keyboard, Focus, and Live-Region Verification Suite (`P01-T01`, `P01-T02`)

* Added `src/api/tests/test_assistant_panel_a11y_159.py` (5 test cases across 2 `unittest.TestCase` classes; strictly typed under `mypy --strict` with zero `# type: ignore` suppressions; zero edits to `chat-widget.js`, `chat.js`, `role-screens.js`, `panels.js`, or stylesheets):
  * `AssistantPanelNodeA11y159Tests` (`P01-T01`, unconditional Node `vm` + real Python `SqlStore` / `ChatPanel` / `Assistants.invoke` integration on synthetic `role_matrix_fixture.build()` seed):
    * `test_real_backend_payload_shapes_cover_answer_refused_withheld_and_fallback`: verifies real `ChatPanel` replies across `answer` (cited case facts), `refused` (`"Approve this case"`), `withheld` (ungrounded mutation prose blocked), and `fallback` (timeout workflow-only help) plus `Assistants.invoke` proposal queueing.
    * `test_widget_keyboard_focus_and_live_region_lifecycle_with_real_payloads`: executes `chat-widget.js` and `chat.js` against the real backend payloads, verifying `aria-expanded` and `heading.focus()` on open, keyboard shortcuts (`Enter` submit, `Shift+Enter` newline, IME `isComposing` and `keyCode === 229` suppression, `Escape` close), `busy(true)` moving focus from `Send` back to `#employee-chat-question` before disabling `Send`, focus preservation across `Send`, `role="log"`, `Sources (N)`, and external controls, distinct polite `role="status"` announcements for `answer`, `refused`, `withheld`, and `fallback`, polite `role="alert"` on blank input and `500` outage with preserved draft, `S`/`M`/`L` and width/height range resizing, `revealBeside` vertical/horizontal overlap scroll clearance, and docked `Escape` un-hiding `#employee-chat-launcher` before focusing it.
    * `test_case_panel_proposal_announcements_and_access_loss_focus_recovery`: verifies `#chat-panel > p[role="status"]` proposal-request announcements disambiguated from `#regulatory-chat`, case-scoped `Open chat`, and `403` `deny()` resetting `#employee-chat`, announcing `"Chat access ended. Reopen from a record you can see, or sign in again."` on `#workspace-status`, and shifting focus to `#app`.
  * `AssistantPanelBrowserA11y159Tests` (`P01-T02`, rendered headless Chromium Playwright + CDP `Accessibility.getFullAXTree` + `MutationObserver` against loopback `App`):
    * `test_browser_launcher_keyboard_resize_dock_and_escape_focus`: verifies the 3px two-tone `:focus-visible` ring on `#employee-chat-launcher`, `Enter` and `Space` open to `#employee-chat-title`, `Tab` traversal through `Close chat`, `About this chat` (`Space`), `Chat size` (`Enter`), `Dock to right edge`, `#employee-chat-width` (`ArrowRight` -> `41vw`), `#employee-chat-height` (`ArrowRight` -> `81dvh`), `S`/`M`/`L` presets (`aria-pressed`), `revealBeside` vertical and horizontal scroll clearance in Chromium, docked `launcher.is_hidden()`, and `Escape` restoring focus to `#employee-chat-launcher`.
    * `test_browser_case_assistant_axtree_live_announcements_and_keyboard_turns`: opens a fresh isolated session on `#/case/ZF-1?tab=ai`, expands `#chat-panel` via keyboard, triggers `Request proposal` and verifies `#chat-panel > p[role="status"]`, opens case-scoped `#employee-chat` (`Context: case ZF-1.`), inspects Chromium's computed `Accessibility.getFullAXTree` (`dialog`, `log` with `live: "polite"` and `relevant: "additions text"`, `textbox` with `aria-describedby` warning description, `combobox`, `button`, `status` and `alert` with `live: "polite"` and `atomic: true`), verifies full `Tab` / `Shift+Tab` order, blank-input `role="alert"`, `Shift+Enter` vs `Enter` case-grounded `answer` turn, `Sources (N)` keyboard disclosure expansion, `Send`-button `Enter` `refused` turn, `500` transport outage `role="alert"` with preserved draft, `MutationObserver` live-region event capture, `Escape` return to `#employee-chat-launcher`, and `403` `deny()` focus recovery to `#app` with `#workspace-status` announcement.

### P02: UX Verification Record, Guard Reconciliation, and Focused Validation (`P02-T01`, `P02-T02`)

* Updated `docs/reference/research/ux/wcag-conformance-baseline.md` (`P02-T01`):
  * Aligned `Audit` table notes for `Keyboard` (`2.1.1, 2.1.2, 2.4.3`), `Name, role, value` (`4.1.2`), `Status messages` (`4.1.3`), and `Focus not obscured, dragging movements` (`2.4.11, 2.5.7`) with dated `2026-11-15 (#159)` automated evidence notes.
  * Added `## Conversational assistant panel keyboard and live-region check (2026-11-15, #159)` documenting the dual-layer `src/api/tests/test_assistant_panel_a11y_159.py` coverage while preserving `Not run` manual cells, non-conformance wording, and open human NVDA/Firefox, VoiceOver/Safari, 320 px reflow, and 400% zoom gates (#151, #155, #619).
* Updated `docs/reference/README.md` row for `wcag-conformance-baseline.md` and appended a dated `2026-11-15` entry to `docs/reference/log.md` (`P02-T01`).
* Executed all Focused-tier validation and regression suites (`P02-T02`).

## Implementation-Time Plan and Detail Updates

* Local judgment (`role_matrix_fixture.build()` + `CHAT_WARNING`): `test_mvp.DATA["staff"]` uses legacy short role strings before `role_matrix_fixture.build()` expands `projection.STAFF_ROLES` (`Retrofit Coordinator`), and `/api/chat/status` sources `warning` from `zava_forward.core.chat_privacy.WARNING`. `test_assistant_panel_a11y_159.py` uses the typed `role_matrix_fixture.build()` synthetic seed and `CHAT_WARNING` directly, preserving approved synthetic-only, zero-production-edit plan intent.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Caller `unittest` (`test_assistant_panel_a11y_159.py`, `test_accessibility_baseline.py`, `test_content_standard.py`) | `src/api/tests` | Passed | `Ran 48 tests in 9.222s — OK` (including all 5 new Node-VM and headless Chromium tests in `test_assistant_panel_a11y_159.py`, 0 skipped) |
| UX/chat/documentation regression `unittest` (`test_chat_panel`, `test_chat_widget_focus`, `test_home_chat_regulatory_keyboard_provenance`, `test_production_ux_acceptance_protocol`, `test_epic149_ux_evidence_results`, `test_screen_design_traceability`, `test_live_doc_links`) | `src/api/tests`, `src/core/tests` | Passed | `Ran 121 tests in 68.515s — OK (skipped=1)` |
| `python3 -m ruff check src/api` & `python3 -m ruff format --check src/api` | `src/api` | Passed | `All checks passed!` and `209 files already formatted` |
| `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` | `src/api` | Passed | `Success: no issues found in 293 source files` |
| Hosted GitHub Actions CI | Remote PR/branch | Not run (blocked by caller `Do NOT push` instruction) | Local-only branch per explicit user instruction; hosted CI runs after future owner push |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all checked `[x]`).
* Completed-work evidence and handoff prose: Synchronized with actual `test_assistant_panel_a11y_159.py` implementation and UX documentation edits.
* Validation, blockers, remaining work, and follow-up items: Focused-tier validation passed; zero active implementation blockers; zero remaining plan markers; human desktop AT/zoom acceptance preserved in `## Follow-Up Items`.
* Review readiness: Ready for one-pass `rpi-review`.

## Blockers

* None for implementation or local Focused-tier validation. Human desktop assistive-technology execution (NVDA/Firefox, VoiceOver/Safari) and 400% zoom acceptance remain external owner/human gates (#151, #155, #619), so commits use `Refs #159` rather than closing #159.

## Remaining Work

* None in declared plan scope (`P01` and `P02` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-plan.md, `## Follow-Up Items`
* Named human desktop screen-reader (NVDA + Firefox on Windows; VoiceOver + Safari on macOS), 400% zoom, and multi-role acceptance execution (`docs/reference/research/ux/production-ux-acceptance-protocol.md`), outside headless automation scope, owned by project owner and named testers (#151, #155, #619).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`, `P02`); completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: Focused tier passed (`48` caller tests OK, `121` regression tests OK, `ruff check` OK, `ruff format --check` OK, `mypy --strict` OK across 293 files)
* Blockers: None
* Current plan and detail updates: All phase and task checkboxes marked `[x]`
* Planning and critique state: Ready (`PC-001` through `PC-003` resolved in one-pass critique)
* Follow-up items: Human desktop NVDA/VoiceOver and 400% zoom acceptance (#151, #155, #619)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Automatic RPI Agent parent continues directly to `rpi-review`

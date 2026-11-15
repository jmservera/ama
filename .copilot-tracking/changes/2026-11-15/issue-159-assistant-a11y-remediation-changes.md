<!-- markdownlint-disable-file -->
# RPI Changes: Issue #159 Conversational Assistant Accessibility Review Remediation (`RV-001`–`RV-003`)

## Task Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y-remediation
* Task slug: issue-159-assistant-a11y-remediation
* Parent task: 2026-11-15-issue-159-assistant-a11y
* Status: Complete
* Date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-remediation-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan-critique.md
* Declared invocation scope: Full plan (`P01`: `P01-T01`, `P01-T02`)

## Opening Implementation State

* Active execution item: `P01` (`P01-T01`, `P01-T02`) — Complete
* Active write boundary: `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md` (zero edits to production web files)
* Initial blockers: None

## Completed Work

### P01: Remediate Test Hermeticity, Scoped Browser Assertions, and UX Baseline Accuracy (`RV-001`–`RV-003`)

* `P01-T01` (`src/api/tests/test_assistant_panel_a11y_159.py`):
  * Cleared `ZF_SIM_STORE` and `ZF_SIM_KEY_FILE` in `APPROVED_CHAT_ENV` and closed `self.app.simulation` defensively in `_SyntheticWorkbenchHarness.close()` (`RV-003`).
  * Added `401` alongside `403` `chat.js` `deny()` verification in `AssistantPanelNodeA11y159Tests` (`#employee-chat` disposed, `#workspace-status` `"Chat access ended. Reopen from a record you can see, or sign in again."`, focus moved to `#app`).
  * Expanded `AssistantPanelBrowserA11y159Tests` (`RV-002`, `PC-001`, `PC-002`):
    * Activated `Close chat` via `Enter` key (`panel` hides, `aria-expanded == "false"`, focus restored to `#employee-chat-launcher`) before re-opening via `Space`.
    * Added rendered Chromium `revealBeside` overlap scroll-clearance verification while floating (`window.scrollY > 0` and `afterBox.bottom <= afterPanel.top`) and while docked (`window.scrollX > 0` and `afterBox.right <= afterPanel.left`).
    * Added `_dialog_ax_subtree` walking `childIds` across all CDP `Accessibility.getFullAXTree` nodes (including `ignored` wrapper nodes) so `log`, `textbox`, `combobox`, `button`, `status` (`len == 1` while non-empty), and `alert` (`len == 1` when visible) assertions are strictly scoped to the `Employee assistant` `dialog` subtree.
    * Added explicit `"\n" in question.input_value()` check after `Shift+Enter`, keyboard `#employee-chat-skill` selection via `ArrowDown` + `Shift+Tab` + `Enter` submit verifying `f"Skill: {selected_skill}."` in the rendered reply, and `401` `app.js` session-expiry verification (`"Your session has ended. Sign in again."` in `#app [role="alert"]` and focus on `#app`) alongside `403` `deny()`.
* `P01-T02` (`docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md`):
  * Removed the nonexistent `S`/`M`/`L` resize preset reference from `docs/reference/research/ux/wcag-conformance-baseline.md` and aligned both the `Status messages` audit row and `## Conversational assistant panel keyboard and live-region check (2026-11-15, #159)` strictly with actual `chat-widget.js` controls and `test_assistant_panel_a11y_159.py` assertions (`RV-001`).
  * Removed the trailing blank line at EOF in `docs/reference/log.md` (`RV-001`).

## Implementation-Time Plan and Detail Updates

* None; implementation followed `P01-T01` and `P01-T02` after applying critique dispositions `PC-001` and `PC-002`.

## Validation Evidence

| Command | Scope | Result | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_assistant_panel_a11y_159.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py -q` | `src/api/tests` | Passed | `Ran 48 tests in 7.445s — OK` (5/5 tests in `test_assistant_panel_a11y_159.py`, 0 skipped) |
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_ux_design_traceability.py src/api/tests/test_screen_design_traceability.py src/api/tests/test_epic149_ux_journey_requirement_traceability.py src/api/tests/test_epic149_ux_evidence_results.py src/api/tests/test_production_ux_acceptance_protocol.py src/api/tests/test_chat_panel.py src/api/tests/test_chat_widget_focus.py src/api/tests/test_home_chat_regulatory_keyboard_provenance.py src/core/tests/test_live_doc_links.py -q` | `src/api/tests`, `src/core/tests` | Passed | `Ran 138 tests in 80.208s — OK (skipped=1)` |
| `python3 -m ruff check src/api` | `src/api` | Passed | `All checks passed!` |
| `python3 -m ruff format --check src/api` | `src/api` | Passed | `209 files already formatted` |
| `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` | `src/api` | Passed | `Success: no issues found in 293 source files` |
| `git --no-pager diff --check` | Working tree | Passed | Exit code `0`, zero whitespace/EOF errors |

## Blockers and Remaining Work

* Blockers: None.
* Remaining active plan work: None (`P01`, `P01-T01`, and `P01-T02` are all `[x]`).

## Follow-Up Items

* Optional Full-tier CI workflow enhancement (`RV-004`): invoke `AssistantPanelBrowserA11y159Tests` after `playwright install chromium` in `.github/workflows/src-ci.yml`.
* Named human desktop screen-reader and zoom acceptance (`NVDA` + `Firefox`, `VoiceOver` + `Safari`, `200%`/`400%` zoom) under Issues #151, #155, and #619 (`docs/reference/research/ux/production-ux-acceptance-protocol.md`).

## Review Handoff

* Review readiness: Ready (`P01` complete, all Focused-tier + traceability + `git diff --check` checks passing, zero `.copilot-tracking/` references in `src/` or `docs/`).

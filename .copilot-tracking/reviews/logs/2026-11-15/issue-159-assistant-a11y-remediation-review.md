<!-- markdownlint-disable-file -->
# RPI Review: Issue #159 Conversational Assistant Accessibility Review Remediation (`RV-001`–`RV-003`)

## Scope and Evidence

* Task ID: 2026-11-15-issue-159-assistant-a11y-remediation
* Task slug: issue-159-assistant-a11y-remediation
* Parent task: 2026-11-15-issue-159-assistant-a11y
* Review date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-remediation-phase-details.md
* Latest plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-remediation-changes.md
* Parent review record: .copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-review.md
* Research: .copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md

## Opening Review State

* Active review target: `P01` (`P01-T01`, `P01-T02`) remediation of `RV-001`, `RV-002`, and `RV-003` plus Focused-tier validation
* Active read-only boundaries: This review stage creates and updates only `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-remediation-review.md` (and session state); it makes no edits to `src/`, `docs/`, plan, details, critique, research, or changes artifacts.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full single-pass review on 2026-11-15 across `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan.md`, `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-remediation-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-remediation-changes.md`, `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md`, refreshed Web Interface Guidelines (`vercel-labs/web-interface-guidelines`), and an independent read-only review lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01: Remediate Test Hermeticity, Scoped Browser Assertions, and UX Baseline Accuracy` | Partial | Core `RV-002`, `RV-003`, and `PC-001` checks pass (`48` + `138` tests, `ruff`, `mypy`), but `wcag-conformance-baseline.md` still overstates four minor details relative to `test_assistant_panel_a11y_159.py` (CDP AXTree `expanded`/`pressed` properties, no-keyboard-trap `Tab` exit past `Send`, post-`403`/`401` `MutationObserver` read, and Node-VM `!prevented` vs Chromium newline insertion), `PC-002` skill-turn submit pressed `Enter` on `Send` rather than `#employee-chat-question`, `_SyntheticWorkbenchHarness.__init__` lacks `try/except` partial-init cleanup, and `docs/reference/log.md` lost its final trailing newline (`RV-001`, `RV-002`). |
| `## Follow-Up Items` | `Follow-Up Items` (`RV-004` CI step + human AT/zoom acceptance under #151, #155, #619) | Reconciled | Properly retained outside active automated scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/tests/test_assistant_panel_a11y_159.py` | Cleared `ZF_SIM_STORE`/`ZF_SIM_KEY_FILE`, closed `simulation`, added Node-VM `401`+`403`, Chromium `Close chat` `Enter`, Chromium `revealBeside` vertical/horizontal scroll clearance, dialog-subtree AXTree scoping, `Shift+Enter` `"\n"` check, `ArrowDown` skill selection, and Chromium `403` + `401` recovery. | 5/5 tests pass in `7.445s`; `ruff` and `mypy --strict` pass. | Passed | Minor precision gaps (`RV-001`, `RV-002`): assert CDP `expanded`/`pressed`, `Tab` past `Send` exits dialog (proving no trap), read `MutationObserver` after `403`/`401` too, test both `Enter` from `#employee-chat-question` after skill change and `Enter` from `Send`, and guard `_SyntheticWorkbenchHarness.__init__` cleanup. |
| `P01-T02` | `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md` | Removed nonexistent `S`/`M`/`L` preset mention and aligned baseline prose; ran `48` + `138` tests, `ruff`, `mypy`, and `git diff --check`. | All commands exited `0`. | Passed | Align remaining four prose nuances in `wcag-conformance-baseline.md` and restore final `\n` at EOF in `docs/reference/log.md` (`RV-001`, `RV-002`). |

## Implementation-Time Plan and Detail Update Assessment

* None recorded; minor execution variance on `PC-002` (`Enter` on `Send` vs `#employee-chat-question`) is captured in `RV-001`.

## Critique and Material Revision Assessment

* Critique dispositions `PC-001` and `PC-002` were recorded in `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-remediation-plan.md`; `PC-001` was fully implemented and `PC-002`'s exact `#employee-chat-question` `Enter` submit step is tightened in `RV-001`. Zero production web files were modified (`✓ pass` under Web Interface Guidelines).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Optional Full-tier `.github/workflows/src-ci.yml` post-Chromium test step | Modifies workflow file, which requires Full gate tier outside caller's Focused tier. | Future Full-tier workflow PR. | Distinct follow-up. |
| Named human desktop screen-reader and zoom acceptance (#151, #155, #619) | Headless shared Linux host lacks desktop AT/audio/human testers. | Project owner and named human testers (`production-ux-acceptance-protocol.md`). | Distinct follow-up. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Complete exact 1-for-1 alignment between `wcag-conformance-baseline.md` claims and `test_assistant_panel_a11y_159.py` assertions

* Related scope: `P01-T01`, `P01-T02`
* Evidence: `docs/reference/research/ux/wcag-conformance-baseline.md` (`Keyboard`, `Name, role, value`, and `## Conversational assistant panel keyboard and live-region check (2026-11-15, #159)`) and `src/api/tests/test_assistant_panel_a11y_159.py`
* Impact: Four small claim-to-test discrepancies remain: (1) `Name, role, value` attributes `aria-expanded` / `aria-pressed` verification to CDP `Accessibility.getFullAXTree` when those states were checked on DOM attributes rather than CDP AX node properties (`expanded` / `pressed`); (2) `Keyboard` claims `without trap`, which should be directly proven in Chromium by tabbing past `Send` out of `#employee-chat`; (3) `window.__a11yLiveEvents` is inspected before the `403` and `401` flows rather than also asserting their live-region mutations afterwards, and `wcag-conformance-baseline.md` quotes `relevant: "additions text"` verbatim rather than asserting the exact `log_props["relevant"]` value; and (4) after `ArrowDown` + `Shift+Tab` on `#employee-chat-skill`, the test tabbed to `Send` instead of submitting via `Enter` from `#employee-chat-question` (`PC-002`), and Node-VM `Shift+Enter` checks `defaultPrevented === false` (non-submit) rather than character insertion.
* Destination: `rpi-implement`
* Smallest useful next action: Assert CDP `expanded` (on launcher/disclosures) and `pressed` (on `Dock to right edge`) in `Accessibility.getFullAXTree`, assert `Tab` past `Send` moves focus outside `#employee-chat` (no keyboard trap), assert `MutationObserver` captures `#workspace-status` (`403`) and `#app [role="alert"]` (`401`) after those steps, submit the skill-change turn via `Enter` from `#employee-chat-question` while also testing `Send`-button `Enter` on a separate turn, and word Node-VM `Shift+Enter` / `scrollBy` accurately in `wcag-conformance-baseline.md`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Guard `_SyntheticWorkbenchHarness.__init__` partial-failure cleanup and ensure single trailing newline across `docs/reference/log.md` and tracking files

* Related scope: `P01-T01`, `P01-T02`
* Evidence: `src/api/tests/test_assistant_panel_a11y_159.py` (`_SyntheticWorkbenchHarness.__init__`), `docs/reference/log.md` (EOF lacks trailing `\n`), and untracked `.copilot-tracking/` files
* Impact: If `_SyntheticWorkbenchHarness.__init__` raises after creating `self.root` or `self.store`, `addClassCleanup(cls.wb.close)` has not yet run; guarding `__init__` with `try/except` avoids leaking temp dirs/SQLite handles. Also, `docs/reference/log.md` should end with a single newline (`\n`) and staged new files should pass `git diff --cached --check`.
* Destination: `rpi-implement`
* Smallest useful next action: Wrap `_SyntheticWorkbenchHarness.__init__` resource acquisition in `try/except` cleanup, ensure `docs/reference/log.md` ends with exactly one `\n`, and verify `git diff --cached --check` across all staged tracked and newly added files before committing.

## Defects

* `RV-001` [Medium] -> `rpi-implement`
* `RV-002` [Low] -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child polish loop: add CDP `expanded`/`pressed`, no-trap `Tab`-exit, post-`403`/`401` `MutationObserver` check, and `#employee-chat-question` `Enter` skill submit in `test_assistant_panel_a11y_159.py` + exact wording in `wcag-conformance-baseline.md`. | Test/doc precision alignment inside scope. |
| `RV-002` | `rpi-implement` | Child polish loop: guard `_SyntheticWorkbenchHarness.__init__` partial-init cleanup, restore single EOF `\n` on `docs/reference/log.md`, and verify `git diff --cached --check`. | Resource hygiene and EOF formatting defect inside scope. |

Later implementation of a routed finding does not require another Review of this completed task.

## Residual Work

* Optional Full-tier `.github/workflows/src-ci.yml` post-Chromium test step.
* Named human desktop screen-reader and zoom acceptance under Issues #151, #155, and #619 (`docs/reference/research/ux/production-ux-acceptance-protocol.md`).

## Blockers and Remaining Work

* Blockers: None.
* Remaining active work: None in this task; `RV-001` and `RV-002` route to the final polish loop before local branch commit.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_assistant_panel_a11y_159.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py -q` | `src/api/tests` | Passed | `Ran 48 tests in 7.445s — OK` |
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_ux_design_traceability.py src/api/tests/test_screen_design_traceability.py src/api/tests/test_epic149_ux_journey_requirement_traceability.py src/api/tests/test_epic149_ux_evidence_results.py src/api/tests/test_production_ux_acceptance_protocol.py src/api/tests/test_chat_panel.py src/api/tests/test_chat_widget_focus.py src/api/tests/test_home_chat_regulatory_keyboard_provenance.py src/core/tests/test_live_doc_links.py -q` | `src/api/tests`, `src/core/tests` | Passed | `Ran 138 tests in 80.208s — OK (skipped=1)` |
| `python3 -m ruff check src/api` & `python3 -m ruff format --check src/api` | `src/api` | Passed | `All checks passed!` and `209 files already formatted` |
| `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` | `src/api` | Passed | `Success: no issues found in 293 source files` |
| `git --no-pager diff --check` | Tracked diff | Passed | Exit code `0` (`RV-002` notes missing final `\n` on `log.md` and untracked file check) |

## Outcome

* Outcome: Defects found
* Outcome rationale: Core `RV-001`–`RV-003` remediations pass all automated suites, `ruff`, and `mypy --strict`, with two small remaining test/documentation precision items (`RV-001` [Medium], `RV-002` [Low]) routed to `rpi-implement` prior to local branch commit.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Resolve `RV-001` and `RV-002` in `test_assistant_panel_a11y_159.py`, `wcag-conformance-baseline.md`, and `log.md`, verify `git diff --cached --check`, and commit locally (`Refs #159`). |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up | Optional Full-tier `src-ci.yml` browser step and human desktop AT/zoom acceptance (#151, #155, #619). |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: `48` caller tests, `138` regression tests, `ruff check`, `ruff format --check`, `mypy --strict`, and tracked `git diff --check` passed.
* Blockers: None.

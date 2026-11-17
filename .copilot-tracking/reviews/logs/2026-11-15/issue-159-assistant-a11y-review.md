<!-- markdownlint-disable-file -->
# Review: Issue #159 Conversational Assistant Panel Accessibility Verification

## Scope and Evidence

* Task ID: 2026-11-15-issue-159-assistant-a11y
* Review date: 2026-11-15
* Review scope: Full task (`P01` and `P02`: `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Automated keyboard operability, focus management, computed browser accessibility-tree semantics, and polite live-region message announcements for the workbench conversational assistant (`#employee-chat-launcher`, `#employee-chat`, `#chat-panel`, `#workspace-status`), UX knowledge-base recording (`docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`), and Focused-tier local validation (`unittest`, `ruff`, `mypy`) without modifying production web scripts or stylesheets.
* Plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md; `src/api/tests/test_assistant_panel_a11y_159.py`; `docs/reference/research/ux/wcag-conformance-baseline.md`; `docs/reference/README.md`; `docs/reference/log.md`; refreshed Web Interface Guidelines (`vercel-labs/web-interface-guidelines`); independent read-only review lens.

## Opening Review State

* Interpreted review goal: Verify once and from direct evidence whether completed implementation and Focused-tier validation fulfill all approved plan requirements (`FR-01`–`FR-04`, `NFR-01`–`NFR-02`), acceptance criteria (`AC-1`–`AC-4`), and resolved critique findings (`PC-001`–`PC-003`) for Issue #159 criterion 6 while preserving zero production web edits and repository UX/conformance honesty rules.
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`)
* Evidence readiness: Ready — plan, phase details, one-pass critique, reconciled changes record, research record, test module, documentation diffs, and Focused-tier validation outputs are present and synchronized.
* Acceptance basis: Plan `## Functional Requirements`, `## Non-Functional Requirements`, `## Acceptance Criteria`, `## Critique Disposition` (`PC-001`–`PC-003`), and `.github/copilot-instructions.md` UX/validation/branch conventions.
* First comparison boundary: Compare `P01-T01` and `P01-T02` test coverage in `src/api/tests/test_assistant_panel_a11y_159.py` against `FR-01`–`FR-03`, `PC-001`–`PC-002`, and zero-production-web-edit scope.
* Active read-only boundaries: This review stage creates and updates only `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-review.md` (and parent session state); it makes no edits to `src/`, `docs/`, plan, details, critique, research, or changes artifacts.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full single-pass review on 2026-11-15 across `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-plan.md`, `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-changes.md`, `.copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md`, `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md`, refreshed Web Interface Guidelines (`vercel-labs/web-interface-guidelines`), `git diff --check`, and an independent read-only review lens. Zero production web files (`src/api/src/zava_forward/api/web/*`) were modified.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01: Conversational Assistant Keyboard, Focus, and Live-Region Verification Suite` | Partial | `src/api/tests/test_assistant_panel_a11y_159.py` passes 5/5 tests, `ruff`, and `mypy --strict`, but omits several planned Chromium assertions (`Close chat` keyboard activation, keyboard `#employee-chat-skill` change, explicit `Shift+Enter` newline value check, Chromium `revealBeside` overlap scroll, `401` `deny()`, and dialog-scoped AXTree `status`/`alert` checks) and inherits ambient `ZF_SIM_STORE` / `ZF_SIM_KEY_FILE` env vars (`RV-002`, `RV-003`). |
| `P02` (`P02-T01`, `P02-T02`) | `P02: UX Verification Record, Guard Reconciliation, and Focused Validation` | Partial | `docs/reference/research/ux/wcag-conformance-baseline.md` overstates three verification details (`S`/`M`/`L` resize presets that do not exist in `chat-widget.js`, Chromium `revealBeside` overlap check not yet run in Chromium, and `401` recovery when only `403` was run), `docs/reference/log.md` has a trailing blank line flagged by `git diff --check`, and `test_ux_design_traceability.py` + `AC-4` commit capture remain to execute (`RV-001`, `RV-003`). |
| `## Follow-Up Items` | `Follow-Up Items` (human NVDA/Firefox, VoiceOver/Safari, 200%/400% zoom acceptance under #151, #155, #619) | Reconciled | Kept outside active automated plan scope with explicit headless-host rationale and UX programme ownership. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/tests/test_assistant_panel_a11y_159.py` | Added `AssistantPanelNodeA11y159Tests` backed by real `SqlStore` + `ChatPanel` + `Assistants.invoke` payloads (`answer`, `refused`, `withheld`, `fallback`, `202` proposal). | 3 Node-VM + Python integration tests pass (`4.50s` combined suite), `mypy --strict` and `ruff` pass. | Passed (`unittest`, `ruff`, `mypy`) | Minor gaps: clear `ZF_SIM_STORE` / `ZF_SIM_KEY_FILE` in `APPROVED_CHAT_ENV`, close `app.simulation` if opened, and cover `401` alongside `403` (`RV-001`, `RV-003`). |
| `P01-T02` | `src/api/tests/test_assistant_panel_a11y_159.py` | Added `AssistantPanelBrowserA11y159Tests` running headless Chromium + CDP `Accessibility.getFullAXTree` + `MutationObserver` across non-case launcher and `#/case/ZF-1?tab=ai` sessions. | 2 Chromium tests pass with zero JS `pageerror`s and zero unexpected `/api/chat/*` HTTP errors. | Passed (`unittest`, `ruff`, `mypy`) | Gaps in `RV-002`: add `Close chat` keyboard activation, keyboard `#employee-chat-skill` selection + `Skill:` check, explicit `"\n"` value assertion after `Shift+Enter`, rendered `revealBeside` scroll check in Chromium, `401` `deny()`, and dialog-subtree scoping for AXTree `status`/`alert`. |
| `P02-T01` | `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, `docs/reference/log.md` | Recorded `2026-11-15` Issue #159 verification section, aligned four `Audit` rows, updated `README.md` index row, and appended `log.md` entry while keeping human `Not run` cells and non-conformance wording intact. | Guard tests (`test_accessibility_baseline.py`, `test_epic149_ux_evidence_results.py`, `test_screen_design_traceability.py`, `test_live_doc_links.py`) pass. | Passed (`unittest`); `git diff --check` failed on trailing blank line | Gaps in `RV-001`: remove nonexistent `S`/`M`/`L` preset mention, align prose strictly with actual Node-VM + Chromium assertions after `RV-002` lands, and remove trailing EOF blank line in `docs/reference/log.md`. |
| `P02-T02` | `src/api/tests/test_assistant_panel_a11y_159.py`, `.copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-changes.md` | Ran caller `unittest` (`48` tests), UX/chat/doc regression `unittest` (`121` tests), `ruff check`, `ruff format --check`, and `mypy`. | Recorded in `changes` validation table. | Passed; `test_ux_design_traceability.py` and `git diff --check` not yet in table | Gaps in `RV-003`: include `src/api/tests/test_ux_design_traceability.py` and `git diff --check` in validation and execute `AC-4` local commit after remediation review. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01`, `P01-T02` (`_SyntheticWorkbenchHarness`) | Used typed `role_matrix_fixture.build()` synthetic seed and `zava_forward.core.chat_privacy.WARNING` (`CHAT_WARNING`) instead of raw `test_mvp.DATA["staff"]` short role labels. | Direct execution of `SqlStore` role lookup for `Retrofit Coordinator` and `/api/chat/status` contract (`server.py`); no user decision needed (local judgment). | Recorded in `.copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-changes.md` under `## Implementation-Time Plan and Detail Updates`. | Preserves `PC-001` dynamic synthetic-seed requirement; no plan revision or second critique needed. | Reconciled and sound. |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001`, `PC-002`, and `PC-003` in `.copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-plan-critique.md` were directly resolved in `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-plan.md` (`## Critique Disposition`). One residual carryover from earlier wording (`S`/`M`/`L` preset mention) remained in `wcag-conformance-baseline.md` and `changes.md` and is captured in `RV-001`.
* Material revisions: None required planning reconsideration or user re-confirmation.
* Dependent-work pause assessment: Plan order (`P01` then `P02`) was respected with no premature resumption.
* Justification assessment: Zero-production-web-edit boundary is fully justified by `chat-widget.js`, `chat.js`, and `style.css` evidence; Web Interface Guidelines refresh confirmed zero changed web files (`✓ pass — 0 web files modified`).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Named human desktop screen-reader and zoom acceptance (NVDA + Firefox on Windows; VoiceOver + Safari on macOS; 200% text resize and 400% zoom) under Issues #151, #155, and #619 | Shared headless Linux host has no desktop screen reader, display server, audio output, or human tester session (`C12`). | Project owner and named human testers executing `docs/reference/research/ux/production-ux-acceptance-protocol.md`. | Open distinct follow-up work (correctly excluded from automated `P01`/`P02` completion claims; requires `Refs #159` non-closing commit wording). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Align UX baseline claims with actual widget controls and executed checks, and fix `log.md` EOF whitespace

* Related scope: `P02-T01` (`P01-T01`, `P01-T02`)
* Evidence: `docs/reference/research/ux/wcag-conformance-baseline.md` (`## Audit` `Focus not obscured` row and `## Conversational assistant panel keyboard and live-region check (2026-11-15, #159)`), `docs/reference/log.md` (EOF blank line flagged by `git diff --check`), and `src/api/src/zava_forward/api/web/chat-widget.js`
* Impact: `wcag-conformance-baseline.md` mentions `resize preset (S, M, L aria-pressed)` even though `chat-widget.js` provides `Dock to right edge` (`aria-pressed`) plus `#employee-chat-width` and `#employee-chat-height` range inputs (no `S`/`M`/`L` presets), and cites `401`/`403` `deny()` plus Chromium `revealBeside` overlap checks when `401` and rendered Chromium `revealBeside` scroll assertions were not yet exercised in `test_assistant_panel_a11y_159.py`. In addition, `git diff --check` reports a trailing blank line at EOF in `docs/reference/log.md`.
* Destination: `rpi-implement`
* Smallest useful next action: Remove the nonexistent `S`/`M`/`L` preset reference from `docs/reference/research/ux/wcag-conformance-baseline.md`, add `401` `deny()` and Chromium `revealBeside` assertions in `src/api/tests/test_assistant_panel_a11y_159.py` so every documented claim is directly tested, and strip the trailing blank line at EOF in `docs/reference/log.md` so `git diff --check` exits `0`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Complete and scope Chromium keyboard and CDP AXTree assertions in `test_assistant_panel_a11y_159.py`

* Related scope: `P01-T02`
* Evidence: `src/api/tests/test_assistant_panel_a11y_159.py` (`AssistantPanelBrowserA11y159Tests`)
* Impact: `AssistantPanelBrowserA11y159Tests` visits `Close chat` and `#employee-chat-skill` during `Tab` traversal without activating `Close chat` via keyboard (`Enter`/`Space` -> dialog hides and focus returns to `#employee-chat-launcher`) or changing `#employee-chat-skill` via keyboard and asserting the selected skill attribution in the rendered reply; presses `Shift+Enter` without explicitly asserting `"\n"` in `#employee-chat-question`'s `input_value()`; omits rendered Chromium `revealBeside` scroll-clearance verification (`window.scrollY` / `window.scrollX`); and queries `role == "status"` / `role == "alert"` across the full-page CDP AXTree rather than scoping to descendants of the `Employee assistant` `dialog` AX node.
* Destination: `rpi-implement`
* Smallest useful next action: Add keyboard `Close chat` activation, keyboard `#employee-chat-skill` selection (`ArrowDown` / non-`general` skill) with reply `Skill:` verification, explicit `"\n"` assertion after `Shift+Enter`, rendered Chromium `revealBeside` scroll-clearance checks (floating vertical + docked horizontal), `401` alongside `403` `deny()`, and `dialog`-subtree child-ID scoping for CDP AXTree `status` and `alert` assertions.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Isolate ambient simulation-store environment variables in `_SyntheticWorkbenchHarness` and run `test_ux_design_traceability.py` + `git diff --check`

* Related scope: `P01-T01`, `P02-T02`
* Evidence: `src/api/tests/test_assistant_panel_a11y_159.py` (`APPROVED_CHAT_ENV` and `_SyntheticWorkbenchHarness`), `src/api/src/zava_forward/api/server.py` (`simulation_lane.Lane.open`), and `src/api/tests/test_ux_design_traceability.py`
* Impact: `App(self.store, LOCAL_PASSWORD)` calls `simulation_lane.Lane.open(os.environ, ...)`, which reads `ZF_SIM_STORE` and `ZF_SIM_KEY_FILE` if set in ambient `os.environ`. Clearing both keys in `APPROVED_CHAT_ENV` and closing any simulation handle on harness teardown guarantees hermetic synthetic isolation. In addition, `src/api/tests/test_ux_design_traceability.py` and `git diff --check` were planned in `P02-T02` and should be executed and recorded before final local commit (`AC-4`).
* Destination: `rpi-implement`
* Smallest useful next action: Clear `ZF_SIM_STORE` and `ZF_SIM_KEY_FILE` in `APPROVED_CHAT_ENV`, close `self.app.simulation` if non-`None` in `_SyntheticWorkbenchHarness.close()`, and run `test_ux_design_traceability.py` and `git diff --check` alongside the caller validation commands before creating the local commit.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: Pre-Chromium unit discovery in `.github/workflows/src-ci.yml` skips `AssistantPanelBrowserA11y159Tests` unless invoked in the browser-check step

* Related scope: `P01-T02` (CI integration boundary)
* Evidence: `.github/workflows/src-ci.yml` and `src/api/tests/test_assistant_panel_a11y_159.py`
* Impact: `AssistantPanelNodeA11y159Tests` runs unconditionally during `src-ci.yml` unit discovery, whereas `AssistantPanelBrowserA11y159Tests` gracefully skips prior to `playwright install chromium`. Editing `.github/workflows/src-ci.yml` would escalate validation from the caller-specified Focused tier to the Full gate tier per repository instructions, so leaving `.github/workflows/src-ci.yml` untouched in this slice is intentional.
* Destination: `follow-up`
* Smallest useful next action: Track optional invocation of `AssistantPanelBrowserA11y159Tests` after `playwright install chromium` in `.github/workflows/src-ci.yml` under a dedicated Full-tier workflow slice if hosted CI browser execution is desired in addition to `browser_check.py`.

## Defects

* `RV-001` [High] -> `rpi-implement`
* `RV-002` [Medium] -> `rpi-implement`
* `RV-003` [Medium] -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child `rpi-implement` remediation task: align `wcag-conformance-baseline.md` prose with actual widget controls (`Dock to right edge` + width/height sliders, `401`/`403`, Chromium `revealBeside`) and remove `docs/reference/log.md` trailing EOF blank line. | Implementation/documentation defect inside accepted scope. |
| `RV-002` | `rpi-implement` | Child `rpi-implement` remediation task: add `Close chat` keyboard activation, keyboard `#employee-chat-skill` change, `Shift+Enter` `"\n"` value check, Chromium `revealBeside` overlap scroll check, `401` `deny()`, and dialog-subtree AXTree scoping in `src/api/tests/test_assistant_panel_a11y_159.py`. | Test-completeness defect inside accepted scope. |
| `RV-003` | `rpi-implement` | Child `rpi-implement` remediation task: clear `ZF_SIM_STORE` / `ZF_SIM_KEY_FILE` in `APPROVED_CHAT_ENV`, close `app.simulation` on teardown, and run `test_ux_design_traceability.py` + `git diff --check` prior to local `Refs #159` commit. | Hermetic test isolation and validation completeness defect inside accepted scope. |
| `RV-004` | `follow-up` | Optional future Full-tier CI workflow task (outside Focused-tier non-workflow scope). | Non-blocking residual CI enhancement. |

Later implementation of a routed finding does not require another Review of this completed parent task.

## Residual Work

* `RV-004`: Optional post-`playwright install chromium` execution of `AssistantPanelBrowserA11y159Tests` in `.github/workflows/src-ci.yml` under a separate Full-tier workflow PR.
* Plan follow-up: Named human desktop screen-reader (NVDA + Firefox on Windows; VoiceOver + Safari on macOS), 200% text resize, and 400% zoom acceptance under Issues #151, #155, and #619 (`docs/reference/research/ux/production-ux-acceptance-protocol.md`).

## Blockers and Remaining Work

* Blockers: None for local automated remediation; human desktop assistive-technology acceptance remains an external owner/human gate (#151, #155, #619).
* Remaining active work: None in this completed parent task; `RV-001`, `RV-002`, and `RV-003` are routed to the immediate child remediation loop prior to creating the local branch commit.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_assistant_panel_a11y_159.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py -q` | `src/api/tests` | Passed | `Ran 48 tests in 9.222s — OK` (5/5 tests in `test_assistant_panel_a11y_159.py`, 0 skipped) |
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_chat_panel.py src/api/tests/test_chat_widget_focus.py src/api/tests/test_home_chat_regulatory_keyboard_provenance.py src/api/tests/test_production_ux_acceptance_protocol.py src/api/tests/test_epic149_ux_evidence_results.py src/api/tests/test_screen_design_traceability.py src/core/tests/test_live_doc_links.py -q` | `src/api/tests`, `src/core/tests` | Passed | `Ran 121 tests in 68.515s — OK (skipped=1)` |
| `python3 -m ruff check src/api` & `python3 -m ruff format --check src/api` | `src/api` | Passed | `All checks passed!` and `209 files already formatted` |
| `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` | `src/api` | Passed | `Success: no issues found in 293 source files` |
| `git --no-pager diff --check` | Repository working tree | Failed | `docs/reference/log.md:11831: new blank line at EOF.` (`RV-001`) |
| `src/api/tests/test_ux_design_traceability.py` | `src/api/tests` | Skipped in parent run | Scheduled in `P02-T02` details but omitted from the regression batch (`RV-003`) |
| Hosted GitHub Actions CI | Remote branch | Unavailable (by instruction) | User explicitly instructed `Do NOT push`; hosted CI cannot run until future push |

## Outcome

* Outcome: Defects found
* Outcome rationale: Execution of `P01` and `P02` completed with zero production web edits and passing `unittest` (`48` + `121`), `ruff`, and `mypy --strict`, but independent evidence comparison found over-claimed control/scenario details in `docs/reference/research/ux/wcag-conformance-baseline.md` plus a trailing EOF blank line in `docs/reference/log.md` (`RV-001`), missing/unscoped Chromium assertions in `src/api/tests/test_assistant_panel_a11y_159.py` (`RV-002`), and unisolated `ZF_SIM_STORE` / `ZF_SIM_KEY_FILE` env vars plus omitted `test_ux_design_traceability.py` execution (`RV-003`). All three defects are concrete, bounded, and routed to `rpi-implement`.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Remediate `RV-001`, `RV-002`, and `RV-003` in `src/api/tests/test_assistant_panel_a11y_159.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, and `docs/reference/log.md`, then re-run Focused-tier checks + `test_ux_design_traceability.py` + `git diff --check` and create local `Refs #159` commit. |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up | `RV-004` (optional Full-tier `src-ci.yml` post-Chromium test step) and human desktop NVDA/Firefox + VoiceOver/Safari + 400% zoom acceptance (#151, #155, #619). |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: `unittest` (`48` caller + `121` regression), `ruff check`, `ruff format --check`, and `mypy --strict` passed; `git diff --check` flagged 1 EOF blank line in `docs/reference/log.md`; `test_ux_design_traceability.py` routed to remediation; hosted CI not run per `Do NOT push`.
* Blockers: None for automated remediation; external human AT acceptance (#151, #155, #619) remains open.

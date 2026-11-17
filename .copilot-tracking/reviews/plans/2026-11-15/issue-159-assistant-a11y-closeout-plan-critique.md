<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #159 Conversational Assistant Accessibility Closeout (`RV-001`)

## Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y-closeout
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-closeout-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-closeout-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Final-candidate plan critique for child micro-closeout task `2026-11-15-issue-159-assistant-a11y-closeout`, verifying whether `P01-T01` cleanly and completely resolves `RV-001` in `src/api/tests/test_assistant_panel_a11y_159.py` without side effects, production web edits, or edits to historical review/critique artifacts.
* Research and evidence considered:
  * .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-closeout-plan.md
  * .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-closeout-phase-details.md
  * .copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-polish-review.md
  * src/api/tests/test_assistant_panel_a11y_159.py
  * docs/reference/research/ux/wcag-conformance-baseline.md
* Decisions, dependencies, and acceptance criteria considered: Zero production web/API/core/agent changes; test ownership locked to `src/api/tests/test_assistant_panel_a11y_159.py` (`0` new files, `none` removed); Focused-tier validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `git --no-pager diff --check`); preservation of historical records and open follow-up items (`src-ci.yml` Full-tier step and human desktop screen-reader/zoom acceptance under Issues #151, #155, and #619).
* Assessment boundary: Evaluates plan and phase-detail accuracy, runtime harness compatibility, type-check safety, teardown exception safety, and baseline alignment strictly from the five supplied files without executing tests or inspecting files outside the read boundary.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| RV-001 (pre-open `Chat size` `expanded`) | Covered | `P01-T01` queries `_dialog_ax_subtree` via `cdp.send("Accessibility.getFullAXTree")["nodes"]` while focus is on `<summary>Chat size</summary>` before `Enter` and asserts `expanded is False` on `DisclosureTriangle` `"Chat size"`, matching `docs/reference/research/ux/wcag-conformance-baseline.md` line 236 (`expanded` `False` / `True` on `"Chat"` and `"Chat size"`) without altering DOM focus. |
| RV-001 (`_SyntheticWorkbenchHarness.close()`) | Covered | `P01-T01` wraps `sim_close()`, `self.app.assistants.stop()`, `self.store.db.close()`, and `shutil.rmtree(self.root, ignore_errors=True)` in nested `try/finally` blocks while preserving `self.app is not None` and `self.store is not None` guards for partial `__init__` failures. |
| RV-001 (`NODE_A11Y_HARNESS` `Enter` keydown + live checks) | Partial | Storing `this._lastSubmit` in `requestSubmit()` and dispatching `input.dispatchEvent("keydown", { key: "Enter" })` for non-`send` turns aligns with `RV-001`, but `FR-01` and `P01-T01` reference `env.liveEvents` (undefined in `NODE_A11Y_HARNESS`; the property in `createDomEnv` is `env.liveMutations`) and do not clear `formEl._lastSubmit` before `keydown` (`PC-001`). |
| FR-01 | Partial | Covers all three `RV-001` sub-items in `src/api/tests/test_assistant_panel_a11y_159.py`, subject to correcting `env.liveEvents` to `env.liveMutations` and resetting `formEl._lastSubmit` before `keydown` (`PC-001`). |
| NFR-01 / AC-01 | Covered | Focused-tier commands (`unittest`, `ruff check src/api`, `ruff format --check src/api`, `mypy` from `src/api`, and `git --no-pager diff --check`) match the single-test-file scope and prior polish review evidence (`48` unskipped tests `OK`, `293` mypy files clean). |
| P01 / P01-T01 | Partial | Single-task structure and file ownership lock are right-sized; requires direct planner correction for `PC-001` before implementation. |

## Verdict

* Verdict: Revise
* Rationale: Two of the three `RV-001` adjustments (`_SyntheticWorkbenchHarness.close()` nested `try/finally` hardening and the pre-open `DisclosureTriangle` `"Chat size"` `expanded is False` CDP AXTree assertion) are accurate and side-effect-free, and `docs/reference/research/ux/wcag-conformance-baseline.md` already matches the target assertions without needing documentation edits. However, `FR-01`, plan `P01-T01`, and phase-details `P01-T01` instruct the implementer to assert `env.liveEvents` inside `NODE_A11Y_HARNESS`, whereas `createDomEnv()` in `src/api/tests/test_assistant_panel_a11y_159.py` defines and returns `env.liveMutations` (`__a11yLiveEvents` exists only in the Playwright `LIVE_OBSERVER_INIT_SCRIPT`), and `formEl._lastSubmit` is not cleared before `keydown` dispatch (`PC-001`).

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Low]: Correct `NODE_A11Y_HARNESS` `env.liveEvents` reference to `env.liveMutations` and clear `formEl._lastSubmit` before non-`send` `Enter` keydown

* Related IDs: RV-001, FR-01, AC-01, P01, P01-T01
* Evidence: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-closeout-plan.md (`FR-01`, `P01-T01`), .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-closeout-phase-details.md (`P01-T01` item 2), and src/api/tests/test_assistant_panel_a11y_159.py (lines 166, 351-353, 490, 686-733, 777-786, 911, 1691)
* Concern: `FR-01`, plan `P01-T01`, and phase-details `P01-T01` item 2 specify asserting `env.liveEvents` captured `role="log"`, `role="status"`, and `role="alert"` entries in `NODE_A11Y_HARNESS`. In `src/api/tests/test_assistant_panel_a11y_159.py`, `createDomEnv()` defines and returns `liveMutations` (`env.liveMutations`), while `__a11yLiveEvents` / `live_events` exists only in the Chromium `LIVE_OBSERVER_INIT_SCRIPT`; reading `env.liveEvents` in Node evaluates to `undefined` (`TypeError` on `.some(...)` / `.filter(...)`). In addition, in the 4-turn loop (`send`, `log`, `sources`, `external`), `formEl._lastSubmit` retains the previous turn's resolved promise unless cleared before `input.dispatchEvent("keydown", { key: "Enter" })`, so a broken `keydown` path that prevented default without calling `requestSubmit()` would read a stale `_lastSubmit` reference.
* Impact: Implementing `P01-T01` verbatim fails at runtime in `AssistantPanelNodeA11y159Tests` (`TypeError` on `env.liveEvents`), or forces an unrecorded implementation deviation from `FR-01` observable acceptance criteria during `rpi-review`.
* Smallest useful change: Replace `env.liveEvents` with `env.liveMutations` in `FR-01`, plan `P01-T01`, and phase-details `P01-T01` item 2, and specify resetting `formEl._lastSubmit = undefined;` immediately before `input.dispatchEvent("keydown", { key: "Enter" })` with `assert.ok(askTask)` in the `mode !== "send"` branch.
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-closeout-plan.md` and `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-closeout-phase-details.md` consistently name `env.liveMutations` and reset `formEl._lastSubmit = undefined` (with `assert.ok(askTask)`) before `input.dispatchEvent("keydown", { key: "Enter" })`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* `_SyntheticWorkbenchHarness.close()` nested `try/finally` design preserves existing `self.app is not None` and `self.store is not None` partial-init safety (`__init__` lines 107-109) while guaranteeing `self.app.assistants.stop()`, `self.store.db.close()`, and `shutil.rmtree(self.root, ignore_errors=True)` run even if an earlier step raises.
* `recordLive()` in `NODE_A11Y_HARNESS` (lines 170-189, 296) already records `append` mutations on `logEl` (`role === "log"`), `text` mutations on `statusEl` (`role === "status"`), and `reveal`/`text` mutations on `errorEl` (`role === "alert"`), so asserting all three roles against `env.liveMutations` works cleanly without modifying `createDomEnv()`.
* Querying `_dialog_ax_subtree(cdp.send("Accessibility.getFullAXTree")["nodes"])` right after focusing `"Chat size"` (line 1257) and before pressing `Enter` (line 1260) is read-only, preserves focus on `<summary>Chat size</summary>`, matches existing `mypy`-clean typing (`list[dict[str, Any]]`), and brings the test into exact parity with `docs/reference/research/ux/wcag-conformance-baseline.md` line 236 (asserting `len(size_ax_closed) == 1` before indexing `[0]`, matching line 1276).
* Residual risk (explicitly accepted in plan `## Follow-Up Items`): `AssistantPanelBrowserA11y159Tests` skips when Playwright or Chromium is absent, so Focused validation must confirm `48` tests run unskipped (`skipped=0`) locally; hosted `src-ci.yml` wiring and human desktop screen-reader/zoom acceptance (#151, #155, #619) remain tracked follow-up items outside this Focused-tier slice.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Read-only assessment constrained to the five caller-supplied artifacts; `chat.js` and `chat-widget.js` were not directly re-read, relying on existing verified assertions in `src/api/tests/test_assistant_panel_a11y_159.py` (such as line 659 `input.dispatchEvent("keydown", { key: "Enter" })`) and `.copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-polish-review.md`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply the direct planner correction in `.copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-closeout-plan.md` and `.copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-closeout-phase-details.md` (`env.liveEvents` -> `env.liveMutations`, plus clearing `formEl._lastSubmit = undefined` and asserting `assert.ok(askTask)` before awaiting non-`send` `Enter` submissions) and finalize the plan without another critique pass.
* User response required: no

<!-- markdownlint-disable-file -->
# RPI Review: Issue #159 Conversational Assistant Accessibility Final Precision Polish (`RV-001`–`RV-002`)

## Review Metadata

* Task ID: 2026-11-15-issue-159-assistant-a11y-polish
* Task slug: issue-159-assistant-a11y-polish
* Parent task: 2026-11-15-issue-159-assistant-a11y-remediation
* Review date: 2026-11-15
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-15/issue-159-assistant-a11y-research.md
* Prior review: .copilot-tracking/reviews/logs/2026-11-15/issue-159-assistant-a11y-remediation-review.md
* Plan: .copilot-tracking/plans/2026-11-15/issue-159-assistant-a11y-polish-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-159-assistant-a11y-polish-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-159-assistant-a11y-polish-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-15/issue-159-assistant-a11y-polish-changes.md
* Delivered files:
  * src/api/tests/test_assistant_panel_a11y_159.py
  * docs/reference/research/ux/wcag-conformance-baseline.md
  * docs/reference/README.md
  * docs/reference/log.md

## Reconciliation and Boundary Assessment

* Plan checklist markers (`P01`, `P01-T01`, `P01-T02`), phase details, critique dispositions (`PC-001`–`PC-004`), changes evidence, validation state, and follow-up items are reconciled.
* Zero production web files were modified (`git diff -- src/api/src/zava_forward/api/web/` is empty; refreshed Web Interface Guidelines verified). Zero `.copilot-tracking/` strings appear in `src/` or `docs/` diffs, and all changed documentation links resolve.
* Independent `rubber-duck` lens confirmed `PC-002`, `PC-003`, single-newline EOF hygiene, and link integrity, while surfacing one narrow test-to-baseline / teardown micro-gap (`RV-001`).

## Findings

### RV-001: Assert pre-open `Chat size` `expanded == False`, exercise non-blank `Enter` keydown in Node-VM, and harden `_SyntheticWorkbenchHarness.close()` with `try/finally`

* Severity: Low
* Destination: rpi-implement
* Evidence:
  * `docs/reference/research/ux/wcag-conformance-baseline.md` (`## Conversational assistant panel keyboard and live-region check (2026-11-15, #159)`) states `` `expanded` (`False` / `True` on `"Chat"` and `"Chat size"`) ``, whereas `test_browser_launcher_keyboard_resize_dock_and_escape_focus` in `src/api/tests/test_assistant_panel_a11y_159.py` currently asserts `expanded` `False` then `True` on `"Chat"` and only `True` (post-`Enter`) on `"Chat size"`.
  * In `NODE_A11Y_HARNESS` (`src/api/tests/test_assistant_panel_a11y_159.py`), blank `Enter` dispatches `keydown` `{ key: "Enter" }`, while the non-blank turn loop invokes `formEl.requestSubmit()` directly instead of dispatching `keydown` `{ key: "Enter" }` when focus is on `input`.
  * In `_SyntheticWorkbenchHarness.close()`, sequential teardown calls could skip `self.store.db.close()` or `shutil.rmtree(self.root, ignore_errors=True)` if `sim_close()` or `self.app.assistants.stop()` raises.
* Required action:
  * Assert `self._ax_props(size_ax_before[0]).get("expanded") is False` on `"Chat size"` before pressing `Enter` to expand it, dispatch `input.dispatchEvent("keydown", { key: "Enter" })` for non-`send` turns in `NODE_A11Y_HARNESS`, and wrap `_SyntheticWorkbenchHarness.close()` steps in nested `try/finally` blocks so `self.store.db.close()` and `shutil.rmtree(self.root, ignore_errors=True)` always run.

## Implementation-Time Updates and Follow-Up Assessment

* Explicit typing (`nodes: list[dict[str, Any]]`) on `find_launcher_ax()` was an appropriate local judgment satisfying `mypy` strict `no-any-return`.
* Plan `## Follow-Up Items` (optional Full-tier `.github/workflows/src-ci.yml` browser step; named human desktop screen-reader and zoom acceptance under Issues #151, #155, and #619) remain outside active scope and are routed as distinct follow-up choices.

## Validation Evidence Reviewed

* `unittest` (`test_assistant_panel_a11y_159.py`, `test_accessibility_baseline.py`, `test_content_standard.py`): `48` tests `OK`.
* `unittest` (`test_ux_design_traceability.py`, `test_chat_panel.py`, `test_chat_widget_focus.py`, `test_chat_widget_layout.py`): `91` tests `OK (skipped=1)`.
* `python3 -m ruff check src/api` and `python3 -m ruff format --check src/api`: passed (`0`).
* `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`: `Success: no issues found in 293 source files`.
* `git --no-pager diff --check`: exited `0` (staged `git --no-pager diff --cached --check` to be verified after `git add`).

## Routing Summary

* `RV-001` (Low) -> `rpi-implement` (final child closeout task before local commit).
* Plan follow-up items -> preserved as distinct ranked follow-up items outside active Focused-tier scope.

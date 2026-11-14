# Issue 76 hazard clock and owner research (2026-11-14)

Task: deliver the last unticked criterion of issue #76, "Hazard and safeguarding items show a clock and named owner". Base 656bf1cf1 (stacked on PR #1639).

## Evidence

* `src/core/src/zava_forward/core/taskqueues.py` `context()` already emitted `hazard_clocks` for unreleased hazards with `owner` (or `Unknown`), `elapsed_hours`, due dates and state.
* Gap 1: an unassigned item showed owner `Unknown`, with no explicit escalation owner.
* Gap 2: no single textual clock statement naming elapsed time and target window; safeguarding items were not distinguished.
* `src/api/src/zava_forward/api/web/app.js` `workSummary()` renders the clocks on queue rows, role screens and case-card tabs, so one change covers all surfaces.
* Existing tests assert `owner == "Unknown"` and existing UI phrases, so new fields are additive.

Planning readiness: Ready.

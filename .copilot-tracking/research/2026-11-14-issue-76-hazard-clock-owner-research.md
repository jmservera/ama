# Issue 76 hazard clock and owner research (2026-11-14)

Task: deliver the last unticked criterion of issue #76, "Hazard and safeguarding items show a clock and named owner". Base 656bf1cf1 (stacked on PR #1639).

## Evidence

* `src/core/src/zava_forward/core/taskqueues.py` `context()` already emitted `hazard_clocks` for unreleased hazards with `owner` (or `Unknown`), `elapsed_hours`, due dates and state.
* Gap 1: an unassigned item showed owner `Unknown`, with no explicit escalation owner.
* Gap 2: no single textual clock statement naming elapsed time and target window; safeguarding items were not distinguished.
* `src/api/src/zava_forward/api/web/app.js` `workSummary()` renders the clocks on queue rows, role screens and case-card tabs, so one change covers all surfaces.
* Existing tests assert `owner == "Unknown"` and existing UI phrases, so new fields are additive.

Planning readiness: Ready.

## Cycle 1 follow-up (independent-direct finding triage, 2026-11-14)

* Finding 1 confirmed: `HAZARD_CATEGORIES` in `src/core/src/zava_forward/core/workflows.py` had no safeguarding value, so the Safeguarding clock label in `taskqueues.context` was unreachable from `raise_hazard` and the `HAZ_CATEGORIES` list in `app.js`.
* Finding 2 not reproducible at this HEAD: `src/api/.../views/taskqueues.py` and `_build_hazard_escalation_items` do not exist; the queue payload exposes no free-text hazard summary (the clock text uses only category-derived kind, hours and due timestamps).
* Finding 3 not reproducible at this HEAD: the invented title "Head of Housing & Building Safety" is absent; `ESCALATION_OWNER` is `Building Safety lead (escalation owner)`, and no `role_catalog.py` exists. The finding report file itself is not in the worktree.

Planning readiness: Ready.

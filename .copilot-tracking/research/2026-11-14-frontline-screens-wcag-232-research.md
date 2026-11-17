# Research: frontline screens WCAG 1.4.1 state text (Issue #232)

* Task: `frontline-screens-wcag-232`; disposition: executed; Planning Readiness: Ready.
* Issue #232 unchecked criterion: accessible per the WCAG 2.2 baseline with textual state meaning and keyboard navigation.

## Findings

* `src/api/src/zava_forward/api/web/role-screens.js` renders `resident-choice` and `resident-service-issues`.
  They showed raw states (Accepted, Waiting, Outstanding, Open) and contact needs without a plain-language cue.
* Domain values: choice `Waiting/Accepted/Declined/Paused/Withdrawn` or `Not recorded`; commitment `Outstanding/Proposed`;
  request `Open/In progress/Resolved/Closed`; contact needs are access codes or empty (Unknown).
* Frontline screens render no access appointment: appointment state appears only in the delivery gate (line ~502, programme screen).
  The update commitment (due date, owner, safe route) is the nearest resident-contact item and is covered instead.
* Existing tests assert exact substrings (for example `Loft insulation: current Paused`), so cues are prefixed to the whole entry.
* `test_design_system` forbids undocumented classes and inline styles: the change adds no classes, text only.
* Env note: the editable `zava_forward.core` install points at another checkout; validation used `PYTHONPATH` to this worktree.

## Decision

Prefix `Confirmed:`, `Waiting for resident:` or `Action needed:` using a shared `stateCue` helper with `Object.hasOwn` lookups; unknown values default to `Action needed`.

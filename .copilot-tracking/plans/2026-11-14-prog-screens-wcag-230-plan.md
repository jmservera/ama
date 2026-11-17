# Plan: Programme screens WCAG state clarity (Issue #230)

Research: [research](../research/2026-11-14-prog-screens-wcag-230-research.md)

## Phases

* [x] 1. Add `programmeStatePrefix`, `programmeStateLabel` (`Object.hasOwn`), `programmeSections` and `programmeJump` to `role-screens.js`.
* [x] 2. Rework `programme-queue` `render` to add the nav group, the state summary list and focusable section wrappers; leave table cells unchanged.
* [x] 3. Add `src/api/tests/test_programme_screen_wcag.py`.
* [x] 4. Run unit tests, `ruff check`, `ruff format --check`, `mypy`.

## Critique (single pass, inline)

* Prefixing table cells would break exact-cell browser checks: rejected, summary list used instead.
* `button` elements would break the no-controls test: anchors with `.btn alt` used.
* `Pass:` would contradict "not a pass": reserved, not emitted.

Verdict: proceed. Validation tier: focused (UI, non-gate).

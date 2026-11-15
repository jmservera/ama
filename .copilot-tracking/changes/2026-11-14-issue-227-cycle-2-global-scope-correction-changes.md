# Issue 227 Cycle 2: global scope collision correction

* Trigger: independent review `independent-rev-227-c1-c594b777a.md`.
* Research: `role-screens.js` declared top-level `const hazardState`, colliding with `function hazardState` in `app.js`. Both load in the shared global scope, so `/app` start-up threw a SyntaxError (Critical). `hazardJump` used unguarded focus and scroll calls (Low).
* Plan: rename the identifier, guard the DOM calls, add regression tests.
* Implement:
  * `src/api/src/zava_forward/api/web/role-screens.js`: `hazardState` renamed `hazardEscalationState`; `hazardJump` uses `heading?.focus?.()` and `heading?.scrollIntoView?.(...)`.
  * `src/api/tests/test_safety_screen_wcag_keyboard.py`: test that no top-level identifier in `role-screens.js` collides with `app.js`; node test invoking the jump `onclick` with a present, missing and bare target.
* Validation: targeted modules (keyboard WCAG, content standard, role screens, design system, accessibility baseline, dependency rule) 68 tests OK; `ruff check`, `ruff format --check`, `mypy` clean. `unittest discover` deliberately not run.
* Review: independent exact-head review required before push; not pushed.

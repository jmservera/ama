# Changes: frontline screens WCAG 1.4.1 state text (Issue #232)

* `src/api/src/zava_forward/api/web/role-screens.js`: `stateCue` helper, cue tables, prefixes on resident-choice and resident-service-issues; `serviceMeaning` lookup now uses `Object.hasOwn`.
* `src/api/tests/test_frontline_screen_wcag.py`: three focused tests (prefixes, inherited-name defaults, service states).
* Divergence: no access appointment exists on these screens; update commitment covered instead.
* Not done: resident or screen-reader validation (#155); issue #232 criterion is not fully proven, so the PR should use `Refs #232`.

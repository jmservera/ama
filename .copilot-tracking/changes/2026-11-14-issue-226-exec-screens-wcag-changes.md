# Issue #226 exec screens WCAG 1.4.15: Cycle 3 changes

* Defect: `test_no_internal_terms_in_web_copy` flagged `role-screens.js` lines 230 and 311.
* Root cause: the banned term was `gates` in the anchor id `asset-gates`, not the "Benefits and phase check" title (`phase` is not in `BANNED`).
* Change: anchor id renamed `asset-gates` to `asset-checks` in `role-screens.js` (2 sites); visible title unchanged. No other references exist.
* Validation: asset_exec_screen_wcag, content_standard, design_system, accessibility_baseline, dependency_rule (61 tests OK), ruff and mypy clean.

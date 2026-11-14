# Plan: Issue #231 state prefixes and section navigation

* Critique (single pass, self): compatible; no conflict with confirmed decisions.
1. Add `evidencePrefixes` map with `Object.hasOwn` lookup and `evidenceLabel`; prefix technical sign-off states (`Verified`, `Pending review`, `Action needed`). An incomplete "Signed off" record is `Action needed`, never `Verified`.
2. Add `screenSection` (id plus `aria-labelledby` heading) and a `nav.screen-links` "Sections on this screen" jump list on the technical screen.
3. Prefix quality per-check states (`Pending review`, `Action needed`).
4. Add `tests/test_assessor_screen_wcag.py`; run full api tests, ruff, mypy.

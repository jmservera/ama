# Changes 153 c2

* `app.js`: `painted = true` now set after `content.replaceChildren(...)` in `paint()`.
* `test_app_js_notices_content.py`: new node-driven test for a throwing first paint; fails without the fix.
* Validation: test_app_js_notices_content, test_content_standard, test_case_journey (52) OK; ruff check and format OK; mypy OK (239 files).

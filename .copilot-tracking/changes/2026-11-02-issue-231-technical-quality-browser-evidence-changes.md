# Changes: issue #231 browser evidence slice

* `src/api/checks/role_screens_fixtures.py`: `technical_quality_data()` synthetic home.
* `src/api/checks/role_screens_browser_check.py`: stories `231` and `231q`, `check_readonly_accessibility`.
* `src/api/README.md`: story and `ZF_AXE_JS` documentation.

Validation: `python3 -m checks.role_screens_browser_check` for `231`, `231q`, `232` and parent all pass locally with pinned axe 4.10.3 (no violations, no incomplete). ruff check passes. No production code changed.

# Cycle 1 changes: plain-language focus cue (#1647, Refs #233)

* Rebased onto origin/feat/demo-233-same-home-tensions-0825 (17628d7db); #1644 stage map kept, duplicate commit skipped, #1647 landmark aria-label, aria-current="step" and focus cue retained (c931e1da0).
* Fixed CI src-api mypy "Source file found twice": src/api/tests/test_role_screens_stage_map_focus.py now imports `from test_role_screens_connected_journey import ...` (no tests/__init__.py in src/api).
* Validation from src/api: journey tests 47 OK; accessibility baseline 13 OK; ruff check and format check pass.
* mypy: duplicate-module error gone; 2 unused-ignore errors remain in tests/test_ai_consumption_api.py (untouched, pre-existing, likely local-environment dependent).
* Original research/plan/changes/review files preserved. Not pushed.

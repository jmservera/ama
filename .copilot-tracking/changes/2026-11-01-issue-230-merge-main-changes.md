# Issue 230 merge of origin/main (PR 662)

* Research: conflict only in role-screens.js; main's role screens lacked registration closers.
* Plan/Implement: kept programme-manager and all main screens, restored closers, kept branch rubric score, kept both log entries.
* Review: node --check passes; 10 screen test modules pass (58+ tests); no open review threads; ruff check clean; pre-existing ruff-format (check-container.py), mypy iot_stream stubs and test_browser_asset_urls import issues are unrelated.

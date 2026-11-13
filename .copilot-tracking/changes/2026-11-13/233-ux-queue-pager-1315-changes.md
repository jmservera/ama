# Changes

Initialized. Entries follow as implemented.

* role-screens.js: Connected view row link with page context (ported from 837da4fde); native disabled on #programme-prev/#programme-next at range ends with focus moved to the other button; absent pager guarded.
* test_programme_screen.py: ported tests plus pager range-end test; typed via any_out so strict mypy has zero errors (the earlier 15 errors were unused/invalid type-ignore comments and a dict invariance error).
* programme_paging_browser_check.py: updated, not run (Chromium forbidden). scenario-manifest not touched: it hashes workbench_browser_check.py only; core manifest and needs tests pass.
* atlas-screen-trace.md updated; log.md untouched.
* Validation: unittest 64 OK, core 19 OK, ruff check/format OK, mypy 236 files OK, git diff --check 0.

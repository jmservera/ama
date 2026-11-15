# C1 plan (Refs #149)

* [x] Reset the page to `about:blank` before each view load in the heading-hierarchy crawl so every view is read from a fresh document.
* [x] Add the repository-convention `type: ignore[no-untyped-call]` on `App(...)` in the landmarks test.
* [x] Run all `test_epic149_*` and `test_accessibility_baseline`, ruff check and format, and project mypy.
* [x] Commit one C1 commit; do not push.

Critique: inline, one pass. Both edits are test-only and compatible with the confirmed constraints; no significant divergence.

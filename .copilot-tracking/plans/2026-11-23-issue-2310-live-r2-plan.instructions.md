---
applyTo: '.copilot-tracking/changes/2026-11-23-issue-2310-live-r2-changes.md'
---
# Issue 2310 plan, live run 2

* [x] Phase 1: add `test_anonymous_api_never_redirects_for_any_method_accept_or_unknown_path` to `src/api/tests/test_auth.py` (GET, HEAD, POST; three Accept values; cookie; unknown /api path; /sign-in to Entra).
* [x] Phase 2: run auth tests and sibling auth suites; ruff check.
* [x] Phase 3: record per-criterion table and live status; research note update.

Tier: focused. Basis: test-only change, no src, workflow or dependency change.

---
applyTo: '.copilot-tracking/changes/2026-11-23-issue-2310-live-r3-changes.md'
---
# Plan issue 2310 r3

* [x] Phase 1: add `do_PUT`, `do_PATCH`, `do_DELETE` in server.py (anonymous /api/ 401, else stdlib 501).
* [x] Phase 2: add regression test in src/api/tests/test_auth.py; run tests.auth suites, ruff, mypy.
* [x] Phase 3: research note addendum, log entry, changes record with table, review, commit.

Tier: FULL class (src change) but gate economy: targeted tests only; the coordinator runs gates. Never run rpi-checks --all.

# Plan: issue 135 round 2, failed import feed

Date: 2026-11-04. Research: ../research/2026-11-04-issue-135-r2-import-feed-research.md. Details: ../details/2026-11-04-issue-135-r2-import-feed-details.md

* [x] P1 Add `feed_failed_imports` to `src/core/src/zava_forward/core/exception_feeds.py`.
* [x] P2 Tests in `src/core/tests/test_exception_feeds.py`.
* [x] P3 Update `src/core/README.md`.
* [x] P4 Focused tests, ruff, mypy.

## Critique (single pass, verdict proceed)

* Risk: row or cell values leak into the queue. Disposition: only source identity, version and stated reason kept; test asserts absence.
* Risk: duplicates on re-read. Disposition: `ref` per batch id or file hash.
* Risk: a human rejection is a deliberate decision. Disposition: raised for steward visibility only because the data did not go live; no action is taken.
* No user decision needed.

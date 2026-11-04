# Plan: issue 135 round 7, stock conflict feed

Date: 2026-11-04. Research: ../research/2026-11-04-issue-135-r7-stock-conflict-feed-research.md. Details: ../details/2026-11-04-issue-135-r7-stock-conflict-feed-details.md

* [x] P1 Add optional `ref` dedupe to `ExceptionQueue.raise_conflict`.
* [x] P2 Add `feed_stock_conflicts` to `exception_feeds.py`.
* [x] P3 Tests in `test_exception_feeds.py`; README update.
* [x] P4 Focused tests, ruff, mypy.

## Critique (single pass, verdict proceed)

* Risk: the feed picks a winner or edits the case. Disposition: read-only; both values shown; eligibility Unknown.
* Risk: duplicates on re-read. Disposition: `ref` is `stock:<case>:<query>`.
* Risk: resolved or withdrawn queries linger. Disposition: only `Unresolved` raised; closed homes skipped. An already raised item is not auto-closed; the owner closes it by hand.
* No user decision needed.

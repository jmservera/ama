<!-- markdownlint-disable-file -->
# Plan: issue 1292 extension E2 (2026-11-09)

Research: [research](../research/2026-11-09-priority-order-1292-e2-research.md). Details: [details](../details/2026-11-09-priority-order-1292-e2-details.md). Critique: [critique](2026-11-09-priority-order-1292-e2-critique.md). Owner-selected demo-targeted tier; hosted CI and independent exact-head review remain mandatory. Extension cycle E2 of five owner-approved new cycles E1-E5; three remain after this. Per-source counter consumes this actual productive correction; no extra grant.

* [x] Phase 1: serialize `MssqlStore._create_indexes` index creation in the existing `BEGIN IMMEDIATE` write transaction.
* [x] Phase 2: remove the skip on `MssqlLegacyEdges.test_large_legacy_backfill_is_linear_and_survives_concurrent_openers` (plus one `fetchall()` test-side fix found by the SQL run); README unchanged (no mention).
* [x] Phase 3: ruff, mypy, SQLite and API tests on the final head; owned SQL Server runs (see changes).
* [x] Phase 4: records, one review, local commit, handoff.

Stop conditions: any failing selected test (not waivable); no assertion weakened or broad catch added; lock busy (honest partial handoff, no wait loop); an unrelated cause surfaces (record, do not refactor). No push, PR, issue, board or merge.

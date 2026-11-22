# Issue 2254 changes (2026-11-22)

Tier: FULL class (src change); per brief no rpi-checks --all. Run: test_sqlreads (18 OK), test_sql*.py (54 OK), ruff check OK. mypy reports 3 errors identical with and without the change (missing opentelemetry stubs, unused ignore in device_provision.py).

## Changes

* src/core/src/zava_forward/core/sqlstore.py: `_repair_identity_columns` now compares and rebuilds the `hazard` column from the body.
* src/core/tests/test_sqlreads.py: regression test `test_stale_safety_column_is_repaired_so_list_matches_tile_and_map_issue_2254` (failed 3 vs 4 before, passes after).
* docs/reference/research/issue-2254-live-probe-2026-11-22.md plus probe script, result JSON and screenshot.

## Criteria

| Criterion (issue expectation) | Status | Evidence |
| --- | --- | --- |
| Reproduce: tile 23, map 23, list 22 | Proven | probe-safety-count-result.json |
| Cause found in src | Proven locally, inferred for live | research note; local test reproduction. Live row unreadable (SQL private) |
| One definition across tile, map and list | Proven locally | regression test; tile, body count and list agree |
| Live demo shows equal counts after fix | Unproven | needs deploy of this commit; no push allowed here |

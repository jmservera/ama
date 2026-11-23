---
title: Issue 2254 live research, run 3 (2026-11-23)
---

Research disposition: executed (reuse of runs 1 and 2 plus a fresh live probe). Planning Readiness: Ready.

Findings from the base (f40302db55):

* The tile (`insights.stats` hazards KPI), the map (`insights.map_view` kind `hazard`) and the in-memory list filter (`insights.matches`) all use `has_hazard(case)`.
* The SQL list filter uses the stored `hazard` column (`FLAG_SQL["hazard"]`). A stale column is the only path to a tile/map 23 versus list 22 split. `SqlStore._repair_identity_columns` already recomputes it from the body (test `test_stale_safety_column_is_repaired_...` in `src/core/tests/test_sqlreads.py`).
* Gap: that test checks tile and list only; the map is not asserted against the same count.

Plan input: extend the existing test with the map hazard count (test only, no `src/` code change), and re-probe the live demo.

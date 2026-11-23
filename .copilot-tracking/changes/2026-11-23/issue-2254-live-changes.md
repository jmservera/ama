---
title: Issue 2254 live changes
---

Tier: focused (no src change). Added only the evidence note [issue-2254-ui-2026-11-23.md](../../../docs/reference/research/issue-2254-ui-2026-11-23.md) with probe, result JSON and two screenshots. The source fix (hazard compared in `SqlStore._repair_identity_columns`) and its test were already on the branch.

| Criterion (issue states no ticked list; expectation: one definition across tile, map, list) | Status | Evidence |
| --- | --- | --- |
| Overview tile shows the same count as the filtered list | Proven | tile 23, All cases "23 cases", API total 23 |
| Map markers match the list | Proven by API only | 2026-11-22 note: map 23 via `/api/map`; markers not re-counted on screen |
| Fix covers the cause (stale `hazard` column) | Proven locally | test in `src/core/tests/test_sqlreads.py` |
| Live row cause observed | Unproven | SQL public access disabled; not changed for the demo |
| Deployed image maps to the source commit | Unproven | digest not mapped |

Validation: test_sqlreads 18 tests OK (src/core). Markdown and link review done.

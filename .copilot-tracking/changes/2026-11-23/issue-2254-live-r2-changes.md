---
title: Issue 2254 live changes, run 2 (2026-11-23)
---

Tier: focused. No `src/` change; `rpi-checks.py --all` not run. Added [issue-2254-map-markers-live-2026-11-23.md](../../../docs/reference/research/issue-2254-map-markers-live-2026-11-23.md) with probe, result JSON and screenshot, plus an index row and a log entry. The source fix (hazard compared in `SqlStore._repair_identity_columns`) and its test were already on the base.

| Criterion (issue lists no checkboxes; expectation: one definition across tile, map, list) | Status | Evidence |
| --- | --- | --- |
| Overview tile matches the filtered list | Proven | tile 23, All cases "23 cases", API total 23 ([ui note](../../../docs/reference/research/issue-2254-ui-2026-11-23.md)) |
| Map markers match the list | Proven | 23 of 443 markers titled "Safety issue open"; `/api/map` 23 (this run) |
| Fix covers the stale `hazard` column cause | Proven locally | `src/core/tests/test_sqlreads.py` |
| Live row cause observed | Unproven | SQL public access disabled; not changed for the demo |
| Deployed image maps to the source commit | Unproven | digest not mapped |

Validation: Markdown and link review, Git diff review. Secret check: probe asserts sign-in values are absent from the result.

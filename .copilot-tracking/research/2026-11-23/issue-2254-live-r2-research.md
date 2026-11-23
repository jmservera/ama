---
title: Issue 2254 live research, run 2 (2026-11-23)
---

Disposition: executed. Planning Readiness: Ready.

Findings: the issue lists no acceptance checkboxes; the expectation is one definition of "safety issue open" across tile, map and list. The probe [probe_map.py](../../../docs/reference/research/issue-2254-map-2026-11-23/probe_map.py) read tile 23, 23 of 443 map markers titled "Safety issue open", `/api/map` 23, `/api/cases` flag=hazard total 23 and KPI 23. The fix (hazard compared in `SqlStore._repair_identity_columns`, with a test in `src/core/tests/test_sqlreads.py`) is already on the base. Gaps stay unproven: image digest to commit and stored-column cause (SQL public access disabled).

Evidence note: [issue-2254-map-markers-live-2026-11-23.md](../../../docs/reference/research/issue-2254-map-markers-live-2026-11-23.md).

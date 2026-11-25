---
title: Details issue 2303 r73
ms.date: 2026-11-25
---

## Phase 1

In `src/core/src/zava_forward/core/ai_tasks.py` `live_report`, add a local dict keyed by the ordered-distinct case ids and reuse the tuple for repeated recommendations.

## Phase 2

Add a test in `src/core/tests/` that wraps `projection.withheld_scope_values` with a counter and calls `Store.ai_live_report`.

## Phase 3

Run the new test, `test_rai_control_plane_218` and `test_management_tokenomics_invariant_100`, then mypy and ruff in src/core.

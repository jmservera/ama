---
title: Issue 108 live plan 2026-11-23
ms.date: 2026-11-23
---

Refs #108. Tier: focused (test only, no src change).

## Critique (executed once)

Verdict: accept. Risk: a test that restates constants. Mitigation: it compares two independent sources (committed Azure record versus Bicep pins) and fails on drift. Quota headroom is not claimed.

## Plan

* [x] Phase 1: add `test_serving_region_record_matches_infra_pins` to `src/agents/tests/test_ai_eval.py`; run the ai_eval tests, ruff and mypy.
* [x] Phase 2: record per-criterion table in the changes record.

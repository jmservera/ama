---
title: Issue 462 live r4 plan
ms.date: 2026-11-19
---

## Plan

* [ ] Phase 1: in `safe_start` require both the dataset `fixture_id` and the fixture `id` to be non-empty strings before comparing them.
* [ ] Phase 2: add regression tests for missing, null, empty and non-string identifiers, on either side.
* [ ] Phase 3: run focused `src/core` tests, per-project mypy, ruff; write the live proof note with the per-criterion table.

Details: [details](../details/2026-11-19-issue-462-live-r4-details.md). Critique: [critique](../critiques/2026-11-19-issue-462-live-r4-critique.md). Tier: FOCUSED local checks with FULL classification recorded (src change); `--all` not run by owner brief.

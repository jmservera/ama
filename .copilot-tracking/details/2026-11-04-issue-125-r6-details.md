---
title: Issue 125 round 6 details
ms.date: 2026-11-04
---

## Phase 1

* `calculate_stage_durations`: UTC-aware ISO timestamps only; bad timestamps or missing source references become gaps.
* `draft_evidence`: optional drafter; reject empty, uncited or non-calculated numbers; fall back to a plain sentence; status always draft for human review.
* Tests: ordering determinism, gaps, accepted draft, invented number, uncited, empty, drafter failure, no data.

## Phase 2 and 3

README slice 3 paragraph; log entry; focused tests, ruff and mypy.

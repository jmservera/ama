---
title: Plan for issue 2245 (employee chat thread creation 503 on busy SQL write lock)
ms.date: 2026-11-23
---

Research: [research](../research/2026-11-23-issue-2245-live-research.md). Tier: FULL (src change); the full gate is run by the coordinator, never `--all` here.

## Phases

* [x] Phase 1: failing-first test in `src/api/tests/test_error_logging.py` (POST thread create with a busy lock answers 503 with Retry-After; POST ask stays 500).
* [x] Phase 2: in `_unhandled` (`src/api/src/zava_forward/api/server.py`) allow the busy-lock 503 for exactly `POST /api/chat/threads` (single insert and commit, nothing committed on a lock timeout).
* [x] Phase 3: research note with per-criterion evidence, changes record, review.

## Critique (executed once, final candidate)

* Verdict: proceed, narrowed. Widening to every POST is unsafe because a failed POST may follow a committed step (the 2237 comment), so only the create-thread path is allowed.
* Rejected: clearing the live AI suspension (human restart authority, no production change) and a banner rewrite (already states the hold, proven live).
* Reworded the 503 message only through the existing text; no new copy.

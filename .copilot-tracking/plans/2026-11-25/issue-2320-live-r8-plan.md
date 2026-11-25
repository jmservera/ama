---
title: Issue 2320 live r8 plan
ms.date: 2026-11-25
---

* [ ] Phase 1: in `store.py` add `BRIEFING_BUSY_TTL_S = 10` and `_briefing_busy` (key to deadline and answer); `briefing` returns an unexpired entry before recomputing; `_briefing_unrecorded` stores its answer; a recorded success removes the entry.
* [ ] Phase 2: add one test in `src/api/tests/test_assistant_release.py`: after a busy fallback, a second GET returns at once without calling `run_text_task` or taking the write lock, and after the TTL it records again.
* [ ] Phase 3: run the focused tests and mypy in `src/core`; record the live finding in `docs/reference/research/issue-2320-live-r8-2026-11-25.md`, index and log.

Tier: FULL (src change). No gate run by this worker.

---
title: Issue 2320 live r8 details
ms.date: 2026-11-25
---

Phase 1: `Store.briefing` starts with the cache lookup under `self.lock`; add `busy = self._briefing_busy.get(key)` and return `busy[1]` when `time.monotonic() < busy[0]`. `_briefing_unrecorded` writes `self._briefing_busy[key] = (monotonic + TTL, out)` under `self.lock`. On a recorded success, pop the key. Initialise `_briefing_busy = {}` in both `Store.__init__` and `SqlStore.__init__`; cap its size by dropping expired entries on write.

Phase 2: reuse the failing-audit setup of `test_briefing_answers_without_503_when_recording_hits_a_busy_write_lock`.

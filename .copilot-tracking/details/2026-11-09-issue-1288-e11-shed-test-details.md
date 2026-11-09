---
title: Issue 1288 E11 details
ms.date: 2026-11-09
---

# Issue 1288 E11 details

* Helper on `AbuseAndHardeningTests`: `own_every_slot(self) -> int` loops `MAX_CONCURRENT` times, `self.assertTrue(self.app.slots.acquire(timeout=SLOT_WAIT_SECONDS))`, counts, returns the count; a failed acquisition raises after the caller's try so only owned slots release (caller increments through a list owned by the helper).
* Regression `test_shed_view_waits_for_delayed_login_worker_release`: replace `self.app.slots` with a `DelayedRelease` wrapper (first N worker-thread releases wait on an event). Login, assert at least one worker release is pending (ordering proved), set the event from a helper thread, require all eight owned, GET returns 503, release only owned, wrapper restored.
* Critique: see `plans/critiques/`.

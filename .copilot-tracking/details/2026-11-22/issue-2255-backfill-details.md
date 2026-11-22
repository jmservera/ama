---
title: Issue 2255 plan details
date: 2026-11-22
---

# Details

* Candidate rule: open, non-safeguarding hazard, no `aware_at`; anchor `recorded_at` else `noticed` T09:00Z; future or absent anchor is skipped.
* Running subset: every (len/N)-th candidate in sorted case id order, `aware_at` = now - 40 percent of the window, rounded to the hour; `noticed` follows; marker records the original.
* Writes: `store._case`, `store.audit("demo-hazard-clock-seed", ...)`, `store.save()` under `store.lock`.
* Tests: pure plan, no overwrite, safeguarding and released skipped, future anchor skipped, running subset, apply persists and is idempotent, inspect writes nothing.
* Evidence: counts-only live outputs, API queue before and after, Playwright screenshot of the safety queue.

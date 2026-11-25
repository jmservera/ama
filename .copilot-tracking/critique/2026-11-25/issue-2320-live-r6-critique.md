---
title: Issue 2320 live r6 critique
ms.date: 2026-11-25
---

Critique executed once on the final candidate. Verdict: proceed.

* Risk: a shared connection attribute would shorten other writers' waits. Applied: thread-local override, scoped by a context manager that restores in `finally`.
* Risk: shorter wait raises more unrecorded answers. Accepted: the answer names itself unrecorded and the next GET records it; 2 s is a bound, not a retry policy.
* Risk: the briefing still holds `store.lock` during the wait. Accepted: the hold is now at most 2 s instead of 15 s.
* Risk: skipping the record for template answers would drop `record_id` the UI uses. Rejected.

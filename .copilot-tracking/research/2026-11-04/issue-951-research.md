---
title: Issue 951 research - max_days default and future received_on
ms.date: 2026-11-04
---

* Task: issue 951, follow-up from review of #938. Research disposition: executed (direct code read). No merged PR already delivered this fix.
* Evidence: `ChallengeRegister.hazard_referrals_overdue(today, max_days=1)` in `src/core/src/zava_forward/core/challenges.py`. The default of 1 day has no owner approval on record. A `received_on` after `today` gives a negative age, which is never greater than `max_days`, so it was silently not flagged.
* Callers: only `src/core/tests/test_challenges.py`; documented in `src/core/README.md`.
* Slice: pure core, read-only flag, no hazard clock, no persistence, API, security, infrastructure, SQL or deployment change. Focused tier. The flag stays for human follow-up; the existing hazard process is not delayed.
* Planning readiness: Ready.

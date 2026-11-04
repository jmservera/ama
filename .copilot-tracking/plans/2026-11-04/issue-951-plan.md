---
title: Issue 951 plan
ms.date: 2026-11-04
---

* [ ] Phase 1: require `max_days`; flag future `received_on` (details: `.copilot-tracking/details/2026-11-04/issue-951-details.md`).
* [ ] Phase 2: tests, README, ruff, mypy strict.
* Critique (one pass, direct): requiring the argument is safer than inventing an approved value, and the issue allows it. Compatible; applied. A future date is surfaced with a `data_quality` note rather than dropped or rejected, so the owner still sees the referral.

---
title: Issue 82 C2 type-safe normaliser research
ms.date: 2026-11-13
---

* Source: closure review finding R1 (review-82-c1-1905).
* `finance._norm` calls `.strip()` on any truthy value; grants `_same_person` and `_complete` use it on recorded identity fields, so non-string values raise AttributeError.
* `role` is compared with `!=`, so it is already type-safe.
* Disposition: executed. Planning Readiness: Ready.
* Fix: local `_norm` in grants.py returning "" for non-strings; test code=123, oid=456, email=["bad"] yields unknown, never passes, never raises.

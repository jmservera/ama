---
title: Issue 82 corrupted replacement details (2026-11-05, continuation)
ms.date: 2026-11-05
---

* Tests in `src/core/tests/test_gates.py` (JSON store): corrupted Submitted, Returned and Fixed recover; originals unchanged, event audited; replacement unaccepted and needs independent acceptance; malformed replacement rejected; non-quality role refused; valid in-progress record still refused; unreadable items recover.
* Code: `quality.py` `submit_quality` in-progress check.
* Final gate selectors (pending): `test_gates`, `test_quality_procurement` (JsonFlows and SqlFlows), `test_hazard_referral`.

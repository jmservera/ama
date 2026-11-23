---
title: Issue 349 live r10 details
ms.date: 2026-11-23
---

Test inserts after `test_duplicate_or_conflicting_oid_claims_deny`. Asserts: a second foreign `tid` claim denies; contractor plus `ZavaForward.ApplicationAdmin` denies; a non-string role claim value is ignored and the valid role still maps.

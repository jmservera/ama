---
title: Issue 949 phase details
ms.date: 2026-11-04
---

* Add `current_decision_version(measure)` returning `len(store.cases["ZF-1"]["measure_decisions"][measure])`.
* `review_body` defaults `review_decision_version` to that value.
* Hold test asserts the stored request version equals the derived current version and that it is 2.
* The older-version binding test passes `review_decision_version=1` explicitly.

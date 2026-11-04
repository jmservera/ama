---
title: Issue 949 research - hold route test hardcodes review_decision_version
ms.date: 2026-11-04
---

* Task: issue 949, follow-up from review of #904. Research disposition: executed (direct code read).
* Prior delivery: #904 (97de62ff2) added `test_complaint_and_independent_review_stay_open_under_every_hold`; no later PR touches this follow-up.
* Evidence: `src/core/tests/test_resident_decisions.py` helper `review_body` hardcoded `review_decision_version=1`. The hold test records two decisions for the first measure (Accepted, then Withdrawn), so the current version is 2.
* Contract: `_res_service_open` (`resident_decisions.py`) requires an int version within `1..len(decisions)` and stores it on the request.
* Constraint: `test_review_binding_survives_new_versions_and_retention_ordinal_reuse` deliberately pins version 1 after a newer version exists; it must stay explicit.
* Slice: test-only, no production, security, infrastructure, SQL or deployment change. Focused tier.
* Planning readiness: Ready.

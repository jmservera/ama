---
title: Identity and RBAC review (#141)
---

Review executed once. Outcome: conformant with open items.

* Criteria 1-3 and 5 delivered by matrix, tests, contractor decision recorded as proposed.
* Criterion 2: IoT Hub role present; chat store deferred (no resource).
* Criterion 4: met by explicit manual steps and a named owner, not declaratively (script does not read the manifest). Criterion 5 contractor/B2B decision (#116) remains open.
* Fix round: matrix test now compares parsed (identity, role, scope) tuples; owner wording corrected; db_ddladmin disclosed with a tracked follow-up.
* Follow-ups: owner sign-off, B2B confirmation (#116), live role comparison, drop db_ddladmin.

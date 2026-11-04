---
title: Issue 79 phase details
ms.date: 2026-11-04
---

* `src/core/src/zava_forward/core/ranking.py`: a policy is signed only with a named owner (not "to be named"), a `signoff` record by that owner, an ISO `signed_on` and a `rule_order_hash` equal to the hash of rules and stage order.
* `src/core/src/zava_forward/core/store.py`: `ranking_publication_status` returns `policy_signed` and `signoff_problems` from the current policy.
* Tests: `src/core/tests/test_ranking_publication.py` (SignoffTests), `src/api/tests/test_ranking_publication_wiring.py`.
* Manual path and AI: no AI involved; managers read the same status endpoint.

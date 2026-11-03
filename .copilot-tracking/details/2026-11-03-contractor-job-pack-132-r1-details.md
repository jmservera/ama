---
title: Issue 132 round 1 details
ms.date: 2026-11-03
---

## Design

* Closed allow-list pack; `pack_digest` binds receipts to scope, design and order version.
* Receipts never accepted; `review_blocker` compares name, email, code against worker, keyer and acknowledger.
* Offline merge keyed by `capture_ref`; stale digest is held, not dropped.
* No-show events map to existing outcomes `Rebooking needed` or `No access`; `resident_refusal` always False.
* Escalation owner roles: managers or Building Safety Liaison; `contract_instruction` False.
* Decision proposal: staff-mediated intake; identity approach (B2B guest per #116) undecided.

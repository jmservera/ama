---
title: Plan for #943
ms.date: 2026-11-04
---

* Slice: single slice, whole issue.
* Phase 1: refuse confirmation unless status is the pre-booked "Capacity only, not booked" (named constant), with a reason naming the claim and its state.
* Phase 2: extend `test_value_claim_is_capacity_until_destination_confirmed` with the Booked case and a no-mutation assertion.
* Validation tier: focused (no security, infrastructure, SQL or deployment change). Gate not run.
* Critique: executed once, inline. Compatible finding applied: check status before the different-person rule so the reason is about state; keep the audit log unwritten on refusal. No human approval or consent boundary changes: confirmation still needs a different manager and a budget owner reference.
* Details: [details](../details/2026-11-04-value-claim-reconfirm-943-details.md).

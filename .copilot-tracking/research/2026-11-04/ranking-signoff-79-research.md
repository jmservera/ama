---
title: Issue 79 research, ranking sign-off check
ms.date: 2026-11-04
---

## Research disposition: executed

Planning readiness: Ready.

## Merged work already delivered for #79

* #41 and #36: ranking-v1 policy, hash-checked registry, snapshot endpoint, reasons per card.
* #896, #1039, #1047, #959: retained snapshot archive, manager publish and verify endpoints, overdue flag.

## Acceptance criteria status before this slice

* Same data and policy give same order: proven (existing tests).
* Policy changes versioned and hash-verified: proven (existing tests).
* Named owner signs first rule order: unmet. Owner is "to be named"; status is "Draft ... not yet signed". Status endpoint hard-codes `policy_signed = False`.
* Snapshot publication scheduled and retained: unmet. No scheduler is deployed (deployment and infrastructure step); retention period is a Legal decision.

## Gap chosen

Nothing in code can recognise a real sign-off, so `policy_signed` cannot become true even after a human signs. Smallest coherent slice: a derived, tamper-evident sign-off check bound to the rule order. A scheduler job would need a service identity and deployment, so it is out of this slice (security and infrastructure).

## Constraints

* `ranking.describe` feeds AI source signatures; it is left unchanged.
* No policy file is edited; no human decision is made by the agent.

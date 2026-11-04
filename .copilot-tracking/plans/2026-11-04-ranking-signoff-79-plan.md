---
title: Issue 79 plan, ranking sign-off check
ms.date: 2026-11-04
---

Branch feat/slice-79, target main. Tier: focused (no security, infrastructure, SQL or deployment change).

Stacked slices: 1 sign-off check (this PR); 2 scheduled publication job and retention (needs service identity, deployment and a Legal retention decision; owner and infra gated); 3 the owner's signed policy version (human).

Phases: [x] add `rule_order_hash`, `signoff_problems`, `is_signed` to ranking; [x] derive `policy_signed` and `signoff_problems` in the status; [x] behavioural tests; [x] README note.

Critique (single pass, self-run): compatible findings applied: keep `describe` unchanged for signature stability; sign-off bound to rule and stage order so an edit voids it; document that the check records, not proves, human approval.

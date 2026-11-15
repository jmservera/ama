# Review: Epic #104 criteria 3 and 5 invariant suite

Execution: one independent code-review pass on the candidate suite, then fixes applied. Not repeated. Outcome: conformant for the added suite; criteria 3 and 5 are not proven closed, so neither is ticked.

## Findings applied

* Vacuous snapshot comparison replaced by a comparison of the task's own snapshot.
* Tautological assistant-review and source-grep concern-pack tests removed or replaced with behavioural tests (assistant review stays covered by core `test_assistants_identity`).
* Ranking test proves the AI order differs from the deterministic order.
* Alert tests assert the owner and exactly one new alert per hold.
* Registry test pins exactly chat as live under the full demo environment.

## Boundary of evidence

* Local, synthetic, offline. OD-51 owner approval of real budgets, alert owners and price source is not evidenced; Azure and billing evidence is not produced.
* Criterion 5 residual: held-out (`heldout_batch`) and chat-eval authorisations have a named approving owner and finite limits but no separate alert owner or threshold.

## Routed follow-ups (ranked)

1. Add alert owner and threshold to the held-out and chat-eval authorisations (gate semantics change; full tier).
2. Assistant output validation forbids only "has been sent" claims; a proposal summary such as "I have approved the grant" is accepted as unapproved text. Add an approval-claim filter like chat's `ACTION_CLAIM` (core change).
3. After the #146 worker merges, re-run this suite and re-assess criteria 3 and 5 on the exact head.
4. `Consumption.authorize` accepts zero-count budgets; this fails closed, so low priority.

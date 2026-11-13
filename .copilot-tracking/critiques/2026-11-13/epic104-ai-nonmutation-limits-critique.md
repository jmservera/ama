# Critique: Epic #104 criteria 3 and 5 plan (single pass)

Execution: executed once on the final candidate plan by an independent rubber-duck agent. Verdict: Revise. No second critique was run.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Unchanged authoritative ranking does not prove the AI never ranks | Applied: the test proves the AI proposal differs from the deterministic order, stays `Proposed`, cannot be resolved by another user, and leaves ranking and cases unchanged. The AI order is a proposal only |
| 2 | Owned alert not established; no alert threshold or held-out owner field | Applied: tests assert the alert owner equals the authorised owner (or the OD-51 placeholder); the missing held-out and chat-eval alert fields are a routed follow-up, not claimed as met |
| 3 | Direct ledger calls do not prove dispatch wiring | Partly applied: existing core tests (`test_ai_consumption*`, run in the focused tier) prove `Ai._request` reserves first. No new adapter spy was added |
| 4 | `ask_unstored` bypasses the model path | Applied: chat is covered through the golden `run_eval` (stored path, state-unchanged assertion) and `ChatModel` admission denial |
| 5 | Synthetic-price demo exception | Applied: tests cover the live synthetic-price hold and the exact demo switch; the demo meter exception is recorded as a boundary |
| 6 | Held-out no-call tests can be vacuous | Applied: a valid live batch first reaches the provider, then each limit is removed and no call is made |
| 7 | Hostile-output tests need a positive control | Applied: a valid cited proposal is accepted for each assistant before the hostile variants |

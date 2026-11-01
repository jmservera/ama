# Research: issue 164 chat grounding evaluation, registration and gates (2026-11-01)

* Task: issue-164-chat-registration; mode: automatic; disposition: executed (repository-only)
* Planning Readiness: Ready

## Findings (evidence)

* `src/agents/src/zava_forward/agents/chat_eval.py` already runs 21 scripted multi-turn scenarios, refusals, non-AI comparison, consumption summary and `enablement_decision` (never "pass"). ACs 1, 2 and 5 are ticked (PR 307).
* `src/core/src/zava_forward/core/ai_registry.py` registers assistant and retained tasks only. `chat-case-conversation` (chat_eval.TASK) is not registered: no accountable function, no enable/disable state, no threshold record. This is AC 4's concrete gap.
* `enablement_decision` hard-codes `state="disabled"` and the reviewer as unknown; it reports one aggregate outcome, so AC 3 (memory-poisoning and prompt-injection must pass before enablement) has no explicit per-category gate.
* Known open critical gap in `evals/chat_golden.json`: valid citation but unsupported claim; lexical guards cannot close it. Needs claim-level grounding plus human review.
* Not achievable offline and out of scope: approved thresholds, named reviewer individual, held-out set, actual-model calls, human exercises, spend authority.

## Slice decision

1. Register the chat task in `ai_registry` (accountable function, individual unknown, enabled=false, thresholds proposed/unapproved, constructed-only).
2. Make `enablement_decision` read the registry entry and emit explicit per-gate results (prompt-injection, memory-poisoning, permission, out-of-scope) so "pass before enablement" is checkable; overall stays fail/insufficient.
3. No claim that AC 3 or AC 4 approval clauses are proven: PR uses Refs.

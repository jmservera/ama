---
title: Issue 891 chat call accounting C1 plan
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109-c1
---

## Task metadata

* Parent `issue-891-chat-call-accounting-1109`. Cycle C1 of five (1/5). Research `.copilot-tracking/research/2026-11-09-chat-call-accounting-891-c1-research.md` (Ready). Details `.copilot-tracking/details/2026-11-09-chat-call-accounting-891-c1-details.md`.
* Base `origin/main` `1b7a1719bee088ce2823bff45242e319bc928295`, merged at `97f0036b573f8d0497c0d67904506f8156c11920`.
* Validation tier: focused (owner DEMO targeted validation). Not the complete gate; the change touches a core AI client file but no permission, secret, deployment, SQL, financial rule, guard or dependency, and the coordinator names the actual-code assessment and actual-head CI as later gates.

## Objective

Replace the envelope-inference count in the chat adapter with a trusted per-invocation witness of the dispatch boundary written by core `Ai`, so `ChatModel` reports the actual attempted provider calls.

## Scope

* `src/core/src/zava_forward/core/ai.py`: the witness type, a context manager that opens one, witness marking in `evidence`, the attempt record immediately before `open_request`. No change to any reserve, complete, check, guard, bound or outcome mapping.
* `src/core/tests/`: a focused new test module for the marker.
* `src/agents/src/zava_forward/agents/chat.py`: use the witness; drop the `provider_calls` envelope heuristic.
* `src/agents/tests/test_chat_model.py`, `src/agents/README.md`.
* Excluded: server, navigation, store, schema, activation, registry, `ai_transport.py`, `ai_consumption.py`, chat panel and any dependency.

## Phases

1. Phase A (tests red): core marker tests and adapter tests that count the real transport stub and compare with the reported calls. They must fail before source edits. Includes: original meter-missing zero case, pre-reservation hold (reserve held), post-reservation pre-dispatch hold (`dispatch_check`), prompt-output guard denial, token failure before dispatch, input refusal, dispatch success, dispatch failure, completion hold after dispatch, unconfigured client, concurrent distinct calls, unwitnessed provider.
2. Phase B (implement): the core witness and the adapter change.
3. Phase C: README, `ruff format`, targeted tests and component lint/type checks.
4. Phase D: changes record and the single post-implementation review.

## Design decisions

* `DispatchWitness` has `witnessed: bool` and `attempts: int`; `count_dispatches()` is a context manager that sets a `ContextVar`, resets it on exit, and yields the witness. Only `Ai` code mutates it.
* `Ai.evidence` sets `witnessed` when a witness is open (including the unconfigured path, which makes zero calls). `Ai._request` increments `attempts` immediately before `open_request`, after `_token` and `dispatch_check`.
* `ChatModel.__call__` opens the witness around `worker.provider_call`. Calls are `witness.attempts` when witnessed; an unwitnessed provider yields a conservative 1 with a bounded warning log naming the unverified provenance. No provider-supplied field is read.
* The witness is per invocation: no `Ai` attribute, no module counter, no use of reservation, `meter_id` or outcome to infer dispatch.

## Acceptance

* Every case in Phase A passes, with calls equal to the counted transport (or the documented unverified conservative 1).
* All existing targeted tests, ruff check, ruff format check and mypy pass for core, agents and the API integration subset.
* Documented residual limits: a fence withdrawal at connect or first byte is still counted as an attempt; non-`Ai` providers are unverified; whole criterion 2 stays unproven.

## Risks and rollbacks

* `ai.py` is shared: edits are additive and small. Rollback is reverting the C1 source commit.
* Contextvar not propagating to a provider on another thread yields the explicit unverified conservative count, never an exact zero.

## Critique dispositions (single critique, applied directly)

* Critique `.copilot-tracking/plans/2026-11-09-chat-call-accounting-891-c1-critique.md`: verdict Revise, no user decision needed. No second critique is run.
* PC-001: exactness is scoped to the trusted composition where the provider is core `Ai.evidence`; the witness proves only what `Ai` dispatched, and a provider that also makes calls outside `Ai` cannot be detected. Documented as the composition trust boundary; the unwitnessed case stays explicit and conservative.
* PC-002: carrying provenance in the receipt needs `chat_panel.py` (shared, not owned). Not changed; the adapter logs the unverified case, the count is an upper bound of 1, README states it, and the receipt provenance field is a routed follow-up.
* PC-003: the witness gets a `closed` state set on exit; late increments after close are ignored. Nested scopes: the innermost witness counts its own invocation, the outer is not incremented. Tests cover nested, late mutation after close and a context copied into a thread while open.
* PC-004: the metric is defined as one count per `Ai` provider request at the transport hand-off; redirect follow-ups inside `urlopen` are not separately counted and this limit is documented. No transport change.
* PC-005: the increment is placed after `open_request = ...` has been built and directly before `with open_request(...)`, so opener construction failure is zero. Fence withdrawal inside the opener is still an attempt (documented).

---
title: Phase details for the final unticked criteria of #891 and #107
description: Test design for the demo-switch guardrail class and the five-assistant attribution test
ms.date: 2026-11-13
---

## Phase 2: `DemoActivationGuardrailPersistenceTests` (api tests)

Fixture: `test_assistants.Base` with `open_store` under `AI_ENDPOINT`, `ZF_DEPLOYMENT_PROFILE=demo` and `ZF_CHAT_DEMO_ACTIVATION=approved-2026-11-03`; `Assistants(store, config())` attaches the real ledger; `urllib.request.urlopen` returns a fake provider response; `ChatPanel(ChatIsolation(store, env=refs), ChatModel(AgentWorker(store.ai.evidence), admission=chat_admission))`. Only the transport is faked.

* (a) per-call gate: one ask makes exactly one provider call and one `reserved` event; a second dispatch under the same root is `financial-held` with no extra call; a role with no chat calls and an exhausted thread-turn limit dispatch nothing.
* (b) token and cost admission: with a tiny demo token budget, then a tiny money budget, the ask falls back to workflow-only with zero provider calls and a hold, no `reserved` event.
* (c) privacy refs: missing DPIA, lawful-basis and notice refs refuse the thread and ask before dispatch; with refs present, an email and phone in the question never reach the provider bytes and are stored masked.
* (d) retention: `decision()` retention stays Unknown, `purge_retention` applies nothing, memory is not a prompt input and the demo switch writes no retention reference.
* (e) refusals: out-of-scope action asks are refused with no call; memory content is never in the provider bytes; an uncited reply and an unsupported-claim reply are withheld or replaced by cited rules.

## Phase 3: all-five-assistants attribution (consumption api tests)

On `ConsumptionApi`: authorize each of the five registered capabilities, give each a distinct fake token usage, drive each through `invoke`, `execute`, verify and review (accept for four, reject for one; one proactive request through `_enqueue`). Independently recompute per-assistant calls, tokens, charge and accepted proposals from raw ledger events, assert equality with `report()["by_capability"]` and the cohort accepted count, and assert sentinel case text, resident name and address are absent from ledger events, the report, captured log records and task events.

## Success criteria

* Both new tests fail if the audited behavior is removed (spot-check one mutation per file).
* Targeted suites, ruff, format check, mypy and content-standard pass.

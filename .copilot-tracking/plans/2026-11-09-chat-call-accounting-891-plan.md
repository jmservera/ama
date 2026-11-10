---
title: Issue 891 chat call accounting plan
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109
---

## Task metadata

* Task `issue-891-chat-call-accounting-1109`. Research `.copilot-tracking/research/2026-11-09-chat-call-accounting-891-research.md` (executed, Ready). Details `.copilot-tracking/details/2026-11-09-chat-call-accounting-891-details.md`. Critique `.copilot-tracking/plans/2026-11-09-chat-call-accounting-891-critique.md` (one cycle, to be recorded). State `.copilot-tracking/rpi-sessions/2026-11-09/chat-call-accounting-891-state.json`.
* Branch `fix/demo-chat-call-accounting-891-1109`, base and target `main` `a04668ae94b5c2f38e6c55ed789db245e8c71d16`. Refs #891 only; the whole issue and criterion 2 stay open.

## Executive summary

`ChatModel` reports `calls=1` for a `financial-held` envelope even when the provider adapter held before any reservation and the transport made zero calls. Make the adapter report 0 only when the envelope proves the hold preceded the reservation (and therefore the transport), and keep counting 1 whenever a reservation exists, because a hold can follow a real transport. No core, server, store, schema or Quality change.

## Decisions and requirements

* D1 Order: this plan and details and one critique are committed-as-written before any `src/` edit. Source and tests change only after the critique is recorded and the state is moved to Implement.
* D2 The regression test is written and run red against unmodified source before the correction, and its raw failure is preserved.
* D3 No blanket zero for `financial-held`. A held envelope that carries `meter_id` keeps `calls=1`.
* D4 No real provider, model, network, Azure or spend. Transport is a counted stub. No new dependency; pip only; the isolated venv from research is used.
* D5 Shared paths (`core/ai.py`, server, store, schema, navigation, Quality) are not edited. The precise core transport marker is a reported follow-up.
* D6 Five total correction cycles, none spent; a cycle is a test or review-driven change after the first complete implementation.

## Functional requirements

* FR1 (amended 22:37Z after the critique) `ChatModel` returns `calls=0` for `disabled`, `input-refused` and a `financial-held` envelope without `meter_id`, as the core `Ai.evidence` envelope contract; `calls=1` for every other outcome and for `financial-held` with `meter_id`. Exception type, outcome string (`provider-unavailable`), usage handling and the completion recheck are unchanged.
* FR2 Real `Ai` plus counted transport plus real `ChatPanel`: the receipt `model_calls` and the `chat.turn` audit detail equal the transport count for pre-dispatch holds (meter missing, `reserve` hold) and for a post-dispatch hold (transport made, `complete` held).
* FR3 Existing gates still behave: denied admission and no admission make zero provider calls; completion revocation keeps its transport count and usage; provider failure and timeout count one; default deny, demo disclaimer and refusal tests in core and API remain green.
* FR4 `src/agents/README.md` states the counting rule and the F3/F4 limitation in the consumption provenance section.

## Phases

* Phase 1 regression test red (details Step 1).
* Phase 2 correction in `chat.py` (Step 2) and green.
* Phase 3 README (Step 3).
* Phase 4 targeted validation, lint, format, type (Step 4).
* Phase 5 changes record, state, local commit, review, handoff.

## Validation (targeted, owner DEMO tier; not the full gate)

* Agents: `test_chat_model` module complete; `test_dispatch`, `test_worker`; `discover -p 'test_chat_*.py'`; then the agents suite in full if time and load allow.
* Impacted core and API: `test_chat_panel` (core), `test_ai_consumption_api` and `test_continuity` (API, they use `Ai.evidence` and `financial-held`), `test_chat_panel`/`test_chat_isolation` (API) when the API distribution can be installed into the venv without a manifest change; otherwise record the exact skip and reason.
* `ruff check`, `ruff format --check` and `mypy` in `src/agents`. Planned classification: focused tier (small agents adapter, tests and docs; no workflow, dependency, deployment, permissions or gate change). The full local gate is not run; independent exact-head review, human approvals and hosted CI remain required and are not claimed.

## Risks

* Over-count remains for the `dispatch_check` hold and the guard denial (F3, F4). Mitigation: documented, conservative direction, follow-up named.
* `meter_id` is an envelope convention of the core provider. Mitigation: it is the existing durable provenance written right after `reserve`; a test asserts both sides; a non-core provider that omits it is counted conservatively except for `financial-held`, which only the core provider emits.

## Success criteria

* Red then green regression with raw logs; targeted checks and lint/format/type exit 0 or exact reported failures; scope is `chat.py`, `test_chat_model.py`, the agents README and tracking records only; no push; clean local commits with the Copilot trailer.

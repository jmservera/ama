# Issue 116 live research (2026-11-20)

Task: issue-116-live. Research disposition: executed. Planning Readiness: Ready.
Base HEAD 7c5aca476. Owner decisions of 2026-11-18 apply (synthetic demo, desktop only, live Azure authorised in rg `ama`, no DPO/Legal or billing proof needed).

## Issue state

Live issue #116 has one unticked criterion: "Apply approved task/audience field, type and size allowlists at every provider boundary, including Ai.run/_chat, Ai.evidence, Ai.look_at, document/image bytes, retained legacy families, reactive assistants and proactive scans." Every other box is ticked. Earlier repo evidence: rounds 1 to 4 under docs/reference/research/issue-116-live-*.

## Provider send sites (static)

* `core/ai.py` is the only core send site; `_request_body` calls `approved_payload` (type and size allowlist) before serializer, meter or socket, and `run`, `evidence`, `_chat` and `look_at` all route through it. `look_at` adds its own image mime and size check and a 6000-character text bound.
* Other send sites, all enumerated by `api/tests/test_ai_call_site_inventory.py`: `api/resident_demo/aoai.py` (closed `guidance`/`case` sources, question 1..500 characters), `api/resident_demo/assistant.py` (fixed topic prompt from an enum), `agents/heldout_aoai.py` (prompt bound `max_prompt_tokens` from the owner authorization, `prompt-too-large` stop in `heldout_batch`).
* Callers: `ai_tasks` (typed prompt render), `store.priority` (registered task), `assistants.build_request` (closed capture fields; used by reactive and proactive paths), `agents/dispatch.foundry_provider`, `agents/chat.ChatModel` (panel `skill_sources`).

## Offline evidence run on this checkout (2026-11-20)

* core: `test_ai_provider_payload_spy test_ai_input_bounds test_epic104_bounded_ai_invariants test_ai_register_completeness test_ai_metering_inventory test_chat_provider_position test_discovery_assistant_boundary`: 73 tests OK.
* api: `test_chat_panel test_resident_aoai test_ai_consumption_api`: 135 tests run, one skipped (opt-in Chromium), `test_assistants_dispatch` not importable here (`opentelemetry` not installed, environment only). `test_ai_call_site_inventory`: 6 OK.
* agents: `test_chat_model`: 17 OK.

## Gap found

`AssistantSerializer` spies the exact wire body only for tasks with `dispatch={}` (requested path). `build_request` also receives `dispatch` for proactive scans (trigger `proactive`, `as_of`); no spy proves that a proactive task, even one whose dispatch metadata carries extra keys, sends the same closed payload. The code reads only `dispatch.as_of`, so this is a coverage gap, not a behaviour defect.

## Live proof boundary

The payload sent to the model is not observable from the deployed apps, and a billable model call is unnecessary for the demo. Only the earlier unknown-task refusal (400 before any provider call, round 3) is reachable live. No Azure resource is created or changed.

## Follow-ups

1. Install opentelemetry to run `test_assistants_dispatch` locally (environment).

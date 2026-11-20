---
title: Entra roles and field-level visibility, provider-boundary evidence round 5 (#116)
description: Boundary-by-boundary offline proof of the one remaining unticked criterion of issue 116, one new proactive-path provider spy, and what stays unproven
ms.date: 2026-11-20
---

## Scope

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. The issue now shows one unticked box: allowlists at every provider boundary. No Azure resource was created or changed, and no credential was read. Tests ran on this checkout (base 7c5aca476) on 2026-11-20.

## Boundary matrix

| Boundary | Task or audience fields | Type and size allowlist | Recorded test evidence |
| --- | --- | --- | --- |
| `Ai.run` and `_chat` | Registered task only; typed prompt render | `approved_payload` before serializer, meter and socket | `test_ai_provider_payload_spy` (`WrapperBodies`), `test_ai_input_bounds` |
| `Ai.evidence` | Closed capability capture; unknown capability refused | Same `approved_payload`; oversize returns `input-refused` | `WrapperBodies`, `AssistantSerializer`, `test_ai_input_bounds` |
| `Ai.look_at`, document and image bytes | File name only in the instruction | PNG and JPEG, 4 MiB; text first 6000 characters | `LookAtBodies` |
| Retained legacy families | Role projection with closed selected fields | Shared boundary | `LegacyRoleProjection` |
| Reactive assistants | `assistants.capture` closed sources per capability | Shared boundary | `AssistantSerializer` |
| Proactive scans | Same `build_request`; only `dispatch.as_of` is read | Shared boundary | New `test_proactive_task_sends_the_same_closed_payload` |
| Employee chat | Panel `skill_sources` | Shared boundary via `ChatModel` and `AgentWorker` | `test_chat_panel`, `test_chat_model` |
| Resident demo, held-out runner | Closed `guidance` and `case` sources, fixed topic enum; owner-authorised prompt bound | Question 1 to 500 characters; `prompt-too-large` stop | `test_resident_aoai`, `test_ai_call_site_inventory`, `test_heldout_aoai` |

## Result

* core: 73 tests OK (spy, bounds, bounded-AI invariants, register completeness, metering inventory, chat provider position, discovery boundary); after the new test the spy module runs 15 tests OK.
* api: `test_chat_panel`, `test_resident_aoai`, `test_ai_consumption_api`: 135 run, 0 failures, 1 skipped (opt-in Chromium). `test_assistants_dispatch` could not be imported because `opentelemetry` is not installed here; it was not run. `test_ai_call_site_inventory`: 6 OK.
* agents: `test_chat_model` 17 OK.
* Mutation check: when `build_request` appends the dispatch metadata, the new test fails; unmodified it passes.
* `python3 -m mypy` in `src/core`: 23 errors, identical with and without the change (missing `opentelemetry` stubs). `ruff check` and `ruff format --isolated --line-length 100 --check` pass on the changed file.

## Finding

The gap was coverage, not behaviour: the assistant spy exercised only requested tasks. `build_request` reads no dispatch field other than `as_of`, so the proactive path already sent the closed payload. The new test pins that.

## Acceptance criteria

| Criterion | Status | Basis |
| --- | --- | --- |
| Allowlists and size limits at every provider boundary | Proven offline for every enumerated boundary; not observable live | Matrix above; the call-site inventory test fails if a new provider call site appears unclassified. The payload sent to the model is not visible from the deployed apps and a billable call is not needed for the demo. Production still needs independent review and hosted CI |
| All other boxes (role-by-endpoint, contractor view, redaction decision, reason roles) | Ticked on the issue before this round | Not re-proven live; rounds 3 and 4 hold the live and offline evidence |

Unproven: live payload contents, a second live role, and `test_assistants_dispatch` in this environment. No box is ticked by this note; the owner ticks after review.

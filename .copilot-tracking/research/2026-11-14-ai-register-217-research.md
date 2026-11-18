---
title: AI feature register research (issue 217)
ms.date: 2026-11-14
---

## Question

Does every AI or automated feature carry purpose, inputs, prohibited uses, limits and a named owner, and can an unregistered feature be enabled or invoked? Disposition: executed. Planning Readiness: Ready.

## Findings

* `src/core/src/zava_forward/core/ai_registry.py` already registers 13 tasks (five assistants, six retained paths, chat, concern pack) with `purpose` and `prohibited_uses`.
* Entries lacked explicit `inputs`, `limits` and `owner` fields; `source_permissions` and `accountable_function` held equivalent data under other names.
* `ai_tasks.require_registered` and `dispatch.TaskMessage.from_json` gated tasks, but `Ai.run` called the model for any task name (tests used "draft", "summarise", "syn-task").
* `Ai.look_at` always uses the registered `read_document` task. Chat is gated by `ChatModel` admission and the registry demo switch.
* Owner remains a function; `accountable_individual` stays `unknown` (no approval is implied).

## Evidence boundary

Constructed offline scaffolding; no approval, DPO, Legal or RAI decision is recorded or implied.

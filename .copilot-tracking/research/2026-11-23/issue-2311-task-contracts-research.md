---
title: Issue 2311 research, per-task data contracts
ms.date: 2026-11-23
---

## Disposition

Research executed 2026-11-23. Planning Readiness: Ready.

## Findings

* `src/core/src/zava_forward/core/ai_registry.py` registers 13 tasks (5 assistants, 6 retained paths, chat, concern pack) with a coarse `inputs` category list but no field-level contract.
* Retained text tasks build prompts only through `ai_prompts.render(task, **values)` (store.py, heldout_eval.py); that is the single chokepoint to enforce before a prompt is built.
* `export_fields.scalars` already refuses unknown fields for external context; it has no per-task contract, types, lengths or prohibited content.
* All five #2311 criteria are code, test or non-claim; no Azure resource is needed, so no live Azure action is taken.

## Decision

New `task_contracts.py` holds a contract per registered task; `ai_prompts.render` calls it. User permission is not an input that can satisfy a contract.

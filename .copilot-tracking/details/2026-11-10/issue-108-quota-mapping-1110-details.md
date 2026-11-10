---
title: Issue 108 quota usage-name mapping details
description: Exact query shapes and stop rules for Q5 to Q8
ms.date: 2026-11-10
---

## Phase 1: queries

Each command sets `AZURE_EXTENSION_USE_DYNAMIC_INSTALL=no`, uses `-o json`, saves stdout and stderr externally, and counts against the original eight.

| Q | Command shape | Proceed only if |
| --- | --- | --- |
| 5 | `az cognitiveservices model list -l uksouth --query "[?model.name=='gpt-4.1-nano' && model.version=='2025-04-14'].{kind:kind,name:model.name,version:model.version,skus:model.skus[?name=='GlobalStandard'].{sku:name,usageName:usageName}}" -o json` | Always. Require exactly one entry with `kind` `OpenAI` and exactly one `GlobalStandard` SKU with a non-empty `usageName`; otherwise stop (mapping unresolved). The CLI filters client-side, so the catalog is fetched in memory only; projected rows only are kept. If the field name differs (schema unverified), that is recorded and the lane stops without a guessed second projection beyond the retry |
| 6 | `az cognitiveservices usage list -l uksouth --query "[?name.value=='<usageName from Q5>'].{n:name.value,limit:limit,unit:unit}" -o json` | Q5 returns exactly one non-empty `usageName`. `currentValue` is never projected. Publish limit and unit only from exactly one row with both fields present; duplicates, nulls or an empty result: unknown, not zero, and not proof the quota is missing |
| 7, 8 | One retry of Q5 or Q6 for a transient read failure only | Transient error classified from stderr; otherwise unused |

## Rules

Stop on ambiguous mapping, permission denial or missing tool. Stderr sanitized before any repository text. A local `az` help read is not a metadata query and is disclosed.

## Phase 2 and 3

Supplementary paragraph, query timestamps and provider units in the same subsection; index and log deltas; checks per the [plan](../../plans/2026-11-10/issue-108-quota-mapping-1110-plan.md). Review created only after implement-done.

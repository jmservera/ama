---
title: Issue 108 quota usage-name mapping research
description: Prospective research for resolving the provider quota usage name of one already observed deployment model
ms.date: 2026-11-10
---

## Task

`issue-108-quota-mapping-1110`, parent [issue-108-model-metadata-1110](issue-108-model-metadata-1110-research.md), frozen baseline `2728993495b2d3157d79dad66410a51c78239447` (preserved, not edited). Research disposition: executed.

## Evidence

* The parent pass spent 4 of 8 read queries. Its Q4 projected the regional usage list with a `starts_with` filter on two guessed spellings (`OpenAI.GlobalStandard.gpt-4.1-nano`, `OpenAI.GlobalStandard.gpt4.1-nano`) and returned `[]`. Earlier repository evidence (`infra/README.md`, 2026-10-18) records usage names of the form `OpenAI.GlobalStandard.gpt4.1-mini` with no returned row, so the usage name is not the model display name and an empty guessed filter is inconclusive, not proof of absence.
* Tool help (not a metadata query), read 2026-11-10: `az cognitiveservices model list -l <location>` shows regional model catalog entries; `az cognitiveservices usage list -l <location>` has `--filter` (undocumented semantics) and no server-side name selector. Catalog entries are expected to carry SKUs with a `usageName`; the exact schema is unverified and is probed by a projection; an empty projection means only "no mapping returned by this projection", not schema confirmation or model absence.

## Plan basis (budget Q5 to Q8, at most four)

1. Q5: regional catalog (`uksouth`) projected only to the entry for model `gpt-4.1-nano` version `2025-04-14` and its `GlobalStandard` SKU `usageName` and capacity bounds. Public catalog; no other model is output.
2. Q6: regional usage list projected only to the exact `usageName` from Q5, returning `limit` and `unit` (never `currentValue`).
3. Q7, Q8: reserved for one transient retry only. No further attempt.

Stop if the mapping is absent or ambiguous, or on permission or tool failure. Unknown is not zero; a missing row is not proof the quota is missing.

## Semantics

Quota limit is not reserved capacity, headroom or budget; no TPM conversion; alias and configured version are not serving attestation. Planning Readiness: Ready.

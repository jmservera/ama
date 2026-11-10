---
title: Issue 108 regional model metadata observation details
description: Phase details and exact query shapes for the read-only model metadata observation
ms.date: 2026-11-10
---

## Phase 1: read-only queries

All commands use the existing authenticated context, `-o json`, narrow `--query` projections and `2>` captured to the external evidence root. Budget eight invocations; one retry only for a transient read failure.

| Q | Command shape | Proceed only if |
| --- | --- | --- |
| 1 | `az containerapp show -g ama -n ca-cutover-test-demo-api --query "properties.template.containers[].{container:name,env:env[?name=='AI_ENDPOINT'\|\|name=='AI_DEPLOYMENT'].{name:name,value:value,hasSecretRef:secretRef!=null}}" -o json` (the backslashes are table escaping only; the real command has a plain doubled pipe; query tested locally against a fabricated document) | Always; stop the lane on error. A secret reference is recorded only as a boolean, its name is not projected and it is not resolved. Require exactly one container carrying both settings; ambiguity or absence stops the lane |
| 2 | `az cognitiveservices account show -g ama -n <account from endpoint host> --query "{kind:kind,location:location,sku:sku.name,endpoint:properties.endpoint}"` | Q1 gives a public endpoint whose first host label names the account; the endpoint returned must match |
| 3 | `az cognitiveservices account deployment show -g ama -n <account> --deployment-name <AI_DEPLOYMENT> --query "{sku:sku,model:properties.model.name,version:properties.model.version,upgrade:properties.versionUpgradeOption,state:properties.provisioningState,cap:properties.currentCapacity}"` | Q2 identity confirmed |
| 4 | `az cognitiveservices usage list -l <account location> --query "[?starts_with(name.value,'OpenAI.<SKU>.<model, hyphenated>')\|\|starts_with(name.value,'OpenAI.<SKU>.<model, unhyphenated>')].{n:name.value,limit:limit,unit:unit}" -o json` (the real command has a plain doubled pipe; the earlier 2026-10-18 evidence spelled the name `gpt4.1-mini`, so both spellings sit in one query) | Q3 model and SKU known; `currentValue` is never projected. The CLI filters client-side, so the full list is fetched in memory only; nothing but the projected rows is written or published, and this is disclosed |

Fallback if Q4 returns an empty list or a permission error: record quota limit and unit as unknown with the exact outcome; do not guess the usage name beyond the one retry.

Handling rules from the critique: stderr goes to a separate external file and is sanitized (subscription ids, principal ids, resource ids, hostnames beyond the project endpoint) before any repository text; raw evidence is never committed. Every `az` invocation, including a retry, counts against the eight; local `az --version` is not a metadata query and is disclosed separately.

## Phase 2: synthesis

Add subsection "Regional metadata observation (2026-11-10)" under the existing configured-demo-model section of [AI Tokenomics](../../../docs/reference/resources/ai-tokenomics.md) with a query table, outcomes, queried time, semantics and the unchanged remaining gates. Update the front matter `ms.date`, the [index](../../../docs/reference/README.md) entry for the page and append a [log](../../../docs/reference/log.md) entry.

## Phase 3: validation and review

Check no subscription id, identity or aggregate usage appears in committed text (`git grep`), links resolve, and the diff is scoped to the knowledge base and RPI tracking. Create the review only after the implementation-done marker and finalize it before review-done.

## Dependencies

External raw evidence under `evidence-108-model-metadata-1110`; witness wrapper preflight before every marker.

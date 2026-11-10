---
title: Issue 108 regional model metadata observation changes
description: Prospective changes record for the read-only model metadata observation
ms.date: 2026-11-10
---

## Status

Implemented 2026-11-10. Four of eight budgeted read-only queries run; knowledge base updated; validation below.

## Planned files

* `docs/reference/resources/ai-tokenomics.md` (changed): dated metadata subsection under the configured demo model section, and `ms.date`.
* `docs/reference/README.md`: index sentence for the page.
* `docs/reference/log.md`: appended entry.
* `.copilot-tracking/` research, plan, details, critique, changes, review and state for `issue-108-model-metadata-1110`.

## Query ledger

| Q | UTC start | Exit | Result | External locator (private) |
| --- | --- | --- | --- | --- |
| 1 container app env projection | 2026-11-10T17:50:46Z | 0 | one container, `AI_ENDPOINT` and `AI_DEPLOYMENT` plain values, no secret reference | `evidence-108-model-metadata-1110/q1.*` |
| 2 account show | 2026-11-10T17:50:53Z | 0 | `AIServices`, `S0`, `uksouth`; same account label, different endpoint domain | `q2.*` |
| 3 deployment show | 2026-11-10T17:50:54Z | 0 | `GlobalStandard` 10, `gpt-4.1-nano` `2025-04-14`, `NoAutoUpgrade`, `Succeeded` | `q3.*` |
| 4 regional usage projection | 2026-11-10T17:50:59Z | 0 | `[]`: quota limit and unit unknown | `q4.*` |

Budget spent 4 of 8; no retry. Local `az --version` (not a metadata query) ran once before the pass. Stderr held only a containerapp extension warning.

## Divergences from the plan

None. Q4 used both quota-name spellings in one query as planned; no second quota attempt was made, so limit and unit are unknown.

## Validation (focused tier)

Provenance and scope reviewed; relative links and anchors checked; no subscription id, identity, secret or aggregate usage in the diff; Git diff scoped to three knowledge base files plus RPI tracking. No runtime, test, provider or hosted check ran.

## Limitations

Read-only configured metadata; not serving attestation, not reserved capacity, not an evaluation. Whole #108, RAI and Tokenomics remain open.

## Erratum (2026-11-10, correction C1)

Appended after a focused independent Readiness assessment; the text above is preserved unchanged as the historical record. The statement "None" under "Divergences from the plan" is qualified as follows.

* The Q2 account metadata reported the account's advertised endpoint domain as `cognitiveservices.azure.com`, while the configured `AI_ENDPOINT` host used `openai.azure.com`. Literal endpoint-string equality between the configured endpoint and the queried account therefore did not hold.
* Q3 proceeded on the same account label inside resource group `ama`. That is a label match only: no endpoint equivalence, network identity or serving attestation was established.
* Q1 to Q4 raw observations, the exit codes and the unknown regional quota limit and unit are unchanged. The criterion stays unticked.

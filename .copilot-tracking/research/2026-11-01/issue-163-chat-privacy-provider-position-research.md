# Research: issue 163 chat privacy, DPIA and retention, 2026-11-01

* Task: issue-163-chat-privacy-provider-position. Disposition: executed (targeted). Planning Readiness: Ready.
* Branch: docs/chat-privacy-dpia-retention (worktree issue-163), base 17e9e297.

## Acceptance state found

| Criterion | Status on main | Evidence |
| --- | --- | --- |
| 1 Data map | Met | `chat_privacy.DATA_MAP`, DPIA record Data map |
| 2 Lawful basis, notice, DPIA decision by DPO and Legal | Unmet, human decision | Record states none given; `CHAT_*_REF` empty. Cannot be authored by an agent |
| 3 Rights locate and erase | Met | `ChatPrivacy.locate/export/erase`, tests |
| 4 Diagnostic and performance exclusion | Met | `diagnostic_safe`, RULE-026 |
| 5 Provider data handling and region | Unmet per 2026-10-31 closure audit: terms never retrieved | Record Model provider section, `MODEL_PROVIDER_POSITION.open_items` |
| 6 Free-text warning, redaction | Met for the regulatory and general staff panels | `chat_privacy.WARNING`, `redact` |

## Findings for criterion 5

Retrieved 2026-11-01 from Microsoft Learn, "Data, privacy, and security for Foundry
Models sold by Azure" (https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy,
page ms.date 2026-05-18, updated 2026-06-05). First 20,000 characters read; the tail
(DPA links) was not retrieved.

* Prompts, completions and embeddings are not available to other customers or OpenAI, and are not used to improve models without permission.
* Models are stateless. Inference is processed in the customer-specified geography, possibly across regions within it; Global and DataZone deployment types may process outside it, while data at rest stays in the designated geography.
* Stateful features (Responses API, Assistants threads, stored completions) persist data in the customer's resource, encrypted at rest, customer-deletable.
* Abuse monitoring: samples of prompts and completions may be stored and human-reviewed by authorised Microsoft staff (EEA staff for EEA deployments) within the resource geography; only approved customers may modify it. Verifiable through the `ContentLogging` capability.
* Processing is governed by the Microsoft Products and Services Data Protection Addendum.
* Previews may differ.

## Not determinable from the repo or the page

* Deployment type actually used (Standard, DataZone or Global) and whether uksouth counts as a UK geography for the processor commitments.
* Whether modified abuse monitoring is approved, and the DPA/IDTA transfer position. These need DPO and Legal.
* Lawful basis, notice and DPIA decision (criterion 2).

## Scope decision

Deliver documentation plus a minimal code-constant update: record the documented provider position (marked as vendor documentation, not DPO-accepted), add a DPO and Legal decision pack that keeps every decision field blank, and refresh stale open items. Criterion 2 stays unmet, so the PR uses `Refs`.

---
title: Chat and Memory Data Protection Analysis Record
description: Draft DPIA working record for per-user agent chat and memory (ADR 0004, issue #163) - data map, decision record, rights handling, logging and redaction, with open items for the DPO and Legal
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

## Status

Draft working record, not an approved DPIA. The owner named Juan Manuel Servera
as the Legal, Compliance and DPO owner on 2026-10-15. No lawful basis, staff
notice or DPIA decision is recorded here, because none has been given. The
demonstrator holds constructed, labelled synthetic data only (ADR 0005). Chat
and memory are not built; the controls are in `mvp/zavaforward_mvp/chat_privacy.py`
and stay refused until the DPO and Legal record references.

Limits of this change, stated plainly:

* The model provider data handling position is not recorded. The Azure OpenAI terms were not retrieved, so nothing here says what the provider retains or monitors.
* The free-text warning is not wired into any UI. `WARNING` exists as text only; no screen shows it yet.
* Lawful basis, staff notice and the DPIA decision are unrecorded and stay with the DPO (Juan Manuel Servera).

Sources: [ADR 0004](../../adrs/0004-per-user-agent-chat-and-memory.md), BRD
CON-003, RULE-019, RULE-022, RULE-025, RULE-026, PRD FR-050 to FR-059, and the
[data-protection snapshots](../regulatory/data-protection/) (UK GDPR current
text, Data Protection Act 2018; check the register before relying on them).

## Data map

| Class | Content | Location | Retention |
| --- | --- | --- | --- |
| Messages and thread headers | Staff typed text, assistant replies, user key, case, task | Azure SQL `chat_thread`, `chat_message` (#160 chat repository, `owner` column), uksouth | Unknown until DPO approval |
| Memory items | Opt-in notes, off by default, never special-category or consent data | Azure SQL `chat_memory`, uksouth | Unknown; expiry required once set |
| Prompts sent to the model | Own thread, own memory, projected case data | Azure OpenAI deployment in uksouth; not stored by Zava | Provider terms Unknown |
| Diagnostic logs | Ids, counts, status only | Process output, Azure Monitor | Platform policy; no content |
| Audit ledger | Event metadata, no content | Append-only ledger | Ledger policy |

## Decision record

| Item | Position | Owner |
| --- | --- | --- |
| Lawful basis | Not recorded. `CHAT_LAWFUL_BASIS_REF` empty | DPO and Legal |
| Staff notice | Not recorded. `CHAT_NOTICE_REF` empty | DPO and Legal |
| DPIA decision | Not recorded. `CHAT_DPIA_REF` empty | DPO and Legal |
| Retention | No period set. Storage code refuses retention unless `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS` exist. The legal retention lock is deferred by owner decision | DPO and Legal |
| Performance use | Prohibited without a separate decision (RULE-026) | DPO, Legal, HR if named |

## Rights requests

`ChatPrivacy.locate`, `export` and `erase` run through the #160 chat repository
(`chatthreads.py`), which owns `chat_thread` and `chat_message` (owner, owner role,
row version, composite thread and sequence key). They find, return and delete a
user's threads, messages and memory by the `owner` column. Only `chat_memory` is
new; its DDL sits beside the chat DDL and is created by the store dialect hooks
(SQLite and Azure SQL). This module opens no connection and issues no DDL. Erasure returns counts
for a metadata-only audit event, so ledger tamper evidence is unaffected. The
request intake, identity check and response deadline process is an owner item.

## Logging and measurement

Diagnostics pass through `diagnostic_safe`, which keeps ids, counts and status
and drops content. Chat and memory content is not an input to time capture or
any performance measure.

## Model provider and region

Direct Azure OpenAI calls through the existing Foundry deployments in uksouth
(owner decision 2026-10-15). Zava stores no prompts. Provider processing terms,
abuse-monitoring retention and any transfer position were not retrieved and are
not verified here.

## Free text warning and redaction

The UI must show (not yet wired into any UI) `chat_privacy.WARNING` beside every free-text field. Messages
are masked for emails, phone numbers, National Insurance numbers, postcodes and
special-category cue words before storage. Memory containing a cue word is
refused, not masked. Masking is best effort and cannot prove absence.

## Memory lifecycle (#161)

Built in `chat_privacy.py`, not wired to any UI or endpoint. Memory is off until the user acknowledges the notice (`opt_in`) and
only after the DPO and Legal references exist. Items carry content, source, class, creation date and expiry; the user can list,
edit, delete one or clear all, and withdrawing deletes them. Classes: `working_preference`, `terminology`, `task_context`; each
retention period stays Unknown until `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS` are recorded. Special-category text is refused.
Memory enters a prompt only as non-authoritative, non-evidence preferences, and ids with prefix `CM-` are rejected as evidence
references. An administrator can switch memory off globally or per task (`chat_memory_control`); items stay visible and deletable.

## Open items

* Owner decision (open): which Entra app role is the memory administrator. `MEMORY_ADMIN_ROLES` uses Retrofit Programme Manager as a placeholder. The role is read from the staff register record, not from the caller's session data.
* Retention (expiry) is Unknown until the DPO approves a period. Expired items are filtered on read once an expiry is set.
* Memory scoping and wiring to users (UI, endpoints, which users see memory) remain open.
* Schema: `chat_memory` gains `item_class`, `source`, `updated_at` through an idempotent ALTER on SQLite and Azure SQL start-up, so a #163-era table is upgraded. `add_memory` requires a known task so the per-task switch always applies.

* DPO and Legal: lawful basis, staff notice, DPIA decision, retention per class, access and break-glass policy (BRD OD-45, OD-46).
* Retrieve and record current Microsoft Azure OpenAI data handling, abuse-monitoring and region terms.
* Rights request intake process and deadlines.
* Model provider data handling is not recorded; retrieval of the terms stays open.
* Wire `WARNING` and redaction into the chat UI when the chat feature is built (#159 onward); this change delivers the controls only.
* Confirm audit ledger metadata retention.
* Dependencies #120 and #121 were not assessed here.

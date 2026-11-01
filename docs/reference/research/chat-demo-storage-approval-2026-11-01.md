---
title: Chat Storage Approval for the Synthetic-Data Demo
description: Dated owner decision enabling chat storage for the synthetic-data demo only, with the references that CHAT_DPIA_REF, CHAT_LAWFUL_BASIS_REF, CHAT_NOTICE_REF and CHAT_RETENTION_REF point to
author: AMA programme
ms.date: 2026-11-01
ms.topic: reference
---

## Decision

On 2026-11-01 (17:46 UTC) Juan Manuel Servera, the DPO, Legal and Compliance
owner named in `chat_privacy.ChatPrivacy.decision()` and in
[the chat and memory DPIA record](./chat-memory-dpia.md), decided:
"Approve all needed to enable storage."

Scope is the synthetic-data demo only: the deployed employee site and the
resident demo site, which hold constructed non-identifying data and no real
residents or staff content.

This is not an approval for production or real personal data. Real-resident
use needs a separate DPO and Legal approval before production. Criteria 2 and
5 of #163 stay deferred. The record is the owner's decision as relayed to the
agent; it is not a legal opinion and no agent has decided that a legal duty is
met.

## References

The deployed settings point to the anchors in this record.

| Setting | Value | Anchor |
| --- | --- | --- |
| `CHAT_DPIA_REF` | `docs/reference/research/chat-memory-dpia.md` | [DPIA reference](#dpia-reference) |
| `CHAT_LAWFUL_BASIS_REF` | `docs/reference/research/chat-demo-storage-approval-2026-11-01.md#lawful-basis` | [Lawful basis](#lawful-basis) |
| `CHAT_NOTICE_REF` | `docs/reference/research/chat-demo-storage-approval-2026-11-01.md#notice` | [Notice](#notice) |
| `CHAT_RETENTION_REF` | `docs/reference/research/chat-demo-storage-approval-2026-11-01.md#retention` | [Retention](#retention) |
| `CHAT_RETENTION_DAYS` | `30` | [Retention](#retention) |

## DPIA reference

The existing [chat and memory DPIA record](./chat-memory-dpia.md), with its
data map, rights controls and decision pack, is the DPIA reference. For the
demo the owner's decision above resolves D1, D3, D4 and D5 for synthetic data
only, with the conditions in this record. D2, D6 and D8 are not extended to
real data. D7 stays prohibited.

## Lawful basis

Demo only. The data is synthetic and constructed. No real resident or staff
personal data is processed. The purpose is the owner's legitimate purpose of
demonstrating the product to the programme. This is the owner's recorded
basis for the demo, not a legal assessment for real data.

Conditions:

* Do not type real personal, special-category or resident contact data. The
  chat warning and best-effort masking stay in place and are not a guarantee.
* Test and demo users only.
* Model activation stays a separate approval; this decision enables storage
  and does not turn on any model.

## Notice

The notice is the text already shown in the employee chat panel:
`chat_privacy.WARNING` (no special-category or resident contact details, masking
can miss things), the retention line, and "Synthetic data only. Model
activation requires separate approval." from `web/chat.js`. The resident demo
shows its own advisory notice and stores no chat thread. Changing either notice
needs the owner's review.

## Retention

30 days for the demo. Rationale: long enough to review a demo cycle and
run acceptance checks, short enough that nothing synthetic lingers, and a round
period that the owner can shorten. It applies to chat messages and memory items
through `CHAT_RETENTION_DAYS`. Ledger metadata follows the ledger policy. This
is a demo period, not a legal retention schedule, and it does not set one for
real data.

## Prohibited use

Chat and memory content stays excluded from performance measurement
(RULE-026). Any change needs its own DPIA update, HR and staff consultation.

## What this changes

* The deploy path sets the five settings on the employee API app and the
  resident demo app (infra change, same PR).
* The employee chat stores threads for authenticated users. Per-user
  isolation, authentication and the other DPIA controls are unchanged.
* The resident demo app does not read these settings today. It stores no chat
  thread, so its behaviour does not change.

## Not approved

* Production use or any real personal data (#163 criteria 2 and 5).
* Provider terms, deployment type and abuse monitoring (D6).
* Resident data lawful basis and Article 9 conditions (D2).
* Rights intake process (D8).

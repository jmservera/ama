---
title: Resident chat learning record (synthetic demo)
description: What the synthetic resident demo chat saves about each question, why, how it is bounded, how the team reads it, and what real-resident use would need
ms.date: 2026-11-01
ms.topic: reference
---

## Purpose

The owner asked whether resident chat conversations are logged so the team can
learn how to improve the experience. Before this change nothing was saved. The
demo now keeps a small learning record so the team can see which questions the
chat did not understand and improve its routing. Refs #466.

## What is saved

One row per chat turn in `src/api/src/zava_forward/api/resident_demo/chat_log.py`,
in a local SQLite file named by `ZF_DEMO_CHAT_LOG_PATH`. It uses the same local
file pattern as the callback agenda. No new infrastructure and no Azure change.
Leave the setting unset and nothing is saved.

| Field | Content |
| --- | --- |
| Time | When the question was answered |
| Session id | One-way hash of the sign-in session id. It is not the resident, case id or email, and a new sign-in gets a new id |
| Topic | The topic that answered (status, documents, forms, home, pause, contact, repair, consents, appointments, regulations, safety), `unrouted` for a harmless question the chat did not recognise, or `refused` for an instruction injection or a request outside the advisory boundary |
| AI enabled | Whether an AI advisor was configured for that turn |
| Question text | Saved only because every demo resident is synthetic. Empty when the resident chose a listed topic. Limited to 200 characters. Emails, UK postcodes and long numbers are masked before saving |

Never saved: the answer text, the resident or case identity, email, address,
case facts and the model prompt.

## Consent and visible flag

* A turn is saved only after the resident has ticked the existing consent box
  "Use my question and limited own-case details for this chat". Requests
  without it are rejected before anything is saved.
* The chat page says: "Synthetic demo only: questions you type may be saved,
  without your name or email, to help the team improve this chat. Do not type
  real personal details."
* Ticking the box is not consent to works. Chat still cannot approve, give
  consent, book or change a case.

## Bounds

* Retention: 14 days. Older rows are deleted on the next write.
* Size: 2,000 rows. The oldest rows are deleted first.
* The file is created with owner-only permissions (0600).
* A failure to save never blocks the chat answer.

## Operator summary

The team reads the record with:

```bash
python -m zava_forward.api.resident_demo.chat_log summary /absolute/path/chat-learning.sqlite
```

It prints the number of questions, the counts of `unrouted` and `refused`
questions, counts by topic and the most common unrouted and refused phrasings,
so routing words can be added. It is read only and never creates a file.

## Routing changes it supports

Owner feedback showed that real questions fell to the flat refusal:
"Can I unpause it?", "How do I unlock my case? Who should I contact?" and
"What docs are missing?". The router now accepts more phrasings for documents,
forms and case status, and has a pause topic and a contact topic. They explain
only recorded facts: whether the record shows contact is paused, and that only
a person can lift a pause. They point to the housing officer or local office,
and say no phone numbers or addresses are recorded. An unrecognised but
harmless question now gets the closest topics as suggestions and the housing
officer route. Instruction injection, other residents' records, approving,
consent, booking and similar requests are still refused. With AI enabled,
status, home and repair questions still use the resident's own case record and
sources. The new topics and the fallback never call AI.

## Real-resident use is not approved

This record is for synthetic demo data only. Saving real residents' questions
is personal data processing. It needs written approval from the Data Protection
Officer and Legal first, covering purpose, lawful basis, notice, retention,
access, redaction and who may read it. The related chat and memory DPIA
decision is deferred under #163. Do not set `ZF_DEMO_CHAT_LOG_PATH` for any
service that signs in real residents. This note does not give legal advice and
is not an approval.

## Evidence

* Code: `chat.py` (router, pause and contact topics, fallback), `chat_log.py`,
  `app.py` (save after a successful answer).
* Tests: `src/api/tests/test_resident_chat_api.py`.
* Working files: `.copilot-tracking/` research, plan, changes and review dated
  2026-11-01 (`resident-chat-learning`).

---
title: Chat and Memory Data Protection Analysis Record
description: Draft DPIA for DPO review covering chat, memory and the synthetic regulatory assistant, with unresolved lawful basis, retention, rights and provider terms
author: AMA programme
ms.date: 2026-11-01
ms.topic: reference
---

## Status

Draft working record, not an approved DPIA. The owner named Juan Manuel Servera
as the Legal, Compliance and DPO owner on 2026-10-15. No lawful basis, staff
notice or DPIA decision is recorded here, because none has been given. The
demonstrator holds constructed, labelled synthetic data only (ADR 0005). Chat
and memory controls are in `src/core/src/zava_forward/core/chat_privacy.py`.
The subsequent synthetic regulatory lookup is built and requires explicitly
simulated privacy references. Neither a configuration reference nor passing
tests completes this DPIA or authorizes actual staff/resident processing.

Limits of this change, stated plainly:

* The model provider data handling position is documented from vendor terms (see Model provider and region) but not accepted by the DPO or Legal.
* The regulatory and general staff panels display `WARNING` beside their question fields and
  reports unknown or simulated retention. This does not establish comprehension
  or consent, and masking remains best effort.
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
| Retention | No approved period set. Memory expiry uses `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS`; regulatory thread age is read-only review metadata, not an enforced disposal schedule. The legal retention lock is deferred by owner decision | DPO and Legal |
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
(owner decision 2026-10-15). Zava stores no prompts.

Documented provider position (2026-11-01, Refs #163). Source: Microsoft Learn,
[Data, privacy, and security for Foundry Models sold by Azure](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy),
page dated 2026-06-05, retrieved 2026-11-01. This is vendor documentation, not
legal advice, not a verified property of the deployed resource and not DPO
acceptance. Mirrored in `chat_privacy.MODEL_PROVIDER_POSITION["documented_terms"]`.

| Topic | Documented position | Remaining check |
| --- | --- | --- |
| Use of prompts and completions | Not available to other customers or OpenAI; not used to train or improve models without permission | DPO and Legal accept the processor terms in the Microsoft Data Protection Addendum (not retrieved here) |
| Statefulness | Models are stateless. Stateful features (Responses API, Assistants threads, stored completions) persist data in the customer resource, encrypted at rest and customer-deletable | Confirm none of these features is enabled; Zava stores chat in its own SQL |
| Location of processing | Standard deployments process in the resource geography, possibly across regions within it. Global and DataZone deployments may process outside it; data at rest stays in the designated geography | Confirm deployment type and that uksouth meets the DPO transfer position |
| Abuse monitoring and retention | Flagged samples of prompts and completions may be stored and human-reviewed by authorised Microsoft staff in the resource geography, unless modified monitoring is approved. Whether abuse monitoring or content logging is active can be confirmed from the resource `ContentLogging` capability setting; not verified here | DPO decides whether to request modified monitoring and records the stored-sample retention exposure |
| Previews | Preview models may use different practices | Confirm the deployed model is generally available |

Transfer position outside the geography stays Unknown until the DPO records it.

## Free text warning and redaction

The UI must show `chat_privacy.WARNING` beside every free-text field. The regulatory
question field does so. The general staff question field now obtains it from
`GET /api/chat/status`, associates it through `aria-describedby`, and blocks
entry while loading or on failure. Other surfaces require separate verification. Messages
are masked for emails, phone numbers, National Insurance numbers, postcodes and
special-category cue words before storage. Memory containing a cue word is
refused, not masked. Masking is best effort and cannot prove absence.

## Memory lifecycle (#161)

Built in `chat_privacy.py` with API endpoints; complete UI/user acceptance is
not established by this record. Memory is off until the user acknowledges the notice (`opt_in`) and
only after the DPO and Legal references exist. Items carry content, source, class, creation date and expiry; the user can list,
edit, delete one or clear all, and withdrawing deletes them. Classes: `working_preference`, `terminology`, `task_context`; each
retention period stays Unknown until `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS` are recorded. Special-category text is refused.
Memory enters a prompt only as non-authoritative, non-evidence preferences, and ids with prefix `CM-` are rejected as evidence
references. An administrator can switch memory off globally or per task (`chat_memory_control`); items stay visible and deletable.

## Decision pack for the DPO and Legal (2026-11-01, Refs #163)

Questions the DPO and Legal must answer before any actual use. Every decision
cell is deliberately blank: this pack records evidence and options, selects
none, and sets no retention period. Options are not legal advice.

| # | Decision | Evidence in this repository | Options to consider | Decision, owner, date, reference |
| --- | --- | --- | --- | --- |
| D1 | Lawful basis for staff chat messages | Purpose in ADR 0004; data map above; UK GDPR snapshot under `../regulatory/data-protection/` | Article 6 bases as the DPO assesses them; staff-facing necessity and alternatives | Not recorded |
| D2 | Lawful basis and condition if resident data is typed | Warning and masking best effort; memory refuses special-category cues | Prohibit by notice and control, or record a resident Article 6 basis, plus an Article 9 condition only where special-category data is involved | Not recorded |
| D3 | Staff notice wording and delivery | `chat_privacy.WARNING`; `CHAT_NOTICE_REF` empty | Approve notice text, placement and acknowledgement record | Not recorded |
| D4 | DPIA outcome | This record; `CHAT_DPIA_REF` empty | Approve, approve with conditions, or require prior consultation | Not recorded |
| D5 | Retention per class (messages, memory, ledger metadata) | Data map; `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS` empty | Set per-class periods after D1 to D4; none is proposed here | Not recorded |
| D6 | Provider terms acceptance, deployment type, abuse monitoring, transfers | Documented position above | Accept, request modified abuse monitoring, restrict to Standard uksouth deployment | Not recorded |
| D7 | Performance and monitoring use | RULE-026 prohibits without a separate decision | Keep prohibited; any change needs its own DPIA update, HR and staff consultation | Not recorded |
| D8 | Rights request intake, identity check, deadlines | `ChatPrivacy.locate/export/erase` | Name the intake owner and response process | Not recorded |

## Open items

* Owner decision (open): which Entra app role is the memory administrator. `MEMORY_ADMIN_ROLES` uses Retrofit Programme Manager as a placeholder. The role is read from the staff register record, not from the caller's session data.
* Retention (expiry) is Unknown until the DPO approves a period. Expired items are filtered on read once an expiry is set.
* Complete memory UI, user acceptance and actual provisioning remain unverified.
* Schema: `chat_memory` gains `item_class`, `source`, `updated_at` through an idempotent ALTER on SQLite and Azure SQL start-up, so a #163-era table is upgraded. `add_memory` requires a known task so the per-task switch always applies.

* DPO and Legal: lawful basis, staff notice, DPIA decision, retention per class, access and break-glass policy (BRD OD-45, OD-46).
* Provider terms are documented above (2026-11-01); DPO and Legal acceptance, deployment type, abuse-monitoring choice and transfer position remain open.
* Rights request intake process and deadlines.
* Verify warning comprehension and other chat/memory surfaces. General staff
  panel warning/failure/keyboard DOM behavior is covered locally, not through
  a human screen-reader or comprehension exercise.
* Confirm audit ledger metadata retention.
* Dependencies #120 and #121 were not assessed here.

## Staff Chat Engineering Boundary (2026-10-27, Refs #157/#162/#159/#164/#163)

This is an implementation update to a draft, not a DPO/Legal decision or a
current-law review. Logical Azure SQL/uksouth locations in the data map remain
architecture targets, not deployment or provider-processing evidence from this
local-only work.

Both general staff HTTP turn routes now use the same cited panel. They send
only bounded own-user question history and currently projected case facts;
neither sends retained memory or prior assistant claims. The existing direct
memory assembly/lifecycle is separately tested, not activated by these routes.
The agents adapter requires server-owned admission before and after a call.
The conversational task has no approved registry/release entry, so the API
denies model dispatch even if synthetic privacy references exist.

One metadata-only `chat.turn` audit event records calls, validated token counts
or Unknown, provider/turn outcome and engineering bounds. It contains no question,
answer, source excerpt, memory or raw provider error. It survives a rejected
completion, including revoked access or deleted thread/case. Linkable user/thread
IDs are still potentially personal data; this is not permission for monitoring,
aggregate performance use, indefinite retention or a new erasure exception.
User deletion continues to leave the existing ledger intact; DPO reconciliation
of ledger, backup and content retention remains necessary.

Engineering caps are one call, zero retries, default 600 output tokens,
16,000 combined system/prompt characters, 4,000 history characters from at most
12 user messages and 1,000 characters for a new question. Oversize uses the
ordinary workflow. These are not approved per-role token/budget/expiry limits,
and character counts do not claim tokenizer equivalence. Prices, full review
effort, provider terms, lawful basis, actual notice approval and retention
remain Unknown. No live model call, personal-data processing approval or new
retention period is delivered.

The local scripted development evaluation still exposes unsupported claims
with valid citation IDs. Poisoning/injection regressions do not establish
serving-model or human effectiveness. Activation remains fail/disabled.
See the [API engineering contract](../../../src/api/README.md#staff-chat-hardening-2026-10-27-157)
and [evaluation reporting](../../../src/agents/README.md#chat-consumption-evidence-2026-10-27-164).

## Regulatory Assistant DPIA Draft for DPO Review (2026-10-16, Refs #217)

Draft only. Juan Manuel Servera is the named exercise DPO, Legal and Compliance
owner, not an invented company appointment. The issue's "DPIA with the DPO
completed before live data use" criterion remains unmet. No DPO review,
consultation, lawful basis, Article 9 condition, notice acceptance, processor
contract or operational approval has been obtained by this work.

### Purpose, necessity and alternatives

The synthetic exercise retrieves dated provisions, compares source versions,
flags deterministic check results and joins a minimum home-fact subset to exact
source quotes. It cannot decide applicability, certify a duty, activate a card,
close a hazard, infer consent, commit money or contact residents. Legal
interpretation and consequential decisions remain with named humans under
[ADR 0005](../../adrs/0005-regulatory-compliance-assistant.md).

The lower-data alternative is deterministic rule cards with provision links.
It remains the shipping baseline unless chat proves added value without weakening
safety/privacy. Current lookup is offline extractive, with no Foundry query,
model tools, retrieved memory or external processor call. This is not evidence
for the safety of a future generative-model path. Actual staff identities,
even with synthetic homes, would still be actual personal-data processing.

### Regulatory data flows and retention alignment

| Class and flow | Necessary content and access | Retention and unresolved decision |
| --- | --- | --- |
| Source store and monitoring candidates | Dated source/provision IDs, excerpts, hashes, versions, gap and review records; candidates stay unverified and separate from approved provisions | Period, immutable snapshot/ledger lifecycle and removal of accidentally imported personal data require DPO/record-owner review |
| Rule-card lifecycle | Versioned interpretation proposal, author, named owner, separate capability and simulated approval/hold/release records | Append-only history is not permission for indefinite retention; period and identity minimisation unknown |
| Checks and checkpoints | Case/home linkage, card version, result, input/evidence hashes, audience, time and decision owner; no raw resident report copied by the check engine | DPO must set check/checkpoint periods, trigger, legal hold and dependency treatment; all remain unknown |
| Alerts and dispositions | Check reference, role audience, clock/safe route, named owner and recorded outcome/evidence note | DPO must set periods and note minimisation; outcomes never close a safety hold |
| Regulatory turns (`reg_chat_turn` equivalent) | Existing `chat_thread` and paired `chat_message` rows; own role/home scope; masked question, complete answer/citations and model marker | Reuses CHAT_RETENTION_REF/DAYS for a simulated review-due report, not deletion. Sender and explicitly referred owner copies have independent ownership; archived threads are included |
| Retrieval and composer | At most four provisions and enumerated category/priority for two hazards, only for permitted roles/purpose; no resident name, address, contact, diagnosis, adjustment, narrative, memory or other home | No provider processing in this path; provision text remains untrusted quoted data, never instructions |
| Chat metadata audit | Actor, role, case/thread/turn IDs, model marker, citation IDs, answer hash, receipt linkage and timestamps; no question/answer/source excerpt or health text | Staff identifiers, linkable hashes and metadata are still potentially personal data. Ledger policy, holds, historical erasure and backup expiry require DPO review |
| Offline usage metadata (engineering delta, 2026-10-27) | Task/schema version, UTC day, outcome and zero model call/token/retry counters in existing chat audit/check/alert records; authenticated own-user/current-role/day summary reads at most 1,000 audit positions, and JSON at most 256 KiB, without messages | Inherits parent records' access and unresolved periods/holds/rights; no separate retention authority. Audit-only coverage can be partial and cannot reconstruct missing events. Staff performance profiling or disciplinary use is not authorized |

`GET /api/chat/regulatory/status` reports the current user's regulatory-thread
review metadata only, with no messages or other owners' records. Missing periods
are `unknown`. A valid `SYNTH-` retention reference remains `simulated`, with
`dpo_reviewed=false` and deletion disabled. The technical 1..36500-day input bound
is not a proposed legal retention period. No numeric default is selected.
Age alone does not authorize erasure, override a hold or satisfy storage limitation.

The 2026-10-27 synthetic engineering delta automatically copies supported
conflict questions and both cited versions to the registered exercise owner's
isolated inbox, with a sender receipt. It reuses the explicit doubt data map,
independent copied-thread ownership and content-free audit. SQL makes the
turn/referral/audit atomic; JSON retains an explicit saved-but-audit-failed
boundary requiring history reload. Automatic referral increases the disclosure
frequency and must be included in DPO necessity, notice, recipient and rights
review before actual processing. It is not consent, a company appointment,
legal interpretation or activation of a rule. No DPO checkbox below changes.

### Risk assessment and proposed controls

These are implementer assessments for review, not accepted residual risks.

| Risk | Potential impact | Engineering control and residual gap | Proposed reviewer |
| --- | --- | --- | --- |
| Cross-role/home disclosure or role restoration from staff cache | High: resident or staff confidentiality loss | Server projection and purpose allowlist; trusted RegulatoryChat capability; direct/generic history guard; authenticated role preserved over wider register role. Actual Entra assignment, revocation and ingress evidence remain unverified | Exercise DPO and technical operator; real owners unverified |
| Sensitive free text or imported source content | High: unnecessary special-category processing | Warning, masking, finite question vocabulary, no narrative/health retrieval, inert exact quotes. Masking cannot detect all sensitive content; source-import review and response handling remain human-owned | Exercise DPO |
| Source/question prompt injection | High: misleading advice or attempted action | Offline composer has no model/tools/write path; quotes never executed; negative tests preserve cards, alerts and holds. No actual-model adversarial assurance is claimed | Exercise Legal/Compliance and technical operator |
| Over-retention, erased evidence or inconsistent referral copies | High: rights failure or lost accountability | Explicit unknown periods and independent copied-thread ownership; no new purge. Existing user deletion, ledger history, holds, backups and source snapshots need a reconciled DPO-approved policy before live data | Exercise DPO and record owners |
| Missing audit after successful turn/referral | High: unverifiable disclosures or review routing | SQL messages, receipt and metadata ledger append share one transaction; injected audit failure rolls everything back. JSON retains a separate-file post-commit audit limitation; Azure SQL execution untested | Technical operator and exercise Compliance |
| Automated consequential decision without reasons | High: unsupported resident outcome | Deterministic safeguard requires named owner, decision source/evidence, time and explicit nonempty reasons before clear. Chat has no decision-write path. Real identity, professional review, contestability and human decision evidence remain unverified | Exercise DPO and relevant human decision owner |

### Rights, incidents and unresolved review questions

Before actual processing, the DPO must reconcile access/export/rectification/
erasure/restriction/objection handling across sender turns, explicit referrals,
check and alert records, immutable source/card events, ledger history, backups
and any future model provider. Do not treat current deletion methods as a complete
rights workflow or invent an erasure exemption. Existing project audit-content
retention direction still needs a lawful, documented human decision; regulatory
chat metadata minimisation is not a determination of that question.

The technical operator should disable the regulatory feature on suspected
disclosure, preserve necessary incident metadata under an approved hold, and
route to the DPO through the existing human process. Do not paste leaked content
into diagnostics, automatically notify residents or invent notification deadlines.
Human incident ownership, escalation and communication procedures need confirmation.

### DPO review and release gate

* [ ] DPO has reviewed this draft, consulted necessary stakeholders and recorded
  purpose, necessity, alternatives and residual-risk decisions.
* [ ] Lawful basis, special-category condition/purpose, notices and actual
  staff/resident scope are approved by the appropriate humans.
* [ ] Per-class periods, triggers, holds, rights, disposal, historical erasure
  and backup/ledger/snapshot alignment are approved and tested.
* [ ] Actual Entra assignments, authenticated ingress and deployed SQL ledger
  controls are verified, with author/approver independence.
* [ ] Provider terms, transfers and minimum query fields are reviewed before any
  regulatory Foundry call; current offline tests cannot substitute.
* [ ] Human review/contestability, named decision owners and recorded reasons
  are exercised and accepted before consequential use.

DPO review date, decision reference and sign-off: not recorded. These checkboxes
are deliberately unchecked. Local test evidence is documented in the
[API acceptance audit](../../../src/api/README.md#regulatory-security-privacy-and-audit-217);
it is not legal advice or a current-law assessment.

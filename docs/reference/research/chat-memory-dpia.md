---
title: Chat and Memory Data Protection Analysis Record
description: Draft DPIA for DPO review covering chat, memory and the synthetic regulatory assistant, with unresolved lawful basis, retention, rights and provider terms
author: AMA programme
ms.date: 2026-10-16
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

* The model provider data handling position is not recorded. The Azure OpenAI terms were not retrieved, so nothing here says what the provider retains or monitors.
* The regulatory panel now displays `WARNING` beside its question field and
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
(owner decision 2026-10-15). Zava stores no prompts. Provider processing terms,
abuse-monitoring retention and any transfer position were not retrieved and are
not verified here.

## Free text warning and redaction

The UI must show `chat_privacy.WARNING` beside every free-text field. The regulatory
question field does so; other surfaces require separate verification. Messages
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

## Open items

* Owner decision (open): which Entra app role is the memory administrator. `MEMORY_ADMIN_ROLES` uses Retrofit Programme Manager as a placeholder. The role is read from the staff register record, not from the caller's session data.
* Retention (expiry) is Unknown until the DPO approves a period. Expired items are filtered on read once an expiry is set.
* Complete memory UI, user acceptance and actual provisioning remain unverified.
* Schema: `chat_memory` gains `item_class`, `source`, `updated_at` through an idempotent ALTER on SQLite and Azure SQL start-up, so a #163-era table is upgraded. `add_memory` requires a known task so the per-task switch always applies.

* DPO and Legal: lawful basis, staff notice, DPIA decision, retention per class, access and break-glass policy (BRD OD-45, OD-46).
* Retrieve and record current Microsoft Azure OpenAI data handling, abuse-monitoring and region terms.
* Rights request intake process and deadlines.
* Model provider data handling is not recorded; retrieval of the terms stays open.
* Verify warnings, redaction and comprehension across all other chat/memory
  surfaces; the regulatory panel alone is covered by this update.
* Confirm audit ledger metadata retention.
* Dependencies #120 and #121 were not assessed here.

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

`GET /api/chat/regulatory/status` reports the current user's regulatory-thread
review metadata only, with no messages or other owners' records. Missing periods
are `unknown`. A valid `SYNTH-` retention reference remains `simulated`, with
`dpo_reviewed=false` and deletion disabled. The technical 1..36500-day input bound
is not a proposed legal retention period. No numeric default is selected.
Age alone does not authorize erasure, override a hold or satisfy storage limitation.

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

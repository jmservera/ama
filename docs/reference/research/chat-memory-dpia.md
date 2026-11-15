---
title: Chat and Memory Data Protection Analysis Record
description: Draft DPIA for DPO review covering chat, memory and the synthetic regulatory assistant, with unresolved lawful basis, retention, rights and provider terms
author: AMA programme
ms.date: 2026-11-15
ms.topic: reference
---

## Status

Draft working record, not an approved DPIA. The owner named Juan Manuel Servera
as the Legal, Compliance and DPO owner on 2026-10-15. No lawful basis, staff
notice or DPIA decision is recorded here, because none has been given. The
demonstrator holds constructed, labelled synthetic data only (ADR 0005). Chat
and memory controls are in `src/core/src/zava_forward/core/chat_privacy.py` and
`src/core/src/zava_forward/core/chat_provider_position.py`.
The subsequent synthetic regulatory lookup is built and requires explicitly
simulated privacy references. Neither a configuration reference nor passing
tests completes this DPIA or authorizes actual staff/resident processing.

Update 2026-11-01: the owner approved chat storage for the synthetic-data demo
only, recorded in [the demo storage approval](./chat-demo-storage-approval-2026-11-01.md)
(30-day demo retention). The blank decision cells below describe the state
before that decision and are not rewritten. Production and real personal data
remain unapproved.

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
| Abuse monitoring and retention | Flagged samples of prompts and completions may be stored in the resource geography and human-reviewed by authorised Microsoft staff, unless modified monitoring is approved. The documented reviewer-location guarantee covers EEA resources only; reviewer location for uksouth is unverified. Whether abuse monitoring or content logging is active can be confirmed from the resource `ContentLogging` capability setting; not verified here | DPO confirms reviewer location for uksouth, decides whether to request modified monitoring and records the stored-sample retention exposure |
| Previews | Preview models may use different practices | Confirm the deployed model is generally available |

Transfer position outside the geography stays Unknown until the DPO records it.

### Runtime residency and data-handling enforcement (2026-11-15, Refs #163)

`chat_provider_position` (`evaluate_provider_position` and `require_provider_position`)
records and enforces the technical model provider and region contract across
`ChatPrivacy`, `regulatory_privacy.readiness_report`, `regulatory_privacy.build_foundry_query`
and `GET /api/chat/status` without substituting for human DPO and Legal acceptance:

| Posture | Regions | Deployment SKUs | Runtime rule |
| --- | --- | --- | --- |
| Primary domestic residency (`uk_south`) | `uksouth` | `Standard` only | Permitted default; `uksouth` with `DataZoneStandard` fails closed (`unapproved_deployment_residency`) because the UK is outside Microsoft's EU Data Zone |
| Bounded EU data-zone residency (`eu_data_zone`) | `swedencentral`, `westeurope`, `northeurope`, `francecentral`, `germanywestcentral`, `italynorth`, `polandcentral`, `spaincentral` | `Standard`, `DataZoneStandard` | Classified as cross-border transfer outside the UK; fails closed (`cross_border_transfer_unapproved`) unless `CHAT_TRANSFER_REF` holds a recorded governance reference |
| Prohibited regions and global routing (`unapproved`) | Any non-UK, non-EEA region (for example `eastus`) | `GlobalStandard`, `GlobalBatch`, `GlobalProvisionedManaged`, or blank/unknown SKU | Always fails closed (`unapproved_region`, `unapproved_deployment_residency`) |

Additional enforced controls:

* Zero model training: customer prompts, completions and opt-in memory are never
  permitted for foundation-model training or improvement. Any enabled or
  unrecognised `CHAT_PROVIDER_TRAINING` setting fails closed (`provider_training_prohibited`).
* Content-filtering versus abuse-monitoring disclosure: `CONTENT_FILTERING_DISCLOSURE`
  records synchronous stateless Azure AI Content Safety harm filtering (`stores_prompts = false`,
  `trains_models = false`), separate from `ABUSE_MONITORING_DISCLOSURE` which
  records platform-default up-to-30-day encrypted flagged-sample storage and
  authorised Microsoft human review (`CHAT_ABUSE_MONITORING_MODIFIED_REF` records
  `mode = "modified_recorded_unverified"` with `modified_abuse_monitoring_verified = false`,
  retaining conservative `default_sample_retention_days = 30` and
  `human_review_possible = true` defaults until DPO and Legal verify Microsoft's
  subscription setting). Vendor documentation guarantees EEA reviewer location
  for EEA resources only, so `uksouth` reviewer residency remains
  `uk_reviewer_residency_verified = false`.
* Cross-border transfer gate, deployment attestation and actual-mode guard:
  explicit `CHAT_CROSS_BORDER_TRANSFER=true` or any EU data-zone configuration
  requires a valid `CHAT_TRANSFER_REF`. Because `infra/main.bicep` currently
  defaults `chatModelSku` to `GlobalStandard` and `infra/modules/containerapps.bicep`
  does not inject `CHAT_PROVIDER_REGION` or `CHAT_DEPLOYMENT_TYPE`,
  `constructed` synthetic evaluations fall back to `uksouth` / `Standard` with
  `deployment_attested = false` (`true` only when both settings are explicitly
  supplied and approved), whereas `ZF_DATA_PROCESSING=actual` requires explicit
  `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` attestation
  (`unattested_region_in_actual_mode`, `unattested_deployment_in_actual_mode`).
  Bare boolean/placeholder tokens are rejected in every mode, synthetic or demo
  reference strings (`SYNTH-*`, `SYN-*`, `SYNTHETIC-*`, demo approval files, or
  this draft file) fail closed when `ZF_DATA_PROCESSING=actual`, and
  `ZF_DATA_PROCESSING=actual` refuses chat, memory and provider readiness
  (`actual_mode_unapproved = true` and `actual_mode_dpo_legal_unapproved`) while
  repository-recorded `DPO_LEGAL_APPROVED` is `False`, even if non-synthetic
  environment reference strings are supplied.
* Pre-approval retention gate: `ChatPrivacy.decision()["retention_days"]` stays
  `None` (`Unknown`) until `DPO_LEGAL_APPROVED` (in `actual` mode), `CHAT_DPIA_REF`,
  `CHAT_LAWFUL_BASIS_REF`, `CHAT_NOTICE_REF` and `evaluate_provider_position`
  all pass alongside `CHAT_RETENTION_REF` and ASCII `CHAT_RETENTION_DAYS` in
  `1..36500`. Every payload carries `dpo_legal_approved = false` and
  `documented_terms.dpo_accepted = false`.

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

## Proposed administrator and break-glass policy (BRD OD-46, not decided)

Update 2026-11-03: the owner approved option A for the synthetic-data demo only, as a disclaimer in place of the DPO and
Legal decision. It is recorded as unreviewed by the DPO and Legal; see
[the demo-only record](./chat-demo-breakglass-disclaimer-2026-11-03.md). The DPO and Legal decision remains open for any
real-data or production use.

Status of the original proposal: for the owner and DPO to accept, amend or reject. Nothing here is approved, and no control reads it as
approved. Retrieved 2026-11-01 from the implemented behaviour in `chat_isolation.py`.

| Option | Administrator can see | Evidence needed | Assessment |
| --- | --- | --- | --- |
| A. Metadata only (recommended starting point) | Thread, message and memory counts for a named user (a count snapshot, no ids), with an advisory expiry timestamp of 1 to 60 minutes | Written purpose of 10 or more characters, named role in `CHAT_BREAKGLASS_ROLES`, policy reference in `CHAT_BREAKGLASS_REF`; granted and refused attempts audited with actor, target and purpose | Implemented as counts only. The expiry is returned and audited but no expiring access grant is created or enforced. Content stays unavailable. |
| B. Content access under dual approval | Message text for a named thread | Option A plus a second approver, DPO notice and a user notification rule | Not implemented. Needs a DPO and Legal decision first. |
| C. No break-glass | Nothing | None | Simplest, but leaves no route to investigate misuse. |

Open questions for the decision: which Entra app role is the administrator, whether affected users are told after access,
the audit retention period, and whether content access (option B) is ever permitted. Until a policy reference is recorded
the endpoint refuses every request and audits the refusal with its stated purpose.
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

Since 2026-11-01 (Refs #164) the panel withholds an answer whose status words
(for example "secured", "approved") or numbers appear in no cited source, so the
scripted unsupported-claim scenario passes. The check is lexical over listed status words and complete numeric tokens;
an unlisted paraphrase (for example "Funding is financed.") can bypass it, so it is not claim-level semantic grounding. Poisoning and
injection regressions do not establish serving-model or human effectiveness.
Activation remains disabled with outcome insufficient (thresholds, reviewer,
held-out, actual-model and human evidence missing).
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

## Status record 2026-11-04 (Refs #163)

Rechecked merged work (#281, #503, #649, #727, #735, #745, #844, #874, #919).
Acceptance criteria 1, 3, 4 and 6 stay evidenced by those PRs. Criteria 2 and 5
stay unmet: no lawful basis, staff notice, DPIA decision, retention approval or
provider terms acceptance is recorded, because the DPO and Legal owner has not
given them. Decisions D1 to D8 above remain "Not recorded". No retention period
is set and nothing in this update approves one. The staff notice and warning
UI are not changed here. Nothing is ticked or closed.

### Issue 217 delivery status (2026-11-04, Refs #217)

Merged PRs 353, 642, 695, 839, 884, 964, 1021 and 506 deliver the offline
audit log, injection and cross-role tests, the live-data readiness gate, the
purpose-scoped Foundry field guard, the Art 22A to 22C decision record builder
and the closed metering schema with read-path validation. No code criterion is
unmet. Criteria 1, 2, 4, 7 and the metering conjunction stay unmet because they
need a named person:

| Criterion | Needed from | Evidence still missing |
| --- | --- | --- |
| DPIA completed with the DPO | DPO | Signed DPIA and live-data permission |
| Retention periods for chat, check and usage records | DPO | Reviewed periods, disposal, holds and backups |
| Foundry minimisation on live calls | DPO, platform owner | Live provider wiring evidence |
| Separate Entra roles | Entra administrator | Tenant role assignments and revocation test |
| Art 22A to 22C named human and reasons | Legal, DPO | Legal assessment and contestability route |
| Metering follows DPIA scope | DPO | DPIA scope sign-off |

This record ticks nothing and implies no approval.

## Enforced model provider and region position 2026-11-15 (Refs #163)

`src/core/src/zava_forward/core/chat_provider_position.py` now records and
enforces the technical model provider data-handling and region position contract
(Issue #163 criterion 5) across `chat_privacy.py`, `regulatory_privacy.py` and
`GET /api/chat/status`: primary `uksouth` `Standard` residency, bounded EU
data-zone allowlist gated on `CHAT_TRANSFER_REF`, unconditional rejection of
`GlobalStandard` and third-country regions, zero-training enforcement, separate
content-filtering and abuse-monitoring disclosures, and pre-approval retention
blocking. Issue #163 criterion 2 remains unmet and human-gated: decisions D1 to
D8 above remain "Not recorded", `ZF_DATA_PROCESSING=actual` remains refused while
`DPO_LEGAL_APPROVED` is `False`, no retention period is approved for real or
production personal data, and passing unit tests do not constitute DPO or Legal
sign-off.

## Whole-System Processing, Derivative Dispatch and Rights-Request Controls (2026-11-15, Refs #121)

Deterministic local engineering update in `src/core/src/zava_forward/core/data_protection.py`
and `src/core/src/zava_forward/core/sqlstore.py` extending the whole-system RAI
processing inventory, task-necessity manifest, intact-attachment dispatch gate
and persisted rights-request workflow. Decisions `D1` to `D8` and the unchecked
DPO and Legal release gates above remain unapproved (`dpo_reviewed=False`).

* Subject-population and residency separation: `DATA_CLASSES` separates
  `fixture_resident` (`constructed`, `constructed_resident_fixture`) from nine
  `actual` classes (`staff_identity`, `tenant_identity`, `review_record`,
  `future_real_resident`, `raw_document`, `prompt_output`, `audit_ledger`,
  `telemetry`, `provider_retained_copy`) across `current_staff_identity`,
  `current_tenant_identity`, `current_review_record` and `future_real_resident`.
  `register_report(env)` surfaces `whole_system_coverage` across inputs, raw
  document/image bytes, prompts/outputs/citations, reviewer identity, audit,
  telemetry/tokens, provider processing and provider retained copies, together
  with `hosting_region_vs_inference_residency`
  (`uk_hosting_does_not_prove_uk_inference_residency: True`, recording that UK
  South application hosting does not establish UK model-inference, abuse-review
  or provider retained-copy residency).
* Whole-system task necessity (`TASKS` and `validate_task_payload`): every
  declared AI task (`rule_lookup`, `check_explain`, `alert_triage`, `agent_chat`,
  `look_at_attachment`, `intake_summary`, `case_brief`, `read_document`,
  `funding_draft`, `priority`) records `purpose`, `audience`,
  `permitted_fields` (`(type, max_length)`), `prohibited` and `necessity`.
  `validate_task_payload` and `model_dispatch` enforce
  `user_permission_establishes_necessity=False`: user permission alone never
  authorizes an undeclared task, an empty payload, an out-of-bounds field or a
  special-category field.
* Intact document and image dispatch boundary (`dispatch_attachment_to_model`,
  `model_dispatch`, `document_model_hold`): upload, storage or download
  permission (`storage_permission_granted=True`) never authorizes sending intact
  bytes to an external model (`storage_approves_ai_dispatch=False`). Model
  dispatch requires non-synthetic class references plus either a human-reviewed
  `reviewed_redacted` derivative (`redaction_reviewer_id` and
  `redaction_review_id`) or a non-synthetic scoped necessity approval
  (`scoped_necessity_ref` or validated `necessity_exception`); all failures
  deny model dispatch and preserve `manual_path`.
* Persisted rights-request ledger (`RightsRequestLedger`,
  `record_rights_request`, `log_rights_action`, `answer_rights_request`,
  `rights_status`): persists statutory requests (`access`, `rectification`,
  `erasure`, `restriction`, `objection`, `portability`) in `Store`, `SqlStore`
  (`meta` document `"rights_requests"`) or atomic JSON files with timezone-aware
  receipt timestamps, one-calendar-month statutory deadlines, `locate`/`export`/`erase`
  action logs and `subject_key`-free metadata audit entries. Local deletion
  (`local_deleted=True`) is never represented as external model-provider
  erasure (`provider_erasure_confirmed=False`; attempts to record confirmed
  provider erasure from local state raise `ValueError`).
* Open human gates (`Refs #121`): named DPO confirmation of per-class lawful
  basis and Article 17(3) audit retention, Legal sign-off of retention periods
  and processor/transfer terms (`DH-006`), and ratified live intake procedures
  remain open before any real personal data processing.

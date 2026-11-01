---
title: Zava Forward Workbench Content Standard, Glossary and Copy Audit
description: Plain-language content standard, status and next-action glossary, blocked-message pattern, AI label wording and the copy audit of the core flow (issue #153)
ms.date: 2026-10-27
ms.topic: reference
---

## Scope and evidence

Implements issue #153 under epic #149 (PRD SA-003 and SA-004, BRD RULE-022).
Sources: `src/api/src/zava_forward/api/web/*.js`, `src/core/src/zava_forward/core/store.py`,
`src/core/src/zava_forward/core/signoffs.py` and the
[design system foundations](./design-system.md). This is a content standard for
a synthetic-data demonstrator. It has not been tested with real staff or
residents, and no resident-facing wording is approved for use (see Human
review).

## Content standard

* Write for a housing officer, resident or contractor who has not seen the
  system before. Short sentences, active voice, everyday words.
* Say what happened, why, who owns it and what to do next. Never leave a person
  at a dead end.
* Use one name for one thing. The glossary below is the source of truth.
* Internal terms are not used in the core flow: gate, hold, provenance, trace,
  envelope, snapshot. Use the plain alternative in the glossary.
* Name the actor. "A person decides", not "it is decided".
* Never imply that an AI output, or a person's review of a draft, is an
  approval, consent or safety decision.
* Plain ASCII punctuation, no em dashes, no jargon abbreviations without
  explanation.

## Blocked and error messages

Every blocked or refused action states three things in one message:

| Part | Rule | Example |
| --- | --- | --- |
| Reason | What is missing or wrong, in plain words | Funding has not been confirmed. |
| Owner | A named person or role, never "unassigned" | Owner: Sam Officer. |
| Next action | One verb-led sentence | Next action: check the funding and record it. |

The case "Final checks" list and the evidence, technical sign-off and funding
approval refusals use this pattern (`gate_reasons`, `technical_gate` and the
funding approval check). Other validation errors state the reason and the fix
in one sentence, for example "Choose which sign-off this is."

## AI suggestion wording (SA-004)

* Unreviewed AI output is labelled exactly "AI suggestion, not approved". The
  server labels (briefing, drafts, priority suggestion, funding draft) and the
  assistant proposal card use this text.
* A template draft is labelled "Template draft, not approved". A rules-based
  summary is labelled "Summary by rules".
* After a person reviews, the text says the draft was accepted, edited or
  rejected as a draft, and that this "is not an approval, consent or safety
  decision". The words "human-approved" and "AI-drafted" are retired.
* Requesting AI help stays optional; a person can choose rules and templates.

## Glossary

| Use | Do not use | Meaning |
| --- | --- | --- |
| Final checks | Gate | What must be in place before a case moves on |
| Cannot move on yet | Gate failed, blocked by gate | The case is waiting on a listed item |
| Pause payment / Payment paused | Hold, on hold | Finance has stopped paying an invoice for now |
| Restart payment | Release hold | Finance lets the invoice be paid again |
| Sources | Provenance, citations (to staff) | Where a statement came from |
| Changes to this suggestion | Proposal history, trace | The record of what changed and who changed it |
| AI suggestion, not approved | AI-drafted, human-approved | Output from AI that no person has approved |
| Not reviewed by a person yet | Pending, unreviewed | No person has looked at it |
| Accepted / Edited / Rejected as a draft | Approved | A person's view of a draft, not an approval decision |
| Waiting on | Blocked by (internal), assigned to | The person or team who must act next |
| Safety issue open | Hazard unresolved | Reported safety concern; affected retrofit work needs an evidenced independent restart decision, not hazard-service closure |
| Stopped retrofit work / Restart decision | Retrofit hold / Release hold | The restriction covers the linked home's retrofit work only; the hazard service still owns its case |
| Resident has not confirmed | Consent pending | The resident has not said they want the works |
| Ready to book the installation | Advance | The next step for a case at final checks |
| Check recorded at / Recorded as of / Recorded view | Snapshot | When a check or view was recorded; not proof that its evidence is current |
| Historical records | Historical snapshots | Restored information from an earlier lookup; ask again for a fresh lookup |
| Suggestion details | Envelope | Technical information about a suggestion, not an approval or decision |

## Copy audit of the core flow

Scope: staff case list, case page, final checks, drafts and AI notes, priority
suggestion, assistant proposal card, finance panels and import summary.
Method: search the named web files for the banned terms gate, hold, provenance,
trace, snapshot and envelope, then read each match; review of server-supplied messages in `store.py`
and `signoffs.py`. Automated by `src/api/tests/test_content_standard.py`.

| Finding | Location | Change |
| --- | --- | --- |
| "Human-approved" label on AI output | Priority suggestion, funding draft | Now "AI suggestion, not approved" |
| "AI-drafted" label with no approval state | Briefing, drafts | Now "AI suggestion, not approved" |
| Reviewed draft shown only as "Accepted" | AI notes | Adds "not an approval, consent or safety decision" |
| "Provenance" in proposal text | Assistant proposal card | "Sources show where a statement came from" |
| "Proposal history" | Assistant proposal card | "Changes to this suggestion" |
| "hold" | Finance panels, import summary | "Pause payment", "already have a record for" |
| Final checks and refusals without owner or next action | Store and sign-off reasons | Reason, owner and next action in each |

Remaining by design, not shown as wording to a person: the internal
identifiers `gate`, `provenance` and `hold` in code and API fields, and the
stored finance decision value "Keep on hold".

### Chat and alert-panel audit extension (2026-10-18, #153)

The existing lexical regression now names seven files: `app.js`,
`assistants.js`, `panels.js`, `ops.js`, `chat.js`, `index.html` and
`welcome.html`. It includes singular/plural snapshot and envelope as well as
the previously guarded vocabulary. This is a conservative source-level guard,
not a JavaScript/HTML visibility parser or a universal audit of dynamic messages.

| Finding | Application-owned location | Plain wording |
| --- | --- | --- |
| "decide a hold" | Building Safety role guidance in chat and alerts | Only an authorised human can make a restart decision for stopped retrofit work |
| "release a hold" | Alert-panel authority disclaimer | This panel cannot acknowledge, decide compliance or restart stopped retrofit work |
| "Check snapshot" | Alert check date label | Check recorded at |
| "historical snapshots" | Restored cited-lookup status | Historical records; ask again for a fresh lookup |
| "snapshot" time labels | Existing case task summary, safety clock and task sources | Recorded as of / Safety clock in this recorded view |

The safety alternatives come from the existing stopped-work/restart glossary.
They do not close a hazard-service case, establish safety, give the panel new
authority or permit a restart without the existing human decision process.
The exact "AI suggestion, not approved" label, proposal-only operation,
independent human emergency/hazard route and unknown/unverified source warnings
are retained.

Scope excludes user/model-authored content, recorded facts, source quotations,
source titles, identifiers, API fields and raw technical JSON shown under
suggestion details. The narrow lexical exceptions retain the existing finance
stored value, code field references and the technical JSON `envelope` key;
these are not permission to use internal terms in adjacent interface labels.
In particular, quoted evidence may contain all six prohibited terms and must
remain verbatim. The local synthetic browser regression in
`src/api/checks/regulatory_ux_check.py` checks that exact quotation before and
after history restoration, separately from application-owned labels.

This extension is partial engineering coverage, not universal core-flow or
reason/owner/next-action coverage for every error. The local browser flow
exercises changed wording and safety/unknown/AI boundaries, not actual staff
or resident comprehension, operational approval, full WCAG conformance or
named human acceptance of resident-facing wording.

### Dated surface and message audit (2026-10-27, #153/#154)

This source inspection extends, not replaces, the historical audit above.
The inventory covers the existing core flow and supporting web assets in
`src/api/src/zava_forward/api/web/`. It is not exhaustive enumeration of every
dynamic message, a reading-age result, comprehension validation or a full
web/accessibility audit. The [resident task designs](./customer-journeys/residents.md#resident-and-representative-task-designs-2026-10-27-154)
are candidate copy, not approved communications.

| Surface and source | Inspected content and states | Outcome and limits |
| --- | --- | --- |
| `app.js`, `index.html`, `welcome.html`: entry, account, work lists, case, overview | Signed-out/session-ended, loading/error/empty queues, recorded task owner/reason/action, safety text, manual path | Core statuses use words; safety remains independent. Long task/source explanations need comprehension testing. Welcome is a research demonstrator, not a resident service |
| `app.js`: resident drafts, document reading, briefing, priority and funding | Exact AI label, optional templates/rules, unreviewed and reviewed drafts, failed requests | Draft-only heading and named-review/no-send explanation clarified. Priority review status and funding approval terminology need a separate end-to-end review; not globally certified |
| `assistants.js`, `chat.js`: proposal, source check, review, chat and alerts | Proposed/ready/stale/failed/reviewed, exact AI warning, unknown source coverage, historical lookup | "Requested using" replaces technical "Invocation"; proposal review now explicitly excludes approval, consent and safety decisions. Quotes, source titles and user/model text remain verbatim |
| `panels.js`: resident measure/representative, updates and complaints | Not recorded/paused/withdrawn decisions, scoped source/date checks, update owner/due/basis, separate response and remedy | Review-date label now says authority is unavailable from that date. Complaint response closure never promises remedy completion or live dispatch |
| `ops.js`: quality, appointments and capacity | Independent acceptance/defect/reinspection/handover, offer and three separate confirmations, provider failure | Offer, consent and confirmation remain separate. Existing instructions are staff-facing, not resident-ready text; no live contact |
| `panels.js`: finance, grants, technical and stock; `app.js`: documents/import/building | Payment pause, grant stages, sign-offs, competing sources, missing files, CSV errors, shared-work restrictions | "Keep on hold" is still a visible stored finance option/disposition; lexical allowance does not mean plain-language compliance. No data migration performed |
| `timecapture.js`, `role-screens.js`: supporting staff tasks | Enabling refusal, read-only evidence, invalid page/role/empty state | Ordinary "hold the same role" changed to "have the same role". Time-capture added to the lexical guard; specialist server-projected content remains manually inspected only |
| `law.js`, `law.html`: supporting reference viewer | Sources/gaps, source status/date/caveats, failed requests, no-AI/no-legal-advice warning | "Sources held", provision metadata and raw failures remain technical supporting copy. They are outside the lexical guard, not an accepted resident explanation |

Identifiers/API fields, stored decisions, quoted evidence and application-owned
labels are different evidence classes. Do not blanket-replace or redact source
quotations to make the lexical test pass. The guard now covers eight named
files; `role-screens.js`, `law.js` and `law.html` are inventoried above, not
silently treated as lexically compliant.

#### Open message findings and accountable follow-up

These are source-inspection findings, not claims about every possible response.
Follow-up roles below own design remediation, not invented live case assignments.

| Finding and source locator | Missing requirement | Follow-up owner and next action |
| --- | --- | --- |
| `app.js`, `api()`: "Something went wrong." and forwarded `data.error`; case refresh forwards `e.message` | Unknown cause, no reliable owner or next action on every error | API/content maintainer: inventory typed error outcomes and supply a truthful recovery/owner contract, including uncertain writes; do not advise blind retry |
| `store.py`, `ranking_snapshot()`: manager-only "ranking snapshot" error; finance option in `panels.js` | Dynamic/internal wording remains visible despite lexical tests | Content and Finance owners: review display-only mappings separately from stored values; retain exact audit history |
| `signoffs.py`, `mutate()`: "Record the design first." and independent-person refusals | Some messages give a fix but no explicit owner; not all reasons follow three-part pattern | Technical workflow/content owner: map each refusal to the actual responsible role and next permitted action |
| `chat.js`, `regulatoryAlertsPanel()`: unknown/"Unassigned" decision owner; `law.js`, `fail()` forwards raw message | Missing owner is explicit but unresolved; recovery is not always actionable | Regulatory-service/content owner: resolve actual appointment or keep Unknown with an owned investigation; no fabricated approver |
| `app.js`, `priorityPanel()` reviewed status; `fundingPanel()` human approval vs AI draft review | Adjacent explanations do not prove every reviewed output disclaims decision authority | AI-task and Finance/content owners: exercise reviewed/failed/stale states and keep draft review distinct from controlled financial approval |

Generic error recovery must distinguish a failed read from an uncertain write:
check recorded history before repeating a change. The existing resident-update
form already uses this distinction. Adding a generic role name to every raw
error would not establish real accountability.

#### Core-flow copy and error contract slice (2026-11-01, #153)

* The lexical guard now names eleven files, adding `role-screens.js`, `law.js` and `law.html`.
* `role-screens.js`: "phase gate" and "gate" became "phase check" in the asset-owner and programme panels.
* `app.js` `api()`: the unknown-error fallback now states the reason (cause not known), owner (application support) and next action (check recorded history before repeating a change, then contact support).
* `law.js` failure status and the manager-only ranking error in `store.py` now name an owner and next action; the ranking error no longer says "snapshot".
* Still open: typed server errors, `signoffs.py` refusals, the stored "Keep on hold" finance value, actual named review of resident wording and comprehension/accessibility testing.

#### Issue #153 acceptance evidence

| Criterion | Evidence and disposition |
| --- | --- |
| Standard and glossary | Exists in this document; previously checked issue criterion preserved |
| Core-flow audit removes internal terms | Expanded inventory delivered; partial, because dynamic messages and visible stored finance wording above remain |
| Errors/blocked steps give reason, owner, next action | Final-check reasons and the generic fallback tested; partial, residuals above prevent universal acceptance |
| Exact AI label and reviewed-draft authority | Exact label retained; draft/proposal disclaimer strengthened. Partial, not a global certification of every reviewed/error state |
| Named human resident wording review before use | Reviewer appointed below; actual review of exact copy Not run. No use authorized |

## Human review

Resident-facing wording defaults to named per-message review. The owner
[appointed Juan Manuel Servera (@jmservera)](https://github.com/jmservera/ama/issues/153)
on 2026-10-15 in the issue comments. This corrects the earlier "no reviewer"
statement; appointment does not establish completed review. No completed named
human review of this candidate wording is evidenced and no live text or sending
is approved. Review records need name,
role, date, exact text and outcome. Unreviewed drafts remain "not approved"
and synthetic only.

Prospective owner-selected proposal (2026-10-23, #441): only a separately
activated versioned evaluated routine policy under
[BRD RULE-028/FR-044/AC-084](../../../brds/agentic-retrofit-programme-brd.md#optional-resident-portal-and-communication-agent-draft-amendment)
may replace individual review for bounded acknowledgements, reminders and
grounded status/process replies. It must state task/channel/audience/content
limits, expiry and actual policy approver/version, disposition and delivery.
Never say "reviewed by a person" when only policy approval occurred.
Consequential, sensitive, uncertain, safety, consent, contractual and financial
content always needs named review. No exception activates in this document;
staff drafts, memory and regulatory no-send boundaries are unchanged.

### Proposed resident status and receipt wording

| State | Candidate plain wording | Must not imply |
| --- | --- | --- |
| Durable file receipt | Received, waiting for checks | Verified, accepted or published |
| Scan clean | File checks complete, waiting for a person | Accepted case evidence or resident-visible publication |
| Reviewed/accepted document | Reviewed as case evidence, publication separate | Approval of works or consent |
| Appointment response | Your response was recorded; waiting for confirmation | Confirmed booking or agreement to works |
| Future routine policy disposition | Sent automatically under the recorded routine policy; AI involvement and source/as-of visible | Per-message human review or company approval |
| Unknown/stale/conflicting answer | We cannot confirm this. Here is how to reach a person | Fabricated reassurance or inferred decision |

These are proposed synthetic-copy patterns, not tested resident wording.
Show reference, owner/next update and assisted route where appropriate.
Urgent help remains visible independently of model success. Source/as-of,
received/reviewed/accepted/published/confirmed states must stay distinct.

## Open items

* Appointed reviewer Juan Manuel Servera to record name, role, date, exact
  wording/version and outcome before resident use; owner to confirm process.
* The finance decision value "Keep on hold" is stored data; renaming it needs
  a migration decision.
* Reading-age targets, translation and accessible-format wording are not set.
* No user testing of the wording has been done; results must be recorded as
  test results under epic #149, not asserted.

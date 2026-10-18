---
title: Zava Forward Workbench Content Standard, Glossary and Copy Audit
description: Plain-language content standard, status and next-action glossary, blocked-message pattern, AI label wording and the copy audit of the core flow (issue #153)
ms.date: 2026-10-18
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

## Human review

* Resident-facing wording (the message and letter drafts and any text a
  resident reads) must be reviewed by a named human before any use. No
  reviewer is named and no resident-facing text is approved.
* The review record needs the reviewer's name and role, date, the exact text
  and the outcome. Until it exists, drafts stay "not approved" and are for
  synthetic-data demonstration only.

## Open items

* Owner to name the reviewer for resident-facing wording and confirm the
  review process.
* The finance decision value "Keep on hold" is stored data; renaming it needs
  a migration decision.
* Reading-age targets, translation and accessible-format wording are not set.
* No user testing of the wording has been done; results must be recorded as
  test results under epic #149, not asserted.

---
title: Employee Case Workspace Redesign (Journey Stepper, Tabs, AI Visibility)
description: Implementable UX design for the single-home case view at #/case/<id> - journey stepper, summary strip, tabbed sections, AI review pattern, states, acceptance criteria and test plan, with the 2026-11-20 update for ten tabs, the equal-height strip, the quality decision and handover cards and the Home sensors tab
ms.date: 2026-11-20
ms.topic: reference
---

## Scope and evidence status

Design for the employee case route `#/case/<id>` (`caseView` in
`src/api/src/zava_forward/api/web/app.js`, with `ops.js`, `panels.js`,
`assistants.js`, `chat.js`). Requested by the project owner. It follows the
[design system](./design-system.md) (Fluent 2 tokens, native semantics, no
framework swap), the [WCAG 2.2 AA baseline](./wcag-conformance-baseline.md) and
the [content standard](./content-standard.md).

Evidence labels: the problem (one long page) is observed in code. That staff
find the new layout easier is an assumption (hypothesis) until tested with real
case officers. Nothing here is a conformance claim. Slide 4 of
`docs/capstone/deck/zava-forward-cowork-v2-draft.pptx` supplies the six step
names, five blockers and the principle "A conflicting record should stop one
approval, not all useful work".

Job (assumed): when I open a home, I want to see where it is, who owns the next
move and what is stopping it, so I can act or hand it on without scrolling.

Update (2026-11-20): the case screen changed after a staff workbench UX review.
[Staff workbench UX update (2026-11-20)](#staff-workbench-ux-update-2026-11-20)
records ten tabs, an equal-height journey strip, the closed-case summary, the
quality decision and handover cards, the Home sensors tab and the scrolling tab
row. Where it differs from earlier text on this page, it governs, and the
earlier text carries a short pointer.

## Current page (observed)

`caseView` renders about 25 cards in one column: cost allocation, header,
status, recorded task context (`workSteps`), safety, regulatory alerts, contact
and stage, return, handoff, quality, stock, log a call, who could take this on,
final checks, write to the resident, documents, funding, assistants, chat,
finance, grant, technical, resident decisions, challenge, history. AI output
sits in four places (`aiNotes`, `assistantProposal`, chat, drafts) with
different density.

## Page layout

Order inside `main` (one `h1`, then landmarks):

1. Header links: Back to the list, Versioned home case and the building link, as separate list items (changed 2026-11-20; it read "Back link and building link (unchanged)").
2. `h1` resident name, "Safety issue open" flag if any hazard is unreleased, reference.
3. Summary strip (`section`, `aria-label="Case summary"`, always visible, not sticky).
4. Journey stepper (`nav`, `aria-label="Retrofit journey"`).
5. Tab list and one visible tab panel.
6. `msg` live region (unchanged) directly below the tab panel.

Safety stays prominent: an open hazard shows a `.blocked` block (SA-003) above
the stepper with the existing `safetyPanel` actions, on every tab.

### Summary strip

A `dl` of six items in a grid (3 columns wide, 2 at 900px, 1 at 600px).
Each value is text; glyph plus words for status.

| Item | Source (existing field) | Empty or unknown text |
| --- | --- | --- |
| Status | `c.status` in `.status-line` (danger when `openHaz.length`, else ok/wait glyph) | "Status not recorded" |
| Current step | Derived step name (see stepper) plus `c.stage` and `c.days_in_stage` days | "Step unknown" |
| Next action | `c.work.next_action`, as one verb-led sentence with a button that opens the tab holding the action | "Ask <owner> to record the next action." (already server text) |
| Owner | `c.owner`, `c.owner_role`; if `c.work.handoff` pending, add "Offered to <proposed_receiver>, not yet confirmed" | "Owner: Unknown" (never "unassigned") |
| Blockers | Count of `c.work.blockers` plus first reason, owner and next action; link "See all blockers" opens the Blockers tab | "No recorded blockers." |
| AI | Count of proposals with approval "Not reviewed" and assistance state (see AI pattern) | "No AI suggestions waiting" or "AI assistance unavailable. Work continues manually." |

Blocker text keeps the content-standard trio: reason, owner, next action.
`work.overdue` count is appended to the Blockers item as "N overdue tasks". A
closed case reads differently (changed 2026-11-20, see the update below).

## Journey stepper

Six steps, fixed order from the slide: Survey, Assessment, Funding, Resident
agreement, Contractor, Quality and handover.

### Markup

```html
<nav aria-label="Retrofit journey">
  <ol class="stepper">
    <li class="step done">
      <a href="#/case/ID?tab=survey">
        <span class="step-glyph" aria-hidden="true">&#10003;</span>
        <span class="step-name">Survey</span>
        <span class="step-state">Done</span>
      </a>
    </li>
    <li class="step current" aria-current="step"> ... <span class="step-state">Current</span></li>
    <li class="step blocked"> ... <span class="step-state">Blocked: funding mismatch</span></li>
    <li class="step upcoming"> ... <span class="step-state">Not started</span></li>
  </ol>
</nav>
```

* Native `ol`, so order and "item N of 6" are announced. `aria-current="step"` only on the current step; none when the case is closed.
* State is visible text, not only colour or glyph. Glyphs are `aria-hidden`; the state word is not.
* Each step links to the tab that holds its work (table below). Links are real anchors, so Tab, Enter and middle-click work. No roving tabindex, no custom keys.
* A step can be both current and blocked: keep `aria-current="step"` and show "Current, blocked: reason".
* Fluent mapping: `--colorBrandBackground` fill for current, `--ok` for done with tick, `--warn` for blocked with no-entry glyph, `--line` outline for upcoming (dashed outline so upcoming differs from done without colour). Use existing tokens only; no new colours.
* Layout: six columns at 1200px and wider, three columns by two rows from 900 to 1199px (changed 2026-11-20; it was one row of six at 900px and wider) and a vertical list below 900px (same `ol`). Connector lines are decorative CSS. Under `prefers-reduced-motion` no transitions (`--motion` is already 0s).

### State derivation (client, from existing `caseView` data)

Stage-to-step map (all 25 `STAGE_ORDER` values; stored once as a constant, with
a unit test asserting every stage is mapped):

| Step | `c.stage` values |
| --- | --- |
| Survey | Home identified, Checking lease, Rescheduled, Contacting resident, Contact paused, Survey being booked, Survey booked, Survey write-up |
| Assessment | Design starting, Design in progress, Design awaiting approval, Design being corrected, Waiting on other works |
| Resident agreement | Waiting for resident decision, Resident paused works |
| Funding | Funding check, Final checks before ordering |
| Contractor | Waiting for block programme, With contractor, Install booked, Works under way |
| Quality and handover | Handover to arrange, Quality check, Closing down, Aftercare issue |

Rules, evaluated in this order:

1. Current = step of `c.stage`. If `c.closed`, all steps Done and no current.
2. Blocked = a step with a matching entry in `c.work.blockers`. Mapping by `step` text: "Final checks: funding" to Funding; "Final checks: resident decision" to Resident agreement; "Final checks: technical review" to Assessment; "Stock review" to Assessment; "Shared building review" and "Safety review" to the current step. Unknown blocker text falls back to the current step.
3. Done = step lies before the current step in slide order, and is not blocked. Upcoming = after current.
4. Funding and Resident agreement exception: in the real data `Waiting for resident decision` comes before `Funding check`, but the slide shows Funding first. Do not show Funding as Done only because of position. Funding is Done when recorded funding is Confirmed; Resident agreement is Done when `c.decision.status` is Accepted. Otherwise a step earlier than current but not evidenced is shown "Not confirmed" (Upcoming style, text "Earlier step not confirmed"). OWNER DECISION: keep slide order, or swap the two steps to match stage order. Recommended: keep slide order and use the evidence rule.

This keeps the slide principle: a blocked Funding step does not hide or disable
the other steps or tabs. Only the actions that depend on the conflicting record
(for example "Ready to book the installation") are refused, using the existing
`c.gate` reasons.

Slide blocker words mapped to existing data (shown as chips in the Blockers tab,
text always visible):

| Slide blocker | Existing evidence | New field needed |
| --- | --- | --- |
| Stale evidence | `c.work.evidence_freshness[].status` | None |
| Unclear owner | `c.work.owner` or blocker `owner` is "Unknown"; `work.handoff` unconfirmed receiver | None |
| Funding mismatch | blocker "Final checks: funding"; funding panel status not Confirmed | Confirm a "mismatch" signal exists; otherwise label it "Funding not confirmed" (existing SIGNALS wording) |
| No resident answer | `c.decision.status` neither Accepted nor Declined ("No resident decision yet" signal) | None |
| Rework | return history in `returnPanel`; stage "Design being corrected"; quality defects in `qualityPanel` | Flag: confirm `c.returns` is in the case API payload |

### New field (optional, recommended)

`c.journey = { step, steps: [{ name, state, reason }] }` computed in the server
so the list, coordinator and case views share one rule. Until then the client
computes it. Either way, the tests below fix the rules.

## Tabs

Native-semantics tab pattern (WAI-ARIA tabs, automatic activation is not used:
arrow keys move focus, Enter or Space activates, to avoid re-render cost and
lost drafts). Tab list is `role="tablist"` with `aria-label="Case sections"`;
each tab is a `button role="tab"` with `aria-selected`, `aria-controls`, roving
`tabindex`; each panel is `role="tabpanel"` with `aria-labelledby` and
`tabindex="0"`. Selected tab is stored in the URL as `?tab=` inside the hash so
refresh and back work. Default tab: the tab of the first active blocker, else
Overview. Each tab label carries a count or state in text, for example
"Blockers (2)", "AI (1 to review)".

If scripting fails the page must not blank: render panels as stacked sections
with `h2` headings (current behaviour) as the fallback.

| Tab | Panels moved here (existing function or markup) |
| --- | --- |
| Overview | `workSummary`, "Where it is up to" card, "Contact" card, building and cost allocation card, "Final checks" card (`c.gate`, `c.can_advance`) |
| Blockers and safety | `workSteps` (blockers, overdue, task sources), `safetyPanel`, `regulatoryAlertsPanel`, `returnPanel`, `stockPanel` |
| Survey and assessment | `technicalPanel`, `documentsPanel` |
| Funding | `fundingPanel`, `financePanel`, `grantPanel` |
| Resident | `residentPanel` (decision per measure, commitment, requests and complaints), "Log a call", "Write to the resident" (drafts), `affectedChallengePanel` |
| Contractor and works | Contractor block of "Where it is up to", appointments and next visit (from the Contact card), work-order links |
| Quality and handover | `qualityPanel`, `handoffPanel` (since 2026-11-20 the merged "Hand this case to a colleague" card, which includes "Who could take this on"; the separate `sugg` card is gone) |
| Home sensors | `sensorPanel` (added 2026-11-20; it moved out of Quality and handover, which keeps a pointer) |
| AI assistance | `assistantCasePanel`, `chatCasePanel`, AI drafts launched from "Write to the resident" (see below) |
| History | "History" card (`c.contacts`, `workSummary`) |

Eight to nine tabs exceed a comfortable row (ten from 2026-11-20). This text
asked for the tab list to scroll horizontally at 900px and below inside a named
focusable area (same pattern as `.table-scroll`). The implementation differs:
since 2026-11-20 the tab list wraps at 900px and wider and scrolls in one row at
899px and below inside a plain wrapper with no name and no focus stop (see the
update below). The stepper links remain a second route to each tab.
Open question for the owner: merge Contractor and works into Overview if staff
rarely use it.

Rules:

* Actions stay where the record is. A summary-strip button switches tab and moves focus to the panel `h2` (`tabindex="-1"`).
* Switching tab never discards unsaved text: panels are built once and hidden with the `hidden` attribute, not rebuilt. After `refresh()` (which calls `caseView` again) the selected tab and any unsaved field values are restored using the existing `captureChallengeDrafts` and `restoreChallengeDrafts` approach, extended to the tab fields.
* Role gating is unchanged and enforced by the server. A tab a role cannot act in still renders read-only content and the existing refusal text.

## AI visibility pattern

Goal: a person always sees what AI produced, how sure it is, where it came
from, and what they decided. AI never changes owners, stages, ranking or
approvals (unchanged).

### Where it shows

* Summary strip "AI" item: count waiting for review, and assistance state from `assistantCasePanel` ("Assistance available", "Assistance unavailable ... Continue ordinary case work manually", "Workflow-only mode").
* Tab label "AI assistance (N to review)".
* Inline: any AI draft elsewhere (for example a message draft) uses the same card and also lists in the AI tab.

### One card for every AI output (`.ai-suggestion`)

Order of content, same for proposals, drafts and briefings:

1. Label (text): "AI suggestion, not approved. Not an instruction." After review: "Accepted/Edited/Rejected as a draft by a person. This is not an approval, consent or safety decision."
2. Status line: Not reviewed, Accepted, Edited, Rejected, Stale, Unverified, Failed (from `p.display_state`, `p.stale`, `d.approval`, `d.verified`). Text plus glyph.
3. What it suggests (`p.output.summary`, findings, "Unknowns").
4. Provenance in plain words: sources (`d.citations`, `f.citations`), removed uncited statements (`d.dropped_uncited`), who ran it and how (mode from `p.provenance` invocation: AI or workflow rules), when (`as_of`, version). Technical `snapshot` and hashes stay in a `details` ("Permitted sources, versions and hashes").
5. Confidence. No confidence value exists in the API or `aiNotes`. FLAG: new field, `confidence` as `{ level: "Low|Medium|High|Not provided", basis: "<one sentence>" }` per proposal. Until it exists, show "Confidence: not provided" and do not infer one from citation counts. Show the level as a word, never a bare percentage or colour; state that confidence is not accuracy.
6. Review controls (see below).

### Accept, edit, reject with reason

Single control set for both existing vocabularies, shown as a `fieldset` with
`legend` "Your review":

* Buttons: "Accept", "Edit", "Reject" (replaces "Accept as is" / "I changed it" in `aiNotes`; assistant cards keep "Accept proposal only" wording in the button help text so the boundary stays explicit).
* "Reason" is a visible `label`ed input. It is required for Edit and Reject. Error is a linked `.field-error` message (`aria-invalid`, `aria-describedby`), not only `setCustomValidity` popups.
* Assistant proposals keep the extra step "I checked the cited sources" before Accept (existing `verify` flow), and the existing `ownVerification` restriction on who may accept stays. Server still enforces authority and revision.
* Result is announced in the card's `role="status"` and recorded in the audit log (existing endpoints `/api/ai/review/...` and `/api/assistants/proposals/.../review`). Reason text is shown afterwards in the card.
* Rejected or stale suggestions collapse into a "Reviewed" `details` list so the tab shows work to do first.

Requesting AI stays optional beside a non-AI route ("Plain visit template",
workflow-only mode).

## Responsive behaviour and zoom

* 1200px and wider: strip 3 columns, stepper horizontal, tabs wrap (this text said one row; see the update below).
* 900px to 1199px: strip 2 columns, stepper 3 columns by two rows (2026-11-20), tabs wrap (this text said scroll in a named focusable area).
* Under 900px (and 320 CSS px at 200% zoom): strip 1 column, stepper vertical, tab list scrolls horizontally in one row inside a plain wrapper (2026-11-20). This text preferred wrapping buttons over a select to keep native tab behaviour; the owner has not chosen between the two rules (CD3 in the [review record](./staff-workbench-ux-review-2026-11-20.md)).
* No fixed heights; no text truncation without a full-text route; `rem` units; touch targets at least 24 by 24 CSS px (existing 40px buttons).
* No sticky strip, so it cannot cover content at 200% zoom or 320px (WCAG 2.4.11 focus not obscured).
* Reduced motion: no tab or stepper animation.
* Forced colours: step state uses text and border style, not fill alone.

## Empty, loading and error states

| Situation | Behaviour |
| --- | --- |
| Case request loading | `aria-busy` with "(loading)" text in the strip; tabs not rendered until data arrives |
| Case request failed | Existing error path; plain sentence with retry button and back link |
| No blockers | "No recorded blockers." Stepper shows no blocked step |
| Blocker owner Unknown | Show "Owner: Unknown" and the next action "Ask <role> to record an owner" |
| No AI suggestions | "No AI suggestions yet. Ordinary case work is not affected." with the request buttons |
| AI unavailable or timed out | Status text from `assistantCasePanel`; strip says "AI assistance unavailable. Work continues manually."; every non-AI action works |
| AI output stale or unverified | Status word "Stale" or "Unverified", Accept disabled with native `disabled` and a visible reason |
| Panel data missing (for example no funding record) | Panel heading plus a sentence stating what is absent and what to do; distinct from "failed to load" |
| Closed case | Stepper all Done, no current; existing "Closed case" and reopen panel (manager) first in Overview; the summary reads "Closed, all six steps done" (2026-11-20) |
| Unknown `tab` value | Fall back to default tab, no error |

## Acceptance criteria

1. A user sees status, current step, next action, owner, blockers and AI state without scrolling at 1280x800 and at 320px width after at most one swipe (strip then stepper).
2. The stepper has six steps in slide order; exactly one has `aria-current="step"` unless the case is closed; each shows a text state; every one of the 25 stages maps to a step.
3. A blocked step does not disable other steps, tabs or unrelated actions; blocked actions explain reason, owner, next action.
4. Every existing panel listed in the case view appears in exactly one tab; no existing action is removed; no new data field is invented (confidence and server `journey` are flagged as optional new fields).
5. Tabs satisfy the WAI-ARIA tab pattern, selection survives refresh and `refresh()`, and unsaved text survives a tab switch.
6. Every AI output shows the exact label, status, sources, confidence (or "not provided"), and accept/edit/reject with a reason required for edit and reject. No AI output changes owner, stage, ranking or approval.
7. No status is shown by colour alone; focus is visible and not obscured; content works at 200% zoom and 320 CSS px without two-dimensional scrolling (except named table and tab regions); reduced motion respected.
8. All copy follows the content standard (ASCII, no em dashes, no internal terms such as gate or provenance in visible text; the current "Final checks" and "Sources" wording is used).

## Test plan

Unit (Python plus JS where the repo already has web tests; otherwise extend `src/api/tests`):

* Stage-to-step map covers all of `STAGE_ORDER` (fail on unmapped stage).
* Derivation table tests: each stage as current; closed; blocker per mapped step; blocked-and-current; Funding and Resident agreement evidence rule; unknown blocker text.
* Summary strip values for owner Unknown, no blockers, pending handoff, no AI.
* AI card: label text exact; Edit and Reject refuse without reason; stale disables Accept; confidence missing shows "not provided".
* Static check that each panel function is referenced by exactly one tab builder.

Automated accessibility (extend `src/api/checks/design_system_browser_check.py`, Playwright with axe-core, synthetic data only):

* axe on every tab, in loading, empty, blocked, AI-unavailable and closed cases. Zero serious or critical violations.
* Landmark and heading outline: one `h1`, tab panels start at `h2`, `ol` with six items.

Keyboard:

* Tab order: back link, strip action buttons, stepper links, tab list (one stop), active panel.
* Arrow Left/Right/Home/End move between tabs; Enter or Space activates; focus moves to the panel heading after a summary-strip jump.
* Complete accept, edit (with reason), reject and the "Ready to book" action without a mouse. No keyboard trap.

Zoom and reflow:

* 200% browser zoom at 1280 wide, and 320 CSS px wide: no clipped text, no overlap, focus not obscured, strip and stepper reflow as specified.
* Forced colours and reduced-motion emulation screenshots; step states still distinguishable.

Manual (Not run, required before any claim): screen reader pass on stepper, tabs
and AI review card (NVDA with Firefox or Chrome, VoiceOver with Safari); a
usability session with real case officers on find-the-blocker and
find-the-AI-suggestion tasks, to test the assumption in the evidence section.

## Out of scope and escalation

No visual brand decisions, no Fluent React or Web Components swap, no new
approval powers for AI. Owner to decide: step order (Funding versus Resident
agreement), number of tabs, and whether to add `confidence` and `journey` to the
API.

## Implementation boundary (2026-10-28, Refs #526)

Owner decision in #526 resolves step order: retain the slide's Funding before
Resident agreement order, using the evidence exceptions above. The initial
implementation kept all nine tabs (ten since 2026-11-20; see the update below). Existing native Fluent tokens, role checks,
manual paths and human/resident approval boundaries remain unchanged.

The client derives journey from the existing payload; no `journey` or
`confidence` field is added. `returns` is present in the existing case detail.
Funding uses "Funding not confirmed", not a fabricated mismatch signal.
Missing confidence displays "Confidence: not provided. Confidence is not accuracy."

Draft and assistant-proposal reviews use their existing audited endpoints.
Chat answers have no existing recorded-review identifier or review endpoint.
Their card displays advisory/source/confidence information and explicitly routes
recorded review to a separately requested proposal. Accept/edit/reject of a chat
turn itself is not implemented or implied. This is a disclosed criterion 6
exception, not a local-only approval or an invented audit record.

Open safety controls are rendered once above the stepper and remain visible
on every tab. Blockers links to that same panel; it does not duplicate controls.
Tab-only navigation retains live panels and in-flight work. Same-case refresh
retains generated resident draft nodes and their review context, plus dirty
fields; completing a form clears only its own inputs. Confirmed departure
disposes case-local drafts. If the optional tab enhancement script fails,
headed sections stay stacked with manual controls available.

Reproduction commands and the local-only evidence boundary are in the
[API guide](../../../../src/api/README.md#employee-case-journey-workspace-526).
Screen-reader, real case-officer usability and post-deployment verification
remain Not run, pending the owner. No accessibility conformance or live
acceptance is inferred.

Engineering continuation: API unit discovery and focused browser checks now
pass on constructed data with Chromium 156.0.8078.4 and pinned axe 4.10.3.
The journey check covers 37 axe states, retained drafts, keyboard draft reviews,
blocked final checks and actual 200% tab zoom. Compact mobile summary spacing
keeps full 16px values within the unchanged one-scroll bound (1581.96875 <=1600
at 320x800); keyboard-focused tabs scroll fully into view at 200%.
Existing workbench, recovery, assistant, provenance, regulatory and challenge
checks also pass. This does not sign off the design's human acceptance criteria.
Independent Review executed with four defects, retained in its original record.
Later repairs preserve same-card and asynchronous proposal drafts by ID/revision,
retain copyable edits when evidence changes, update document review counts and
correct local runner import parity. New regression checks pass, including
27 assistant scenarios. The clean committed-candidate publication gate and
exact-head assessment remain separate pending steps.

## Staff workbench UX update (2026-11-20)

On 2026-11-20 the owner asked for a UX review of the staff workbench. Two designer
agents reviewed the product on synthetic data. The
[review record](./staff-workbench-ux-review-2026-11-20.md) holds the evidence, the
findings and their dispositions, the decisions taken on the owner's behalf and the
open owner decisions; CD1 to CD12 below refer to it. The case screen changed as
described here. The evidence is engineering checks in Chromium on constructed data.
No user, screen reader or other browser was involved. Nothing here is an
accessibility conformance claim or an owner approval.

### Tabs

The case has ten tabs, in this order: Overview, Blockers and safety, Survey and
assessment, Funding, Resident, Contractor and works, Quality and handover, Home
sensors, AI assistance and History. History stays last. The sensor panel moved out of
Quality and handover into Home sensors (`?tab=sensors`). Quality and handover keeps
one line, "Home sensor readings and alerts are on the Home sensors tab.", and an Open
Home sensors button that selects the tab and moves focus to its title. The AI tab
label is shorter when the count cannot be read ("AI assistance (count unavailable)").

The tab list wraps at 900px and wider. At 899px and below the tab buttons sit in one
row, inside a plain wrapper (`.case-tabs-row`) that scrolls sideways, and script
scrolls the selected tab into view along the row only. The wrapper has no name and no
focus stop; the buttons are the focus stops. The earlier design asked for a named
focusable area. Whether assistive technology still announces one tab list with the
right count is not checked, and the owner has not chosen between this and wrapping
(CD3). The final review measured three costs that are not fixed. At 1024px the tab
list wraps to three rows (it was two) and, with the two-row strip, the work panel
starts about 133px lower; starting the scrolling row at 1199px or shortening the tab
names would recover it (CD3). A selected tab can sit out of view after a resize or a
turn of the device, because script reveals it only on selection and on a label
change. The long AI label does not fit the row at 320px.

### Summary and header

* A closed case reads "Closed, all six steps done" for the current step, "None. A
  manager can reopen this case." for the next action and "No recorded blockers. This
  case is closed." for blockers. It shows no blocker disclosure and no jump button:
  Open next action is left out, and See all blockers shows only for an open case that
  has blockers. Before the update the same summary said "Step unknown", asked for a
  next action and showed a blocker while the strip above it showed six done steps. The
  first build of the update still offered both buttons beside text that said there was
  nothing to do.
* The header holds three separate links in a list: "Back to the list", "Versioned
  home case" and "Shared building context: {id}".

### Journey strip

Cards stretch to the tallest card in their visual row. The link takes the free height
and the blocker button sits at the foot of the card, so the cards in one row have
equal height. The strip is six columns at 1200px and wider, three columns by two rows
from 900 to 1199px and one column at 899px and below. A blocked step shows the fixed
words "Why blocked" on its button; its accessible name still starts "{Step}: why
blocked", and the popover with the reason, owner and next action is unchanged. The
summary button keeps the first sentence of the reason and the word Details. The
three-column layout and the fixed label are decisions taken on the owner's behalf
(CD2).

The summary strip above the journey strip has three columns at 1200px and wider, two
at 1199px and below and one at 899px and below. The earlier text on this page says two
at 900px and one at 600px. Flagged, not changed: the stylesheet governs.

### Quality decisions card

Each measure is one record card: the measure as a heading, a status line, a fact list
(Evidence version, Checklist, Evidence from, and Accepted by or Handed over by when
they apply), the recorded checks in a disclosure that is open while the work is
submitted, returned or fixed, the defect when one exists (What is wrong, Why it was
returned, Who will put it right, Remediation evidence) and a decision area for the
state.

| State | Status words | Decision area |
| --- | --- | --- |
| Submitted | Waiting for an independent check | Accept this work (Note, optional) beside Return with a defect (Why you are returning it, What the defect is, Who will put it right; all required); stacked below 1200px |
| Returned | Returned: defect to put right | Record that the defect has been put right (Who fixed it; What was corrected, with the photo, document or inspection reference; both required) |
| Fixed, awaiting reinspection | Fixed, waiting to be checked again | Check the fix again: one optional note and the buttons Accept this work and Still not right; Enter in the note does nothing |
| Accepted | Accepted, ready to hand over to the resident | Hand over to the resident (What the resident was given or told; the tick The resident has been told; both required) |
| Handed over | Handed over to the resident | Add an aftercare note (required) |
| Superseded | Replaced evidence: previous acceptance and handover no longer apply | No controls and a link to the current record |

In the Submitted and Fixed states a viewer who may not check sees "A Quality Inspector or a manager checks this work."
with the owner and next action. Every field has a visible label, its hint and a
"(required)" or "(optional)" mark. Empty required boxes post nothing: one sentence
appears beside each and focus moves to the first. A refusal from the server shows its
own reasons, with owner and next action, inside the record. A success shows a
"Recorded: ..." line at the top of the card and moves focus to the record heading.
The decision buttons carry the measure in their accessible names, for example
"Accept this work: {measure}". The evidence form below the records is one labelled
fieldset with Save evidence as the primary button.

### Handover card

One card, "Hand this case to a colleague", replaces the handoff card and the "Who
could take this on" card. It stays in the Quality and handover tab by a decision taken
on the owner's behalf (CD1).

* Status: a status line and a definition list (Case stays with, Who must act next,
  Offered by, What they are asked to do, How urgent, Due, Note from {name}, Chase
  owner, Resident update owner), in local dates and with no record paths. The person
  an offer is made to reads "Offered to you, waiting for your answer" and "What you are
  asked to do"; everyone else reads "Offered to {name}, waiting for an answer" and
  "What they are asked to do".
* The receiver sees "Your answer": Record receipt (not acceptance), Accept this case
  (source reference, source version and reason, all required) and Decline this case
  (reason, required).
* The sender or a manager, with an open offer, sees "Change this offer": Withdraw the
  offer to {name}, and a closed disclosure to escalate to a manager. The new owner
  sees "Complete the handover" after accepting, as the card heading and as the name
  of its button.
* Anyone who may offer sees "Who could take this on": one button per suggested
  person, "Offer this case to {full name}", which opens a labelled form (source
  reference, source version and reason required; next action, urgency, due date and
  note optional) and sends the `offer-handoff` action. "Offer to someone who is not
  listed" holds the full colleague list with nobody preselected.
* When offering is not possible (the case is closed, an offer is open, an acceptance
  is not complete, or the viewer is not the owner or a manager) a notice gives the
  reason, the owner and the next action.
* Text the server holds back shows as "Held back for your role. Owner: {name}. Next
  action: ask {name} ..." (CD6). The sentence is built once, and the quality record
  uses it too in a handed-over record, its previous handover note and its aftercare
  notes. Results show in the card, and the history reads one sentence per event.
* A missing required field gets one short sentence, for example "Say where this change
  came from."; blocked or refused actions keep the reason, owner and next action. The
  suggestions read "1 open case" for one case.
* The server rule is unchanged: the case moves only when the other person accepts.

### Home sensors tab

Panel `#case-panel-sensors`, content `#sensors`. The readings come from
`GET /api/cases/{id}/sensors` and `/sensor-drafts`. Only the Quality Inspector and the
Retrofit Programme Manager may read; every other staff role sees a plain explanation
and the page makes no request. The tab label gains a count once, after the reply, and
only when something needs attention, for example "Home sensors (1 alert)". Contents, in
order: the title; a status line with "Checked {time} (UK time)"; one muted line
("Readings are advice for a person to check. They do not change the case."); "Alerts for this
home", where each alert gives What we see, Owner and Next action; "Latest reading";
"Recent readings" with local times, tabular figures and no reading ids; "Around the
first quality evidence record" (Before and From then on); "Sensor review draft"; and a
closed "About these readings" disclosure.

| State | Status words | What shows |
| --- | --- | --- |
| Loading | Loading home sensors | The status line only |
| Role may not read | Sensor readings are not shown for your role | An explanation that names a Quality Inspector or a Retrofit Programme Manager as the owner |
| Not connected | Sensor readings are not connected in this setup | Owner application support; use the ordinary quality check |
| Account not linked | Your staff account is not linked to your role | Readings hidden; owner your team manager; no drafts request |
| Service down | Home sensors are unavailable right now | Owner application support; refresh the page |
| Unavailable | Sensor readings could not be read | Owner application support; refresh this home |
| No readings | No sensor readings recorded | "Use the ordinary quality check." |
| Recent | Recent reading (within 15 minutes) | Full content |
| Out of date | Reading out of date (older than 15 minutes) | One alert; the label gains a count |
| Sensor may be offline | Sensor may be offline (no reading for over 24 hours) | One alert; the label gains a count. The server's map label still says "Sensor offline" |
| Readings disagree | Readings disagree | An alert and a table of the rows that disagree; no single latest value |
| Sensor fault, reading out of range | Sensor fault; Reading out of range | An alert; the latest reading is marked "Do not use this reading" |
| Consent withheld | Readings withheld: monitoring consent is not granted | No values and no table; owner the resident's consent owner |
| Dated in the future | Latest reading is dated in the future and is not treated as recent | The reading is not treated as recent |

The alerts name "the quality team" as the owner. The owners in this copy are phrases
that the roster owner still has to confirm (CD4).

### Left open

The decisions CD1 to CD12 and D1 to D14 in the review record stay with the owner. The
panel's own scroll, the compact summary at 390px and the safety panel placement are
unchanged, and so is the handover card's place at the foot of the Quality tab (CD1).

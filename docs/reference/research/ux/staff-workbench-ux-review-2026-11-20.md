---
title: Staff Workbench UX Review and Case Screen Change Set (2026-11-20)
description: Evidence, findings, dispositions, decisions taken on the owner's behalf, open owner decisions and validation limits for the 2026-11-20 UX review of the staff workbench and the changes it led to
ms.date: 2026-11-20
ms.topic: reference
---

## Scope and evidence

On 2026-11-20 the owner asked for a UX review of the whole staff workbench. The request (Reported) gave four examples from the case screen (`#/case/{id}`):

* In the Quality and handover tab, the text boxes beside "Accept this work" and "Return with a defect" had no visible label or hint.
* The six-step journey strip was misaligned when a step had details.
* No case tab showed this home's IoT telemetry and alerts.
* The case handover had no buttons to hand the work to the people it names.

Two UX designer agents reviewed the product with rendered evidence. One took the case screen and one took every other screen. Their reports were session files, not repository files, and are not retained here: `ux-review/case/report.md` (24 findings, F1 to F24, specifications A to D) and `ux-review/app/report.md` (40 findings, F01 to F40, specifications FB-1 to FB-11, a defer list D1 to D14). The screenshots and JSON audits are not retained either. After the build was committed each designer also wrote a final review of it (`ux-review/case/final/final-review.md` and `ux-review/app/final/final-review.md`); those are session files too. This page carries the findings, the evidence summary, the dispositions, the decisions and the limits, so it can be read without them. It documents engineering changes to a synthetic-data demonstrator. No acceptance criterion, for example AC-034, is ticked by it.

The change set was developed as a series of commits on the pull request branch, and the squash merge replaces their ids, so this page cites spec ids and file paths instead.

Evidence labels follow the reports. Observed means measured in a rendered artefact or in code during the review; it is not observed user behaviour. Reported means stated by the owner or in a repository document. Assumed means plausible and untested. Unresolved means open.

### What was reviewed

* Build: a snapshot of `origin/main` at `5e7af3e01` (`git archive`), served from a throwaway loopback server on a JSON store with synthetic data only. The working tree was not rendered.
* Case screen: the Retrofit Programme Manager, Quality Inspector and Resident Liaison Officer on all nine tabs of that build, and the Contractor's restricted job view, which has no tabs. Every tab at 1440, 1024 and 390px, plus 1280, 1100, 900, 899 and 320px for the strip experiments. 395 screenshots with JSON audits.
* Every other screen: all eight roles, 49 URLs, 115 role-and-route variants at 1440, 1024 and 390px (345 captures) and 54 forced-state captures, 399 in all. An in-page audit script (labels, headings, tables, targets, overflow), axe-core 4.10.3 (rule identifiers only), a copy scan and keyboard probes. Both reviews used Chromium through Playwright 1.64.
* Starting evidence: the owner's four screenshots.
* Final reviews: each designer scored the committed build against the acceptance criteria of their own report. The case review used 49 criteria at nine widths from 1440 to 320px. The application review used 24 criteria, re-ran the same 115 role-and-route variants at 1440 and 390px (230 audited captures) and added 50 forced-state captures. Both read the build as it stood before the polish commits, and neither ran again afterwards (see Second pass).

### How states were produced

* Real server (seeded data, real API calls or real clicks): blocked steps; open, escalated, accepted, declined and withdrawn offers; the open safety issue; the closed case; the six quality record states, reached by submit, accept, handover, aftercare, return, fix and resubmit calls; a refused Accept; a refused offer click; every denial and unknown route; the sensor state "not connected".
* Intercepted responses (Playwright route interception): every other sensor state (fresh, stale, readings disagree, offline, withheld, unavailable, account not linked, service down), built with the repository's own sensor view helpers over hand-made reading rows. In the application review: startup held open or failing, session ended, list error, list denied, list loading, visits error, time capture enabled (the feature is off in the demo data) and one assistant proposal.
* Strip variants V0 to V4: CSS injected into a scratch copy of `style.css` plus one DOM move. The repository was not touched.

### What was not done

* No user took part. No staff member, resident or assistive-technology user was observed, so every effect on staff in the findings is Assumed or Reported.
* No screen reader, no keyboard-only walk by a person, no real device, no zoom or text-size run and no browser other than Chromium.
* The resident demo site was not reviewed. Its browser check needs a throwaway SQL Server.
* Real SQL-backed sensor readings were not run. The sensor responses were intercepted. A live Entra sign-in was not reproduced: the account-not-linked state came from interception and from reading the core code.
* No contrast value, conformance statement or accessibility verdict was produced. Those route to the accessibility skill.

### Records that still describe the earlier layout

These dated records were not edited. The 2026-11-12 trace in the [prototype profile review](./zava-forward-prototype-profile-review.md) says the Quality and handover tab composes the sensor panel with the quality and handover panels; the sensor panel now has its own tab. The [2026-11-18 live evidence for #619](../issue-619-live-at-consent-evidence-2026-11-18.md) records nine tabs on the deployed demo build.

## The four reported defects

### 1. Quality decision fields without visible labels

* Observed: eight inputs had only a hidden accessible name and none was marked required or optional. One wrapping row held the fields and the buttons. One note box served both Accept (optional) and Return (the reason, required), and the Return button said "add the reason above".
* Change (labelled-field helper and quality decisions): `fields.js` adds one labelled-field helper (see the [design system](./design-system.md#labelled-field-and-check-row)). The Quality checks and defects card is now one record card per measure: heading, status line, fact list, the recorded checks in a disclosure, a defect block and a decision area. Accept this work and Return with a defect are separate fieldsets with visible labels, hints and "(required)" or "(optional)". Return with empty boxes sends nothing, puts one sentence beside each empty box and moves focus to the first. A refused action shows the server's own reasons, with their owner and next action, inside the record. The evidence form is one labelled fieldset with Save evidence as the primary button. At 600px and below the tab panel keeps bottom padding so the chat launcher does not cover the last button.
* Where: `web/fields.js`; `web/ops.js` (`qualityPanel`, `qualityField`, `qualityTick`, `qualityComplete`, `qualityRecorded`); `web/style.css` (the `ux-batch:quality-decisions` block).
* Checked by: `test_fields_helper.py` and `test_quality_decisions_ui.py` (labels, validation, inline refusals, Enter never accepting fixed work, the names and ids that other checks rely on) and the case journey browser check. No person used the form.

### 2. Misaligned journey strip

* Observed: four card heights for one case at 1440 and 1024px (66, 90, 110 and 134px). A closed case with no blocked step still had two. At 1024px "Assessment" broke mid-word and blocked steps showed five letters of the reason before an ellipsis.
* Cause (Observed in code): the strip used `align-items:start`, the blocker button sat inside the card and names could wrap to two lines.
* Change (journey strip, header links and closed-case summary): cards stretch to the tallest card in their visual row and the blocker button sits at the foot of its card. From 900 to 1199px the strip is three columns by two rows; at 899px and below it is one column. Step cards show the fixed words "Why blocked" instead of a clipped reason. The accessible name and the popover with the full reason are unchanged. The case header links are separate list items, and a closed case's summary agrees with its six done steps. A closed case offers no Open next action or See all blockers button, and See all blockers shows only for an open case that has blockers.
* Where: `web/style.css` (`.stepper`, `.step`); `web/case-workspace.js` (`blockerDisclosure`, `summary`, `nextTab`); `web/app.js` (`.case-links`).
* Checked by: `case_view_ux_browser_check.py` measures equal heights within each visual row for five fixtures (no blockers, one blocked, two blocked, current and blocked, closed) at thirteen widths from 1920 to 320px, with a 45-character stress name, the header links and the closed summary. `test_case_journey.py` gains two tests for the closed-case summary.

### 3. No Home sensors tab

* Observed: the sensor panel was the first card in the Quality tab. With readings it was 2,380 to 2,444px tall at 1440px and 6,831 to 7,039px tall at 390px (intercepted data), above the quality decisions. Alerts existed on the map only. The owner's third screenshot showed a refusal in internal terms ("Use the manual route: manual-sensor-review").
* Change (Home sensors tab and tab row): a Home sensors tab after Quality and handover (`?tab=sensors`, panel `#case-panel-sensors`, content `#sensors`). It shows the status line first, with when it was checked, then one muted advisory sentence, then alerts with what is seen, the owner and the next action, the latest reading, tables in UK local time without reading ids, the sensor review draft and a closed "About these readings" note. Every state has its own sentence with an owner and a next action. The tab label gains a count only when something needs attention, for example "Home sensors (1 alert)". The Quality tab keeps one line and an Open Home sensors button. The same change makes the tab list one scrolling row at 899px and below and shortens the AI tab label to "count unavailable".
* Where: `web/ops.js` (`sensorPanel`, `SENSOR_COPY` and helpers); `web/case-workspace.js` (label count, tab row); `web/app.js` (tab list); `web/style.css` (the `ux-batch:sensors` block).
* Checked by: `test_home_sensors_tab.py` (every badge state has a copy entry, no internal identifier reaches the screen, a role that may not read makes no request) and `quality_sensors_browser_check.py`, updated for the new tab. Real SQL-backed readings were not part of the review.

### 4. Handover without buttons for the named people

* Observed: offer buttons showed only when the viewer could offer. Each posted only the colleague to the older `handover` action, and the real server refused it ("Enter the source reference, from 1 to 200 characters.") with the message at the bottom edge of a 900px window. The working form was a separate card whose drop-down preselected the first colleague. Buttons carried first names only ("Offer to Resident"). A non-owner saw an empty card. The status was four run-on paragraphs with a raw timestamp and a record path.
* Change (handover card): one card, "Hand this case to a colleague". Status is a definition list. Each suggested person has "Offer this case to {full name}", which opens a labelled form: source reference, source version and reason (required), plus next action, urgency, due date and note (optional). It sends `offer-handoff` with `source`, `source_version`, `reason` and `handoff_version`. "Offer to someone who is not listed" holds the full colleague list with nobody preselected. When offering is not possible, a notice gives the reason, the owner and the next action. Results show in the card, with Withdraw as the undo. The history reads one sentence per event. The person an offer is made to reads "Offered to you, waiting for your answer" and "What you are asked to do", and the button that completes an accepted handover is "Complete the handover". Text the server holds back from the viewer's role reads "Held back for your role. Owner: {name}. Next action: ask {name} ..."; `fields.js` builds that sentence once and the quality record uses it too. The server rule is unchanged: the case moves only when the other person accepts.
* Where: `web/app.js` (`handoffPanel`, `handoffRows`, `handoffNotice`, `handoffOfferRow`, `handoffElsewhere`, `recordedChangeForm`); `web/style.css` (the `ux-batch:handover` block).
* Checked by: `test_handover_ux.py` runs the shipped card in a mini DOM (one button per person, empty fields post nothing and show one short sentence each, a valid send posts `offer-handoff`, nobody preselected, a status list with no raw times or record paths, the receiver's own wording, and the held-back wording pinned to both server constants and the copy in `fields.js`). The journey and provenance browser checks open "Offer to someone who is not listed" first.

## Findings and dispositions

Dispositions were checked against the code of the pull request branch on 2026-11-20, including the polish that followed the final reviews.

* Done in this change: the code does what the finding asked.
* Done in part: some of it is done and the residual is stated.
* Deferred to the owner: waits for a decision. CD1 to CD12 are labels this page gives to the open items of the case screen report, which carried no identifiers. D1 to D14 are the application report's own.
* Deferred (backend change): the cause is server text or a missing server field.
* Not planned: a specification exists (its id is shown) but this change set does not build it.

### Specification build status

| Spec | Subject | State |
| --- | --- | --- |
| A | Quality decisions | Built |
| B | Journey strip, case header links, closed-case summary | Built |
| C | Home sensors tab and tab row | Built |
| D | Handover | Built |
| FB-1 | One labelled-field pattern | Built; a missing required field gets one short sentence |
| FB-2 | One check-row pattern | Built; the label carries the spacing so the whole row is clickable, and the hint lines up under the label text |
| FB-3 | Button hierarchy and link rows | Not built, except one primary button in the work-order row (built under FB-1) |
| FB-4 | Facts as description lists | Not built |
| FB-5 | Empty, error and denied states with an owner and next action | Not built |
| FB-6 | Page identity | Built except the route-level error copy, which belongs to FB-5. The tab title leaves the safety flag out, work lists name their list with a second-level heading and the Microsoft sign-in card matches the password card |
| FB-7 | Quiet status line | Not built |
| FB-8 | Links, targets and numbers | Built, with the exclusion list and the target rule in `:where()`. The coordinator's compact link rule is limited to links in tables, and the page-end space applies at 600px and below |
| FB-9 | Copy defects | Built except date formatting, which needs FB-4 |
| FB-10 | Programme queue request | Built; the funnel's as-of time is formatted like the neighbouring panels |
| FB-11 | Next-action links on specialist screens | Not built; owner confirmation first (D8) |

### Case screen findings (F1 to F24)

| ID | Screen | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| F1 | Quality and handover: quality decisions | Blocks the task | Eight inputs with a hidden name only, none marked required or optional; one note box fed both Accept and Return | Done in this change (Spec A) |
| F2 | Journey strip | Confuses | Four card heights for one case; a closed case was uneven too | Done in this change (Spec B) |
| F3 | Quality and handover: sensor panel | Blocks the task | No tab for this home's sensors; the panel opened the Quality tab and ran to 7,039px at 390px | Done in this change (Spec C) |
| F4 | Quality and handover: handoff | Blocks the task | Offer buttons missing or refused by the server; a separate form with a preselected colleague; first names only; no reason when offering was impossible | Done in this change (Spec D) |
| F5 | Sensor panel: 403 reply | Confuses | Internal terms, a code-style route name and advice that did not exist, with an owner who cannot fix a staff-list gap | Done in this change (Spec C). The same cause still shows in the AI tab and the summary line (R1, R2 below; CD11) |
| F6 | Quality decision results | Blocks the task | A refused Accept showed a generic message with the wrong owner while the real reason sat below the panel; an empty Return named no field | Done in this change (Spec A) |
| F7 | Handoff status | Confuses | Run-on paragraphs, repeated facts, a raw timestamp and a record path; the same block on Overview had a doubled full stop | Done in part (Spec D, FB-9). The card is fixed, the person an offer is made to reads the status as written to them and the doubled stop is gone; the Overview task-context block still prints the semicolon run-on with a raw time and a record path (FB-4, D14) |
| F8 | Handoff: receiver view | Confuses | Held-back text read "Held for roles with a recorded need"; the receiver could not see what they were taking on | Done in part (Spec D). The receiver reads "Offered to you, waiting for your answer" and "What you are asked to do"; the held-back sentence names an owner and next action and is the same in the card and in a handed-over quality record. Whether a receiver should see the held text is open (CD6) |
| F9 | Handoff: escalated offer | Confuses | "Escalated to ..." read like an answer and the manager was not told what to do | Done in this change (Spec D) |
| F10 | Case header | Confuses | Two links ran together, one hiding a second destination | Done in this change (Spec B) |
| F11 | Case screen layout | Confuses | Work panel below the first screen; the tab list wrapped to eight rows at 390px; a tenth tab adds a row | Done in part (Spec C). One scrolling row at 899px and below and a shorter AI label. The final review measured it: at 390px the tab list went from eight rows to one and the work panel now starts at 1,819px instead of 2,246px (Programme Manager); at 1024px the tab list wraps to three rows (it was two) and the strip is taller, so the panel starts about 133px lower (1,184px against 1,052px). Not fixed: that 1024px regression (width choice in CD3), a selected tab out of view after a resize and the long AI tab label clipped at 320px |
| F12 | Journey strip: blocked step | Confuses | The reason showed as five letters and an ellipsis | Done in this change (Spec B). Step cards say "Why blocked"; the full reason stays in the popover and the summary |
| F13 | Strip, summary, popover | Confuses | A Quality Inspector sees "Held for roles with a recorded need" as the reason | Deferred to the owner (CD6). The text is server wording |
| F14 | Quality record cards | Confuses | Six record states looked alike, one run-on sentence each | Done in this change (Spec A) |
| F15 | Quality: evidence form | Confuses | Unexplained scope revision, nothing marked required, eleven fields in one column | Done in this change (Spec A) |
| F16 | Sensor panel | Confuses | Five paragraphs of caveats before the data, a repeated source sentence, raw ids and UTC times | Done in this change (Spec C) |
| F17 | Sensor panel wording | Confuses | Internal identifiers and jargon, an em dash, and the case and map disagreeing on when a sensor is offline | Done in part (Spec C). Client copy rewritten and the 24-hour offline rule copied with a pinning test. The case tab says "Sensor may be offline (no reading for over 24 hours)", as its alert does, while the server's map label still says "Sensor offline"; the server's own strings are unchanged (Deferred (backend change)) |
| F18 | Summary: AI item | Confuses | "AI review count unavailable" has the same cause as F5 and does not say so | Deferred to the owner (CD11). Still true in the final review (R2 below) |
| F19 | Case screen at 390px | Polish | The summary block is 625px tall and pushes the strip down | Deferred to the owner (CD7). The final review measured 541 to 668px (R5 below) |
| F20 | Status line glyph | Polish | The waiting glyph is a font character that rendered as an empty box on the review machine | Deferred to the owner (CD12). Still an empty box in the final review's render (R6 below) |
| F21 | Tab panel | Polish | The panel scrolls inside the page and results sat below the scroller | Done in part (Specs A and D). Results now show in the card; the inner scroll stays (CD8). The final review measured the Quality tab at 4,214px of content in a 591px frame on a phone (R3 below) |
| F22 | Chat launcher | Polish | The fixed launcher covered the last button | Done in this change (Spec A, FB-8). The clearance applies at 600px and below, where the launcher can cover the last card; wider screens were not re-measured |
| F23 | Safety panel above the strip | Confuses | Two long forms push the strip about 1,500px down | Deferred to the owner (CD9) |
| F24 | Summary: closed case | Confuses | "Step unknown", a next-action prompt and a blocker on a closed case | Done in this change (Spec B). A closed case reads "Closed, all six steps done", "None. A manager can reopen this case." and "No recorded blockers. This case is closed."; it offers no Open next action or See all blockers button |

### Application findings (F01 to F40)

The application report banded its findings: F01 to F09 block the task, F10 to F33 confuse, F34 to F40 are polish.

| ID | Screen | Severity | Finding | Disposition |
| --- | --- | --- | --- | --- |
| F01 | Work list | Blocks the task | The heading sat about 2,187px down (4,643px at 390px) with 23 Tab stops before the first case; the briefing and priority panels came first | Done in part (FB-6). The h1 is the first heading in the page and the results sit under their own second-level heading, "My open cases" or "All open cases"; the briefing and priority panels still open above the list, which the final review found about 2,271px down at 1440px with no change in the Tab presses to the first case (D1) |
| F02 | Capacity: work orders | Blocks the task | Two unlabelled text boxes and a select beside four buttons; one note box served four actions | Done in this change (FB-1) |
| F03 | Programme queue | Blocks the task | The request had no as-of time, the server answered 400 and the panel always read Unknown | Done in this change (FB-10) |
| F04 | My cases, empty queue | Blocks the task | The empty state names no owner or next action | Deferred to the owner (D13). The FB-5 copy is proposed, not approved, and not built |
| F05 | Specialist screens | Blocks the task | The next action has no link; the way on is a link at the foot of a 5,937px page | Deferred to the owner (D8; FB-11) |
| F06 | List read error | Blocks the task | The error block sits about 2,000px below the message | Deferred to the owner (D1). It depends on the list order; the final review found the block still below the briefing |
| F07 | Denials, unknown URLs, route errors | Blocks the task | No heading, owner or next action; Try again offered for a denial; an unknown URL shows My cases | Not planned (FB-5). The route-level copy was left out of FB-6 |
| F08 | Assistant proposals | Blocks the task | The only content is the server sentence "Durable SQL is required; use the ordinary case/manual route." | Deferred (backend change) (FB-5 server copy) |
| F09 | Home case page | Blocks the task | "Recording a new version is a staff action through the API" | Deferred to the owner (D7). The wording is unchanged |
| F10 | Time capture | Confuses | Case reference, Minutes and Activity had no visible label | Done in this change (FB-1) |
| F11 | Sign-in, first visit | Confuses | A first visit showed "Your session has ended"; no orientation or way back | Done in this change (FB-6) |
| F12 | Every list page | Confuses | About 370 characters of status text above each list, eight lines at 390px | Not planned (FB-7) |
| F13 | Button rows | Confuses | Rows of equal-weight buttons; navigation styled as buttons | Done in part (FB-1). The work-order row has one primary button, though its blocks still change height when a hint or an error differs (application N5 below); the rest of FB-3 is not built; the three AI draft buttons stay equal by design (D11) |
| F14 | Case cards, picker rows, home case, building, progress | Confuses | 822 run-on paragraphs of label and value facts at 1440px | Not planned (FB-4). The final review counted 695 after trimmed copy; the structure is unchanged |
| F15 | Many screens | Confuses | Raw times, doubled full stops, record paths, raw braces, a stray "null", a repeated phrase | Done in part (FB-9). The null, braces, repeats and most doubled stops are fixed, and the programme funnel's as-of time is formatted like the neighbouring panels; raw ISO times elsewhere and record paths remain (FB-4, D14) and the capacity evidence cell still doubles a stop |
| F16 | Specialist screens | Confuses | The home picker takes 5,452px of a 5,937px page | Deferred to the owner (D8) |
| F17 | Journey-stage panel | Confuses | Stages numbered twice; the same refusal up to seven times | Done in this change (FB-9) |
| F18 | Work list, overview, handoff screen, chat | Confuses | Research and governance wording shown to staff | Deferred to the owner (D5) |
| F19 | Headings | Confuses | The first heading on lists was "Filter"; duplicate headings; a skipped level; no heading on one denial | Done in part (FB-6). Work lists start with the h1 and name the list with a second-level heading; the duplicate headings on two specialist screens, the heading level on the assistant card and the missing heading on the capacity denial are not built |
| F20 | Document title | Confuses | One title on all 115 variants | Done in this change (FB-6). The title is the page heading, a vertical bar and Zava Forward; on the case screen the safety flag text is left out of it |
| F21 | Header bar | Confuses | 341px high at 390px for 13 links | Deferred to the owner (D2) |
| F22 | Navigation labels | Confuses | Eight labels differ from their page titles; Aftercare opens different pages by role | Deferred to the owner (D2, D3). The tab title now repeats the page heading, so the mismatch also shows in the browser tab (final review) |
| F23 | Aftercare | Confuses | Resident voice shown to staff; three jobs on one page; ragged field widths | Done in part (FB-1). Widths only, equal in the final review; voice and layout remain (D3) |
| F24 | Time capture navigation item | Confuses | Present for every staff role and ends in a configuration dead end | Deferred to the owner (D4) |
| F25 | Forms on cards | Confuses | Fields keep their intrinsic width | Done in part (FB-1). Forms built with the field block share one width rule, and the final review found widths equal in 12 of 13 card or row groups; the coordinator filter card still has unequal control widths at 1440px (cosmetic); older forms keep their own widths |
| F26 | Overview sensor filter, staff intake | Confuses | The checkbox sat above its label | Done in this change (FB-2) |
| F27 | Overview map | Confuses | "Show these as a list" always opens All cases and drops the chosen filter | Deferred to the owner (D9) |
| F28 | Overview: sensor data | Confuses | Telemetry only in the map popup; no count of homes with stale or offline sensors | Deferred (backend change) (D6) |
| F29 | Employee chat | Confuses | Composer boxes unlabelled; Attach and Voice permanently disabled; "Open a case first." has no link | Done in part (FB-1, FB-8). Labels, a composer that takes more of a narrow panel at 600px and below (the whole Attach and Voice explanation shows at 390 by 800; at 390 by 700 it is still too short for the full line) and launcher clearance at 600px and below. Attach and Voice stay disabled and "Open a case first." has no link |
| F30 | Coordinator flow | Confuses | Twelve fields; the cutoff is a typed ISO timestamp | Deferred to the owner (D10) |
| F31 | Visits | Confuses | One run-on line, the phone as plain text, a bare "No booked visits." | Not planned (FB-4, FB-5) |
| F32 | Progress, Closed cases | Confuses | Five paragraphs before the charts; a wall of download text | Deferred to the owner (D13) |
| F33 | Spreadsheet check, coordinator, building, home case | Confuses | The context line said "Case workspace" | Done in this change (FB-6) |
| F34 | Links in lists, tables and map lists; specialist screen buttons | Polish | 111 targets below the app's own minimum height | Done in this change (FB-8). In the coordinator flow, count links in tables keep a compact minimum size and count links inside sentences stay inline. The overview map list now scrolls at 390px where it nearly fitted (application N10 below) |
| F35 | Links in the page body | Polish | 421 of 1,343 link instances in browser blue | Done in this change (FB-8) |
| F36 | After a route change | Polish | Mouse navigation shows the focus frame around the page | Done in this change, on the owner's request of 2026-11-20 (D12 is settled in the owner's favour). The frame around the main container is gone for mouse navigation, keyboard navigation and the skip link, and focus still moves there. The accessibility review of the choice is pending |
| F37 | Brand lockup, sign-in | Polish | The logo alternative repeated the visible name; no theme colour; sign-in with no orientation | Done in this change (FB-6). The password and Microsoft sign-in cards carry the same orienting sentence and a "Back to the welcome page" link; Microsoft sign-in was read in code and not run |
| F38 | Number columns | Polish | Tabular figures on three tables only | Done in this change (FB-8) |
| F39 | Metadata and flags | Polish | 334 text elements smaller than body text | Deferred to the owner (D13) |
| F40 | Capacity controls | Polish | Disabled pager buttons with one page; Withdraw acts at once | Not planned (FB-3) for the pager; Deferred to the owner (D11) for Withdraw |

### Backend changes identified and not made

* The server's advisory sentence with an em dash, and sensor sentences that name a route or say "Durable SQL is required" (F17). The case screen replaces them with client copy.
* The assistant proposals sentence (F08).
* A damp-and-mould watch. `sensor_view.advisory` computes one, but `annotate` in `sensor_badges.py` sets a fixed advisory sentence before the payload reaches the page. Showing it needs a backend change and an owner decision; no alert is invented from thresholds.
* One offline rule shared by the map and the case screen. The case payload gives fresh or stale only, so the case screen copies the 24-hour rule from the map code and a test pins the copy; a payload field would replace the copy. The wording still differs: the case tab says "Sensor may be offline (no reading for over 24 hours)", as its alert does, and the server's map label says "Sensor offline".
* An overview aggregate for homes with stale or offline sensors (F28, D6).

## Second pass (final reviews)

After the build was committed, each designer scored it against the acceptance criteria of their own report. Both reviews read the build as it stood before the polish commits that followed, and neither ran again afterwards. The scores therefore describe the earlier build, and the tables below say what the polish changed. The case review labels its criteria by specification (A1 to A13, B1 to B10, C1 to C14, D1 to D12); those letters are not the application defer items D1 to D14.

| Review | Criteria | Pass | Fail | Not tested |
| --- | --- | --- | --- | --- |
| Case screen | 49 | 47 | 2 | 0 |
| Every other screen | 24 | 22 | 2 | 0 |

* Case criterion C3 failed. A muted sentence came before the status line in every Home sensors state, and the criterion says the status line comes first. The polish moved the status line first.
* Case criterion C7 failed. The Home sensors tab held none of the forbidden internal words, but the AI tab showed the server sentence "Durable SQL is required; use the ordinary case/manual route." on a JSON store. The AI tab is out of scope for this change (R1 below).
* Application criterion 1.5 failed. The coordinator filter card has unequal control widths at 1440px. The effect is cosmetic and it is not fixed.
* Application criterion 9.1 failed. The copy scan still found raw ISO times (347 on main, 352 on the reviewed build, five of them from the programme funnel panel, which the polish then formatted) and two doubled full stops (269 on main), one of them in the capacity evidence cell. Timestamp formatting was not in the batch.

The case review judged the four reported defects resolved at every width it measured, from 1440 to 320px. The application review counted, on the build it read, no control without a visible label (8 on main), no page with the default tab title (115 of 115 on main) and no link in the page body in browser blue (421 of 1,343 on main). All of these are Observed in Chromium on synthetic data. No person used the product.

### New defects found by the final reviews

The case review logged 11 (two confuse, nine polish). The polish commits fixed eight and left three.

| ID | Screen | Finding | Outcome |
| --- | --- | --- | --- |
| N1 | Closed case summary | "None. A manager can reopen this case." and "No recorded blockers." sat beside Open next action and See all blockers buttons | Fixed by the polish. A closed case offers neither button, and See all blockers shows only for an open case that has blockers |
| N2 | Quality record, handed over | "Held for roles with a recorded need" showed in the record and its aftercare note, with no owner or next action | Fixed by the polish. One held-back sentence is built in `fields.js` and used in the handover card, the record, its previous handover note and its aftercare notes |
| N3 | Home sensors, every state | A muted sentence came before the status line | Fixed by the polish. The status line comes first, then the muted sentence |
| N4 | Home sensors, stale beyond a day | The status said "Sensor offline" while the alert under it said "Sensor may be offline" | Fixed by the polish. The status reads "Sensor may be offline (no reading for over 24 hours)"; the server's map label still says "Sensor offline" |
| N5 | Case screen at 1024px | The tab list wraps to three rows (it was two) and the strip is taller (228.8px against 134.4px for a case with two blocked steps), so the work panel starts about 133px lower | Not fixed. The owner chooses between starting the scrolling row at 1199px instead of 899px and shortening the tab names (CD3) |
| N6 | Narrow case screen after a resize or a turn of the device | The selected tab can sit out of view (1,090px along a 356px row); it is in view on first load | Not fixed. Script reveals the selected tab only on selection and on a label change |
| N7 | Case screen at 320px, AI tab selected | The long AI tab label ("AI assistance (count unavailable)") does not fit the row | Not fixed |
| N8 | Handover, receiver | The receiver read "Offered to {name}" and "What they are asked to do" about themselves | Fixed by the polish. "Offered to you, waiting for your answer" and "What you are asked to do" |
| N9 | Handover, after accepting | The button said "Complete handoff" while the card says handover everywhere else | Fixed by the polish. "Complete the handover" |
| N10 | Handover forms | A missing field said "... Owner: you. Next action: ..." while the quality forms used one short sentence | Fixed by the polish. Every validation error is one short sentence (see the decisions below) |
| N11 | Handover suggestions | "1 open cases (team average 1)" | Fixed by the polish, in the sentence built by `recommend_handover` in `src/core/src/zava_forward/core/insights.py` |

The application review logged 11 (three confuse, eight polish). The polish commits fixed eight, fixed one in part and left two.

| ID | Screen | Finding | Outcome |
| --- | --- | --- | --- |
| N1 | Work lists | After the h1 moved up, the case list followed the last second-level heading of the briefing with nothing naming it | Fixed by the polish. A second-level heading, "My open cases" or "All open cases", comes before the results |
| N2 | Case screen tab title and heading | The tab title ran the name and "Safety issue open" together, and a stray "0" followed the name when no safety issue was open (it also exists on main) | Fixed by the polish. The title leaves the flag text out and the heading no longer prints the 0 |
| N3 | Employee chat composer at 390 by 800 | The explanation for the disabled Attach and Voice buttons was cut after one line | Fixed in part. At 600px and below the composer can take more of the panel and the whole explanation shows at 390 by 800; at 390 by 700 it is still too short for the full line |
| N4 | Work lists | The new title row sat flush against the filter and the briefing | Fixed by the polish. The title row keeps a space below it |
| N5 | Time capture and the capacity work-order row | A block without a hint puts its label lower than its neighbours, and an error under one control pushes that block's label up and the Save button out of line | Not fixed |
| N6 | Overview sensor filter and staff intake checkboxes | The hint started under the box, not under the label text | Fixed by the polish. The label carries the spacing, so the whole row is clickable and the hint lines up under the label text |
| N7 | Coordinator flow | The compact link rule reached count links inside sentences and grew those lines, and nine single-digit count links were still narrow | Fixed by the polish. The rule is limited to links in tables, with a minimum width and centred text; count links in sentences stay inline |
| N8 | Programme queue, selected home | The funnel panel printed its as-of time as a raw ISO timestamp | Fixed by the polish. It is formatted like the other panels |
| N9 | Sign-in, Microsoft mode (read in code, not run) | The card said "Back to welcome", had no orienting sentence and showed its neutral instruction in the error style | Fixed by the polish. It matches the password card, and the error style is for errors only |
| N10 | Overview map list at 390px | The taller links make the list scroll where it nearly fitted, so the fifth home is cut off | Not fixed |
| N11 | Every page | About 100px of empty space ended every page, including at 1440px | Fixed by the polish. The space applies at 600px and below |

The application review also found, outside its scope and not counted, that a manager opening the case of a home whose invoice has no kind got "Workspace unavailable". The fault is identical on main, and the reviewer judged it probably a gap in the synthetic data. The polish fixed it defensively in `panels.js`: a missing kind reads as empty.

### Residual issues the case review found that the build did not touch

These six are unchanged by the polish.

* R1: the AI tab shows "Durable SQL is required; use the ordinary case/manual route." on a JSON store, the cause of the C7 failure.
* R2: the summary says "AI review count unavailable" for an account that is not linked, without naming the cause (case F18, CD11).
* R3: the tab panel still scrolls inside the page, and on a phone the Quality tab is 4,214px of content in a 591px frame (case F21, CD8).
* R4: the handover card is the last block of the Quality tab (CD1).
* R5: the summary block is 541 to 668px tall at 390px (case F19, CD7).
* R6: the waiting glyph draws as an empty box in the review render (case F20, CD12).

### How the application review graded the first-pass findings

The application review counted F02, F03, F10, F11, F17, F20, F25, F26, F33, F34, F35, F37 and F38 as fixed; F01, F06, F13, F14, F15, F19, F23 and F29 as partly fixed; and the other 19 as unchanged by decision. The tables above differ in three places. F25 reads Done in part here because of the coordinator filter card. F06 and F14 read as deferred and not planned here because the cause or the structure was not touched, where the review counted the h1 move and the trimmed copy as partial. F36, which the review left unchanged, is now settled by the owner's request.

The polish settled one owner decision, the focus frame on the main container (F36, D12). CD1 to CD12 and D1 to D14 are otherwise unchanged, and CD3 now also carries the 1024px width choice from case N5.

## Decisions taken in this change on the owner's behalf

Each of these was chosen so the work could proceed, except the focus frame, which the owner asked for. Each needs the owner's confirmation or reversal; for the focus frame the open step is the accessibility review.

| Decision | What the code does now | Basis | Owner to confirm |
| --- | --- | --- | --- |
| Handoff stays in the Quality and handover tab | The merged handover card sits in the Quality and handover tab; `nextTab` still sends staff there when the next action is a handoff | The case report treats a move as an owner decision, and several checks click that tab. Assumed that stable names are lower risk | Keep or move (CD1) |
| Three columns from 900 to 1199px | The strip is three columns by two rows in that range and six columns above it | Observed: six narrow cards broke "Assessment" mid-word at 1024 and 900px. Assumed that two rows of three read better | Accept, or return to six columns (CD2) |
| One-line "Why blocked" on step cards | Step cards show the fixed words; the summary button keeps the first sentence of the reason; the popover and accessible name are unchanged | Observed: five letters and an ellipsis said nothing. Assumed that a fixed label is easier to scan | Fixed label or clipped sentence (CD2) |
| A single scrolling tab row at 899px and below | The tab buttons sit in a plain inner wrapper that scrolls sideways; at 900px and above the wrapper takes no box and the tabs wrap as before. The wrapper has no name and no focus stop, and script scrolls the selected tab into view along the row | Observed: the tab list wrapped to eight rows at 390px. The design text gives two narrow-screen rules (scroll sideways in one section, prefer wrapping in another) and asked for a named focusable area, which this is not. Needs a screen-reader pass | Which rule governs (CD3); the screen-reader pass is routed to the accessibility skill |
| Required and optional in visible labels | `Fields.fieldBlock` appends "(required)" or "(optional)" to the label text; required wins if both are set; a field with neither flag stays bare | The content standard has no rule. The aftercare form already used "(required)" in its label. Assumed that marking reduces refusals | Confirm the rule proposed in the content standard (CD5) |
| "Held back for your role" wording | The server placeholder "Held for roles with a recorded need" is replaced on screen by "Held back for your role. Owner: {name}. Next action: ask {name} ...", or the person who recorded it when no name is known. `Fields.heldBack` builds the sentence once for the handover card, a handed-over quality record, its previous handover note and its aftercare notes. A test pins the match to both server constants | Observed: the placeholder gave no owner or next action, and the first build fixed it in the handover card only (case N2). No change to who may read is proposed | Wording, and whether a receiver should see the text (CD6) |
| No palette change | Every rule added uses existing tokens; the app keeps its Fluent 2 tokens and teal brand. The deck-derived palette stays on the public welcome page only | Reported: the owner fixed Fluent 2 and the teal brand, and the design system records the welcome page as the one exception | Confirm |
| Page titles | The tab title is the page heading, a vertical bar and "Zava Forward"; "Sign in" in the same pattern when signed out; the static title when a screen has no heading yet. The safety flag text on the case heading is left out of the title | Observed: one title on all 115 variants, and the first version ran the flag text into the name (application N2). Assumed that people with several tabs open can then tell screens apart | Confirm the format |
| Link colour from existing tokens | Links in the page body use `--brand-d` (hover `--ink`) unless they are buttons, card links or link-styled buttons | Observed: 421 of 1,343 link instances were browser blue | Confirm; contrast on each background is routed to the accessibility skill |
| Validation errors are one short sentence | A missing required field gets one sentence that says the reason and the fix, for example "Enter the case reference, for example ZF-1." or "Say where this change came from."; the hint under the field stays. The reason, Owner and Next action form is kept for blocked or refused actions, and server refusals keep their own wording | Observed: the first build used the three-part form on handover and time capture fields and the short form on the quality card (case N10). The content standard already asks for the reason and the fix in one sentence for other validation errors | Confirm the split (CD5) |
| No focus frame around the main container | The focus rule for elements with tabindex -1 leaves out the main container, and one override, `#app:focus-visible`, sets its outline colour to transparent and removes its box shadow. Focus still moves to the main container after a route change and from the skip link. Links, buttons, fields and the case tab panel headings keep their frame. The outline stays defined, only transparent, so forced-colours mode can still draw one | Reported: the owner asked on 2026-11-20, with a screenshot of a thick frame around the whole content area. Mouse navigation, keyboard navigation and the skip link all arrive there, and Chromium treats the container as keyboard-focused after Enter on a link, so the change took two steps | The accessibility review of this choice is pending. It settles F36 and D12 in the owner's favour. How forced-colours mode draws the outline was not checked |

## Owner decisions still open

### Case screen (CD1 to CD12)

| ID | Decision | What is needed |
| --- | --- | --- |
| CD1 | Where handoff lives | Keep it in the Quality and handover tab or schedule a move. A move touches `nextTab`, the checks that open that tab and the step links |
| CD2 | Strip layout and card text | Confirm three columns from 900 to 1199px and the "Why blocked" label, or return to six columns and a clipped reason |
| CD3 | Narrow-screen tab rule | Say which of the two rules in the case workspace design governs, scroll sideways or wrap, and name who runs the screen-reader pass on the scrolling row. The final review adds a width choice (case N5): start the scrolling row at 1199px instead of 899px, or shorten the tab names, because at 1024px the tab list now wraps to three rows |
| CD4 | Owners named in the new copy | The roster owner confirms or replaces "the quality team", "your team manager", "application support", "a Quality Inspector or a Retrofit Programme Manager" and "the resident's consent owner" |
| CD5 | Required and optional rule, and the field error split | Confirm the rule proposed in the [content standard](./content-standard.md#staff-workbench-wording-and-the-required-and-optional-rule-2026-11-20), and confirm the split the code now follows: one short sentence for a validation error, and reason, owner and next action for a blocked or refused action |
| CD6 | Held-back text | Decide whether the placeholder and its replacement wording are intended, whether a receiver should see the next action and note, and whether the server wording changes. No change to who may read is proposed |
| CD7 | Compact summary at 390px | The one-scroll bound was owner-approved. A change needs a find-the-blocker task result first |
| CD8 | The panel's inner scroll | Keep or remove it. An existing browser check protects the attached-tabs design |
| CD9 | Open safety issue | Whether "Raise a safety observation" folds into a closed disclosure while an issue is open. Needs the Building Safety Liaison's view and a read of the safety checks |
| CD10 | Pre-filling source, version and reason | Governance: these fields are meant to be recorded by a person. Owner decision |
| CD11 | AI tab label and summary wording | Coordinate with the owner of the AI tab; name the cause when an account is not linked |
| CD12 | Pictograms and the waiting glyph | Brand and font decision of low value |

### Application (D1 to D14)

| ID | Decision | What is needed |
| --- | --- | --- |
| D1 | Work list order and how prominent the AI briefing and priority suggestion are | They are headline demonstration features with tested states, so moving them changes the demo story |
| D2 | Header bar below tablet width; navigation labels against page titles | The manifest `152-ia-v1` is owner-decided and tests pin the rules and labels |
| D3 | Aftercare: title and voice, one page or three, which role sees what | Server copy and a role question |
| D4 | Time capture in the navigation before it is enabled | Information architecture |
| D5 | Internal research and governance wording shown to staff | The wording records owner decisions and tests pin it |
| D6 | A count or list of homes with stale or offline sensors on Overview | A server aggregate that the stats call does not return |
| D7 | Home case: a "Record a new version" button or wording only | A write action |
| D8 | Specialist screens: a compact home picker, and whether read-only screens may carry plain links to the case workspace | Read-only boundary wording and a layout rework |
| D9 | Filters held in the URL against the decided "return reloads first page"; whether Overview's list link carries the chosen filter | Recorded as decided in the manifest |
| D10 | Coordinator flow: date and time inputs for the cutoff, and the default field set | Analyst workflow |
| D11 | AI draft review: three equal-weight buttons are deliberate neutrality; confirmation or undo for Withdraw | Approval-boundary design |
| D12 | The focus frame around the page after a route change | Settled by the owner's request of 2026-11-20: the frame is removed (see the decisions above). The accessibility review of the choice is pending, including how forced-colours mode draws the outline that stays defined; the focus guard test must stay green |
| D13 | Wording under the named-human content review: the My cases sentence (tested), the owners in the empty-state copy, the programme queue failure sentence, the placement of Progress and Closed cases prose, small-text sizes | The [content standard](./content-standard.md) records that the named review has not run |
| D14 | How internal record paths such as `case:ZF-1/hazards/0` appear in Source lines | A per-record display mapping and wording |

## Findings that are not UX defects

The owner's third screenshot shows "Current staff role has changed or been revoked." in the Home sensors panel. That is an identity setup fact, not a layout or wording defect.

* Observed in code: `authorize()` in `src/core/src/zava_forward/core/assistants.py` looks the signed-in user up in the staff table by email. A signed-in Entra person with no staff-list entry carries a derived address ending `@entra.invalid` (`email_for` in `identity.py`). No staff row matches it, so the call is refused with that sentence. The sensor read (`GET /api/cases/{id}/sensors`) and the AI assistance calls both pass through `authorize()`, so such a person can neither read sensor readings nor use AI assistance.
* Reported: the live demo showed the message. Observed: the reviewers reproduced the state by intercepting the response, not through a live Entra sign-in.
* What changed: the Home sensors tab now says so in plain words with an owner and a next action: "Your staff account is not linked to your role, so home readings are hidden. Owner: your team manager. Next action: ask them to check that your account is on the staff list with your role, then refresh this page. Until then, use the ordinary quality check." The AI item in the case summary and the AI tab keep their generic "AI assistance unavailable" wording (F18, CD11).
* Linking an account to a staff row is an identity administration step that needs the owner's approval. This change does not touch authorisation, the staff table or sign-in.

## Validation

These are engineering checks on constructed, synthetic data. They show that the code does what the specifications say. They are not user validation, a conformance result or an assistive-technology run.

New unit and mini-DOM tests, counted from the test files:

| File | Tests | Covers |
| --- | --- | --- |
| `test_fields_helper.py` | 10 | The labelled-field helper and its styles |
| `test_quality_decisions_ui.py` | 13 | Quality record cards, labels, validation, refusals, stable names, held-back notes |
| `test_handover_ux.py` | 19 | The handover card, offers, notices, one-sentence validation, the receiver's own wording, the shared held-back sentence and "1 open case" |
| `test_home_sensors_tab.py` | 21 | Tab order, states, alert copy, status line before the advisory sentence, label count, tab row |
| `test_app_wide_ux.py` | 32 | FB-1, FB-2, FB-6, FB-8, FB-9 and FB-10; two FB-8 tests load the real stylesheet in Chromium and skip when it is missing |
| `test_polish_ux.py` | 14 | The polish after the final reviews: title row spacing, check rows, coordinator links, the chat composer, the page end, a missing invoice kind and the focus frame on the main container. The stylesheet cases run the shipped CSS and chat widget in Chromium on small constructed pages |
| `test_case_journey.py`, `test_static_assets.py`, `test_epic149_role_workbench_heading_hierarchy.py` | 5 added | The closed-case summary (2); `fields.js` linked, versioned, served and packaged (1); each work list names its results and the case heading has no stray 0 (2) |

That is 114 new tests. Nineteen existing test files were edited so that counts and wording follow the change, for example the count of sites that set the invalid state, the content audit file list, the strip and tab assertions and the heading check, whose list of recorded h1-first gaps is now empty. The nine modules above ran 157 tests with no failure and none skipped on the branch head when this page was last updated (Chromium and Node available).

Browser checks (Chromium only): `case_view_ux_browser_check.py` (strip geometry, header links, closed summary), `case_journey_browser_check.py` (ten tabs, closed summary, the offer path), `quality_sensors_browser_check.py` (the new tab), `provenance_browser_check.py`, `workbench_browser_check.py`, `procurement_browser_check.py` and `atlas_tensions_browser_check.py` were edited for the new structure or wording. The polish edited the case view, provenance and map checks again for the new names. The implementer's final runs on the integrated branch passed with no failing assertion in the case view check (153 passing), the case journey check (420), the design system check (160), the regulatory UX check (21 browser states) and the employee acceptance check (3 tests). Those run logs are session files and are not retained in the repository, and the results predate the polish commits; this page records no browser-check result after them.

FB-8 on the real stylesheet: the Chromium test pins the link colour, the compact height of links in tables, map lists and disclosure lists, the unchanged size of buttons, jump links and the map attribution, tabular figures and the page-end clearance at 600px and below. Before the polish the implementer measured 23 routes at 1440 and 390px (session log): no listed link below the compact height and no overlap between the last card and the chat launcher on All cases, at a time when the clearance applied at every width. The application review then measured the same rules on its 115 variants: links in the compact contexts under the minimum fell from 58 of 90 on main to 0 at 1440px and from 24 of 90 to 0 at 390px. The 111 shortfalls of the first review were not re-counted on all 49 URLs.

Failures that exist identically on the base commit `5e7af3e01`: the capacity, procurement (needs a SQL store), loading and briefing, workspace scripts, atlas tensions and specialist keyboard browser checks. The map fullscreen check has one sub-pixel assertion that fails intermittently. Reported by the implementer from base-commit runs; those logs are not retained. The application review ran the repository's browser checks from snapshots of both builds and found six failures that repeat with identical messages on main. One is the chat widget check ("Focused control is obscured or outside the viewport"), so that check can neither confirm nor clear the composer finding (application N3).

The whole API unit suite is recorded in the next subsection.

### Final checks on the pull request head

* Full API unit suite on the final tree before the last small fix: 4,381 tests OK, 662 skipped (Chromium and Node available).
* The browser checks run as the workflow runs them, all with no failing line: the employee acceptance check (3 tests), the design system check (160 passing), the regulatory UX check with axe (21 browser states), the case journey check with axe (420 passing) and the chat panel test. The case view check (158 passing) also ran.
* Hosted CI found two core checks that the local API run does not cover, and the last commit fixed them: the scenario manifest pins the hash of the workbench browser check, which the handover change had edited, and the Atlas screen check compares the journey stage names with the walkthrough, typed numbers included (the data table keeps them and the screen strips them, so the list is numbered once). A local run of the whole core suite then showed only environment failures that CI does not have (the Azure SDK is not installed here, and one test needs an installed package path).
* Hosted CI on the head pushed at 21:43Z (the last code change): all ten `Source projects CI` jobs passed, including `src-api` (unit tests, lint, type check, the browser checks, the image build, the container controls and the vulnerability gate).

### Live demo deployment (2026-11-20)

* Image: built from the pull request head (the `src/` tree is identical), checked with `src/check-container.py api` and a 15-step smoke test of the new screens, then pushed by digest `sha256:b197cf9dca5191c5eb6597deec7f46c900cc96424070e5e351681505c2d20e81` through a short registry window. The window was closed and the registry read back as found: public access off, default action `Allow`, no IP rules, exports off. A first read showed the default action had changed from `Deny` since the morning (another session); the window script forces `Deny` while open, so it was set back to `Allow`.
* App: `ca-cutover-test-demo-api` was updated by hand, not through Bicep. The image was set by digest, and `ZF_RESIDENT_SITE_URL` was set again because the migration's template (revision 35, created 19:09Z) had dropped it.
* What failed: revision 36 (this image) and revision 35 (the previous image) both exit with code 2 about a second after the container starts, three times, and then fail to activate. `server.py` exits with code 2 when the in-process container hardening guard refuses to start, and the migration's template sets `ZF_CONTAINER_HARDENING=enforced` and adds two `EmptyDir` mounts. The same image starts under plain Docker with the guard enforced, so the refusal is specific to Azure Container Apps; the guard's message was not retained, so which check refuses is not known.
* What was done: on the owner's instruction `ZF_CONTAINER_HARDENING=off` was set on the app. Revision 37 is Running and Healthy with all traffic. The container still runs as the image's non-root user. A later Bicep deployment would set the variable back to `enforced` and drop `ZF_RESIDENT_SITE_URL` again, and the app would then fail to start until the guard is fixed for Container Apps.
* Checked live from outside: the health endpoint, the welcome page and its resident link, the served stylesheet (it carries the new rules), the sign-in redirect to Microsoft, and that `/app` and `/api/cases` refuse an unauthenticated request. Not checked live: the signed-in screens, which need a Microsoft sign-in. The owner's account is not linked to a staff row, so the Home sensors tab shows its "not linked" state and AI assistance stays unavailable for that account.
* Rollback to the previous screens: `az containerapp update -n ca-cutover-test-demo-api -g ama --image crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:50091c6d8282e84f62662506d39c53cdd198fcc58fd0cb82ff3eb3079f70ad37`. To turn the guard back on once its refusal is fixed: `az containerapp update -n ca-cutover-test-demo-api -g ama --set-env-vars ZF_CONTAINER_HARDENING=enforced`.

## Not validated

* No user, staff member or resident tested any layout or wording. No named human reviewed the new wording (see D13 and the [content standard](./content-standard.md)).
* The final reviews read the build before the polish commits and did not run again. The polish was checked by the unit and mini-DOM tests listed above, which include Chromium checks of the shipped stylesheets on constructed pages, and not by a repeat of the designers' measurements. The 390 by 700 composer height, the wide-screen effect of the narrower page-end space and the corrected tab titles were not measured on the real application after the polish.
* The browser checks and the reviews used Chromium only. Native popovers, the `:where()` and `:is()` selectors and the scrolling tab row were not seen in another browser, and no real device was used.
* Real SQL-backed sensor readings, a live Entra sign-in and the resident demo site were not exercised.
* The review made no accessibility verdict. These items are routed to the accessibility skill and were not run:
  * Name and label agreement for every new button and field, including the measure suffix on the decision buttons and the removed hidden name on the measure drop-down.
  * Focus after each redraw (record heading, handover status line, offer form heading) and focus not hidden behind the fixed chat launcher.
  * What a screen reader announces for the "Recorded:" line, the tab label count change and the handover status, which had three separate announcement areas in the old card.
  * The link between each inline error and its field.
  * Colour independence, forced-colours and reduced-motion rendering of the new status lines, alert cards and strip states.
  * Control size for full-width buttons and tab buttons at 390 and 320px.
  * Reflow and zoom for the scrolling tab row, the forms and the sensor tables.
  * Table structure and keyboard reach for the sensor tables and their scroll areas.
  * From the application review: the length of whole-card link names on the work list and home picker; the removal of the focus frame around the main container, which the owner requested (D12 is settled in the owner's favour), including how forced-colours mode draws the outline that stays defined; repeated section labels and an information panel nested in a card on four screens; the length and politeness of the status text announced on every filter change; name-in-label and form probes on the screens that gained labels; announcement of the new page titles; and keyboard order with the chat panel docked at 390 and 1024px.
* The [WCAG baseline status section](./wcag-conformance-baseline.md#staff-workbench-ux-update-status-2026-11-20) records what changed in accessibility behaviour and what was not run. No conformance is claimed.

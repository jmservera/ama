---
title: Assistive-technology, consent and Fluent/WCAG live re-proof on revisions 0000054 and 0000026 (Refs #619)
description: Comparison of each #619 acceptance criterion with main and the live demo revisions on 2026-11-23, with the 200 percent text finding assessed and a per-criterion proven, unproven and owner-gated result
ms.date: 2026-11-23
ms.topic: reference
---

Refs #619 (carried over from #550 and #552). This repeats [the 2026-11-22 record](./issue-619-live-at-consent-evidence-2026-11-22.md) against live revisions `ca-cutover-test-demo-api--0000054` and `ca-resident-demo--0000026` and decides whether the one code observation from that record is a real gap. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 waive person-run assistive-technology testing, DPO and Legal approval and billing reconciliation for the demo. No Azure resource was created or changed and nothing needs deleting.

## Main versus live

* Both revisions were created on 2026-11-22 between 23:14:23 and 23:14:37 UTC (`az containerapp revision show`).
* The last `src/` commit that touches web or resident code on main is `a6ba1956db` (2026-11-22 23:05 UTC). The only later `src/` commit, `10cad2e413`, changes two test files. Main and the live revisions therefore carry the same application code for these criteria.

## Method

* Playwright Chromium, 1366 by 900 viewport, run on 2026-11-23 against `ca-cutover-test-demo-api` (employee) and `ca-resident-demo` (resident). Credentials were read from the owner's files at run time and never printed.
* axe-core 4.10.3 (wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa). Drivers, redacted JSON and screenshots are under `.copilot-tracking/evidence/2026-11-23/issue-619-live/` (`employee_proof.py`, `employee_followup.py`, `resident_proof.py`, `text_scale_proof.py`).
* Local tests (127, all passing): `test_accessibility_baseline`, `test_content_standard`, `test_chat_consent_boundary`, `test_resident_sensor_consent`, `test_alert_chat_visit_consent_boundary_215`, `test_chat_panel_accessibility`, `test_resident_screen_wcag`, `test_resident_assistant_api`, `test_resident_aoai`.
* Engineering evidence of markup, focus and geometry only. It is not what a screen reader speaks and not a person's record.

## Observations

| Area | Result on 2026-11-23 | Against 2026-11-22 |
| --- | --- | --- |
| Case view axe | 0 violations, 30 passes; 10 tabs, arrow keys cycle and wrap | Same |
| Blocker disclosure | Enter and Space open, Escape closes, focus returns to the trigger; axe 0 violations | Same |
| Tab walk, 80 stops | Three stops flagged without an indicator. Their accessible name is the page text, so they are the document body at the wrap rather than a control; the date-time input shows a 3 px outline | Same |
| Reflow, case view | No horizontal scroll at 683 by 450 and 320 by 256 | Same |
| Employee chat | Opens by keyboard to a named dialog; axe 0 violations, 20 passes; Escape returns focus; at 320 by 256 Send is reached by Tab and scrolls into view | Same |
| Resident consent | Box unticked; asking without it sends no `/demo/assistant` request and shows "Agree to use your own record for this question first."; box marked invalid and focused | Same |
| Resident answer after consent | HTTP 200, "Summary by rules - AI unavailable: the AI usage limit was reached", 6 sources; axe 0 violations, 21 passes | Same: the guard still holds AI |
| Untick | Log emptied, question cleared, "Record use stopped. Previous answers cleared." | Same |
| Works consent | "Summary by rules - workflow only, no AI used"; agreeing to use the record is stated not to be consent to works | Same |
| Escape, reflow, motion, session | Escape closes and returns focus; no horizontal scroll; no long animation; still signed in after reload | Same |
| Text at 200 percent (root font size) | No horizontal scroll, no control off sideways. The entry area is a 105 px scroll box holding 1124 px; the consent block alone is 765 px, so the question input sits about 1180 px down | Same numbers |

## The 200 percent text observation is not a code gap

The consent block is the 765 px child of the scrolling entry area at 200 percent text; it holds the statement of what own-record data the chat uses, which must stay readable before the question. Raising the composer share from 55 to 80 percent in a live style experiment moved the input only 29 px (from 1180 to 1151). The root-font-size probe is also harsher than WCAG 1.4.4 and 1.4.10 test conditions: a real 200 percent zoom halves the viewport in CSS pixels and was proven to reflow at 683 by 450, and text-only scaling keeps all content and every control reachable by scrolling inside the panel (axe `scrollable-region-focusable` passes). A layout change would trade consent wording or panel size for a small gain, so no `src/` change was made. Recorded as an observation for the production protocol.

## Per-criterion result

| # | Criterion (unticked in #619) | Status | Basis and limit |
| --- | --- | --- | --- |
| 1 | Screen reader testing recorded by a person | Unproven, owner-gated (production build) | No screen reader ran; waived for the demo by the 2026-11-18 decision and tracked in #1907 |
| 2 | Keyboard testing recorded by a person | Engineering proof only; person record unproven | Scripted operation of case tabs, blockers, employee chat and the resident consent journey passed again on live |
| 3 | Zoom testing recorded by a person | Reflow proven by proxy; person record unproven | 683 by 450 and 320 by 256 viewports reflow; 200 percent text keeps all content reachable, assessed above |
| 4 | Consent step proven with a real resident journey | Proven on the synthetic demo; a real resident journey is unproven and owner-gated | Refusal without consent, no request sent, withdrawal clearing, works-consent statement. Real resident, DPO and Legal approval waived for the demo |
| 5 | #550 resident consent step remains before any data is used | Proven for the demo build | No assistant request before the box is ticked on live; `test_missing_or_withdrawn_consent_returns_manual_path_without_a_model_call` passes. A consented AI-generated answer was not observed because the AI usage guard still returns the labelled rules summary |
| 6 | #552 Fluent 2 and WCAG baselines preserved | Partly proven | axe 0 violations on case view, blocker case, employee chat and resident panel; baseline and content-standard tests pass. No Fluent 2 re-audit and no conformance claim |

## Why #619 stays open

Closing needs named people to complete the rows of [production-ux-acceptance-protocol.md](./ux/production-ux-acceptance-protocol.md) with screen readers and real zoom, and a real resident journey under DPO and Legal approval. A pull request refers to the issue with `Refs #619` only.

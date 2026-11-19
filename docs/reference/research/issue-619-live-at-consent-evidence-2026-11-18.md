---
title: Assistive-technology, consent and Fluent/WCAG acceptance live demo evidence (Refs #619)
description: Per-criterion record of what the live synthetic demo proves for the unticked acceptance criteria of issue 619, with the limits that keep person-run assistive-technology testing and a real resident journey production-only
ms.date: 2026-11-18
ms.topic: reference
---

Refs #619 (carried over from #550 and #552). Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive billing reconciliation, DPO and Legal approval and person-run assistive-technology testing for the demo. The production-build rows stay with #1905 to #1908 and the blank record in [production-ux-acceptance-protocol.md](./ux/production-ux-acceptance-protocol.md). No source code changed, no Azure resource was created or changed, and nothing needs deleting.

## Method

* Playwright Chromium, 1366 by 900 desktop viewport, 2026-11-18 11:50 to 12:10 UTC. Employee site `ca-cutover-test-demo-api` (Entra sign-in with the employee test account) and resident site `ca-resident-demo` (shared demo sign-in with the resident test account). Credentials were read at run time from the owner's files and never printed; a literal scan of every retained evidence file for each credential value found no match.
* axe-core 4.10.3 with the tags wcag2a, wcag2aa, wcag21a, wcag21aa and wcag22aa. The same pinned file as the local checks.
* Drivers, redacted JSON outputs and screenshots are under `.copilot-tracking/evidence/2026-11-18/issue-619-live/`: `employee_proof.py`, `employee_followup.py` (with `employee_proof_lib.py`) and `resident_proof.py`.
* "Zoom equivalent" means a Chromium viewport of 683 by 450 CSS px (200 percent of a 1366 by 900 window) and 320 by 256 CSS px (400 percent). It is a viewport size, not a person using browser zoom or text scaling.
* Reused, not repeated: chat keyboard operation and announcements in [issue-159-live-chat-experience-evidence-2026-11-18.md](./issue-159-live-chat-experience-evidence-2026-11-18.md), workbench axe in [issue-151-live-wcag-axe-evidence-2026-11-18.md](./issue-151-live-wcag-axe-evidence-2026-11-18.md).
* Everything below is engineering evidence. It shows markup, focus, geometry and what a screen reader is offered, not what one speaks aloud.

## Observations: employee case view and chat (script A and B subset)

| Step | Result | Evidence |
| --- | --- | --- |
| Case view tab list | One tab list "Case sections" with 9 tabs, each with a panel link; the selected tab is exposed | `employee_proof.json` |
| axe on the case view (1366 px) | 0 violations, 34 passes; on a case with three blockers 0 violations, 35 passes | `employee_proof.json`, `employee_followup.json` |
| Arrow keys on tabs | ArrowRight moves through all 9 tabs and wraps; End goes to History, Home to Overview; Tab from a tab moves to the next control | `employee_proof.json` |
| Blocker disclosure by keyboard | Trigger name "Case: why blocked. Retrofit work is stopped for safety review. Details"; Enter and Space open the popover, Escape closes it and focus returns to the trigger | `employee_followup.json` |
| Tab walk, 80 stops | Focus indicator present on every stop except three flagged samples: two are the "Skip to main content" link at the wrap point and one is `#hz-aware` (a date-time input), which shows a 3 px outline when focused directly. The flags are not shown to be defects | `employee_proof.json`, `employee_followup.json` |
| Reflow, case view | No horizontal scrolling at 683 by 450 or 320 by 256; all 9 tabs still present | `employee_proof.json`, `case-view-320x256.png` |
| Reduced motion | `prefers-reduced-motion: reduce` emulated: no running animation or transition longer than 10 ms on the case view or with the chat open | `employee_proof.json` |
| Chat launcher | Reached by Tab, name "Chat", visible focus indicator, Space opens a `role="dialog"` named "Employee assistant", `aria-expanded` true, focus moves to the dialog heading | `employee_proof.json` |
| axe on the open chat | 0 violations, 20 passes | `employee_proof.json` |
| Chat reflow | At 683 by 450 the input and Send are inside the viewport. At 320 by 256 the panel scrolls inside itself and the input and Send start below the visible area (input top at 430 px in a 256 px viewport); Tab to Send scrolls it into view. At 320 by 450 both are visible. No horizontal scrolling at either size | `employee_followup.json`, `chat-open-320x256.png` |
| Escape | Closes the panel and returns focus to the launcher | `employee_proof.json` |
| Tab cycle | Tab leaves the panel after Send and continues into the page (the panel is not modal); the observed path is Close, About this chat, Chat size, conversation log, question, skill selector, Send, then page content | `employee_proof.json` |

## Observations: resident chat consent journey (script C subset, synthetic resident only)

| Step | Result | Evidence |
| --- | --- | --- |
| Sign-in | The resident test account signs in; session reported as signed in | `resident_proof.json` |
| Launcher | Reached by Tab, name "Chat"; Enter opens a `role="dialog"` named "Help with your case"; focus moves to its heading; the consent checkbox is unticked by default | `resident_proof.json`, `resident-chat-consent-unticked.png` |
| What will be used, before use | Checkbox text: "Use my question and limited own-case details for this chat, including AI when enabled. This is not consent to works." The saved-questions notice is always visible; the advisory note, the AI-or-rules label statement and the "A person can help instead" route sit under the collapsed "About this chat" disclosure | `resident_proof.json` |
| Ask without ticking | No request to `/demo/assistant` was sent (network capture); the alert reads "Agree to use your own record for this question first."; the checkbox is marked invalid and receives focus; the log stays empty | `resident_proof.json` |
| Tick with Space and ask | One `/demo/assistant` request, HTTP 200; label "Summary by rules - AI is not enabled"; 6 sources; the answer entry is added to the log | `resident_proof.json`, `resident-chat-answer-labelled.png` |
| axe on the open panel with an answer | 0 violations, 21 passes | `resident_proof.json` |
| Untick | Log emptied (0 entries), question cleared, status "Record use stopped. Previous answers cleared." | `resident_proof.json` |
| "Have I given consent to the works?" | Label "Summary by rules - workflow only, no AI used"; the answer says works consent is not available in the showcase, that it cannot say whether consent was given, and that agreeing to use the record in chat is not consent to works | `resident_proof.json` |
| Escape, reflow, motion | Escape closes the panel and returns focus to the launcher; no horizontal scrolling at 320 by 256; no long running animation under reduced motion; session still signed in after reload | `resident_proof.json` |

## Per-criterion result

| # | Criterion (unticked in #619) | Status for the demo | Basis and limit |
| --- | --- | --- | --- |
| 1 | Screen reader testing recorded by a person (NVDA with Firefox, VoiceOver with Safari) | Unproven; production-only | No screen reader ran and no person was involved. Person-run testing is waived for the demo. Live regions and names are offered correctly (see observations and #159), which is not what a reader speaks |
| 2 | Keyboard testing recorded by a person | Engineering proof only; person record unproven | Keyboard-only operation of the employee chat, case tabs, blocker disclosure and the resident chat consent journey was driven and passed. A scripted browser is not a named person, so the protocol rows stay `Not run` |
| 3 | Zoom testing recorded by a person (200 percent text, 400 percent zoom) | Partly proven by viewport equivalent; person record unproven | Reflow without horizontal scrolling passes at both sizes on the case view, employee chat and resident page. The employee chat input and Send need scrolling or Tab at 320 by 256. 200 percent text scaling and real browser zoom were not run |
| 4 | Consent step proven with a real resident journey | Proven on the synthetic demo only; real journey unproven | Refusal without consent, no request sent, focus to the checkbox, withdrawal clearing answers and the "not consent to works" statement were all observed with the synthetic resident account. A real resident, DPO and Legal approval and research consent are production requirements and are waived here, so the criterion is not met |
| 5 | #550: the resident consent step remains before any data is used | Proven for the demo build | Network capture shows no assistant request before the checkbox is ticked; the checkbox text states use of the question and own-case details; "About this chat" and the saved-questions notice explain use. The live demo had AI disabled, so consent before AI use was observed only for the rules path |
| 6 | #552: Fluent 2 and WCAG baselines in `docs/reference/research/ux` are preserved | Partly proven | The live pages pass axe WCAG 2.2 A and AA tags with 0 violations on the case view, the open employee chat and the resident panel; focus indicators, native semantics, reduced motion and reflow behave as the baseline requires. These are engineering results and no conformance claim follows. Fluent 2 adoption remains partial per the [design system](./ux/design-system.md) and was not re-audited; owner confirmation of the target level (O-1) is still open |

## Adverse and incidental observations

* The first resident attempts failed: a cold-start timeout, then HTTP 429 from the demo login limiter, which a few earlier retries of this session triggered. The pass followed a wait of more than ten minutes. The limiter is a working control.
* Earlier probe versions mis-targeted selectors (a blocker trigger searched by visible text, which lives in its accessible name; a hidden-element text read) and were corrected. The first resident passing run is superseded by the final run, whose output is retained.
* The live resident app stores typed questions for chat improvement (see the on-page notice); four synthetic questions were asked across two full runs and cannot be deleted from the browser. They contain no personal data.
* The live demo resident chat runs rules only ("AI is not enabled"), so AI labelling for generated text was not observed.

## Why #619 stays open

Closing needs named people to complete the protocol rows with NVDA and VoiceOver, 200 percent text and real zoom, a real resident journey under DPO and Legal approval, and the owner's confirmation of the target level. None of these is needed for the demo and none is claimed here. A pull request refers to the issue with `Refs #619` and no closing keyword.

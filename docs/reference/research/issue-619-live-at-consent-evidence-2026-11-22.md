---
title: Assistive-technology, consent and Fluent/WCAG live demo re-proof (Refs #619)
description: Re-run on 2026-11-22 of the keyboard, axe, reflow and resident consent proofs against the live demo after the web redesigns, with a new text-scaling probe and the per-criterion result
ms.date: 2026-11-22
ms.topic: reference
---

Refs #619 (carried over from #550 and #552). This refreshes [the 2026-11-18 record](./issue-619-live-at-consent-evidence-2026-11-18.md) because staff case screen, chat routing and other web changes landed on main since then (for example #2161 and #2199). Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 waive person-run assistive-technology testing, DPO and Legal approval and billing reconciliation for the demo. No source code changed, no Azure resource was created or changed, and nothing needs deleting.

## Method

* Playwright Chromium, 1366 by 900 viewport, 2026-11-22 23:17 to 23:25 UTC, against `ca-cutover-test-demo-api` (employee) and `ca-resident-demo` (resident). Credentials were read from the owner's files at run time and never printed.
* axe-core 4.10.3 (wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa). Drivers, JSON and screenshots: `.copilot-tracking/evidence/2026-11-22/issue-619-live/` (`employee_proof.py`, `employee_followup.py`, `resident_proof.py`, `text_scale_proof.py`).
* The first `employee_followup.py` run failed with a transient `Failed to fetch` on `/api/cases`; one rerun passed and its output is retained.
* Everything here is engineering evidence of markup, focus and geometry. It is not what a screen reader speaks and not a person's record.

## Observations

| Area | Result on 2026-11-22 | Change since 2026-11-18 |
| --- | --- | --- |
| Case view axe (1366 px) | 0 violations, 30 passes | Passes 34 to 30 after the redesign |
| Case tabs | One tab list with 10 tabs; arrow keys cycle and wrap; Tab moves into the panel | Tab count 9 to 10 (AI assistance added) |
| Blocker disclosure | Enter opens, Escape closes, focus returns to the trigger | Same |
| Tab walk, 80 stops | Only the skip link (twice at the wrap) and a date-time input flagged, as before | Same |
| Reflow, case view | No horizontal scroll at 683 by 450 and 320 by 256; all tabs present | Same |
| Reduced motion | No long-running animation on the case view or chat | Same |
| Employee chat | Launcher by Tab, Space opens a named dialog, focus to heading; axe 0 violations, 20 passes; Escape returns focus to the launcher | Same |
| Employee chat reflow | No horizontal scroll; at 320 by 256 the input and Send are below the visible area and reached by Tab; at 320 by 450 both are visible | Same limit |
| Resident consent | Checkbox unticked by default; asking without ticking sends no `/demo/assistant` request, shows "Agree to use your own record for this question first.", marks the box invalid and focuses it | Same |
| Resident answer | After ticking with Space: HTTP 200, label "Summary by rules - AI unavailable: the AI usage limit was reached", 6 sources; axe 0 violations, 21 passes | New: AI is now attempted and falls back to rules with a visible label |
| Untick | Log emptied, question cleared, "Record use stopped. Previous answers cleared." | Same |
| Works consent question | "Summary by rules - workflow only, no AI used"; says agreeing to use the record is not consent to works | Same |
| Resident Escape, reflow, motion, session | Escape closes and returns focus; no horizontal scroll at 320 by 256; no long animation; signed in after reload | Same |
| Text scaling (new, proxy) | Root font size set to 200 percent on the open resident chat (CSP bypassed in the test context only): no horizontal scroll and no control off-screen sideways, but the chat entry area becomes a 105 px scroll box holding 1124 px of content; the question input sits about 1180 px down, outside the 900 px viewport, reachable only by scrolling within the panel. With WCAG 1.4.12 text spacing the panel stays usable (282 px box, 509 px content) | New. Content is not lost but the 200 percent layout is cramped; recorded as an observation, not fixed |

## Per-criterion result

| # | Criterion (unticked in #619) | Status for the demo | Basis and limit |
| --- | --- | --- | --- |
| 1 | Screen reader testing recorded by a person | Unproven; production-only | No screen reader ran. Names, roles and live regions are offered correctly, which is not what a reader speaks |
| 2 | Keyboard testing recorded by a person | Engineering proof only; person record unproven | Scripted keyboard operation passed on case tabs, blocker disclosure, employee chat and the resident consent journey. A script is not a named person |
| 3 | Zoom testing recorded by a person | Partly proven by proxy; person record unproven | Viewport equivalents of 200 and 400 percent reflow without horizontal scroll. The root-font-size probe found the resident chat entry area cramped at 200 percent text. No real browser zoom or text scaling by a person |
| 4 | Consent step proven with a real resident journey | Proven on the synthetic demo only; real journey unproven | Refusal without consent, no request sent, withdrawal clearing answers and the works-consent statement observed with the synthetic resident. A real resident, DPO and Legal approval are production requirements |
| 5 | #550 the resident consent step remains before any data is used | Proven for the demo build | No assistant request before the checkbox is ticked; the checkbox text states what is used. AI generation was attempted after consent and fell back to labelled rules, so consent before a successful AI answer was not observed |
| 6 | #552 Fluent 2 and WCAG baselines preserved | Partly proven | axe 0 violations on the redesigned case view, employee chat and resident panel. Fluent 2 adoption was not re-audited and no conformance claim follows |

## Why #619 stays open

Closing needs named people to complete the protocol rows in [production-ux-acceptance-protocol.md](./ux/production-ux-acceptance-protocol.md) with screen readers and real zoom, and a real resident journey under DPO and Legal approval. A possible code follow-up is the cramped resident chat entry area at 200 percent text. A pull request refers to the issue with `Refs #619` only.

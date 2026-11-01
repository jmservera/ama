---
title: Today's briefing HAX design note (#531)
description: Dated note mapping the Microsoft HAX Toolkit guidelines to the employee Today's briefing and loading feedback, with evidence and limits
ms.date: 2026-11-01
ms.topic: reference
---

## Scope and status

Design note for the employee workspace Today's briefing (`briefing` in
`src/api/src/zava_forward/api/web/app.js`) and the loading feedback in
`workspace-shell.js`, `index.html` and `async-action.js`. It records which
[HAX Toolkit](https://www.microsoft.com/en-us/haxtoolkit/library/) guidelines
the shipped design applies, from merged work in #538, #581, #604 and #628.

* Authorship: maintainer-authored from source and owner feedback of 2026-10-28.
  The 2026-10-31 UX specialist invocation returned discovery questions, not a
  design note, so this is not a specialist contribution or approval.
* Evidence type: source inspection and constructed-data local browser checks.
  It is not staff usability research, screen-reader or voice-control testing,
  or live employee-site verification (#531 criterion 7 stays unmet).
* Design system: native elements with Fluent 2 derived tokens per the
  [design system](./design-system.md). The
  [Fluent UI React Storybook](https://storybooks.fluentui.dev/react/) informs
  patterns only; no React or framework adoption.

## Guideline mapping

| HAX guideline | Design applied | Where to verify |
| --- | --- | --- |
| G1 Make clear what the system can do | Scope line states permitted open cases and how many are summarised (up to 8); mode choice says whether AI is used | `paint` in `app.js` |
| G2 Make clear how well it can do what it can do | No confidence score is invented; "References show what was cited, not whether the statement is correct" | `paint` |
| G7 Support efficient invocation | Explicit assistance-mode choice and Refresh briefing | `load`, mode control |
| G8 Support efficient dismissal | Hide briefing and Show briefing; no case record changes | `dismiss` |
| G9 Support efficient correction | Outcome buttons Use this draft, Edit this draft, Do not use this draft; text box appears only for the chosen outcome; Cancel review before recording | `choose`, `chooseEdit` |
| G10 Scope services when in doubt | Unverified, stale or unmatched sources disable Use this draft and say to request a fresh draft | `unavailable` |
| G11 Make clear why the system did what it did | "Why these cases" states the fixed ranking; per-statement Sources used lists; mismatches named | `paint` |
| G15 Encourage granular feedback | Visible paragraph on how to correct or give feedback; reasons are kept in the audit log | `data-briefing-feedback` |
| G16 Convey the consequences of user actions | Each review says it records a review only and does not approve works, contact a resident or change a case | `box` legend text |
| G17 Provide global controls | Workflow-only mode via an explicit choice instead of an unclear checkbox | mode control |

## Separating generated, rules-derived and source content

* The label is always present: "AI suggestion, not approved. Not an
  instruction." or "Summary by rules. Not an instruction."
* The heading differs by origin: "Generated briefing and its sources" or
  "Rules-derived summary and its sources".
* Source data is behind each statement's "Sources used (n)" disclosure and
  links to the case record where the case is known. Labels use text, not
  colour alone.

## Loading feedback

* Static startup message in the shell works before scripts load, with a polite
  live region, a slow-load hint and a retry; the script-retry path (#524) states
  retries and persistent failure.
* Per-panel and per-action feedback appears at once and shows a spinner after
  200 ms; reduced motion is respected.

## Unchanged boundaries

Human approval, reason requirement for edits and rejections, server-side
source and review checks, immutable recorded reviews and "not approved, not an
instruction" labelling are unchanged. Content follows the
[plain-language standard](./content-standard.md) and the
[WCAG baseline](./wcag-conformance-baseline.md).

## Evidence

Run on 2026-11-01 against main `efebfc6d`: 73 focused unit tests
(`test_loading_feedback`, `test_workspace_scripts`, `test_ai_tasks`) passed;
`loading_briefing_browser_check` with axe-core 4.10.3 is recorded in
`.copilot-tracking/changes/2026-11-01-issue-531-hax-design-note-changes.md`.
Axe incompletes (colour contrast) remain for human assessment.

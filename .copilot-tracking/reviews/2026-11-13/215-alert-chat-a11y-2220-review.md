---
title: Issue 215 alert and chat WCAG cue review
description: Single post-implementation review of the criterion 3 software and markup slice
ms.date: 2026-11-13
---

## Execution and outcome

Executed once on the local candidate. Outcome: conformant for the stated engineering scope; open items routed as follow-ups, none reopened in this task. This is not an independent human review.

## Assessed boundary

`chat.js` regulatory alert and chat panels, `style.css` rules, new static test, browser check additions and the three documentation notes.

## Findings

| Id | Finding | Severity | Routing |
| --- | --- | --- | --- |
| R1 | Cues are observed in Chromium only; screen reader announcement of the status text and plain explanations is untested | Medium | Follow-up: manual assistive-technology sessions per the regulatory acceptance protocol |
| R2 | Plain-language mode shows explanations, it does not rewrite quoted source excerpts or role guidance paragraphs | Low | Follow-up: content owner decision; quoted evidence must stay verbatim |
| R3 | Criterion 5 staff comprehension is unmet | High (human boundary) | Unclaimed; needs repairs, housing and grants staff |
| R4 | Web guidelines Title Case rule not applied | Info | Owner content standard governs |

## Checks against requirements

* Non-colour cues on every alert state, grounding outcome, doubt route, no-source and unknown coverage: met (static and browser).
* Keyboard: disclosure, Escape with focus restoration, form submit and source links operable in the browser check.
* `aria-invalid` sites unchanged at eight; `test_accessibility_baseline.py` and `test_content_standard.py` green.
* Scope respected; no #232 screens, `infra/` or ranking edits. No checkbox on issue 215 changed.

## Follow-ups (ranked)

1. Run manual keyboard and screen reader sessions (R1), evidence grounded in the acceptance protocol.
2. Staff comprehension testing (R3).
3. Content owner review of plain-language wording (R2).

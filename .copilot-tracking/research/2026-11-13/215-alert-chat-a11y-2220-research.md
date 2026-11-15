---
title: Issue 215 alert and chat non-colour cues, keyboard and plain-language research
description: Research for closing software and markup gaps in criterion 3 of issue 215 (regulatory alerts and home chat)
ms.date: 2026-11-13
---

## Scope

Issue #215 criterion 3 only: `WCAG 2.2 AA: no colour-only status, keyboard operable, plain-language mode`, limited to the regulatory alerts panel and the home regulatory chat panel in `src/api/src/zava_forward/api/web/chat.js` with its CSS and dedicated tests. Criterion 5 (comprehension tested with repairs, housing and grants staff) is a human research boundary and stays unmet and unclaimed. No queue screens (#232), `infra/` or ranking modules are touched.

Research disposition: executed. Prior art: `.copilot-tracking/research/2026-11-13/215-regulatory-ux-a11y-audit-1953-research.md` (audit only, no code change).

## Sources read

* `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md` (constraints: human approval, resident consent, no operational approval claimed), `docs/reference/README.md`, `docs/reference/memory.md` (context only).
* `docs/reference/research/ux/design-system.md`, `wcag-conformance-baseline.md` (rows for status messages, error identification, focus not obscured; every row is partial, no conformance claim), `content-standard.md` (glossary, banned internal terms, ASCII punctuation, reason/owner/next action).
* `.github/skills/web-design-guidelines/SKILL.md`; guideline source fetched 2026-11-13 (decorative icons need `aria-hidden`, async updates need `aria-live`, visible focus, native semantics first). The source's Title Case rule conflicts with the owner plain-language standard, which takes precedence.
* `src/api/README.md` section "Regulatory alert and home chat UX (#215)" and issue criterion audit table.

## Findings (code read 2026-11-13)

`regulatoryAlertsPanel` and `regulatoryChatPanel` (`chat.js`) already give: textual `Status: <result>` headings, plain-language checkbox (default on) toggling `.plain-explanation`, `role="status"` regions, native `details`/`summary` disclosure, labelled form, source links with new-tab warning, doubt button with `aria-disabled`.

Gaps against the three criterion 3 clauses:

| Clause | Gap | Evidence |
| --- | --- | --- |
| No colour-only status | Status is text only; no glyph or shape cue distinguishes alert states (`breach risk`, `attention`, `unknown`, `clear`, `not applicable`), chat grounding outcomes (`answer`, `refused`, `conflict`), the no-source held list item, the doubt sent state, or outage and unknown-coverage notices. The repo pattern elsewhere is a CSS `:before` glyph (`.status-line`, `.flag.danger`). | `chat.js` 330-350, 380-395; `style.css` 104-115, 304-307 |
| Keyboard operable | Disclosure is native and operable, but Escape does not close the chat disclosure and return focus to its summary (the chat widget dialog does). | `chat-widget.js:183`; no Escape handler in `chat.js` |
| Plain-language mode | Alert states have plain text, chat outcomes show the raw word `answer`, `refused` or `conflict` with no plain meaning; no plain text for the no-source state, the doubt route or the unknown-coverage notice. | `chat.js` `meanings`, `show()` |

Constraints found: `test_accessibility_baseline.py` pins eight `aria-invalid` sites; no new site is needed (empty question keeps its status message and focus), so the count must stay eight. `test_content_standard.py` guards internal vocabulary (gate, hold, provenance, trace, envelope, snapshot) in `chat.js`; the new copy must avoid them. Existing browser check `src/api/checks/regulatory_ux_check.py` asserts `.plain-explanation` visibility by toggle.

## Approach

1. Add per-state CSS classes with non-colour glyph and border-style cues (alerts, chat outcomes, no-source, doubt sent, unavailable). Glyphs are generated content with an empty alternative so they are decorative; the visible text stays the accessible name.
2. Add plain-language explanations for chat outcomes, the no-source state, the doubt route and unknown coverage, using the glossary and a reason/owner/next action shape.
3. Add Escape on the chat disclosure that closes it and restores focus to the summary.
4. Add dedicated static tests (new file) and extend the existing browser check for Escape and cue presence. Run the focused tier.

## Not in scope or not claimed

Screen reader announcement, assistive technology testing, manual acceptance, staff comprehension (criterion 5), real owner notification, operational approval, full WCAG conformance.

## Planning Readiness

Ready.

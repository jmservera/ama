---
title: Research - #215 non-colour, keyboard and plain-language matrix
description: Audit of alert cards, doubt route, no-source state and chat live regions across the seven #215 role groups
ms.date: 2026-11-14
ms.topic: reference
---

## Scope

Refs #215, criterion `WCAG 2.2 AA: no colour-only status, keyboard operable, plain-language mode`. Stacked child of `feat/demo-215-alert-chat-wcag-plain-2220` (7b8e1086f). Focused validation tier: test-only, `src/api` web scripts read, none changed.

Read before any web edit: `.github/skills/web-design-guidelines/SKILL.md` (rules fetched 2026-11-14; the first 8000 characters held every rule section, the remainder was not read), `docs/reference/research/ux/design-system.md`, `wcag-conformance-baseline.md`, `content-standard.md`.

## Findings

* Roles: `regulatoryRoleHelp` in `chat.js` covers all 7 staff roles (`STAFF_ROLES`); data handlers share `regulatoryGuidance`; suppliers (contractor view) are not staff roles and take the fallback line. Covered, but previously untested per role.
* Non-colour: every state has a glyph with an empty alternative, a 4px border (dotted for no-source) and visible `Status:` / `Lookup status:` text. Existence was already tested; the matrix adds glyph distinctness and fallback to the unknown cue.
* Plain-language mode: native labelled checkbox, on by default, CSS toggles `.plain-explanation`. Copy is ASCII with no banned internal terms.
* Doubt route: button uses `aria-disabled` (stays focusable), text changes to "Sent to exercise owner; awaiting human review", result announced in `role="status"` with a next step.
* Live regions: `chat.js` has no `role="alert"`. `chat-widget.js` status is `role="status"` + polite (correct). The widget error element is `role="alert"` + `aria-live="polite"`, a mixed pair.

## Routed question: widget error live region

Changing the error pair would break existing checks: `test_chat_widget_focus.py` asserts `aria-live` polite on the error (lines 389, 514) and `test_chat_panel.py` locates it by role `alert`. The element shows only genuine errors, so `role="alert"` is right. Decision: leave `chat-widget.js` and the workbench recipe SHA unchanged; pin the pair in the new matrix and route the choice as a follow-up.

## Gaps

The named modules `test_alert_chat_accessibility` and `test_alert_chat_keyboard_live` did not exist. Static source checks only; no screen reader, assistive technology or comprehension evidence.

Research disposition: executed. Planning Readiness: Ready.

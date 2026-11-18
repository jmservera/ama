---
title: Chat grounding and provenance research
ms.date: 2026-11-14
---

## Scope

Owner demo feedback on case-level chat (Refs #164, #215): unclear answer origin, and unblock or
visit questions withheld with Sources (0).

## Evidence

* `chat_panel.py` already returned `answer_source`, but labels were generic and the withheld
  state had no origin wording; `chat.js` rendered legacy labels.
* Unblock and next-step questions went to the model first. An ungrounded draft only recovered
  through the rules fallback when case facts yielded citations; the rules reply cited recorded
  facts only, never the fixed workflow rules, so a thin case card could still end withheld with
  no sources. Local sweep of all 5 synthetic cases, 6 skills and 3 model modes did not reproduce
  the withheld state, so the live failure is treated as a fragile path, not a confirmed defect.
* Refusal boundaries (approve, consent, contact, diagnose) and the lexical status or figure
  check are separate and must stay unchanged.
* Planning readiness: Ready. Research disposition: executed.

## Sources read

* docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md
* UX design system, WCAG baseline, content standard; redesign and web-design guidelines skills
* chat_panel.py, chat_case_answers.py, chat.js, chat-widget.js, existing chat, accessibility and
  content tests

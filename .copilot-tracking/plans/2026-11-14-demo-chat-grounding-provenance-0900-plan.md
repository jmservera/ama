---
title: Chat grounding and provenance plan
ms.date: 2026-11-14
---

## Plan

* [x] Add citable fixed workflow rules (chat boundary, safety stop sequence, visit consent) to
  the unblock answer.
* [x] Answer unblock questions from the case rules first (no model call, `decision-rules`),
  keeping the strict status or figure withholder for generative replies.
* [x] Add `answer_origin` (`decision_rule`, `generative_model`, `withheld`, `refused`,
  `workflow_message`) and plain-language labels; render "Answer origin:" text in the chat UI.
* [x] Regression tests; update label expectations; README note.
* [x] Focused validation: chat, accessibility, content tests, ruff, mypy.

## Critique (single pass)

The plan keeps refusals, the lexical withholder and read-only behaviour untouched. Decision: use
ASCII labels per repository style. Compatible; applied.

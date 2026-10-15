---
title: Issue 164 chat grounding, evaluation and human-review boundaries research
description: Evidence and planning readiness for the chat evaluation slice
ms.date: 2026-10-15
---

## Disposition

Research executed. Planning Readiness: Ready.

## Evidence

* Issue 164 (parent 157, depends on 108 and 159); owner decision on layout in ADR 0006 (Accepted): all new code in `src/`, `mvp/` holds a pointer only.
* Merged base: `src/core` `chat_panel`, `chat_isolation`, `chat_privacy`, `chatthreads`; `src/agents` `chat.py`, `ai_eval.py`, `evals/registry.json`; `src/api` chat routes and `web/chat.js`.
* Gap found: the panel had no refusal path for approve, decide, consent, contact or diagnose requests, and stale assistant turns stayed in model history after sources were withdrawn.
* `ai_eval` (#108) is single-turn; reuse `build_case`, extend with a multi-turn harness rather than rebuild.
* Memory reaches a prompt only through `ChatIsolation.build_prompt`; `ChatPanel.ask` sends sources and thread history only.

## Constraints

* Synthetic data only; no enablement; portable SQL (no SQL added); pip only; dependency rule enforced by `test_dependency_rule.py`.

## Owner decisions (not decided here)

* Thresholds, accountable reviewer, enablement state, held-out labelled set, live model run, human exercises, review-effort comparison.

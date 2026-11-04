---
title: Issue 164 call authorization research
ms.date: 2026-11-04
---

Refs #164. Research disposition: reused. Planning Readiness: Ready.

* Merged work not redone: #307 (harness, scenarios, refusals), #663 (task registered, disabled), #728 and #737 (claim checks), #837 (rates beside consumption), #923 (approved-threshold checks bound to versions).
* Met per the issue: multi-turn scenarios, out-of-scope refusals, non-AI comparison, consumption reporting.
* Unmet and not implementable offline: approved thresholds and named reviewer (owner decision), frozen independent held-out set, actual-model and human exercises, real-model injection assurance.
* Implementable now: the tokenomics criterion that any actual call stays inside a finite owner-authorised limit. `chat_eval` had no such guard.
* Branch note: requested branch feat/agent-chat-skills-530 already exists on origin with unrelated work; the worktree branch feat/issue-164-r4 (from origin/main) is used instead to allow a non-force push.

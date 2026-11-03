---
title: Issue 222 AI priority cohort research
ms.date: 2026-11-03
---

## Research

Disposition: executed (reused prior evidence plus code reading). Planning Readiness: Ready.

Delivered on main: #636 (core evaluator), #697 (ranking run), #821 (approval binding), #421 (draft manifest). #939 (cohort record in the AI eval report) merged into the stacked branch of #956, not main, so this slice does not touch `ai_eval.py` and stays independent of it.

Gap: the issue covers "deterministic prioritisation and AI tasks". Only the ranking policy runs through cohort evaluation. The AI priority task (`Store.ai_priority`) has no cohort run, no AI-unavailable cohort check and no negative control.

Constraints found: the task caps a recommendation at 10 cases, and the template fallback is a different view from the ranking, so the manual path is the deterministic ranking.

Slice chosen: evaluate the AI priority task over the same 48 paired cases in groups of ten (pairs stay together), with faithful, biased and AI-unavailable modes. Validation tier: focused (not security, infrastructure, SQL or deployment).

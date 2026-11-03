---
title: Issue 164 chat threshold checks research
ms.date: 2026-11-03
---

Disposition: executed. Prior merged work not redone: #307 (golden multi-turn scenarios, refusal, comparison), #663 (task registered disabled, gates), #728 and #737 (claim-level grounding), #837 (outcome rates and consumption reporting).

Gap found: `enablement_decision` only checks that `approved_by` is set. It does not apply approved floors to rates or renew evidence when model, prompt, policy, source or memory versions change (RAI criterion 5). Planning Readiness: Ready.

Unmet and owner-gated: threshold approval and reviewer, held-out set, actual-model and human exercises, authorised limits and prices.

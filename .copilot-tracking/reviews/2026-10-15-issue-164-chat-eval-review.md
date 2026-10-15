---
title: Issue 164 chat evaluation review
description: Single post-implementation review
ms.date: 2026-10-15
---

## Execution and outcome

Executed once. Outcome: conformant with open items (owner decisions and known gaps). Boundary: src/core, src/agents, src/api web and docs.

## Checks

* Dependency rule, no `mvp/` code, no new SQL, no enablement, synthetic data only: pass.
* Refusal precedes any model call; role and case re-checked each turn: pass.
* Criteria needing owner decisions or evidence are unticked in the changes file: pass.

## Routed findings

* Known gap fixes need a grounding verifier (claim-level) and prose injection filtering: later work.
* Regex-based refusal is coarse and may over- or under-match: improve with the held-out set.

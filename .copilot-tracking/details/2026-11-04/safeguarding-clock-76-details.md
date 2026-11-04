---
title: Issue 76 details, safeguarding clock
ms.date: 2026-11-04
---

## Phase 3 outline (not started)

* Add a safeguarding marker to the case model in `src/core` with named owner, opened time and an approved response duration supplied by configuration, not hard-coded.
* Project the marker per role on the server; hide detail from roles without need; never expose it to AI paths or memory.
* Reuse the PR 897 plain-word owner and response-state sentence; an unknown owner is stated as unknown.
* Behavioural tests in `src/core/tests` and `src/api/tests`: owner shown, unknown owner stated, role without access sees nothing, AI-unavailable and manual paths unchanged.
* Tier: security-sensitive (special-category-adjacent data), so the complete gate applies and the coordinator runs it.

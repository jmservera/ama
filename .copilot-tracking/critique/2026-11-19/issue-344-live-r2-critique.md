---
title: Issue 344 live r2 critique
ms.date: 2026-11-19
---

Critique executed once on the plan "no source change; record per-criterion table".
Verdict: accept. Challenge considered: a code-only mitigation (app-level 401 for JSON requests) cannot work, because Easy Auth intercepts before the app sees the request while the path is protected, and excluding /api from Easy Auth would remove a security control (FULL tier). Rejected as out of scope. No significant or divergent issue.

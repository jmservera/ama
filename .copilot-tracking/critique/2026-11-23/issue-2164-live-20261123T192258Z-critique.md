---
title: Critique for issue 2164 live r9
ms.date: 2026-11-23
---

Verdict: proceed. Executed once. Risks: tests must not assert behaviour the code lacks (empty tenant allowed is explicit in code: `staff.get("tid") in (None, "", user.get("tid"))`); keep fixtures inside the existing `bound_entra` helper. Disposition: applied directly, no user decision needed.

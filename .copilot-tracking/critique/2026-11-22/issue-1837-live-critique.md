---
title: Critique issue 1837 live, 2026-11-22
ms.date: 2026-11-22
---

Verdict: proceed. Risk: live probes could write to the shared demo; mitigated by sending only invalid or empty input and comparing the case before and after. No src change, so the focused tier holds.

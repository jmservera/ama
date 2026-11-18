---
title: Issue 138 run 2 critique (one pass)
ms.date: 2026-11-18
---

Verdict: proceed.

* Risk: overwriting the committed first-run artifacts. Applied: first-run research restored; run 2 uses `-run2` names.
* Risk: claiming OIDC proof without Entra data. Applied: mark Unproven with the missing privilege and settings.
* Risk: implying demo group equals pipeline environment. Applied: state the naming mismatch.
* Boundary: no Azure writes; what-if is read-only; temp files deleted.

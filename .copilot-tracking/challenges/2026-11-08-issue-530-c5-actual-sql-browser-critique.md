---
title: Issue 530 C5 actual chat SQL and employee browser critique
ms.date: 2026-11-08
---

* Execution: one independent prospective critique (rubber-duck, read-only), before execution. Verdict: Revise. Findings: F1 SQL safety and environment, F2 origin proof, F3 egress and Chromium, F4 lock descriptors and failure cleanup, F5 SQL ownership recheck (all blocking), F6 result-check strictness, F7 frozen head ambiguity (non-blocking).
* All applied in the details amendments. F3 is applied in part: native Chromium network confinement is not enforceable here (`unshare -rn` denied), so the maintained boundary is used and recorded as a limitation; a missing matching Chromium revision stops the run.
* No user decision required.

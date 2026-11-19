---
title: "Critique: issue 1840 plan (single pass)"
ms.date: 2026-11-18
---

Verdict: approve with direct dispositions. Executed once.

* Risk: requiring `before == pending` inside `completed()` could turn a trustworthy VIOLATED into INSUFFICIENT. Disposition: acceptable; the `before` state is a precondition already treated as a gap, and adverse evidence from other steps and snapshots is unaffected.
* Risk: changing the `completed()` signature. Disposition: single caller (`judge`); updated directly.
* Risk: the two `config()` typing errors may not reproduce. Disposition: measure first, fix only if reproduced.
* Conflict with owner decisions: none. No Azure action is relevant to an offline judge.

---
title: Issue 432 per-call expiry plan critique
ms.date: 2026-11-13
---

Independent rubber-duck critique, executed once. Verdict: Revise.

* PC-001: fixed `now` defeats per-call expiry. Applied: `now` replaced by an injected `clock` read before every dispatch; tests pass `clock`.
* PC-002: a reapproved replacement manifest still looks frozen. Applied: initial digest and `threshold_approval` snapshot compared before every dispatch (`freeze-drift`).
* PC-003: failing clock or `check_freeze` could lose the report. Applied: check failures stop with `check-failed`, keeping accrued rows and spend.

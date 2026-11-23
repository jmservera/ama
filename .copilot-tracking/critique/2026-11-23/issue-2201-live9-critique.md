---
title: Issue 2201 live9 critique
ms.date: 2026-11-23
---

Executed once on the final candidate. Verdict: approve with direct dispositions.

* Leakage: store `type(error).__name__` only, never the message. Applied.
* Repeat firing: `on_error` may fire repeatedly; keep the first class. Applied.
* Precedence: separate attribute, so `callback_error_type` is never overwritten. Applied.
* Scope: raised codes unchanged. Applied.

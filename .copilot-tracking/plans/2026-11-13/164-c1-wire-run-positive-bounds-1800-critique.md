---
title: "#164 plan critique (rubber-duck, one pass)"
ms.date: 2026-11-13
---

Verdict: revise, all findings compatible and applied directly.

* Usage contract: read `ModelReply.usage` and `ModelUnavailable.usage`, not `last_usage`; spend priced at the rate the declared per-call bounds imply. Applied.
* Concurrency: dispatch and reconciliation serialised under the ledger lock. Applied.
* Scripted bypass: exempt only `type(model) is Scripted`; subclasses are wrapped. Applied, tested with a dispatching subclass.
* Receipts: breach `ModelUnavailable` carries calls, usage and meter ids. Applied.

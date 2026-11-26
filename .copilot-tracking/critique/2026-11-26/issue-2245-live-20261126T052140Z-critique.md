---
title: Critique, issue 2245 live 20261126T052140Z
ms.date: 2026-11-26
---

Executed once on the final candidate plan. Verdict: proceed.

* Finding 1 (compatible, applied): the fix must not claim the hourly reset as live-proven until a call is seen after the next hour boundary; the plan adds a post-06:00 UTC probe and records the result either way.
* Finding 2 (compatible, applied): other workers share the demo API, so call-budget breaches may come from their probes; the note records this as an alternative explanation, not a finding about the meter.
* Finding 3 (rejected, conflicts with the owner decision of 2026-11-18): deploying the corrected wording; deploys are outside this run.
* Scope: wording constants and one test only; the ledger hold semantics stay unchanged.

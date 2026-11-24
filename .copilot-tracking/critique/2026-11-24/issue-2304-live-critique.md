---
title: Issue 2304 round 2 critique (2026-11-24)
ms.date: 2026-11-24
---

# Critique (executed once)

Verdict: proceed, findings applied directly.

* Risk: memoising `release_reference` could serve a value that changes mid-compute. The forecast reads on one read-only connection under `rel.read_only()` and never records, so the value is fixed for the run; the memo lives on the per-run `ForecastReads` view and is not shared. Applied: limit the memo to `ForecastReads`; the write paths keep the unmemoised read.
* Risk: `assessment` may record an invalidation as a side effect. Under `rel.read_only()` it does not write, so one call equals many.
* Risk: a start-up warm job needs an identity. Rejected with reason; cold compute becomes fast.
* Risk: fixing the registry rebuild globally changes shared behaviour. Rejected as out of scope; recorded as follow-up.

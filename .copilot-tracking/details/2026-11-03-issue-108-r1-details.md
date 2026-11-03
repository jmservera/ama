---
title: Issue 108 round 1 details
ms.date: 2026-11-03
---

* Input: baseline and candidates, each with `id`, `observations` (case_id, accepted, critical_miss, unsupported_claim, overridden, reopened, refused, latency_ms, input_tokens, output_tokens), optional `price_source` (id, as_of, currency, input and output per million) and `changes` (one lever).
* Output: per-candidate counts, refusal rate, latency, token mean/min/max/stdev, economics (Unknown with named missing inputs), verdict (failure, no saving claimed, not cheaper, cheaper without a recorded regression), plus a not-comparable list.
* Boundaries: no price, budget or target set; no approval; synthetic observations are not actual-model or human evidence.

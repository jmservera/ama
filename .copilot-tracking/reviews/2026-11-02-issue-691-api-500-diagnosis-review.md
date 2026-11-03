---
title: Review for issue 691 API error diagnosis
ms.date: 2026-11-02
---

Review execution: executed once (self-review of the diff, focused tier). Outcome: self-review found no issues; unverified pending gate and independent review. Open items are routed below. Independent exact-head review, hosted CI and the coordinator gate remain required and are not claimed.

## Findings

* Goal 1 met: 403 are role denials; 503 are optional-provider gaps (photo token, law store) with clear bodies and UI handling; statuses intentionally unchanged (law 503 is fail-closed).
* Goal 2 partially met: no app code path emits a 500, and an earlier ad hoc local burst of 1000 concurrent mixed requests (JSON store and SqlStore, script not retained) showed none; the committed test now runs a bounded 140-request burst; cause of the live 500 is unproven and may be the ingress or Easy Auth sidecar.
* Goal 3 met: escaped exceptions now log class, path, status and raising frame, without message, query or headers; asserted by test.
* Goal 4 met: only escaped exceptions change behavior (dropped connection becomes a 500 body).

## Routed work

* After deploy, rerun the live burst and read the `http-error` and `http-response` lines: `http-error` present means an app exception; absence with a client 500 means ingress or Easy Auth. This is why the PR uses `Refs #691`.

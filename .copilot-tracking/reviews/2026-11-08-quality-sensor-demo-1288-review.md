---
title: Issue 1288 review
description: Single post-implementation review of the retained sensor read model, employee UI and Quality evidence grounding
ms.date: 2026-11-08
---

Executed once on 2026-11-08T19:31Z after implementation, by the implementing agent reading the diff against the plan and acceptance intent. Boundary: the working tree before the commit. Evidence: [changes](../changes/2026-11-08-quality-sensor-demo-1288-changes.md). This is not the independent exact-head assessment, which the coordinator owns.

## Execution and outcome

* Execution: executed. Outcome: conformant for the delivered slice with the findings below routed as later work. No finding blocks the source slice.

## Checked and held

* Values come only from retained `SYNTHETIC` rows for one home, bounded by `LIMIT` and a sealed window. No fixture generation, weather or other variables on the read path.
* The employee view and the model snapshot use one function, and a test proves the captured model request carries the API's IDs and values.
* The flag exists only for source `ai`, outcome `returned`, carries model attribution and cited IDs, and states it is not acceptance, payment, defect closure, consent, hazard diagnosis or ranking. Mock-provider tests are labelled and not proof of real AI.
* Existing authorization, staff scope, revocation, release, staleness and expiry controls are reused. No new service, ingestion or model database access.

## Findings routed to later work

* F1 Medium: rule and registry hash change retires every existing quality-evidence release. An approved matching release and serving-model attestation are needed before an actual exercise. Route: release step.
* F2 Low: `Programme Support Officer` is in the UI quality role list but `quality-evidence` authorization may deny it; the panel then shows the server message and manual route. Route: align role lists.
* F3 Low: the review-flag block and the 503 and consent-withheld panels were not browser-exercised; consent-withheld and unavailable are covered by SQL tests only.
* F4 Low: SQL Server (`OFFSET/FETCH`) path is unexecuted here (no SQL Server).
* F5 Low: up to about four proposals per case per day after sealed-window changes, bounded by allowance, expiry, release admission and the default-off proactive flag.
* F6 Info: before/after uses the first quality record time, not an install date, until a retained stage marker exists.

## Follow-ups

1. Live-envelope admission from the independent simulator work (#184) and a matching quality release.
2. Browser check of the review-flag block and absence states.
3. Role list alignment (F2).

---
title: Issue 1288 retained sensor values and Quality AI grounding plan
description: Plan for the bounded read model, employee UI values and sensor-grounded quality-evidence capture
ms.date: 2026-11-08
---

Research: [research](../research/2026-11-08-quality-sensor-demo-1288-research.md). Details: [details](../details/2026-11-08-quality-sensor-demo-1288-details.md). Authored 2026-11-08T19:17Z, before source edits. Source and local only.

## Phases

* [x] Phase 1 core read model: `core/sensor_view.py`, consent read on a supplied connection, served through `Assistants.sensors` (no `Store.sensor_view`).
* [x] Phase 2 API and employee UI: `GET /api/cases/{id}/sensors`, values/IDs/units/freshness/before-after panel in the Quality tab, flag block in `assistantProposal`.
* [x] Phase 3 quality-evidence grounding: capture sensors source and reading citations, rule/category/purpose update, proactive predicate, derived review flag.
* [x] Phase 4 tests: core unit, API SQL permission/bounds/restart/dedupe, captured model-request correlation with the API values (mocked provider, labelled), stale/revocation/unavailable, focused browser and axe check.
* [x] Phase 5 docs and evidence: component README note, changes artifact, one Review, commit.

## Constraints

* No fixture values on production read paths, no unbounded history, no weather mixing, no extra variables.
* No new agent service, simulator, ingestion engine or model database access; the model receives the inert snapshot only.
* No quality acceptance, payment, defect, consent, hazard or ranking effect. Existing release, staleness, revocation, continuity and finite allowance controls are reused unchanged.
* No Azure, push, PR or real model call.

## Critique (single final-candidate pass, 2026-11-08T19:17Z)

* Risk: a live five-minute window in the snapshot would defeat dedupe. Applied: window sealed to 6 hour UTC boundary; live latest reading is displayed but excluded from the snapshot.
* Risk: freshness in the snapshot would make it time-varying. Applied: freshness computed only in the API view, never captured.
* Risk: "flag" shown for fixture or unavailable output. Applied: derive only when envelope source is ai and outcome returned.
* Risk: consent bypass. Applied: values withheld unless consent is granted; the capture carries the withheld state, not values.
* Risk: reference date mistaken for install date. Applied: wording states it is the first active quality evidence record date.
* No conflict with confirmed owner decisions found.

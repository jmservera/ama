---
title: Quality sensor demo #1288 correction 1 plan
ms.date: 2026-11-08
---

Written 2026-11-08T19:40Z (UTC) after the C1 research artifact. Details:
[c1 details](../details/2026-11-08-quality-sensor-demo-1288-c1-details.md). Scope: the nine findings only.
No new service, simulator, ingestion engine, model call, Azure write or private data.

## Phases

* Phase 1, read model: provenance classes by `schema_version` and `scenario`; clock-free capture holding newest
  readings and the latest; composite citation keys; explicit retrofit-unavailable and quality-record anchor;
  bounded consent lookup by sensor ID; one narrow `(home_id, observed_at)` index created by the consumer.
* Phase 2, assistants: trigger signature that is clock-free and bucketed to six hours of latest observation;
  use it for task identity, staleness, scan, forecast, claim and export; `known` guard so an unchanged
  signature is not re-proposed; strict flag projection; consent-withdrawal projection in view/list/export.
* Phase 3, UI and docs: sensor panel shows provenance, latest from the capture, retrofit-unavailable text,
  anchor naming and the endpoint role set; flag block states manual/uncited/rejected/stale/withheld accurately.
* Phase 4, validation: focused unit/API tests on SQLite, the same scoped regressions on local SQL Server
  under one heavy-lock holder, real Chromium with a local API and scripted provider, pinned axe, ruff, node check.

## Decisions

* Live simulator rows stay in the demo, labelled synthetic, weather-derived and not calibrated.
* Evidence is exact; only the trigger is coarse. Fresh readings are never omitted to save cost.
* Consent withdrawal withholds values in current projections; stored records are unchanged.
* The flag is a suggestion for a person to review; no recipient or delivery is claimed.

## Critique (single pass, 2026-11-08T19:41Z)

* Risk: a coarse trigger could hide a newer reading from the model. Accepted change: the capture always holds the
  newest readings; only identity/staleness uses the bucket, and a proposal view reports newer readings exist.
* Risk: the index could change a shared schema. Accepted: additive, idempotent `CREATE INDEX IF NOT EXISTS`
  (SQLite) and guarded `CREATE INDEX` (SQL Server) in the consumer's existing schema step, verified on real SQL.
* Risk: unknown real sensor IDs for consent. Accepted: derive sensor IDs from the retained rows of the home and
  look each up by primary key, plus the two canonical per-home IDs; an unmatched sensor is withheld.
* Risk: tests that restate constants. Accepted: tests assert behaviour (equality across seal, multi-seal digest
  stability, flag matrix, HTTP withdrawal, role matrix, collision).
* Critique verdict: proceed; no finding conflicted with a confirmed decision, all applied directly.

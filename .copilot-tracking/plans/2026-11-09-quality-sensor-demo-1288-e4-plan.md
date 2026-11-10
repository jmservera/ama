---
title: Plan - issue 1288 E4
---

# Plan: issue 1288 E4 (fourth of five additional cycles; one remains)

Task `issue-1288-e4`, parent `issue-1288-e3`. Refs #1288 only; whole and live criteria stay OPEN. Research: [research](../research/2026-11-09-quality-sensor-demo-1288-e4-research.md). Details: [details](../details/2026-11-09-quality-sensor-demo-1288-e4-details.md).

## Phases

* [x] P0 Ordinary fresh `origin/main` (`ad679b96b`) merge, local, no conflicts (`ebb08e21d`).
* [ ] P1 Dedicated simulation store and sealed capability in core: `sensor_sql.SensorSqliteConnector`, `simulation_lane` (store, key, fixture, composer, mint, verify, orchestration), `ai_consumption` seal context and refusal type, `Ai.provider_body`, `Ai._admit_captured` verification before data hold, meter, token and socket.
* [ ] P2 Production composition and routes: `Assistants.dispatch_hold`, `App` lane opening from explicit environment only, three role-gated routes, default deny when unconfigured.
* [ ] P3 Visible synthetic UI panel (`simulationPanel`) in the existing assistants view, with unavailable and manual route text.
* [ ] P4 Tests: boundary and negative regressions at `Ai` with the real loopback TLS peer and counting meter/token; composition equality of UI view and recorded request bytes; routes, roles and default deny; browser check; typing.
* [ ] P5 Targeted validation (demo tier, no full gate): modified and impacted unit, SQLite, owned SQL under nonqueued `flock -n`, browser and axe, ruff, same-tool mypy comparison against the E3 baseline (0 new, 63 core and E3 api baseline kept).
* [ ] P6 One review, handoff, clean local commit; independent exact-head review required before any publication.

## Constraints kept

* Private and real captured-data Ai route stays OFF: `Assistants.execute` and the API fence are unchanged; a captured request without a valid seal is refused as today.
* No IDs, prefixes, flags, environment paths, value coincidence, shared case store or free text can open anything; only a seal minted by the lane key over the exact serialized body.
* Results are unapproved proposals stored only in the dedicated store; no controlled-domain write, no auto-acceptance, no approval action offered.
* Existing provider, release, suspension, token, cost meter and manual route guards are preserved and applied; nothing is weakened or bypassed.
* No live, Azure, model, financial or approval authority; no push, PR, issue, board or merge.

## Acceptance for E4

* A real `Ai` over a local loopback TLS peer sends exactly the sealed bytes; the recorded request reading IDs and values equal the stored and UI-visible values.
* Every negative case is refused explicitly before meter, token and socket (peer accepts, bytes, meter and tokens zero).
* Targeted tests green with counts recorded; 0 new mypy diagnostics; browser and axe pass.

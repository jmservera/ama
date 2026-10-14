---
title: In-Use Monitoring Analytics Research Plan (Dew Point and Trend Risks)
description: Research phase plan for analysing humidity and temperature sensor data received through Azure IoT Hub, including dew point and surface condensation risk, with leads, unknowns, evidence rules and exit criteria
author: AMA programme
ms.date: 2026-10-14
ms.topic: reference
---

## Status

Plan only. Nothing here is a validated method, threshold, legal duty or
approved rule. The leads below come from an uncited web synthesis retrieved on
2026-10-14 and from general Microsoft Learn results; each must be confirmed
against a primary source in phase R1 before it is used. Sensor data remains
simulated until the open items in
[BRD OD-43](../../brds/agentic-retrofit-programme-brd.md) are closed.

Related decisions: [ADR 0003](../../adrs/0003-journey-derived-capabilities-runtime-fit.md)
(Azure IoT Hub ingestion), [ADR 0002](../../adrs/0002-pilot-readiness-architecture.md#sensor-data-capture-analysis-and-map)
(capture and review-signal design), BRD FR-048/AC-090 and RULE-014, and PRD
FR-050 with AC-066 to AC-068.

## Questions

* Which derived measures are meaningful from air temperature and relative
  humidity alone, and which need surface temperature or outdoor conditions?
* How should dew point be derived, with what formula, valid range and error,
  and what margin to a surface temperature indicates condensation or mould
  risk?
* What persistence rule (duration, repeat count, time of day) separates a
  transient peak from a sustained risk, and how much data is sufficient?
* Which trends are worth surfacing to a human reviewer: sustained high
  humidity, small gap between air temperature and dew point, repeated
  overnight peaks, slow drift after a retrofit measure, or divergence from
  comparable homes?
* How do sensor accuracy, placement, calibration, clock drift and missing data
  change the confidence of each signal?
* How can the result be explained to a resident, a housing officer and a
  retrofit assessor without implying a diagnosis?

## Leads to verify (unverified)

| Lead | What to confirm | Primary source to find |
| --- | --- | --- |
| Dew point from air temperature and relative humidity by the Magnus approximation, with commonly cited constants for temperatures above 0 C | Constants, validity range and error against a psychrometric reference; behaviour at low temperature | Meteorological or metrology reference, for example WMO or a national standards body |
| Surface condensation when a surface is at or below the dew point; mould risk when surface relative humidity is sustained near 80 percent | Whether 80 percent and any margin to dew point are stated in current UK guidance; the averaging period | BS 5250 and related UK condensation and mould guidance, PAS 2035 monitoring provisions, building physics literature |
| Temperature factor (fRsi) compares internal surface temperature with internal and external air temperature, with commonly cited dwelling thresholds near 0.75 | Definition, thresholds and when it applies; needs surface and outdoor temperature, which the demonstration does not capture | BRE or BS EN ISO 13788 and BS 5250 |
| Persistence and trend rules reduce false alerts | Window lengths, minimum valid samples and seasonal effects | Peer-reviewed or industry monitoring studies in social housing |
| Occupancy behaviour, ventilation and heating drive indoor humidity | How to separate behaviour, building fabric and weather without blaming residents | Retrofit monitoring evaluations; resident-engagement guidance |

The web synthesis also claimed that PAS 2035 mandates ongoing monitoring of
air and surface conditions. Treat that as unverified; the local regulatory
corpus does not establish it.

## Phases

| Phase | Work | Output | Gate |
| --- | --- | --- | --- |
| R1 Source review | Locate and cite primary sources for each lead; record source date, retrieval date and classification (guidance, technical standard, research) | Cited evidence table in this file | Each retained lead has a primary source; unverified leads are dropped or labelled |
| R2 Method options | Specify candidate derived measures (dew point, dew point margin, sustained-high-humidity duration, overnight peak count, post-measure drift) with inputs, formula, data sufficiency and failure modes | Versioned method specification; no numeric threshold asserted without a source | Competent building-physics reviewer and Asset sign off the method as a candidate |
| R3 Synthetic validation | Generate labelled fictional scenarios (normal, condensation-prone, sensor fault, missing data, seasonal shift) and test each method for detection, false alerts and sufficiency handling | Scenario pack, confusion summary and sensitivity notes, kept separate from real data | Methods meet agreed false-alert and miss limits on synthetic data; limits are labelled exercise values |
| R4 Explainability and review | Draft the reviewer view, resident-safe wording and non-AI comparator; check accessibility and no-diagnosis wording | Review-ready explanation set | DPO, Resident Engagement and Safety review wording; no diagnosis or blame |
| R5 Real-data readiness | Confirm inventory, mapping, calibration, lawful basis, retention and thresholds with owners | Updated OD-43 disposition | Named owners approve before any non-synthetic use |

## Constraints

* Derived signals only create a human condition-review task. They never
  diagnose a hazard, start a statutory clock, override a resident report,
  release a hold or change investment ranking directly (BRD FR-048, RULE-014).
* The deterministic method is primary. Any AI-assisted trend discovery is
  exploratory, runs on synthetic or approved data only, is compared against the
  deterministic result, and needs its own purpose, field access and evaluation
  (PRD CON-009 still applies to delivered builds).
* Missing, stale or invalid data is `INSUFFICIENT`, never normal, and never
  lowers a home's priority or service.
* Residents may decline monitoring without penalty.
* Cite source and retrieval dates for every regulatory or standards claim, and
  record newer retrievals in the regulatory register rather than editing
  snapshots.

## Exit criteria

* A cited evidence table, a versioned method specification and a synthetic
  scenario result exist.
* Every threshold is either sourced or labelled as an exercise value.
* The owner has accepted, rejected or deferred each candidate measure.

## Evidence record

| Date | Action | Result |
| --- | --- | --- |
| 2026-10-14 | Plan created from an uncited web synthesis and Microsoft Learn IoT Hub results | No primary source reviewed yet; phases R1 to R5 not started |

---
title: In-Use Monitoring Analytics Research Plan (Dew Point and Trend Risks)
description: Research phase plan for analysing humidity and temperature sensor data received through Azure IoT Hub, including dew point and surface condensation risk, with leads, unknowns, evidence rules and exit criteria
author: AMA programme
ms.date: 2026-10-14
ms.topic: reference
---

## Status

Plan with a first source check. Nothing here is a validated method,
threshold, legal duty or approved rule. The leads came from an uncited web
synthesis and were checked on 2026-10-14 against the sources in
[Source verification (2026-10-14)](#source-verification-2026-10-14). Phase R1
remains open: the standards are paywalled and several confirmations rest on
secondary sources, so a competent reviewer must confirm against the official
text before use. Sensor data remains
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

## Leads and verification status

| Lead | What to confirm | Status (2026-10-14) |
| --- | --- | --- |
| Dew point from air temperature and relative humidity by the Magnus approximation, with commonly cited constants for temperatures above 0 C | Constants, validity range and error against a psychrometric reference; behaviour at low temperature | Partly verified: constants and range confirmed through Lawrence (2005); the original paper's own error figure was not retrieved |
| Surface condensation when a surface is at or below the dew point; mould risk when surface relative humidity is sustained near 80 percent | Whether 80 percent and any margin to dew point are stated in current UK guidance; the averaging period | Partly verified: the 80 percent and 70 percent air figures are in BS 5250:2011 text via a mirror only; not found in current gov.uk damp and mould guidance |
| Temperature factor (fRsi) compares internal surface temperature with internal and external air temperature, with commonly cited dwelling thresholds near 0.75 | Definition, thresholds and when it applies; needs surface and outdoor temperature, which the demonstration does not capture | Verified in the BS 5250:2011 text via a mirror and two secondary sources; BRE IP 1/06 original not retrieved |
| Persistence and trend rules reduce false alerts | Window lengths, minimum valid samples and seasonal effects | Verified at practitioner level (LOTI 2025); no peer-reviewed study found |
| Occupancy behaviour, ventilation and heating drive indoor humidity | How to separate behaviour, building fabric and weather without blaming residents | Verified for the no-blame principle (Housing Ombudsman); behaviour separation method still open |

The web synthesis claimed that PAS 2035 mandates ongoing monitoring of air and
surface conditions. This is an overstatement. A secondary source states that
PAS 2035 requires a risk-based monitoring and evaluation strategy, with sensor
monitoring at intermediate levels, not for every retrofit. Do not cite a
blanket sensor mandate; the official PAS 2035 text is paywalled and was not
read.

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
| 2026-10-14 | Plan created from an uncited web synthesis and Microsoft Learn IoT Hub results | Leads listed |
| 2026-10-14 | Source check by the research agent against public pages (below) | Leads partly verified; official BSI, BRE and AMS texts not read; R1 stays open; R2 to R5 not started |

## Source verification (2026-10-14)

All sources were retrieved on 2026-10-14. Quotes are short extracts reported by
the checking agent and were not independently re-read by the author.
Status values: Verified, Partly or Not found.

| # | Lead | Status | Source | Caveat |
| --- | --- | --- | --- | --- |
| 1 | Magnus dew point, a = 17.625, b = 243.04 C, range about -40 to +50 C | Verified (constants and range); Partly (stated error) | Lawrence, M.G. (2005), Bulletin of the American Meteorological Society 86(2), 225-233, as cited on Wikipedia "Dew point"; Alduchov and Eskridge (1996) title confirmed only through an abstract mirror | The publisher page was blocked, so the original paper's error figure was not read |
| 2 | Mould risk when surface relative humidity exceeds 80 percent; room air above 70 percent likely to give surface above 80 percent | Verified in BS 5250:2011 text; provenance Partly | BS 5250:2011 text via a third-party mirror, not BSI; BSI product page not accessible | Not found in current gov.uk "Understanding and addressing the health risks of damp and mould" guidance, which gives no numeric threshold. Confirm against the official standard |
| 3 | fRsi not less than 0.75 sufficient to avoid mould growth; see BS EN ISO 13788 and BRE IP 1/06 | Verified | BS 5250:2011 text via the same mirror; thermalbridgecalcs.com and specifierreview.com corroborate | BRE IP 1/06 original was not reachable. fRsi needs surface and outdoor temperature, not captured in the demonstration |
| 4 | PAS 2035 mandates ongoing monitoring | Partly: overstated | RISE Retrofit "Monitoring and Evaluation" toolkit, riseretrofit.org.uk (secondary guidance) | Accurate wording: PAS 2035 requires a risk-based monitoring and evaluation strategy that may include sensor data. BSI's PAS 2035 page is paywalled and was not read |
| 5 | Persistence and trend rules reduce false alerts | Verified (practitioner) | London Office of Technology and Innovation, "IoT Sensors for Damp and Mould Project: Winter Follow-Up", loti.london, 2025 | Practitioner report, not peer reviewed; no BRE or university study located |
| 6 | Avoid blaming residents for damp and mould | Verified | Housing Ombudsman Service, "Housing Ombudsman urges zero tolerance approach on damp and mould", 2021-10-26 (Spotlight report "Damp and mould: It's not lifestyle") | None significant |
| 7 | Azure IoT Hub tiers, routing, provisioning and authentication | Verified | learn.microsoft.com: iot-hub/iot-hub-scaling, iot-hub/iot-hub-devguide-messages-d2c, iot-dps/about-iot-dps, iot-hub/authenticate-authorize-azure-ad | Pages carry no fixed date. Basic tier is device-to-cloud only; standard adds cloud-to-device messaging, twins and IoT Edge. Message routing is available on both tiers. Devices authenticate with symmetric keys or X.509, not Entra ID; managed identity applies to service-side access |

Consequences for the design: use the 80 percent and fRsi figures only as
candidate exercise values labelled with the BS 5250:2011 source until the
official text is confirmed, and keep the analysis review-only.

## arXiv search (2026-10-14)

Searched the arXiv API (export.arxiv.org) on 2026-10-14 for dew point and
humidity formulas, mould and damp in housing, condensation risk in dwellings,
hygrothermal mould models, retrofit and social-housing indoor monitoring,
occupant behaviour, and the Magnus formula. No result addressed these topics,
so arXiv does not validate leads 1 to 6 above; the BS 5250, fRsi, PAS 2035 and
mould-risk questions need standards, BRE and building-physics journal sources.

Only generic sensor-method papers were relevant. They were read as abstracts
only and support method design (phase R2), not any threshold or standard:

| arXiv ID | Date | Title | Possible use |
| --- | --- | --- | --- |
| [1805.11999](https://arxiv.org/abs/1805.11999) | 2018-05-30 | Reference-free Calibration in Sensor Networks | Calibration of dense low-cost sensor networks without a reference |
| [2406.17488](https://arxiv.org/abs/2406.17488) | 2024-06-25 | Environmental Variation or Instrumental Drift? A Probabilistic Approach to Gas Sensor Drift Modeling and Evaluation | Separating real change from sensor drift |
| [2112.09072](https://arxiv.org/abs/2112.09072) | 2021-12-14 | Sampling Trade-Offs in Duty-Cycled Systems for Air Quality Low-Cost Sensors | Sampling cadence versus data quality |
| [1411.2188](https://arxiv.org/abs/1411.2188) | 2014-11-09 | Semantic-based Detection of Segment Outliers and Unusual Events for Wireless Sensor Networks | Outlier and unusual-event detection in sensor streams |

Next step for R1: search building-science sources (for example Building and
Environment, Energy and Buildings, BRE, Housing Ombudsman) and obtain the
official BS 5250, BS EN ISO 13788 and PAS 2035 texts through the owner's
licensed access.

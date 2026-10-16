---
title: In-Use Monitoring Analytics Research Plan (Dew Point and Trend Risks)
description: Research phase plan for analysing humidity and temperature sensor data received through Azure IoT Hub, including dew point and surface condensation risk, with leads, unknowns, evidence rules and exit criteria
author: AMA programme
ms.date: 2026-10-16
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

## Historical outdoor climate source decision (2026-10-16, Refs #178)

This is an offline evidence audit, not a completed historical-source study.
The issue and its owner comment were read on 2026-10-16; that is a GitHub
decision-evidence date, not a climate-data or licence retrieval date. No
external climate records or licence pages were retrieved for this audit.
The existing generator and tests explicitly state that climate records have
not been retrieved. No outdoor temperature or humidity figure is introduced
here.

### Owner direction and current selection

The [owner's issue comment](https://github.com/jmservera/ama/issues/178)
dated 2026-10-15 directs use of Met Office (UKCP18) and Environment Agency
open data under the Open Government Licence (OGL) where available, otherwise
clearly labelled synthetic data, with retrieval dates and licence recorded
per dataset. This is source direction, not dataset-specific reuse confirmation.

The selected current fallback remains
`synthetic-uk-seasonal-model-v1`, as declared by
[`sensor_backfill.py`](../../../src/core/src/zava_forward/core/synthetic/sensor_backfill.py).
It is constructed demonstration data, not historical North East England
weather, and has no external climate retrieval date. The owner-directed
external source family is recorded, but no historical product, station,
grid cell, release or observation period is selected as verified.

UKCP18 is the owner's named lead. Before selecting any product from that
family, establish whether the particular files contain historical
observations, historical model output or future projections; neither a
projection nor a generic provider name proves historical observation bounds.
HadUK-Grid and MIDAS Open remain candidates, not silent substitutions for
the owner's direction. A different product choice must be explicit.

### Candidate comparison and verification gaps

The candidate names in #178 were explicitly unverified. The table compares
their outstanding suitability questions, not verified product properties.
`Unverified` means no supporting dataset metadata, records or terms are held
in this audit; it does not mean unavailable from the provider. No candidate
passes the historical temperature-and-humidity evidence gate yet.

| Candidate | North East coverage and historical period | Resolution and required variables | Licence and reuse evidence | Current disposition |
| --- | --- | --- | --- | --- |
| Met Office HadUK-Grid, via CEDA | Unverified; identify cells and period covering the intended North East locations | Unverified; confirm spatial/temporal resolution and both outdoor temperature and relative humidity fields | Unverified; obtain the exact release's terms, attribution and redistribution conditions; do not assume OGL | Issue-named candidate; no records retrieved |
| Met Office MIDAS Open station data, via CEDA | Unverified; identify station IDs, locations, elevations, period and missingness | Unverified; confirm observation cadence, temperature and relative humidity availability and quality flags | Unverified; confirm the selected collection/version's access and reuse terms and attribution | Issue-named candidate; no records retrieved |
| Met Office historic station data | Unverified; identify a representative station and actual record period | Unverified; confirm whether the published variables and cadence support both required bounds rather than temperature alone | Unverified; retain the selected station file's applicable terms and attribution | Issue-named candidate; no records retrieved |
| Copernicus ERA5 reanalysis | Unverified; identify cells, product, version and period | Unverified; distinguish modelled fields from observations; establish whether relative humidity is supplied or must be derived from other fields with a cited method | Unverified; confirm product-specific licence, acknowledgement and redistribution terms | Issue-named alternative; no records retrieved |
| CIBSE weather files | Unverified; identify location, vintage and whether the file represents actual history or a constructed design year | Unverified; confirm cadence and both variables, and whether design-year extrema are suitable for historical bounds | Unverified; check access, purchase, permitted use and redistribution terms before obtaining or sharing files | Issue-named alternative; no records retrieved or purchase authorized |
| Met Office UKCP18 | Unverified; resolve the owner's lead to an exact historical product and period, if suitable | Unverified; distinguish observations, model output and projections; confirm both variables, units and resolution | Unverified; establish dataset-specific OGL applicability or other terms rather than generalizing from the owner comment | Owner-directed lead; no verified historical dataset selected |
| Environment Agency open data | Unverified; no collection or station has been identified | Unverified; first establish whether a collection supplies both required climate variables at relevant locations/cadence | Unverified; confirm the exact dataset's licence and attribution even where described as open data | Owner-directed lead; not yet an identified climate dataset |

### Retrieval, provenance and reuse register

| Field | Recorded state on 2026-10-16 |
| --- | --- |
| Current generator source | Labelled synthetic seasonal model; unchanged |
| Verified historical dataset and release | None selected |
| Climate record retrieval date | Not retrieved; no date to record |
| Licence evidence retrieval date | Not retrieved; no date to record |
| Dataset licence, version and terms | Unknown; OGL only where dataset-specific evidence establishes applicability |
| Attribution | Not yet verified; retain the provider's exact required acknowledgement with the eventual dataset citation |
| Source URLs, station/cell IDs, observation period and input hashes | No retrieved dataset packet held; must be recorded before deriving historical bounds |
| Reuse confirmation | Open; Juan Manuel Servera is the synthetic-exercise Legal, Compliance and DPO owner, not an inferred operational approver |
| Observed outdoor temperature and humidity bounds | Not derived; no retrieved records available |

An open-data label, access permission, or owner source preference does not
itself establish the terms for redistributing records or derived assets.
Agents may retrieve when authorized, compare, summarise and flag terms;
legal interpretation and reuse confirmation stay with the named human owner.
Real owners and sources remain a gap before operational reliance, consistent
with [ADR 0005's synthetic-only acceptance](../../adrs/0005-regulatory-compliance-assistant.md#owner-decision-acceptance-and-authority-2026-10-16).
No consent, safety decision, operational rule, purchase or financial
commitment follows from this source register.

### Evidence packet and bounds derivation gate

To resume offline, supply a locally retained evidence packet; alternatively
obtain separate authorization for external climate retrieval. The packet
must identify the provider, exact product/release and stable source URLs;
dataset and terms retrieval dates; applicable licence text/version or
reference and required attribution; raw file hashes; station IDs or grid
coordinates and elevation where supplied; historical period, timezone,
cadence, variable definitions, units, quality flags and missing-value codes.
Record any download query, extraction and conversion so the analysis can be
reproduced. Do not redistribute protected records before reuse review.

Derive bounds from the retained records, not from the generator's parameters:

1. Establish the selected locations and observation window from metadata and
   preserve the raw inputs. Identify observation versus modelled data; do not
   silently pool products, stations, periods or resolutions.
2. Parse timestamps and units using the source definitions. Count total,
   missing, duplicate, quality-rejected and valid values per variable,
   location and period. Retain rejection reasons; do not silently fill gaps.
   If humidity must be derived, cite and version that method and its inputs.
3. Calculate the minimum and maximum of the retained valid temperature and
   relative humidity records. Report the extrema with their source row/time,
   sample counts, window and input hashes. Report paired-sample coverage if
   temperature and humidity support a joint model. An empty required variable
   is insufficient evidence, never a default bound.
4. Retain the analysis command/code version and output hash. Review seasonal
   and location coverage and limitations before using the results to justify
   any synthetic range. One station or a short period cannot establish
   region-wide extremes. Observed sample extrema are not physical limits,
   a forecast, indoor thresholds or safety rules.
5. Obtain the owner's dataset-specific reuse confirmation and any required
   competent method review before adopting changed generator/test limits.
   Keep derived historical evidence separate from synthetic scenario
   parameters and injected faults; do not clip observations to make an
   exercise test pass.

The existing
[`OUTDOOR_EXERCISE` expectations](../../../src/core/tests/test_sensor_plausibility.py)
remain selected exercise values. Their tests establish internal synthetic
plausibility, not historical climate validity. Neither they nor this audit
satisfy the broader PRD AC-066 to AC-068 IoT, method or live-platform gates.

### Issue #178 acceptance audit

| Acceptance criterion | Status | Evidence and missing work |
| --- | --- | --- |
| Candidate sources compared on coverage, resolution, licence and reuse terms | Unmet; offline comparison framework only | All issue-named candidates and owner leads are listed above, but the dataset properties and terms remain unverified. Retrieve and compare primary metadata and applicable terms |
| Chosen source, retrieval date and licence recorded; licence stays open until the owner confirms reuse | Unmet; fallback/source direction recorded only | Synthetic fallback and owner direction are explicit; no verified historical source, retrieval date or licence evidence exists. Dataset-specific reuse confirmation remains open |
| Outdoor temperature and humidity bounds derived from retrieved records, not typed in | Unmet; blocked on records | Existing bounds are exercise values. No historical observations or calculated extrema are available; execute and retain the derivation above once records are supplied |

All three issue checkboxes remain unchanged. This audit is a bounded
documentation contribution, not completion of #178 or approval for real use.

## Public document check (owner-supplied, 2026-10-14)

Two public documents on BS 5250:2021 were supplied by the owner.

| Document | Result |
| --- | --- |
| BMI Group, "BS 5250:2021 Management of moisture in buildings: a guide to the updated British Standard and the changes to pitched and flat roofing", issued August 2021 (PDF on assets.ctfassets.net) | Retrieved and text-extracted. A manufacturer's roofing guide, not the standard. It confirms that a 2021 edition of BS 5250 exists and defines condensation as deposition when air temperature drops to or below the dew point. It lists BS EN ISO 13788 (internal surface temperature to avoid critical surface humidity and interstitial condensation) as a calculation method. It does not state the 80 percent surface humidity figure, the 70 percent room air figure or an fRsi threshold, and says nothing about sensor monitoring |
| Scribd, "BS5250 2021 New Guidance on Managing Moisture Risk in Buildings" | Not read. The page returned an access challenge to an automated request, and the full document needs a signed-in browser session. It may be a copy of protected material and its provenance is unknown, so it is not used as a source until the owner confirms the right to use it |

Effects on the leads:

* The thresholds checked earlier come from the 2011 edition of BS 5250. A 2021
  edition now exists, so each figure (80 percent surface humidity, fRsi 0.75)
  must be confirmed against the 2021 edition and BS EN ISO 13788 before use.
  Until then they stay labelled candidate exercise values from the 2011 text.
* The dew point definition of condensation is supported by the BMI guide only
  as a general definition; it does not validate the Magnus constants.
* Nothing in these documents changes the PAS 2035 finding.

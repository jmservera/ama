<!-- markdownlint-disable-file -->

# Task Research: climate-paired-source-178

| Field | Value |
|---|---|
| Date | 2026-10-21 |
| Researcher / agent | rpi-research (activated), inline waves |
| Status | Complete (Blocked outcome: no lawful anonymous paired records) |
| Artifact path | .copilot-tracking/research/2026-10-21/climate-paired-source-178-research.md |

## Research Brief

* What to research: can official, openly accessible North-East England historical records with timestamped actual temperature AND humidity/dew point be lawfully retrieved without account, credential, payment or prohibited scraping, to derive observed bounds for #179?
* Why it matters: #179 (indoor model) needs grounded outdoor paired bounds; PR371 delivered only Durham monthly temperature (no humidity).
* Scope: Met Office/CEDA MIDAS Open, HadUK-Grid, Environment Agency hydrology API (owner decision 2026-10-15 comment: UKCP18 / EA OGL where available, otherwise clearly labelled synthetic). Non-goals: indoor/retrofit equations, source approval, licence signoff, Azure, private data.
* Output mode: audit/comparison (decision state, no source selection).
* Posture: focused (caller-specified: avoid unlimited source chasing). Limits: none beyond brief.
* Resolved evidence root: .copilot-tracking/

## Extension Registry

| Kind | Candidate | Disposition |
|---|---|---|
| Instruction | repository AMA instructions (legal/regulatory evidence, KB conventions) | Selected; licence/owner gates, no source approval |
| Skill | rpi-research | Selected |
| Specialist | RPI Researcher | Skipped: lanes small and coupled, inline |

User participation: no interaction (non-interactive run); owner direction taken from issue comments.

## Prior Knowledge Gate

* Reviewed: .copilot-tracking/research/2026-10-17/climate-source-evidence-178-research.md (C/W1-W14), docs/reference/research/climate-source-evidence-178.json, tools/climate_station_bounds.py, issue 178 comments to 2026-10-17T08:35Z.
* Reused and re-verified today: MIDAS Open is OGL, hourly with calculated RH; CEDA file bytes need login (PR371 W4 for HadUK hurs; re-tested below for MIDAS).
* Superseded: none. PR371 temperature-only statistics remain valid and unpromoted.

## Research Questions

| # | Question | Status |
|---|---|---|
| Q1 | Do MIDAS Open hourly NE files download anonymously? | Answered: no |
| Q2 | Does EA Hydrology (OGL) carry humidity/dew point? | Answered: no |
| Q3 | What NE MIDAS coverage exists for an owner-authorised retrieval? | Answered (listing only) |
| Q4 | Any other in-boundary official anonymous paired source? | Answered: none found |

## Research Cycle Log (cycle 1)

### Wider

* Probed CEDA data/dap hosts, Met Office station-data pub path, EA Hydrology measures API.
* Candidates: MIDAS Open hourly (temperature + RH), HadUK-Grid monthly hurs (monthly only), EA Hydrology, Met Office station text (no humidity).

### Deeper

* C-evidence from tests run 2026-10-21T01:23-01:25Z (curl, no cookies/credentials):
  * W1: `https://dap.ceda.ac.uk/badc/ukmo-midas-open/data/uk-hourly-weather-obs/dataset-version-202607/` directory listing returns HTTP 200 anonymously and lists counties incl. `durham`, `tyne-and-wear`, `northumberland`, `cleveland`. Dataset versions listed: 201901 to 202607.
  * W2: Anonymous listing of `tyne-and-wear/00307_newcastle-weather-centre/qc-version-1/` shows yearly CSV names. Year coverage from listings: Newcastle Weather Centre 1974-2005 (32 files), Tynemouth 1957-2001 (45), Washington 1973-1981 (9), South Shields 1985-2003 (18), Sunderland University 1989-2003 (14), Durham 1972-2025 (54), Houghall 1972-1978 (7). Listing names are not proof the files carry usable RH rows.
  * W3: Every file fetch tested (`00README_catalogue_and_licence.txt`, station-metadata CSV, station `capability.csv`) returned body `Unauthenticated` or HTTP 302 to `/login/` on dap.ceda.ac.uk, and a 302 on data.ceda.ac.uk. No data bytes obtained. Per CEDA token/access guidance (PR371 W14) access is distinct from licence; obtaining a login is an account/credential step excluded by this brief.
  * W4: EA Hydrology API (https://environment.data.gov.uk/hydrology/id/measures.json, OGL v3 in response `meta.license`, retrieved 2026-10-21): sampled 2000 measures contain only Water Flow, Water level, Rainfall amount, Temperature (8, hydrological/water), Groundwater level; `observedProperty=humidity` returned zero items; documented observedProperty enumeration (waterFlow, waterLevel, rainfall, groundwaterLevel, dissolved-oxygen, fdom, bga, turbidity, chlorophyll, conductivity, temperature, ammonium, nitrate, ph) has no humidity or dew point. EA does not supply atmospheric paired data.
  * W5: PR371 evidence retained: HadUK-Grid regional hurs file is monthly and login-gated (PR371 W4); Met Office station text file (Durham) has no humidity.

### Contrarian

* Could unauthenticated listing/mirror access be used lawfully to read files? Rejected: the access control returns Unauthenticated; bypassing via alternate hosts/redirects would circumvent it.
* Could a non-approved source (for example NOAA ISD, ERA5 via account, Open-Meteo, Meteostat) fill the gap? Outside the owner-selected Met Office/EA OGL boundary, licence/reuse approval unproved, some need accounts; recorded as options needing owner confirmation only, not retrieved. Rejected as source-chasing and as a silent substitution.
* Could typed or synthetic values satisfy bounds? Rejected: criterion requires retrieved records; synthetic fallback may never fulfil record-derived historical bounds.

### Parent synthesis

* Accepted: blocker. Paired records cannot be lawfully obtained anonymously within boundaries; exact access evidence W1-W4.
* Rejected: bypass, substitution, synthetic fulfilment.
* Deferred: authenticated CEDA retrieval (owner/human with their own account), owner confirmation of reuse and station choice.
* Re-entry decision: no second cycle; waves saturated, next sources are outside boundary.

## Findings and Decisions

* No actual paired NE temperature/humidity records were retrieved; no bounds derived; PR371 Durham temperature stays temperature-only.
* Smallest unblocker: owner/authorised human with CEDA account downloads MIDAS Open `qcv-1` yearly CSVs (Newcastle Weather Centre 1974-2005, Durham 1972-2025 are the broadest listed) and supplies files for hash-pinned import, or owner explicitly approves an alternative public no-login source. Source, licence and reuse remain unapproved.
* #179 stays sequenced behind this. A grounded synthetic indoor model may use only clearly labelled synthetic outdoor inputs that never claim historical observation.

## Planning Readiness

Ready for a bounded evidence-only plan: record blocker artifact and precise owner action; no code added (nothing to ingest).
Research disposition: executed.

## Self-check

Findings cite W1-W5 with URL, date; no secrets; no edits outside research root.

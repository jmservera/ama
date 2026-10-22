<!-- markdownlint-disable-file -->

# Task Research: climate-paired-alt-source-178

| Field | Value |
|---|---|
| Date | 2026-10-22 |
| Researcher / agent | rpi-research (activated), inline waves |
| Status | Complete (alternative public source found and retrieved) |
| Artifact path | .copilot-tracking/research/2026-10-22/climate-paired-alt-source-178-research.md |
| Parent | climate-paired-source-178 (2026-10-21, blocked outcome preserved unchanged) |

## Research Brief

* What: find an openly accessible, credential-free, payment-free source of paired hourly temperature and humidity for North East England, verify terms, retrieve a small fixed sample and derive bounds from it.
* Why: #179 needs grounded outdoor paired inputs; the MIDAS route is login-gated (2026-10-21 blocker) and Durham is temperature-only.
* Authority: owner decision 2026-10-22 ("Investigate another source, no need to be extremely precise for the demo ... keep it in the documentation as a pending point for production"). This permits a labelled modelled demonstrator source with a production follow-up. It does not approve licence, precision or representativeness.
* Output mode: comparison with a demonstrator selection (parent-owned, proposal only).
* Posture: focused; bounded set of three new candidates plus the existing ones.
* Evidence root: .copilot-tracking/

## Extension Registry

| Kind | Candidate | Disposition |
|---|---|---|
| Instruction | AMA repository instructions (legal/regulatory, KB conventions) | Selected |
| Skill | rpi-research | Selected |
| Specialist | RPI Researcher | Skipped: small coupled lanes, inline |

User participation: none (non-interactive); owner direction from the 2026-10-22 decision.

## Prior Knowledge Gate

* Reused: 2026-10-17 candidate register and Durham temperature statistics (docs/reference/research/climate-source-evidence-178.json), 2026-10-21 blocker (docs/reference/research/climate-paired-source-blocker-178.json). Both stay unchanged and valid as negative and temperature-only evidence.
* Regulatory register (docs/reference/regulatory/README.md) holds legislation and funding sources only; it holds no climate-data licence entries, so licence claims below are cited to the live publisher pages with retrieval date, not to a local snapshot. No legal conclusion is drawn.
* Superseded: nothing. The 2026-10-21 "options needing owner confirmation" list named Open-Meteo, ERA5 and others; this cycle acts on the owner's 2026-10-22 authorisation to retrieve.

## Research Questions

| # | Question | Status |
|---|---|---|
| Q1 | Which bounded alternatives provide anonymous hourly paired T and RH for the North East? | Answered |
| Q2 | Do published terms permit the intended demonstrator reuse? | Answered with limits |
| Q3 | Can a small fixed sample be retrieved and validated? | Answered |
| Q4 | Do two independent modelled sources agree enough for a demo? | Answered |

## Research Cycle Log (cycle 1)

### Wider

Candidate set (bounded): Open-Meteo Historical Weather API (ERA5/ERA5-Land), NASA POWER hourly API (MERRA-2 based), Meteostat. Existing: MIDAS Open (login), HadUK-Grid (monthly, login), Durham station (temperature only, monthly), EA Hydrology (no humidity), CIBSE (licensed files), ERA5 direct from CDS (account/API key).

Meteostat was considered and not retrieved: it needs an API key or paid plan for the JSON service and its bulk data terms were not verified; recorded as not examined rather than rejected on evidence.

### Deeper

* W1 Open-Meteo terms, https://open-meteo.com/en/terms retrieved 2026-10-22: free API for non-commercial use under 10,000 calls/day, accepts the CC BY 4.0 licence. Non-commercial examples include public research at public institutions, educational content and non-profit apps without subscriptions or advertising. Commercial use needs a paid plan (not examined further, not used).
* W2 Open-Meteo licence, https://open-meteo.com/en/licence retrieved 2026-10-22: API data under CC BY 4.0; attribution link "Weather data by Open-Meteo.com" is required; weather reanalysis sourced from Copernicus Climate Change Service C3S, which carries its own licence.
* W3 Open-Meteo Historical Weather API docs, https://open-meteo.com/en/docs/historical-weather-api retrieved 2026-10-22: ERA5 (0.25 degrees, from 1940) and ERA5-Land (0.1 degrees, from 1950); hourly `temperature_2m`, `relative_humidity_2m`, `dew_point_2m` are instantaneous values; no key parameter in the free call.
* W4 Retrieval, 2026-10-22T13:57Z, no credentials, HTTP 200: `https://archive-api.open-meteo.com/v1/archive?latitude=54.768&longitude=-1.585&start_date=2023-01-01&end_date=2023-12-31&hourly=temperature_2m,relative_humidity_2m,dew_point_2m&models=era5&timezone=UTC&temperature_unit=celsius`. Response resolved the requested point to ERA5 cell 54.75 N, -1.5 E at 98 m model elevation; 8,760 hourly values per variable, no nulls; SHA-256 96e707ea5f7bd35af3ebdf896c7f9a41a055d220a0a0e832aa5ad008b7484a26. Saved as docs/reference/research/climate-paired-sample-178/open-meteo-era5-durham-2023-raw.json.
* W5 NASA POWER, https://power.larc.nasa.gov/docs/referencing/ retrieved 2026-10-22: citation guidance requires the POWER data reference with service, version and access date and requests notification of publication or redistribution. No explicit licence text was retrieved: the NASA data information policy page returned HTTP 403 to the fetch. Licence therefore unverified.
* W6 NASA POWER retrieval 2026-10-22T13:57Z, no credentials, HTTP 200: `https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=T2M,RH2M&community=RE&longitude=-1.585&latitude=54.768&start=20230101&end=20231231&format=JSON&time-standard=UTC`. API v2.10.3, sources MERRA2 and POWER, fill value -999, 8,760 hourly values, none filled; model elevation 144.05 m; SHA-256 cba9cf308878e9a4b2f2847cbbc4e66f06d14a1b734d4da48be0133fef9c6db1. Saved beside the first file.
* W7 Cross-source check (computed from W4 and W6, same 8,760 UTC hours): Open-Meteo ERA5 temperature range -5.5 to 26.7 degC and RH 36 to 100 percent; NASA POWER -3.35 to 24.61 degC and RH 43.43 to 100 percent. Mean ERA5 minus POWER temperature 0.96 degC (mean absolute difference 1.24 degC); RH mean difference -7.1 points (mean absolute difference 8.3 points). Elevation differs (98 m versus 144 m) and the grids are coarse, so the two modelled values disagree by more than station noise.
* C1 docs/reference/research/climate-paired-source-blocker-178.json: MIDAS Open, EA and HadUK negative evidence retained.
* C2 docs/reference/research/climate-source-evidence-178.json: Durham monthly temperature 1991-2020, humidity unavailable, retained separately.

### Contrarian

* Modelled reanalysis is not a station observation; ERA5 is 0.25 degrees (about 20 km), smooths terrain and the NE coast to Pennine gradient and systematically differs from POWER. It must be labelled modelled everywhere and not presented as observed, region-wide or safety-grade.
* Open-Meteo free use is non-commercial. A demonstrator for AMA training and research is plausibly within the stated examples, but whether the Zava Forward demonstrator is "non-commercial" is the owner's call; a production deployment by a housing association is not shown to qualify. Recorded as pending, not approved.
* The RH reported by ERA5 is derived from model temperature and dew point; humidity is not invented, but its consistency can be tested. The validator therefore checks the supplied RH against a Magnus-formula value from temperature and dew point.
* One year (2023) is a short and unrepresentative window for extremes; bounds are sample bounds only.
* NASA POWER stays a cross-check, not the selected source, because the licence text was not retrieved.

### Parent synthesis

* Accepted: Open-Meteo ERA5 hourly 2023 sample for Durham as the labelled modelled demonstrator source (W1-W4). NASA POWER sample as cross-check and sensitivity evidence (W5-W7).
* Rejected: treating either as an observation or as production-approved; deriving humidity; bypassing MIDAS login; replacing Durham temperature evidence.
* Deferred (production): station-grade source (MIDAS via an authorised account or a Met Office agreement), commercial-use terms, licence confirmation by the owner, representativeness across the NE, multi-year window, ERA5-Land versus ERA5 choice.
* Re-entry: none; waves saturated for the bounded set.

## Findings and Decisions

* Usable demonstrator source found: Open-Meteo ERA5 hourly, no key, CC BY 4.0 with attribution, free for non-commercial use.
* Terms permit the intended demo reuse as read on 2026-10-22 only if the demo is non-commercial; this is a reading, not legal approval.
* Disagreement between ERA5 and POWER (W7) is the documented demonstrator accuracy limit and a production follow-up.
* #178 criterion 2 licence confirmation stays unmet; criterion 3 is met for a labelled modelled demonstrator sample only, not for observed station data.

## Planning Readiness

Ready. Plan: hash-pinned validating adapter, tests, derived report, synthesis and index/log updates, no downstream issues.
Research disposition: executed.

## Self-check

Findings cite W1-W7 and C1-C2 with URLs, retrieval dates and hashes; no credentials used; negative evidence preserved.

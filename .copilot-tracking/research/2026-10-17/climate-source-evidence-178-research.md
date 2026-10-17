<!-- markdownlint-disable-file -->

# Task Research: climate-source-evidence-178

## Bounded Rebase Verification (2026-10-17)

Research disposition: reused. Planning Readiness: Ready for rebase-only
continuation, not new source research. Caller supplies independent Pass/MERGE
for the narrow partial feature at f4ea7542874baf6045db2e33764b1348a976c238;
this is not owner approval or complete #178 acceptance.

* C2: clean status and exact requested branch verified before writes. PR #371
  is open against main at the supplied head. Fetched origin/main is
  4e4a389f53870137a0f0582861766be5983a8f96, including #368/#370.
* C3: upstream diff overlaps only docs/reference/README.md,
  docs/reference/log.md and src/core/README.md. #176 adds replay provenance,
  deterministic-input caveats and an index route; #360 adds a current auth
  route and append-only log evidence. No competing climate source intent.
* C4: retained public input at the existing details locator is readable;
  SHA-256 remains d2c9ff2a443b8502957ce88fe8bfdbbd0d5ac111208eab0842bc574d4d4306f9.
  No redownload or private data inspection is needed.

Prior official-source research remains adequate for this history-only change.
No new three-wave source cycle executed or claimed. Exact resolutions must
retain all upstream source blobs, every upstream log entry and every original
feature log entry, plus the conditional climate route and no-RH/UNMET caveats.
Any ambiguous source intent blocks the affected resolution. No new claims,
downloads, feature work, Azure actions, spending, roles/networks or approvals.
Ruff/mypy are absent from default Python/PATH; investigate only an existing
recorded validation environment before reporting check availability.

## Research Brief

* Date: 2026-10-17. Status: Complete. Researcher: RPI Agent.
* Task: #178, online continuation of merged #367, not a re-run of its offline audit.
* Purpose/audience: evidence for the owner's historical outdoor climate choice.
* Scope: official metadata, dataset-specific terms and bounded public records for
  HadUK-Grid, MIDAS Open, historic stations, ERA5, CIBSE, UKCP18 and EA leads.
* Non-goals: owner approval, private data, paid/account/terms acceptance,
  operational activation, generator replacement, #176 and #360 changes.
* Criteria: compare coverage/resolution/licence/reuse; recommend a justified
  candidate with actual retrieval dates; derive only supported record bounds.
* Output mode: convergence; prepares the subsequent Plan phase.

## Research Parameters

* Posture: focused, selected from the caller's bounded source list.
* Evidence root: `.copilot-tracking/`; research writes restricted to research
  artifacts except required RPI state/session tracking.
* Internal starting areas: canonical sensor synthesis, source register within
  that synthesis, original/addendum, reference index/memory and #367.
* External starting areas: Met Office, CEDA, Copernicus, CIBSE, EA, National Archives.
* No arbitrary source/time ceiling. Stop on adequate in-scope evidence or precise
  access blockers. No upload of repository content or private data.

## Extension Registry and Provenance

| Kind | Candidate | Disposition and authority |
| --- | --- | --- |
| Instructions | `.github/copilot-instructions.md`, caller | Selected: immutable snapshots, canonical integration, human reuse boundary and PR workflow |
| Skill | rpi-research | Selected: three ordered waves and evidence/readiness record |
| Specialist | research / RPI Researcher | Skipped: one coupled bounded source-selection trace, handled inline |
| Domain | regulatory register | Selected as evidence-handling convention, not a new legal assessment |

## User Participation and Research Decisions

Explicit caller requests the full ordered loop and public retrieval, push and PR,
then stop. No interaction needed or available. This is an explicitly authorized
automatic task, not a manual-to-automatic inference. No follow-up child loop.

## Scope and Success Criteria

Question Q1: what does each named candidate actually supply and on what terms?
Question Q2: which candidate merits recommendation, distinct from approval?
Question Q3: which observed bounds can public records genuinely support?
All questions require official URLs, actual retrieval dates and explicit gaps.

## Direction Controls

Preserve owner UKCP18/EA preference as a lead, not proof of historical suitability.
No replacement source to manufacture closure. No humidity inferred from
temperature-only records. Never infer owner's licence/reuse approval.

## Prior Knowledge Gate

* #178 and comments, merged #367 read on 2026-10-17.
* Canonical original/addendum, reference index/memory, sensor synthesis and
  regulatory evidence conventions read.
* C1: `docs/reference/research/iot-sensor-analytics-research-plan.md:169`
  records an explicitly offline audit, not verified product properties.
* Clean worktree, requested branch `docs/climate-source-evidence-178`.
  Open #368/#370 belong to #176/#360; no matching active PR. Reuse requested branch.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Official metadata retrieved for all source families (2026-10-17).
HadUK-Grid explicitly supplies monthly hurs from 1961, not daily humidity.
MIDAS Open supplies hourly temperature and calculated RH; site coverage varies.
Historic Durham monthly file retrieved (1880-01 through provisional 2026-09).
ERA5 is hourly 0.25-degree reanalysis, not station observations. CIBSE is
TRY/DSY design weather, not an unmodified historical sequence. EA flood API
provides hydrology/rainfall, not this required variable pair.

Reflection: prioritize HadUK-Grid's exact release and anonymous access;
MIDAS is the stronger cadence candidate if accessible without registration.

#### Wave 2: Deeper

Exact HadUK-Grid regional release catalogue retrieved (W3): v1.3.2.ceda,
published 2026-06-23, OGL v3 and required dataset citation. CEDA explicitly
requires registration/login. The actual regional hurs NetCDF request (W4)
returned HTTP 200 HTML at accounts.ceda.ac.uk, not climate data. MIDAS release
README likewise redirected to login. No account, token or agreement attempted.

Met Office policies/tandc retrieved:
OGL v3 content grant with attribution and exclusions, but an additional
restriction on automated monitoring/copying. No further Met Office website
retrieval after discovering that restriction; record this for owner review.
Do not treat an OGL label as blanket automated-access permission.

#### Wave 3: Contrarian

Tested the strongest candidate against the actual replay need: HadUK-Grid's
monthly RH cannot evidence hourly or three-per-day extremes. Current CEDA
release adds daily mean temperature and says daily temperature was extended
to 1931 in v1.3.1; the generic Met Office variable page still says 1960.
Use release-specific metadata, not the stale generic start date.
MIDAS QC-version-1 is latest state, not proof all fields passed QC (W7).
Durham monthly daily-max/min averages cannot establish instantaneous extrema
and contain no humidity. CIBSE purchase/user licensing and TRY/DSY morphing
rule it out for this bounded observed-history study (W10). EA flood API's
documented variables do not establish that all EA datasets lack temperature.

Reflection: retain HadUK-Grid v1.3.2.ceda as the recommended observational
context product, not an hourly replay adapter; prefer MIDAS investigation for
future cadence-specific records. No named product yet supports adoption of
both replay bounds under the allowed access constraints.

#### Parent Synthesis and Disposition

* Accepted Q1: substantive comparison is possible from official metadata.
* Accepted Q2: recommend the exact HadUK release as contextual candidate only;
  explicit product refinement of owner's UKCP18 lead, not a silent substitution.
* Accepted Q3 partially: derive Durham monthly temperature statistics from
  retrieved file; humidity and replay-scale paired extrema remain blocked.
* Rejected: interpolated grid values, reanalysis or TRY/DSY as direct station
  measurements; synthetic defaults as retrieved bounds.
* Deferred: CEDA registration/login, owner reuse approval and method/adoption.
* Re-entry: no further cycle needed for this scope. Targeted official metadata
  and an actual hurs request establish the access blocker. Additional public
  searches cannot authorize account creation or owner reuse.

## Evidence Log

All W# records actually retrieved on **2026-10-17 UTC**. Summaries, not copied
pages. Official sources only; full raw pages and protected datasets not bundled.

| ID | Evidence and URL | Result / confidence |
| --- | --- | --- |
| W1 | [HadUK overview](https://www.metoffice.gov.uk/research/climate/maps-and-data/data/haduk-grid/haduk-grid) and [variables](https://www.metoffice.gov.uk/research/climate/maps-and-data/data/haduk-grid/datasets) | UK 1km interpolated observations, coarser averages, monthly hurs from 1961; high, generic daily-temperature start stale versus release |
| W2 | [HadUK 1km v1.3.2.ceda](https://catalogue.ceda.ac.uk/uuid/789b3065d74a4c948ab05d33556c86d0/) | Exact release 1836-2025, variables start separately, adds daily tas; high |
| W3 | [HadUK regions v1.3.2.ceda](https://catalogue.ceda.ac.uk/uuid/386b3c1ee2054ef5ae0d73060963a9f1/) | OGL v3, citation, register/login access, publication 2026-06-23; high |
| W4 | [Actual RH file](https://dap.ceda.ac.uk/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.3.2.ceda/region/hurs/mon/v20260512/hurs_hadukgrid_uk_region_mon_196101-202512.nc?download=1) | HTTP 200 HTML login, not NetCDF; high |
| W5 | [Historic station metadata](https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data) and [Durham file](https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/durhamdata.txt) | Monthly tmax/tmin, 1880-01 to 2026-09, no RH; file SHA-256 d2c9ff2a443b8502957ce88fe8bfdbbd0d5ac111208eab0842bc574d4d4306f9; high |
| W6 | [MIDAS Open collection](https://catalogue.ceda.ac.uk/uuid/dbd451271eb04662beade68da43546e1/) | OGL, hourly/daily UK stations, 1853 to previous full year, coverage varies by station; high |
| W7 | [MIDAS user guide](https://help.ceda.ac.uk/article/4982-midas-open-user-guide) and [hourly archive](https://data.ceda.ac.uk/badc/ukmo-midas-open/data/uk-hourly-weather-obs) | Air temperature/calculated RH fields; qc-version not automatic QC acceptance; latest listed directory v202607; high, stale 2020 FAQ not used |
| W8 | [ERA5 catalogue API](https://cds.climate.copernicus.eu/api/catalogue/v1/collections/reanalysis-era5-single-levels) | CC-BY-4.0, DOI 10.24381/cds.adbb2d47, hourly 0.25-degree reanalysis from 1940; high |
| W9 | [CDS API setup](https://cds.climate.copernicus.eu/how-to-api) | Login/account/PAT and dataset terms acceptance required by documented route; no submission made; high |
| W10 | [CIBSE weather data](https://www.cibse.org/knowledge-research/weather-data/) | 2025 v1.1, historical baseline 1994-2023, 28 zones, hourly T/RH, morphed TRY/DSY, prepayment and user licences; exact redistribution terms not retrieved; high |
| W11 | [UKCP18](https://www.metoffice.gov.uk/research/approach/collaboration/ukcp) | Observations plus projections, 60/12/2.2km models; family name not a historical product licence; high |
| W12 | [EA flood API](https://environment.data.gov.uk/flood-monitoring/doc/reference) | OGL v3, no registration, hydrology/rainfall and attribution; no T/RH pair documented in this API; high |
| W13 | [Met Office legal](https://www.metoffice.gov.uk/policies/legal), [website terms](https://www.metoffice.gov.uk/policies/tandc), [OGL v3](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) | Content grant, attribution, exclusions, automated-copy restriction; no further Met Office fetches after reading restriction; high |
| W14 | [CEDA tokens](https://help.ceda.ac.uk/article/5100-archive-access-tokens) and [CC BY](https://creativecommons.org/licenses/by/4.0/) | Access distinct from licence; attribution/change indication for CC BY; high |

Failed discovery URLs: obsolete Met Office /about-us/legal/tandc and
/about-us/legal/tandc/met-office-website; /ukcp/data; old ECMWF
How+to+download+ERA5; guessed CIBSE weather-data-faqs returned 404.
Replaced with successful current official links above, not treated as evidence.
Direct urllib CIBSE requests returned 403; web_fetch successfully read the current
page including raw main content/FAQs (not merely the truncated simplification).
`python` was absent (exit 127); used installed `python3`, no install.

## Findings, Alternatives and Decision State

Recommended candidate (product identity locked during Plan, PC-003):
HadUK-Grid administrative regions v1.3.2.ceda, UUID
386b3c1ee2054ef5ae0d73060963a9f1, observational context, OGL v3 and exact
release citation (W3-W4). W2's 1km grid is a separate alternative. Not adopted, not humidity
data retrieved. Alternative MIDAS is better for cadence but station coverage,
records and QC need authorized access. Durham is a bounded temperature-only
cross-check, not a substitute for the chosen paired source. ERA5 offers
spatial completeness but reanalysis and derived RH differ; CIBSE costs/licence
and design-year construction are unsuitable here. UKCP18/EA blanket approval
would conflate product purpose and terms.

## Open Questions, Risks and Residual Uncertainty

* Owner reuse approval UNMET for every external dataset.
* CEDA hurs/MIDAS login boundary; no authorized public humidity records obtained.
* Durham automated-access terms require owner review; do not add a downloader.
* Geographic/sample extrema do not define region-wide physical or safety limits.

## Sources and Self-check

W1-W14 are primary official retrievals with dated provenance. No private or
support/cohort data used; no worker outputs or web synthesis treated as evidence.
All three waves executed in order inline; no delegated lanes needed.
Every question answered or has precise smallest missing evidence.

## Planning Readiness

**Ready** for a bounded implementation that reports partial acceptance honestly.
Research disposition: **executed**. The record/data/approval gaps block issue
acceptance, not the independently possible comparison and local derivation.
RPI parent continuation: Plan, carrying W1-W14 and the access/approval boundaries.

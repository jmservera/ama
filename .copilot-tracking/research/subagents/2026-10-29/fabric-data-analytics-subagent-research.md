<!-- markdownlint-disable-file -->

---
title: Fabric Data and Analytics Internal Research Lane
date: 2026-10-29
---

# Cycle 1, Wave 1 Wider: Internal Data and Analytics Evidence

## Delegated Contract

| Field | Value |
| --- | --- |
| Cycle / wave | 1 / Wider |
| Lane | Internal: Fabric data, analytics, IoT, source and persistence fit |
| Parent primary artifact | .copilot-tracking/research/2026-10-29/microsoft-fabric-project-fit-research.md |
| Source baseline | 9b74ac8daaec2a880172e43161b37ac7f2c3f801 |
| Research posture | Balanced: comprehensive bounded inventory with deeper reads at data boundaries |
| Writable scope | This artifact only |
| Scope | src/importer; data, forecast, analytics, ranking and sensor code in src/core; relevant src/api analytics endpoints; tools/climate*; synthetic data dictionaries/manifests; ADR 0003; IoT plan; data-source and UX chart/KPI evidence |
| Non-goals | Fabric adoption decision, code/docs/dataset edits, private data, live/cloud queries, deployment, paid calls, installation, commit, branch or acceptance claims |

## Questions and Evidence Criteria

1. Identify implemented source formats and systems, the 60,000-stock and 980-case distinction, persistence structures, reporting, forecasts, deterministic simulations, stream/replay behavior, declared scale, schema/device-ID compatibility, synthetic/live boundary, data quality and provenance.
2. Locate an actual unmet cross-source, historical, stream, or BI requirement, if present, without treating proposals or exercise data as production needs.
3. Identify source/sink boundaries that could be relevant to Azure SQL mirroring, Blob/ADLS shortcuts, Event Hubs or Eventstream, without researching external product capabilities.
4. Separate arithmetic from declared sampling from measured workload and name the cheapest discriminating check.

Wave evidence goal: widen the factual internal inventory and map claims to implementation, neighboring tests, and current project evidence. No canonical parent IDs or adoption recommendation are assigned here.

## Research Result

* Preflight: this exact path is under .copilot-tracking/research/subagents/2026-10-29/ and is distinct from the parent primary artifact. It is the sole lane artifact written.
* Status: complete for this bounded Wider/internal lane.
* Outcome: the repository contains a useful synthetic multi-source analytical pack, a transactional Azure SQL-compatible programme store, finite synthetic sensor replay and deterministic reporting. It does not contain a demonstrated live multi-system ingestion, sustained stream, lakehouse, ADLS/Blob shortcut or BI semantic-model workload.
* No adoption recommendation: findings are constraints for the parent assessment only.

## Findings

| Local ID | Question / finding | Evidence and confidence | Fabric-relevant constraint, not recommendation |
| --- | --- | --- | --- |
| L1 | The public discovery pack intentionally imitates at least eleven source-system labels: asset extract, tracker, mailbox, assessor and contractor portals, CRM, QA/evidence logs, grant tracker, housing management, planned maintenance and programme. It is a synthetic 14-CSV analytical pack, not a connected production integration. | docs/reference/research/retrofit-synthetic-data/data-dictionary.md:113-138; docs/reference/research/retrofit-synthetic-data/README.md:346-370; manifest.json:1-29. High for fixture composition; low for production-system count. | This is the strongest candidate cross-source analytical need: joining heterogeneous historical exports and resolving identity/date/quality defects. No actual source connector, schedule, source change feed or live system is implemented. |
| L2 | The declared 60,000-home stock and the retained 980-case programme lineage are separate denominators. The public pack reports 996 property rows, 992 candidate rows, 9,859 lifecycle events and 980 resident journey rows; it also records duplicates and imperfect source matching. | docs/reference/research/retrofit-synthetic-data/README.md:39,73-91,346-370; docs/reference/research/retrofit-synthetic-data/manifest.json:1-29. High. | A lakehouse would have to preserve versioned source denominators and unknown/unlinked records, not silently merge stock and cases. The figures are synthetic, so they cannot justify capacity or cost. |
| L3 | The importer is a future/manual Excel transition boundary, not a data platform. It reads a single .xlsx values-only under 10 MiB source size and 20,000-row/200-column workbook limits; the sole declared case-list shape has six fields. Preview preserves source SHA-256, sheet and row lineage, and exports CSV/one-way XLSX with history. No HTTP, queue transport or production import is built. | src/importer/README.md:10-18; src/importer/src/zava_forward/importer/xlsx.py:14-18,89-146; src/importer/src/zava_forward/importer/mapping.py:31-44,113-166; src/importer/src/zava_forward/importer/export.py:1-74; src/importer/tests/test_excel_transition.py:107-162,374-378. High. | An analytical landing path could be relevant only if an approved operational extract programme replaces this bounded, human-reviewed transition. No Blob/ADLS sink or shortcut exists here. |
| L4 | Programme state has a portable SQLite/Azure SQL schema. `cases` carries indexed derived fields plus a JSON `body`; `recommendations` and `staff` also keep JSON bodies; `audit` is append-only. The Azure SQL dialect has `NVARCHAR(MAX)` bodies and supports an Azure SQL append-only ledger for audit. | src/core/src/zava_forward/core/sqlstore.py:39-80,192,301-416; src/core/src/zava_forward/core/mssqlstore.py:30-52,208,281-283. High. | Azure SQL is the current state authority. Mirroring or analytics extraction would need explicit treatment of JSON bodies, derived-column reconstruction, append-only audit/ledger semantics, privacy and consistency. No such extraction implementation exists. |
| L5 | Current dashboards and exports are application-local, read-only and labelled demonstration data. They aggregate synthetic cases in Python; historical progress combines returns, handoff history and quality history, identifies gaps and emits a deterministic declared forecast with explicit limits. The API exposes progress, closed-case, stats/cases CSV and ranking routes rather than a BI endpoint. | src/api/src/zava_forward/api/progress.py:241-325; src/api/src/zava_forward/api/web/progress.js:40-154; src/core/src/zava_forward/core/progress.py:25-33,539-690; src/api/src/zava_forward/api/server.py:285-331,413-435. High. | No unmet BI query is implemented: aggregation scope is bounded to cases/current dashboards and CSV export. A real request for governed cross-source trend reporting, reusable semantic KPIs or independent historical retention is missing. |
| L6 | Ranking and forecasts are deterministic, versioned exercise logic rather than ML or observed predictive analytics. Ranking is a pure policy/hash function; forecast is a declared capacity/duration scenario and returns unavailable without inputs. | src/core/src/zava_forward/core/ranking.py:1-6,22-62,126-171; src/core/src/zava_forward/core/progress.py:539-599. High. | These functions do not create a high-volume analytics need. Any future analytical platform must preserve policy/version/as-of provenance and keep scenarios distinct from measured outcomes. |
| L7 | Sensor history is generated, not device telemetry. Default backfill is synthetic, 730 days, hourly and CSV-sharded with Azure SQL DDL; it estimates size from a 20-home sample and records seed, schema/version, source revision, hashes and source-type label. The research plan records one actual synthetic full-stock run of 43,800,000 rows at one record/home/day over 730 days, separately from three/day stream accounting. | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:1-60,195-236,247-377; docs/reference/research/iot-sensor-analytics-research-plan.md:395-401,450-459; src/core/tests/test_synthetic_determinism.py:60-161. High for generated/evidence claims; not a production workload. | CSV and Azure SQL are the only implemented historical sensor stores. No ADLS/Blob analytical data lake sink, catalog or lakehouse table is present in the scoped sources. |
| L8 | The implemented stream boundary is a finite opt-in replay and receiver, not a continuously running pipeline. The API has no HTTP/startup activation; replay has a maximum 100 monitored homes/100,000 home-slots and run budgets, and the Event Hub receiver uses managed identity, validates exact bindings and writes through `SensorIngestion` to SQL. | src/api/src/zava_forward/api/iot_stream.py:1-95,145-335; src/api/src/zava_forward/api/sensor_ingestion.py:1-32; src/core/src/zava_forward/core/synthetic/sensor_stream.py:1-183; src/api/tests/test_iot_stream.py:73-203,391-583. High. | Event Hub is an intended source-only transport boundary, not a measured live stream. There is no Eventstream or downstream streaming analytics consumer. |
| L9 | Sensor consumer data has closed-schema acceptance, idempotent `(sensor_id, reading_id)` storage, delivery witnesses and separate data-quality records. It accepts synthetic-only records and requires configured control data; per-row transactions stop a batch on database failure. | src/core/src/zava_forward/core/sensor_consumer.py:20-45,135-166,210-298,340-440; docs/reference/research/iot-sensor-analytics-research-plan.md:190-237. High. | Any mirror/stream derivation must retain accepted versus rejected/replay state and the SQL data-quality boundary, rather than treating raw transport events as analytical truth. |
| L10 | There is a historical producer compatibility risk, not a Fabric requirement: legacy stock-derived IDs can be 73-character lowercase-hex sensor IDs and reading IDs longer than the consumer's former 20/40 constraints. Later canonical-key work documents a compact mapping but real device ingestion remains unverified. | docs/reference/research/iot-sensor-analytics-research-plan.md:343-358,395-401,414-459; src/core/tests/test_sensor_consumer.py:122-219. High. | Schema/device-ID reconciliation must precede any replicated stream/warehouse design. It is a correctness gate, not evidence that a streaming platform is needed. |
| L11 | ADR 0003 keeps Azure SQL as system of record, Event Hub as the proposed custom routed transport and deterministic, versioned `sensor_analysis`; retention, live identities, actual deployment and derived analysis remain open. | docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:35-60,74-139,146-200. High. | The planned source/sink shape potentially aligns with SQL and Event Hub capabilities but no Azure SQL mirroring, Blob/ADLS shortcut, Eventstream, OneLake or Fabric implementation is present. |
| L12 | Climate tools are offline hash-verified authoring/analysis tools. They consume supplied local station/reanalysis files, reject malformed/incomplete input and do not fetch or infer missing data. Their reports identify reanalysis rather than station observations and retain licence/reuse as unmet. | tools/climate_station_bounds.py:1-151; tools/climate_paired_bounds.py:1-220; docs/reference/research/iot-sensor-analytics-research-plan.md:805-868. High. | They are reproducible batch inputs, not recurring ingestion jobs. A future historical climate pipeline would first need an approved source/reuse decision and a retained source contract. |

## Inventory by Scoped Part

| Scope part | Actual implementation / data boundary | Neighboring corroboration | Uncertainty |
| --- | --- | --- | --- |
| src/importer | Values-only XLSX preview, declared case-list mapping, quarantine history and CSV/XLSX snapshot export | src/importer/tests/test_excel_transition.py:27-162,201-378 | No import HTTP/queue, downstream production source or volume beyond guards |
| src/core SQL and analytics | SQLite development store mapped to Azure SQL, JSON bodies plus indexed derived fields, audit/ledger, SQL lists and in-memory detail/exports | src/api/tests/test_mssqlstore.py:1-4,464-582,598-812 | No observed Azure SQL query profile, table size, retention, read-write contention or mirror |
| src/core ranking/forecast/progress | Pure ranking policy, deterministic historical reconstruction and constrained scenario forecast | src/core/src/zava_forward/core/ranking.py:1-171; src/core/src/zava_forward/core/progress.py:25-33,539-710 | No calibrated forecast or external reporting consumer |
| src/core sensors | Synthetic backfill, register/reading SQL DDL, provenance/manifest/hash, replay budgets and SQL consumer | src/core/tests/test_synthetic_determinism.py:60-161; src/core/tests/test_sensor_consumer.py:27-219,371-753 | No real telemetry, source credentials, production monitoring or live historical series |
| src/api analytics | Role-protected progress/closed-case/stat/case CSV/ranking views; accessible client-side charts/tables | src/api/src/zava_forward/api/server.py:285-331,413-435; src/api/src/zava_forward/api/web/progress.js:40-154 | No Power BI, semantic model, direct query or analytical API |
| src/api stream | Explicit finite Hub receiver/publisher using SDKs, bound synthetic device identities and SQL consumer | src/api/src/zava_forward/api/iot_stream.py:1-335; src/api/tests/test_iot_stream.py:194-203,391-583 | Source-only/configuration-gated, no live Azure operation or Eventstream |
| tools/climate* | Local-hash input parsing and bounded climate statistics | tools/climate_station_bounds.py:1-151; tools/climate_paired_bounds.py:1-220 | No recurring source acquisition, weather operational data or approved reuse |
| Synthetic dictionaries/manifests | Public synthetic multi-table pack and private generated/synthetic asset inventories, provenance labels and row counts | docs/reference/research/retrofit-synthetic-data/data-dictionary.md:225-242,412-460; manifest.json:1-29 | No private dataset read; only fixture metadata inspected |
| ADR 0003 and IoT plan | Azure SQL authority; Event Hub/IoT concept; deterministic sensor analysis proposal and explicit open gates | docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:74-200; docs/reference/research/iot-sensor-analytics-research-plan.md:1-123 | Architecture intent and source-only work are not live workload or acceptance evidence |
| UX/KPI evidence | Charts render current synthetic counts and accessible equivalent tables; UX evidence says richer analytics and portfolio decision journeys remain future/unavailable | src/api/src/zava_forward/api/web/progress.js:40-154; docs/reference/research/ux/customer-journeys/data.md:35-92; docs/reference/research/ux/zava-forward-prototype-profile-review.md:299-318 | No user validation, KPI governance or BI audience requirement |

## Declared Arithmetic, Separate from Measurements

* Stream-accounting declaration: $3 \times 60{,}000 = 180{,}000$ paired observations/day, an average $180{,}000 / 86{,}400 \approx 2.083$ records/second. This is not a peak, tested rate or device count.
* Sample-payload arithmetic: the documented 366-byte constructed JSON sample gives $366 \times 180{,}000 = 65{,}880{,}000$ bytes/day, approximately 65.9 MB/day decimal or 62.8 MiB/day. At the same unproven cadence for 365 days it is about 24.0 GB decimal (22.4 GiB) payload only. It excludes transport/TLS/properties/retries/rejections and SQL/index/storage overhead.
* Historical nominal arithmetic: $3 \times 60{,}000 \times 730 = 131{,}400{,}000$ records over two years, from the stated three/day scenario. The existing pre-generation estimate of 131,025,000 rows and 14.77 GiB is a different hourly-with-dropout generator estimate, not a live measurement.
* Measured synthetic result: the research plan records 43,800,000 rows, 730 per home over a complete two-year window, and 703,111,263 compressed bytes. That is one record/home/day in an exercised synthetic run, not the three/day stream scenario and not an operational workload.
* Provenance: docs/reference/research/iot-sensor-analytics-research-plan.md:95-103,239-291,395-401,450-459; src/core/src/zava_forward/core/synthetic/sensor_backfill.py:195-236.

## Unmet Requirement and Discriminating Checks

### Current evidence state

The only concrete unmet analytical requirement evidenced locally is a *synthetic discovery scenario* that needs historical joins across deliberately heterogeneous exports, cross-source identity reconciliation, mixed date formats, duplicate handling, current-state versus event-history distinction and transparent reporting. The pack itself says it was constructed for that analysis. The repository does not evidence an approved, live cross-system history or a user requirement for managed lakehouse storage, continuous streaming analytics, Fabric BI, Azure SQL mirroring, Blob/ADLS shortcuts or Eventstream.

The most concrete current technical gap is the sensor producer/consumer identifier and schema boundary, together with absent live identity/transport/retention evidence. Adding a platform before resolving that contract would preserve or amplify ambiguity rather than answer a confirmed workload need.

### Cheapest falsifiers

1. Run an owner-approved read-only source inventory against the actual candidate operational systems: source, extract/change-feed format, watermark, identity keys, historical retention, record/day, peak rate, data classification and accountable owner. One confirmed recurring multi-system historical KPI that cannot be reproduced from the current SQL/CSV extract path would falsify the present "no demonstrated lakehouse need" conclusion.
2. Execute the existing synthetic 980-case CSV pack through the simplest governed SQL staging/read-only reporting path, then document whether required joins, source-version provenance, unknowns and a chosen KPI are missing or exceed agreed refresh/query limits. This falsifies the "current SQL/CSV is sufficient for the demonstrated analytical pack" hypothesis without cloud purchase or live data.
3. Use a disposable synthetic Azure SQL/SQL Server test to measure the current JSON-body/derived-column query and append path at an agreed sample. Existing MSSQL tests are explicitly throwaway-only and offer a local harness; no such measured workload result was found. A failing target should identify the exact query/append condition before selecting a platform.
4. For streaming, validate the intended device-ID mapping and send a bounded synthetic replay through the existing receiver with actual approved transport only after separate authorization. Evidence needed: observed peak/burst, partition lag, replay/recovery, retained SQL/DQ outcome and cost/headroom. The current finite replay tests cannot falsify or prove a production streaming requirement.

## Source and Sink Inventory

| Candidate boundary | Observed state | Missing fact |
| --- | --- | --- |
| Azure SQL programme state | Implemented portable schema and Azure SQL dialect; state authority remains SQL | Mirroring configuration, scope, latency, retention and approval |
| JSON case bodies / audit ledger | Stored inside SQL (`body`, audit detail); Azure ledger support for audit | Analytical projection schema, change-data semantics and governance |
| Synthetic CSV operating pack | Repository CSV/JSON manifest fixture for discovery | Operational export endpoint, landing zone, refresh/watermark and real source terms |
| XLSX transition | Read-only human-review preview and values-only output | Approved inbound system, repeated operational volume and authoritative merge control |
| Sensor backfill | Generated CSV shards and optional SQL loader | Data-lake target, ongoing retention, measured query/access pattern |
| IoT/Event Hub | Source-only custom Event Hub/IoT design plus finite SDK receiver/publisher | Provisioned identities, endpoint/route, live traffic, partition/replay operations |
| Blob documents/digests | Blob appears for documents and immutable ledger digests outside this lane's analytics path | Any analytical data-lake use or shortcut |
| Eventstream / OneLake / ADLS / Power BI | No implementation found in scoped code/docs | Any user-approved workload, capacity/licensing, security or operating model |

## Gaps, Conflicts and Parent-Synthesis Pointers

* The data dictionary/README uses synthetic source-system names to model a multi-system discovery problem. Do not equate these with Zava North Homes integrations.
* 60,000 stock and 980 cases must remain separately labelled. The 60,000 stock generator/private assets were not opened; 980 is not the whole stock.
* Historical row counts have different parameters: 131.4M is three/day arithmetic, 131.025M is an estimate with an hourly/dropout generator context, and 43.8M is a measured synthetic one/day result. They must not be collapsed.
* Existing Event Hub/IoT evidence is source-only or bounded synthetic engineering; it is not a live stream, event rate, Fabric Eventstream requirement or acceptance.
* `sensor_analysis` is specified in ADR intent but no derived-analysis implementation/screen was found in the scoped code. The analytical method plan remains open and does not establish a stream-analytics workload.
* Source formats in the synthetic operating pack include CSV, JSON manifests, Excel/xlsx transition and private JSON/SQL seed representations. Actual company formats, number of systems, integration rights and growth rates are unavailable.
* No production measurements of Azure SQL performance, storage growth, BI concurrency, stream throughput, device count, retention, RPO/RTO, licence/capacity or operational owner/team capability were found.

## Files Examined

* src/importer/README.md
* src/importer/src/zava_forward/importer/xlsx.py
* src/importer/src/zava_forward/importer/mapping.py
* src/importer/src/zava_forward/importer/export.py
* src/importer/tests/test_excel_transition.py
* src/core/src/zava_forward/core/sqlstore.py
* src/core/src/zava_forward/core/mssqlstore.py
* src/core/src/zava_forward/core/ranking.py
* src/core/src/zava_forward/core/progress.py
* src/core/src/zava_forward/core/sensor_consumer.py
* src/core/src/zava_forward/core/synthetic/sensor_backfill.py
* src/core/src/zava_forward/core/synthetic/sensor_stream.py
* src/core/tests/test_sensor_consumer.py
* src/core/tests/test_synthetic_determinism.py
* src/api/src/zava_forward/api/server.py
* src/api/src/zava_forward/api/progress.py
* src/api/src/zava_forward/api/sensor_ingestion.py
* src/api/src/zava_forward/api/iot_stream.py
* src/api/src/zava_forward/api/web/progress.js
* src/api/tests/test_mssqlstore.py
* src/api/tests/test_iot_stream.py
* tools/climate_station_bounds.py
* tools/climate_paired_bounds.py
* docs/adrs/0003-journey-derived-capabilities-runtime-fit.md
* docs/reference/research/iot-sensor-analytics-research-plan.md
* docs/reference/research/retrofit-synthetic-data/README.md
* docs/reference/research/retrofit-synthetic-data/data-dictionary.md
* docs/reference/research/retrofit-synthetic-data/manifest.json
* docs/reference/research/retrofit-synthetic-data/scenario-manifest.json
* docs/reference/research/ux/customer-journeys/data.md
* docs/reference/research/ux/zava-forward-prototype-profile-review.md

## Stop Decision

Stop reason: delegated lane criteria met. The required internal implementation/data-boundary inventory, tests, arithmetic, uncertainties and falsifying checks are recorded. Current Fabric product fit, cost/licensing, tenant capacity and final recommendation remain for parent synthesis and other lanes.

## Dated Cadence Correction (2026-10-30, Refs #558)

The original arithmetic bullet and gaps summary above incorrectly describe
131,025,000 rows as an hourly/dropout estimate. Those statements are retained
as original research, not current sizing guidance. The controlling
[backfill estimate record](../../../../docs/reference/research/iot-sensor-analytics-research-plan.md#historical-backfill-stack-boundary-2026-10-27-refs-177)
specifies `estimate(homes=60000, days=730, cadence=480)`, with cadence in
minutes and a 20-home legacy sample.

Thus 1440 / 480 = three paired observations/home/day before dropout:
60,000 x 730 x 3 = 131,400,000 nominal records. The 131,025,000-row/14.77-GiB
estimate is the same three/day scenario after sampled dropout, not hourly
sampling, a measured generated run or an hourly storage bound. The generator's
hourly default in L7 does not override the explicit estimate parameter.
A hypothetical complete hourly history is 60,000 x 730 x 24 = 1,051,200,000
rows before dropout. The separate recorded 43,800,000-row generated run is
daily; none of these figures proves production throughput or Fabric sizing.
<!-- markdownlint-disable-file -->

---
title: Fabric operational architecture internal research lane
date: 2026-10-29
---

# Cycle 1, Wave 1 Wider: Internal Operational Architecture

## Delegated Input Contract

| Field | Value |
| --- | --- |
| Cycle / wave | 1 / Wider |
| Lane type | Internal |
| Topic | Microsoft Fabric project-fit: operational architecture, authority and interface boundaries |
| Parent primary artifact | .copilot-tracking/research/2026-10-29/microsoft-fabric-project-fit-research.md |
| Source baseline | 9b74ac8daaec2a880172e43161b37ac7f2c3f801 on clean initial jmservera/fabric-research |
| Research posture | Balanced, with comprehensive bounded component coverage |
| Explicit limit | No arbitrary source ceiling; stop at sufficient material evidence. Read-only application/infrastructure, no live/private data access, installs, exhaustive test runs, branches, commits or deployments. |

## Questions and Criteria

* Q1: What controls programme state, deterministic decisions, approvals, permissions, orchestration, bounded AI/model fallback, per-user memory/chat and resident communications?
* Q2: Which behaviours are source-implemented versus proposals, unaccepted or live-unknown?
* Q3: Which workloads could benefit from a separate analytical platform, and which must retain transactional or human authority?
* Criteria: inspect each scoped project README, nearest controlling implementation and neighboring tests; include the scoped ADRs, BRD/PRD and existing staff/resident design evidence; distinguish source observations, test evidence and claims.

## Scope and Non-goals

* Included: src/core, src/agents, src/api, src/orchestrator; ADRs 0001-0005; relevant BRD/PRD and staff/resident design evidence.
* Excluded: Fabric adoption decision, source/doc changes outside this artifact, infrastructure changes, private datasets, live acceptance claims and exhaustive testing.
* Wider evidence goal: establish a breadth inventory of existing authority, persistence, interface and analytical-demand boundaries to support parent synthesis.

## Status

* Status: complete; README, ADR, controlling-source and neighboring-test review completed.
* Path preflight: this artifact is under .copilot-tracking/research/subagents/2026-10-29/ and differs from the parent primary artifact above.

## Interim Evidence Log

| Local ID | Question | Observation | Evidence and status | Fabric-fit relationship | Confidence |
| --- | --- | --- | --- | --- | --- |
| I1 | Q1/Q3 | The written product contract makes the workbench API the only controlled write path for case edits, approvals and accepted suggestions. Its state store owns versioned relationships, workflow history, tasks, handoffs and approval records; the proposed orchestrator is subordinate to API state and permissions. | Proposal/requirement, not proof of complete implementation: docs/prds/zava-forward-retrofit-programme-demonstrator.md:251-259. | Supports retaining transactional authority outside an analytical platform; a downstream analytical copy must not become an approval/write path. | High |
| I2 | Q1/Q2 | The actual `Store` composes workflow, quality, procurement, finance, grants, signoff, resident-decision, governance, continuity and document controls. Its gate logic holds a case on unconfirmed funding, unreleased hazards, resident and technical checks; its rank cache calls deterministic ranking. | Source observation: src/core/src/zava_forward/core/store.py:44-78, 153-193. Existing tests not yet read in this lane. | Supports a single operational authority with analytical workloads derived from controlled state, not replacing it. | High |
| I3 | Q1/Q3 | SQL persistence is implemented for cases, derived/query fields, recommendations and an append-only audit ledger with no-update/no-delete triggers. `SqlStore` initializes schema, migrations, indexes and a cross-process synchronization path. | Source observation: src/core/src/zava_forward/core/sqlstore.py:1-24, 31-63, 151-222. Azure SQL parity is described in comments but this read does not prove a live Azure deployment. | Candidate analytical workload is read-only reporting/history from SQL; the source does not establish a need to duplicate transactional data into a second store. | High |
| I4 | Q1/Q2 | Chat threads, messages, opt-in memory and memory controls are separate tables, owner-key filtered and optimistic-concurrency protected. Message content is excluded from the audit ledger; memory is explicitly barred from evidence citations. | Source observation: src/core/src/zava_forward/core/chatthreads.py:1-55, 79-253, 276-380. ADR 0004 accepts direction but leaves DPO/legal, retention, access, thresholds and live personal-data activation open: docs/adrs/0004-per-user-agent-chat-and-memory.md:1-18, 87-145, 183-224. | Sensitive conversational data is not a generic reporting feed. Any future analytic use needs separate purpose, access and retention authority. | High |
| I5 | Q1/Q2 | Five assistant capabilities have closed field allowlists by task and role, explicit output limits/citation validation, and a manual-work failure outcome. The stated service has no domain-write capability. | Source observation: src/core/src/zava_forward/core/assistants.py:1-49, 74-188, 304-350. README reports the current offline chat golden run intentionally exits 1 because an unsupported-claim scenario remains a critical failure: src/agents/README.md:55-77. | AI outputs remain bounded proposal data, not analytical facts or operational authority; reported local evidence does not establish model/human acceptance. | High |
| I6 | Q1/Q3 | Current API staff chat explicitly exposes five selected advisory skills, re-reads the role-scoped case projection each turn, returns workflow-only help on model failure, and stores masked questions only when synthetic privacy references pass. | Source/README claim plus declared focused local test route: src/api/README.md:154-205. It explicitly excludes live employee-site/model/SQL/human acceptance. | Existing chat's privacy/role boundary narrows any analytical extraction; no platform should bypass the API projection. | Medium |
| I7 | Q1/Q3 | Resident assistance is a separate, bounded own-case feature: a constrained selector sees only safe mapped answer data, falls back deterministically, uses disabled-by-default managed identity, and has a permanent SQL reservation/accounting model. | Design/source-status evidence: docs/architecture/resident-assistant-prototype.md:7-48, 113-160. Provisioning is recorded but SQL migration, running configuration and authenticated inference remain separately unevidenced. | Resident communications and usage accounting should retain their existing bounded/purpose-specific authority; they are not a case for broad analytical copying. | High |
| I8 | Q1/Q3 | The current API has a synthetic-only progress dashboard and manager-only closed-case archive. It labels lifecycle coverage/unknowns and exposes semantic tables; it is not a general operational BI service. | Source/README claim plus focused-test command: src/api/README.md:74-150. Constructed loopback checks are engineering evidence, not live acceptance. | This is the clearest present reporting workload. A separate analytical platform could later serve governed aggregate history, but source evidence does not establish actual volume, consumer need or tenant readiness. | High |
| I9 | Q1/Q2 | Orchestrator code is narrow: digest verification/publication, source monitoring and bounded document rescans. Documentation states the scheduled jobs are separate images; hosted executions remain unproven. | Source/README observation: src/orchestrator/README.md:1-15, 17-70, 72-155. | It does not implement a general workflow orchestration or analytics pipeline; a Fabric pipeline would add a new operational surface rather than replace deployed orchestration. | High |
| I10 | Q2/Q3 | ADR 0001/0002 describe a broader queue/worker architecture as proposed/deferred while the shared API/SQL realization is current. ADR 0003 accepts an exercise IoT transport choice but preserves SQL as system of record, deterministic derived signals and human review; live transport/provisioning/analysis are unmet. | Design and acceptance boundary: docs/adrs/0001-azure-architecture.md:1-64, 69-113, 156-185; docs/adrs/0002-pilot-readiness-architecture.md:78-157; docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:1-22, 56-143, 166-180. | Potential analytical candidates are synthetic sensor history and aggregate portfolio reporting, but they must remain downstream of SQL and human review. | High |
| I11 | Q1/Q2 | The real SQL Server/Azure SQL adapter uses Entra authentication (managed identity by default), T-SQL case/audit/chat tables, an application lock for serialized writes and append-only ledger enforcement. The test suite is opt-in and explicitly requires a disposable database. | Source observation: src/core/src/zava_forward/core/mssqlstore.py:1-21, 28-83, 91-120, 203-299. Neighboring test evidence: src/api/tests/test_mssqlstore.py:1-42, 43-184 asserts constructed data across independent SQL sessions, but is skipped unless `ZF_TEST_MSSQL=1`; no live Azure execution was run in this lane. | An analytical platform cannot substitute for the concurrent transactional/ledger contract. A database replica/export would need access control and reconciliation design, none evidenced here. | High |
| I12 | Q1/Q3 | Sensor processing stores a closed synthetic observation schema, controls, delivery receipts and restricted DQ exceptions. It admits only mapped, consented, calibrated and in-order readings; accepted records append by `(sensor_id, reading_id)` and rejection creates a human-route exception. The reader schema includes raw observation body and sensitive-ish device/home linkage. | Source observation: src/core/src/zava_forward/core/sensor_consumer.py:240-367, 472-636; src/core/src/zava_forward/core/synthetic/sensor_backfill.py:53-61. Neighboring test evidence: src/core/tests/test_sensor_consumer.py:1-123 covers local constructed SQL replay, conflicting content and consent/calibration/identity rejection. No Hub, real device, Azure SQL or throughput test was run. | A separate analytical platform could analyze appropriately governed retained synthetic sensor history. It must not bypass admission/DQ/human-review controls or treat the finite 1..100 generator limits as real scale evidence. | High |

## Initial Component Inventory

| Component/interface | Observed responsibility | Evidence status |
| --- | --- | --- |
| src/core | Domain store, SQL abstraction, workflow/control mixins, deterministic ranking, bounded assistants and chat persistence | Source and targeted SQL/chat/sensor tests inspected; local/constructed evidence only |
| src/agents | Offline evaluation harness and golden data; five runtime assistant contracts remain in core | README inspected; reported test evidence is synthetic/local |
| src/api | Staff workbench/API, chat, case views, progress/closed-case reporting, resident demo/preview routes | Source and targeted chat/dashboard/resident/SQL tests inspected; live acceptance unknown |
| src/orchestrator | Ledger digest, source-monitor and document-rescan jobs | Source/README and targeted digest test inspected; no general workflow scheduler observed |
| Staff interface | API workbench with role-projected cases, explicit advisory chat and synthetic dashboard | Implemented source/documentation; live acceptance unknown |
| Resident interface | Optional own-case prototype/preview with deterministic and bounded-AI paths | Proposal/partially implemented design; activation and resident acceptance remain unknown/unmet |

## Source Observations, Test Evidence and Claims

* Source observations establish code-level contracts only. The API dispatches all POST mutations through authenticated, role-gated server routes and returns conflict/gate failures instead of accepting a silent transition: src/api/src/zava_forward/api/server.py:826-1096. Its staff chat route derives owner from the signed-in user, uses a constrained panel, permits a separate proposal request only and returns controlled errors: src/api/src/zava_forward/api/server.py:638-747.
* Deterministic authority is implemented in code: the ranking module is a pure policy/version/hash based order with a case-ID tie break and does not consult AI: src/core/src/zava_forward/core/ranking.py:1-12, 45-123. Workflow actions require a role, named user and controlled change provenance before handoff/state mutation: src/core/src/zava_forward/core/workflows.py:1-15, 96-183, 199-339.
* Permission and sensitive-field control is implemented at the server/projection boundary, not in a reporting product. Entra trusted-proxy authentication rejects missing/mismatched tenant/object/role claims; application role comes from Entra, not the staff file: src/api/src/zava_forward/api/auth.py:1-11, 99-166. Each chat turn re-reads role and case projection, masks content and withholds action-shaped or withheld-field replies: src/core/src/zava_forward/core/chat_isolation.py:1-14, 58-154.
* Reporting is deliberately synthetic-only. Progress filters admitted synthetic cases, marks malformed/partial lifecycle history unknown and produces demonstration aggregates: src/api/src/zava_forward/api/progress.py:1-19, 52-140, 217-300. HTTP requires an allowed role and routes `/api/progress` through that reader: src/api/src/zava_forward/api/server.py:279-300.
* Test evidence is local/constructed rather than acceptance evidence. The SQLite store tests assert restart persistence, cross-process refresh, stale-write refusal, gate rollback and ledger tamper detection: src/core/tests/test_sqlstore.py:24-139. Chat tests assert owner isolation, role recheck, masking and no mutation from injected content: src/api/tests/test_chat_isolation.py:1-31, 74-250; bounded panel tests assert cited output, refusal and workflow-only fallback: src/api/tests/test_chat_panel.py:1-8, 77-176. The dashboard test uses only labelled synthetic rows and explicitly includes a non-synthetic private-name exclusion probe: src/api/tests/test_progress_dashboard.py:1-93.
* Claims/proposals remain distinct. ADR 0004 is an accepted staff-chat direction but not DPO/legal/retention/live-personal-data approval: docs/adrs/0004-per-user-agent-chat-and-memory.md:1-18, 183-224. ADR 0005 permits synthetic regulatory-assistant development only and denies legal/action/consent/communication authority: docs/adrs/0005-regulatory-compliance-assistant.md:1-34, 111-206. The unsigned PRD still labels its broad decomposition as proposed and its optional resident portal/communication feature as separately gated: docs/prds/zava-forward-retrofit-programme-demonstrator.md:240-290; docs/case_study_48_addendum.md:13-65.

## Material Constraints and Risks for Parent Synthesis

* Do not move programme-state, approval, role/field authorization, case workflow, audit/ledger, consent, resident decision or sensor-admission authority into a separate analytical platform. The implementation and requirements position API plus SQL as authority, while dashboards are read-only and synthetic.
* Preserve data minimisation and audience filtering in any analytics feed. Case bodies contain resident/contact, adjustment, financial, supplier and communication material; chat tables contain masked free text and opt-in memory, and sensor delivery keeps observation bodies plus home/device linkage.
* Avoid representing the present reporting/dashboard or sensor fixtures as a demonstrated Fabric-scale workload. Progress is synthetic-only; sensor generation/consumer paths are bounded constructed exercises; no tenant capacity, operating demand, actual telemetry volume or live analytics consumer evidence was examined.
* A Fabric-like analytical sidecar could be evaluated only for governed aggregate portfolio/dashboard history, reconciliation, long-retention synthetic sensor trend exploration or cross-source read models. It must have a documented one-way, minimum-necessary export/reconciliation boundary, preserve source/as-of/unknown/denominator semantics, and leave all actions with the API/SQL/humans.
* Current source risks include data duplication across `cases.body` JSON and derived columns, application-filtered chat isolation (ADR 0004 leaves database row-level security undecided), loss of semantic coverage if reporting copies only aggregates, and incorrect inference that local constructed tests establish live SQL, model, IoT, resident or accessibility acceptance.

## Evidence Gaps Identified

* Obtain separately scoped deployment or operational evidence to distinguish local source parity from Azure SQL/live state evidence.
* Obtain an approved data/retention/access contract before extracting reporting data beyond the current role-filtered views.
* Establish a real analytical demand, decision-user and scale baseline before treating any analytical platform as required.

## Completion, Gaps and Stop Decision

### Questions Answered

* Q1: Code and requirements locate authority in the API/core Store and SQL abstraction: deterministic ranking/workflow gates, server-side role and field projection, human-owned approvals, append-only audit, bounded proposal/chat paths and resident/sensor controls.
* Q2: Source implementation and local constructed test coverage exist for SQL/store behavior, chat isolation/fallback, dashboards and sensor admission. Broad worker topology, resident operational activation, live model/IoT, tenant capacity/cost, DPO/legal approval and human acceptance remain proposals, unaccepted or live-unknown as stated above.
* Q3: The source supports only downstream analytical candidates, principally synthetic-only progress/cohort reporting and retained synthetic sensor history. It does not support substituting analytics for programme transaction, permission, consent, approval, audit or communications authority.

### Useful Deeper Questions

* What exact existing SQL schema/record counts, retention, update rate and query pain exist in the deployed exercise, and which read model cannot be met through Azure SQL plus the current dashboard/export contract?
* Which minimum fields, identifiers, residency/retention rules and role model would govern a one-way analytics feed, especially for `cases.body`, chat, resident and sensor-delivery data?
* What real decision users, refresh latency, historical window and cross-system sources justify an analytical platform beyond the current synthetic progress/coordinator/CSV outputs?
* What reconciliation, late-arriving-event, correction and deletion/hold behaviour must a downstream analytical copy preserve without becoming a parallel case authority?

### Files Examined

* Parent brief; case-study original/addendum; knowledge-base index/memory; all scoped project READMEs.
* ADRs 0001-0005; relevant PRD/BRD/component-contract passages; resident assistant and employee-workspace design evidence.
* Core Store, SQLite/SQL Server stores, workflows, ranking, chat threads/isolation, assistants and sensor consumer/schema; API auth/server/progress/resident-chat; orchestrator README; targeted SQL/chat/dashboard/sensor/resident/orchestrator tests.

### Limitations

* No application tests, deployments, live/private dataset reads, Azure/Fabric calls, installs or exhaustive suites were run. Test evidence is read from source, not rerun.
* This lane did not inspect importer/infra or perform external Fabric product research; those are outside the delegated bounded scope.
* Line evidence identifies the inspected baseline source. It cannot prove the currently deployed image, live Azure SQL contents, operational permissions, real user need, performance, cost or acceptance.

### Stop Decision

* Status: Complete.
* Stop reason: sufficient material evidence and component coverage for the bounded Wider internal operational-architecture lane; remaining questions require parent synthesis, external product evidence or separately scoped deeper/live evidence.

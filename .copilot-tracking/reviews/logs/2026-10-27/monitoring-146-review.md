---
title: "Independent RPI Review: monitoring task 146"
description: "One bounded post-implementation review of the monitoring candidate."
ms.date: 2026-10-27
---

## Opening Review State

* Interpreted review goal: independently assess task #146 authored Bicep and documentation against approved scope, critique and honestly bounded evidence.
* Review scope: complete supplied task artifact set and source diff from f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc to 64148474e6c6e8cbedfeb09b1f4e9a3775b15318.
* Evidence readiness: supplied research, plan, phase details, critique and changes paths identified; detailed comparison pending.
* Acceptance basis: issue #146, current plan and critique dispositions, with explicit authoring-only user constraints.
* First comparison boundary: task artifacts versus committed Bicep, workbook and runbook changes; no live deployment acceptance.
* Active read-only boundaries: only this canonical review record may be written. Parent session state is dirty and excluded; no source, plan, tests, secrets or private datasets may be changed or read.
* Initial blockers: no KQL, Azure or portal execution evidence; live activation, ownership, privacy and OD51 cannot be assumed. No heavy or --all gate is authorized.

## Scope and Evidence

* Task: #146, Monitoring coverage: alerts, dashboards and runbooks.
* Review date: 2026-10-27.
* Base: f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc.
* Exact assessed source commit and HEAD: 64148474e6c6e8cbedfeb09b1f4e9a3775b15318.
* Boundary: the complete 13-file committed diff, including the dated task evidence and committed session record; the latter is workflow evidence, not monitoring functionality. Independent byte comparisons confirmed all 12 non-session files still match that commit.
* The existing dirty .copilot-tracking/rpi-sessions/2026-10-27/monitoring-146-state.json belongs to the parent, is excluded from source assessment and was not changed by Review.
* Assessed implementation: infra/main.bicep, infra/modules/operationalMonitoring.bicep, infra/monitoring-workbook.json, infra/monitoring-runbooks.md, infra/README.md, docs/reference/README.md and docs/reference/log.md.
* Compared artifacts: .copilot-tracking/research/2026-10-27/monitoring-146-research.md; .copilot-tracking/plans/2026-10-27/monitoring-146-plan.md; .copilot-tracking/details/2026-10-27/monitoring-146-phase-details.md; .copilot-tracking/reviews/2026-10-27/monitoring-146-plan-critique.md; .copilot-tracking/changes/2026-10-27/monitoring-146-changes.md.
* Read issue #146 and its 2026-10-27 owner comment with `gh issue view 146 --json title,body,comments`. All four base, eight RAI and three tokenomics criteria remain unchecked. The comment explicitly reserves actual owners and live thresholds for human decisions.
* Context: case-study original/addendum, reference index and owner memory; existing container job names/conditions, monitoring resources, Key Vault rules and IoT budget predicates. Memory was context, not acceptance evidence.
* Inspected the supplied external validation helper as source without executing it. The recorded generated output location was not read or modified. No private data, secrets, .env, deployment, application/test edits or nested delegation were used.
* The delivered Azure workbook is dashboard configuration, not an application-web redesign; this review makes no web accessibility or portal-rendering acceptance claim.

## Execution Status

* Execution status: Complete.
* This means the one independent Review completed the supplied source/evidence comparison. It does not mean all issue implementation or operational acceptance ran.
* P01/P02 source-authoring work is complete on the available evidence. P03-T01 is fulfilled by this record; the parent owns any marker update. P03-T02 draft publication remains pending and outside this review's write authority.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01, FR1, AC1 | Disabled job/IoT candidates and main wiring | Reconciled | Normal/demo names, optional auth job, independent IoT conditions and action group align with existing source. |
| P01-T01, FR2, AC2 | Workspace workbook, aggregate weighted samples and missing states | Reconciled within source boundary | Schema/source checks are recorded, not KQL execution. Cost and AI feeds remain explicitly absent. |
| P01-T02, FR3/FR4, AC3/AC4 | Runbook catalogue, 15-row matrix and ledger override | Reconciled | 24 distinct entries; 26-hour outer range and predicate; original thresholds/names preserved. |
| P01-T03 | Infra/reference navigation and append-only log | Reconciled | Links describe source-only delivery and unmet gates. Original case study and memory unchanged. |
| P02-T01, AC5 | Compilation, combined 87-test result and external source assertions | Reconciled as reported evidence | Initial failure/correction preserved. No new committed tests or heavy gate. |
| P02-T02 | Explicit human/runtime gaps and validation limitations | Reconciled | No issue acceptance, live threshold, privacy or financial approval invented. |
| P03-T01/P03-T02 | Review and draft publication handoff | Pending at supplied boundary, appropriate | This record supplies the one Review; parent must preserve outcome and publish only the requested draft with Refs #146. |
| Follow-Up Items | Owners, producers, privacy and Finance | Reconciled | Explicitly outside active authoring completion and routed below, not silently added to implementation. |

## Completed Work Assessment

### Candidate wiring and activation

* Existing containerapps.bicep authors orchestrator, ledger verification and import jobs only with deployWorkloads and deployBackgroundWorkloads. main.bicep passes deployApplications as deployWorkloads. The new job array uses the same conjunction; environment-only and API-only paths do not acquire absent-job alerts.
* Normal suffixes orchestrator/ledger-verify/import/auth-renewal and demo suffixes orch/audit/load/auth match actual job definitions. applicationPrefix adds the demo generation once. The auth candidate requires enableEntraTokenStore, which supplies the existing token-maintenance identity used by the job condition.
* The module uses the stable shared prefix for backing-service alert names, actual application job names for job-scoped rules, the existing IoT resource ID and existing action group. Explicit guard/apps dependencies and output references retain ordering; no identity, endpoint or telemetry platform is added.
* New rule enablement is the conjunction of the false-default switch and nonempty trimmed approval reference. False remains false with a reference; true with empty/whitespace remains false. A nonempty reference is intentionally not approval authentication. Existing enabled alerts are unaffected.
* Job Executions/Maximum with proposed state=Failed is correctly described as a presence candidate, not an exact execution count. Four IoT Total rules have independent single criteria and no invented device dimensions. Provider values and delivery remain activation checks, not proven operation.
* No implementation defect was identified in this wiring.

### Ledger range and existing behaviour

* The only ledger source change adds overrideQueryTimeRange PT26H while retaining P1D evaluation window, hourly evaluation, LessThan 1, Count, existing scope/actions/name/severity and explicit ago(26h).
* This addresses the prior 24-hour outer query bound instead of merely restating an inner predicate. Actual console table/schema/job matching and hosted verification remain unverified, as already disclosed.
* The catalogue accurately distinguishes Foundry ClientErrors from throttle-only evidence, digest marker matches from failed job detection, and actual80/forecast100 notifications from a hard cap.

### Workbook source, schema and missing data

* Refreshed the two official Microsoft table references on 2026-10-27. AppRequests declares TimeGenerated datetime, _ResourceId string, ItemCount int, Success bool and DurationMs real. AppAvailabilityResults declares the same fields used by its query. The workbook's typed empty datatables and projections match those published types.
* Both queries use workspace queryType 0/resourceType, the exact Application Insights resource filter, selected TimeRange, window/as-of fields and weighted ItemCount denominators. AppRequests calculates weighted failures and percentilew DurationMs; availability uses its own test samples, not request success.
* The typed empty union with isfuzzy=true is a source-level absent-table strategy. Summarize yields aggregate rows for no samples; zero denominators become null measurements and Insufficient. Invalid sample fields are counted and force Insufficient rather than clean acceptance. A genuine observed zero failure count is distinct from missing data.
* Permission, schema and query failures are not programmatically converted into status rows. Static text explicitly labels these Blocked even if the query panel displays an error. This matches the revised plan's qualified contract; it is not evidence that error handling or fallback has executed successfully in KQL.
* The official workbook JSON Schema pass is implementation-reported structural evidence. The inspected helper uses string assertions for missing/empty/invalid/error contracts and a separate constructed arithmetic oracle; it does not interpret queries. No runtime/path coverage is inferred from those assertions.
* No prompts, raw text, properties, identities, IPs, URLs, readings or chat are projected. Projection is not ingestion redaction. Source privacy acceptance remains expressly unmet.
* Budget substitution displays configuration in billing currency, not observed spend. Actual/forecast costs and variance remain Unknown/unreconciled. AI usage, prices and harm indicators remain disconnected/Blocked. No live budget, OD-51 decision, SLO or availability attainment is invented.

### Runbooks and complete issue matrix

* Reconciled eight existing rules, four budget notification conditions, eight candidate anchors including optional auth, and four distinct missing-signal procedures: 24 unique entries.
* Each entry contains proposed routing, triage, bounded response and recovery evidence, directly or by explicit shared-response reference. Common guidance requires actual primary/backup appointment and escalation approval; proposed roles are not presented as named owners.
* The matrix contains all B1-B4, R1-R8 and T1-T3 rows. Missing poison signals, incident integration, repeated-event/window reconciliation, disabled-task ownership/manual routes, source privacy controls and financial reconciliation remain visible.
* Manual/emergency routes, resident consent, restricted evidence and separate human restart/activation remain intact. No queue purge/replay, digest replacement/deletion, credential disclosure or automatic task restart is authorized.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Update and trigger | Reconciliation and decision assessment |
| --- | --- | --- |
| P01-T01/P02-T01, PC-001 | Named table types, typed fallback, invalid fields, weighted denominators and error caveat | Present in details, workbook and changes. Ordinary direct critique correction; execution limitations explicit. No divergent platform or producer decision. |
| P01-T01/P02-T01, PC-002 | Enumerated deployment/name and activation combinations, guard chain and independent IoT rules | Reflected in source and inspected helper. Reported 32 deployment/name and six activation combinations match its loops. No new live approval assumed. |
| P01-T02/P02-T02, PC-003 | Enumerated 12 existing entries, eight candidates, four gaps and 15 criteria | Source predicates and authored catalogue reconcile; no omission found. |
| P01-T01 shared prefix | Existing policy regression found demo-specific backing-service prefix | Changes preserve original failure and correction. Current prefix is shared; job names remain demo-specific. This preserves approved intent and is not a significant/divergent revision. |
| P02-T01, PC-004 | Plan rejects critique's execution-path prohibition and records external output | Disposition and original critique both preserved. Historical parent execution authority cannot be independently established from source artifacts alone; review does not certify that historical path choice. Current Review did not execute the helper, access that output path or repeat its temporary-file behaviour. |
| P03 and Follow-Up Items | Keep publication draft-only and defer operational acceptance | Consistent across plan/details/changes and current user instruction. No active scope expansion or invented approval. |

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with four Medium findings; it was not overwritten or re-run.
* PC-001, PC-002 and PC-003 have explicit applied dispositions and source/evidence counterparts.
* PC-004 has an explicit rejection and rationale, not a false claim of application. The competing historical execution-constraint statements are retained as a provenance limitation; no source correctness conclusion relies on resolving that conflict.
* No significant/divergent authoring choice or unapproved active implementation expansion was found. Naming correction and direct critique refinements preserve confirmed user intent; no fresh planning/critique cycle is required for them.
* There is no evidence of dependent work proceeding past a newly accepted human activation decision; activation remains blocked.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Owner appointments, thresholds, windows, recipients and activation | Human authorization, not Bicep authoring | Project owner and actual appointed Operations/incident leads | Open; RV-001 distinct activation follow-up. |
| Poison/AI/harm aggregates and incident integration | Requires application/runtime producers prohibited in this task | Engineering with competent task and incident owners | Open; RV-002 distinct runtime follow-up. |
| Diagnostic exclusion and restricted retention | Existing ingestion controls and qualified privacy approval not delivered | Engineering and DPO/Compliance | Open; RV-003 distinct privacy follow-up. |
| OD-51, price source and financial reconciliation | Unapproved Finance decisions and missing feeds | Finance with engineering | Open; RV-004 distinct financial follow-up. |

These are not defects in the accepted authoring direction or new active P01/P02 tasks.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Operational verification and actual monitoring appointments remain open

* Class: residual work; non-blocking for disabled source authoring, blocking for activation or operational acceptance.
* Related scope: P01-T01, P03-T02, B1-B3, R1/R3/R5/R7 and T3; plan owner follow-up.
* Evidence: infra/modules/operationalMonitoring.bicep defaults disabled; infra/monitoring-workbook.json and infra/monitoring-runbooks.md explicitly disclose absent KQL/portal execution, unverified metric state values, no notification drill and proposed-only owners. Changes records the same limits.
* Impact: authored definitions cannot establish table fallback behaviour, deployed ingestion/availability, delivered alerts, staffed response or named-human live approval.
* Destination: distinct operational activation/verification follow-up, owned by the project owner and subsequently appointed operators; not a current rpi-implement defect.
* Smallest useful next action: record actual primary/backup owners and approved windows/thresholds/recipients, then separately authorize controlled KQL absent/empty/invalid/error checks, portal inspection, metric/dimension verification and delivered/resolved notification drills. Retain disabled status until accepted evidence exists.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Poison, AI-limit and harm monitoring still require runtime delivery

* Class: residual work; non-blocking for this authoring scope, blocking for whole-issue B1, R1-R5/R8 and T1 acceptance.
* Evidence: infra/monitoring-runbooks.md explicitly marks both poison queues, AI-limit aggregates and RAI incident triggers as missing signals; the workbook marks these Blocked/Insufficient. The plan and changes defer runtime producers.
* Impact: no installed poison-specific depth/age alert or complete capability/period breach signal, owned harm-to-incident suspension integration, durable restart reconciliation or complete review-effort/cohort evidence is established.
* Destination: distinct runtime monitoring follow-up, Engineering with competent task and incident owners.
* Smallest useful next action: scope safe aggregates and durable integration through existing SQL audit/report/incident surfaces under separate authority; preserve manual routes and independently approved human restart. Do not substitute service-wide queue counts or future IoT dependency.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Aggregate output does not establish source-side diagnostic exclusion

* Class: residual work; non-blocking for the metrics-only addition, blocking for B4/R6 and privacy acceptance.
* Evidence: infra/monitoring-runbooks.md, Workbook and Privacy Boundary, identifies existing allLogs/audit/instrumentation exclusions as unproven; issue #146 requires diagnostic exclusion. No source-side redaction implementation or privacy approval is supplied.
* Impact: the new projections cannot certify that existing ingested records exclude personal data, raw readings, chat, source text or sensitive metadata.
* Destination: distinct source-telemetry/privacy follow-up, Engineering and DPO/Compliance.
* Smallest useful next action: establish source allowlisting/redaction and separately protected evidence access/retention with approved exclusion tests, without enabling content capture to populate the workbook. This is a correctness/acceptance observation, not a vulnerability assessment.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: AI economics and billing reconciliation remain Unknown

* Class: residual work; non-blocking for configuration display, blocking for B2/T2 and complete financial monitoring acceptance.
* Evidence: workbook cost/AI panels and infra/monitoring-runbooks.md T2 explicitly disclose no connected actual/forecast cost, complete capability/period usage, dated price or reconciled variance; OD-51 remains open.
* Impact: configured budget is not actual consumption, available headroom or a reconciled AI cost record. Notification semantics alone do not provide spending enforcement.
* Destination: distinct financial monitoring/OD-51 follow-up, Finance with Engineering.
* Smallest useful next action: obtain human-approved price/budget/reconciliation decisions and matching calendar-period/scope/currency records before connecting metering or making cost/variance claims.

## Defects

* No substantive implementation defect was identified in the exact assessed Bicep/workbook/documentation boundary.
* Severity summary: 0 Critical, 0 High, 4 Medium residual-work findings, 0 Low. No active authoring fix or significant decision revision is requested.

## Routed Findings

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct operational activation follow-up | Project owner and appointed Operations/incident owners | Explicit human/runtime boundary, not a missing authoring correction. |
| RV-002 | Distinct runtime monitoring follow-up | Engineering and competent task/incident owners | Requires separately scoped producers and incident integration. |
| RV-003 | Distinct telemetry/privacy follow-up | Engineering and DPO/Compliance | Requires source enforcement and qualified privacy evidence. |
| RV-004 | Distinct financial/OD-51 follow-up | Finance and Engineering | No approved price/reconciliation decision or connected feed. |

Later implementation of routed work does not require another Review of this task.

## Residual Work

* RV-001 through RV-004 preserve the plan's four separate follow-up areas. None is added to active P01/P02 completion or represented as a defect merely because it remains open.
* Issue #146 stays open with its criteria unchecked. A draft PR must say Refs #146, not claim closure, deployment, live approval or merge readiness.

## Blockers and Remaining Work

* Review blockers: none within the supplied source boundary.
* Operational blockers: actual owner appointments, named-human threshold/activation evidence, live signal/query/render/notification verification, privacy exclusion, runtime poison/AI/harm integration and financial reconciliation remain unmet.
* Remaining parent work: preserve this exact outcome, reconcile P03 workflow state without rewriting this record, and complete authorized draft publication. Review performed no commit, push or PR creation.
* No --all/heavy gate or receipt exists. No --changed invocation was used. This is the explicitly authorized draft-only exception boundary, not a claim that the repository's full publication/merge/release gate passed.

## Validation Evidence

| Check | Status | Evidence and limitation |
| --- | --- | --- |
| Strict Bicep compilation | Passed, implementation-reported | Changes records `az bicep build --file infra/main.bicep --stdout > /dev/null`, no analyzer diagnostics; not rerun by Review. |
| Initial Bicep policy suite | Failed then corrected, implementation-reported | 50 run, one new module-prefix failure; correction and original result preserved. |
| Initial related infrastructure suites | Passed, implementation-reported | 37 passed; not added to final combined count as extra unique coverage. |
| Final combined existing infrastructure regressions | Passed, implementation-reported | `PYTHONPATH=infra/tests python3 -m unittest test_bicep_policy test_iothub_module test_container_contract test_governance test_secret_lifecycle -q`: 87 passed, zero skips. Not repeated without cause. |
| Compiled/schema/contract helper | Passed, implementation-reported; helper source inspected | 32 deployment/name and six activation combinations, metric contracts, ledger range, official workbook JSON Schema, 24 anchors/15 rows and relative links. String/arithmetic assertions do not execute KQL. Generated outputs not independently read. |
| Exact source comparison and lightweight independent Python assertions | Passed in Review | 12 non-state files match exact commit; JSON parse, two resource/time-scoped query contracts, 24 unique entries, 15 matrix rows and PT26H override independently checked without file writes. |
| Published table schema checks | Passed in Review | Official AppRequests/AppAvailabilityResults references retrieved 2026-10-27; published field types match projections and fallback datatables. |
| `git diff --check f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc 64148474e6c6e8cbedfeb09b1f4e9a3775b15318` | Passed in Review | Committed assessed diff; review-record formatting checked separately at closeout. |
| Actual KQL interpretation, query failures and portal rendering | Not run | Outside source-only evidence and no live execution authorized; cannot certify runtime fallback or visual/accessibility behaviour. |
| Azure deployment, metric dimension values and delivered notifications | Not run | Explicit no-deployment constraint; no Azure/private-data/secret reads by Review. |
| Privacy, incident/suspension, availability and financial acceptance | Unavailable | Required qualified approvals and runtime evidence not supplied; routed as residual work. |
| --all/heavy/--changed gate, receipt and hosted checks | Not run | Explicit caller restriction, zero gate runs; no merge/release readiness inference. |

Official schema sources checked:

* https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/apprequests
* https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/appavailabilityresults

## Outcome

* Outcome: Residual work.
* Source authoring is conformant with the accepted bounded direction on the available static evidence; no implementation defect was identified. The task is not whole-issue or operationally accepted because four explicit follow-up areas remain unresolved.
* This is one complete independent Review, not a partial review, a request to fix source in this stage or a requirement for a second review pass.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement correction requested for this boundary. |
| Decision gap or invalid assumption | None in active authoring | No rpi-plan revision requested; operational decisions remain explicit follow-ups. |
| Material evidence gap preventing source verdict | None | No rpi-research return required; unexecuted operational evidence stays outside acceptance. |
| Non-blocking residual work | Four distinct follow-ups, RV-001 through RV-004 | Project owner/Operations; Engineering/task/incident owners; DPO/Compliance; Finance. |

* Execution status: Complete.
* Outcome: Residual work.
* Validation coverage: independent exact-source/static/schema comparison plus honestly attributed existing compilation, 87-test and helper results; no live execution or heavy gate.
* Blockers: no blocker to preserving this source Review and requested draft handoff; operational/whole-issue activation blockers remain.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/monitoring-146-research.md](.copilot-tracking/research/2026-10-27/monitoring-146-research.md) | Source and signal evidence baseline. |
| [.copilot-tracking/plans/2026-10-27/monitoring-146-plan.md](.copilot-tracking/plans/2026-10-27/monitoring-146-plan.md) | Authoring scope, dispositions and separate follow-ups. |
| [.copilot-tracking/details/2026-10-27/monitoring-146-phase-details.md](.copilot-tracking/details/2026-10-27/monitoring-146-phase-details.md) | Phase contracts and validation boundaries. |
| [.copilot-tracking/reviews/2026-10-27/monitoring-146-plan-critique.md](.copilot-tracking/reviews/2026-10-27/monitoring-146-plan-critique.md) | Preserved original Complete / Revise critique. |
| [.copilot-tracking/changes/2026-10-27/monitoring-146-changes.md](.copilot-tracking/changes/2026-10-27/monitoring-146-changes.md) | Reported implementation evidence and limitations. |
| [infra/monitoring-runbooks.md](infra/monitoring-runbooks.md) | Complete catalogue and 15-criterion evidence/gap matrix. |
| [infra/modules/operationalMonitoring.bicep](infra/modules/operationalMonitoring.bicep) | Disabled alert candidates and workbook packaging. |
| [infra/monitoring-workbook.json](infra/monitoring-workbook.json) | Aggregate source panels and explicit missing evidence. |
| [.copilot-tracking/reviews/logs/2026-10-27/monitoring-146-review.md](.copilot-tracking/reviews/logs/2026-10-27/monitoring-146-review.md) | This one complete independent Review. |

## Next Steps

Active parent: preserve Complete / Residual work and all RV findings, then finish
the requested draft PR with Refs #146 and the exact source/evidence boundary.
State missing gates and operational acceptance plainly. Do not fix or re-review
this task in this stage; arrange the four separately owned follow-ups before any
claim of live monitoring or whole-issue acceptance.

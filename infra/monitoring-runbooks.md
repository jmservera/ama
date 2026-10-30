---
title: Monitoring candidates and operator runbooks
description: Source-only alert catalogue, proposed routing, safe responses and unresolved monitoring acceptance
ms.date: 2026-10-27
ms.topic: how-to
---

## Status and Authority

Refs #146. These are authored Bicep/workbook/runbook candidates, not a deployment,
operator appointment, privacy approval or operational release. No issue criterion
is ticked by this document. Existing resources are described from source, not a
fresh Azure inventory. Thresholds already in source are not re-approved here.

The proposed accountable role for technical alerts is the Digital service owner;
Finance owns proposed budget response, and the competent task owner with Safety
and Assurance owns proposed harm response. These are routing proposals, not named
human appointments. Before activation the owner must record actual primary and
backup appointees, acknowledgement/escalation limits and coverage, approved
thresholds/windows/recipients and dated signal verification. Missing appointments
or approvals mean Blocked. Do not send resident/case data in alerts or Teams.

New rules in [operationalMonitoring.bicep](./modules/operationalMonitoring.bicep)
are disabled by default. `enableCandidateMonitoringAlerts=true` only enables
them when `monitoringApprovalReference` is nonempty after trimming; this is a
source guard, not verification of the referenced approval. Do not enable them
until actual approval and a separately authorized signal/notification drill are
reviewed. Their proposed thresholds are exercise candidates, not live limits.
Existing rules/notifications retain their source enablement; the new switch
does not disable, reapprove or attest to any of them.

No Azure command, paid inference, real dataset or secret access is required by
this authoring delivery. Future provisioning/activation is a separate action.
Keep all resource operations inside `ama`; never delete that resource group.

## Common Response and Recovery

On any alert, the appointed operator records UTC detection/window, resource and
release, alert status, accountable owner, scope and a restricted evidence
reference. Confirm signal freshness and access before interpreting counts.
Missing telemetry means Insufficient, not zero failure. Distinguish a fired,
resolved, disabled or never-evaluated rule from a healthy service.

Triage with aggregate metrics and deployment/execution status first. Keep
payloads, credentials, raw readings, device/resident identities, chat, source
text and sensitive reasons out of diagnostic exports and notifications. Use the
existing restricted audit/evidence surfaces when justified, not pasted logs.

Preserve manual case work, resident choice/consent and independent emergency,
hazard and statutory response. A platform alert cannot approve a proposal,
diagnose a hazard, move an investment rank or restart a suspended AI task.
Recovery needs the specific evidence below plus operator verification that the
signal recovered, missed/duplicate work was reconciled and notification reached
the appointed owner. Do not infer this from alert auto-resolution.

## Existing Alerts

Source names use `prefix` for workload/environment and `applicationPrefix` for
the optional separate demo generation; they are not observed deployed IDs.
Existing thresholds below are literal source behavior.

### Foundry client errors

Anchor: `foundry-client-errors`. `alert-${prefix}-foundry-throttle` in
[main.bicep](./main.bicep) counts `ClientErrors` Total >20 over 15 minutes,
evaluated every five minutes, severity 2. Despite its name, it is not proven to
select only throttling/429.
Proposed owner: Digital service owner. Triage: inspect aggregate response codes,
quota, permissions and endpoint/deployment health, not prompts. Response:
retain the bounded workflow-only path; do not raise quota/limits or call a
second model without approval. Recovery: classified root cause, successful
authorized bounded check and preserved finite allowance/expiry.

### SQL CPU

Anchor: `sql-cpu`. `alert-${prefix}-sql-cpu`: `cpu_percent` Average >85 over
15 minutes, every five minutes, severity 3. Proposed owner: Digital service
owner. Triage: aggregate load, blocking and cold-start timing, without exporting
SQL text/parameters or rows. Response: preserve manual work and investigate
bounded concurrency; no schema/capacity changes or disabling audit controls.
Recovery: CPU and latency observations in the same window and reconciliation
of failed writes/retries before resumed work.

### API errors

Anchor: `api-errors`. `alert-${applicationPrefix}-api-5xx`: Requests Total >5
with `statusCodeCategory=5xx` over five minutes, every minute, severity 2; only
authored when applications deploy. Proposed owner: Digital service owner.
Triage: revision/readiness and dependency metrics, distinguish authentication
denials from 5xx. Response: expose owned manual routes; rollback only through
separately approved release control, never bypass authentication. Recovery:
authorized health/role checks and aggregate request/error evidence, including
sample counts. No production availability claim from request success.

### API restarts

Anchor: `api-restarts`. `alert-${applicationPrefix}-api-restarts`: RestartCount
Total >3 over 15 minutes, every five minutes, severity 3; applications conditional.
Proposed owner: Digital service owner. Triage: revision events, resource limits
and dependency failure without console-content dumps. Response: contain repeated
dispatch/retry and retain manual work; no blind restart loop. Recovery:
stable revision plus durable audit/queue reconciliation and no duplicate effect.

### Ledger digest mismatch

Anchor: `ledger-digest-mismatch`. `alert-${applicationPrefix}-ledger-digest-mismatch`:
console `LEDGER_DIGEST_ALERT` matches >0 over one hour, hourly evaluation,
severity 1; background workloads conditional. Its description mentions failed
jobs but its query matches the marker only; the candidate job alert below is a
separate check. Proposed owner: Digital service owner, with Compliance/Legal for
integrity/retention decisions. Triage: verify job/version, restricted chain and
remote anchor evidence. Response: stop affected reliance, preserve all digests
and audit records; never republish over a disputed anchor, delete evidence or
change retention/irreversible lock. Recovery: reconciled mismatch, independent
verification and competent human disposition; not a new successful job alone.

### Ledger verify missing

Anchor: `ledger-verify-missing`. `alert-${applicationPrefix}-ledger-verify-missing`:
fewer than one `LEDGER_DIGEST_OK` console match in 26 hours, hourly evaluation,
severity 1. `overrideQueryTimeRange=PT26H` extends the outer query range beyond
the one-day evaluation window. Triage: distinguish missed schedule, failed
execution, absent logs and table/job-name mismatch from an actual integrity
failure. Proposed owner: Digital service owner. Response: record verification
as Unknown and preserve evidence; do not mark the chain verified. Recovery:
fresh authorized verification against correct immutable remote anchors and
notification proof. JobName prefix/schema and actual hosted operation remain
unverified; see [digest acceptance](../docs/adrs/0002-pilot-readiness-architecture.md#2-blob-storage-for-documents-and-ledger-digests).

### Vault expiry

Anchor: `vault-expiry`. `alert-${vaultName}-secret-expiry` in
[keyvault.bicep](./modules/keyvault.bicep): AzureDiagnostics matches
`SecretNearExpiryEventGridNotification` or `SecretExpiredEventGridNotification`
>0 over one day, hourly evaluation, severity 2. Proposed owner: Digital service
owner. Triage: confirm actual event availability/collection and expiring binding
metadata; this source query is not proof those events arrive. Response: follow
[Key Vault lifecycle](./README.md#key-vault-secret-lifecycle), never print values
or copy a webhook. Recovery: separately approved rotation, binding validation and
fresh expiry metadata; absence of this log does not prove a valid credential.

### Vault denied

Anchor: `vault-denied`. `alert-${vaultName}-denied-access`: AzureDiagnostics
401/403 matches >4 over one hour, every 15 minutes, severity 3. Proposed owner:
Digital service owner. Triage: aggregate failure source and current role/scope
metadata under access review. Response: no blanket access grant, public network
opt-out or authentication bypass. Recovery: least-privilege authorized operation,
audited role disposition and successful notification.

## Budget Notifications

### Budget actual80

Anchor: `budget-actual80`. `budget-${prefix}:actual80`: monthly resource-group
actual cost >80 percent of `monthlyBudget`; email notification to `alertEmail`.
Proposed owner: Finance budget owner, with Digital. Triage: same month/scope/
currency billing record, lag, commitments and unallocated consumption. Response:
record remaining liability as Unknown until reconciled; Finance decides any
spending change. Do not stop hazard/manual routes or delete resources.
Recovery: approved spending disposition and retained billing/notification
evidence. This notification is not a hard cap or AI dispatch control.

### Budget forecast100

Anchor: `budget-forecast100`. `budget-${prefix}:forecast100`: monthly forecast
>100 percent. Proposed owner: Finance budget owner. Triage and response as
[actual80](#budget-actual80), distinguish forecast from actual, preserve
uncertainty. Recovery: reviewed forecast/commitment changes and recorded
Finance disposition, not a forecast silently treated as an invoice.

### IoT budget actual80

Anchor: `iot-budget-actual80`. `budget-${iotHubName}:actual80` in
[iothub.bicep](./modules/iothub.bicep): actual >80 percent of the filtered
IoT transport allocation (hub, dedicated Event Hub namespace and their two
private endpoints). Proposed owner: Finance budget owner, with Digital.
Triage: reconcile only those resource costs and the overall group budget.
Response/recovery as [actual80](#budget-actual80); this is a subset allocation,
not additive headroom or a second overall hard cap.

### IoT budget forecast100

Anchor: `iot-budget-forecast100`. Same filtered allocation, forecast >100
percent. Proposed owner: Finance budget owner. Use
[forecast100](#budget-forecast100), preserving subset/overall reconciliation.
Recovery requires retained forecast record and Finance disposition.

## New Disabled Job Candidates

Each `alert-${jobName}-failed` checks `Microsoft.App/jobs` `Executions`,
dimension `state=Failed`, Maximum >0 over 15 minutes, every five minutes,
severity 2. This is a proposed failure-presence filter, not an exact count of
distinct executions. Provider dimension values and signal behavior need
verification before activation. Only authored background jobs receive candidates;
environment-only/API-only paths have none.

### Job orchestrator

Normal `job-${applicationPrefix}-orchestrator`, demo suffix `orch`.
Proposed owner: Digital service owner. Triage: execution metadata, release,
dependency status and ownership of delayed work. Response: contain bounded
retries and use manual scheduling; never reinterpret an expired authority.
Recovery: known execution outcome and idempotent reconciliation of missed work.

### Job ledger

Normal suffix `ledger-verify`, demo `audit`. Proposed owner: Digital service
owner. Triage: failed execution independently of console markers. Response:
mark verification Unknown and follow [digest mismatch](#ledger-digest-mismatch);
do not publish a replacement anchor. Recovery: successful restricted integrity
verification and retained failure disposition, not just metric resolution.

### Job import

Normal suffix `import`, demo `load`. Proposed owner: Digital service owner,
with Data and Performance. Triage: event-triggered execution/queue metadata,
schema/release and count reconciliation; no raw import content. Response: hold
affected batch, preserve poison evidence and manual correction path. Never empty
or bulk replay a queue. Recovery: owned per-batch disposition and idempotent
retry under separate approval.

### Job auth

Normal suffix `auth-renewal`, demo `auth`; only with token storage and background
workloads. Proposed owner: Digital service owner. Triage: expiry/binding and
execution metadata without fetching SAS or tokens. Response: follow
[Key Vault lifecycle](./README.md#key-vault-secret-lifecycle) and preserve
authentication, no logon bypass. Recovery: approved renewal and binding/expiry
verification; do not print or manually paste credentials.

## New Disabled IoT Candidates

Each rule is independent, `alert-${prefix}-${suffix}`, Total >0 over
15 minutes, every five minutes, severity 2, scoped to the existing hub with no
device dimensions. Proposed owner: Digital service owner; Data and Performance
and the sensor control owner handle data-quality/consent handoffs. No-traffic,
missing consumer append, freshness or consent acceptance is established by these
transport counters. Routing bootstrap stays Insufficient, not healthy.

### IoT ingress throttle

Suffix `iot-ingress-throttle`, metric `d2c.telemetry.ingress.sendThrottle`.
Triage: aggregate attempted/successful ingress and configured quota. Response:
bound retries, preserve consent/manual reporting and do not increase SKU or
enable routing without approval. Recovery: same-window transport reconciliation
and downstream append evidence; counters alone do not prove complete ingestion.

### IoT routing dropped

Suffix `iot-routing-dropped`, metric `d2c.telemetry.egress.dropped`.
Triage: dead endpoint, keyless role propagation and endpoint/network status.
Response: preserve owned gap evidence and manual condition review; no public
endpoint or credential fallback. Recovery: approved endpoint repair and
end-to-end count/idempotency reconciliation without exposing readings.

### IoT routing invalid

Suffix `iot-routing-invalid`, metric `d2c.telemetry.egress.invalid`.
This is endpoint incompatibility, not consumer schema-validation evidence.
Triage: endpoint/routing configuration and supported transport. Response: hold
the affected route change; no payload logging or schema acceptance by AI.
Recovery: reviewed compatible routing and separately evidenced downstream DQ.

### IoT routing orphaned

Suffix `iot-routing-orphaned`, metric `d2c.telemetry.egress.orphaned`.
Triage: unmatched/disabled routes, including deliberately disabled bootstrap
fallback. Response: keep route activation separately approved, reconcile gaps;
do not enable blanket routing to clear an alert. Recovery: approved routing
contract plus exact window/source/destination reconciliation.

## Explicit Missing-Signal Procedures

These are not installed alerts. Appointments, signal production and safe
notification drills remain required. Do not substitute service-wide queue depth
for either poison queue or infer a zero from no samples.

### Agent tasks poison

Queue `agent-tasks-poison`. Proposed owner: Digital service owner, with competent
task owner. Gap: no safe queue-specific depth/oldest-age producer or owned
arrival alert. Triage under separate authorization: inspect aggregate queue
properties only; avoid peek/export of message bodies. Response: contain affected
dispatch and record restricted task/version evidence; never purge/replay blindly.
Recovery: owner-disposed failed items, authorized idempotent retry and reconciled
queue counts without duplicate decisions.

### Import jobs poison

Queue `import-jobs-poison`. Proposed owner: Digital service owner, with Data and
Performance. Same missing depth/age signal; audit-category storage diagnostics
do not establish successful enqueue monitoring. Triage: aggregate queue/batch
status only. Response: hold affected import and retain manual correction.
Recovery: batch/schema disposition, controlled retry and count reconciliation.

### AI limits

Proposed owner: competent task owner and Digital; Finance owns budget/price
approval. Gap: no installed capability/period call/token/budget/expiry aggregate
breach alert. The existing bounded assistant allowances and protected usage
records are partial, not complete NFR-017 delivery.
Response: use existing runtime disable/manual path when authority, usage, price
or liability is unknown; no extra inference or raised limits. Hazard work
continues independently. Recovery: owner-approved finite limits, dated versioned
price and billing record, per-request termination, owned notification and expiry
checks. OD-51 remains open; no invented price, tolerance, budget or appointee.

### RAI harm

Proposed monitoring owner: competent task owner; incident owner: named Safety/
Assurance appointee with Digital support, appointment pending. Gaps: task/release
indicators, denominators/windows, approved thresholds, durable repeated-event
reconciliation, automated owned-incident routing and actual drill evidence.
Use [existing incident controls](../src/api/README.md#incident-and-restart-contract-221)
and protected SQL audit/report surfaces. Include unsupported claims, critical
misses, stale review attempts, challenges, cohort errors and complete preparation,
review, correction and re-review effort as applicable, not approval rate as
safety. Missing samples/approvals/thresholds mean Insufficient/Blocked.

Response: record owned task/version incident through the existing authorized
suspension path; block new dispatch/reliance, preserve manual/emergency routes.
An infrastructure notification does not perform that suspension. Disabled tasks
still need visible monitoring ownership/manual-route status. Recovery: qualified
corrective tests and distinct authorized human restart approval; current actual
restart remains held as documented in #221. Constructed thresholds/fixtures are
synthetic offline tests only, never actual human authorization.

## Workbook and Privacy Boundary

[monitoring-workbook.json](./monitoring-workbook.json) is packaged as a shared
workbook by Bicep, scoped to the existing workspace/Application Insights.
`operationsWorkbookId` identifies the authored resource; no deployment or portal
rendering is established here. Its request/error/p95 and availability-test tables
report sample denominators, window and as-of UTC; absent/empty tables produce
Insufficient and null measurements. Query/access/schema failures are Blocked
and must not be interpreted as clean data. Invalid sample counts are visible.
Instrumented/sampled request durations are not end-to-end scenario p95, and
availability-test success is not a production availability SLO.

Configured budget is shown separately from Unknown actual/forecast spend.
AI capability/period usage, price and metered-to-billing variance are explicitly
not connected, Unknown/unreconciled. This does not satisfy the cost/dashboard or
tokenomics dashboard acceptance criterion. Finance must compare matching period,
scope and currency, retaining the Azure billing record as financial source.
Token cost alone is not Total Cost of AI or value above a quality floor.

New candidates consume platform metrics only; no new diagnostic categories or
raw-content exporter is enabled. Existing IoT diagnostics are metrics-only.
However, existing Container Apps `allLogs`, Foundry/SQL/Key Vault/storage audit
collection and application instrumentation are not proven personal-data-free.
Storage/Insights schemas can include identity/IP/URI fields; console logs can
contain arbitrary application output. Workbook projections do not redact
ingested records. The privacy criterion remains unmet until source-side
allowlisting/redaction and restricted evidence retention/access are tested and
approved by the DPO/Compliance owners. Do not enable content tracing, prompt/
completion capture, raw readings/chat or raw exception/source text to make a
dashboard populate. Existing collection settings are not silently changed here.

## Issue Evidence and Gap Matrix

All rows remain unproven as whole-issue acceptance; source authoring is narrower.
B/R/T IDs below label the issue's criteria positionally, not new requirements.

| Criterion | Authored evidence | Remaining evidence or human decision |
| --- | --- | --- |
| B1 job/poison/ledger/IoT alerts | Disabled job/IoT candidates; existing ledger rules, 26h correction; queue gap procedures | Safe poison-specific producer, signal checks and owned notification drill; #110/#115 actual acceptance |
| B2 availability/errors/latency/cost vs budget dashboard | Workbook aggregate query sources, configured budget and Unknown cost | Actual instrumentation/tests, KQL/portal execution and financial cost feed/reconciliation |
| B3 each alert runbook with owner | All eight existing rules/four budget notices and eight candidates catalogued; proposed roles | Named actual primary/backup appointments and response/escalation limits |
| B4 diagnostic exclusion | No new log categories, aggregate query projections, metrics-only IoT | Existing diagnostic source exclusion/redaction tests and DPO/privacy approval |
| R1 indicators/denominators/window/thresholds/owners/response | RAI procedure and blocked workbook panel | Per-task/release approved declaration and real appointments |
| R2 unsupported claims/critical misses/stale review/challenges/cohort errors/effort | Explicit indicator list in RAI procedure | Applicable producer coverage and complete review-effort evidence |
| R3 missing samples/usage/approvals/thresholds not green | Typed empty query sources, null measurements, static Blocked/Unknown panels | Actual query/error/serving behavior; approved sufficiency and threshold evidence |
| R4 seeded harm/breach creates incident and suspension | Existing authorized incident path documented | Owned signal-to-incident integration and actual accepted drill; no suspension from metric alert |
| R5 restart reconciliation and disabled-task ownership/manual routes | Required response/recovery and blocked panel | Durable windows/denominators/repeated-event runtime coverage and appointment evidence |
| R6 no raw prompts/source/sensitive reasons/tokens/identities | No new content logging; protected audit separation documented | Source-level exclusion/retention/access tests on existing telemetry |
| R7 offline constructed vs named-human live thresholds | Disabled candidates labelled proposed, approval-reference boundary | Named actual human approvals, not a nonempty string or fixture |
| R8 existing audit/report/UI, no new platform/future-IoT dependency | Reuse existing Azure Monitor and SQL audit/continuity paths; IoT rules independent | Actual runtime/report integration without adding a separate platform |
| T1 calls/tokens/budget/expiry breach alerts owned/runbook | AI-limit gap procedure, no invented producer | OD-51 owners/limits, complete metering, durable breach notification and test |
| T2 capability/period usage beside Azure cost/variance | Explicit missing usage, Azure actual cost Unknown and unreconciled variance panel | Complete same-period usage/billing/dated-price feed and approved tolerance |
| T3 budget80 actual/100 forecast notification not cap | Budget runbooks, workbook and corrected parameter description | Source semantics documented; delivery/receipt not tested |

Linked requirements: [ADR 0001 operational targets](../docs/adrs/0001-azure-architecture.md#operational-targets-and-cost-model),
[PRD observability/RAI/tokenomics](../docs/prds/zava-forward-retrofit-programme-demonstrator.md#observability-and-slo-measurement-method),
[BRD OD-51 and NFR-012/FR-052](../docs/brds/agentic-retrofit-programme-brd.md),
[AI tokenomics evidence](../docs/reference/resources/ai-tokenomics.md).

## Source Validation and Activation Checklist

Local source checks: strict Bicep build, existing infrastructure regression tests,
compiled optional-job/name/activation assertions and workbook JSON/schema/source
review. These do not execute KQL, render Azure Portal, send notifications, test
deployed dimension values or establish SLOs/privacy/financial acceptance.

Before any later separately authorized activation, the appointed operator needs:

* Owner approval reference with actual primary/backup appointees, thresholds,
  windows, response/escalation and notification destinations.
* Current schema/dimension/resource-ID checks, missing/empty/invalid/error
  samples, synthetic failure injection and delivered/resolved notifications.
* Review of extra rule/query/retention cost against approved budget headroom.
* Source-side privacy exclusion and distinct protected evidence access/retention.
* For AI/harm: approved indicator/limit declarations and owned incident/suspend/
  manual-route drills with qualified human restart approval.
* Finance-approved billing/price/variance evidence before any monetary claim.

Official schema references retrieved 2026-10-27:
[job metrics](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/supported-metrics/microsoft-app-jobs-metrics),
[IoT metrics](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/supported-metrics/microsoft-devices-iothubs-metrics),
[requests](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/apprequests),
[availability](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/appavailabilityresults),
[console logs](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/containerappconsolelogs),
[queue logs](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/storagequeuelogs).

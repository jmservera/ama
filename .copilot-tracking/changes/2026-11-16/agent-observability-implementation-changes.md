<!-- markdownlint-disable-file -->
---
description: Privacy-safe OTLP implementation outcomes, validation and retained publication gates
ms.date: 2026-11-16
---

# RPI Changes: Agent observability implementation

## Metadata

* Task ID: `agent-observability-implementation`
* Related plan: [.copilot-tracking/plans/2026-11-16/agent-observability-implementation-plan.md](../../plans/2026-11-16/agent-observability-implementation-plan.md)
* Implementation date: 2026-11-16

## Execution Status

* Status: Partial
* Declared invocation scope: full plan.
* Completed scope markers: P01, P01-T01, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02.
* All remaining active-plan markers: P04-T01 and P04.
* Status basis: runtime and operating guidance pass focused checks; native deck
  has synchronized draft deliveries with reproduced baseline diagram failures.
  Review, main integration and full publication gate remain.

## Execution Summary

Implement a default-off, content-free OTel layer and protected trace-to-audit
joins. Retain SQL/domain authority and all dispatch/consent/fence controls.
Add Agent 365 as a conditional future capstone proposal only.

## Completed Work

### Privacy-safe SDK pipeline and consistent packages

* Related task: P01-T01.
* Files: [src/core/src/zava_forward/core/telemetry.py](../../../src/core/src/zava_forward/core/telemetry.py),
  core metadata, all five consumer input/hashed locks, worker Dockerfile and
  core telemetry tests/support.
* Export remains off by default. Explicit OTLP initialization owns one pipeline,
  bounded batching/timeouts, no resource detectors or exception events,
  parent-based sampling and W3C traceparent-only propagation. Metric dimensions
  are bounded; token counters require settled usage.
* Nine real-SDK tests, focused Ruff/mypy and four worker dependency-boundary
  tests pass. All five locks resolve; installed component extras pass `pip check`.
* Initial carrier test exposed OTel's current random-trace flag (`03`), which
  the initial overly strict validator rejected. Corrected to accept the W3C
  flag byte while retaining exact shape and nonzero IDs; regression passes.
  Metric tests distinguish lawful trace exemplars from forbidden ID dimensions.
* No collector initialized in application execution or live model inference.
* Additional offline tests prove controlled work completes while the real batch
  processor's exporter is blocked. Invalid exporter modes, disabling an active
  pipeline and malformed/control-character headers fail explicitly without
  echoing their values.

### Causal runtime instrumentation with unchanged protected controls

* Related task: P02-T01.
* Core assistant SQL transactions, SQL-backed producer attempts, stored optional
  traceparent, claimed workflow execution, copied physical-thread context and
  actual `Ai._request` are instrumented. Existing JSON audit gets random trace
  identifiers without schema changes. No case/task/meter/hash identifiers export.
* Worker message/result carriers are optional and backwards compatible;
  consumer/workflow/thread/post-back causal relationships retain normal
  acknowledgement/redelivery/timeout/slot behavior. API request context resets
  per keep-alive request. API/active-worker initialization/shutdown is opt-in;
  worker standby/health/version retain their behavior.
* Validation: 79 worker transport/lifecycle/dispatch/dependency tests and 10
  HTTP/core-composition tests pass. Prior protected-assistant run: 160 total,
  100 passed and 60 MSSQL cases skipped without local SQL; not a full receipt.
  Core/API/agents strict mypy passed before the final test-only additions.
* The new causal test initially hit the genuine release model-version guard
  after replacing its fake provider. It now installs the existing synthetic
  release fixture for that provider; production admission is unchanged.

### Structured diagnostics retain trusted context and redaction

* Related task: P02-T02.
* Enabled console JSON serializes guarded LogRecords with timestamp/severity,
  empty caller attribute bag, service metadata and context-derived IDs.
  Caller extras and exception content remain discarded; default-off startup
  retains legacy formatting. SDK export diagnostics cannot echo destinations.
* Validation: 22 core telemetry/diagnostic cases pass, including hostile extras,
  payload/secret canaries, delayed-format resource/context snapshots, active/
  no-span correlation and original meter markers. Six HTTP tests include an
  interrupted/no-response request classified as failure, not successful work.

### Operating contract and indexed lasting findings

* Related task: P03-T01.
* Updated [infra/monitoring-runbooks.md](../../../infra/monitoring-runbooks.md)
  and core/API/agents guides with exact settings, bounds, synthetic checks,
  propagation/audit joins, rollback and denominator/coverage limitations.
  The existing knowledge index links this synthesis and its append-only log
  records the change; no duplicate knowledge page or owner-memory change.
* Distinguishes source/offline/live evidence, completed-attempt histograms from
  business-scenario SLOs, authoritative SQL/consumption from diagnostics and
  future Agent 365 from demonstrated ingestion/governance.
* Validation: added local links and diff whitespace pass; no documentation
  build exists. All runtime/test owned changes pass Ruff; full strict checks:
  core 328, agents 57 and API 305 source files, no issues.

### Agent 365 is a conditional future capstone proposal

* P03-T02: updated existing slides 24/25 and relevant B27 notes/Q&A/roadmap;
  synchronized native draft PPTX/PDF, pitch and compact source receipt.
  No new slide, live integration or automatic governance/explainability claim.
* Native Build/Verify, 32 shape checks, source hashes, insertion/navigation,
  protected-cost checks and 10 preview tests pass. Preview contains 55 pages
  and 108 verified jumps; changed pages/neighbours were inspected.
  All six protected financial slide and note XML parts remain byte-identical.
* Preserved adverse evidence: both diagram-generator checks fail and the
  architecture suite is 7 passed/4 failed on this worktree AND exact original
  HEAD 723d5026. Failures concern discovery addendum/programme evidence,
  importer/sensor-consumer hashes and native SVG provenance. Current source
  edits add hash drift but introduce none of those failure statuses.
  Do not call this fully validated: compact receipt remains Partial.
* No unrelated baseline diagram regeneration. Native PowerPoint/assistive-
  technology and live Azure/Agent 365 checks remain unperformed.

## Implementation-Time Plan Updates

* Planning completed its single critique, preserving Complete/Revise and resolving
  PC-001 through PC-006. No scope/authority expansion or new owner decision.
* Tooling isolated under `/var/tmp/ama-otel-FdLcBv`; Python 3.12.15, official
  checksum-verified PowerShell, actionlint, ShellCheck and Trivy restored.
  Existing Bicep works without modification. Native preview uses task-owned
  LibreOffice tooling/container; no global installation or shared takeover.

### Current-main integration authorized without history rewrite

* P04-T01: current main advanced during work. The canonical gate requires its
  ancestry. Owner selected merging main into the child after committing owned
  work. Preserve the separate research PR and all original review evidence.
* Use a clean external validation worktree for the committed candidate.
  Existing unrelated ignored working files remain in place.

### Direct Azure exporter adds unrequested metadata and background traffic

* Affected marker: P01-T01; dependent runtime/deck finalization pauses.
* Installed exporter 1.0.0b59's `_utils.azure_monitor_context` adds the machine
  name as `ai.device.id` and locale independent of the supplied OTel Resource.
  `_base.BaseExporter` also starts Statsbeat/customer SDK statistics and a
  OneSettings configuration worker unless explicitly disabled.
* This contradicts the planned content-free/minimal-resource/one-destination
  guarantee. No network exporter has been initialized and no application data
  was sent; installation alone revealed it.
* Proposed correction: ship standard OTLP only; defer direct Azure exporter
  pending a supported minimal-metadata path or approved collector integration.
  Do not patch SDK private globals or invent a privacy guarantee.
* Decision state: owner selected "Implement OTLP first; defer direct Azure
  exporter". Plan scope, selection, risk and readiness reconciled; P01 resumes.
  SDK foundation, instrumentation and Agent 365 proposal remain within scope.

## Business Alignment

* None. No implementation-time change to cited business requirements.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|---|---|---|---|
| Ancestry | Child/parent branch | Passed | Both at 723d502687ee148c7cbd869cad2ec3036e71a8a2; PR 1823 open |
| Targeted tests/type/lint | P01/P02 | Passed | 22 core, 79 worker and 10 API focused tests; strict core/agents/API types; focused Ruff |
| Capstone | P03 | Partial | Native build/32 shape checks, 55-page preview/108 jumps, financial guards and 10 preview tests pass; 2 generators/4 assertions fail identically on original HEAD |
| Full gate/exact-head review | P04 | Unavailable | Requires completed/committed implementation |
| Live Azure/provider/Agent 365 | Excluded | Skipped | No live authorization; offline tests only |

## Pre-Review Reconciliation

* Plan markers and task-local context: current.
* Completed-work entries and handoff prose: runtime and operating guidance current.
* Validation, blockers, remaining work, and follow-up items: current.
* Review readiness: P01-P03 scope ready after authorized main integration;
  P04 publication remains pending, not full-plan completion.

## Blockers

* Backend decision resolved: OTLP first, direct Azure exporter deferred.
* New publication blocker: fetched `origin/main` is
  `bfed6c99e0f510d0d244c170a79b31dc23e268a3`; merge-base with current
  child is `d74518fce8eab67286487b0f66aedcc816ff95a7`.
  Full gate requires descent from current main. Owner authorized the merge
  after committing owned work; no rebase, force-push or parent-PR merge.
* Existing unrelated ignored working files prohibit using this checkout as a
  clean gate candidate. Preserve them; use a new clean validation worktree
  at the committed candidate rather than deleting or moving them.

* Full SQL/browser/image gate has not run. Resolve actual prerequisite failures
  locally if encountered; no bypass or cloud fallback.

## Remaining Work

* P04-T01 and P04: commit/authorized main merge, one post-implementation Review,
  complete gate, independent exact-head assessment and publication/hosted CI.

## Follow-Up Items

* Canonical plan list: [.copilot-tracking/plans/2026-11-16/agent-observability-implementation-plan.md](../../plans/2026-11-16/agent-observability-implementation-plan.md).
* Existing baseline diagram provenance failures remain unselected; preserved
  in the compact capstone receipt and above, not silently reported passing.

## Return-to-Caller State

* Implementation execution status: Partial, full plan.
* Validation coverage: focused runtime, strict types/lint, operational links,
  native build/render/navigation/cost; diagram/full gate checks incomplete.
* Planning and critique state: Ready; original Complete/Revise preserved.
* Continuation owner: automatic RPI parent, finishing P03-T02 then P04-T01.

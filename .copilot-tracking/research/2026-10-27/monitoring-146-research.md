<!-- markdownlint-disable-file -->

# Task Research: monitoring-146

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/monitoring-146-research.md |

## Research Brief

* Target: #146 monitoring alerts, dashboard/workbook and owned runbooks.
* Purpose: prepare a source-only Bicep/documentation draft PR for operators.
* Scope: existing infrastructure, linked ADR/BRD/PRD, current signal contracts.
* Non-goals: deployment, application changes, new observability platforms,
  private datasets, live threshold/owner appointment or legal/privacy approval.
* Criteria: map every original, RAI and tokenomics criterion to actual evidence
  or an explicit unmet dependency. Never equate authored resources with operation.
* Requested outputs: dated research, plan/details/critique, changes and Review;
  source-only implementation and a draft PR.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Which safe monitoring surfaces exist, which definitions can be authored, and which activation decisions remain human-owned? |
| Codebase scope | infra/, docs/, relevant signal producers in src/ |
| External scope | Official Azure resource schemas/metric documentation if needed |
| Initial internal areas | infra/main.bicep, infra/modules/monitoring.bicep, ADR 0001/0002/0003/0006, linked PRD/BRD |
| Research posture | focused; default for named bounded issue |
| Explicit limits | No deployment, no secrets/.env/private datasets/uv; local tests only; at most one locked --changed gate only if large; no --all |
| Completion basis | Material in-scope questions covered with evidence; all three waves |
| Research edits | Evidence and required session state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Authority and disposition |
| --- | --- | --- |
| Instructions | Repository AMA guidance | Selected: branch safeguards, reference index, dated evidence, src layout, human boundaries |
| Skill | rpi-research | Selected: ordered wider/deeper/contrarian research |
| Skill | telemetry-foundations | Selected: aggregate bounded telemetry and default-deny sensitive data |
| Specialist | RPI Researcher | Skipped: a tightly coupled source trace needs no separate context |
| Web skills | Design/accessibility | Skipped: Azure workbook JSON authoring, no application UI changes |

## User Participation and Research Decisions

Caller explicitly requests the full ordered loop and draft publication on the
already-created branch. This authorizes this task's automatic phase progression,
not unrelated follow-up work. Non-interactive execution; no invented approvals.
Issue comment names owner/threshold decisions as outstanding. Independent
authoring can proceed; activation requiring those decisions must remain blocked.

## Scope and Success Criteria

Read #146, its comments, #110 and #115, reference index/memory and both case-study
documents first. Check linked requirements and source contracts next. Use stable
C/W evidence IDs with locations. Preserve all unchecked issue criteria.

## Task Research Requests and Direction Controls

* Deliver #146 as Bicep and docs only, one draft PR to main, no deployment.
* Reuse clean branch feat/monitoring-146; no existing PR. Review base after fetch:
  f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc.
* Owner-decided live thresholds, recipients and actual operational appointments
  must not be inferred. Publish independent source work with Refs #146.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What alerts/signals and requirements already exist? | depth | Answered C3-C6 |
| Q2 | What dashboard can represent missing usage/cost/quality honestly? | depth | Answered C7-C8; missing signals blocked |
| Q3 | What privacy, owner and activation gaps prevent issue acceptance? | depth | Answered C1, C7-C9 |

## Prior Knowledge Gate

Issue #146's current owner comment says tick none and explicitly identifies
missing dashboard/runbooks/RAI/tokenomics and owner/threshold decisions. Existing
ledger alerts must be inspected rather than duplicated. #110 and #115 remain
partially delivered; neither operational IoT nor hosted digest acceptance can
be assumed.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline inventory found four existing metric rules, two ledger log rules, two
Key Vault rules and monthly/IoT budgets. The current issue narrative understates
ledger coverage. IoT is now source-authorized but route activation remains
separate. Reflection: extend existing wiring, do not replace services.

#### Wave 2: Deeper

Official schemas confirm job Executions/state, IoT ingress throttling and
routing-drop metrics; queue logs have OperationName, Uri, StatusCode. Console
logs have JobName and Log. Existing queue diagnostics use the audit category,
which does not establish a successful PutMessage signal. Existing ledger
missing-success query has a 24h search window despite a claimed 26h horizon.
Reflection: use bounded platform metrics for new job/IoT definitions; preserve
existing ledger alerts and correct its lookback. No safe per-poison-queue depth
signal exists in the authored infrastructure.

#### Wave 3: Contrarian

Challenged queue-wide message count as poison-specific evidence: rejected
because a service-level aggregate cannot isolate either poison queue.
Challenged a filter/project in a workbook as privacy enforcement: rejected,
because ingestion still retains personal metadata/free-text from allLogs.
Challenged request success percentage as availability and averaged platform
latency as p95: rejected. Missing samples cannot be coalesced to zero.
Challenged placeholder AI/cost rows as acceptance: rejected. A source-only
workbook may expose explicit Blocked/Unknown and links, not fabricate metering.
Reflection: independent authoring is safe with new alerts disabled, proposed
role routing and prominent activation blockers. No live threshold appointment
can be supplied by this task.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Add job/IoT metric alert candidates, default disabled | C3-C6, W1-W2 | Accepted | No new telemetry exporter or identity; caller limits respected |
| Add source workbook with aggregate API panels and explicit missing evidence | C7-C9 | Accepted | Useful source delivery without false operational acceptance |
| Poison queue depth or harm/AI-limit alert from nonexistent producer | C7-C9, W3 | Deferred | Requires existing-runtime safe aggregate producer and owner contract |
| Enable alerts or name an actual operational appointee | C1, C7-C8 | Deferred | Owner decision, not author authority |

#### Cycle Re-entry Evaluation

No further cycle required for bounded independent authoring. Evidence covers
the source surfaces; remaining gaps need runtime work or human decisions,
not more discovery. Ready for source-only planning, not issue/live acceptance.

## Evidence Log

| ID | Finding | Source | Confidence |
| --- | --- | --- | --- |
| C1 | Issue remains open; human owners/live thresholds not appointed here | gh issue view 146 --comments, retrieved 2026-10-27 | High |
| C2 | No sub-issues; #110/#115 dependency acceptance remains incomplete | gh issue view 110 / 115, retrieved 2026-10-27 | High |
| C3 | Existing alerts and monthly notification configuration | infra/main.bicep:415-605 | High |
| C4 | App diagnostics collect all logs, no source redaction enforced here | infra/modules/containerapps.bicep:78-87 | High |
| C5 | IoT metrics-only diagnostics; route disabled at bootstrap | infra/modules/iothub.bicep:169-187; docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:35-60 | High |
| C6 | Both poison queues exist; queue audit logs do not establish enqueue/depth monitoring | infra/modules/storage.bicep:89-124 | High |
| C7 | Harm monitoring and human threshold/owner/suspend requirements | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1550-1570,2168-2173 | High |
| C8 | Tokenomics is draft; OD-51 remains open | docs/brds/agentic-retrofit-programme-brd.md:1603-1604,2169; docs/reference/resources/ai-tokenomics.md:73-110 | High |
| C9 | Proposed API SLOs unmeasured; cost budget notifications are not enforcement | docs/adrs/0001-azure-architecture.md:273-278; docs/prds/zava-forward-retrofit-programme-demonstrator.md:1604-1636 | High |
| C10 | Existing incident suspension path and restart remain human gated | src/api/README.md:1652-1719 | High |

### External Evidence (retrieved 2026-10-27)

| ID | Source and claim | URL |
| --- | --- | --- |
| W1 | Microsoft.App/jobs Executions supports state dimension and Maximum/Total | https://learn.microsoft.com/en-us/azure/azure-monitor/reference/supported-metrics/microsoft-app-jobs-metrics |
| W2 | IoT sendThrottle, dropped/invalid/orphaned metrics are dimension-free counts | https://learn.microsoft.com/en-us/azure/azure-monitor/reference/supported-metrics/microsoft-devices-iothubs-metrics |
| W3 | StorageQueueLogs includes identities, IP and URI; not privacy-safe by default | https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/storagequeuelogs |
| W4 | ContainerAppConsoleLogs contains JobName and Log | https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/containerappconsolelogs |
| W5 | AppRequests includes ItemCount, Success, DurationMs and _ResourceId | https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/apprequests |
| W6 | AppAvailabilityResults includes ItemCount, Success and _ResourceId | https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/appavailabilityresults |
| W7 | Workbook Notebook/1.0 schema; used for actual local JSON Schema validation | https://raw.githubusercontent.com/microsoft/Application-Insights-Workbooks/master/schema/workbook.json |

An attempted ContainerAppSystemLogs reference URL returned 404; no reliance on
that table or invented failure reasons. No external query received repository
source, private data or credentials.

## Findings, Alternatives and Decision State

Selected additive candidate module and workbook plus exhaustive runbook coverage.
Reuse action group, existing SQL audit/report/runtime and incident surfaces.
Reject broad service-level queue counts and invented AI telemetry tables.
Keep new rule enablement false pending named-human approvals and signal checks.

## Open Questions, Risks and Residual Uncertainty

Live operation and named-human approval cannot be established by Bicep authoring.
Owner must appoint actual operators/incident owners and approve thresholds,
windows, spending/price records and activation. DPO/privacy review must establish
source-side redaction before sensitive diagnostics. This task will stop at the
independent source boundary and record these decisions in its draft PR.

## Planning Readiness

Ready for independent Bicep/docs authoring only (C3-C10, W1-W4).
Not ready for operational activation or whole-issue acceptance.

## Research Disposition and Self-check

Research disposition: executed. Wider, deeper, contrarian and synthesis complete;
questions covered; evidence/alternatives/gaps checked. No source changes or
deployment in Research. Parent next action: Plan in the user-requested full loop.

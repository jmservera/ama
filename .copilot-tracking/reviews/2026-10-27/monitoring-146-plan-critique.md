---
title: Monitoring 146 final-candidate plan critique
ms.date: 2026-10-27
---

## Metadata

* Task ID: 146
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/monitoring-146-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/monitoring-146-phase-details.md
* Research: .copilot-tracking/research/2026-10-27/monitoring-146-research.md
* Critique execution status: Complete
* Review base supplied by planning: f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc
* Worktree: feat/monitoring-146. Supplied planning/research/session records were already untracked and were not changed.
* This is the single final-candidate critique, not an implementation Review or a second research cycle.

## Inputs and Criterion Boundary

* Caller direction: Bicep/docs authoring only; no application edits, new test source, deployment, Azure/secret/private-data reads, paid inference or full/heavy gates. One draft PR with Refs #146; whole-issue acceptance requires evidence beyond this task.
* Read the complete supplied plan, phase details and research. Read the required case-study original, addendum context, reference index and owner memory. Memory was context only.
* Inspected supplied-source contracts in infra/main.bicep, infra/modules/monitoring.bicep, infra/modules/containerapps.bicep, infra/modules/authTokenStore.bicep, infra/modules/keyvault.bicep, infra/modules/iothub.bicep, infra/bicepconfig.json and the relevant existing infrastructure test sources.
* Read the supplied issue #146 and its owner comment using read-only GitHub issue retrieval. Checked linked ADR operational targets, PRD monitoring/telemetry requirements and the tokenomics synthesis. The issue's four base, eight RAI and three tokenomics criteria are the criterion boundary, not just the five local authoring criteria.
* Re-read the research's supplied W1/W2 Microsoft metric references on 2026-10-27. Relevant rows were available; the IoT page response was truncated after the relevant rows. No unrelated external discovery was performed.
* Actual operators, incident owners, live thresholds, privacy approval and OD-51 remain human decisions already deferred by the caller. Their absence does not block disabled source authoring; it does block operational acceptance.
* This assessment establishes planning credibility, not deployed metric availability, KQL execution, financial reconciliation, privacy compliance, human appointment or issue completion.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1; C3/C5; W1/W2; P01-T01 | Partial | Metric choices are supported; explicit resource/activation truth-table checks are missing, PC-002. |
| FR2; C7-C9; P01-T01; AC2 | Partial | Honest aggregate-only intent is sound; absent-table/error behavior and query-contract evidence need a bounded method, PC-001. |
| FR3; C3/C6-C10; P01-T02; AC3 | Partial | Catalogue and matrix are promised, but exact existing semantics and reconciliation need an enumerated oracle, PC-003. |
| FR4; P01-T02 | Covered | overrideQueryTimeRange PT26H plus explicit ago(26h), retaining a supported evaluation window, corrects the actual 24-hour outer limit. |
| NFR: no new producer, identity, raw-content outputs or privacy claims | Covered | Existing collection gaps remain explicit; query projection is not represented as source-side exclusion. |
| AC1; P02-T01 | Partial | Strict compilation and compiled assertions are appropriate; conditional combinations need explicit acceptance cases, PC-002. |
| AC2; P02-T01 | Partial | JSON parsing is necessary but does not validate KQL table availability or missing-data behavior, PC-001. |
| AC3/AC4; P01-T02 | Partial | All 15 issue criteria are in scope; a source-to-catalogue/matrix reconciliation is needed, PC-003. |
| AC5; P02-T01 | Partial | Existing bounded suites are suitable; their default temporary-file behavior conflicts with the execution restrictions, PC-004. |
| P01-T03 | Covered | Infra navigation, knowledge-base index and append-only log updates are bounded and appropriate. |
| P02-T02 | Covered | Commands, counts, skips and unproven criteria remain separately recorded. |
| P03-T01/P03-T02 | Covered | One independent implementation Review, preserved outcome and one draft PR; no deployment or activation authority. |
| Caller limits and human decisions | Covered | No app changes, new test source, full gate, actual appointment or invented approval is authorized. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 0 High, 4 Medium, 0 Low.
* Rationale: The bounded source-only approach is credible, and the selected signals and ledger fix are feasible. Four direct planning corrections are needed to make the workbook's failure semantics, conditional checks, catalogue completeness and local validation executable and auditable.
* All findings are planner-direct corrections within the confirmed scope. None requires a significant or divergent user decision. Apply dispositions once and finalize without another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: The workbook lacks a defined absent-table and query-error contract

* Related IDs: FR2, AC2, P01-T01, P02-T01, research C7-C9; base criterion B2 and RAI criterion R3 below.
* Evidence: The plan requires missing telemetry to show Insufficient and queries to use actual schema columns. Details P01-T01 specifies weighted request p95 and a separate availability-test denominator, but neither supplied research nor details identifies the request/availability table contracts or explains how an absent table produces the promised status. P02-T01 validates substituted JSON, not KQL execution. infra/modules/monitoring.bicep creates workspace-based Application Insights; resource creation alone does not establish populated request or availability-test tables.
* Concern: A query against an unavailable table may fail resolution rather than return an empty result. Handling a zero-row summarize alone cannot guarantee Insufficient. Likewise, JSON parsing cannot demonstrate weighted denominators, null handling or a valid query schema. This is a missing planning contract, not an assertion that an uncreated workbook already contains a defect.
* Impact: A central deliverable could render errors or misleading percentages while its authoring checks pass. No-sample availability must not become request success, zero percent or green.
* Smallest useful change: Specify the workspace query dialect, table/column contract, request/resource/time filters, weighting and units. Define distinct behavior for absent tables, empty windows, null fields and query/access errors. Use a typed fallback or another supported missing-table strategy; where an error cannot be converted into a query result, retain a visible static Insufficient/Blocked explanation rather than claim a successful empty-data panel. Require denominator, as-of/window and sampling caveats beside each aggregate. Keep configured budget separate from Unknown actual/forecast cost and unavailable reconciled AI usage.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T01/P02-T01 identifies the intended schema and query/status contracts and a bounded source-review/assertion checklist covering absent table, zero samples, populated weighted samples and query failure. The later changes record must distinguish JSON/source checks actually run from KQL/service behavior not run. No Azure query, producer or new test-source file is required.
* Decision route: Direct planner correction. Do not select a new telemetry platform or resolve live thresholds.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Conditional and activation assertions lack explicit acceptance cases

* Related IDs: FR1, activation NFR, AC1, P01-T01, P02-T01; research W1/W2.
* Evidence: Details says to inspect enabled flags, scopes and an optional job array. infra/main.bicep:333-378 passes applicationPrefix, deployApplications, deployBackgroundWorkloads and optional token-maintenance identity into the apps module. infra/modules/containerapps.bicep:239-240,332-333,373-374,420-421 defines distinct workload conditions and normal/demo names. A template build preserves parameter expressions; it does not exercise each condition.
* Concern: The plan does not name the combinations or expected resource sets that its compiled inspection must prove. Inspecting default parameters alone cannot establish that environment-only/API-only deployments omit job alerts, that auth renewal needs both background deployment and token storage, or that a bare activation switch cannot enable alerts without the evidence reference.
* Impact: Source definitions could refer to absent/wrong-name jobs or accidentally enable candidates while still compiling and passing pre-existing tests.
* Smallest useful change: Add the explicit local acceptance matrix below. Specify separate rules for the four IoT failure signals, or otherwise demonstrate independent triggering; placing all four criteria in one allOf would require simultaneous breaches. Bind the new module/workbook resources into the existing parameter-guard dependency chain.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T01 names bounded inline compiled-template assertions for each case below, including expected job IDs, flags, action group and full metric contracts. Preserve stdout/results in the changes record; do not add committed test source or claim evaluation against Azure.
* Decision route: Direct planner correction. Candidate evaluation settings remain proposals; live values/approvals remain human-owned.

| Local acceptance case | Required result |
| --- | --- |
| Default candidate activation | Every new metric rule disabled. |
| Activation false with a supplied reference | Still disabled. |
| Activation true with empty or whitespace-only reference | Reject activation or keep every new rule disabled. Document which behavior is implemented. |
| Activation true with a nonempty synthetic reference | Only the source guard is demonstrated; no actual human approval is inferred. |
| deployApplications false, including deployEnvironmentOnly true | No job-scoped candidate for workloads not authored. |
| Applications true, background false | No job-scoped candidate, even if enableEntraTokenStore is true. |
| Applications/background true, token storage false | Orchestrator, ledger and import candidates only. |
| Applications/background/token storage true | Add auth-renewal candidate. |
| Normal/demo naming | Normal suffixes orchestrator/ledger-verify/import/auth-renewal; demo suffixes orch/audit/load/auth, using the demo application prefix exactly once. |
| Each IoT condition independently breaches | Its own disabled candidate exists without requiring any other failure signal to breach. Routing bootstrap is not interpreted as healthy ingestion. |
| All new source resources | Correct resource IDs, existing action group, no new identity, and existing guard dependency preserved. |

The supplied W1 reference supports namespace Microsoft.App/jobs, Executions,
state dimension and Maximum aggregation. It does not enumerate state values:
Failed remains a proposed filter requiring later activation verification.
The supplied W2 reference supports namespace Microsoft.Devices/IotHubs and
dimension-free Total for d2c.telemetry.ingress.sendThrottle,
d2c.telemetry.egress.dropped, d2c.telemetry.egress.invalid and
d2c.telemetry.egress.orphaned. Maximum > 0 is a failure-presence candidate,
not an exact count of distinct failed runs. No new metric needs console-log
content or IoT device-identity logs.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Exhaustive runbook coverage needs a source-accurate reconciliation list

* Related IDs: FR3, AC3, AC4, P01-T02, P02-T02; research C3/C6-C10.
* Evidence: Details groups existing metric, ledger, Key Vault and budget rules without enumerating their exact predicates or a completeness check. infra/main.bicep:415-605 contains eight of the catalogue's source entries including the two overall budget notification conditions; infra/modules/keyvault.bicep:77-133 and infra/modules/iothub.bicep:215-250 supply the rest. The issue owner explicitly corrects the original issue narrative's claim that ledger alerts are absent.
* Concern: Broad labels conceal important distinctions. The existing Foundry rule counts all ClientErrors, not proven throttle-only errors. The ledger mismatch description mentions a failed job, but its query matches only LEDGER_DIGEST_ALERT. Both budgets notify at 80 percent actual and 100 percent forecast, not four actual/forecast combinations or a hard spending cap. A generic runbook entry must not overstate these source contracts.
* Impact: Operators could triage the wrong signal or believe a failure/cost control exists when it does not. Catalogue completeness and all-criterion traceability would remain difficult to verify.
* Smallest useful change: Adopt the reconciliation inventory and 15-row criterion boundary below as the P01-T02/P02-T02 oracle. Preserve existing source names/behavior except the requested ledger time correction. Every actual rule/notification and new candidate needs a distinct addressable entry; separate missing-signal procedures must be visibly labelled gaps, not installed alerts.
* Action owner: Planning parent.
* Exact resolving evidence: Revised task details require a one-to-one inventory-to-runbook-anchor reconciliation, with source predicate, proposed accountable role, triage, safe response, recovery evidence, activation/approval boundary and gap status. Require one evidence/gap matrix row for each of B1-B4, R1-R8 and T1-T3, linking exact source/docs and identifying unresolved runtime/human evidence. No issue checkbox changes or new application implementation are needed.
* Decision route: Direct planner correction. Actual owner appointments, response limits, live thresholds, privacy approval and OD-51 remain deferred, not requests to the user during this task.

### Catalogue reconciliation oracle

Names below are source-name patterns, not invented deployed IDs. Candidate
suffixes/anchors must be selected by implementation and reconciled to this list.

| Entry | Source contract / required distinction |
| --- | --- |
| Existing alert-${prefix}-foundry-throttle | ClientErrors Total > 20 over PT15M, evaluation PT5M; severity 2. Not throttle-only evidence. |
| Existing alert-${prefix}-sql-cpu | cpu_percent Average > 85 over PT15M, evaluation PT5M; severity 3. |
| Existing alert-${applicationPrefix}-api-5xx | Requests Total > 5, statusCodeCategory 5xx, PT5M/PT1M; applications conditional. |
| Existing alert-${applicationPrefix}-api-restarts | RestartCount Total > 3, PT15M/PT5M; applications conditional. |
| Existing alert-${applicationPrefix}-ledger-digest-mismatch | Count of LEDGER_DIGEST_ALERT console matches > 0 in PT1H; does not independently select failed executions. |
| Existing alert-${applicationPrefix}-ledger-verify-missing | Fewer than one LEDGER_DIGEST_OK match; correct the outer search to PT26H and retain explicit 26-hour predicate. Missing success includes missing execution/logging, not proof of tampering. |
| Existing alert-${vaultName}-secret-expiry | AzureDiagnostics near-expiry/expired notification operation matches, Count > 0 in P1D; event collection/operation availability still needs verification. |
| Existing alert-${vaultName}-denied-access | AzureDiagnostics 401/403 matches, Count > 4 in PT1H, evaluation PT15M; not arbitrary Key Vault failures. |
| Existing budget-${prefix}: actual80 | Resource-group monthly budget notification > 80 percent actual; email notification, not action-group enforcement or a hard cap. |
| Existing budget-${prefix}: forecast100 | Same budget, > 100 percent forecast. |
| Existing budget-${iotHubName}: actual80 | Filtered IoT transport resource allocation notification > 80 percent actual; not reconciled AI spend or a second independent overall cap. |
| Existing budget-${iotHubName}: forecast100 | Same filtered IoT budget, > 100 percent forecast. |
| New orchestrator failure candidate | Executions Maximum > 0, proposed state Failed; normal/demo name and workload conditions. |
| New ledger job failure candidate | Same metric contract, distinct from digest-mismatch content and missing-success rules. |
| New import job failure candidate | Same metric contract; event-triggered workload, not a daily schedule assumption. |
| New optional auth-renewal failure candidate | Same metric contract; conditional on token maintenance and background workload deployment. |
| New IoT ingestion throttle candidate | d2c.telemetry.ingress.sendThrottle Total > 0; no invented dimensions. |
| New IoT routing dropped candidate | d2c.telemetry.egress.dropped Total > 0; dead-endpoint delivery loss. |
| New IoT routing invalid candidate | d2c.telemetry.egress.invalid Total > 0; endpoint incompatibility, not a generic payload-validation signal. |
| New IoT routing orphaned candidate | d2c.telemetry.egress.orphaned Total > 0; no matching route, including fallback. |
| Gap procedure: agent-tasks-poison | No authored per-queue depth/age producer; service-wide queue counts/audit logs are not substitutes. |
| Gap procedure: import-jobs-poison | Same explicit gap, separately addressable queue procedure; no automatic empty/replay action. |
| Gap procedure: AI limits | Calls/tokens/budget/expiry owner-and-response contract; no installed aggregate breach alert established here. |
| Gap procedure: RAI harm/incident | Task/version-bound suspension, protected evidence, manual routes and human-gated restart; infrastructure alerts do not establish this automation. |

There are 12 existing rule/notification entries, seven mandatory new candidates
and one optional auth candidate, plus explicitly separate gap procedures.
The eight existing alert resources remain behaviorally distinct from the four
budget notification conditions. Proposed role routing is not an appointment.

### Complete issue evidence/gap boundary

B/R/T labels are positional identifiers assigned by this critique to the current
issue's criteria, not new requirements or claimed official requirement IDs.
All remain operationally unproven at this authoring boundary.

| Criterion | Existing or proposed authorable evidence | Unresolved evidence / accountable follow-up |
| --- | --- | --- |
| B1: job, poison, ledger and IoT alerts | Existing ledger rules; disabled job/IoT definitions; poison procedures | Per-queue producer, actual metric/log signals and verified delivery; Operations/engineering, with human activation approval. |
| B2: availability, errors, latency and budget/cost dashboard | Aggregate workbook; configured budget explicitly labelled; missing sources disclosed | Availability tests, valid samples, actual/forecast billing data and reconciliation; Operations/Finance. |
| B3: each alert has runbook and owner | Exhaustive catalogue with proposed accountable roles | Named actual appointments, recipients, capacity and response limits; owner. |
| B4: diagnostics exclude personal/raw/chat data | Existing diagnostic configuration and explicit privacy gap | Source-side exclusion/redaction and restricted evidence/retention approval; engineering/DPO/Compliance. Aggregate projections do not resolve ingestion. |
| R1: per-task/release indicators, denominators, windows, thresholds, owners and response | PRD contract and blocked activation register | Approved task/release monitoring contract and actual monitoring/incident appointments; owner/domain leads. |
| R2: unsupported claims, misses, stale review, challenges, cohort errors and full review effort | Criterion-specific evidence/gap rows linked to existing audit/report surfaces | Complete aggregate producers, applicable denominators and observed measures; application/domain follow-up. |
| R3: missing samples/usage/approvals/thresholds not zero or green | Workbook's explicit Insufficient/Blocked states; PC-001 | Runtime/query failure behavior and approvals; engineering/owner. Approval rate is not safety evidence. |
| R4: seeded critical harm or breach creates incident and suspension | Existing incident/restart contract, research C10 | Connected monitoring trigger, owned incident and witnessed suspension evidence; incident owner. |
| R5: reconcile windows/events across restart; disabled tasks show ownership/manual route | Existing task/version incident contracts and proposed procedure | Reconciled denominators/repeated events, actual ownership/manual-route evidence; incident/domain owner. |
| R6: no raw prompts/source text/sensitive reasons/tokens/identities in telemetry; restricted evidence separate | Diagnostic gap disclosure and protected-evidence boundary | Source-side enforcement and approved separate evidence retention; engineering/DPO/Compliance. |
| R7: constructed thresholds offline only; named-human live approval | Disabled candidates and reference guard | Genuine named-human threshold/activation evidence; owner. Nonempty string checks do not prove approval. |
| R8: existing audit/report/UI surfaces; no new platform or unrelated IoT dependency | Reuse existing workspace/action group and link current API/SQL/report/incident contracts | End-to-end RAI implementation through those surfaces, not delivered by workbook links; application follow-up. |
| T1: owned AI calls/tokens/budget/expiry limit alerts/runbooks | Explicit gap procedure and existing bounded authority documentation | Full breach signalling, actual alert owners and approved limits; owner/application follow-up. |
| T2: capability/period AI usage beside billing with visible variance | Workbook states missing reconciled feed; tokenomics synthesis records partial assistant usage already exists | Complete capability/period metering, approved prices and Azure billing reconciliation; engineering/Finance under OD-51. Do not claim no usage exists anywhere or that this workbook implements it. |
| T3: 80 percent actual / 100 percent forecast budget notice is not cap | Existing overall/IoT budget definitions and source-accurate runbooks | Operational notification evidence remains unproven; Finance/Operations. Do not invent a hard cap or live budget approval. |

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Planned validation would use an unspecified external temporary directory

* Related IDs: Test Ownership and Coverage Lock, AC5, P02-T01.
* Evidence: The plan places compiled ARM/validation output in a new external temporary directory. Details repeats a new external directory without an execution-safe path. infra/tests/test_bicep_policy.py:324-338 uses TemporaryDirectory without an explicit directory; its default location is affected by the process temporary-directory environment. The active execution constraints prohibit file operations in /tmp, /var/tmp or temporary directories and require created files to be relative to the project.
* Concern: Running the named suite unchanged with default environment can write outside the allowed project boundary. Calling a directory external does not make its use authorized.
* Impact: The otherwise appropriate bounded validation can violate execution restrictions or fail before providing AC5 evidence.
* Smallest useful change: Replace the external/temporary-directory instruction with a uniquely named, project-relative validation-output location. Before running the existing suite, route Python's temporary-file base to that allowed project-local location, without modifying test source. State how only current-task generated outputs are retained/excluded or cleaned under the retention policy; do not remove historical tracking evidence.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T01 gives the allowed project-relative output path and environment setup for the existing TemporaryDirectory caller, and the changes record reports the resolved scratch base with the bounded commands/counts/skips. If policy still prohibits that helper's temporary-directory operation, record it as blocked rather than running it. No forbidden path is used and no test-source change or heavy gate is introduced.
* Decision route: Direct planner correction, not authorization for broader filesystem operations.

## Strengths and Residual Risk

* The selected job metric aggregation and dimension-free IoT metrics are supported by the supplied official references. Independent alert activation remains disabled; no new telemetry producer is invented.
* The ledger correction addresses the real outer-window defect. Retaining P1D as the evaluation window while overriding the query range to PT26H is materially different from merely putting ago(26h) inside a 24-hour search. Keep severity, names, hourly evaluation and action routing unchanged.
* Source-only assertions should check the compiled override and query predicate together; service execution and actual console table availability remain explicitly unverified.
* The workbook correctly separates request success from availability, uses sampled/weighted rather than averaged-platform p95 intent, and does not claim scenario SLO attainment.
* Configured budget, billing cost, partial existing assistant usage and reconciled capability/period AI economics are distinct evidence classes. Unknown actual/forecast spend and absent reconciled feeds are not zero cost or whole-issue delivery.
* No poison replay, digest deletion, control disablement or automatic restart is authorized. Independent manual/emergency/statutory routes and resident consent remain intact.
* The caller's no-heavy-gate direction is explicit. Document the absent full local gate and limit publication to the requested draft; do not fabricate a receipt or claim merge/release readiness.

## Questions or Blocking Evidence Gaps

* No user response is required for these four plan corrections.
* Live owner/threshold appointments, privacy exclusion, runtime signal acceptance and OD-51 remain unresolved by design. They must stay explicit in the matrix and draft PR, not become authoring-stage questions or invented approvals.
* If a table schema or supported fallback cannot be established from the supplied source boundary, record that query as an unresolved source-validation gap and constrain its claims. Do not expand into Azure reads or a new observability implementation.

## Limitations

* No implementation exists for the new module/workbook/runbook yet. Findings concern plan completeness and source contracts, not defects asserted in uncreated files.
* No build, test, KQL execution, Azure call, deployment, secret read, private-data read, full gate or independent implementation Review was performed.
* The metric reference does not prove deployment-specific dimension values or signal production. The supplied research's unconfirmed table and operational dependencies remain unconfirmed.
* Only this critique artifact was written. Plan, details, research, session state, application/test sources and prior evidence were left unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define the workbook schema and absent/empty/error result contract, then directly incorporate all four dispositions into plan/details and finalize.
* User response required: No. No significant/divergent authoring choice remains; human activation and financial/privacy decisions stay deferred.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/monitoring-146-plan.md](.copilot-tracking/plans/2026-10-27/monitoring-146-plan.md) | Supplied final-candidate plan, unchanged. |
| [.copilot-tracking/details/2026-10-27/monitoring-146-phase-details.md](.copilot-tracking/details/2026-10-27/monitoring-146-phase-details.md) | Supplied phase details, unchanged. |
| [.copilot-tracking/research/2026-10-27/monitoring-146-research.md](.copilot-tracking/research/2026-10-27/monitoring-146-research.md) | Supplied evidence baseline, unchanged. |
| [.copilot-tracking/reviews/2026-10-27/monitoring-146-plan-critique.md](.copilot-tracking/reviews/2026-10-27/monitoring-146-plan-critique.md) | Complete critique and full actionable finding set. |

## Next Steps

Active planning parent: resolve PC-001 through PC-004 directly, preserve this
original Complete / Revise outcome and record dispositions. Finalize without
another critique, then continue only the already-authorized bounded
implementation, one independent Review and one draft PR with Refs #146.
No user action or new human decision is required to correct the plan.

---
title: Monitoring 146 phase details
ms.date: 2026-10-27
---

Task ID: 146. Source-only boundary; no deployment. Research C1-C10 and W1-W4
are the evidence baseline; no repeated research is needed.

Current status: P01/P02 complete. Combined infrastructure regressions: 87 passed,
zero skips. Official workbook JSON Schema, 32 workload/name combinations, six
activation combinations, metric contracts, ledger lookback, 24 runbook anchors
and 15 criterion rows passed source checks. See changes record for commands,
original failure/correction and external output path. KQL/portal/live acceptance
not run. P03 independent Review and draft publication remain parent-owned.

<!-- phase: P01 -->
## P01: Author monitoring definitions and operator guidance

<!-- task: P01-T01 -->
### P01-T01: Candidate alerts and workbook

Use the existing action group/workspace, jobs named by the existing normal/demo
conditions and optional auth-renewal workload. Executions Maximum >0 filtered
state Failed is a candidate presence check, not an exact distinct-run counter.
IoT dimension-free sendThrottle and dropped/invalid/orphaned counts use Total >0.
Every new alert is disabled unless explicit activation and approval reference
are supplied; no actual threshold approval is inferred. Workbook takes Bicep
resource IDs/budget via loadTextContent and substitutions; no hardcoded tenant,
resource IDs, operator emails or fabricated telemetry tables.
Request success is not availability. Availability tests need their own sample
denominator; request p95 uses item-count weights, is not a scenario SLO.
AI metering, harm, reconciliation and actual/forecast spend are explicitly
Blocked/Unknown with links to existing surfaces and operator instructions.

PC-001: use workspace KQL AppRequests(TimeGenerated, _ResourceId, ItemCount,
Success, DurationMs) and AppAvailabilityResults(TimeGenerated, _ResourceId,
ItemCount, Success). Typed empty datatable plus union isfuzzy=true handles
absent tables; no rows produces Insufficient and null rates/latencies, not zero.
Missing required sample fields are excluded and surfaced as invalid samples.
Queries filter exact Application Insights resource and selected time range.
Static text always warns that access/query errors are Blocked, not empty success.
Include window/as-of, weighted denominator and sampling caveats. Local source
assertions and constructed arithmetic do not constitute KQL service execution.

<!-- task: P01-T02 -->
### P01-T02: Ledger and runbooks

Set overrideQueryTimeRange PT26H and explicit ago(26h) predicate without changing
the existing rule names/severity/action. Keep a supported evaluation window.
Document existing metric rules, ledger rules, Key Vault rules, overall/IoT
budget notices and new candidates. Add proposed role, symptoms, triage, bounded
response, recovery evidence and separate approvals. Never empty/replay poison
queues, delete digests, disable controls or restart a suspended AI task on a
metric alert. Document missing per-queue signal as a gap, not an approximation.
Map all four base, eight RAI and three tokenomics criteria separately.
PC-003: adopt the critique's 12-entry existing inventory (eight rules, four budget
notification conditions), seven mandatory new metric candidates, optional auth
candidate and four distinct gap anchors (two queues, AI limits, harm incidents).
Reconcile source predicate to each anchor. Foundry ClientErrors is not proven
throttle-only; digest mismatch marker is not a failed-execution detector.

<!-- task: P01-T03 -->
### P01-T03: Navigation

Link the runbook/workbook from infra/README.md and docs/reference/README.md;
append one dated knowledge-base log entry. Do not edit memory, immutable source
snapshots, original case study or unsigned business requirements.

<!-- phase: P02 -->
## P02: Validate and reconcile

<!-- task: P02-T01 -->
### P02-T01: Local validation

Existing compile helper in infra/tests/test_bicep_policy.py uses local
az bicep build (not Azure). Run test_bicep_policy, test_iothub_module,
test_container_contract, test_governance and test_secret_lifecycle together.
Compile main and the new module into a new external directory; parse serialized
workbook after substitution; inspect every new rule enabled flag and resource
scope/action plus optional job array. Check doc links and git diff.
No Python test source additions under caller's Bicep/docs restriction.
No --all, --changed, what-if, deployment, actual dataset access or paid inference.

PC-002 compiled assertion matrix: applications false (environment-only both
values) gives no job candidates; background false gives no job candidates even
with token store true; apps/background true gives three jobs plus optional auth
only with token store. Check both normal/demo suffixes/prefix exactly once.
Activation false stays disabled with empty or nonempty reference; activation
true with empty/whitespace reference stays disabled; nonempty synthetic reference
only demonstrates source gating, not human approval. IoT has four independent
rules, never an allOf requiring simultaneous failures. New module must depend on
the existing guard. Inspect scopes, action group, metric namespace/aggregation/
state filter and ledger override. Source JSON assertions cover absent/empty/
invalid/populated/error paths and weighted arithmetic; KQL/portal behavior not run.

PC-004: use a uniquely named external scratch directory for compiled output;
parent has no prohibition on /tmp. No historical evidence cleanup. The critique's
claimed environment prohibition does not apply to this execution.

<!-- task: P02-T02 -->
### P02-T02: Evidence reconciliation

Record exact commands/counts/skips, file changes and any amendment/divergence.
Keep issue criteria unmarked if they depend on operation or actual appointments.
All authored query/metric assumptions remain activation verification tasks.

<!-- phase: P03 -->
## P03: Review and publication

<!-- task: P03-T01 -->
### P03-T01: Independent Review

Fresh independent worker, read-only implementation scope, writes only the dated
Review artifact. Assess actual current diff, source-only criteria and human
boundaries; preserve execution and outcome separately. No second Review.

<!-- task: P03-T02 -->
### P03-T02: Draft PR

Use gh authenticated id/login privacy-safe local commit email for both author
and committer. Include required Co-authored-by trailer. Push only the existing
topic branch, never force; one draft PR to main with Refs #146. State no full
gate by explicit caller restriction, no deployment, every unproven criterion
and human decisions. Leave merge/activation to the owner.

---
title: Monitoring 146 implementation evidence
ms.date: 2026-10-27
---

Task ID: 146. Execution: Implement complete, P01/P02 scope. P03 belongs to
the parent Review/publication stages. Plan and details dated 2026-10-27.

## Intended Changes

Disabled job/IoT alert candidates, aggregate operations workbook, complete
runbook catalogue/evidence matrix, corrected 26-hour ledger search, navigation.
No application/test code changes, telemetry producers, Azure operations or
human/live approvals.

## Plan and Critique State

One original critique Complete / Revise preserved. PC-001/002/003 incorporated;
PC-004 rejected with evidence of parent/caller execution authority in plan.
No repeat critique. Source-only checks below completed; operational gates remain
unmet. P01/P02 checkmarks mean authored/locally checked scope only.

## P01: Authored Source

* New operationalMonitoring.bicep: three job candidates plus optional auth job;
  four independent dimension-free IoT failure rules; default disabled with
  trimmed approval-reference guard. Existing action group and guard chain reused.
* Workbook: two aggregate sample-weighted KQL sources with typed empty fallbacks,
  explicit Insufficient/Blocked/Unknown states, configured budget and no invented
  AI metering/cost. Microsoft AppRequests/AppAvailabilityResults schemas checked
  2026-10-27; no KQL execution or portal rendering.
* main.bicep: correct normal/demo job naming, optional-workload gating, existing
  ledger rule overrideQueryTimeRange PT26H and budget notification description.
* Runbook: 12 existing rule/notification entries, eight candidate anchors, four
  missing-signal procedures and all 15 issue-criterion evidence/gap rows.
  Infra/reference navigation and append-only knowledge log updated.

## Implementation Amendments and Divergences

Ordinary current-state correction: initial existing Bicep policy run discovered
the new module prefix was demo-specific, violating stable backing-service
monitor names. Changed its prefix input to the shared workload prefix (job names
remain correctly demo-specific). No existing tests changed. This preserves
approved intent and naming, not a significant divergence or new user decision.

## P02: Validation

| Check | Exact execution and outcome |
| --- | --- |
| Strict Bicep compilation | `az bicep build --file infra/main.bicep --stdout > /dev/null`: passed, no analyzer diagnostics |
| Initial Bicep policy suite | `python3 -m unittest discover -s infra/tests -p test_bicep_policy.py -q`: 50 run, one failure on new monitoring module's demo prefix; corrected shared prefix, no test changes |
| Initial related regressions | `PYTHONPATH=infra/tests python3 -m unittest test_iothub_module test_container_contract test_governance test_secret_lifecycle -q`: 37 passed |
| Final combined regression | `PYTHONPATH=infra/tests python3 -m unittest test_bicep_policy test_iothub_module test_container_contract test_governance test_secret_lifecycle -q`: 87 passed, zero skips |
| Compiled/schema/contract assertions | Session-owned external validation script: 32 deployment/name combinations, six activation combinations, metric contracts/action group/scopes, true PT26H override, official Microsoft workbook JSON Schema validation, missing/empty/invalid/error source contract, 24 actual runbook anchors, all 15 criterion rows, relative links and constructed weight arithmetic: passed |
| Source formatting | `git diff --check`: passed |

Final external generated output: `/tmp/ama-monitoring-146-avrs3goz` contains
compiled ARM/module, resolved workbook and retrieved official schema. It contains
constructed resource identifiers only, no deployment output or secrets.
Validation helper lives outside the repository in the session files directory.
The helper was corrected for Bicep's compiled createObject parameter wrapper and
ARM object-property representation before its successful run; these were harness
errors, not production pass claims. Its anchor assertion identified three
nonmatching prose anchors; actual runbook headings were corrected before pass.
No committed Python/test additions or historical artifact cleanup.

Source/schema assertions are not KQL interpretation or an Azure Portal render.
Constructed weighting uses 19 successful weight at 100ms plus one failed weight
at 1000ms: denominator 20, failure 5%, weighted nearest-rank p95 100ms. This is an
arithmetic oracle, not service verification. Actual metric `state=Failed`,
table availability, KQL warnings/access errors, notification delivery, RAI drills,
privacy exclusion and billing reconciliation were not executed.

No heavy gate warranted or run (zero --changed invocations); --all explicitly
prohibited by caller. No gate receipt, full local publication-gate pass, build/
type-check of unaffected application packages, hosted check or deployment
acceptance is claimed. Draft-only publication is the caller-requested boundary.

## Human Decisions and Remaining Work

Actual owner appointments/live thresholds, privacy controls, poison-queue and
AI/harm aggregate producers, approved cost reconciliation and operation remain
outside authoring acceptance. Draft PR must expose these and use Refs #146.

## Review Handoff

P01/P02 implementation complete and reconciled with plan/details. One fresh
independent Review is next; P03-T01/T02 remain pending. Review must distinguish
source-only authoring from unmet whole-issue/live acceptance and preserve its
original outcome. No new implementation after that Review in this task.

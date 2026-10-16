---
title: Environment parameter sets review
description: Single post-implementation evidence review for issue 137
ms.date: 2026-10-16
---

## Scope and Evidence

Task ID: issue-137. Task slug: environment-parameter-sets.
Review scope: full offline implementation and acceptance audit, not deployment.
Plan: .copilot-tracking/plans/2026-10-16/environment-parameter-sets-plan.md
Details: .copilot-tracking/details/2026-10-16/environment-parameter-sets-phase-details.md
Critique: .copilot-tracking/reviews/2026-10-16/environment-parameter-sets-critique.md
Changes: .copilot-tracking/changes/2026-10-16/environment-parameter-sets-changes.md
Research: .copilot-tracking/research/2026-10-16/environment-parameter-sets-research.md

## Opening Review State

Goal: compare the implementation with issue 137's five criteria, issue 139's
offline gates and current user constraints. Evidence is ready: P01 and
P02-T01 complete; compiled tests, all-file build/lint, Python lint/types and
local App smoke passed. First comparison is environment inputs/defaults and
owner-decision boundaries. Read-only boundary: all source/planning evidence;
write authority only this review record. No implementation blockers.
Fresh live checks and pilot decisions are explicitly unavailable.

## Execution Status

Review execution: Complete, executed once on 2026-10-16.
Outcome: Residual work. Offline implementation is supported; live region/
quota evidence and pilot decisions remain deliberately unaccepted.

## Plan-to-Change Reconciliation

| Marker | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | main.bicep, three bicepparam files, guard/SQL modules, deploy.py | Reconciled: production-safe independent inputs, private SQL, open pilot locations and ama-only CLI |
| P01-T02 | test_bicep_policy.py/test_deploy.py plus coupled edge/governance assertions | Reconciled: four added methods; existing matrices/mutations retained and extended |
| P01-T03 | infra/README.md and reference README/log | Reconciled: one differences table, historical/current distinction, naming/tags and human boundaries |
| P02-T01 | Tool execution results recorded below | Reconciled: complete offline validation and synthetic local App run |
| P02-T02 | This single review | Acceptance audited below; no issue checkboxes edited |
| P02-T03 | Commit/push/PR | Delivery remains the parent's next action; not yet claimed |

## Acceptance Audit: Refs #137

| Acceptance criterion | Result | Exact evidence and limits |
| --- | --- | --- |
| Parameter files for dev, test and pilot exist, with no secrets and with placeholders marked | Met offline | main.bicepparam, main.test.bicepparam, main.pilot.example.bicepparam; all compile and actual values/placeholders are asserted. Pilot is intentionally a non-deployable example; no actual IDs or secrets added |
| Differences between environments are documented in one table (profile, SKUs, redundancy, retention, public access) | Met | infra README Environments table; old competing profile table replaced by prose |
| Production profile is the default and development relaxations are explicit | Met offline | Production defaults; dev explicitly disables purge/quarantine only. Test/pilot production. Extended compiled matrix and guard-bypass mutations; no live ARM claim |
| Region and quota choices are parameters with recorded checks, not assumptions | Partial; fresh checks unmet | location/sqlLocation and model/version/SKU/capacity are inputs, regionCheckReference/quotaCheckReference are empty marked placeholders with named guards. Dated historical observations retained and labelled insufficient; no fresh Azure region/quota result or pilot choice invented |
| Resource naming and tagging convention is documented and applied | Met offline | Existing prefix/compact/hash expressions and key service names asserted; all main modules forward allTags; semantic union assertion proves required tags beat overrides while extras survive. Component refinements/untaggable children documented |

The coordinator, not this task, owns any issue-checkbox changes at merge.
No pilot deployment readiness or operational acceptance is asserted.

## Quality Gate Audit: Refs #139

| Criterion | Result | Evidence |
| --- | --- | --- |
| Configured significant lint warnings fail | Met offline | Existing error-level bicepconfig; real unused-parameter mutation fails build/lint; all 17 Bicep files build/lint |
| Rule set checks documented security controls | Met offline | Existing compiled private endpoints, no keys, Entra-only SQL, purge and immutability assertions/mutations retained; permanent private SQL strengthened |
| Production cannot deploy with public access | Met offline | Exact named guard failures across profile/public/purge/quarantine matrix and bypass mutation rejection; live ARM diagnostic remains unverified |
| Unsupported combinations fail clearly | Met offline | Named nonempty guard contracts and exact semantic failure sets, including independently missing region/quota records and unresolved locations; all resources wait for guard |

## Implementation-Time Updates and Critique

PC-001 through PC-004 were applied directly and preserve user intent:
independent development opt-outs, synthetic valid-reference test baseline,
README reconciliation and exact acceptance mapping. PC-005 was rejected
because its prohibition on system/session temporary directories was not
supported by the caller's actual requirements. Existing isolated temporary
fixtures and explicitly synthetic App data remain appropriate.

The full-suite failures in coupled source-text SQL/environment assertions
were expected consequences of the changed contract; those assertions were
updated in place to stronger private-SQL and unresolved-pilot checks. No
test removal, new approval, new pipeline/check name or unrelated feature.
Proper ClassVar/mapping annotations enabled mypy on the compiled suite.
No significant divergent decision or dependent-work pause was required.

## Validation Evidence

All source project paths below were absolute in PYTHONPATH during execution.
The session-local pip venv installed missing ruff/mypy and editable source
distributions; no cloud extras or private datasets were required.

| Command / check | Result | Evidence |
| --- | --- | --- |
| REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q | Passed | 121 tests, no skips, final run 41.861 s; all three real bicepparam files compiled |
| az bicep build --stdout and lint for infra/*.bicep and infra/modules/*.bicep | Passed | All 17 files; no Azure login/deployment |
| ruff check, isolated E/F/I/B/UP and formatting | Passed | deploy.py, test_deploy.py, test_bicep_policy.py |
| mypy --check-untyped-defs | Passed | Same three files; no suppressions/casts added |
| tests.test_auth.RuleHttpTests from src/api | Passed | Six synthetic local App HTTP/persistence tests, healthy loopback server started/stopped and temporary fixtures removed |
| git diff --check and Markdown/link review | Passed | Changed relative reference links target infra README; no legacy/config/dataset modifications |
| Azure what-if, deployment, quota/current capability checks | Not run | Offline infrastructure slice; pilot region/subscription ownership unresolved; no cloud operations needed |
| Actual human/pilot/operational approval | Not performed | Not delegated to agents; Legal/Compliance/DPO exercise owner unchanged |

Initial validation failures and corrections are retained in the changes
record, not presented as passing runs.

## Findings and Routing

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Pilot decisions and fresh live checks remain open

* Evidence: empty pilot locations and region/quota references, historical
  check register and current user instruction.
* Impact: examples cannot be used as deployment-ready pilot parameters.
* Destination: distinct owner-led deployment-readiness follow-up, not a code
  defect or a return to implementation within this task.
* Owner/next action: the project owner decides pilot region/subscription
  ownership, obtains dated provider capability/quota/cost evidence for the
  exact configuration and records the reviewed references privately.
* Operational human approval, private networking/edge acceptance and legal/
  retention validation are separate readiness boundaries, not inferred here.

## Defects

No material implementation defect identified within the assessed offline
boundary. Missing live checks are deliberately preserved, not waived.

## Plan Follow-Up Assessment

The plan's owner-decision/fresh-check follow-up remains valid, outside this
implementation and grounded in the current user request. It is represented
once as RV-001; do not start Azure discovery or another RPI loop automatically.
No second Review or in-task correction cycle is requested.

## Outcome and Closeout Routing

Execution: Complete. Outcome: Residual work.
Offline artifacts and gates meet the bounded implementation contract.
The region/quota criterion is only partially evidenced, with live acceptance
unmet. Delivery parent may commit/push/open the requested PR; no merge,
deployment, issue-checkbox update or follow-up work has been authorized here.

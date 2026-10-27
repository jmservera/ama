<!-- markdownlint-disable-file -->
---
title: API minimum replicas implementation changes
description: Scoped source changes and offline verification evidence
ms.date: 2026-10-27
---

# RPI Changes: API minimum replicas

## Metadata

* Task ID: aca-api-min-replicas-2026-10-27
* Task slug: aca-api-min-replicas
* Related plan: .copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md
* Implementation date: 2026-10-27

## Execution Status

* Status: Complete (implementation scope only)
* Declared invocation scope: Full plan P01-P02
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01
* Remaining markers: None
* First boundary: P01-T01, described bounded parameter and parent forwarding.

## Execution Summary

Implement `apiMinReplicas` default 0 in shared API sources, examples,
documentation and existing tests. No other workload behavior changes.
One critique completed; original Revise preserved, PC-001 rejected as an
inapplicable worker-local storage constraint. Parent plan is Ready.

## Approved Write Boundary

Five Bicep/parameter files, infra README, two existing infra tests, and task
RPI artifacts only. Generated templates stay on stdout. No Azure operations,
private datasets, secrets, full gate, uv or publication without mandatory gate.

## Completed Work

### Bounded minimum and parent forwarding

* Task: P01-T01.
* Files: infra/modules/containerapps.bicep, infra/main.bicep and all three existing
  main parameter examples.
* Change: apiMinReplicas integer default 0, bounds 0..4, description distinguishing
  cost-safe demos and explicit production 2; main forwards to API scale.
* Evidence: only API minimum changes in resource bodies; examples select 0.
* Validation: compiled schema/forwarding and example tests passed.

### Documentation and existing regression contracts

* Task: P01-T02.
* Files: infra/README.md, infra/tests/test_bicep_policy.py,
  infra/tests/test_resident_demo_deploy.py.
* Change: environment table and rule explain 0..4, default 0, cold starts and
  private production 2; remove stale fixed-two main API wording.
* Tests: two new methods only, compiled schema and 0/1/2/4 forwarding/evaluation,
  compiled examples all 0. Existing policy retains max/probes/edge and adds
  explicit HTTP/agent scale invariants. Resident separation assertion is updated
  without changing its independent 0..1 scale/readback/what-if guards.
* Evidence: all 447 infra tests pass; no API max, HTTP rule, probes, authentication,
  agent/job or standalone resident source behavior changed.

### Scoped offline validation

* Task: P02-T01.
* Initial discovery: 362 tests, 10 errors from missing installed zava_forward
  distributions; first Ruff invocation also failed because ruff was absent.
  These environment failures are preserved, not reclassified as source failures.
* Installed only after failure, in task-owned session files venv using pip:
  `--no-deps -e src/core -e src/agents -e src/api -e src/orchestrator`,
  `PyYAML==6.0.3`, `ruff==0.17.1`, and hashed src/api/requirements.txt.
  No dependency manifest changed and no system/shared package install.
* Rerun: same existing infra discovery with REQUIRE_AZ_BICEP=1, task venv Python
  and task TMPDIR passed all 447 tests in 94.791s, no skips.
  Test output mentioning post-deployment checks comes from fake/local fixtures,
  not an Azure deployment in this task.
* All 24 existing Bicep entry points/modules build and lint successfully.
  Three example build-params outputs consumed in full by compiled tests; this
  supersedes the earlier interrupted output-shape probe, not its original record.
* Both changed test files pass existing Ruff rules and formatting; diff check clean.

## Implementation-Time Plan and Detail Updates

No material divergence. Use task-owned session files storage for temporary
files and any conditional dependency environment, with TMPDIR set for tests.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Azure CLI Bicep version | Local tooling | Passed | 0.48.1 |
| Parameter output shape probe | Existing dev example | Probe interrupted | Piping stdout to head closed its pipe early; CLI emitted BrokenPipeError. No source effect. Subsequent build-params checks will consume complete JSON. |
| Initial offline discovery | System Python | Failed: prerequisites | 362 tests, errors=10, missing source distributions |
| Initial Ruff | Changed tests | Failed: prerequisite | No module named ruff |
| Compiled API and parameter contracts | Existing infra tests | Passed | Included in final 447-test discovery |
| Full offline infra discovery | infra/tests | Passed | 447 tests, no failures or skips |
| Bicep build/lint | All 24 infra templates | Passed | No build/lint diagnostics |
| Ruff lint/format | Two changed tests | Passed | All checks passed; 2 files already formatted |
| git diff --check | Source diff | Passed | No whitespace errors |
| Live what-if, deployment and full gate | Cloud / full matrix | Not run | Explicit caller exclusions |

### Reproduction Commands

Run from the repository root with the documented source distributions and
test prerequisites installed using pip. This task used Python 3.12.3 and Bicep
0.48.1 in its task-owned external environment:

```bash
REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q
for file in infra/*.bicep infra/modules/*.bicep; do
  az bicep build --file "$file" --stdout > /dev/null || exit 1
  az bicep lint --file "$file" || exit 1
done
python -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_resident_demo_deploy.py
python -m ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py infra/tests/test_resident_demo_deploy.py
git diff --check
```

## Pre-Review Reconciliation

Plan markers/details are complete, changes evidence matches current source,
and no implementation task remains. Validation includes original prerequisite
failures and successful rerun. No material amendments or divergences.
Review readiness: Ready for one independent implementation Review, not
exact-commit publication acceptance.

## Blockers

Publication only: complete infrastructure gate is mandatory but explicitly
excluded by the caller. No push or PR will be attempted without its evidence.

## Remaining Work

One independent Review and local commit. No source implementation remains.

## Follow-Up Items

Canonical plan Follow-Up Items retains later authorized complete-gate,
exact-head assessment and publication work.

## Return-to-Caller State

Implementation Complete for full plan P01/P02; active parent continues one
Review. Publication remains Blocked separately. No full receipt or live
runtime/cost/availability claim is made.

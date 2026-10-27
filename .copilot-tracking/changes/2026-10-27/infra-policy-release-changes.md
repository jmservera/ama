<!-- markdownlint-disable-file -->
# RPI Changes: infra-policy-release

## Metadata

Task ID: 147-138. Implementation date: 2026-10-27.
Plan: .copilot-tracking/plans/2026-10-27/infra-policy-release-plan.md
Details: .copilot-tracking/details/2026-10-27/infra-policy-release-phase-details.md

## Execution Status

Complete; full plan P01/P02, including P01-T01/P01-T02/P02-T01/P02-T02.
Write boundary: Bicep, deployment YAML, existing infra tests, related runbook/
exception metadata and dated RPI artifacts only. No runtime source changes.

## Execution Summary

Implement independent authoring gaps identified by research. One plan critique
executed, original Revise preserved, PC-001/002/003 corrected directly in plan
and details before implementation. No owner decision inferred.

## Completed Work

### Pilot lock invariant and historical exception

P01-T01: infra/main.bicep and modules/guard.bicep add pilotRequiresLocks
using the existing named minLength guard; no default dev/test behavior change.
Existing compiled-policy matrix tests all environment/lock combinations and
rejects forced-ok mutation. EX-001 reason is historical, not public SQL authority;
owner and dates preserved. No new assignment scope or pricing change.

### Exact-main CI prerequisite and release inventory

P01-T02: .github/workflows/src-deploy.yml adds read-only source-ci prerequisite
before build. Exact workflow endpoint, explicit GET, bounded filters and complete
response success predicate fail closed. Existing pipeline test executes actual
Bash under fake gh for 14 positive/negative cases, including nonzero API exit with
plausible success output. The four-project release build now emits SPDX from the
same scanned/exported image and requires artifact success before docker save.
Both vulnerability scan contracts retained separately. Existing names unchanged.

### Runbook and criterion-level acceptance boundary

P02-T02: infra/README.md documents manual main source CI, rebuilt-image SBOMs,
pilot guard, historical exception and unresolved owner decisions.

| Issue / criterion | Authoring evidence | Acceptance boundary |
| --- | --- | --- |
| #147 AC1 owner/cost decisions | Governance table names @jmservera; paid plans remain opt-in | NOT satisfied: coverage/subplan appraisal, actual cost and owner activation decision absent |
| #147 AC2 policy assignments or management decision | Existing governance.bicep; all-file compile | Already ticked by owner; no deployment/compliance claim |
| #147 AC3 pilot locks/tags | Existing pilot example and allTags; new pilotRequiresLocks guard/mutation matrix | Authoring strengthened; no observed pilot deployment |
| #147 AC4 exceptions/expiry/owner | Existing EX-001, 2026-12-31, Juan Manuel Servera; historical reason clarified | Already ticked by owner; no new exception/renewal |
| #138 AC1 environment OIDC | Existing per-environment plan/publish/deploy login/client separation | Authored/offline only; actual federation NOT RUN |
| #138 AC2 PR what-if/result | Existing trusted infra-plan.yml, candidate SHA and artifact | Contracts tested; actual what-if/artifact NOT RUN |
| #138 AC3 approval/templates/parameters | Existing environment check, same compiled parameter payload | Contracts tested; actual approval/deployment NOT RUN |
| #138 AC4 versioned pushed images used | Existing per-project tags, run-bound digests, pull admission; new exact CI/SBOM gates | Contracts tested; registry push/deployment NOT RUN |
| #138 AC5 automatic fail-closed health/auth | Existing private SQL and 200/401/302 probes; real local synthetic HTTP tests | Local tests pass; deployed health/SQL/model acceptance NOT RUN |
| #138 AC6 no secret values in logs/repository | Existing quiet operations, synthetic canary tests, no stored-secret references; new read-only job | Offline boundary only; no live workflow log observation, no blanket secret-free claim |

No issue checklist edited. Use Refs #147 and Refs #138, never Closes.

## Implementation-Time Plan and Detail Updates

No scope/architecture divergence. PC-001 complete GET/response predicate,
PC-002 compiled matrix/mutation integration, PC-003 separate scan/SPDX assertions
implemented in their planned existing files. One additional test method, within
maximum four; no removals or new runtime code/files.

## Validation Record

| Check | Result | Evidence |
| --- | --- | --- |
| Initial host targeted compiled-policy suite | PASS | 50 tests, 82.567s |
| Initial host pipeline suite | FAILED environment prerequisite | 29 tests; installed local API smoke could not start because no src distributions installed |
| Initial host Ruff | UNAVAILABLE | command not found |
| Prerequisite recovery | PASS | Isolated external session venv; pip editable --no-deps src/core,agents,api,orchestrator,importer; PyYAML 6.0.3, Ruff 0.17.1 and hashed src/api requirements |
| REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q | PASS | 452 tests, 140.796s, zero skips, including local synthetic API smoke |
| az bicep build --file each --stdout | PASS | All 25 infra/*.bicep and infra/modules/*.bicep; Bicep 0.48.1 |
| az bicep lint --file each | PASS | All 25 Bicep files |
| actionlint -config-file infra/tests/actionlint.yaml | PASS | infra-plan/src-deploy/src-ci/mvp-ci/mvp-validation |
| Ruff check/format --isolated, line length 100, py312 | PASS | Modified test_bicep_policy.py and test_pipeline.py |
| git diff --check | PASS | No whitespace errors |
| Optional scoped heavy gate | NOT RUN | Bounded authoring changes, not large; zero invocations |
| Full --all gate / Azure operations | NOT RUN | Explicitly prohibited by user |

Dependencies restored only after missing prerequisites manifested. External venv:
/home/azureuser/.copilot/session-state/f6de980f-cfa4-4d1f-bc9e-d3ce1529694e/files/infra-venv.
No deployment, cloud what-if, workflow dispatch, environment/protection change,
secret/.env read, private dataset access or billable inference.

## Pre-Review Reconciliation

Plan/details checked only for local authoring scope, changes evidence and
runbook current, validation complete, no active-plan work remaining.
Ready for one independent Review. Live/owner gates remain explicit follow-ups.

## Blockers and Follow-Up Items

No independent authoring blocker. Owner @jmservera must decide Defender cost/
coverage/activation and provision environments/OIDC/private runners for live
acceptance. All live pipeline/whole-application acceptance remains Not run.

## Remaining Work

No active implementation markers. One independent Review and publication remain.

## Return-to-Caller State

Implementation complete, parent-owned continuation to Review. No Azure
operations. Owner cost decision and real pipeline acceptance remain outside
authoring completion and block whole-issue acceptance.

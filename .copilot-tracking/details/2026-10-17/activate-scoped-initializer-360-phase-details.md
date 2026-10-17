<!-- markdownlint-disable-file -->
# RPI Phase Details: Activate scoped initializer #360

## Metadata

* Task ID: 360
* Task slug: activate-scoped-initializer-360
* Date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/activate-scoped-initializer-360-plan.md
* Research: .copilot-tracking/research/2026-10-17/activate-scoped-initializer-360-research.md

## Phase Index

| ID | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Reviewed API-only slice | Complete | P01-T01, P01-T02 |
| P02 | Exact activation | Complete | P02-T01 |
| P03 | Evidence/publication preparation | Complete; parent Review/publication next | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Reviewed API-only source slice

Context: Research C1/C4 show two reviewed custom roles; W4 previews four
Creates, including unapproved relay. Preserve default compatibility and exact
GUIDs. This is a conditional selection, not a new role design.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Conditional omission and tests

Add described `includeResultRelay` bool default true to existing template.
Condition both relayRole and relayAssignment with the same parameter. Retain
API definition/assignment and all reviewed actions, IDs and resource scopes.
Existing relay resource remains read-only metadata; avoid unneeded changes to
shared guard or defaults. Do not add jobs/write or tenant roles.

Tests belong in existing identity matrix and compiled-policy files. Reuse
compile_bicep/resources/evaluate helpers rather than a new framework. Assert
conditions for both relay resources and no condition on API resources,
default true, exact role properties/scopes and two/four active authorization
resources. Test maximum three additions; no removals. Mutation uses a deep
copy of compiled output, never working Bicep.

Completion: source diff and focused semantic/regression tests.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Quality and independent source gate

Run az bicep build/lint on template and guard; existing identity and compiled
policy tests with REQUIRE_AZ_BICEP=1; lint changed Python with repository
conventions. Install existing prerequisites only upon missing-dependency
failure. Do not run broad application suites for an RBAC boolean.

Fresh read-only independent reviewer assesses source diff and tests, exact
owner boundary and permission conditions. Reviewer can write only a dedicated
source-review evidence artifact, cannot approve broader owner scope. Source
review must finish with no material defect before P02 apply. This bounded
predeployment gate is not the later full-task RPI Review.

<!-- rpi:phase id=P02 -->
## P02: Exact authorized live activation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Preview, apply, verify

Use existing deployment command, group ama, incremental mode, exact:
apiName=ca-cutover-test-demo-api,
initializerIdentityName=id-cutover-test-init,
includeResultRelay=false.

Record source hash after review and preview without retaining unrelated Ignore
payloads. Require status Succeeded, only same-root Ignore rows plus exact API
role definition and API child assignment Creates/NoChange. Check roleName,
four actions, assignableScopes ama, no dataActions, target scope, role ID and
principal binding to existing MI. Unresolved principal reference in what-if
must match reviewed identity expression and be resolved by identity read
before apply, then actual assignment readback afterward.

Expected role ID:
ama/providers/Microsoft.Authorization/roleDefinitions/0d8c4586-d46e-514c-9c19-680d9f068755.
Expected API assignment:
ca-cutover-test-demo-api/providers/Microsoft.Authorization/roleAssignments/3a7e0803-3997-5cbe-af9c-c9776b37f3a7.
Expected principal: 3830883a-f4af-44f8-bff8-8859b78fc2f8.

If exact preview passes and input/source unchanged, deploy same source/inputs.
Do not run restart or create temporary jobs to test capabilities. Read back
definition, assignment, relay absence and unchanged demo ingress/revision
metadata. Readback establishes grant, not effective token propagation or MI
runtime execution. On real denial, capture only code/action/scope metadata;
never retry with broader authority. Retain any partial successful resource
creation in receipt; no deletion rollback is authorized.

<!-- rpi:phase id=P03 -->
## P03: Evidence and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Durable factual evidence

Update infra/README.md, docs/architecture/cutover-evidence-pack.md,
docs/reference/README.md, and append docs/reference/log.md without rewriting
prior entries. Distinguish historical unapplied IAM from current outcome.
Receipt includes exact IDs/actions, approval limitation, safe outputs and
unchanged restrictions; no private roster/secret/job tags.
Keep #360 d/e and private publisher blocked. Changes record owns ordered
Research/Plan/Implement/Review phase log, tests, amendments and live outcome.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Review/publication handoff

After implementation reconcile plan tasks/details/changes and required
validation. Prepare pointer-first handoff for parent to activate rpi-review
exactly once and independently assess complete bounded diff/evidence. Parent
owns state/final review dispositions and publication after Review; later work
remains outside current task. Parent records privacy-safe account email
locally, commit trailer, pushes only requested topic, creates main PR
Refs #360 and verifies remote head matches local. No closing syntax, merge
or force push. Preparation completes this task; Review and actual publication
must have separate parent evidence before session stops.

## Implementation Completion Evidence

All P01/P02/P03 implementation/preparation tasks complete. Bicep template and
scope-guard build/lint passed. Final combined identity/compiled-policy suite
59 passed without skips. Existing compiled-test Ruff lint/format passed.
Additional F-only check on the older identity test exposed unchanged F841
`allowed_conn`; same finding reproduced from HEAD, left outside scope.
With only that baseline diagnostic ignored, F-only check passed. No claim
that the older file has a clean unqualified lint baseline.

Exact preview and live receipts record source hashes and exact permitted
changes/readback. Live operation Succeeded; canonical URI/expected identity
Read verifier amendments are documented in changes. Runbook/KB/log updated;
append-only prefix and new receipt link anchors verified. One independent
full-task RPI Review and publication remain parent lifecycle work.

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
| P04 | Explicitly approved relay scope delta | Apply/readback/evidence/targeted review complete; final publication handoff ready | P04-T01, P04-T02 |

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

<!-- rpi:phase id=P04 -->
## P04: Explicitly approved relay delta (2026-10-17)

Prior Review and publication at 38e6abf verified complete on the continuing
clean topic/main PR #379 before this work. New owner true approves exactly
existing-job encrypted-tag read/write definition+assignment, resolving RV-001.
No Bicep source edit or new full RPI/repeated plan critique.
The caller's includeResultTagRelay wording maps to the reviewed template's
actual `includeResultRelay=true`, not a new parameter.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Preview, apply, independent readback

MI id-cutover-test-init:
principal 3830883a-f4af-44f8-bff8-8859b78fc2f8,
client 8fd2cb23-cc1c-4ee5-ab8d-4b6fdff4564e.
Job job-cutover-test-init in existing cae-cutover-test, ama.
Role 64ec5d6d-f8ae-51ab-a93a-394f6cc97c6c; assignment
8e9a497e-3b90-50e2-a783-93e58755165b scoped only to that job.
Fresh what-if must contain only those Creates, same-root Ignore/NoChange and
proven unchanged API/benign guard. No arbitrary Modify/Delete or unrelated creation.
Actual preview's API Modify is limited to known exact MI reference/canonical
role URI and principalType NoEffect. Normalize only those two values, require
whole before/after equality, then compare independent actual API role and
assignment to original receipt. Preserve raw Modify in evidence. Any other
delta blocks apply; this gate implements caller's proven-API-unchanged case.
Explicitly verify role actions exactly tags/read and tags/write, no
dataActions/exclusions, assignableScopes ama only and exact MI reference.
Check prior API definition/assignment matches existing receipt before/after.
Same reviewed source hash and inputs required; no secret reads, tag values,
test writes, temporary jobs/configuration/execution or runtime checks.
A separate read-only verifier must check actual post-apply facts/operations,
not simply trust deployment success.

Completed: exact approved relay apply Succeeded and separate post-apply
verifier passed. Receipt includes two actions, existing-job scope/principal,
canonical role URI, unchanged prior API/AcrPull, preserved observed job/API
metadata and sanitized operations. Existing API/empty-guard idempotent PUTs
are labeled Create by ARM; two effective grants only are new.
No source change, test tag, job execution or permission denial.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Evidence and targeted final-state review/publication

Preserve original first-approval receipts and original full Review. Add
explicit dated delta, actual sanitized receipts and a labelled targeted review
of only this continuation. No new source expected; if source changes become
necessary, pause apply until standard independent source review.
Update factual runbook/evidence/index and append-only log. Commit once at end
with authenticated privacy-safe email/trailer, push same branch/PR and verify
final head outside commit. No extra publication receipt commit after final
head. Publisher/tenant/browser/SQL/AI and d/e remain unproven.

Completed evidence/review/handoff: primary assistant inline targeted final-state
review appended to the existing canonical Review without changing the original
independent review. No defects found in exact approved relay delta.
All P04 implementation markers complete; one normal final commit/push and
external remote/PR-head verification remain the terminal parent action.
No already-pushed-final-head claim is made inside this self-referential record.

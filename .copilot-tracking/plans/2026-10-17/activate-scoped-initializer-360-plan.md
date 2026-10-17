<!-- markdownlint-disable-file -->
# RPI Plan: Activate scoped initializer #360

## Task Metadata

* Task ID: 360
* Task slug: activate-scoped-initializer-360
* Date: 2026-10-17
* Planning status: Ready; independent critique Pass
* Details: .copilot-tracking/details/2026-10-17/activate-scoped-initializer-360-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/activate-scoped-initializer-360-plan-critique.md

## Executive Summary

Preserve the reviewed roles and default behavior while adding an explicit
`includeResultRelay` boolean, default true, to omit both existing-job tag
resources when false. Independently review this source amendment before
deploying only the API read/restart role and its demo-API-scoped assignment.
Exact preview and principal/scope/actions readback are complete; deployment
Succeeded, with no permission denial observed. Runbook/KB updates are prepared
for final independent RPI Review and main PR publication.

### What You May Not Know

The merged template has no temporary-job lifecycle role. Those operations
belong to the setup operator, whose existing permission metadata already
reports ["*"]. That capability is not approval for runtime execution. Existing
initializer-job tag writes are a different scope/operation and remain
unapproved. API-only activation cannot unblock the private publisher or prove
staff/browser/SQL/AI acceptance; #360 d/e remain UNMET.

### Unresolved Decisions or Blockers

Relay activation requires separate exact approval; it does not block the API
subset if the amendment passes independent source review and exact what-if.
No source review means no live deployment of amended source.

## User Decisions and Requirements

* Owner 2026-10-17 explicitly requests FULL ordered RPI on clean requested
  branch/worktree at latest main e065ecd2; #375 is merged, do not duplicate it.
* Boolean true permits only reviewed API read/restart and temporary staff-job
  lifecycle permissions in ama; no broader roles, tenant roles, spending,
  networking or deletion.
* Flag existing initializer-job relay tag permission ambiguity; it is not
  implicitly approved. API subset may use a small proper safely reviewed
  amendment, not improvised extension scope.
* Target actual ca-cutover-test-demo-api and existing id-cutover-test-init.
* No Graph/SQL/Key Vault secrets, payload inventory, restarts, browser
  acceptance, build, new infrastructure or old-stack modification.
* Commit dated phase evidence and factual runbook/KB/index/append log; use
  privacy-safe GitHub account email/trailer, push/open main PR Refs #360, no
  closing syntax, merge or history rewrite; stop after outcome/real blocker.

## Goals

* Activate only the authorized API permission slice or document concrete
  authorization/permission failure, preserving all unrelated resources.
* Make approval distinction and remaining live gates durable and auditable.

## Scope and Non-Goals

* In scope: conditional omission of relay resources, focused offline guards,
  independent source review, exact RBAC-only preview/apply/readback, evidence.
* Non-goals: new actions/role designs, operator lifecycle provisioning,
  whole-repository cleanup, runtime execution, release or #360 acceptance.

## Functional Requirements

* `includeResultRelay=false` excludes the relay definition AND assignment.
  Default true preserves merged behavior, all GUIDs/actions/scopes unchanged.
* API restart role stays four exact actions, no wildcard, dataActions or
  settings/secrets access, assigned only at the selected demo API.
* Deployed assignment must bind exact existing initializer principal and role.

## Non-Functional Requirements

* No hand-edited compiled templates or broad role fallback.
* Incremental ama-only deployment from independently reviewed source.
* Preview allows exactly two Creates (or exact already-correct NoChange),
  same-root Ignore rows only; stop on Modify/Delete/unsupported action/resource,
  unresolved nonprincipal payload or wrong target. A metadata-only nested
  guard deployment is allowed by source but must not introduce workload writes.
* Sanitize CLI output to role/principal/scope/action metadata only. Never
  retain credentials, unrelated Ignore payloads or job-tag contents.

## Acceptance Criteria

* Compiled tests verify default four and subset two authorization resources,
  exact action sets and correct conditions; disabled-relay mutation is caught.
* Existing Bicep lint/build, focused identity/compiled guard tests pass.
* Fresh independent source review before any amended-template live deployment.
* Exact API-only what-if and approved names/scope recorded before create.
* Successful create requires exact definition/assignment readback; a genuine
  failure is recorded as failure without payload or a fabricated denial.
* No tag role/assignment activated, old API untouched, no workload/network writes.
* Durable ordered phase evidence and factual KB/runbook updates; independent
  one post-implementation RPI Review and main PR publication; d/e still UNMET.

## Sources

* Research: .copilot-tracking/research/2026-10-17/activate-scoped-initializer-360-research.md, C1-C4/W1-W4.
* Prior #360 review, resource/publication receipts: historical dependencies only.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reviewed API-only source slice

Dependencies: Research complete and one plan critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add conditional relay exclusion and focused guards

Existing template amended; default/actions/GUIDs unchanged. Two compiled tests
added, existing matrix assertion extended; false excludes both relay resources.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate and obtain independent predeployment source review

Build/lint template/module; run focused guard/matrix tests. A fresh read-only
reviewer must assess complete source diff before deployment; fix genuine
coupled defects or block, no unreviewed live workaround.

Completed: Bicep build/lint, 11 identity tests, 48 compiled-policy tests and
Ruff lint/format; independent source review PASS with no material findings.
Evidence: .copilot-tracking/reviews/2026-10-17/activate-scoped-initializer-360-source-review.md.

<!-- rpi:phase id=P02 -->
### [x] P02: Exact authorized live activation

Dependencies: P01, including independent source review, complete.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Preview, gate, apply and read back exact API-only RBAC

Use `includeResultRelay=false`, demo API and existing initializer MI; record
exact permitted IDs, input/source hash and sanitized results. Stop affected
action on failure; do not infer MI execution from role readback.

Completed: exact two-Create preview and single successful create; canonical
role GUID, ama-only assignableScopes, exact API assignment/principal/actions
read back. Relay absent; old API/initializer metadata and AcrPull preserved.
Verification adjusted only for Azure's canonical subscription-level role URI
and expected identity Read, not source/actions/scope. No redeployment.

<!-- rpi:phase id=P03 -->
### [x] P03: Evidence and publication handoff

Dependencies: exact live outcome or concrete blocker established.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Reconcile documentation and implementation evidence

Update existing runbook/evidence/KB index and append log, leaving historic
receipts intact; record changes, amendments, validation and retained blockers.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Prepare independent Review and publication handoff

Prepare one independent Review's exact evidence pointers and publication
boundary. Lifecycle parent then executes Review once, routes residuals to
later work, resolves privacy-safe GitHub email before commits, includes
trailer, pushes topic/opens main PR Refs #360, no closing syntax. Owner merges.
Review/publication are parent lifecycle actions, not implementation source
work; preparation must not claim they already ran.

Completed: plan/details/changes reconciled; exact preview/live receipts and
source-review evidence prepared, final combined 59 tests passed; parent owns
one independent RPI Review and subsequent privacy-safe publication.

## Test Ownership and Change Budget

* Canonical: infra/staff-initializer-rbac.bicep; existing test_identity_rbac.py
  source matrix test plus test_bicep_policy.py compiled test helpers.
* Generated: only temporary build output, not committed.
* Removals: none. Maximum new tests: three in existing test files; no new
  production Python module, role, permission action or CI job.
* Semantic: evaluate compiled resource conditions for true/false/default and
  assert exact active role types/actions/scopes. Regression: default behavior
  and role matrix preserved; mutation removing one relay condition must fail.
* Validation evidence: Bicep build/lint and focused tests, code-review artifact,
  exact what-if JSON projection, live readback or sanitized genuine error.

## Dependencies

* Source review is a hard gate before live apply, independent of later RPI Review.
* Existing role-create/assignment capabilities are not substitute owner approval.
* Private publisher/relay/tenant/browser/runtime are later release prerequisites.

## Critique Disposition

Exactly one independent final-candidate critique executed by
scoped-360-plan-critique using rpi-plan-critique. Verdict Pass; no actionable
findings. Planner accepts the result; no further critique or user decision
needed. Source-review and exact-preview gates remain mandatory.

## Follow-Up Items

* Exact existing-job tags/read + tags/write approval: owner; outside current
  approval. No deployment of that role/assignment.
* Existing private publisher supplies immutable worker digest: publisher owner;
  no infrastructure, build, networking or spend in current task.
* Genuine tenant/browser/role/SQL/AI acceptance, then later explicit retirement:
  human operators/owner; #360 d/e remain UNMET.

## Handoff

Implementation evidence: .copilot-tracking/changes/2026-10-17/activate-scoped-initializer-360-changes.md.
All implementation tasks complete. Source-review/exact-preview/live readback
gates passed. Parent next activates one independent full-task RPI Review,
then publishes exact outcome/blocker and stops as requested. Required human
tenant/runtime acceptance remains unperformed, not approved by these markers.

<!-- markdownlint-disable-file -->
# RPI Changes: Activate scoped initializer #360

## Metadata

* Task ID: 360
* Task slug: activate-scoped-initializer-360
* Date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/activate-scoped-initializer-360-plan.md
* Details: .copilot-tracking/details/2026-10-17/activate-scoped-initializer-360-phase-details.md

## Execution Status

* Status: Complete for full-plan implementation and handoff preparation.
* Declared scope: full plan.
* First execution boundary: P01-T01; no live apply before P01-T02 source review.
* Completed markers: P01/P01-T01/P01-T02, P02/P02-T01, P03/P03-T01/P03-T02.
* Remaining active implementation markers: none. Independent Review complete; main PR #379 published and implementation head verified.
* Approved writes: conditional relay exclusion, existing focused tests,
  dated evidence and directly related runbook/KB documentation; API-only
  RBAC deployment after review/exact what-if.

## Ordered Phase Log

| Phase | Activation and disposition |
| --- | --- |
| Research | rpi-research activated first; focused wider/deeper/contrarian inline cycle completed; Ready with unapproved relay excluded |
| Plan | rpi-plan activated second; plan/details finalized; one independent rpi-plan-critique Pass, no findings |
| Implement | rpi-implement activated third; all implementation tasks complete; exact API-only apply/readback succeeded |
| Review | rpi-review activated fourth; fresh independent full-task Review Complete, no implementation defects; three Medium wider residuals routed to later owners |

## Execution Summary

API-only permission deployment Succeeded after independent source review and
exact two-Create what-if. Role/principal/actions/scope readback passed.
Existing-job tag relay remains unapproved/absent; no temporary lifecycle role
or job was created. Existing private publisher remains blocked; no new
image/infrastructure attempted. #360 d/e remain UNMET.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Baseline unittest identity matrix | infra/tests/test_identity_rbac.py | Failed dependency | 11 tests, 1 missing zava_forward import; install existing source distributions in isolated venv before rerun |
| Restored identity matrix | Existing editable core/agents/api installed --no-deps in session venv | Passed | 11 tests |
| Bicep build/lint | Staff RBAC and unchanged scope guard | Passed | az bicep 0.48.1, no diagnostics |
| Compiled guard suite | infra/tests/test_bicep_policy.py | Passed | 48 tests, including two new semantic/mutation guards |
| Ruff lint/format | Changed compiled-policy test file | Passed after format | Existing Ruff 0.17.1 installed after command-not-found; two long new lines formatted, lint/format/diff clean |
| Final combined suite | Existing identity + compiled-policy modules, REQUIRE_AZ_BICEP=1 | Passed | 59 tests, no skips, after final formatting |
| Extra F-only lint | Existing identity test file | Pre-existing failure isolated | F841 allowed_conn reproduced on HEAD line130/current133; unrelated line unchanged; --ignore F841 passes, no baseline fix |
| Evidence hygiene | Source hashes, append-only KB prefix, receipt anchors | Passed | Both JSON receipts match deployed source hashes; original log prefix byte-for-byte retained |

## Completed Work

### P01-T01 conditional relay selection

Added one boolean default true to existing Bicep, conditioning both relay
resources. API role definition/assignment, actions, IDs and scopes unchanged.
Extended existing identity-matrix assertion; two compiled tests prove true
four/false two authorization resources, exact actions/principal expression/
scope, no extra resource types, and reject independently removed relay
conditions or changed default. No generated templates committed.

Added runbook selection/approval warning, including incremental omission
does not revoke any already-existing grant.

### P01-T02 independent source gate

Fresh scoped-360-source-review agent completed bounded STANDARD source
review, PASS with no actionable findings; source safety confirmed under false.
Reviewer independently compiled and ran new compiled tests; one unrelated
identity import unavailable there, all 11 passed in parent's declared venv.
Review artifact: .copilot-tracking/reviews/2026-10-17/activate-scoped-initializer-360-source-review.md.
Source gate passed; exact preview and live readback still required.

### P02-T01 exact pre-apply gate

Fresh API-only what-if `staff-iam-360-api-20261017` Succeeded with exactly two
Creates and 94 same-root Ignore rows: role
`0d8c4586-d46e-514c-9c19-680d9f068755` at ama and assignment
`3a7e0803-3997-5cbe-af9c-c9776b37f3a7` at ca-cutover-test-demo-api.
No job tag resources, workloads or networking changes. Exact four API actions,
assignable scope and existing principal reference checked programmatically;
identity read resolves to 3830883a-f4af-44f8-bff8-8859b78fc2f8.
Receipt: .copilot-tracking/changes/2026-10-17/activate-scoped-initializer-360-what-if.json.
Bicep SHA256 bf2a63b667d238bb4ec54bf6a36dea6bf4c9e64d90ae6996a718cdfba1f7caf8;
guard unchanged. Source/input hashes will be rechecked immediately before
incremental create. Owner's explicit API-only authorization applies; relay
remains excluded. This records the intended authorized action before apply.

### P02-T01 actual apply and readback

Deployment `staff-iam-360-api-20261017` returned Succeeded, correlation
2177965b-1d42-4709-962b-3475e2186264. No Azure permission denial observed.
Full sanitized metadata receipt:
.copilot-tracking/changes/2026-10-17/activate-scoped-initializer-360-live-receipt.json.
Same reviewed source/inputs used; no second deployment.

The initial post-create verifier incorrectly required RG-addressed
roleDefinitionId. Azure returned canonical subscription-level URI for the
same GUID. A second read-only verifier initially rejected the expected
existing MI Read operation. These local assertions were corrected narrowly:
exact canonical role GUID, sole ama assignableScopes, exact demo API scope
and principal/action set, permitted RBAC/empty-guard Creates plus exact MI
Read/output evaluation. Both corrected checks passed; no role source,
authorization, action, scope or provider behavior changed.

Actual role readback:
0d8c4586-d46e-514c-9c19-680d9f068755, four reviewed API actions only,
empty dataActions/notActions/notDataActions. Assignment
3a7e0803-3997-5cbe-af9c-c9776b37f3a7 binds existing principal
3830883a-f4af-44f8-bff8-8859b78fc2f8 only at ca-cutover-test-demo-api.
Initializer assignment inventory now contains preserved AcrPull and this
assignment only. No relay definition/assignment, job grant or old API grant.
Both APIs' observed environment/revision/ingress metadata unchanged; demo
deny-all retained. Existing job identity/environment metadata unchanged.

### P03-T01 durable evidence

Runbook records exact approval, independent source gate, selection commands,
role/assignment IDs/actions and readback limits. Evidence pack and KB index
route to dated API-only receipt; original #375 historical statements explicitly
distinguished. Append-only KB entry added without rewriting previous entries.
No legal, operational, image publication or human acceptance claim introduced.

### P03-T02 Review/publication preparation

Pointer-first evidence ready: research C1-C4/W1-W4; finalized plan/details and
critique; source-review Pass; exact what-if/live receipt; complete source/docs
diff against e065ecd2. GitHub account resolved by gh api user as jmservera /
8036360; repository-local author email set to
8036360+jmservera@users.noreply.github.com. Parent must include required
Copilot trailer for author/committer and publish only requested topic to main
PR using Refs #360, without closing/merge/force push.

## Independent Review and Parent Disposition

Exactly one independent full-task RPI Review by scoped-360-full-rpi-review:
execution Complete; bounded verdict Conformant with justified divergence,
no implementation defects. Three Medium residual findings: RV-001 exact relay
approval, RV-002 existing private publisher, RV-003 genuine human runtime
acceptance and later separately approved retirement. Parent wider outcome is
**Residual work**, not overall release conformance or #360 closure.

Independent reviewer passed all three changed tests, compared receipt source
hashes and links/log history, and assessed parent's 59-test evidence and
disclosed baseline lint. Only canonical Review record changed during Review.
No second Review, live reexecution, closure fix or child task was started.
The parent now publishes the reviewed exact outcome and stops as requested.

## Publication and Stop

Implementation/phase evidence committed as
4bf12775ca4025a15cd2c196547fc047375fd6e1 and pushed normally to
chore/activate-scoped-initializer-360. Main PR #379 OPEN:
https://github.com/jmservera/ama/pull/379 .
Local HEAD, origin branch and PR head matched that SHA; both author and
committer use the authenticated privacy-safe address and required trailer.
No issue closing syntax, merge, forcepush or unrelated source work.

Publication receipt:
.copilot-tracking/changes/2026-10-17/activate-scoped-initializer-360-publication-receipt.json.
Initial PR check rollup was empty; no remote CI/rubric success is claimed.
An evidence-only completion commit records the stopped session; final head
is verified against origin/PR outside its self-referential receipt.
Owner explicitly requested this stop: no follow-up child, extra Review,
runtime execution or further Azure mutation. #360 d/e remain UNMET.

## Implementation-Time Plan and Detail Updates

P03-T02 clarified as Review/publication preparation, not a requirement to run
the next lifecycle phase inside Implement. This removes a circular completion
claim while preserving required independent Review and publication as parent
actions. Plan/details/summary reconciled; no user requirement changed and no
new critique needed. Existing dependency restoration is local judgment.

## Blockers

* Unapproved existing-job tag grants excluded; full template must not be deployed.
* Private publisher and human tenant/runtime acceptance remain later blockers.
* Initial missing source/Ruff dependencies resolved in isolated session venv.

## Pre-Review Reconciliation

Plan markers/details/changes/summary/handoff reconciled. All implementation
tasks complete; source tests and exact actual outcome recorded, retained
blockers routed as follow-ups. Parent's next phase is exactly one independent
full-task RPI Review, then publication. Source and unrelated work remain
unchanged during Review; human acceptance stays explicitly unperformed.

## Follow-Up Items

Relay approval, existing private publisher, human tenant/runtime acceptance and
eventual explicitly approved retirement, as recorded in plan.

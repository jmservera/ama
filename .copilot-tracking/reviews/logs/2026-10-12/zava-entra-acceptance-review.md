---
title: API Authentication Initialization and Deployed Logo Review
description: Single review of the delivered initializer and logo repair, with separate tenant and browser acceptance
ms.date: 2026-10-12
---

## Scope and Evidence

* Task ID: zava-entra-acceptance-2026-10-12.
* Review date: 2026-10-12.
* Review scope: Full current task: completed P01/P03 and outstanding P02.
* Assessed boundary: Callback-only initialization, profile isolation, identity
  validation, preservation and explicit errors; generated/image asset
  permissions and deployed PNG; publication and separate live acceptance.
* Plan: .copilot-tracking/plans/2026-10-12/zava-entra-acceptance-plan.md.
* Phase details: .copilot-tracking/details/2026-10-12/zava-entra-acceptance-phase-details.md.
* Plan critique: Unavailable; no critique artifact is recorded for this
  owner-directed bounded implementation.
* Changes: .copilot-tracking/changes/2026-10-12/zava-entra-acceptance-changes.md.
* State: .copilot-tracking/rpi-sessions/2026-10-12/zava-entra-acceptance-state.json.
* Other evidence: Source commit 0723508, publication record af1bc84, PR #65,
  initializer/migration/MVP tests, CI, ACR db2 and deployed revision
  ca-forward-test-api--0000001.

## Opening Review State

* Interpreted review goal: Assess the delivered changes first, then route only
  concrete remaining work; do not repeat the parent reset's completed Review.
* Review scope: Full current task; P02 remains unclaimed, not silently promoted
  to completed by the P01/P03 delivery.
* Evidence readiness: Plan, details, changes, state, source and recorded
  validation are available. A critique is unavailable and live tenant/browser
  acceptance has not been established.
* Acceptance basis: Owner-requested repeatable callbacks and supplied logo,
  approved P01/P03 requirements, and explicit P02 live acceptance requirements.
* First comparison boundary: Initializer discovery/preservation/error behavior,
  then packaging/live PNG, publication and residual acceptance.
* Active read-only boundaries: Review record and review-owned state only;
  no source, plan, details or changes edits during Review.
* Initial blockers: Existing operator lacks Graph authority; a real workbench
  user session is not established. Automatic-mode confirmation was unavailable,
  so the explicit Review request proceeds in manual mode.

## Execution Status

* Execution status: Complete.
* Review execution evidence: Compared the current plan, details, changes,
  state, initializer/tests, migration atomic write/tests, Dockerfile, static
  test and image CI. Rechecked the live CLI discovery, read-only initializer,
  deployed PNG, health/API protection, browser entry, links and exact-head CI.
  Missing tenant/browser access limits acceptance, not review execution.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Callback-only initializer | Reconciled | Existing client/FQDN discovery, minimal patch, verification and isolated login match the approved boundary |
| P01-T02 | Initializer tests and CI | Reconciled | Thirteen tests pass; current MVP validation workflow succeeds |
| P01-T03 | Documentation and publication | Reconciled | Source 0723508 and record af1bc84 are published through #65; guidance distinguishes creation from callback repair |
| P03-T01 | Public assets and packaging | Reconciled | New mode 0644, preserved existing permissions and non-root packaging match the diagnosed cause |
| P03-T02 | Rebuilt/deployed asset | Reconciled | Exact source PNG is returned from ready revision ca-forward-test-api--0000001 by UID 10001 |
| P02-T01 | Separate acceptance | Reconciled as incomplete | Remains unchecked; no authenticated acceptance is claimed |

The plan's root-cause paragraph describes the pre-fix PermissionError. The
checked P03 markers and deployment evidence establish the current repaired
state. Earlier changes-record paragraphs are implementation history; its
publication/completion section owns the current bounded status.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 | infra/scripts/initialize-api-auth.py; infra/tests/test_initialize_api_auth.py; .github/workflows/mvp-validation.yml; infra/README.md | Preserve an existing registration while synchronizing its deployed callback | Validated discovery and source 0723508 publication | Thirteen tests pass; real --check reaches Graph read and fails explicitly on permission denial | Conformant within the source-tested boundary; live Graph update is not accepted as executed |
| P03-T01 | tools/rename-zava.py; tools/rename-zava-tests.py; mvp/Dockerfile; .github/workflows/mvp-ci.yml | Repair public asset modes and make the packaged PNG readable without running as root | ACR db2 built from mode-0600 source; image CI also deliberately uses 0600 | Twenty-two migration tests and current image CI pass | Root cause addressed at generation and deployment boundaries |
| P03-T02 | mvp/tests/test_mvp.py; tools/rename-zava.md; docs/reference/README.md; docs/reference/log.md | Cover and document actual PNG delivery and preserve acceptance distinctions | Live 200 image/png, 14325 bytes, 644 x 225; source hash matches | Runtime UID 10001, asset mode 0644; health 200 and unauthenticated API 401 | Deployed asset repair verified; no fabricated claims or auth exception |

The initializer validates nonempty GUIDs, FQDN labels, enabled authentication,
tenant agreement and the returned app identity. Login refuses the operator
profile and requires a private directory. It updates only web.redirectUris,
merges old redirects, verifies their retention and skips writes on rerun.
Check-only mode never patches. Errors remain explicit rather than being
converted to success. Roles, assignments, names and credentials are outside
its mutation scope.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 | Added repeatable callback initialization instead of rerunning the creation helper | Owner requested an initialization script after reporting manual repair | Plan, details, changes and state preserve the existing registration and human bootstrap | Owner-directed bounded implementation; critique unavailable | Supported; avoids destructive role/secret side effects |
| P03 | Added packaging/generation repair and actual redeployment | Owner reported missing logo; runtime traceback established permission denial | P03 markers, details, changes and source/tests match the observed cause | Local repair consistent with confirmed branding/runtime intent; critique unavailable | Supported; no architectural or approval-boundary divergence |
| P02 | Kept real tenant/browser acceptance distinct | Owner-reported callback repair is not a verified tenant read or user session | Unchecked marker, blockers and completion qualifications agree | Requires external authority/session, not another speculative source change | Correctly unclaimed |

## Critique and Material Revision Assessment

* Latest critique dispositions: Unavailable. No critique artifact or execution
  evidence exists for this owner-directed implementation; none is invented or
  retrospectively claimed.
* Material revisions: The owner explicitly added the missing-logo repair.
  Its diagnosed local permission change preserves approved identity,
  application behavior and authentication boundaries.
* Dependent-work pause assessment: P02 has not been marked complete or bypassed.
* Justification assessment: The focused callback repair and permission
  normalization are supported by the owner direction and runtime evidence.
  This Review is not a substitute for an unrun plan critique.

## Plan Follow-Up Assessment

| Follow-up item | Why outside completed implementation | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| P02 live tenant state | Published initializer cannot supply missing Graph authority | Authorised registration owner/provisioning profile | Open; distinct external follow-up, RV-001 |
| P02 signed-in browser acceptance | Static/server/CI checks do not establish a real workbench session | Authorised workbench user | Open; distinct external follow-up, RV-002 |

The plan has no separate Follow-Up Items list. P02 explicitly carries the
residual acceptance requirement and remains unchecked, not a defect added to
P01/P03. No unrelated work is introduced to fill a follow-up quota.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Live registration state remains unverified

* Related scope: P02-T01 and P01's explicit live-validation limit.
* Evidence: Actual Azure CLI discovery confirms enabled auth and the existing
  configured client. Running infra/scripts/initialize-api-auth.py with --check
  through the current operator reaches the Graph registration read and exits
  1 with Insufficient privileges. The existing delegated M365 session's
  app-specific read also returns Insufficient privileges. No isolated tenant
  profile is present.
* Impact: The owner's callback repair cannot be independently checked; current
  tenant display name/roles and legacy-role transition remain unverified.
  No live successful initializer patch is claimed.
* Destination: Distinct P02 tenant-verification follow-up, owned by an authorised
  registration owner/provisioning identity; not rpi-implement.
* Smallest useful next action: Authenticate an authorised isolated provisioning
  profile, run --check, and inspect the registration name/roles before deciding
  whether an approved tenant update is necessary.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Real-user workbench acceptance has not run

* Related scope: P02-T01.
* Evidence: Playwright starts without an authenticated workbench tab.
  Navigating to the deployed root reaches Microsoft's "Sign in to your
  account" page rather than the workbench. No credentials, claims or
  authentication bypass were supplied.
* Impact: Scoped My cases, 443 open All cases, map/tiles and the logo in a real
  signed-in workbench remain unverified. Correct deployed PNG bytes do not
  establish this broader user journey.
* Destination: Distinct P02 authenticated-browser acceptance follow-up, owned
  by an authorised workbench user; not a code repair inferred from sign-in.
* Smallest useful next action: Complete legitimate Entra sign-in, verify the
  scoped lists/count/map/logo, and record observed outcomes or actual failures.

## Defects

* No implementation defect found in the assessed P01/P03 source, regression,
  packaging, deployment or publication boundary.
* RV-001/RV-002 are external acceptance gaps, not evidence that the delivered
  initializer or asset repair is defective.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | P02 tenant-verification follow-up | Authorised registration owner/profile | Missing authority and live state, not a source failure |
| RV-002 | P02 authenticated-browser follow-up | Authorised workbench user | Human sign-in prerequisite; no runtime bypass permitted |

No code-fix child loop is justified by the current evidence. Restarting
Research/Plan/Implement with the same missing authority would not resolve
either gate. A later observed defect can own a distinct child loop; this
Review and the parent reset Review must not be repeated to claim closure.

## Residual Work

* Complete P02 tenant verification and legitimate signed-in acceptance.
* Rubric scorer run 38258267201 completed successfully and published score
  45/100 for af1bc84 in workflow commit 17c2b8a. The recorded capstone floors
  remain unmet and its outcome is Incomplete; a non-regression workflow pass
  is not capstone acceptance. This pre-existing project-wide limitation is
  outside the current initializer/logo task, not a new source-fix requirement.
  The bot record was preserved by fast-forward, with no score edits.
* Automatic RPI mode confirmation was unavailable. The recorded session
  remains manual/stopped rather than falsely reporting a running auto session.

## Blockers and Remaining Work

* Blockers: Graph application read/manage authority is unavailable to the
  current operator; no legitimate workbench browser session is established.
* Remaining active work: P02-T01. An authorised profile and real user session
  are prerequisites; no source change can responsibly substitute for them.
* P01/P03 completion remains bounded and verified. Full task acceptance is
  not declared complete.

## Validation Evidence

| Command or check | Scope | Status | Summary |
| --- | --- | --- | --- |
| python3 -m unittest discover -s infra/tests -v | Initializer | Passed | Thirteen tests cover preservation, rerun, validation, isolation and explicit failure |
| python3 tools/rename-zava-tests.py with existing script dependencies | Migration | Passed | Twenty-two tests, including new mode 0644 and preserved existing modes |
| Actual az containerapp auth show query | Discovery | Passed | enabled true; existing client ID resolves with the script's flattened query |
| initialize-api-auth.py --check with current operator profile | Live initializer | Expected permission failure | Exits 1 at Graph registration read; no write attempted |
| m365 entra app get --appId with selected public app properties | Existing delegated session | Expected permission failure | Insufficient privileges; no alternate authorised registration-read path established |
| Deployed API static PNG probe | Asset delivery | Passed | 200 image/png, UID 10001, 0644, exact 14325-byte source hash |
| Container App ready revision/image query | Deployment | Passed | ca-forward-test-api--0000001; logo-20261012-permissions image |
| Public health and unauthenticated API | Protection | Passed | healthz 200; api/me 401 |
| Playwright navigation to the deployed root | Login boundary | Passed redirect; acceptance unavailable | Microsoft sign-in page reached; no authenticated workbench checks possible |
| Existing link checker and git diff --check | References and formatting | Passed | No new targets/fragments; eight existing missing targets remain |
| MVP CI 38258267105 at af1bc84 | Unit/API, image and SQL parity | Passed | Exact-head workflow success; includes restricted-mode/non-root image regression |
| MVP validation 38258266937 at af1bc84 | MVP and initializer CI | Passed | Exact-head workflow success |
| Prototype validation 38258267034 at af1bc84 | Existing prototype behavior | Passed | Exact-head workflow success |
| Capstone rubric scorer 38258267201 | Separate workflow/non-regression gate | Passed | Completed success; workflow record 17c2b8a measures af1bc84 at 45/100 |
| Existing capstone readiness floors | Project-wide gate outside this task | Not met | Workflow record says floors_met false and outcome Incomplete; not confused with a technical CI pass |
| Live successful Graph update; signed-in lists/map/name/roles | P02 and live initializer | Unavailable | Missing authorised profile/user session; not substituted with mocks or proxy headers |

## Outcome

* Outcome: Residual work.
* Outcome rationale: P01/P03 source and deployed asset meet their bounded
  acceptance requirements. P02 remains unexecuted behind real external
  authority/session gates, so full-task conformance is not claimed.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None supported | No repair loop started |
| Decision gap or invalid assumption | None identified in approved source direction | Critique execution remains explicitly unavailable |
| Material evidence gap requiring rpi-research | None identified beyond known external prerequisites | P02 requires legitimate access, not speculative research |
| Non-blocking residual work relative to P01/P03 | RV-001 and RV-002 | Authorised owner/profile and workbench user |

* Execution status: Complete.
* Outcome: Residual work.
* Validation coverage: Current unit, migration, exact-head CI, live PNG,
  discovery, read-only failure, health/authentication, browser redirect and
  reference checks; real Graph mutation/user acceptance unavailable.
* Blockers: P02 authority/session prerequisites. Manual mode remains recorded;
  automatic-mode confirmation was not available.

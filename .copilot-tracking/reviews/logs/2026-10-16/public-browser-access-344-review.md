---
title: Public browser access review
description: One postimplementation assessment of issue 344 and remaining acceptance gates
ms.date: 2026-10-16
---

## Scope and Evidence

* Task ID: 344; slug: public-browser-access-344.
* Review date: 2026-10-16.
* Scope: Full supplied implementation, deployment, parity audit and acceptance
  boundary; publication is subsequent parent-owned work.
* Plan: .copilot-tracking/plans/2026-10-16/public-browser-access-344-plan.md
* Details: .copilot-tracking/details/2026-10-16/public-browser-access-344-phase-details.md
* Critique: .copilot-tracking/plans/2026-10-16/public-browser-access-344-critique.md
* Changes: .copilot-tracking/changes/2026-10-16/public-browser-access-344-changes.md
* Research: .copilot-tracking/research/2026-10-16/public-browser-access-344-research.md
* Evidence: docs/architecture/cutover-evidence-pack.md,
  docs/architecture/cutover-azure-evidence.json,
  docs/architecture/mvp-to-src-parity-matrix.md and executable diff/tests.

## Opening Review State

* Goal: Distinguish implemented public transport and safe auth configuration
  from unmet real-user and complete deployed MVP acceptance.
* Evidence readiness: One reconciled task set; P01/P02 executed, P03 Review
  and publication pending. Required public curl, private readback, serving-image
  asset manifest and filed gaps exist.
* Acceptance basis: Supplied #344 criteria, owner networking/private SQL
  constraints and PC-001 through PC-004.
* First comparison: Additive edge/auth/callback changes against exact public
  statuses and the complete feature matrix; local contracts are not live login.
* Authority: Evidence-only, writing this one review record. No implementation,
  plan, details, changes, research, tenant or deployment mutation in Review.
* Initial blockers: #349 tenant prerequisites; #350 browser API 302 and full
  feature/data/configuration/positive-role acceptance.

## Execution Status

* Execution status: Complete.
* Execution evidence: One inline postimplementation comparison of the complete
  supplied boundary. No additional reviewer, live positive-user verification,
  repeated critique or repeat Review is asserted.
* Exactly one postimplementation Review; no repeated critique or correction
  loop is authorized by this record.

## Plan-to-Change Reconciliation

| Scope | Changes and evidence | Reconciliation | Boundary |
| --- | --- | --- | --- |
| P01-T01 | Existing-stack entry point, runtime private/auth-enabled origin guard, unchanged main production guard; GET health probe and explicit route | Reconciled | Actual deployment stays synthetic-development, not production acceptance |
| P01-T02 | Edge HTTPS callback option preserves registration fields; Custom proxy used in main and existing-stack helper | Reconciled | No credential/registration/staff invented; native and browser API semantics differ |
| P01-T03 | 123 infra tests; API 549/110 skips; auth loopback, Ruff/mypy/Bicep | Reconciled | Local positives are not platform sign-in |
| P02-T01 | Incremental edge, scoped async approval, private SQL readback and exact resource record | Reconciled | One owned empty trial rule set removed; zero pre-existing deletion |
| P02-T02 | Public health/welcome 200, native API 401, browser Entra redirect and canonical hostile-header callbacks | Reconciled with Blocked acceptance | Browser API 302 and actual login remain unmet |
| P02-T03 | 16 historical assets, 17 matching image assets, 26 capabilities, #349/#350 | Reconciled | Presence/denial do not imply rendered or positive-role functionality |
| P03 | This Review and subsequent commit/push/PR | Review executed | Publication remains parent-owned, not a deployment or owner acceptance gate |

## Completed Work Assessment

The executable changes are bounded to infra. The src serving image is unchanged;
only its guide changes. The new wrapper references existing resources and
deploys only guard/auth/edge modules. It never applies the broad data-public
switch. Main still rejects production public-data relaxations. The edge has
one fixed API origin, matching Host/TLS, HTTPS all-path route, WAF Prevention,
no rewrite or cache configuration, and a GET health probe.

Default browser action is RedirectToLoginPage; bearer-only remains explicit
opt-in. Existing provider validation, exclusions, credentials and token store
are retained. Main and existing-stack auth use Custom X-Forwarded-Host/Proto.
Initializer tests reject unsafe URLs and incorrect/Standard proxy settings,
retain origin callbacks/roles/credentials, and verify idempotence.

Public native requests prove exact health/welcome 200 and API 401, not
authenticated operation. A browser request reaches Entra with the public
callback. Forged principal/malformed bearer are denied, conflicting Host is
421, and forwarding attacks retain the canonical HTTPS callback after
configuration propagation. Only the API has ingress; no alternate edge origin
or host-rewrite path was added.

The asset job observes package hashes without opening a data store; its second
execution observes only anonymous private HTTP status/redirect host. The
continuing feature audit does not silently equate either observation with
functionality. Missing registrations/staff, representative workload, models,
map/photo/law configuration and positive workflows are explicitly filed.

## Implementation-Time Plan and Detail Update Assessment

| Area | Update and trigger | Reconciliation and user intent | Assessment |
| --- | --- | --- | --- |
| P01 runtime guards | Two tiny helper modules required for existing runtime references and auth preservation | Recorded in changes/details; same one additive entry point and no new test files | Justified, no architecture/safety expansion |
| P02 inventory provenance | Exact-image manual job supplies hashes where auth interception cannot prove presence | Same ama environment/image/identity; no Store/private data; exact new job recorded | PC-004 correction supported |
| P02 private diagnostics | Reuse owned job for four anonymous private HTTP observations | Separates origin health from delayed public edge; no protected reads | Bounded execution amendment |
| P02 forwarding | Standard accepted supplied RFC Forwarded; reserved-header deletion was rejected | Custom proxy corrected in both entry points; initializer and tests match; repeated public probes canonical | Direct PC-001 correction preserves approved intent |
| P02 trial cleanup | Rejected rule attempt left one empty unassociated owned rule set | Exact resource/deletion recorded before removal; final list empty | User permits deletion of resources created by this task; no pre-existing deletion |
| P02 browser API behavior | Native 401 but browser User-Agent 302 | Filed #350; no exemption without platform-principal proof | PC-002 branch remains Blocked, not silently accepted |

No new architecture decision, policy bypass or tenant mutation was introduced.
The one final-candidate critique was not repeated. Later changes implement its
compatible isolation/provenance corrections rather than reopen owner choices.
The captured implementation hash snapshot predates the final comment-only edge
proof annotation; it is a historical observation, not a hash of the eventual
documentation commit.

## Critique and Material Revision Assessment

* PC-001: Sole fixed origin/Host/TLS and route/domain assertions, hostile Host
  421, corrected Custom proxy and repeated canonical callback probes present.
* PC-002: No API exemption was enabled. Native denial and local positive/
  negative principal contracts exist; live positive principal and browser API
  coexistence remain explicitly Blocked and routed.
* PC-003: Return401/NoProxy baseline and bounded endpoint-disable/auth-restore
  recovery documented. Final native transport/denial/isolation gates passed;
  no destructive recovery or intentional failure injection was required.
* PC-004: Historical filenames come from the supplied matrix, current package
  hashes from the serving digest, with separate public-intercept/rendered cells.
* Dependent unsafe work was not enabled to satisfy missing positive proof.
  Real-user/operational approval is not inferred from local tests or redirects.

## Plan Follow-Up Assessment

| Follow-up | Outside completed execution because | Owner or next action | Route |
| --- | --- | --- | --- |
| Tenant registration/credential/callback/staff | No valid retained workbench app or supplied tenant authority/credential | Authorized tenant operator and staff owner, #349 | Distinct prerequisite follow-up |
| Browser API 401 | Anonymous browser request is intercepted with 302; exemption needs positive platform trust proof | After #349, bounded auth implementation with live positive/negative checks, #350 | Later rpi-implement |
| Full positive-user feature parity | Present package assets cannot prove role/data/model/financial/safety workflows | Authorized operator plus named human owners, #350 and specialist issues | Later rpi-research to establish executable evidence/configuration boundaries |

These remain distinct later work, not new active plan tasks or satisfied
acceptance cells.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Real-user browser access remains unavailable

* Scope: #344 public workbench/sign-in acceptance, P02-T02.
* Evidence: public_browser_344 configuration has invalid_client_uuid equivalent
  `valid_client_uuid=false`, browser credential absent and no staff binding.
  Browser redirect is observed but no real callback/session exists.
* Impact: A person cannot yet use the restored public workbench.
* Destination: Distinct prerequisite follow-up #349, authorized tenant/staff
  owner; not an invented registration or new active implementation task.
* Next action: Provide intended app and private credential, reconcile callback/
  staff and perform actual-user sign-in under tenant authority.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Browser API requests still redirect instead of returning 401

* Scope: API/browser coexistence, P01-T02/P02-T02.
* Evidence: public_browser_344.public_curl additional browser API probe is 302;
  the same native anonymous API probe is 401.
* Impact: Browser fetch/session-expiry cannot be called MVP-compatible or a
  proven API 401 contract. JSON Accept alone does not alter platform behavior.
* Destination: Later rpi-implement, #350, after trustworthy positive platform
  principal evidence is available; do not exempt API paths based on denial alone.
* Next action: Establish live principal preservation/stripping, then implement
  and verify the smallest safe browser/API contract.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Complete deployed feature acceptance has no positive-user proof

* Scope: P02-T03 and every protected feature in the dated matrix.
* Evidence: 26 capability rows Blocked where positive-user operation is needed;
  only one fictional proof case, no deployed model/API AI settings, empty
  production tiles, disabled photo token store and absent law-store settings.
* Impact: Serving assets and anonymous denial cannot establish MVP feature
  parity, role projection, workflow persistence or operational controls.
* Destination: Later rpi-research evidence/configuration scope under #350 and
  existing specialist issues, dependent on #349; implementation follows each
  established gap rather than a blind full acceptance run.
* Next action: Define approved representative synthetic fixture and authorized
  role sessions, resolve explicit configuration gaps and execute each matrix row.

## Defects and Routed Findings

No additional executable defect was identified in the bounded additive-edge,
callback-validation or forwarding implementation. RV-002 is the known
unfinished behavior contract, not a reason to weaken authentication.

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct follow-up #349 | Authorized tenant/staff owner | External prerequisite, not source-only authority |
| RV-002 | Later rpi-implement, #350 | Auth implementer after positive platform proof | Required browser API behavior unmet |
| RV-003 | Later rpi-research, #350 | Deployment/evidence operator and named human owners | Material positive feature/configuration evidence missing |

Later implementation owns routed work; this task does not return to Implement
or repeat Review.

## Residual Work and Blockers

* #349 and #350 are release/acceptance blockers, not completed approvals.
* Parent publication remains: commit, push and PR with Refs, no merge or issue
  checkboxes. Routine publication metadata may be updated without claiming a
  second Review or closure of these findings.
* Named human legal interpretation/rule activation, resident consent, safety,
  financial commitments and real-source/owner approval remain intact.
  Juan Manuel Servera is the exercise Legal/Compliance/DPO owner only;
  ADR 0005 synthetic-development acceptance is not operational reliance.

## Validation Evidence

| Command or observation | Scope | Status | Result |
| --- | --- | --- | --- |
| REQUIRE_AZ_BICEP=1 session-venv/python -m unittest discover -s infra/tests -q | Infra | Passed | 123 tests |
| Absolute core/agents test PYTHONPATH, python -m unittest discover -s tests -q from src/api | API | Passed | 549 tests, 110 opt-in skips |
| Auth-specific loopback suite | Server trust contracts | Passed | 31 tests, not live Entra |
| API Ruff/format/mypy; changed initializer mypy; compiled-test Ruff/format | Static checks | Passed | No claimed full infra test-fixture mypy |
| Bicep build/lint | Main, wrapper and modules | Passed | Exact Custom and NoProxy compiled contracts checked |
| Cut-over parser suite | Matrix parser | Passed | Nine tests |
| Public VM curl at 17:01 UTC | Health, welcome, native denial, browser redirect, hostile headers | Passed for stated boundary | 200 / 401 / 302 / Host 421; canonical callback |
| Browser User-Agent API request | Browser API contract | Failed acceptance | 302, filed #350 |
| Serving-image job | Asset presence | Passed | 17 matching hashes, not functionality |
| SQL/env metadata | Private networking | Passed | SQL Ready/Disabled/Approved; env internal/Disabled |
| Real-user login and full matrix workflows | Tenant and functional acceptance | Blocked | #349/#350, no human approval fabricated |
| Older initializer test-fixture optional mypy | Existing heterogeneous fixture types | Failed, pre-existing | Disclosed; production initializer passes |

## Outcome

* Outcome: Not accepted for full #344 acceptance.
* Rationale: Safe public transport, default browser redirect and native API
  denial are proven, but real-user sign-in, browser API 401 and positive-user
  feature parity remain material open requirements. This is not a conformant
  full cut-over or production acceptance claim.

## Closeout Routing Record

| Finding class | Destination | Owner or action |
| --- | --- | --- |
| Implementation behavior gap | Later rpi-implement | RV-002 / #350 after platform-principal proof |
| Decision gap or invalid assumption | None | Owner edge choice and synthetic-only approval preserved |
| Material evidence gap | Later rpi-research | RV-003 / #350 |
| External prerequisite follow-up | Distinct #349 | RV-001, authorized tenant/staff owner |
| Publication | Parent action | Commit/push/PR; no merge, no issue ticks |

* Review execution: Complete.
* Outcome: Not accepted for full task acceptance.
* Current blockers: RV-001, RV-002, RV-003.

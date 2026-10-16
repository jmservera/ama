---
title: "Demo direct ingress post-implementation review"
description: "Single offline RPI Review for issue-360/demo-direct-ingress."
ms.date: 2026-10-16
---

## Scope and Evidence

* Task ID: issue-360/demo-direct-ingress.
* Review date: 2026-10-16.
* Scope: complete implementation diff against origin/main, changed infrastructure code/tests/documentation and supplied tracking artifacts.
* Plan: .copilot-tracking/plans/2026-10-16/demo-direct-ingress-plan.md.
* Details: .copilot-tracking/details/2026-10-16/demo-direct-ingress-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-16/demo-direct-ingress-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-16/demo-direct-ingress-changes.md.
* Research: .copilot-tracking/research/2026-10-16/demo-direct-ingress-research.md.
* Baseline: origin/main and HEAD both e7e69b8bc13d31de1c0c70821c3ed1c03f1e3cdf, branch feat/demo-direct-ingress. Reviewed 16 modified tracked files and the supplied untracked artifact set. Implementation changes were already present at intake; no branch switch, commit, push or PR mutation was performed.
* Additional evidence: .copilot-tracking/rpi-sessions/2026-10-16/demo-direct-ingress-state.json; required original/addendum/index/memory context; bounded src API authentication/router and core projection code to establish actual role semantics; existing deployment image helper to check migration compatibility; parent validation receipt; public Microsoft naming reference.
* History and lifecycle: main integration and PR 359 intake status are supplied research/user evidence. HEAD equals origin/main locally. device_login is outside the diff and deliberately unchanged; this review does not duplicate PR 359 or claim its merge. Historical 15e8158 comparison is assessed as cited research, not as new live evidence; no legacy working-tree files were read.

## Opening Review State

* Goal: assess high-confidence functional defects, acceptance fidelity and migration risks once, without implementation changes or live-readiness claims.
* Evidence readiness: supplied artifact set exists; implementation and parent validation are reported complete. P04 still records review/publication delivery, not missing implementation.
* Acceptance basis: offline a/b/f and proposed c only; PC-001 consumer staging, PC-002 strict probes and PC-003 inherited authentication corrections; production/default/private dependencies and existing optional Front Door/bearer behavior unchanged.
* First comparison boundary: current plan/details/critique/changes/research against all changed source, tests and documentation relative to origin/main.
* Read-only boundaries: only this canonical record may be written. No Azure calls, deployments, what-if, private data, MVP/prototype working-tree reads, source fixes or second review.
* Initial blockers: none. Live c approval and d/e remain separate unmet gates.

## Execution Status

* Execution status: Complete.
* Review execution evidence: exactly one post-implementation Review assessed the complete offline boundary on 2026-10-16, read changed source/tests beyond string assertions, and recorded the full finding set here.
* This is the task's one Review, not a second critique, implementation pass or live certification. Only this canonical record was written by the reviewer.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01 / P01-T01 | P01 infrastructure; Integrated validation | Reconciled | Separate external generation, private dependencies and staging implemented; job naming has RV-001. |
| P02 / P02-T01 | P02 auth/probes; Integrated validation | Reconciled | Direct discovery/auth and strict probes implemented; role-denial contract has RV-002. |
| P03 / P03-T01 | P03 documentation | Reconciled | Proposal, parity/drain/rollback, acceptance audit, historical separation and cost/retirement gates present; affected names/probe wording must follow the routed fixes. |
| P04 / P04-T01 | Validation; Integrated validation; Remaining Work; plan Handoff | Reconciled | Offline checks complete by supplied receipts. Unchecked review/publication checklist is delivery bookkeeping, not missing implementation or unrun validation. This report supplies the Review; parent owns commit/push/PR delivery. |
| Follow-Up Items | Remaining Work; plan Follow-Up Items; evidence audit c/d/e | Reconciled | Migration/cost approval, tenant/browser/SQL/AI proof and retirement deliberately remain distinct live work. No issue checkbox or readiness claim is authorized. |

The changes record's early "Implementation active" and lane-validation-pending
paragraphs are superseded by its completed P01/P02 and integrated-validation
sections and final Remaining Work, consistent with the user's intake. They do
not prevent a credible review. Session-state `review: null` is pending parent
bookkeeping, not a missing implementation requirement; it was not edited.

## Completed Work Assessment

| Marker / acceptance | Files and semantic evidence | Validation / assessment |
| --- | --- | --- |
| P01; a, default/production compatibility | infra/main.bicep; infra/modules/guard.bicep | demoDirectIngress defaults false; existing application/background defaults retained. New guard checks reject production, edge, public backing and missing browser audience/bearer demo combinations; environment-only staging remains possible. Existing guards are retained. Compiled test matrix evaluates actual guard expressions, including bypass mutations. |
| P01; a, private dependencies | infra/main.bicep; infra/tests/test_bicep_policy.py | Only applicationPrefix changes; identity, SQL, registry, storage, vault, Foundry, monitoring and IoT naming inputs remain on the original prefix. publicAccess is still independently derived; SQL is always private. Tests evaluate private publicNetworkAccess, stable names and reused identity inputs rather than merely locating strings. No new shared-service definition, RBAC grant or data path was added. Main still reconciles all services, so the documented no-unrelated-delta what-if gate remains essential for later authorized deployment. |
| P01; a, own network | infra/modules/network.bicep; infra/modules/containerapps.bicep | Conditional dedicated snet-aca-demo/NSG, delegated Microsoft.App/environments and distinct external environment; old subnet definitions/NSG and service private DNS/links retained. Explicit Internet allow is TCP 443; no Internet 80/arbitrary-port rule. Default Azure/VNet NSG rules are not misrepresented as a novel deny-all firewall. Demo uses the new subnet and omits internal environment DNS. Public access affects the demo environment, not backing services. Subnet vacancy, routing and platform support are not established offline. |
| P01; a/c, workload names and staging | infra/modules/containerapps.bicep; infra/main.bicep; infra/tests/test_bicep_policy.py; infra/tests/test_edge_module.py | Environment/API/agents/jobs have a distinct demo prefix and existing user-assigned identities. False background switch omits agents and all four jobs, with ledger alerts gated consistently; it does not stop existing resources. Truth-table and mutation tests cover real compiled conditions. Names are distinct but several jobs are invalid: RV-001. Existing edge text test is supplemented, not substituted for compiled behavior tests. |
| P02; b, direct discovery | infra/scripts/setup-entra.py; infra/tests/test_setup_entra.py | Explicit flag or unique tagged API branches before cdn/afd discovery; ambiguous direct candidates fail, exact selection remains available. API subscription/RG, external ingress, selected environment and exact public origin checks are present. Tests execute fake CLI/REST interactions and fail on any afd/cdn command, including repeat/check runs. Extension diagnostics name only required isolated installation. Optional edge discovery remains in its branch. No live CLI call was made here. |
| P02; b, auth compatibility | infra/scripts/setup-entra.py; infra/tests/test_setup_entra.py | Direct auth forces NoProxy. Inherited Return401 requires explicit browser enablement or explicit service mode; missing browser credential remains actionable. Shared registration/roster/assignment-required/secret lifecycle is retained. Tests exercise stale Custom/Standard, callback retention, repeat-run idempotence, secret failure and existing bearer/edge behavior. Pure in-memory review assertions also preserved legacy Custom/Return401 and verified explicit direct browser conversion. This does not prove actual tenant credential readiness. |
| P02; probe tooling, not d acceptance | infra/scripts/private-cutover-proof.py; infra/tests/test_private_cutover_proof.py | Private DNS remains default; direct bypasses only that check. HTTPS origin constraints, exact content/denial statuses, separate browser JSON profile, malformed bearer/forged-principal negatives, disabled automatic redirects and bounded same-origin auth hops precede exact HTTPS Microsoft-host validation. Sanitized outputs do not print session values, response bodies or redirect queries; missing role session is Not run. Fake HTTP tests actually traverse the request/redirect handler, but wrong-role semantics are not established: RV-002. |
| P03; f and proposed c | infra/README.md; docs/adrs/0001-azure-architecture.md; docs/architecture/README.md; docs/architecture/cutover-evidence-pack.md; docs/reference/README.md; docs/reference/log.md | All documentation changes assessed. Proposal requires retained prefix/private parameters, whole-stack delta review, exact digests/config/auth/identity/DNS parity, API-only fresh staging, queue/schedule/import drain, single generation, reverse rollback and separately gated selective retirement. Shared services/VNet/ama and endpoints must remain. Historical edge observations and MVP git prior art are explicitly not replacement acceptance. KB index and append-only log updated; memory/original untouched. Cost arithmetic separates empty environment, replicas/jobs/logs/network, retained edge and management-feature costs; rates are explicitly illustrative, not a quote. Two routed fixes require matching runbook updates. |

## Implementation-Time Plan and Detail Update Assessment

| Affected markers | What changed and why | Triggering evidence and decision | Reconciliation / planning state | Assessment |
| --- | --- | --- | --- | --- |
| P01/P02/P03 partition | Infrastructure, auth/probe and documentation responsibilities separated for write-disjoint delivery | Changes Execution; user retained offline scope | Current plan/details and lane summaries agree; critique references to earlier task labels map to current markers by described scope | Organizational refinement only; no material architecture/scope divergence or new critique needed. |
| P01/P03; PC-001 | Added compiled background omission and complete consumer/drain inventory | Prior critique identified KEDA and in-flight work hazards | Current details and runbook cover agents, orchestrator, imports, token maintenance, ledger and producers; source gates all consumers | Accepted direction preserved; omission semantics and rollback limitations explicit. Job name validity still needs RV-001, not a new plan assumption. |
| P02; PC-002/PC-003 | Explicit public smoke contract and inherited-auth mode correction | Prior critique and existing browser API 302 / Return401 state | Current plan/details, implementation and tests align on mode boundaries; default bearer behavior not globally converted | Compatible corrections applied; role-denial implementation is defective despite contract/test claims (RV-002). Known browser API gap is not counted as introduced. |
| P04 | Installed missing source dependencies; corrected API test working directory | Recorded missing packages and six root-relative import errors | Final API receipt supersedes initial failure; no runtime source changed to hide failure. Baseline Ruff/type diagnostics explicitly retained | Validation invocation correction, not acceptance expansion or material replanning. |

## Critique and Material Revision Assessment

* Exactly one prior critique is supplied, with PC-001 High and PC-002/PC-003 Medium all marked Applied in the finalized plan.
* PC-001: compatible consumer-staging correction is implemented and semantically covered by compiled-condition truth tables and mutation tests. Fresh-generation/omission, drain and rollback caveats remain explicit; RV-001 blocks safe job activation independently of staging logic.
* PC-002: direct/public mode, unchanged private-DNS default, strict status/redirect matrix, hostile redirects and Not run handling are present. The real endpoint role contract was not reconciled: RV-002. Fake status fixtures alone cannot close that part.
* PC-003: direct NoProxy, explicit Return401 browser transition, secret prerequisite and default bearer preservation are implemented. Existing edge Custom forwarding/callback cases remain covered.
* Material decision gaps: none found. No new system-wide change, runtime authorization change or accepted-scope expansion is justified or requested by this Review.
* Dependent-work assessment: corrections are reflected in the current plan/details before the completed implementation evidence. No evidence of affected work proceeding under an unresolved divergent decision. Review does not independently timestamp each edit or infer live approval.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| FU-360-MIGRATION: c approval and actual cost | User authorized a proposal, not migration, spend or live delta review | Owner approves exact runbook, quoted rates, overlap and rollback window; coordinator later verifies whole-stack delta/capability/quota/subnet | Open, distinct owner/coordinator follow-up. Do not add to active offline implementation or count as a defect. |
| FU-360-LIVE: d tenant/browser/roles/SQL/AI | Real identities, deployed transport and private persistence/model evidence require separate authority | Coordinator after approval executes real sign-in/callback/session/account-switch, role/unknown-staff denial, SQL restart persistence and bounded AI proof; retain #349/#350 constraints | Open, distinct live acceptance work. Browser JSON API 302 is failure, not an accepted 401 or reason to weaken probes. RV-002 only fixes offline tooling. |
| FU-360-RETIREMENT: e | Destructive action depends on d, rollback-window completion and a second explicit approval | Owner authorizes exact dedicated edge/old-workload scope; coordinator drains, checks dependencies and carries separately reviewed IaC retirement delta | Open, distinct follow-up. Shared private services/identities/VNet/ama are never retirement targets here. |

These are the plan's unresolved Follow-Up Items, mirrored in the changes record
and evidence audit. They are neither missing P01-P03 implementation nor new
active scope. Offline completion cannot close them.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Demo job names exceed the Container Apps naming limit

* Related scope: P01-T01, P03-T01; criterion a and migration c.
* Evidence: infra/main.bicep:123 adds `-demo` to the entire workload prefix consumed by infra/modules/containerapps.bicep:234,327,368 job names. The default demo generates `job-forward-dev-demo-orchestrator` and `job-forward-dev-demo-auth-renewal` (33 characters), and `job-forward-dev-demo-ledger-verify` (34). The documented cutover-test generation produces 34, 34 and 35 characters respectively. The Microsoft CLI reference for `az containerapp job --name`, retrieved 2026-10-16, requires names to be less than 32 characters: https://learn.microsoft.com/en-us/cli/azure/containerapp/job?view=azure-cli-latest. The versioned 2025-07-01 ARM reference exposes only a broad name pattern, explaining why compilation does not catch this: https://learn.microsoft.com/en-us/azure/templates/microsoft.app/2025-07-01/jobs.
* Impact: default demo deployment, or activation after API-only staging, cannot create these jobs. The documented sequence stops the old background generation before new activation, so an otherwise approved cutover can lose background service when the invalid names are rejected. API-only staging does not expose this failure.
* Test evidence: infra/tests/test_bicep_policy.py explicitly expects the overlong default names but does not validate platform length constraints. Offline name arithmetic reproduced all lengths; no deployment was attempted.
* Destination: later rpi-implement.
* Smallest useful next action: choose deterministic shorter demo-only job names, preserve all non-demo names and shared dependencies, update alerts/outputs/runbook consumers, and add compiled name-validity tests for default and documented prefixes plus supported input bounds.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Wrong-role probe expects 403 on an endpoint allowed to every mapped role

* Related scope: P02-T01, P03-T01; PC-002 and criterion d tooling.
* Evidence: infra/scripts/private-cutover-proof.py:314-315 appends a `wrong_role_denial` check against `/api/me` expecting 403; infra/README.md:539-542 explicitly documents that endpoint. src/api/src/zava_forward/api/server.py:236-243 returns 401 when the trusted provider rejects a principal, then applies projection authorization; server.py:297-304 returns the current-user payload. src/core/src/zava_forward/core/projection.py:34-38,59-63 permits `me` for all seven staff roles and Contractor. src/api/src/zava_forward/api/auth.py:137-155 rejects unmapped/multiple roles and unknown staff before the endpoint. In-memory execution of the actual provider and projection role gate reproduced `/api/me` 200 for every default mapped role and 401 for an unmapped role; Contractor `/api/stats` correctly gates to 403.
* Impact: a legitimate authenticated lower-privilege session fails this proposed acceptance probe with 200, while an unknown/unmapped principal yields 401. A 403 from an unrelated upstream restriction could be mislabelled role evidence. Live acceptance remains unmet regardless.
* Test evidence: infra/tests/test_private_cutover_proof.py fake HTTP server returns a configured 403 solely when a supplied cookie/token matches the fixture. It proves status comparison and non-leakage, not the application's role-denial semantics.
* Destination: later rpi-implement.
* Smallest useful next action: use a fixed safe endpoint genuinely denied to an explicitly described role, separately verify the supplied session is authenticated (for example `/api/me` 200 without logging its body), keep unknown-staff checks distinct, and add a regression against the real provider/router authorization semantics. Do not weaken runtime authorization or claim synthetic sessions are tenant proof.

## Defects

* RV-001 High: overlong demo jobs; later rpi-implement.
* RV-002 Medium: wrong-role probe endpoint/status mismatch; later rpi-implement.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low implementation defects. No additional decision or material research gap was identified.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Later rpi-implement | Parent routes demo-only valid job names and compiled bounds/consumer regressions | Defect within the accepted architecture; shared naming/default behavior must remain unchanged. |
| RV-002 | Later rpi-implement | Parent routes endpoint/session contract correction plus real application authorization regression and matching documentation | Defect in new offline tooling, not a request to alter API authorization or run real-user acceptance. |

Later implementation of these findings does not require another Review.

## Residual Work

* FU-360-MIGRATION, FU-360-LIVE and FU-360-RETIREMENT remain distinct owner/coordinator work as above. No acceptance, deletion, budget or tenant authority is inferred from this review.
* P04 review recording is supplied here. Parent owns status reconciliation and requested privacy-safe commit, non-forced push and PR delivery. Those delivery items were explicitly excluded from implementation-gap findings.
* No source fixes, plan changes or additional artifact edits were made. Do not mark the entire issue accepted while c/d/e remain unmet.

## Blockers and Remaining Work

* Review blockers: none; execution Complete.
* Offline outcome blocker: RV-001 prevents accepting the job-capable implementation; RV-002 remains a probe correctness defect.
* Implementation was complete enough to review. The routed corrective work is not a retroactive claim that the P04 validation commands were never executed.
* Live blockers/gates: owner migration/cost approval, authorized tenant/network/browser/role/persistence/AI evidence, known browser API behavior and separate retirement approval. These are not blockers to completing the offline Review.

## Validation Evidence

| Command / check | Scope | Status | Evidence and limitation |
| --- | --- | --- | --- |
| Parent: REQUIRE_AZ_BICEP=1 infra unittest discovery | All infrastructure tests, including compiled matrices | Passed (supplied) | 234 tests; no skips. Reviewed semantic assertions and mutation checks. Not independently rerun; compilation/unit success does not establish live resource naming acceptance or real role semantics. |
| Parent: all infra/*.bicep and infra/modules/*.bicep build/lint | Every root/module Bicep template | Passed (supplied) | Local compiler only. This reviewer ran no az command. Broad ARM name schema does not catch RV-001. |
| Parent: Bicep-policy Ruff/format; setup mypy --check-untyped-defs; probe Ruff | Scoped changed checks | Passed (supplied) | No whole-repository lint/type cleanliness inferred. |
| Parent: setup/probe focused suites | Fake CLI/auth and HTTP/session contracts | Passed (supplied) | 54 setup / 18 probe tests. Fake wrong-role response is not semantic acceptance; see RV-002. |
| Parent: broader setup Ruff / probe mypy | Broader existing diagnostics | Failed baseline retained (supplied) | Setup 159 Ruff diagnostics; probe 3 mypy diagnostics; reported zero introduced. Baseline cleanup is outside scope. |
| Parent: API unittest discovery from src/api with absolute test paths | Full API | Passed (supplied) | 563 tests, 110 explicit conditional skips. Initial root invocation had six import errors, corrected without source changes. No live SQL/AI/browser proof. |
| Parent: CLI help, local auth HTTP fixtures, documentation links/anchors and diff checks | Offline executable/documentation behavior | Passed (supplied) | Responsive loopback synthetic fixtures; not Azure or real-user acceptance. |
| Reviewer: PYTHONDONTWRITEBYTECODE=1 python3 in-memory unittest loader | Six file-free existing probe tests | Passed (observed) | 6 tests, 5.761 seconds. Strict status/Not run, hostile redirects, bounded local auth hops, safe argument failure and --help. Actual loopback HTTP handler ran; no fixture files or external requests. Remaining session-file/full suites rely on parent evidence to avoid private input or additional filesystem artifacts. |
| Reviewer: actual auth provider plus AST-selected actual projection role-gate execution | Role contract, all default mapped roles and one unmapped synthetic role | Passed reproduction (observed) | Every mapped role authorizes `me` (handler gives 200); unmapped principal returns no user (handler gives 401); Contractor `stats` gate denies (403). Confirms RV-002 without changing runtime code or reading data. |
| Reviewer: actual auth_patch pure in-memory assertions | Legacy versus explicit direct auth behavior | Passed (observed) | Legacy Custom forwarding/Return401 preserved; direct explicit browser conversion yields NoProxy/RedirectToLoginPage and existing secret reference. |
| Reviewer: deterministic name-length calculation and public Microsoft reference | Default and documented demo job names | Defect reproduced (observed) | 33-35 characters versus documented limit below 32. Public reference retrieval only, no Azure service/control-plane/data-plane request. |
| Reviewer: git diff --check; HEAD/origin/main identity; full diff/source inspection | Entire supplied change boundary | Passed (observed) | No whitespace errors; HEAD equals origin/main; only canonical report written by reviewer. |
| Deploy, what-if, Azure readback, live tenant/browser/roles/SQL/AI, retirement | c/d/e live scope | Skipped, prohibited/outside scope | Not run. No live readiness or current deployed resource state claimed. |

## Outcome

* Outcome: Not accepted.
* Outcome rationale: Review execution is Complete, but a High naming defect blocks job deployment/activation and a Medium probe defect misstates application authorization semantics. These prevent accepting the completed offline implementation as conformant until later correction. They do not expand this task to live c/d/e.
* Otherwise, default/production/private dependencies, distinct environment/subnet and workload identity reuse, guards, direct no-afd/cdn branch, retained edge/bearer behavior, strict transport/redirect checks, sanitized probe output, migration parity/drain/rollback and gated retirement/cost documentation are supported within the explicitly offline evidence boundary.
* No Azure capability certification, real tenant authority, successful sign-in, SQL persistence, AI outcome, migration approval or retirement acceptance is claimed.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | Later rpi-implement | Parent routes RV-001 and RV-002, preserving accepted scope; no second Review required. |
| Decision gap or invalid assumption | None | No material accepted-direction change identified. |
| Material evidence gap | None for completing this offline Review | Actual platform/tenant/live proof belongs to distinct live gates, not new offline research scope. |
| Non-blocking residual work | FU-360-MIGRATION; FU-360-LIVE; FU-360-RETIREMENT | Owner/coordinator obtains approvals, executes authorized proof, and separately approves selective retirement. |
| Delivery bookkeeping | Active parent P04 | Record this Review, reconcile statuses and perform requested commit/push/PR delivery without claiming issue acceptance. |

* Review execution: Complete.
* Outcome: Not accepted.
* Validation coverage: complete supplied offline receipts plus direct semantic reproductions and six targeted probe tests; no live checks.
* Review blockers: none. Corrective implementation: RV-001 High and RV-002 Medium.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/research/2026-10-16/demo-direct-ingress-research.md | Supplied evidence and history/integration boundary |
| .copilot-tracking/plans/2026-10-16/demo-direct-ingress-plan.md | Current accepted offline scope, markers and follow-ups |
| .copilot-tracking/details/2026-10-16/demo-direct-ingress-phase-details.md | Current implementation and critique corrections |
| .copilot-tracking/reviews/plans/2026-10-16/demo-direct-ingress-plan-critique.md | Single critique and PC-001 through PC-003 |
| .copilot-tracking/changes/2026-10-16/demo-direct-ingress-changes.md | Completion, validation and remaining delivery evidence |
| .copilot-tracking/reviews/logs/2026-10-16/demo-direct-ingress-review.md | This single canonical Review and complete RV finding set |
| .copilot-tracking/rpi-sessions/2026-10-16/demo-direct-ingress-state.json | Read-only parent continuation state |

## Next Steps

Return this one Review result to the active parent. Route RV-001 and RV-002 to
a later rpi-implement invocation; do not perform source fixes or another Review
inside this invocation. Parent owns P04 bookkeeping and PR delivery. Keep live
approval/proof/retirement follow-ups separate and unmet.

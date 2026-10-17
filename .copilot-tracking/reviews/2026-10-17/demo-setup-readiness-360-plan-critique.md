---
title: Demo setup readiness final-candidate plan critique
description: Single evidence-grounded critique of the issue 360 implementation candidate
ms.date: 2026-10-17
---

## Metadata

* Task ID: issue-360 / demo-setup-readiness-360
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/demo-setup-readiness-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/demo-setup-readiness-360-phase-details.md
* Research: .copilot-tracking/research/2026-10-17/demo-setup-readiness-360-research.md
* Critique execution status: Complete
* Execution count: Exactly one final-candidate assessment; no agents launched.
* Write boundary: This critique artifact only. No implementation, tests, Git
  lifecycle writes or Azure actions were performed.

## Inputs and Criterion Boundary

The supplied plan, details and research were assessed together against the
caller's confirmed full-loop direction and restrictions. Existing ama resources
only; no private datasets, Graph/SharePoint mutation by this executor, role
activation, paid build path, public backing bypass or app-secret fallback are
authorized. The new source-job-only tag permission remains offline. The
encrypted relay must retain authenticated run/operation/digest binding and
require terminal success plus confirmed cleanup. Credential storage uses a
minimal secureString ARM deployment independent of the vault firewall. Issue
358 expiry and secret-preservation behavior remains outside this work.

Same-VNet cross-environment reuse must retain exact subscription/resource-group
and subnet guards. Additive external API migration is conditional on the exact
reviewed what-if and preservation checks; no old resource retirement is allowed.
Existing tests cannot be removed and at most 25 targeted tests may be added.
The critique does not authorize later execution actions.

Evidence considered:

* Supplied research C1-C8/W1-W5, as recorded evidence, not freshly verified
  Azure inventory or independently refreshed external documentation.
* infra/scripts/staff_azure.py, infra/scripts/staff-azure-worker.py and
  infra/scripts/staff_roster.py.
* Relevant setup discovery, Azure adapter, mode selection, credential creation
  and orchestration in infra/scripts/setup-entra.py.
* infra/staff-initializer-rbac.bicep, infra/cutover-proof.Dockerfile and
  relevant API/auth resources in infra/modules/containerapps.bicep.
* infra/tests/test_staff_azure.py and relevant existing credential/setup test
  references in infra/tests/test_setup_entra.py.
* infra/README.md direct-demo migration and in-VNet staff sections;
  docs/architecture/cutover-evidence-pack.md issue 360 criterion audit.
* Existing validation selectors in .github/workflows/src-ci.yml.
* Required repository context in docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md; supplied task state.

Assessment covers requirements, research, tasks, acceptance criteria,
dependencies, decisions, cleanup, privacy, migration and publication gates.
This is a plan credibility assessment, not implementation verification,
penetration testing, live readiness approval or a new research cycle.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C2/W3/W4; P01-T01 encrypted relay | Covered | Existing AES-GCM binding is retained; tag capacity, collision and framing checks, selective Merge/Delete, terminal success and cleanup are explicit requirements |
| P01-T01 same-VNet reuse | Covered | Both environment/subnet IDs must be verified in ama with matching VNet, and temporary execution uses the API environment rather than the source environment |
| C4/W1/W2; P01-T02 secure ARM credential deployment | Partial | Secure body, fixed host, exact Create-only what-if and metadata checks are specified; store selection and early credential reuse can bypass the adapter, PC-001 |
| P01-T03 least privilege and issue 358 boundary | Covered | Source-job-only tag permission and API-only restart scope remain offline; expiry/preservation edits are excluded |
| C7; P02-T02 additive migration | Partial | Exact preserving payload and what-if are required, with redacted-value blocker; staging before auth-child completion lacks a fail-closed exposure rule, PC-002 |
| Image publication and role activation dependencies | Covered | Explicit human blockers, not permission inferred from ambient Owner or a reason to open the registry |
| P02-T01 validation and test budget | Covered | Existing suites, Bicep, lint/type selectors, no removals, at most 25 additions; new modules must be included |
| P02-T03 documentation and criterion a-f audit | Covered | Historical separation, offline/live/Not run/blocked distinction, index/log and actual human actions are required |
| P03-T01 final review and P03-T02 publication | Partial | One review is appropriate, but unconditional routing of material findings to later work lacks a stop or blocked-publication rule, PC-003 |
| Full loop, private data, Graph/SharePoint and retirement restrictions | Covered | Full loop is confirmed; no extra approval request or child loop is warranted, and no current blocker is permission to retire resources |

## Verdict

* Verdict: Revise
* Severity counts: 0 Critical, 2 High, 1 Medium, 0 Low.
* Rationale: The selected transports and authorization boundaries are credible
  for bounded implementation, but three execution contracts need correction.
  Existing credential control flow can violate the Azure-mode storage rule;
  separate API/auth creation needs a fail-closed staging gate; and a material
  final-review failure must prevent an unqualified ready-for-merge handoff.
  These are direct planner corrections, not grounds for reopening settled
  architecture or asking for new permissions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Vault-call replacement does not cover app-store selection and reuse

* Related IDs: C4; P01-T02; P01-T03; Azure-mode Key Vault/no-fallback
  requirement; credential regression acceptance criterion.
* Evidence: infra/scripts/setup-entra.py:1216-1269 returns an existing matched
  credential before reaching vault discovery, and chooses the storage mode
  from explicit selection or the recorded store tag. An app selection can
  bypass both vault preflight and vault write. P01-T03 in the supplied details
  limits wiring to replacing those vault calls and excludes credential
  selection edits. Removing network-failure fallback alone does not cover
  these paths.
* Concern: The candidate states that --run-in-azure uses Key Vault, while its
  specified surgical edit can still accept a recorded or explicitly selected
  app store or reuse an existing app-backed credential without reaching the
  new adapter.
* Impact: The authorized mode's storage guarantee can be violated even when
  all new adapter and network-failure tests pass.
* Smallest useful change: Specify an Azure-mode storage compatibility guard
  before credential reconciliation and directory writes. Reject an explicit
  app-store request or incompatible existing/recorded app-backed state with
  a sanitized blocked result. Do not silently migrate or rotate that
  credential. Preserve valid Key Vault reuse and non-Azure explicit app
  behavior. Implement this as a preflight boundary, not changes to issue 358
  expiry selection or secret rebuilding.
* Action owner: Planning parent, then P01-T02 implementation owner.
* Exact resolving evidence: Revised P01-T02/P01-T03 specify placement and
  behavior for explicit app, recorded app and matched app-backed credential
  cases. Targeted fake-CLI assertions show Azure mode blocks before Graph or
  storage writes in those cases, valid vault-backed reuse is unchanged, both
  vault-failure paths have no fallback, and non-Azure app mode is preserved.
  Include these cases within the existing 25-test ceiling.
* Decision route: Direct planner correction. The caller has already settled
  Azure-mode Key Vault storage and no app-secret fallback; no user decision
  or automatic conversion of existing credentials is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Additive API creation needs an auth-before-exposure staging gate

* Related IDs: P02-T02; exact reviewed migration what-if; authentication and
  preservation requirements; issue 360 criteria c/d.
* Evidence: The details permit creating the demo API and its auth child in the
  existing external environment. infra/modules/containerapps.bicep:102-187
  creates an ingress-enabled API; its authConfigs/current child is a separate
  resource at lines 190-238 and depends on the parent existing. The migration
  runbook requires browser authentication for serving demo workloads.
* Concern: Reviewing an exact two-resource delta and copying auth properties
  do not establish that the API cannot receive public requests before the
  auth child completes, or after that child fails. The candidate gives no
  explicit intermediate-state gate or safe failure disposition. This is a
  missing planned guarantee, not a claim that the proposed new payload has
  already exhibited a live failure.
* Impact: A successful parent creation with pending or failed authentication
  can leave an externally reachable workload that does not meet the stated
  serving prerequisite. Later HTTP denial checks do not protect the interval
  before those checks.
* Smallest useful change: Require fail-closed staging with no unrestricted
  public exposure until the auth child and required runtime authentication
  settings are verified. Define the supported staging mechanism, exact
  expected delta and readback gate; inspect the exact what-if for every
  transition. If a preservation-compatible mechanism cannot be established
  from supported existing resources, record a migration blocker and do not
  apply. On partial failure leave the new path restricted, preserve the old
  path and do not infer permission to delete either one.
* Action owner: Planning parent, then P02-T02 migration executor.
* Exact resolving evidence: Revised P02-T02 includes the staged payload
  contract, allowlisted direct-ingress/auth deltas, auth verification and
  failure disposition. Offline contract tests or payload assertions show
  initial staging is restricted and auth-child failure cannot trigger the
  exposure step. Any later live apply requires the exact reviewed what-if
  and sanitized readbacks; otherwise the receipt records Not run/blocked.
  No new role activation, Graph mutation, backing-network opening or
  destructive rollback is authorized by this correction.
* Decision route: Direct planner correction within the already conditional
  migration authorization. An unsupported safe staging path is an execution
  blocker, not a request to weaken authentication.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The single final review lacks a material-finding publication gate

* Related IDs: P03-T01; P03-T02; full-loop completion and readiness audit.
* Evidence: P03-T01 in the details says material findings route to distinct
  later work, not another implementation/review cycle. P03-T02 then directs
  completion reconciliation, push and PR publication without conditioning
  readiness or phase completion on that review's verdict.
* Concern: The bounded no-loop instruction is reasonable, but it is not an
  acceptance policy for unresolved material defects. The current sequence
  can mark delivery complete and publish an ordinary ready PR even when the
  sole implementation review identifies a failed privacy, cleanup,
  authentication or authorization boundary.
* Impact: Later-work tracking could substitute for a current safety gate,
  obscuring which portions are actually eligible for use or merge.
* Smallest useful change: State that unresolved material review findings block
  readiness and unqualified phase completion. Under the one-review/no-child
  loop constraint, publish only a clearly blocked draft PR when publication
  is still required, with exact findings and follow-up ownership, or stop at
  the documented concrete blocker. Do not perform further live actions based
  on a failed review, and do not turn known deployment blockers into a claim
  of live acceptance.
* Action owner: Planning parent and P03 publication owner.
* Exact resolving evidence: Revised P03-T01/P03-T02 define Pass versus
  material-failure handoff states. The final review, persistent phase state,
  a-f audit and publication receipt agree; any materially failed candidate
  remains explicitly blocked/draft with no readiness claim. No second
  critique or routine second review is introduced.
* Decision route: Direct planner correction. The owner requested a full loop
  and publication, not acceptance of material defects; no user response is
  necessary.

## Strengths and Residual Risk

* The candidate reuses the existing authenticated encryption protocol and
  source initializer rather than adding a service, exposing logs or handing
  an operator token to Azure.
* The tag relay deliberately retains bounded framing, unrelated-tag
  preservation, job ownership checks, terminal success and cleanup gates.
  These are requirements to prove during implementation, not observed
  properties of the unmodified console-based worker.
* ARM credential deployment is supported by supplied W1/W2 rather than an
  assumed firewall bypass. Secure parameters, no secret outputs, exact
  scope and write-only metadata verification remain essential.
* Cross-host serialization is explicitly an operator window, not a claimed
  distributed lock. Hard termination and uncertain cleanup remain recovery
  conditions; do not blindly repeat SQL apply.
* Private image publication, source-job tag/API restart permission activation
  and tenant/browser acceptance are acknowledged unmet dependencies.
  The critique does not ask the executor to resolve them through an
  unauthorized build, role write, Graph action or network change.
* Retaining the deployed API digest is not proof that the new staff worker
  is available. Worker publication and its approved source-image handoff
  remain separate prerequisites, as the candidate already records.
* A 302, a ready environment, passing mocks or metadata existence cannot
  establish real sign-in, role behavior, SQL persistence, AI readiness or
  old-path retirement eligibility.

## Questions or Blocking Evidence Gaps

* No unresolved user choice is needed for the three corrections.
* Safe staged migration payloads and exact live what-if/readbacks are not
  supplied. This is an explicitly conditional implementation gate, not
  grounds to claim live feasibility or request broader authorization.
* New image publication, role activation and real-user acceptance remain
  human-owned blockers. They do not block source implementation or this
  completed critique and do not change the verdict to live readiness.

## Limitations

* Source inspection was read-only and bounded to the supplied trace and
  its directly relevant existing contracts. No agents or external research
  were used; referenced external evidence is accepted only as recorded in
  the supplied research.
* No test suite, Bicep compilation, Azure inventory, what-if, deployment,
  token operation or live HTTP probe was executed during this critique.
* No private datasets, roster, credentials or private configuration exports
  were accessed. Repository fixtures were inspected as offline evidence.
* The complete actionable finding set for this supplied candidate is PC-001
  through PC-003. No additional findings are withheld for another pass.

## Recommended Next Action

* Highest-impact finding: PC-002, fail-closed staging before public exposure.
* Action owner: Planning parent.
* Smallest next action: Revise P02-T02 to gate exposure on verified auth or
  record a blocker; incorporate PC-001 and PC-003 in the same direct revision.
* User response required: No.
* Handoff: Finalize the revised plan with explicit dispositions, then continue
  the already confirmed parent loop under its existing gates. Do not launch
  another final-candidate critique.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/demo-setup-readiness-360-plan.md](.copilot-tracking/plans/2026-10-17/demo-setup-readiness-360-plan.md) | Assessed final-candidate plan, unchanged |
| [.copilot-tracking/details/2026-10-17/demo-setup-readiness-360-phase-details.md](.copilot-tracking/details/2026-10-17/demo-setup-readiness-360-phase-details.md) | Assessed phase details, unchanged |
| [.copilot-tracking/research/2026-10-17/demo-setup-readiness-360-research.md](.copilot-tracking/research/2026-10-17/demo-setup-readiness-360-research.md) | Supplied evidence and settled directions, unchanged |
| [.copilot-tracking/reviews/2026-10-17/demo-setup-readiness-360-plan-critique.md](.copilot-tracking/reviews/2026-10-17/demo-setup-readiness-360-plan-critique.md) | Complete single critique and actionable finding set |

## Next Steps

The active planning parent should resolve PC-001 through PC-003 directly,
record their dispositions and finalize without another critique. No user
action is required. This critique stops here; it authorizes no implementation
or Azure action.

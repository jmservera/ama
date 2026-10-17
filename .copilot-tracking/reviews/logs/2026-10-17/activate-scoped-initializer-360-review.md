<!-- markdownlint-disable-file -->
# Review: Activate scoped initializer #360

## Scope and Evidence

* Task ID: 360; task slug: activate-scoped-initializer-360; date: 2026-10-17.
* Scope: complete bounded task against e065ecd2, not re-review of merged #375.
* Plan: .copilot-tracking/plans/2026-10-17/activate-scoped-initializer-360-plan.md
* Details: .copilot-tracking/details/2026-10-17/activate-scoped-initializer-360-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/activate-scoped-initializer-360-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/activate-scoped-initializer-360-changes.md
* Research: .copilot-tracking/research/2026-10-17/activate-scoped-initializer-360-research.md
* Source review: .copilot-tracking/reviews/2026-10-17/activate-scoped-initializer-360-source-review.md
* Exact preview/live receipts: .copilot-tracking/changes/2026-10-17/activate-scoped-initializer-360-what-if.json and activate-scoped-initializer-360-live-receipt.json.

## Opening Review State

* Goal: independently compare owner approval, plan acceptance, source/guard
  changes and exact live outcome; distinguish permission grant from d/e acceptance.
* Readiness: complete plan/details/changes, critique Pass, separate preapply
  source review Pass, final 59 tests and exact sanitized preview/live receipts.
* Acceptance basis: owner API-only approval subset; existing-job tag grant
  unapproved; no runtime/network/spend/deletion/secret operations; full lifecycle
  and publication handoff, no merged implementation duplication.
* First comparison: plan-to-change reconciliation and live principal/scope/action
  receipt, then changed source/docs and validation limitations.
* Read-only: reviewer may write only this canonical Review record; no source,
  plan/details/research/changes/state edits or live Azure operations.
* Blockers: relay approval/private publisher/human tenant-runtime d/e remain
  distinct later dependencies, not evidence that API-only deployment failed.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one independent full post-implementation RPI
  Review on 2026-10-17, using the rpi-review reference and review-log template.
  All seven tracked file diffs against e065ecd2c5b09b0f4bc22bfbfdb343e41910189b
  and the matching dated research, plan, details, critique, changes, source
  review, what-if, live receipt and parent state were assessed.
* Branch: chore/activate-scoped-initializer-360; HEAD remains the supplied base.
  No commit or PR existed in the supplied boundary. Publication remains a
  parent lifecycle action, not completed implementation or Review evidence.
* Authority: this record is the only edited file in this Review. No live
  Azure read/write, source correction, plan/state mutation or nested agent.
* Review execution is complete; this does not mean the parent publication
  lifecycle or issue #360 acceptance is complete.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record evidence | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Conditional relay selection | Reconciled | One default-true boolean conditions both relay resources; existing role actions, GUID expressions and assignment scopes unchanged. |
| P01-T02 | Independent source gate; validation record | Reconciled | Build/lint, focused suites and separate predeployment source-review PASS precede the recorded API-only preview/apply. That source review is not this Review. |
| P02-T01 | Exact pre-apply gate; actual apply/readback | Reconciled | Two permitted Creates/94 same-root Ignore rows, same inputs/source hashes, successful single deployment and exact principal/actions/scope readback. |
| P03-T01 | Durable evidence | Reconciled | Existing runbook/evidence/index updated; prior KB log prefix preserved. Historical #375 observations remain distinguished from the later API grant. |
| P03-T02 | Review/publication preparation | Reconciled | Preparation is complete; actual independent Review and commit/push/main PR remain separately owned parent actions. No publication acceptance is inferred from checked markers. |
| Follow-Up Items | Blockers; follow-up items | Reconciled | Relay approval, private publisher and human runtime acceptance/retirement remain outside active implementation; routed separately below. |
| Parent lifecycle | Ordered phase log; pre-Review handoff; state | Reconciled | Changes' “Not yet activated” Review row is a pre-Review snapshot. Parent state says Review active; this record supplies the actual Review outcome. Parent must update its lifecycle evidence after return. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/staff-initializer-rbac.bicep | Added includeResultRelay=true and identical conditions on relayRole/relayAssignment to exclude unapproved existing-job tags without redesigning roles. | Complete Bicep diff; API resources unconditional; guard unchanged and contains no workload resources. | Reviewer independently passed both compiled semantic/mutation tests. | Conformant; false has two active authorization resources; default/true retain four. |
| P01-T01 | infra/tests/test_bicep_policy.py; infra/tests/test_identity_rbac.py | Two tests plus helper in existing compiled suite, three assertions in existing matrix test. | Checks exact actions, empty exclusions/dataActions, ama assignable scope expression, initializer principal expression, API/job scopes and both conditions. Mutations remove each condition and flip default independently. | All three changed tests passed independently without skips. | Within test budget; existing helpers reused; no new module/framework/generated artifact. |
| P01-T02 | .copilot-tracking/reviews/2026-10-17/activate-scoped-initializer-360-source-review.md | Independent STANDARD source gate before live apply. | PASS/no actionable findings; independently compiled and ran two new tests. | Parent reports all 11 identity tests; reviewer-environment import limitation disclosed, not represented as a pass. | Source gate evidence adequate and distinct from full-task Review. |
| P02-T01 | .copilot-tracking/changes/2026-10-17/activate-scoped-initializer-360-what-if.json; .copilot-tracking/changes/2026-10-17/activate-scoped-initializer-360-live-receipt.json | Exact false-parameter preview, successful bounded apply and sanitized readback. | Deployment staff-iam-360-api-20261017 Succeeded; correlation 2177965b-1d42-4709-962b-3475e2186264. | Independent offline receipt/hash assertions passed; no live reexecution. | Authorized API permission slice succeeded, not runtime acceptance. |
| P03-T01 | infra/README.md; docs/architecture/cutover-evidence-pack.md; docs/reference/README.md; docs/reference/log.md | Dated factual receipt, opt-out warning, history/current-state separation and durable routing. | Complete documentation diff; actual IDs/actions and remaining gates agree with receipts. | Added links/anchors resolve; original log prefix byte-for-byte retained; git diff --check passed. | Conformant; omission does not revoke existing grants and commands are not renewed approval. |
| P03-T02 | Current plan/details/changes and parent state | Prepared full evidence set and publication boundary. | All implementation markers complete with no remaining active implementation task. | Cross-artifact reconciliation performed in this Review. | Preparation complete; parent still owns publication and must not claim #360 closure. |

### Actual Live Boundary

* The exact four role actions are Microsoft.App/containerApps/read,
  Microsoft.App/containerApps/revisions/read,
  Microsoft.App/containerApps/revisions/replicas/read and
  Microsoft.App/containerApps/revisions/restart/action. The source and
  role readback agree; dataActions/notActions/notDataActions are empty.
* Role 0d8c4586-d46e-514c-9c19-680d9f068755 has only ama in
  assignableScopes. Assignment 3a7e0803-3997-5cbe-af9c-c9776b37f3a7 binds
  principal 3830883a-f4af-44f8-bff8-8859b78fc2f8 only to
  ca-cutover-test-demo-api, not ca-cutover-test-api or the API runtime MI.
* The two actionable preview rows are the expected API role and API-child
  assignment. The retained projection counts 94 same-root Ignore rows and
  intentionally omits their unrelated payloads. Its applied=false records
  the pre-apply gate, not a denial of the subsequent live receipt.
* The live operation projection contains exactly five successful operations:
  two RBAC Creates, the empty-resource scope-guard deployment metadata,
  the existing initializer identity Read and deployment-output evaluation.
  The guard is not new workload/network infrastructure.
* The receipt records preserved registry AcrPull, only one new initializer
  assignment, absent relay definition/assignment, no old-API new assignment,
  identical before/after observed API environment/revision/ingress metadata
  and retained demo deny-all. These are bounded metadata observations, not
  exhaustive proof of all resource contents or independent live reinspection.
* Existing operator wildcard capability metadata is not consent, nor a new
  lifecycle grant. No temporary job or operator/MI lifecycle role was needed
  or created. No runtime rights were exercised, and the record makes no
  Graph, SQL, secret, browser, image, network, spend or deletion claim.
* Sanitized receipts contain authorization/resource metadata, hashes and
  operation outcomes; no credential values, staff payloads or job-tag values
  are present. All current source hashes equal both receipt hashes.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| Research disposition; P01/P02 | API-only subset rather than unchanged four-resource deployment. | Merged template included existing-job tag grants outside boolean approval. Owner allowed a small properly reviewed amendment; no broader approval presumed. | Current plan/details explicitly select false; source, tests, preview, receipt and docs agree. | This choice was already in the final candidate assessed by the one Pass critique; independent source review and exact preview then passed. | Justified conservative divergence from historical full-template activation; not an unresolved decision or unreviewed material revision. |
| P02-T01 readback | Accept provider-canonical subscription-level role URI for the same exact GUID while requiring ama-only assignableScopes and exact demo-API assignment. | Successful deployment followed by an overly strict local RG-URI assertion; live receipt preserves both forms. | Changes and docs disclose failed initial verification, corrected read-only checks and no second deployment. | No source/action/principal/scope change or expanded owner decision; no new planning/critique gate warranted. | Justified verifier correction, not permission widening or a fabricated Azure denial. |
| P02-T01 operation verifier | Allow exact expected existing MI Read alongside two RBAC Creates, empty guard metadata and output evaluation. | Initial operation-kind assertion rejected identity resolution already required by plan. | Corrected expected operation projection retained in live receipt; all five operations succeeded. | Clarifies existing approved behavior, not new work; no fresh plan/critique needed. | Reconciled; no broad allowlist or runtime retry evidenced. |
| P01-T02 validation | Restore existing source distributions and Ruff only after observed missing import/tool failures; disclose baseline F841. | Recorded failures and final combined 59-pass result; no manifest/framework change. | Plan/details/changes distinguish parent venv success from source-review worker import limitation. | Local execution judgment, not material scope revision. | Conformant; unqualified lint success for the older identity file is not claimed. |
| P03-T02 | Clarify PREPARE Review/publication handoff instead of executing parent lifecycle inside Implement. | Avoid circular implementation completion while preserving required later independent Review and publication. | Phase index, checked task wording, completion evidence, changes summary and handoff consistently separate preparation from lifecycle execution. | Administrative stage-ownership clarification preserves critiqued gates and owner intent; no material revision or new critique needed. | Reconciled; parent must still publish after this Review. |

## Critique and Material Revision Assessment

* Exactly one final-candidate critique is Complete/Pass, with no PC findings.
  The current plan records the planner's accepted disposition; nothing is
  silently dropped or carried into active work.
* The relay opt-out and its compatibility/safety gates were planned and
  critiqued before implementation. They are not a post-critique expansion.
* The independent source-review PASS is expressly before preview/apply in the
  supplied ordered evidence. No evidence shows dependent live work resumed
  before that hard gate. This Review relies on those dated records rather
  than claiming access to unretained raw execution history.
* Later verifier normalizations, dependency restoration and P03-T02 ownership
  clarification do not change authorization, source semantics, acceptance
  boundaries or required lifecycle gates. Their rationale is explicit and
  adequately reconciled; no unaccepted material decision remains.
* No material evidence gap prevents a credible bounded verdict. Raw Ignore
  payloads and live runtime checks are intentionally unavailable/excluded,
  not omitted acceptance evidence for this API-only permission task.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Existing-job tags/read and tags/write approval | Not within API read/restart or temporary-job lifecycle consent. | Owner decides exact existing-job relay grant before any separate activation. | Open; RV-001, distinct approval/activation follow-up, not active implementation defect. |
| Private worker publication | No authorized existing publisher/digest supplied; image build or new infrastructure/spend prohibited here. | Publisher owner supplies immutable worker digest through an existing authorized private path. | Open; RV-002, distinct publisher follow-up. |
| Genuine tenant/browser/role/SQL/AI acceptance and later retirement | Permission assignment does not establish runtime acceptance or authorize release/retirement. | Human operators/owner complete dependencies and later separately authorize retirement. | Open; RV-003, human acceptance follow-up; d/e remain UNMET and retirement remains separately gated. |

Unresolved follow-ups remain outside active P01/P02/P03 implementation,
completion and permission-slice acceptance claims. Each is mirrored in changes
and parent state; none is converted into new current plan work.

## Findings

No implementation defects, unaccepted decision gaps or material research gaps
were found. The complete RV set consists of the following known, non-blocking
residuals for the wider #360 outcome, not defects in this bounded delivery.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Existing-job result relay remains unapproved and absent

* Related scope: Plan Follow-Up Items; P01/P02 authorization boundary.
* Evidence: Current plan, research C1/W4, both relay conditions in
  infra/staff-initializer-rbac.bicep, false-parameter what-if and live receipt
  explicitly record absent relay role/assignment.
* Impact: API permission activation alone cannot enable the existing-job
  result transport. Default true still requires separate tag approval;
  disabled incremental deployment is not a revocation mechanism.
* Destination: Distinct owner approval and later scoped relay activation
  follow-up; not current rpi-implement, rpi-plan or rpi-research.
* Smallest useful next action: Owner decides exact tags/read + tags/write
  authorization for the existing initializer job; until then retain false
  and do not deploy the full/default template.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Immutable private worker publication remains unavailable

* Related scope: Plan Follow-Up Items; publisher dependency.
* Evidence: Research C2/C3, changes blockers, live receipt private_publisher
  and updated runbook/evidence pack consistently retain the existing-publisher
  blocker and record no build attempt.
* Impact: The successful API grant does not provide the worker image required
  for later setup; no new builder/network/spend authority follows from it.
* Destination: Distinct existing private publisher follow-up, owned by the
  publisher owner.
* Smallest useful next action: Supply the immutable worker digest via an
  existing authorized private publisher, or seek a separate decision if no
  such authorized route exists. Do not improvise infrastructure here.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Human live acceptance and later retirement remain gated

* Related scope: Plan Follow-Up Items; issue #360 d/e and release boundary.
* Evidence: Live receipt criterion_d/criterion_e are UNMET; execution_limit
  excludes MI token/propagation/runtime tests. Runbook and evidence pack
  preserve deny-all, tenant/browser/staff/SQL/AI gates and old-stack retention.
* Impact: Role readback cannot establish effective runtime behavior, sign-in,
  staff readiness, acceptance, release authority or retirement safety.
* Destination: Distinct human acceptance follow-up, owned by human
  operators/owner; later retirement requires its own explicit approval.
* Smallest useful next action: After separate relay/publisher dependencies,
  obtain the required human tenant/runtime evidence and disposition d/e.
  Keep demo restrictions and old resources; no restart, job execution,
  browser acceptance or retirement is authorized by this Review.

## Defects

* None within the accepted implementation boundary.
* No Critical or High findings; Medium 3 residual findings; Low 0.
* The identity test's unchanged allowed_conn F841 is a disclosed baseline
  diagnostic, not caused by the three added assertions and not a defect
  demanding current-scope correction. No unrelated cleanup is requested.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct relay approval/activation follow-up | Owner decides exact existing-job tag permission. | Explicitly excluded approval dependency; not an implementation omission. |
| RV-002 | Distinct private publisher follow-up | Publisher owner supplies immutable authorized digest. | Image publication intentionally prohibited in this task. |
| RV-003 | Distinct human acceptance follow-up | Human operators/owner gather real evidence; separately approve later retirement. | Wider d/e remain UNMET; permission configuration is not runtime acceptance. |
| None | rpi-implement | No implementation defect to route. | Current accepted source direction is implemented. |
| None | rpi-plan | No unaccepted decision or invalid plan assumption. | Conservative selection and descriptive updates are reconciled. |
| None | rpi-research | No material evidence gap for this bounded verdict. | Dated sanitized receipts support permission-slice conclusions without live reexecution. |

Later implementation of separately routed work does not require this Review
to run again.

## Residual Work

* RV-001, RV-002 and RV-003 remain distinct wider-delivery dependencies.
* Parent publication is the next already-authorized lifecycle action, not a
  source defect or another RPI Review: record this outcome, resolve/confirm
  privacy-safe GitHub author and committer identity, commit with the required
  Copilot trailer, push only the topic and open a main PR using Refs #360.
  Verify remote head; do not use closing syntax, merge, force push or rewrite
  history. Let normal PR/rubric checks run and leave merge to the owner.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active implementation markers: none.
* Wider #360 blockers: the three routed residuals. They do not invalidate
  the authorized API-only outcome or become new active implementation tasks.
* Remaining parent lifecycle work: persist Review disposition/state and
  factual publication evidence, then stop at the requested boundary. This
  read-only reviewer has not committed, pushed, created a PR or edited state.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Parent Bicep build/lint | Staff RBAC and unchanged scope guard | Passed, recorded | Changes/details record Bicep 0.48.1 with no diagnostics; not independently rerun as a lint check. |
| Parent REQUIRE_AZ_BICEP=1 combined unittest run | Identity and compiled-policy modules | Passed, recorded | Final 59 tests, no skips; parent isolated environment restored existing distributions after missing import. |
| Independent predeployment source review | Source/test/runbook selection boundary | Passed, recorded | PASS/no actionable findings; two new compiled tests independently passed; one identity import unavailable in that worker, parent all 11 passed. |
| Parent scoped Ruff lint/format | infra/tests/test_bicep_policy.py | Passed, recorded | Existing Ruff restored after missing-tool failure; final formatting included in 59-test run. |
| Additional parent identity F-only lint | infra/tests/test_identity_rbac.py | Failed baseline; isolated check passed, recorded | Unchanged F841 allowed_conn reproduced from HEAD; --ignore F841 passes. Not an unqualified clean-lint claim. |
| PYTHONDONTWRITEBYTECODE=1 REQUIRE_AZ_BICEP=1 python3 -m unittest infra.tests.test_bicep_policy.BicepPolicyTests.test_staff_initializer_compiled_relay_selection infra.tests.test_bicep_policy.BicepPolicyTests.test_staff_initializer_relay_condition_mutations_are_rejected infra.tests.test_identity_rbac.RoleMatrixTests.test_staff_initializer_custom_role_matches_matrix_and_api_only_assignment -v | Three changed selection/mutation/matrix guards | Passed, independently run in Review | 3 tests in 10.703 seconds, no skips; compiled output supports false/two, true/four, preserved defaults and rejection mutations. No broad suite or dependency install. |
| Read-only Python receipt/hash/documentation assertions | Both JSON receipts, Bicep/module hashes, exact actions/principal/scope, operation projection, metadata preservation, links and log prefix | Passed, independently run in Review | Source hashes match both receipts; exact API-only identities/inputs; no relay/old-API assignment; five successful bounded operations; d/e UNMET; added Markdown targets/anchors exist; original log is a byte-for-byte prefix. |
| git diff --check | Complete tracked implementation diff | Passed, independently run in Review | No whitespace errors. |
| Live Azure reinspection, effective token/propagation, runtime restart/job, Graph/SQL/vault-secret, browser, image build | Prohibited live and wider acceptance checks | Not run, intentionally excluded | Reviewer authority is offline/read-only except this record; dated receipts are assessed without claiming independent live observation. |
| Commit/push/PR checks | Parent publication lifecycle | Not yet run in assessed boundary | Parent owns authorized post-Review publication; no claim that remote head or rubric checks passed. |

## Outcome

* Outcome: Conformant with justified divergence.
* Rationale: The complete bounded implementation matches confirmed approval,
  the critiqued API-only selection, compatibility requirements and exact
  recorded live outcome. Excluding ambiguous existing-job tags is the
  justified conservative divergence from the historical merged full-template
  activation, not a missing authorized grant. Both relay conditions/default
  and unchanged API role semantics are independently supported by focused
  tests; sanitized receipts and source hashes support the assigned scope.
  Verifier corrections do not widen rights or conceal a deployment denial.
* Acceptance limit: This verdict accepts only this permission-configuration
  task and its prepared evidence/handoff. It does not accept #360 d/e,
  private publication, runtime setup, release, retirement, PR checks or merge.
  The three Medium residuals are known distinct follow-ups, not current
  implementation defects. No later correction or repeat Review is requested.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement route required. |
| Decision gap or invalid assumption | None | No rpi-plan route required. |
| Material evidence gap | None | No rpi-research route required. |
| Non-blocking residual work | RV-001 relay; RV-002 publisher; RV-003 human acceptance | Distinct owners/actions above; no automatic child work or scope expansion. |
| Authorized lifecycle continuation | Active parent publication | Record this outcome, privacy-safe commit/trailer, push topic, open main PR Refs #360, verify head/checks; no merge or issue closure. |

* Execution status: Complete.
* Outcome: Conformant with justified divergence.
* Validation coverage: Entire seven-file diff and matching task artifacts
  compared; three changed tests and bounded offline evidence checks passed
  independently; parent 59-test/build/lint evidence and limitations assessed.
* Review blockers: None. Wider acceptance remains explicitly UNMET.
* This is the task's one complete post-implementation RPI Review. Return to
  the active parent; do not invoke another review, implementation or live step.

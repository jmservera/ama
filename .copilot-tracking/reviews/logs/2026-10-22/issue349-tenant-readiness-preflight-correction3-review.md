<!-- markdownlint-disable-file -->
# Review: Issue 349 tenant-readiness preflight correction3

## Scope and Evidence

* Task ID: issue349-tenant-readiness-preflight-correction3
* Review date: 2026-10-22
* Review scope: One independent pre-commit implementation Review of the supplied correction3 working diff and five correction3 artifacts.
* Assessed boundary: infra/scripts/tenant-readiness-preflight.py and infra/tests/test_tenant_readiness_preflight.py at HEAD 3b881a65c808b02f6ca1bd29d227172f5ad453f6, with reviewed main b4d467cad84535ed106cffa1ae9aa303db7bfed2 as supplied context. No assessment of unrelated historical changes.
* Plan: .copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-22/issue349-tenant-readiness-preflight-correction3-changes.md
* Research: .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction3-research.md

## Opening Review State

* Interpreted review goal: Determine whether readiness now requires both platform.enabled and identityProviders.azureActiveDirectory.enabled literally true, preserving fail-closed behavior, read-only commands, sanitization and the existing output contract.
* Review scope: Only the supplied two-file working diff and exact correction3 artifact set.
* Evidence readiness: HEAD and bounded diff inspected; five exact artifacts supplied and pending comparison. Parent reports 35 focused tests, isolated Ruff 0.17.1 lint/format and diff checks passed, with 30 red-first failures.
* Acceptance basis: Supplied strict-boolean requirement and preserved safety/output behavior; parent explicitly rejects PC-001/PC-002 as worker-local filesystem constraints, not parent constraints.
* First comparison boundary: Reconcile Pxx/task markers and critique dispositions with the two-line production change and synthetic regression tests.
* Active read-only boundaries: Only this review record may be written. No fixes, artifact edits, commit, gate, remote mutation, Azure/Graph access, credentials, deployment, acceptance ticks or second Review.
* Initial blockers: None established. Commit, complete local gate, independent coordinator exact-committed-head assessment and hosted/human acceptance are later work, not presumed results.

## Execution Status

* Execution status: Complete
* Review execution evidence: Exactly one independent Review completed. Inspected the complete two-file working diff, relevant full source/test context and all five supplied correction3 artifacts; independently ran 34 synthetic tests with bytecode disabled. Only this record was written.
* This status describes Review execution, not completion of the whole plan. P01 is complete; P02-T01 is satisfied by this record, but its marker remains parent-owned. P02-T02 has not run.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Three new methods, positive Fake flag and two production edits | Reconciled | Diff matches the declared test budget and strict conjunction. All 32 existing test methods remain. |
| P01-T02 | 35 passing tests, isolated Ruff lint/format and whitespace check | Reconciled | Parent-reported results agree across plan, details and changes. Reviewer separately reproduced 34 tests; evidence attribution is explicit below. |
| P02-T01 | One independent Review remains | Reconciled at entry | This record completes that action; the parent must reconcile the still-unchecked marker before committing. Review cannot edit other artifacts. |
| P02-T02 | Commit, full gate and receipt verification remain | Reconciled | Correctly pending; no gate success, receipt or committed candidate is asserted. |
| Follow-Up Items | Coordinator, hosted checks and human/tenant acceptance | Reconciled | Remain separate, not implementation completion or issue acceptance. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/scripts/tenant-readiness-preflight.py | AUTH_QUERY adds the property-level Azure AD enabled projection; readiness uses two literal-True identity comparisons | Complete bounded diff contains only these two production edits | Independent synthetic subset passes | Conformant: missing, null, false, strings, numbers, objects and arrays cannot satisfy either comparison. |
| P01-T01 | infra/tests/test_tenant_readiness_preflight.py | Positive Fake provider flag plus projection, strict-state and sanitized CLI regression methods | Exactly three added methods; no removed original methods | All three new methods pass independently | Both-true retains overall ready; both-false and either invalid flag block. Query assertion is independent of Fake dispatch. |
| P01-T01 | Both targets | Preserve reporting and safety behavior | No new transport call, credential field, status, reason, check ID, facts field, output-schema field or early return | Existing synthetic guard, sanitization and output tests pass in subset | api-auth-enabled remains mismatch/auth-disabled with empty facts on rejection. Text/JSON exit 1, readOnly=true and acceptanceEstablished=false are retained. |
| P01-T02 | Plan, details and changes | Preserve red-first and green evidence without overstating acceptance | Parent records 35 tests/30 expected failures before source fix and 35 passing afterward | Parent-only lint/format/diff evidence; reviewer 34 passing tests | No validation inconsistency or source blocker found. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01/P01-T02 | Completion markers, actual test counts and handoff updated after implementation | Two-line correction and parent red/green/quality evidence; no new product decision | Plan, phase details and changes agree | One critique retained; parent dispositions recorded | Descriptive updates preserve approved scope and intent. |
| Critique Disposition/P02-T02 | Parent rejects PC-001/PC-002 rather than changing test fixtures or gate output | Supplied parent context explicitly distinguishes worker-local filesystem restrictions from parent authority and requires unique external /tmp gate output | Plan records individual rejection reasons; details retain parent-owned gate; changes preserve original Revise | No second critique required or performed | No significant product or architecture divergence. Worker restrictions are not propagated to the parent. |
| P02-T01/P02-T02 | Review completion and final candidate preparation | This one Review produces new evidence | Parent reconciliation remains pending; this record does not change plan markers | No new planning or critique cycle indicated | Routine authorized continuation, not a technical defect. |

## Critique and Material Revision Assessment

* Latest critique execution is Complete; its original Revise verdict and two High findings remain unchanged in the original artifact.
* PC-001 and PC-002 each have an explicit parent rejection. As directed, this Review assesses technical correctness without treating this worker's filesystem restrictions as restrictions on the parent. Neither finding identifies a defect in the boolean correction, query path, output or permissions.
* The reviewer did not perform any temporary-directory operation. The unchanged usage/help test was excluded from the independent run for this worker only. This does not invalidate or replace the parent's reported 35-test run, and does not require a parent fixture edit.
* Material revisions: None in the implementation diff. Strict comparison, unchanged reporting and the three-method budget all match the accepted plan.
* Dependent-work pause assessment: Research, critique/disposition and P01 evidence precede this Review; commit and gate remain pending. No evidence of premature gate/publication is present in the bounded artifacts.
* Justification assessment: The two production edits are sufficient for the accepted fail-closed requirement. Research qualifies moving CLI dev-source evidence and failed schema retrievals rather than asserting live-version or tenant proof.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Independent coordinator exact-committed-head assessment | Requires the later committed candidate and completed local gate | Parent supplies exact HEAD/base/receipt to independent coordinator | Open; distinct follow-up RV-002, not replaced by this pre-commit Review. |
| Retained hosted checks | This loop prohibits push and PR mutation | Publication owner retains/reviews checks when separately authorized | Open; RV-003, not locally established. |
| Human sign-in/tenant acceptance | Synthetic tests do not establish actual configuration, authority, staff binding or sign-in | Authorized human/tenant owner supplies actual evidence | Open; RV-003; acceptance remains unestablished. |

Unresolved follow-up items remain outside active implementation scope and are not defects or acceptance claims.

## Findings

No implementation defects, significant decision gaps or material research gaps were found in the supplied boundary. The following complete actionable set records remaining delivery work, not source defects.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Committed candidate and complete local gate remain pending

* Related scope: P02-T01/P02-T02.
* Evidence: Plan and phase details leave P02-T02 pending; changes records commit, full gate and receipt verification as remaining. Inspected HEAD remains 3b881a65c808b02f6ca1bd29d227172f5ad453f6 with the correction uncommitted.
* Impact: This Review cannot establish a committed candidate, complete local gate or exact-head receipt. Publication remains prohibited.
* Destination: Distinct active-parent continuation, not rpi-implement, rpi-plan or rpi-research.
* Smallest useful next action: Parent reconciles this one Review into authorized evidence, creates the authorized privacy-safe commit, fetches main and confirms the supplied base, then performs the single authorized full gate and exact-head/base receipt verification. Preserve outputs and stop on failure; do not claim a pass before execution.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Independent coordinator assessment must follow the gate

* Related scope: Plan Follow-Up Items.
* Evidence: Supplied user instruction explicitly requires remaining independent coordinator exact-committed-head assessment after local gate; plan/details/changes preserve that boundary.
* Impact: A conformant pre-commit Review is not approval of the eventual committed and gated HEAD.
* Destination: Distinct independent coordinator follow-up, owned by parent/coordinator.
* Smallest useful next action: After successful gate and receipt verification, provide exact committed HEAD, current reviewed base and external receipt to the independent coordinator. This is not a request for a second RPI Review.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Hosted and human acceptance remain unestablished

* Related scope: Plan Follow-Up Items and acceptance disclaimer.
* Evidence: No live tenant calls or hosted checks were run in this Review. Checker render keeps acceptanceEstablished=false and text states Acceptance: not established. Changes explicitly retain hosted/human requirements.
* Impact: Local synthetic conformance is not tenant readiness, actual sign-in, issue completion, publication authorization or human approval.
* Destination: Distinct later hosted-check and human/tenant acceptance follow-up.
* Smallest useful next action: Authorized publication owner retains hosted checks when publication is permitted; authorized human/tenant owner separately evaluates real sign-in and acceptance. No push, issue/PR change, acceptance tick or deployment is authorized here.

## Defects

* None found in the bounded implementation.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Active-parent P02-T02 continuation | Parent reconciles evidence, commits and executes the single authorized gate/verification | Planned delivery work not yet executed; no source fix needed. |
| RV-002 | Distinct coordinator follow-up | Independent coordinator assesses exact committed/gated HEAD | Required later assessment cannot be replaced by pre-commit Review. |
| RV-003 | Distinct hosted/human follow-up | Publication owner and authorized human/tenant owner | External acceptance is outside local synthetic evidence and current authority. |

No rpi-implement, rpi-plan or rpi-research handoff is indicated. No second Review is requested.

## Residual Work

* RV-001 remains active parent-owned plan work.
* RV-002 and RV-003 remain distinct plan follow-ups, outside bounded source completion.

## Blockers and Remaining Work

* Review blockers: None.
* Remaining active work: Parent reconciliation of P02-T01, then P02-T02 commit/gate/receipt. Review has not performed any of these operations.
* Publication/acceptance constraints: No push or PR mutation authorized; coordinator, hosted and human gates remain outstanding. No claim that prerequisites for the full gate are available or that its result will pass.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Read-only git status/branch/rev-parse and bounded git diff | Two authorized source/test targets | Passed, reviewer-executed | Confirmed topic branch and supplied HEAD; no staged changes. Unrelated state artifact seen in status was not assessed or changed. |
| python3 -B with in-memory unittest loader selecting all module tests except CliTests.test_usage_errors_and_help | 34 synthetic tests, including all three new regressions | Passed, reviewer-executed | Ran 34 tests in 0.108s, OK. No test/source edits, bytecode, cache or temporary-directory operation. Fake transport only. |
| CliTests.test_usage_errors_and_help | One unchanged original test | Skipped by reviewer | Its existing TemporaryDirectory fixture conflicts with this worker's runtime restrictions only. Parent reports the full 35-test module passed; not a defect or parent execution restriction. |
| python3 -B -m unittest discover -s infra/tests -p test_tenant_readiness_preflight.py -q | Full 35-test focused module | Passed, parent-reported | Supplied instruction and changes/details agree; not independently rerun in full. |
| Red-first focused suite | Same module before production correction | Failed as expected, parent-reported | 35 tests, 30 failures, exit 1. External log named in changes was not opened; no independent red-first claim. |
| Ruff 0.17.1 check --isolated --no-cache --select E,F,I,B,UP --target-version py312 --line-length 100 on both targets | Targeted lint | Passed, parent-reported | Changes records the exact command; reviewer did not invoke the externally located tool. |
| Ruff 0.17.1 format --isolated --no-cache --line-length 100 --check on both targets | Targeted format | Passed, parent-reported | Two files already formatted; not independently rerun. |
| git diff --check | Whitespace | Passed, parent-reported | Not independently rerun; review authority limited to inspection and synthetic focused tests. |
| Full --all gate, receipt verification, coordinator, hosted and live sign-in checks | Later committed candidate and acceptance | Not run by reviewer | Pending parent/follow-up owners; explicitly outside current authority. |

## Outcome

* Outcome: Conformant
* Outcome rationale: The supplied working implementation satisfies strict dual-flag readiness and preserves positive readiness, fail-closed behavior, read-only calls, sanitized output and the existing check/status/reason schema. Plan/detail updates and critique dispositions are reconciled. This verdict applies only to the bounded pre-commit correction, not whole-plan completion, the eventual committed HEAD, gate success, publication or issue/tenant acceptance.
* Severity summary: Critical 0; High 0; Medium 0; Low 3, all remaining-work/follow-up records rather than technical defects.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No later rpi-implement needed for reviewed scope. |
| Decision gap or invalid assumption | None | No rpi-plan revision needed. |
| Material evidence gap | None | No rpi-research handoff needed for this bounded correction. |
| Remaining plan work | RV-001 / P02-T02 | Parent reconciles, commits and executes the single gate/verification. |
| Non-blocking residual work | RV-002 and RV-003 / distinct follow-ups | Coordinator, publication owner and authorized human/tenant owner retain their separate gates. |

* Execution status: Complete.
* Outcome: Conformant within the bounded pre-commit scope.
* Validation coverage: Independently passed 34 synthetic tests; full 35, red-first, Ruff and diff checks attributed to parent; complete gate and external acceptance not run.
* Blockers: None to the Review; remaining candidate/acceptance work is not inferred complete.

| Artifact | Description |
| --- | --- |
| [infra/scripts/tenant-readiness-preflight.py](infra/scripts/tenant-readiness-preflight.py) | Reviewed checker working diff and safety/output context |
| [infra/tests/test_tenant_readiness_preflight.py](infra/tests/test_tenant_readiness_preflight.py) | Reviewed regression additions and retained tests |
| [.copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction3-research.md](.copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction3-research.md) | Bounded evidence and uncertainty |
| [.copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan.md](.copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan.md) | Current markers, acceptance and critique dispositions |
| [.copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction3-phase-details.md](.copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction3-phase-details.md) | Task detail and remaining gate work |
| [.copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan-critique.md) | Original critique retained unchanged |
| [.copilot-tracking/changes/2026-10-22/issue349-tenant-readiness-preflight-correction3-changes.md](.copilot-tracking/changes/2026-10-22/issue349-tenant-readiness-preflight-correction3-changes.md) | Parent red/green and quality evidence |
| [.copilot-tracking/reviews/logs/2026-10-22/issue349-tenant-readiness-preflight-correction3-review.md](.copilot-tracking/reviews/logs/2026-10-22/issue349-tenant-readiness-preflight-correction3-review.md) | This single independent pre-commit Review |

## Next Steps

The active parent reconciles this Review, continues the authorized commit and single local gate with exact-head receipt verification, then obtains the independent coordinator exact-committed-head assessment. Preserve original outcomes, stop on gate failure, and retain separate hosted/human acceptance. No user response, source fix, new research, second Review or publication action is requested by this reviewer.

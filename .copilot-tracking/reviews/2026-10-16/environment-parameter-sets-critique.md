---
title: Environment parameter sets final-candidate critique
description: Bounded credibility assessment for issue 137
ms.date: 2026-10-16
---

## Metadata

* Task ID: issue-137.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/environment-parameter-sets-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/environment-parameter-sets-phase-details.md
* Critique execution status: Complete.
* Finding counts: Critical 0; High 2; Medium 3; Low 0.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and research once against current caller direction: pilot region and subscription owner remain open; no actual IDs or secrets; ama-only resources; SQL permanently private; production default with individually explicit dev relaxations; one environment differences table; existing issue 139 offline gates; no legacy-directory or private configuration/dataset access.
* Evidence: .copilot-tracking/research/2026-10-16/environment-parameter-sets-research.md and the necessary infra sources cited below. Research statements about GitHub issues are supplied evidence, not independently retrieved issue text.
* Reviewed requirements, research conclusions, P01/P02 tasks, acceptance criteria, decision boundaries, dependencies, offline verification and delivery. The implementation sequence has a coherent dependency: P01 changes precede P02 validation, review and delivery.
* This assessment does not select pilot inputs, run Azure operations, prove live region/quota availability, infer human approval or implement changes. The current caller direction overrides the historical pilot comment.
* The only written artifact is this critique. Existing untracked planning artifacts were not edited, moved, staged or committed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Existing three parameter paths; no naming migration | Covered | P01-T01 preserves file paths and current hash/name lineage. |
| Pilot region and subscription owner open | Partial | Parameter placeholders and environment prose are covered; another current-looking README assertion is not explicitly reconciled. PC-003. |
| Production default; individually explicit dev relaxations | Partial | Private dev/test intent is clear, but inherited quarantine/purge semantics conflict with independent opt-ins. PC-001. |
| SQL always private, no firewall | Covered | P01-T01/P01-T02 expressly remove the switch/firewall and replace conditional assertions with unconditional isolation and mutation assertions. |
| ama-only scope; workload validation | Covered within stated wrapper scope | Fake-az rejection before discovery/deployment is explicitly required. No group creation/deletion or deployment is planned. |
| Region/quota references; retained issue 139 matrix | Partial | New missing-reference guards need an explicit valid baseline and independent negative/mutation cases in the existing harness. PC-002. |
| Naming/tag forwarding and exceptions | Covered | P01-T02/P01-T03 require semantic checks, existing names and documented taggable-resource exceptions. |
| Single differences table and current documentation | Partial | Consolidation must include the existing profile table and contradictory governance prose. PC-003. |
| Five issue 137 acceptance criteria | Partial | P02-T02 promises an audit, but the supplied inputs do not enumerate the five criteria or their evidence mapping. PC-004. |
| P02-T01 offline tests, compile/lint, Python checks and smoke | Partial | Required gates are identified; scratch paths need an explicit repository-local constraint. PC-005. |
| Maximum 12 added test methods; retain regression gates | Covered subject to revisions | Plan fixes the owner, two existing test files and ceiling; apply findings through existing helpers/methods and parameterized subtests first. |
| P02-T03 delivery and approval boundaries | Covered | Existing topic branch, privacy-safe identity, required trailer, PR without merge or issue checkbox edits; no live acceptance claim. |

## Verdict

* Verdict: Revise.
* Rationale: The overall slice is credible and bounded, but independent development controls and compatibility with the existing guard harness need concrete planner corrections. Documentation, acceptance traceability and repository-local validation paths also need resolution before execution. These are direct corrections under current direction, not new user choices.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Development profile still implicitly disables independent controls

* Related IDs: Functional Requirements; P01-T01; P01-T02.
* Evidence: .copilot-tracking/details/2026-10-16/environment-parameter-sets-phase-details.md, P01-T01, says dev declares quarantine/purge relaxations. infra/main.bicep defines `purgeProtection = !isDev && keyVaultPurgeProtection` and forwards registry `quarantine: !isDev`. infra/tests/test_bicep_policy.py, assert_parameter_controls, expects purge protection to depend only on the profile for accepted combinations.
* Concern: Merely setting development disables quarantine and purge protection, even when purge protection remains explicitly true. There is no independent main-template quarantine input to declare in the dev file. Preserving these expressions would not meet individually explicit relaxations.
* Impact: A caller cannot select development while retaining either control independently; a nominally private development stack silently loses unrelated protection.
* Smallest useful change: Specify production-safe defaults and separate explicit development opt-outs for quarantine and purge protection. State that development alone does not disable either, production rejects opt-outs, dev explicitly declares intended opt-outs, and test/pilot retain protections. Include the required registry forwarding change in P01-T01's allowed surfaces. Keep SQL outside every relaxation.
* Action owner: Planning parent; primary implementer executes the corrected contract.
* Exact resolving evidence: Revised P01-T01 names the independent inputs and expected outcomes; P01-T02 extends existing compiled forwarding/profile assertions for development with default protections, each independent opt-out and production rejection. Mutations must detect forced-off values and disconnected inputs. Reuse existing matrix/mutation methods before adding methods.
* Directly applicable: Yes.
* Decision route: Direct planner correction; current caller direction resolves the desired safety semantics.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: New check-reference guards lack a compatible test baseline

* Related IDs: Research evidence on missing deployment-check references; P01-T01; P01-T02; P02-T01.
* Evidence: P01-T01 calls for separate nonempty region/quota references; P01-T02 promises missing-check rejection and preservation of the existing matrix. infra/tests/test_bicep_policy.py, assert_parameter_controls, constructs values from template defaults, expects `failures()` to be empty and asserts exact failure sets throughout its profile matrix.
* Concern: Fail-closed empty reference defaults add two failures to every existing case unless the harness is deliberately adapted. Nonempty defaults or example references introduced merely to retain green tests would instead weaken the missing-reference gate and risk presenting placeholder evidence as current checks.
* Impact: The implementation can break existing issue 139 gates or make missing-check rejection ineffective while passing compilation. Compilation itself cannot demonstrate named guard rejection.
* Smallest useful change: Define empty/unverified committed reference values and a separate synthetic valid-reference baseline used only by offline semantic tests. Extend the existing guard harness to test region and quota missing separately and together, valid-reference success, expected profile failures with valid references, and guard bypass/disconnection mutations. Do not claim reference validity or live readiness from a nonempty string.
* Action owner: Planning parent; primary implementer owns test updates.
* Exact resolving evidence: Revised P01-T02 specifies the baseline and cases; existing assert_parameter_controls accepts the synthetic test baseline and checks exact named failure sets; compiled guard constraints, forwarding and dependency ordering remain covered. All three committed parameter files compile offline while remaining explicitly unverified for deployment. No actual subscription/tenant/Entra IDs are introduced.
* Directly applicable: Yes.
* Decision route: Direct planner correction, not a request for live checks or pilot choices.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: README reconciliation omits contradictory pilot authority and a second differences table

* Related IDs: Authoritative open pilot decisions; single differences table; P01-T03.
* Evidence: P01-T03 targets settled decisions in the environment section and SQL statements elsewhere. infra/README.md, Governance controls, still says the region and subscription owner were decided on 2026-10-15. Its Deployment profile section has a separate control-differences table in addition to Environments.
* Concern: Updating only the specified environment prose leaves another current-looking assertion of settled region/ownership. Keeping both control tables also leaves competing environment-policy descriptions after development semantics change.
* Impact: An implementer or deployment reviewer can rely on superseded authority or inconsistent relaxation rules even after the environment section is corrected.
* Smallest useful change: Explicitly include Governance controls and Deployment profile in the bounded README reconciliation. Mark superseded pilot region/subscription ownership as historical, without reopening unrelated role decisions. Consolidate environment/control differences into the single canonical environment table and reference it from profile prose; preserve distinct historical observation and governance tables.
* Action owner: Planning parent; primary implementer updates infra/README.md.
* Exact resolving evidence: P01-T03 lists these sections; final documentation review finds no present-tense settled pilot region/subscription owner, one canonical environment-differences table, and consistent SQL/private and independent-relaxation descriptions. Historical dates remain clearly historical.
* Directly applicable: Yes.
* Decision route: Direct planner correction; do not ask the owner to reconfirm superseded choices.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The promised five-criterion acceptance audit is not defined in supplied evidence

* Related IDs: Acceptance Criteria; P02-T02; research issue-evidence summary.
* Evidence: The plan says to audit each of five issue 137 criteria. The supplied research records that the issue was read but does not quote or enumerate those criteria; the phase details refer only generically to issue acceptance.
* Concern: This critique cannot establish that the selected tasks cover all five original criteria or identify which original claims current direction supersedes.
* Impact: Final review may substitute inferred goals for the issue's actual acceptance boundary and overstate completion, particularly for live region/quota or pilot prerequisites.
* Smallest useful change: Have the planning parent materialize the five already-read criteria and map each to a P01 task, exact offline evidence, and any explicitly unverified live prerequisite. Annotate superseded ownership/region assumptions using current direction. Do not expand this critique into GitHub research or invent absent criterion text.
* Action owner: Planning parent, using the issue evidence it already obtained.
* Exact resolving evidence: A five-row acceptance mapping in the planning inputs, with criterion wording, task/evidence pointers and offline-versus-live status; P02-T02 audits that same mapping without ticking issue checkboxes or asserting deployment readiness.
* Directly applicable: Yes.
* Decision route: Direct planner evidence correction. No user response is required; exact original wording is an evidence limitation, not an unresolved user preference.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Validation does not constrain scratch storage to the repository

* Related IDs: P02-T01; no private datasets/configuration; validation execution constraints.
* Evidence: P02-T01 specifies an isolated synthetic temporary data path but no location. infra/tests/test_bicep_policy.py, test_configured_lint_error_fails_build_and_lint, and infra/tests/test_deploy.py, run_deploy and resolver mutation checks, use TemporaryDirectory without an explicit parent.
* Concern: The planned commands can write synthetic data, fake-az fixtures and compilation scratch files to the operating-system temporary directory, contrary to the execution boundary. Isolation alone does not ensure an allowed path.
* Impact: Validation can fail on prohibited writes before producing credible offline evidence, or put smoke data outside the controlled workspace.
* Smallest useful change: Add a repository-local scratch parent for validation, configure the process temporary-directory environment to that absolute path before invoking Python/Bicep tooling, and use a separate repository-local synthetic ZF_DATA path for smoke tests. Keep scratch/compiled artifacts untracked, review the final diff and remove scratch artifacts after validation.
* Action owner: Planning parent; primary implementer owns validation setup and cleanup.
* Exact resolving evidence: P02-T01 records the repository-local paths and command environment; test/smoke execution evidence confirms those locations, synthetic-only data and cleanup. No reads of private configuration/datasets or writes to system temporary directories are needed.
* Directly applicable: Yes.
* Decision route: Direct planner correction; no new dependency or test framework is needed.

## Strengths and Residual Risk

* SQL removal is explicit and appropriately stronger than the old conditional firewall contract. Keep unconditional disabled public access, absence of any SQL firewall resource, absence of the SQL public-switch interface, private endpoint coverage and mutations that reintroduce or remove those protections. Do not restore conditional firewall assertions.
* The test budget is credible if existing helpers, matrix cases and mutation subtests are extended. The ceiling remains 12 added test methods total across test_bicep_policy.py and test_deploy.py, with no test-file removal or parallel policy framework.
* Existing profile/resolver/security gates, canonical Bicep/parameter inputs, temporary compiled JSON and existing workflow/check names are preserved.
* Region/quota references can prove only that an input was supplied. Freshness, service/model SKU/capacity availability, zone support, costs, private-edge acceptance and human approvals remain explicitly unverified deployment prerequisites.
* Pilot region and subscription ownership remain open. They are not blockers for this offline implementation and must not be filled with historical values to close a critique finding.

## Questions or Blocking Evidence Gaps

* No user question is necessary for these corrections.
* Exact original acceptance-criterion text is absent from the supplied evidence; PC-004 routes it to the planning parent. No live or private evidence is requested.

## Limitations

* Only the three supplied planning/research files, the skill template and necessary infra sources were read. No GitHub issue/comment fetch, legacy-directory access, private configuration/dataset read, Azure command, test run or implementation occurred.
* This is a plan critique, not a verification that future changes pass tests. Compiled-template semantic assertions remain offline evidence, not live ARM or pilot acceptance.
* This is the single complete actionable finding set for the supplied boundary. No further critique pass is requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct independent development-control semantics and extend the existing matrix contract, then apply PC-002 through PC-005 directly and finalize the plan without another critique.
* User response required: No. Pilot decisions remain open and outside this offline slice.

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-16/environment-parameter-sets-plan.md](.copilot-tracking/plans/2026-10-16/environment-parameter-sets-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-16/environment-parameter-sets-phase-details.md](.copilot-tracking/details/2026-10-16/environment-parameter-sets-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-16/environment-parameter-sets-research.md](.copilot-tracking/research/2026-10-16/environment-parameter-sets-research.md) | Supplied evidence and decision boundaries |
| [.copilot-tracking/reviews/2026-10-16/environment-parameter-sets-critique.md](.copilot-tracking/reviews/2026-10-16/environment-parameter-sets-critique.md) | Complete critique and recorded Revise verdict |

## Next Steps

The active planning parent should apply PC-001 through PC-005, retain the 12-added-test ceiling and finalize without another critique. No user action is required. Critique execution stops here; no implementation or nested delegation is authorized by this review.

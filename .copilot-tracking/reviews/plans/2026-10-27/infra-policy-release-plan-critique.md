<!-- markdownlint-disable-file -->
# RPI Plan Critique: infra-policy-release

## Metadata

* Task ID: 147-138
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/infra-policy-release-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/infra-policy-release-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate critique; no delegated or repeated critique.

## Inputs and Criterion Boundary

* Caller requirements: ordered Research, Plan, Implement and Review followed by one commit/push/PR workstream, authoring only #147/#138. Require local az bicep build and existing infra tests. No Azure deployment, secret reads, private data, runtime changes, branch-protection changes or full gate. No scoped heavy gate is planned.
* Supplied evidence: .copilot-tracking/research/2026-10-27/infra-policy-release-research.md, especially C1-C11; supplied plan and phase details; current infra/main.bicep, infra/modules/guard.bicep, infra/policy-exceptions.json, infra/README.md, infra/tests/test_bicep_policy.py, infra/tests/test_pipeline.py, infra/tests/test_governance.py, infra/scripts/pipeline.py, .github/workflows/src-ci.yml and .github/workflows/src-deploy.yml.
* Local CLI contract: gh api --help confirms that adding field parameters changes the default method to POST unless --method GET is explicit.
* Decisions: Defender cost/coverage/activation and actual protected environments/OIDC remain owner decisions, not implementation assumptions. Existing workflow/check names, default dev/test lock behavior and historical exception dates remain unchanged. Live criteria remain unchecked/Not run.
* Dependencies: existing #137 parameter authoring; a successful manual main src-ci.yml run for the release's exact SHA; owner setup for eventual live acceptance, not for offline authoring.
* Acceptance boundary: assess credibility of proposed guard enforcement, fail-closed source-CI prerequisite, four release-image SPDX artifacts, local regression validation and truthful issue evidence. This critique does not establish implementation correctness or live acceptance.
* Workspace: feat/infra-policy-147; supplied planning inputs were already untracked. No source was changed or moved. Read-only PR inspection returned no matching PR.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller scope, ordered RPI and one PR | Covered | Research precedes this critique; implementation, one independent Review and publication remain later parent actions. |
| C1-C5, owner decisions and live criteria | Covered | No Defender activation, actual environment assumptions, deployment or issue closure proposed. |
| C6, P01-T01, pilotRequiresLocks | Partial | Appropriate existing guard pattern; exact-set matrix and mutation fixture integration need explicit correction, PC-002. |
| C7-C8, P01-T02, exact-SHA CI prerequisite | Partial | Correct manual main workflow and dependency approach; executable query/response contract is underspecified, PC-001. |
| C7, P01-T02, four release SPDX artifacts | Partial | Correct same-image/matrix intent; existing two-Trivy-step assertion must be adapted without weakening scans, PC-003. |
| C9, P01-T01, historical SQL exception | Covered | Clarification preserves dates and denies current SQL bypass or renewal authority. |
| C10-C11, P02-T02, criterion-level evidence | Covered | Authoring and application/live acceptance remain distinct; Refs rather than unsupported Closes. |
| P02-T01, validation and test ownership | Covered with corrections | Existing suites, required Bicep, all builds and actionlint; no removals/new test files, maximum four new methods. PC-002/003 are extensions of existing methods. |
| Publication constraints | Covered | No full gate or workflow/check rename; no scoped heavy gate planned; privacy-safe local identity, non-force push and one PR specified. |

## Verdict

* Verdict: Revise
* Severity summary: 1 High, 2 Medium, 0 Critical, 0 Low.
* Rationale: The bounded authoring direction is credible and owner boundaries are respected. Before implementation, make the source-CI query demonstrably fail closed and explicitly reconcile two existing executable test contracts that the planned additions affect. All findings are direct planner corrections, not new owner choices.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify the read-only query and validate a successful run, not only its SHA

* Related IDs: C7-C8; P01-T02; P02-T01; missing/failed/wrong-SHA/inaccessible CI acceptance.
* Evidence: .copilot-tracking/details/2026-10-27/infra-policy-release-phase-details.md:38-48 specifies API filters and returned SHA comparison, but its executable cases cover only success, missing/wrong SHA and API failure. .github/workflows/src-ci.yml:3-6 confirms PR and manual triggers. Local gh api --help states that field flags select POST unless --method GET is supplied.
* Concern: The proposed query is not yet a reproducible fail-closed contract. A same-SHA failed, incomplete, wrong-branch or wrong-event record is not an explicit negative test, and no response-side success validation is specified. A fake command returning convenient output can pass tests while ignoring the actual endpoint, HTTP method or filters. Field-based gh invocations can also accidentally become POST. These are planning gaps, not claims about code that has not been written.
* Impact: An implementation could reject all valid releases through the wrong method, or accept insufficient CI evidence if it checks SHA alone or suppresses an API/query error.
* Smallest useful change: Specify the workflow-specific repos/{repository}/actions/workflows/src-ci.yml/runs endpoint, explicit --method GET for field-based queries, bounded page size and exact head_sha/branch/event/status filters. Require successful API/parsing exit status and at least one well-formed record whose head_sha equals RELEASE_SHA, head_branch is main, event is workflow_dispatch, status is completed and conclusion is success. Deny empty/null/malformed responses; do not mask command failure. Keep the prerequisite main-only, contents/actions read-only and free of id-token; make build depend on its success without an overriding always condition. Do not auto-dispatch CI.
* Action owner: Planning parent; implementation owner executes the corrected contract.
* Exact resolving evidence: Plan/details state the endpoint/method, response predicate, bounded query and error propagation. Existing test_pipeline.py gains bounded subcases executing the actual extracted workflow Bash with a fake gh that checks endpoint/method/filter arguments and exercises valid success, no runs, wrong SHA, same-SHA failure/incomplete/wrong event/wrong branch, malformed/null evidence and nonzero API exit, including nonzero exit with plausible output. Structural assertions preserve the gate-to-build-to-publish-to-deploy chain and least privilege. These cases fit the existing maximum of four added test methods through subtests.
* Decision route: Direct planner correction. No user response required; the caller already requires successful exact-SHA manual main CI and fail-closed behavior.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Integrate pilot lock semantics into existing exact-set and mutation assertions

* Related IDs: C6; P01-T01; P02-T01; compiled guard compatibility acceptance.
* Evidence: infra/tests/test_bicep_policy.py:1657-1797 evaluates every guard and compares exact failure sets. Its current profile/public/purge/quarantine matrix invokes pilot with the default enableLocks=false, but pilot_expected contains only the existing profile failures. The same helper is reused by test_mutations_reject_production_guard_bypass at lines 1972-1995. The committed-parameter contract at lines 497-551 already asserts pilot enableLocks=true and the exact placeholder failure set.
* Concern: Details say to extend the matrix and preserve named expectations but do not identify the existing pilot calls that become invalid when pilotRequiresLocks is added. Adding separate lock assertions while leaving those expectations unchanged deterministically breaks both the baseline helper and mutation tests, potentially making a mutation appear rejected for the wrong reason.
* Impact: The new guard can be correct while the existing suite fails, or mutation rejection can become vacuous because the unmutated assertion already fails.
* Smallest useful change: Explicitly extend the existing matrix across environment and lock state: pilot/unlocked adds pilotRequiresLocks alongside any existing failures; pilot/locked retains previous expectations; dev/test accept both lock states without changing defaults. Add the new guard to the existing forced-ok mutation loop. Preserve committed pilot parameters and their existing placeholder failures rather than accepting a new unrelated failure.
* Action owner: Planning parent; implementation owner updates the existing compiled-policy tests.
* Exact resolving evidence: Plan/details name assert_parameter_controls, the existing pilot_expected calculation, the guard-bypass mutation loop and the committed-parameter contract. Targeted execution proves the unmutated helper passes, pilot/unlocked fails by the named lock guard, pilot/locked does not, dev/test remain compatible, the forced-ok mutation fails for the intended lock case, and the committed pilot example retains only its known placeholder failures.
* Decision route: Direct planner correction. No owner decision or production-default change required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Preserve scan assertions when adding the third Trivy SBOM step

* Related IDs: C7; P01-T02; P02-T01; SPDX artifact acceptance.
* Evidence: infra/tests/test_pipeline.py:212-236 selects every aquasecurity action in build, asserts exactly two entries and indexes those entries as the fixable gate and unfixed-inclusive report. P01-T02 requires reusing the pinned Trivy action for new SPDX generation, introducing a third matching entry.
* Concern: The plan budgets existing-test extensions but does not state how this executable two-entry contract changes. Simply appending the SBOM action fails the current test; merely changing the count to three leaves positional scan assertions fragile and does not prove that the third invocation generates the required SPDX from the exported image.
* Impact: Regression validation will fail or can be weakened while appearing to cover release inventory.
* Smallest useful change: Extend the existing release contract to identify vulnerability scans separately from the format=spdx-json image invocation. Preserve both original scan semantics and assert exactly one SBOM step per matrix expansion, the same release image reference, generation and successful artifact upload before docker save, a project-unique output/artifact name and if-no-files-found=error. Generation/upload failures must prevent normal export/publication.
* Action owner: Planning parent; implementation owner updates the existing pipeline workflow contract.
* Exact resolving evidence: Plan/details explicitly assign the existing test_release_is_main_only_serialized_and_gates_exact_image extension, retaining its two vulnerability-scan assertions and adding separate SPDX/artifact/order assertions for the unchanged four-project matrix. Targeted test_pipeline.py execution and actionlint pass without deleting scan coverage or adding test files.
* Decision route: Direct planner correction. No user response required.

## Strengths and Residual Risk

* Existing guard, release matrix, pinned actions, permissions and dependency chain are reused instead of creating parallel controls or renaming checks.
* Manual main CI is correctly distinguished from historical PR success and is not automatically dispatched with additional workflow-write permissions.
* Per-release SPDX addresses independently rebuilt images rather than presenting source-CI inventory as release-image evidence.
* Historical EX-001 clarification preserves original dates and owner control without granting present public SQL authority.
* Defender spending/activation and actual environment/OIDC setup remain explicitly unresolved. Offline authoring does not tick live criteria or establish deployment, health, private connectivity or application acceptance.
* The supplied no-full-gate instruction governs this task; no contrary gate recommendation is made. Local tests and a later independent Review remain required and are not approval substitutes.

## Questions or Blocking Evidence Gaps

* No decision-critical user answer is needed to correct this plan.
* Owner Defender decisions and actual environment/OIDC setup remain blockers only to their corresponding live acceptance, not to this authoring slice.

## Limitations

* This is a plan critique, not an implementation Review. No build, test suite, workflow dispatch, Azure call, secret read or deployment was performed.
* Issue acceptance boundaries use the supplied caller context and research C1-C2; issue bodies and remote API run behavior were not independently re-researched.
* Source contracts and local CLI help support the findings. No implemented defect or actual hosted execution result is inferred.
* Only this critique artifact was authored; supplied plan, phase details, research and other records were not edited.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Directly correct the query/negative-case contract and existing-test integrations in plan/details, record all three dispositions, then finalize planning and continue the already authorized implementation sequence.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/infra-policy-release-plan.md](.copilot-tracking/plans/2026-10-27/infra-policy-release-plan.md) | Supplied candidate plan |
| [.copilot-tracking/details/2026-10-27/infra-policy-release-phase-details.md](.copilot-tracking/details/2026-10-27/infra-policy-release-phase-details.md) | Supplied phase and task details |
| [.copilot-tracking/research/2026-10-27/infra-policy-release-research.md](.copilot-tracking/research/2026-10-27/infra-policy-release-research.md) | Supplied bounded research evidence |
| [.copilot-tracking/reviews/plans/2026-10-27/infra-policy-release-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/infra-policy-release-plan-critique.md) | Original single-pass critique and complete actionable finding set |

## Next Steps

The active planning parent corrects PC-001 through PC-003 directly and records
their dispositions without another critique or further agents. No user action
is required. Preserve this original Revise verdict and continue the ordered
implementation, local validation, independent implementation Review and one-PR
handoff under the caller's existing authorization and owner boundaries.

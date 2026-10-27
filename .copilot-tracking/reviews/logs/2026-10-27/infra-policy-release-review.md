<!-- markdownlint-disable-file -->
# Review: infra-policy-release

## Scope and Evidence

Task ID: 147-138. Date: 2026-10-27. Full task, authoring-only boundary.
Base: 0ded682bab690d24eb59b78e704be82d337bf6cd (fetched origin/main).
Evidence set:
* .copilot-tracking/research/2026-10-27/infra-policy-release-research.md
* .copilot-tracking/plans/2026-10-27/infra-policy-release-plan.md
* .copilot-tracking/details/2026-10-27/infra-policy-release-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-27/infra-policy-release-plan-critique.md
* .copilot-tracking/changes/2026-10-27/infra-policy-release-changes.md

## Opening Review State

Goal: independent comparison of bounded implementation against plan, criteria
and critique dispositions, including fail-closed workflow and guard semantics.
Readiness: full plan checked with local validation; original critique preserved.
Acceptance basis: authoring/local evidence only, not owner/live issue acceptance.
First boundary: complete git diff against base and supplied reconciled artifacts.
Read-only: only this canonical review record may be written. No source fixes,
new investigation scope or cloud operations. No initial authoring blocker.

## Execution Status

* Execution status: Complete.
* Exactly one independent post-implementation Review performed, without agents
  or a repeated Review. All seven changed source files and all five supplied
  RPI inputs were compared.
* Assessed candidate: working-tree implementation on feat/infra-policy-147
  against 0ded682bab690d24eb59b78e704be82d337bf6cd. Read-only inspection confirmed
  both HEAD and origin/main resolve to that supplied fetched base.
* This is not an exact final committed-head assessment, hosted result, human
  approval, publication approval or whole-issue acceptance.

## Compared Artifacts

Complete source diff, 200 insertions and eight deletions:

* .github/workflows/src-deploy.yml
* infra/main.bicep
* infra/modules/guard.bicep
* infra/policy-exceptions.json
* infra/tests/test_bicep_policy.py
* infra/tests/test_pipeline.py
* infra/README.md

The five RPI inputs listed in Scope and Evidence were read in full. Relevant
unchanged behavior was traced through .github/workflows/src-ci.yml,
infra/scripts/pipeline.py, infra/tests/test_governance.py, src/trivy.yaml and
the committed-parameter contract in infra/tests/test_bicep_policy.py.
Repository case-study, addendum opening, reference index and owner memory were
read for context, not treated as fresh operational or approval evidence.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Pilot lock invariant and historical exception | Reconciled | Main expression, constrained guard parameter/output, matrix and mutation cover the intended lock requirement; exception metadata retains dates and owner. |
| P01-T02 | Exact-main CI prerequisite and release inventory | Reconciled | Main-only read-only prerequisite gates build, publish and deploy; release-image SPDX generation/upload precede image export. |
| P02-T01 | Validation Record | Reconciled | Parent reports required-Bicep full discovery, all builds/lint, actionlint and modified-test Ruff passing; initial missing-prerequisite failures remain recorded. |
| P02-T02 | Runbook and criterion-level acceptance boundary | Reconciled | Runbook and changes distinguish authoring from every owner/live criterion and use Refs, not unsupported closure. |
| Follow-Up Items | Blockers and Follow-Up Items | Reconciled | Defender decisions and actual environment/OIDC/pipeline acceptance remain outside active implementation and acceptance claims. |
| Handoff | Remaining Work / Return-to-Caller State | Reconciled | Implementation and local validation are complete; this Review is the next stage. Publication is later parent work, not a completed or authorized Review action. |

Plan checkboxes, phase status, completion evidence, critique dispositions and
handoff prose agree at the authoring boundary. The details' commit/push/PR
instructions describe the later parent continuation; their presence does not
establish that publication has occurred or belongs to this Review.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/main.bicep; infra/modules/guard.bicep; infra/tests/test_bicep_policy.py | Require pilot locks without changing dev/test defaults | pilotRequiresLocks returns empty only for unlocked pilot; minLength(1) constrains the named parameter; existing guard dependencies remain | Parent's compiled-policy/full infra PASS; independent source comparison | Conformant for authoring; no ARM deployment claimed |
| P01-T01 | infra/policy-exceptions.json; infra/README.md | Remove misleading present public-SQL authority from historical EX-001 | Only reason text changes in the register; owner, scope, firstObserved and expiry remain unchanged | Parent's existing governance/full infra PASS; diff inspection | Conformant; no new exception or activation |
| P01-T02 | .github/workflows/src-deploy.yml; infra/tests/test_pipeline.py | Require complete successful exact-SHA manual main source CI | Workflow-specific explicit GET, bounded filters and response-side predicate; actual extracted Bash exercised by fake gh | Parent's full infra and actionlint PASS; source and test inspection | Conformant fail-closed authoring |
| P01-T02 | .github/workflows/src-deploy.yml; infra/tests/test_pipeline.py | Retain inventory of each independently rebuilt release image | Four-project matrix, same image reference, SPDX output/artifact and required upload before docker save | Parent's full infra and actionlint PASS; ordering and failure-path inspection | Conformant; existing two vulnerability gates retained |
| P02-T01 | infra/tests/test_bicep_policy.py; infra/tests/test_pipeline.py | Extend canonical tests, not parallel test infrastructure | One added method; existing matrix, mutation and scan assertions extended; no test removals | 452 tests PASS, zero skips; lint/build evidence below | Completion supported within supplied validation boundary |
| P02-T02 | infra/README.md; changes record | Explain manual-CI prerequisite, release SBOMs, pilot locks and owner/live gaps | Runbook and all four #147 / six #138 criterion rows agree with scoped changes | Documentation/diff review; whitespace PASS | Completion supported; issue closure remains unproven |

### Source CI and Existing Release Behavior

The new source-ci job is main-only, contains one explicit Bash step, has only
contents:read/actions:read and no Azure login or id-token permission. GitHub
context values enter through environment variables, not shell interpolation
of expressions. The workflow-specific endpoint selects src-ci.yml; explicit
GET prevents field flags from changing the request to POST. Filters include
the exact release SHA, main, workflow_dispatch, success and per_page=1.

The jq predicate requires an array containing a record with matching head_sha,
main head_branch, workflow_dispatch event, completed status and success
conclusion. It does not merely trust query filters or the SHA. Empty, missing,
null, malformed or wrong-shaped evidence cannot satisfy it. Explicit shell:bash
uses the runner's error/pipefail behavior; the enclosing failure branch exits
nonzero on API or parser failure, including plausible JSON accompanying a
failed API exit. Tests execute the extracted Bash with that same error model
and check exact gh arguments in 14 positive/negative subcases.

Build now needs source-ci without an always() bypass. Publish still needs the
entire build matrix and deploy still needs publish. Consequently failed or
skipped prerequisite/build jobs prevent release progression before Azure.
The existing src-ci.yml retains manual/PR triggers and all existing jobs.
Its manual run has no PR base, so the existing changed-images dispatcher
selects all four images rather than accepting a path-filtered PR subset.
This assessment does not claim that such a hosted manual run has occurred.

Both original Trivy vulnerability invocations retain their semantics and
failure evidence. The new SPDX step targets the same local image tag as the
scans and docker save, with no intervening rebuild/tag mutation. Every matrix
project gets a distinct release-sbom artifact and file. Generation, required
artifact upload and export have neither failure-tolerant conditions nor
continue-on-error; ordinary success gating blocks export on either failure.
Pinned actions, existing workflow/job names, serialization, protected
environments, approval-before-login, OIDC separation, same-run artifacts,
versioned tags and digest handoff remain unchanged.

### Pilot Guard and Existing Parameter Behavior

The new guard uses the existing constrained nested-template pattern. Its output
includes the parameter, and resource dependencies on parameter-guard remain
intact. The compiled-expression matrix checks all six environment/lock
combinations across the existing profile/public/purge/quarantine combinations,
retaining exact failure-set assertions. Locked pilot keeps previous expected
failures; unlocked pilot adds only pilotRequiresLocks. Dev/test accept both
explicit choices and retain the false default.

The forced-ok mutation loop includes pilotRequiresLocks and reuses the passing
unmutated helper, so rejection is not explained by a known baseline failure.
The unchanged committed-parameter test still requires pilot locks and only
the original region/quota/location placeholder failures. No placeholder was
filled and no production/profile or private-network control was weakened.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 / PC-001 | Specify exact GET/query/response/error and executable negative-case contract | Original critique identified implicit-POST and insufficient-evidence risks; no new owner choice | Plan disposition, phase details, changes and workflow/tests agree | Original Revise preserved; direct correction recorded before implementation | Compatible clarification, no significant divergence |
| P01-T01 / PC-002 | Integrate lock semantics into existing exact-set matrix and forced-ok mutations | Original critique identified deterministic old-expectation failures | Plan/details name the helper and committed-parameter boundary; actual test diff implements both | Direct correction documented; no defaults changed | Reconciled |
| P01-T02 / PC-003 | Distinguish two vulnerability scans from the added SPDX invocation | Original critique identified the two-entry assertion conflict | Plan/details and extended release contract preserve scan assertions and add artifact/order checks | Direct correction documented | Reconciled |
| P02-T01 | Restore missing installed distributions/tools after local prerequisite failures | Initial API smoke and missing Ruff, as supplied by parent; no scope or cloud authority added | Changes and phase completion retain initial adverse results and subsequent passing full suite | Implementation dependency recovery, not an architecture revision | Justified; no fresh planning/critique required |

No material scope, architecture or acceptance divergence was identified.
The existing owner decisions were not replaced by implementation assumptions.

## Critique and Material Revision Assessment

* PC-001 High: resolved for authoring. Explicit workflow-specific GET and
  per_page=1 accompany all filters; response validation includes all five
  success properties. Fake-gh cases validate arguments and deny API failure
  with success-shaped output, malformed/null/empty data and wrong run fields.
* PC-002 Medium: resolved for authoring. Existing matrix integrates both lock
  states for dev/test/pilot, exact expected sets remain meaningful, forced-ok
  mutation covers the new guard, and committed pilot placeholder expectations
  remain unchanged.
* PC-003 Medium: resolved for authoring. Tests distinguish two original scans
  from exactly one SPDX invocation and assert same-image output, project-unique
  artifact, required file, ordering and non-tolerant failure behavior.
* Original critique remains Complete / Revise, with one High and two Medium
  findings. Their later dispositions do not rewrite that historical result.
* The supplied chronology records direct plan/detail corrections before
  implementation; no contradictory evidence of early dependent-work
  resumption was found. No new significant decision or material revision
  requiring owner selection was identified.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Defender coverage, accepted cost and activation, #147 | User authorized authoring only; subscription-specific quantities/cost and activation approval are absent | Subscription owner @jmservera records selected plans/subplans, cost and activation decision | Open distinct owner follow-up; not an implementation defect or active-plan task |
| Protected environments, OIDC/RBAC, private runners and actual pipeline acceptance, #138 | Live configuration and execution are expressly prohibited in this task | Owner arranges separately authorized setup and observed federation/what-if/approval/push/deployment/health evidence | Open distinct live-acceptance follow-up; all such checks remain Not run |

The changes record mirrors both follow-ups. Neither is included in active
P01/P02 completion or whole-issue acceptance. Already owner-ticked governance
criteria remain historical owner status, not new deployment/compliance proof.

## Findings

No substantive RV-xxx finding was identified within the complete supplied
authoring boundary. Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low.
The two explicit owner/live follow-ups are preserved separately, not
misclassified as implementation defects or new review findings.

## Defects

None identified within the reviewed authoring scope.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | Parent retains this single Review result | No implementation defect, significant decision gap or material authoring-evidence gap found |

Later implementation of any separately identified work does not require this
Review to run again.

## Residual Work

* Distinct owner follow-up #147: Defender coverage/cost/activation decision.
* Distinct owner/live follow-up #138: environment/federation/private-runner
  setup and observed pipeline/application acceptance.
* Publication remains later parent work. This Review neither implements nor
  publishes anything and does not establish exact final committed-head status.

## Blockers and Remaining Work

* Review/authoring blockers: none.
* Remaining active implementation work: none identified.
* Whole-issue/live acceptance remains blocked by the explicit owner decisions,
  configuration and unrun observations above. No issue closure is supported.
* No Azure operation, workflow dispatch, deployment, secret/private-data read,
  environment/protection change or heavy/full gate was requested or performed
  by this Review. No forbidden operation is recommended to complete authoring.

## Validation Evidence

Passing execution results below are supplied parent evidence corroborated
against the changes record and test contracts, not independently rerun suites
or exact final committed-head receipts. Repetition was unnecessary for this
bounded evidence review.

| Command or check | Scope | Status | Summary |
| --- | --- | --- | --- |
| Initial compiled-policy suite | Existing policy tests | Passed, parent evidence | 50 tests, 82.567s |
| Initial host pipeline suite | Existing pipeline/API smoke | Failed, parent evidence | 29 tests; installed local API could not start because src distributions were absent; retained as initial prerequisite failure |
| Initial host Ruff | Modified tests | Unavailable, parent evidence | Command missing; not represented as a passing initial run |
| Isolated session venv / pip recovery | Missing local src distributions and tools | Passed, parent evidence | Recovery occurred after observed prerequisites failed; no runtime source or dependency manifest changed |
| REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q | Full infra discovery | Passed, parent evidence | 452 tests, zero skips, 140.796s; includes actual-Bash fake-gh cases, compiled guard/mutations and synthetic API smoke |
| az bicep build --file each --stdout | All 25 top-level/module Bicep files | Passed, parent evidence | Bicep 0.48.1; no generated ARM source files committed |
| az bicep lint --file each | Same 25 Bicep files | Passed, parent evidence | All passed |
| actionlint -config-file infra/tests/actionlint.yaml | infra-plan/src-deploy/src-ci/mvp-ci/mvp-validation | Passed, parent evidence | All five relevant workflows passed |
| Ruff check and format --isolated, line length 100, py312 | Both modified test files | Passed, parent evidence | Pinned Ruff 0.17.1 lint/format accepted |
| git diff --check | Complete source diff | Passed, independently executed in this Review | No whitespace errors |
| Complete diff and artifact comparison | Seven changed sources and five supplied RPI inputs | Complete, independently performed | All source changes examined against supplied fetched origin/main base |
| Duplicate full-suite execution | Same supplied passing candidate | Not run | Avoided unnecessary repetition and additional file writes; no evidence mismatch required it |
| Hosted exact-SHA manual CI / actual release-image SBOM generation and upload | Future hosted release | Not run | Offline contracts establish authoring behavior, not an observed hosted run |
| Azure/OIDC/what-if/approval/push/deploy/health and whole-application acceptance | Live acceptance | Not run | Outside authorization; owner/live gates preserved |
| Optional scoped heavy gate / full gate | Gate tooling | Not run | No heavy gate needed for this bounded slice; full gate explicitly prohibited |

## Outcome

* Outcome: Conformant.
* Rationale: Complete local-authoring requirements and all three critique
  dispositions are supported by the complete source comparison and supplied
  passing local evidence. Existing behavior and controls are preserved except
  the intended stronger pilot/release requirements. No substantive defect or
  unaccepted decision was identified at this boundary.
* This verdict does not accept #147/#138 in full, resolve owner decisions,
  convert Not run into passed, or establish hosted/human/publication approval.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement finding |
| Decision gap or invalid assumption | None in active scope | No rpi-plan finding; existing #147 owner follow-up remains separate |
| Material evidence gap | None in authoring scope | No rpi-research finding; unrun hosted/live evidence is not fabricated |
| Non-blocking residual work | Distinct #147 and #138 follow-ups | @jmservera for Defender decision; owner for separately authorized environment/live acceptance |

* Execution status: Complete.
* Outcome: Conformant.
* Finding count: zero; all severity counts zero.
* Validation coverage: supplied full local infra/compiler/linter evidence plus
  independent complete diff/artifact/behavior comparison and whitespace check.
* Blockers: no authoring/Review blocker; owner/live issue gates remain open.
* Next owner: active parent receives this one Review result and controls later
  continuation. No implementation, publication or repeat Review was performed.

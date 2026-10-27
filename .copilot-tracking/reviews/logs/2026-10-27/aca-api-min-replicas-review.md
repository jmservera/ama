<!-- markdownlint-disable-file -->
---
title: API minimum replicas independent implementation review
description: One post-implementation review of bounded infrastructure changes
ms.date: 2026-10-27
---

# Review: API minimum replicas

## Scope and Evidence

* Task ID: aca-api-min-replicas-2026-10-27
* Review date: 2026-10-27
* Scope: Full local implementation P01/P02 and task evidence, not publication acceptance.
* Base: 4bd06495651e58e9957ace590880006eedb8047a.
* Plan: .copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md
* Details: .copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/aca-api-min-replicas-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/aca-api-min-replicas-changes.md
* Research: .copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md

## Opening Review State

* Goal: independently compare default 0/production 2 input chain, preservation
  and scoped verification against owner direction and canonical plan.
* Scope: working source diff and reconciled dated evidence before local commit.
* Evidence readiness: P01/P02 checked; 447 infra tests pass without skips,
  24 Bicep builds/lints and changed-test Ruff pass recorded.
* Acceptance basis: owner scope, plan requirements, locked test contract and
  critique disposition. No deployed-state or cost claim.
* First boundary: main/module schemas and forwarding, then examples/docs/tests
  and complete RPI reconciliation.
* Read-only boundary: source and all prior artifacts; only this review record
  may be written by the independent reviewer.
* Initial blocker: publication requires excluded full gate; does not prevent
  local review. No push/PR is authorized absent mandatory evidence.

## Execution Status

* Review execution status: Complete.
* Planned implementation execution: Complete for P01/P02.
* Evidence boundary: independent read-only assessment on 2026-10-27 of the
  complete eight-file working source diff against
  4bd06495651e58e9957ace590880006eedb8047a on fix/aca-api-min-replicas, all
  canonical task artifacts and the current automatic-parent state.
* This is the task's single post-implementation Review. No agents, further
  review pass, source edits, test reruns, dependency installs or cloud calls
  were used. The reviewer independently ran only read-only inspection and
  git diff --check.
* The candidate is not committed at this review boundary. Local commit and
  parent closeout remain continuation work, not an unexecuted P01/P02 task.
  Exact-commit acceptance, publication and hosted acceptance are not assessed.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Bounded minimum and parent forwarding | Reconciled | Main/module default 0 and bounds 0..4, exact forwarding and all three examples present. |
| P01 / P01-T02 | Documentation and existing regression contracts | Reconciled | README and both existing tests match the new API contract; separate resident scale remains unchanged. |
| P02 / P02-T01 | Scoped offline validation | Reconciled | Complete markers agree with phase index, completion evidence, changes and recorded 447-test result. |
| Critique Disposition | PC-001 rejected as worker-local | Reconciled | Original Revise retained; parent-specific storage boundary and TMPDIR instructions are explicit. |
| Follow-Up Items | Later authorized publication gate and exact-head assessment | Reconciled, open | Mirrored in changes and state blocker; remains outside active implementation acceptance. |
| Handoff / Remaining Work | One Review and local commit | Reconciled at review entry | Review is now complete in this record; parent owns state/closeout and local commit. Prior artifacts are intentionally not rewritten here. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/main.bicep; infra/modules/containerapps.bicep | Add bounded integer apiMinReplicas default 0; forward to the API scale minimum, allowing explicit 2. | Complete diff shows exact parameter forwarding and no other resource-body modification. | Recorded compiled schemas and expression evaluation for 0/1/2/4. | Conformant. |
| P01-T01 | infra/main.bicepparam; infra/main.test.bicepparam; infra/main.pilot.example.bicepparam | Explicit 0 in each committed example, independent of production security profile. | Each diff adds only the requested parameter assignment. | Recorded build-params assertions consume full compiled JSON. | Conformant. |
| P01-T02 | infra/README.md | Update date, environment table, range, cold-start caveat and private production override; remove stale fixed-two wording. | Documentation distinguishes API scaling from other costs/workloads and retains standalone isolation. | Direct diff/Markdown review. | Conformant; no observed savings, latency or availability claim. |
| P01-T02 | infra/tests/test_bicep_policy.py | Add two methods for compiled schemas/forwarding and examples; update obsolete hardcode assertion and strengthen invariants. | Existing helpers evaluate the actual compiled forwarding and scale expressions. No test method removed. | Recorded offline discovery and changed-file Ruff pass. | Conformant with locked test ownership and two-method addition limit. |
| P01-T02 | infra/tests/test_resident_demo_deploy.py | Rename/update stale main-stack assertion without weakening resident separation. | Existing no-main/wrapper resident wiring assertions and standalone exact 0..1 scale check remain. | Recorded offline discovery and changed-file Ruff pass. | Conformant; renamed method is retained coverage, not removed coverage. |
| P02-T01 | Canonical plan, details and changes | Reconcile completion, prerequisite failures, successful validation and publication limit. | P01/P02 markers, phase index and state agree at review entry. | Parent evidence accepted as recorded, not independently rerun. | Conformant for local scope only. |

The complete source diff preserves API maximum 4, HTTP concurrency 50, probes,
authentication, ingress, security profiles, agent minimum 0/maximum 5 and all
jobs. The only modified workload property is the API minimum expression.
Standalone resident infrastructure, wrappers and runtime sources are unchanged.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01 / validation storage | Select task-owned session-files TMPDIR and conditional isolated pip venv. | PC-001 imported its worker's external-storage restriction; parent explicitly identified that restriction as inapplicable to its execution environment. Missing imports and Ruff then triggered permitted pip setup. | Plan disposition, phase instructions, changes and state consistently describe the boundary and actual validation. | Original critique Complete / Revise preserved; parent Ready after explicit rejection. | Justified execution clarification, not a functional divergence or unsupported extension of worker authority. |
| P01/P02 completion | Mark implemented tasks complete after scoped checks. | Recorded 447-test success, 24 build/lint successes and changed-file Ruff pass. | Plan markers, detail index/completion and changes agree. | No material design revision requiring fresh planning or critique. | Reconciled. |
| Publication follow-up | Keep complete-gate work distinct from component validation. | Confirmed no-full-gate scope conflicts with mandatory infrastructure publication policy. | Research C8, plan follow-up, changes blocker and state agree. | No bypass or readiness upgrade. | Correct residual-work separation; RV-001. |

## Critique and Material Revision Assessment

* Latest critique is the sole original critique, execution Complete and verdict
  Revise, with PC-001 as its only finding. That historical verdict is not
  changed to Pass by this Review.
* PC-001 has an explicit planning-parent disposition and rationale in the
  canonical plan. The supplied parent boundary permits its task-owned
  session-files storage. A restriction applicable to the critique worker does
  not automatically constrain the parent. Conversely, this review worker's
  narrower storage/write restrictions remain binding on this reviewer; no
  parent validation or storage operation was repeated here.
* TMPDIR routing is reflected in phase details and successful-validation
  evidence. The earlier conditional-pip requirement is preserved: dependency
  installation followed actual missing-package failures, with no uv or
  dependency-manifest changes.
* No significant or divergent functional decision emerged during
  implementation. Bounds, explicit examples, production opt-in and unchanged
  other infrastructure all follow the accepted plan and owner intent.
* Dependent-work pause assessment: current artifacts record the disposition
  and Ready state before implementation continuation; no contrary evidence
  requires a planning route. This is artifact reconciliation, not independent
  reconstruction of every historical execution step.
* Material revision readiness: no unresolved material revision or decision
  gap; no new critique or planning cycle is required for this bounded source
  change.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Complete publication gate, exact-head assessment and push/PR | Full gate is explicitly excluded now but mandatory for infrastructure publication. | Parent/owner under a later authorized publication scope. | Open, correctly mirrored in changes/state; distinct publication follow-up RV-001, not a source defect or added P02 task. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Publication remains ineligible without mandatory complete-gate evidence

* Related scope: plan Follow-Up Items and publication acceptance, not P01/P02
  source implementation.
* Evidence: src/README.md, Local RPI gate; canonical research C8; plan
  acceptance criteria and Follow-Up Items; changes Blockers and Follow-Up
  Items; state publication-full-gate blocker. Current candidate is also
  uncommitted at the review boundary.
* Impact: the 447 offline tests, 24 Bicep build/lint checks and changed-test
  Ruff evidence establish scoped local validation only. They do not authorize
  push, PR creation, exact-head acceptance or a hosted acceptance claim.
* Destination: distinct follow-up, authorized publication readiness; parent
  and owner own this route. No rpi-implement, rpi-plan or rpi-research
  invocation is warranted for a defect or gap in the current implementation.
* Smallest useful next action: finish the authorized local commit with dated
  original evidence and this Review, then stop before push/PR. Under a later
  scope explicitly authorizing the full gate, fetch main, run the complete
  gate against the committed candidate and reviewed base, retain its external
  receipt, verify against current origin/main immediately before publication,
  and obtain the required independent exact-head assessment and hosted/human
  gates. Changes to candidate/base/inputs invalidate earlier gate evidence.
* This is residual publication work, not a source defect and not permission
  to run the excluded gate now. A later exact-head publication assessment is
  distinct from repeating this single RPI Review.

Severity summary: Critical 0; High 0; Medium 1 residual publication finding;
Low 0. No implementation defects, unaccepted decisions or material research
gaps found in the supplied review boundary.

## Defects

* None found. No corrective source implementation is routed.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct publication follow-up | Parent/owner; local commit now, later authorize mandatory gate before push/PR. | Existing out-of-scope publication dependency, not an implementation defect. |

Later implementation of any future routed finding does not require this
Review to run again.

## Residual Work

* RV-001 retains the existing publication follow-up without adding active plan
  scope. No full receipt, current-origin-main verification, independent
  exact-head acceptance, hosted checks or human approval is claimed.
* Cold-start latency, actual cost and live availability are unmeasured by
  design. README warns appropriately; no additional research or deployment
  is required for this local task.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active implementation markers: none.
* Parent continuation: record this one Review result, reconcile parent-owned
  closeout/state and commit the source plus dated evidence locally.
* Publication blocker: RV-001; push/PR remain blocked while the complete gate
  is unauthorized and absent. Do not waive it or substitute component checks.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Initial offline discovery using system Python | infra/tests | Failed: prerequisites | Changes preserve 362 tests with 10 import errors from missing zava_forward distributions. |
| Initial Ruff invocation | Changed tests | Failed: prerequisite | Changes preserve missing ruff rather than recasting it as a source defect. |
| Conditional isolated pip setup | Parent task-owned environment | Recorded completed | Missing prerequisites addressed after failure; no manifest change or uv use recorded. Reviewer did not install or inspect secrets. |
| REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q | Complete offline infra suite | Passed, parent-run | 447 tests in 94.791s, OK and no skips. Reviewer directly corroborated final log tail supplied by parent; did not rerun suite. |
| az bicep build --file ... --stdout; az bicep lint --file ... | All 24 infra entry points/modules | Passed, parent-recorded | Changes record successful build/lint without diagnostics. |
| Existing compiled main/module/parameter-example tests | Schemas, forwarding, values and preservation | Passed, parent-run | Included in 447 tests; independent source inspection confirms actual compiled-expression coverage. |
| python -m ruff check and python -m ruff format --check, exact selectors in changes | Two changed Python tests | Passed, parent-recorded | Existing lint/format rules passed. |
| git diff --check | Complete tracked source diff | Passed, independently run | No whitespace errors. |
| Interrupted parameter-output probe | Earlier exploratory stdout probe | Interrupted, superseded | BrokenPipeError honestly preserved; final tests consume complete JSON. Not counted as a passing probe. |
| Live Azure what-if, deployment and secret access | Cloud/live state | Not run | Explicit exclusions; offline fake CLI fixtures are not cloud evidence. |
| Complete local gate and receipt verification | Publication matrix | Not run, blocked by scope | Mandatory before publication; RV-001. |
| Exact-commit, hosted and human acceptance | Publication/merge | Unavailable at review boundary | Uncommitted working candidate; not claimed. |

The parent-run discovery log was supplied from its task-owned session-files
area outside this worktree. Canonical workspace-relative evidence is the
changes record. Build/lint and Ruff results are accepted as recorded parent
evidence, not represented as independently repeated checks.

## Outcome

* Outcome: Residual work.
* Local source assessment: Conformant with owner requirements and accepted
  plan; no source defects found.
* Rationale: the single review completed and P01/P02 are fully reconciled,
  but the requested eventual publication remains blocked by the separately
  recorded mandatory gate. The justified PC-001 execution-boundary
  disposition does not alter functionality or waive publication requirements.
* This outcome does not establish exact-commit, deployed-state, hosted or
  human acceptance.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement correction required. |
| Decision gap or invalid assumption | None | PC-001 disposition supported for parent boundary; no rpi-plan route. |
| Material evidence gap | None for local scope | No rpi-research route; live measurements excluded. |
| Residual publication work | Distinct follow-up RV-001 | Parent/owner authorize complete gate later; keep push/PR blocked now. |

* Execution status: Complete.
* Outcome: Residual work; local source conformant.
* Validation coverage: 447 offline tests without skips, 24 Bicep build/lint
  successes and two-file Ruff pass recorded; independent full-diff inspection
  and diff whitespace check complete.
* Blockers: publication only; no review or source-implementation blocker.
* Parent handoff: continue local commit/closeout, not another RPI Review.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md](.copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md) | Research C1-C9 and scope. |
| [.copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md](.copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md) | Completed markers, disposition and follow-up. |
| [.copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md](.copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md) | Phase contracts and completion evidence. |
| [.copilot-tracking/reviews/plans/2026-10-27/aca-api-min-replicas-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/aca-api-min-replicas-plan-critique.md) | Original Complete / Revise critique. |
| [.copilot-tracking/changes/2026-10-27/aca-api-min-replicas-changes.md](.copilot-tracking/changes/2026-10-27/aca-api-min-replicas-changes.md) | Source changes and exact validation selectors. |
| [.copilot-tracking/rpi-sessions/2026-10-27/aca-api-min-replicas-state.json](.copilot-tracking/rpi-sessions/2026-10-27/aca-api-min-replicas-state.json) | Parent entry state and publication blocker. |
| [.copilot-tracking/reviews/logs/2026-10-27/aca-api-min-replicas-review.md](.copilot-tracking/reviews/logs/2026-10-27/aca-api-min-replicas-review.md) | This single independent Review. |

## Next Steps

The active parent should persist this result, finish authorized local
commit/closeout and stop before push/PR. Keep RV-001 as the distinct later
publication follow-up. No source fix, additional RPI stage or repeated Review
is requested.

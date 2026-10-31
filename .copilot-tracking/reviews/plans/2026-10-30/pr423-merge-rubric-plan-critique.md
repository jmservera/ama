---
title: "RPI Plan Critique: PR423 merge and rubric diagnosis"
description: Single independent final-candidate assessment of preservation, rubric repair and local validation constraints
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: pr423-merge-rubric-2026-10-30
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/pr423-merge-rubric-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/pr423-merge-rubric-phase-details.md
* Critique execution status: Complete
* Critique count: One final-candidate assessment; no repeat critique requested.

## Inputs and Criterion Boundary

* Caller requirements: full ordered RPI; merge origin/main into docs/demo-transport-plan-360-fix without rewriting either history or silently losing content or decisions; retain DN1-DN4, existing tests and documents; current main implementation/src migration outranks stale proposals. Diagnose the actual D1 extra evidence2 defect in hosted run 40556907743. No Azure operations, deployment, sign-in, secrets, warming, other existing worktree access or push.
* Reviewed inputs: the supplied plan, phase details and research; repository case-study original/addendum, reference index and owner memory; named adapter/preflight tests and adapter; named infrastructure documentation/tests; and the supplied main and merge-preview objects.
* Pinned references: reviewed main 5634f9a077d175a931c15e3400114665d8c071ee; original branch head 4696866850f230238617c95b0dbd4297f7e8b245; supplied merge-preview tree cdb205605c4ecd7c0439aa987c159dfc7e5af2ba. All object inspection occurred through this worktree's repository, not another checkout.
* Decisions and dependencies: merge rather than rewrite; preserve DN1-DN5 as already scoped; two added D1 rejection parameter cases total in existing adapter/preflight tests, none removed; no prompt, generated lock, scoring-contract, threshold or grade changes; local commit later with Refs #360 and Copilot trailer; independent original Review before candidate/evidence commit; full gate and external exact-head evidence remain separate from hosted/human approval.
* Assessment boundary: credibility and completeness of the supplied implementation/validation plan. This critique does not merge, implement, run application tests, reproduce the hosted submission, approve live operation or certify the future candidate.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI and one critique | Covered | Research precedes this candidate; implementation waits for critique disposition; original independent Review is planned. |
| AC1, AC2, C1, C7-C10, P01-T01 | Partial | Merge ancestry and named conflict/semantic targets are appropriate; explicit two-sided content/test preservation evidence is missing, PC-001. |
| DN1-DN5 and main implementation precedence | Covered direction; partial proof | Preserve private Blob decisions and historical proposals with dated supersession, without restoring mvp; PC-001 supplies the missing verification boundary. |
| AC3, C2-C6, W1-W2, P01-T02 | Covered | Exact D1 evidence2 rejection at adapter and existing jq preflight; existing valid controls retained; only two new parameter cases and no scoring changes. |
| AC4 and evidence integrity | Covered | Invalid submission has no score; removing evidence2 is only a counterfactual 77-versus-77 replay; actual baseline and unavailable live/panel/publication proof remain distinct. |
| P02-T01, AC5, C9 | Partial | Existing relevant suites, offline Bicep, lint/types/migration and full gate are identified; runtime scratch-path restriction conflicts with the supplied runner, PC-002. |
| P02-T02 and Review disposition | Partial | Preserve one original Review and adverse outcomes, but blanket routing to follow-up omits blocking-finding handling, PC-003. |
| Exact-head receipt and publication constraints | Covered direction | Commit original evidence first, external output, no false success on failure, later commits invalidate evidence; final current-main verification remains coordinator-owned. PC-002 prevents a prohibited attempt. |
| AC6 and change budget | Covered | Privacy-safe local identity, required reference/trailer, no push/cloud activity and no removed tests are explicit. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 1 Medium, 0 Low.
* Rationale: The rubric diagnosis and bounded implementation are credible. Before implementation, make preservation objectively checkable, reconcile the full-gate command with the actual runtime prohibition, and distinguish blocking Review findings from deferrable residual risks. These are direct planning corrections, not requests to change owner decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Ancestry and passing suites do not prove two-sided preservation

* Related IDs: AC1, AC2, C1, C7-C10, P01-T01, P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-30/pr423-merge-rubric-plan.md requires both histories' docs/tests intact but offers ancestry, conflict resolution and existing suites as the completion evidence. .copilot-tracking/details/2026-10-30/pr423-merge-rubric-phase-details.md names the role matrix, Blob writer, worker namespace and workflow hash without defining a two-parent content comparison. The supplied merge-preview object combines changes in storage, RBAC, worker/controller, Docker context, infrastructure tests, CI and gate tooling. The original-head-to-main histories differ across substantially more paths than the four textual conflicts.
* Concern: Both commits can be ancestors while a resolution drops source, tests, log entries or decision text. A suite can pass after its assertions or cases disappear. "Tests and docs intact" is not yet a reproducible acceptance check, particularly where old tag assertions must legitimately yield to Blob behavior and main's current implementation.
* Impact: An apparently successful merge could silently lose the owner's decisions or main functionality while still satisfying the listed ancestry/test checks.
* Smallest useful change: Add a bounded preservation checklist against both pinned parents, scoped to differing/overlapping integration paths and original evidence. Record both ancestry checks; review resulting diffs against each parent; account for unexpected deletions and test/function/assertion losses; compare both appended log ranges and historical RPI evidence; and map DN1-DN5 to retained authoritative text/implementation or explicit dated supersession. Name the existing role-matrix, Bicep, profile-bound Blob, Docker-context and namespace/migration selectors used to validate the semantic merge. Account explicitly for the src-ci fingerprint and all expected combined gate lint/type entries. Do not add tests or expand the two-case budget for this check.
* Action owner: Planning parent specifies the checklist; implementer records its results in the changes artifact.
* Exact resolving evidence: Revised P01-T01/P02-T01 and AC2 require a two-parent preservation ledger, including the four conflict resolutions, unchanged original evidence/log sequences, accounted test differences and existing semantic selector outcomes. The eventual changes artifact records actual checks/results and explains every intentional supersession; ancestry alone is not accepted as content proof.
* Decision route: Direct planner correction. Main implementation precedence and preservation of historical decisions are already owner-selected; no user decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The planned full-gate attempt would use a prohibited fixed scratch path

* Related IDs: AC5, C9, P02-T01, P02-T02, full-gate prerequisite risk.
* Evidence: The supplied main version of src/README.md documents a shared /tmp/ama-rpi-heavy.lock. The supplied merge-preview version of tools/rpi-checks.py still sets that absolute path in acquire_heavy_lock. P02-T02 unconditionally schedules python3 tools/rpi-checks.py --all with an external output placeholder. The active runtime instructions prohibit file operations in /tmp or temporary directories.
* Concern: Selecting a different --out directory or setting TMPDIR does not relocate an absolute lock path. Therefore the proposed command cannot be treated as an authorized attempt in this execution environment. Existing targeted tests also use tempfile helpers, so their scratch configuration must be checked before execution rather than assuming that synthetic/offline means path-compliant.
* Impact: Implementation could violate a hard execution constraint while trying to satisfy AC5, or misleadingly describe a never-authorized full command as an ordinary missing-tool failure.
* Smallest useful change: Add an explicit pre-execution path prerequisite. Record the stock full gate as blocked by its fixed lock path unless an already-supported, compliant execution route is demonstrated. Do not execute it, weaken the gate, change scoring/tooling outside scope, or substitute a partial receipt. Configure permitted task-owned scratch for eligible targeted tests, with no dirty candidate inputs. Amend AC5 to distinguish a command actually attempted from a pre-execution blocked command, and preserve the blocker for coordinator handoff.
* Action owner: Planning parent corrects the plan; implementer records the pre-execution blocker and only runs permitted validation; coordinator owns any later authorized full-gate execution.
* Exact resolving evidence: Revised P02-T01/P02-T02 and AC5 name the fixed-path incompatibility, identify permitted scratch/output handling for runnable checks and explicitly retain full-gate Blocked status if unresolved. A compliant complete run still requires its own new external receipt bound to the committed candidate, reviewed/current base and unchanged tools/images; no receipt or success is inferred from this critique.
* Decision route: Direct planner correction under the current restriction. No user response is needed to report Blocked. Any later broader tooling change or execution authorization is separate work, not presumed permission here.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Blanket follow-up routing does not distinguish blocking Review findings

* Related IDs: P02-T02, AC1-AC5, ordered RPI completion and no-push handoff.
* Evidence: .copilot-tracking/plans/2026-10-30/pr423-merge-rubric-plan.md says "Route any residual findings to follow-up rather than repeat Review." The phase details require the original Review and transparent gate disposition but do not define what happens when Review finds a preservation, regression or evidence-integrity violation.
* Concern: Maintaining one original Review is appropriate, but routing every finding to follow-up can mark the requested local repair complete even when its own acceptance criteria are broken. A local commit or green deterministic check does not resolve an adverse independent finding.
* Impact: The handoff can blur an accepted candidate, a locally committed but unaccepted candidate, and genuinely deferrable live/hosted risks.
* Smallest useful change: Require a finding-disposition table distinguishing scope/acceptance-blocking defects from genuinely deferrable residuals. For blockers, correct within authorized scope with targeted validation while preserving the original Review, or stop and hand off as Not accepted/Blocked if correction or required independent acceptance is unavailable. Do not schedule another critique or silently override the original Review; the one-Review rule does not confer acceptance.
* Action owner: Planning parent specifies the disposition rule; implementer records original finding IDs, corrections/evidence or explicit unresolved blockers.
* Exact resolving evidence: Revised P02-T02 completion text and later changes/handoff artifacts retain the original independent outcome, identify each blocking finding and its status, and never describe unresolved AC1-AC5 violations as accepted completion. Deferred live/panel/publication evidence remains separately unavailable without fabricated results.
* Decision route: Direct planner correction. The owner has not authorized bypassing acceptance; no user response is required for honest blocked handoff.

## Strengths and Residual Risk

* The supplied research identifies an extra evidence2 field in D1, not a missing change_reason. Adapter source confirms exact-key enforcement; the existing jq preflight already covers this schema shape generically.
* Two precise parameter additions using existing valid controls are sufficient for the scoped regression. No adapter relaxation, prompt/generated-lock edit, scoring modification or artificial scorecard repair is warranted.
* The 77 counterfactual is explicitly diagnostic rather than a new assessment. Open A1/A3/A5 already being at 5 gives no evidence-backed numerical uplift from this infrastructure documentation work.
* The plan preserves the distinction between current Blob decisions, superseded tag design and unverified production behavior. Main's IoT/release/current src work is not to be rolled back to satisfy a stale proposal.
* Hosted model compliance, live private transport, production position sizes/action names, signed attestation and human/panel/publication acceptance remain unavailable. Local evidence cannot establish them.

## Questions or Blocking Evidence Gaps

* No unresolved owner choice is needed for these revisions.
* Full-gate execution is blocked by the documented fixed-path conflict in this runtime unless a compliant already-supported route is demonstrated. Reporting that blocker is permitted; bypassing it is not.

## Limitations

* This is one complete assessment of the supplied candidate boundary. It is not a second research pass or a future exact-head independent Review.
* The external safe-output/context files were not read or re-downloaded. Their hashes, run attribution and replay results are research-supplied evidence, not fresh reproduction by this critique.
* No merge, application/test execution, gate execution, cloud operation, dependency installation, commit or push occurred. No other existing worktree was inspected.
* Only the caller-specified critique artifact is written; plan, details, research, source and original review records remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the two-parent preservation checklist and resolving-evidence requirements, then disposition PC-002/PC-003 directly in the same plan/details revision.
* User response required: No.
* Do not request another critique. Preserve this original Revise verdict and record each finding's disposition before entering implementation.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/pr423-merge-rubric-plan.md](.copilot-tracking/plans/2026-10-30/pr423-merge-rubric-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/pr423-merge-rubric-phase-details.md](.copilot-tracking/details/2026-10-30/pr423-merge-rubric-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-30/pr423-merge-rubric-research.md](.copilot-tracking/research/2026-10-30/pr423-merge-rubric-research.md) | Supplied integration and rubric evidence |
| [.copilot-tracking/reviews/plans/2026-10-30/pr423-merge-rubric-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/pr423-merge-rubric-plan-critique.md) | Original single critique and complete finding set |

## Next Steps

The active planning parent directly revises and dispositions PC-001 through
PC-003, finalizes without another critique, and continues the ordered RPI loop
only within the retained constraints. No user action is required. Full-gate
or Review blockers must remain explicit in the local coordinator handoff;
this critique authorizes neither a prohibited command nor publication.

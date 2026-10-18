---
title: Issue 108 evaluation run accounting plan critique
description: Single independent final-candidate assessment at the supplied base
ms.date: 2026-10-18
---

## Metadata

* Task ID: 108
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-108-evaluation-runs-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-108-evaluation-runs-phase-details.md
* Critique execution status: Complete
* Verdict: Revise
* Assessment count: exactly one independent final-candidate critique
* Branch: fix/evaluation-run-accounting-108
* Verified HEAD and supplied base: 69091f4149f2fd217fc33a8c965ebcb6d5064956
* Source correction allowance: at most two cycles; this planner correction does not require a source correction.

## Inputs and Criterion Boundary

The supplied plan, details, research C1-C7 and baseline log define the bounded
engineering objective. The caller requires actual returned per-priority-run
identity and both latencies, separate run/scenario accounting, mixed-source
orders, template-only and five-output regressions, one scripted reviewer action
per scenario, unchanged critical/citation gates and explicit final-only legacy
quality. Provider-call accounting and actual-model, held-out, human or benefit
approval are excluded. Parent #104 is hierarchy only; issue dependencies are
None.

The assessment read the relevant ai_eval.py implementation and existing focused
tests, Store recommendation construction, Ai.run fallback behavior, API report
consumer/negative controls, agents README, agents quality configuration and
existing CI commands. It also inspected the frozen golden scenario definitions,
the PRD model-evaluation/RAI/real-inference boundaries, and the required case-study
and knowledge-base orientation material. No private inputs, services, remote
research, inference, deployment or nested agents were used.

This is a plan credibility assessment, not implementation validation or issue
acceptance. It covers P01-P03, their tasks, acceptance criteria, dependency order,
test ownership/budget, evidence preservation and publication/review boundary.
The candidate already resolves the design choices; the remaining finding is a
direct execution-safety correction, not a significant or divergent decision.

### Supplied input fingerprints

| Input | SHA-256 before critique |
| --- | --- |
| .copilot-tracking/plans/2026-10-18/issue-108-evaluation-runs-plan.md | fb6feea7042c79924cb3bf4044267bfdaa64619ede3a88c4247fa9aff0d1db61 |
| .copilot-tracking/details/2026-10-18/issue-108-evaluation-runs-phase-details.md | 8ff9c1ddb0068a588c9e7245bad9611dfa8501ae29d2cb4958a1c47b6f15886d |
| .copilot-tracking/research/2026-10-18/issue-108-evaluation-runs-research.md | 39905b6e9ee58611cedb9749d6e9a3ee8be2dff4b6adb9a0f182a06a29006bca |
| .copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-baseline.log | c6937e4e8a973cd729bdb0f618300ae743584028ceb02f75074f4c22ab921a50 |

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Per-run identity and both latencies; C1/C2/C4; P01-T01/P02-T01 | Covered | Ordered returned recommendation evidence exists before the comparator; candidate preserves exact source/model/prompt, ordinal, recommendation ID and distinct latency meanings. Mutated returned metadata tests distinguish observation from reconstructed identity. |
| Distinct denominators and aggregate identity sets; C2/C5; P02-T01 | Covered | All priority run records drive source counts and sets; scenario membership overlaps for mixed sources. Provider calls, text tasks and the extra comparator are explicitly excluded. |
| Mixed orders, unknown identity, template-only, five outputs; C4/C5; P01-T01 | Covered | Both valid/fallback orders, repeated template cases and varying/null returned metadata are required. Five outputs must yield five AI records and distinct recommendation IDs, not one final-source scenario. |
| Full golden reconciliation; C5; P03-T01 | Covered | Frozen definitions contain ten priority scenarios and fourteen repetitions. Supplied baseline identifies eight AI/six template results, eleven total report results and ten reviewer actions as the intended repaired reconciliation. |
| Final-only quality and compatibility; C2/C3/C6; P01-T01/P02-T02 | Covered | Final overlap/Spearman/recall and existing arrays/variation remain compatible; JSON and README must disclose the final-only scope. ai_runs changes meaning visibly rather than silently multiplying final sources. |
| Failure and authority gates; C3/C6; P01-T01 | Covered | Existing code checks every repetition for critical misses/citations and preserves ranking/state/review controls. Planned early-miss/later-valid negative control supplements retained API citation/authority controls. No new threshold or gate policy is proposed. |
| Scripted reviewer identity and binding; C3; P01-T01/P02-T01 | Covered | One final-draft action is preserved and gains actual scripted-owner/final-recommendation binding. Summary counts/reasons remain compatible; no participant-effectiveness claim follows. |
| Direct consumer and bounded ownership; C6/C7; P02-T02 | Covered | Existing manager-only API report passes evaluation through. One direct assertion block and a narrow README change suffice; seven focused methods maximum, no removals or fixture-byte changes. |
| Offline isolation and allowed file locations; P01-T01/P03-T01 | Partial | Empty inherited endpoints/credentials are specified, but env -i omits the explicit permitted temporary root needed by existing tempfile consumers. PC-001. |
| Existing validation and tool exemptions; C7; P03-T01 | Covered | Focused red/green, agents discovery, configured Ruff/format/mypy, focused API controls, actual JSON CLI reconciliation and receipts are planned. Migration exemptions are explicitly disclosed, not strict harness-check claims. |
| Dependencies, correction/review/publication gates; P01-P03/P03-T02 | Covered | Regression lock precedes implementation; local evidence precedes one original independent Review and publication. Original adverse evidence is immutable; at most two correction cycles, no second original Review, no unilateral integration. |
| PRD RAI/model-evaluation/CON-009 claim boundary | Covered | Offline scripted repair remains partial engineering. Actual serving/version, labels/held-out study, humans, Finance, region/quota and platform acceptance remain unmet rather than becoming dependencies for this repair or fabricated approvals. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The accounting design and bounded regression ownership are credible.
  One explicit environmental requirement is missing from the validation recipe:
  clearing the environment without a permitted TMPDIR does not keep existing
  tempfile writes inside the project. Correct this before executing P01 or P03.
  The adverse verdict remains part of this original artifact even after direct
  planner disposition.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Isolated validation omits the permitted temporary root

* Related IDs: P01-T01, P03-T01; task-local-store requirement; hard prohibition on file operations in /tmp, /var/tmp or other temporary directories outside the permitted project location.
* Evidence: .copilot-tracking/details/2026-10-18/issue-108-evaluation-runs-phase-details.md, P01-T01 requests tempfile stores and P03-T01 specifies env -i with PATH, session-local HOME and optional test-only PYTHONPATH, but no permitted temporary root. src/agents/src/zava_forward/agents/ai_eval.py imports tempfile and run_eval creates TemporaryDirectory contexts for every priority scenario and text-task checks. src/api/tests/test_ai_tasks.py, Endpoints.setUp also uses tempfile.TemporaryDirectory().
* Concern: HOME does not select Python's temporary directory. Under the stated cleared environment, default tempfile discovery can select /tmp; any inherited TMPDIR is removed. The proposed tests and actual CLI can therefore violate the explicit file-location boundary despite using constructed inputs and task-local Store instances. This is an execution-recipe gap, not an observed write by this critique.
* Impact: The required red/green and final harness evidence could require prohibited writes or fail under runtime enforcement before the accounting behavior is tested. Repeated retries or a source-level rewrite of tempfile consumers would be unnecessary.
* Smallest useful change: Have the planning parent specify one writable task-owned scratch directory beneath this worktree and explicitly pass its absolute path as TMPDIR in every env -i test/application command, including red baselines and the JSON CLI. Require that directory to exist before execution, verify Python resolves its temporary root there, and clean task scratch data without deleting evidence. Do not change application behavior, add test methods, touch fixtures or expand the scope.
* Action owner: Planning parent for P01-T01/P03-T01 disposition and command recipe; implementer for executing that recipe.
* Exact resolving evidence: Updated plan/details explicitly bind all isolated application/test processes to the permitted project-local TMPDIR; subsequent validation logs include the exact isolated environment command and a tempfile.gettempdir() result resolving to that directory before any Store/harness run. No source change or new regression method is necessary.
* Decision route: Direct planner correction. Existing instructions already resolve the choice; no significant/divergent human decision or user response is required.

## Strengths and Residual Risk

* The canonical ordered run records address the demonstrated loss directly,
  rather than estimating repetitions from the final source.
* Returned template model labels remain evidence labels, not successful AI
  outputs or serving-version attestation. Unknown identities remain null in
  records while aggregate sets omit unknowns.
* Legacy quality remains deliberately final-recommendation-per-scenario;
  all-repetition safety/citation checks and the scripted reviewer denominator
  remain distinct. The plan explicitly accepts this limited quality scope.
* The frozen fixture, seven-method ceiling, single direct-consumer block and
  retained tests constrain scope without preventing the stated regressions.
* Actual-model/human/held-out/benefit and real-platform prerequisites are
  explicitly deferred. A passing offline report cannot accept issue #108,
  grant release authority or establish measured resident/business outcomes.
* Historical tool exemptions remain a disclosed residual checking limitation.
  The parent must not promote configured lint/type passes into comprehensive
  strict analysis of the exempt harness/tests.

## Questions or Blocking Evidence Gaps

* No decision-critical research gap or unresolved user choice was found.
* PC-001 requires a plan disposition before executing validation, not another
  research phase or a second critique.

## Limitations

* The supplied baseline log was read as historical evidence. Its six-test pass
  and environment/install narrative were not independently rerun in this
  read-only planning assessment; it does not contain full command transcripts.
  P03 already requires exact commands, exits, full failures and hash receipts.
* No source tests, imports of application modules, installs, CLI evaluation,
  server, SQL, inference or external service operations were performed.
* The golden JSON was parsed read-only to corroborate scenario/repetition
  definitions; no fixture or source was written.
* Supplied issue hierarchy/dependencies were assessed as caller-confirmed
  inputs; no remote issue/board mutation or additional research was performed.
* Only the caller-authorized critique artifact was written. Plan, details,
  research, baseline log and implementation sources remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: Planning parent.
* Smallest next action: Record direct disposition and specify/verify the
  project-local TMPDIR recipe for all isolated validation processes.
* User response required: No.
* Preserve this original Revise artifact and its hash. Finalize by direct
  planner disposition without another critique; implementation and the one
  original independent Review remain separate subsequent gates.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-18/issue-108-evaluation-runs-plan.md](.copilot-tracking/plans/2026-10-18/issue-108-evaluation-runs-plan.md) | Assessed final candidate, unchanged |
| [.copilot-tracking/details/2026-10-18/issue-108-evaluation-runs-phase-details.md](.copilot-tracking/details/2026-10-18/issue-108-evaluation-runs-phase-details.md) | Assessed execution boundaries, unchanged |
| [.copilot-tracking/research/2026-10-18/issue-108-evaluation-runs-research.md](.copilot-tracking/research/2026-10-18/issue-108-evaluation-runs-research.md) | Supplied C1-C7 evidence and alternatives |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-baseline.log](.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-baseline.log) | Historical baseline, unchanged |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-108-evaluation-runs-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-108-evaluation-runs-plan-critique.md) | Single complete independent critique and original verdict |

## Next Steps

The active planning parent should directly disposition PC-001, retain this
original adverse verdict/hash, and finalize the plan without a second critique.
No user action is required. This assessor stops after returning the artifact
and its SHA-256; no implementation or original Review is performed here.

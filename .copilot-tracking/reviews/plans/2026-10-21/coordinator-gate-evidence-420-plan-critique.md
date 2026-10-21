<!-- markdownlint-disable-file -->
# RPI Plan Critique: PR420 gate-evidence correction

## Metadata

* Task ID: 420-gate-evidence
* Critique date: 2026-10-21
* Plan: .copilot-tracking/plans/2026-10-21/coordinator-gate-evidence-420-plan.md
* Phase details: .copilot-tracking/details/2026-10-21/coordinator-gate-evidence-420-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: bounded correction of the false implication that the mandatory complete local RPI gate is waived (validation-01 line 29). Criteria: original history preserved, no claim the gate ran, scope limited, no source change. Launch clarification: the worker does not run the full gate, the coordinator owns it, no push.
* Research and evidence considered: .copilot-tracking/research/2026-10-21/coordinator-gate-evidence-420-research.md (C1 to C9); /tmp/brief-420-gate-correction-2113.md; /tmp/ama-wave-20261020-2113-common.md; lines 20 to 35 of .copilot-tracking/hve-builder/2026-10-20/coordinator-sonnet-55-validation-01.md (confirms line 29 row and line 31 verdict text).
* Decisions, dependencies, and acceptance criteria considered: plan User Decisions, Acceptance Criteria, P01 to P02 dependency, alternative A selection.
* Assessment boundary: plan and details credibility only. Research citations (C3 to C8) were not re-verified against the repository or PR metadata; the launch clarification is taken from the caller prompt, as it is not in either brief file.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Original history preserved | Partial | Alternative A edits validation-01 in place while the brief says not to overwrite original records; the guardrail is only implicit (PC-003). |
| No claim the gate ran | Partial | Exclusions stated, but P01-T02 records checks "run today" before P02 runs them, and no negative verification exists (PC-001). |
| Scope limited, no source change | Covered | Boundaries exclude agent source, author-01, review-01; diff versus f3e8a8f1 limited to tracking. |
| Gate stays coordinator-owned | Covered | P02 excludes rpi-checks.py --all, heavy lock, push. |
| P01-T01 | Covered | Row and verdict wording match C1, C2, C9 and the actual file lines. |
| P01-T02 | Partial | Sequencing defect (PC-001). |
| P02-T01 | Partial | Missing fetch and base recording, commit conventions and handoff content (PC-002). |

## Verdict

* Verdict: Revise
* Rationale: the approach (alternative A) is evidence-backed and scoped correctly, but the task order makes the correction record claim checks before they run, and the freeze task omits repository-mandated steps the coordinator needs to run the gate validly. All are direct planner corrections.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Correction record is written before the checks it must report

* Related IDs: P01-T02, P02-T01, Non-Functional Requirements (truthfulness)
* Evidence: plan P01-T02 expected result "records focused checks"; details P01-T02 "focused checks actually run today"; details P02 runs the checks after P01 and commits only after Review.
* Concern: validation-02 cannot truthfully list command results that have not yet run, and a Review finding could force edits after the record is written. No step greps the final files for gate-ran wording.
* Impact: risk of either a premature claim of execution or a second edit and drift between validation-02 and the changes record.
* Smallest useful change: split P01-T02 into drafting (original quote, falsity, corrected wording, boundary) and a P02 step that appends the executed checks with commands and results after they run and after Review, before the single commit. Add a P02 check: grep validation-01 and validation-02 to confirm the gate is described only as "not run" and that no receipt or pass is claimed.
* Action owner: planning_parent
* Exact resolving evidence: revised plan and details show the ordering; the final validation-02 lists each check with command and result matching the changes record; grep output is recorded.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Freeze task omits base recording, commit conventions and a complete handoff

* Related IDs: P02-T01, Acceptance Criteria (clean head frozen), C8
* Evidence: /tmp/brief-420-gate-correction-2113.md lines 8 and 10 (inspect fresh main and PR state before freeze; resolve email via gh api user; Conventional Commit and Copilot trailer); /tmp/ama-wave-20261020-2113-common.md lines 9 and 15 (record reviewed origin main SHA); .github/copilot-instructions.md gate paragraph (any later commit invalidates a receipt).
* Concern: C8 reflects a state at research time. P02-T01 only records HEAD; it does not require a fresh fetch of origin main, a recorded base SHA, the repository-local noreply email, a Conventional Commit message with the trailer, or no amend, rebase or fast-forward unless a genuine clean upstream commit exists. The handoff content is not defined.
* Impact: the coordinator may receive a head without the base SHA, or a commit that breaks identity rules, forcing an invalidating recommit before the gate.
* Smallest useful change: add to P02-T01 fetch origin main and PR420 metadata before commit, with the SHA recorded; commit with the gh-derived noreply email, Conventional Commit subject and trailer, with no amend; final report lists candidate HEAD, base SHA, artifact paths, focused checks, and states "full gate not run, no receipt, any later commit invalidates a receipt, no push".
* Action owner: planning_parent
* Exact resolving evidence: revised P02-T01 text and, at implementation, the changes record containing those values and a clean `git status`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: In-place edit of an original record lacks an explicit minimal-diff guardrail

* Related IDs: P01-T01, Acceptance Criteria (original wording preserved)
* Evidence: brief line 8 "Do not overwrite the pre-existing original HVE records to claim tests were run then"; details P01-T01 boundaries; validation-01 line 31 verdict also states "No source edits, commit, push, PR or delegation performed."
* Concern: the plan does not say the edit must touch only line 29, line 31 scope wording and one dated note, nor that the "No source edits..." sentence and the parent closure paragraph stay intact. "Preserved in Git history" depends on the diff being reviewable.
* Impact: a broader rewrite could blur the adverse static-only history.
* Smallest useful change: add a validation expectation that `git diff` of validation-01 shows changes limited to line 29, the verdict scope and the correction note, with other lines unchanged, and that the correction note is dated 2026-10-21 and says the original text is quoted in validation-02. Also update the plan's "Critique Disposition" from "Pending critique" once dispositioned.
* Action owner: planning_parent
* Exact resolving evidence: revised P01-T01 validation expectation; implementation diff stat for the file.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* The scope boundary, rejected alternatives and exclusion of agent source are evidence-backed.
* The launch clarification is applied consistently and the gate is explicitly handed to the coordinator, with no receipt claimed.
* Residual risk: the full gate has not run for this candidate and any later commit invalidates a receipt; this is accepted by the plan and owned by the coordinator.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Citations C3 to C9 and PR420 state were not independently re-verified.
* The launch clarification exists only in the caller prompt and the plan, not in the supplied brief files.
* Execution outcomes of P01 and P02 are not assessable at planning time.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: direct revision of plan and details for PC-001 to PC-003, then finalize without another critique
* User response required: no

<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-152-empty-queue-coverage-correction-2

## Metadata

* Task ID: issue-152-empty-queue-coverage-correction-2
* Critique date: 2026-11-09
* Plan: .copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-correction-2-plan.md
* Phase details: .copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-correction-2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: fix only the test_no_internal_terms_in_web_copy failure; no audit weakening or bypass; no behaviour change; focused tier; fail-before and pass-after evidence; lightweight checks only; old evidence untouched.
* Research and evidence considered: .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-2-research.md; src/api/src/zava_forward/api/web/app.js:462-463; src/api/tests/test_content_standard.py; src/api/README.md:3872. Read-only re-run of `python3 -m unittest tests.test_content_standard` from src/api at head 06954540e: 18 tests, 1 failure, the app.js line 462 violation only (not written to any artifact).
* Decisions, dependencies, and acceptance criteria considered: plan AC1-AC4, FR1, P01-T01..T03, Alternatives A-C.
* Assessment boundary: the logged coordinator failure at /tmp/ama-g152-c1-1109/0024-project-api.log is outside the workspace and was not read. Hosted CI and the coordinator gate are not assessable here.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Correct only this failure | Covered | Comment removal; module run shows no other audit violation. |
| No audit weakening or bypass | Covered | Alternative A rejected; test files untouched. |
| No behaviour change (FR1) | Covered | Comment-only; queue test and node --check planned. |
| Focused tier, lightweight checks | Covered | Heavy gates explicitly excluded; coordinator keeps them. |
| Fail-before / pass-after (AC1) | Partial | Fail-before is asserted as "already reproduced" but no durable record is planned (PC-001). |
| Old evidence untouched (AC4) | Partial | Verification command not specified (PC-002). |
| AC3 diff scope | Partial | Ambiguous against a commit that also adds tracking files (PC-002). |
| Critique disposition | Partial | Placeholder to be filled (PC-003). |

## Verdict

* Verdict: Revise
* Rationale: The approach is correct, minimal and compliant. Three small, planner-owned precision gaps weaken the evidence trail the caller asked for. None needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Fail-before evidence is asserted, not recorded

* Related IDs: AC1, P01-T02
* Evidence: plan AC1 and details P01-T02 ("failed before, reproduced at the candidate head"); the only logged failure is an external /tmp path.
* Concern: The plan gives no step that captures the fail-before run, with head SHA and exit code, in the changes file before the edit. Implementation could edit first and lose the red state.
* Impact: Weakens the caller's fail-before/pass-after requirement and relies on evidence outside the workspace.
* Smallest useful change: Make P01-T02 begin with a pre-edit run of the audit test at the unmodified head. Record the command, `git rev-parse HEAD`, exit code (non-zero) and the line 462 violation in the changes file. Then edit, rerun, and record exit 0.
* Action owner: planning parent (implementer)
* Exact resolving evidence: the changes file shows a pre-edit non-zero audit result naming app.js line 462 with the head SHA, followed by a post-edit exit 0 on a dirty-source tree.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: AC3 and AC4 lack concrete verification commands

* Related IDs: AC3, AC4, FR1
* Evidence: plan AC3/AC4; details P01-T02 lists only `git diff --check`.
* Concern: AC3 says the source diff is only two removed lines, but the commit will also add plan, details, research, changes and critique files. AC4 has no check that old artifacts and receipts are unmodified.
* Impact: A reviewer cannot mechanically confirm scope.
* Smallest useful change: Specify `git diff --numstat -- src` showing 0 added and 2 deleted for app.js alone, and `git show --stat --name-status HEAD` showing only app.js modified plus new-file additions under .copilot-tracking for correction 2 (no modified or deleted earlier files). Also state that the commit may include the tracked correction 2 artifacts.
* Action owner: planning parent
* Exact resolving evidence: those two outputs recorded in the changes file.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Critique disposition left as a placeholder

* Related IDs: plan Critique Disposition section
* Evidence: plan text "Dispositions are recorded below after it returns."
* Concern: Nothing is recorded below it. A final candidate needs explicit dispositions.
* Impact: Review cannot see which findings were applied.
* Smallest useful change: Record PC-001 to PC-003 as accepted and applied, and note the README line 3872 and the correction 1 test name containing "provenance" as unaudited and intentionally untouched (consistent with the research).
* Action owner: planning parent
* Exact resolving evidence: plan Critique Disposition table lists each PC ID with its disposition.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Removal is the smallest change and cannot reintroduce a banned term. The audit and tests are untouched.
* Running the whole content-standard module covers hidden violations in other audited files. I confirmed there is only one.
* Residual risk, accepted: the rest of the failed focused gate was not re-run and stays with the coordinator.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* The external /tmp failure log, hosted CI and the coordinator gate were not examined.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: apply PC-001 to PC-003 directly to the plan and details, then implement without a further critique.
* User response required: no

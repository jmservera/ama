<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-152-empty-queue-coverage-correction-1

## Metadata

* Task ID: issue-152-empty-queue-coverage-correction-1
* Critique date: 2026-11-09 (prospective, written before any source edit)
* Plan: .copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-correction-1-plan.md
* Phase details: .copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-correction-1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: keep coverage unknown without independent authority; no producer, schema, SQL, data, identity or permission change; focused tier; focused regression for stale/unrelated/unverified provenance; keep no-match, unknown, populated and all-cases behaviour; accurate README and tests; no AC-034/043 completion claims; no browser, SQL, Docker or changed gates.
* Research and evidence considered: .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-1-research.md (C1-C6, Alternatives A-D), plan and phase details above. Source files were not re-read; research claims about app.js, the test file and the README are taken as supplied.
* Decisions, dependencies, and acceptance criteria considered: plan AC1-AC5, FR1-FR3, P01 to P02 dependency, follow-ups F1-F3.
* Assessment boundary: plan credibility only. Whether the line references and test structure are as described is not independently verified.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Fail closed without independent authority (FR1, Alt D) | Covered | Removing the branch is the simplest safe result and needs no anchor; rejection of Alt A/B/C is reasoned. |
| No producer/schema/SQL/data/identity/permission change | Covered | Scope and non-goals exclude them; the change is client, test and README only. |
| Focused regression, AC1 | Partial | Fails-before proof may fail for the wrong reason (PC-001). |
| Preserve no-match, unknown, populated, all-cases (FR2, AC2) | Covered | Retained tests; byte-identical outputs required (P01-T01). |
| README accuracy (AC4, P02-T01) | Partial | Other doc or check surfaces and the unknown copy are not verified (PC-002). |
| No AC-034/043 completion claim | Covered | AC4 and the executive summary state partial evidence only. |
| Commit/identity/`Refs #152` requirement | Missing | No task owns the commit (PC-003). |
| Supersession of original artifacts | Partial | Original artifacts assert the declared state; correction needs a pointer (PC-004). |

## Verdict

* Verdict: Revise
* Rationale: The approach is sound and in scope, with no Critical or High findings. Four direct planner corrections are needed so the key evidence (regression fails before the change) is valid, removal is complete across surfaces, and the commit requirement has an owner.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Fails-before check can fail for the wrong reason

* Related IDs: AC1, P01-T02, P02-T02
* Evidence: phase details P01-T02 ("The Node extractor cuts only `queueEmptyExplanation`") and P02-T02 (run the new test against pre-change `app.js`).
* Concern: In the original source `queueEmptyExplanation` calls `trustedCoverage`. An extractor that cuts only the one function would raise a ReferenceError against the original, which counts as a failure but does not show the stale/unverified provenance yielding "declared-unrepresented". The new test must also call with the original signature (coverage and ctx) to exercise the defect, which the details only imply ("unchanged coverage input").
* Impact: AC1's claim that the regression reproduces the defect is not demonstrated, so a reviewer cannot trust it.
* Smallest useful change: Specify that the check runs the new test body against the original function plus `trustedCoverage` (for example via a temporary extractor argument or a copy of the original source from git), passing coverage and ctx, and records the actual returned state `declared-unrepresented` as the failure. State that the final test passes the same inputs to the new helper, which ignores them.
* Action owner: planning parent
* Exact resolving evidence: P02-T02 and the changes record show the pre-change run's assertion message (state `declared-unrepresented` versus expected `coverage-unknown`), not a ReferenceError.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Removal completeness is checked only by one token and one grep scope

* Related IDs: AC3, AC4, P02-T01, C5, C6
* Evidence: plan AC3 (grep for `declared-unrepresented` and `trustedCoverage` in `src`); research Risk line (grep of `src`, `tools`, `docs`); plan Dependencies and Risks (unrun Playwright checks).
* Concern: The declared-gap copy (user-visible wording quoting fixture and source) and `work_queues.coverage` references can survive in browser checks under `src/api/checks`, other README sections, docs or tracking text without containing the two tokens. The retained unknown copy also needs a check that it does not imply a declaration may appear.
* Impact: The unrun Playwright checks could assert the removed text and fail later at the coordinator gate, or documentation could keep an inaccurate active claim.
* Smallest useful change: Extend AC3 and P02-T02 to grep `src`, `tools` and `docs` (excluding `.copilot-tracking` originals) for the declared copy phrases, `coverage` under `work_queues`, `fixture_version` and `declared gap`; list any unrun-check hits in the changes record for the coordinator without editing out-of-scope files (or stop and reassess if a check asserts the removed text). Confirm the unknown copy wording is accurate with the branch removed.
* Action owner: planning parent (implementation phase executes)
* Exact resolving evidence: grep results recorded with zero active hits or an explicit coordinator hand-off list; unknown copy reviewed in the changes record.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: No task owns commit, identity and review-time guideline refresh

* Related IDs: User Decisions and Requirements, P02-T02
* Evidence: plan requirements (repository-local privacy-safe identity, Conventional Commit, `Refs #152`, co-author trailer, web-design-guidelines again before review, `file:line` report); the phase checklists end at validation.
* Concern: The requirements are stated, but no task or done condition covers them.
* Impact: Easy to omit; the instructions require them for the candidate.
* Smallest useful change: Add P02-T03: resolve identity via `gh api user`, set repo-local email, commit with `Refs #152` (not a closing keyword) and the trailer, record the SHA; note the guideline refresh and `file:line` report belong to the review step.
* Action owner: planning parent
* Exact resolving evidence: plan checklist contains P02-T03 and the changes record has the commit SHA and message.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Original artifacts still assert the declared state

* Related IDs: Parent task reference, C5, C6
* Evidence: plan Parent task row ("preserved unchanged") and User Decisions (preserve original Residual work review).
* Concern: Preserved originals describe the declared-gap behaviour as delivered; readers could take it as current.
* Impact: Possible stale-claim reuse in later review or in the PR description.
* Smallest useful change: In the correction changes record and the PR text, state that this correction supersedes the declared-state claims of the parent artifacts, without editing them.
* Action owner: planning parent
* Exact resolving evidence: the changes record includes a supersession statement naming the parent artifacts.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Removing the branch avoids an invented trust anchor and keeps focused tier, as the caller required.
* FR1 to FR3 and AC2 pin the preserved behaviours; scope exclusions are explicit.
* Residual risk accepted by the plan: loss of the future declared path (preserved in git history; owner decision F1); browser, `--changed`, independent review and hosted checks are left to the coordinator.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Source files, tests and README were not re-read; findings rest on the supplied research and plan. No checks were run.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: apply PC-001 to PC-004 directly to the plan and phase details, then finalize without another critique.
* User response required: no

## Related Artifacts

| Path | Description |
|---|---|
| [.copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-correction-1-plan.md](.copilot-tracking/plans/2026-11-09/issue-152-empty-queue-coverage-correction-1-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-correction-1-phase-details.md](.copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-correction-1-phase-details.md) | Phase details under critique |
| [.copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-1-research.md](.copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-1-research.md) | Supporting research |

## Next Steps

No user action is required. The planning parent applies PC-001 to PC-004 directly and finalizes. When dispatched by `rpi-plan`, return this verdict to the parent.

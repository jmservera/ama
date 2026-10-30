<!-- markdownlint-disable-file -->
# RPI Plan Critique: fictional-form-review-97-b6-rubric

## Metadata

* Task ID: 97-b6 (additional cycle 1 of at most 4)
* Critique date: 2026-10-23
* Plan: .copilot-tracking/plans/2026-10-23/fictional-form-review-97-b6-rubric-plan.md
* Phase details: .copilot-tracking/details/2026-10-23/fictional-form-review-97-b6-rubric-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: reviewer finding B6 (latest.json B6 rationale cites src/core/README.md 928-943, evidence cites the pitch brief and src/api/README.md:2555-2561). No hand edit of generated output, no spoofed evidence or approval, no weakened validation or gates, no push or PR update. Up to 4 extra cycles authorized.
* Research and evidence considered: .copilot-tracking/research/2026-10-23/fictional-form-review-97-b6-rubric-research.md (C1-C7), checked against .github/rubric/scores/latest.json, git show a74652aa and b22d8639, git show 572a80e0 and c158ab1e, .github/workflows/rubric-score.md, .github/rubric/scripts/gate.py, .github/rubric/README.md, git log and reflog, gh pr view 424, and a read-only pytest run of .github/rubric/scripts.
* Decisions, dependencies, and acceptance criteria considered: plan AC-1..AC-3, FR-1/FR-2, P01 and P02 tasks, critique disposition "Pending".
* Assessment boundary: no hosted run, force-with-lease, scorer dispatch or complete gate was executed. Claims about what a future push would trigger or produce are inferences from workflow text, not observed.

## Research claim verification

| Claim | Result | Note |
| --- | --- | --- |
| C1 mismatch in committed bytes | Confirmed | HEAD latest.json B6: evidence pitch brief 1-137 and src/api/README.md:2555-2561, rationale cites src/core/README.md:928-943. |
| C2 introduced by second bot commit | Confirmed, root cause understated | b22d8639 (rebased as 572a80e0) had core README 928-937 plus the test file. a74652aa (rebased as c158ab1e) changed evidence back to exactly the pre-existing main baseline B6 evidence (pitch brief and api README), kept the score at 4, and rewrote only the rationale. So the model re-emitted stale baseline evidence for an unchanged score. The research says "replaced" but does not note the evidence is the baseline value. |
| C3 workflow is sole writer | Confirmed | rubric-score.md triggers on pull_request, push to main and workflow_dispatch. dispatch force runs never update latest.json (README). |
| C4 gate.py accepts evidence for unchanged scores | Confirmed | gate.py lines 188-196: evidence is only checked against changed files when the score changes. Line range cited in research is slightly narrow (180-196). |
| C5 no manual-correction route | Confirmed for scripts and README; absence claim is by search only |
| C6 conflict-free rebase, one ms.date line removed | Confirmed | HEAD c158ab1e descends from origin/main f1e2d830, 9 commits ahead. origin/main last changed latest.json at 140d8f49. |
| C7 81 passed, 9 failed | Not reproduced | Read-only run of python3 -m pytest .github/rubric/scripts gave 21 failed, 324 passed, 7 skipped. Failures include test_gate, test_prepare, test_scorecard_adapter (KeyError 'total' or 'criteria', result probably carries an error) and 12 test_safe_output_runtime tracking-only trigger cases. The research command and filter are not recorded. |

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR-1 lineage preserved | Partial | Lineage verified, but rebase rewrote published PR 424 head a74652aa; publication consequence not planned (PC-002). |
| FR-2 B6 recorded as unresolved with options | Partial | Options (b) and (d) present, but (d) is not shown to fix B6 and (b) conflicts with repo guidance (PC-003, PC-005). |
| P01-T01 rebase | Partial | Done before plan existed; disclosure deferred "if the critique so requires" (PC-001). |
| P01-T02 verification | Covered | Reproduced. |
| P02-T01 record findings | Partial | Depends on C7 figures that do not reproduce (PC-004). |
| P02-T02 complete-gate plan | Partial | Missing author, force-with-lease, rubric test dependency, receipt directory choice (PC-006). |
| AC-1..AC-3 | Partial | AC-1 and AC-2 are weak or unverifiable as written (PC-007). |

## Verdict

* Verdict: Revise
* Rationale: The core conclusion is sound and verified: no legitimate deterministic fix exists, hand editing latest.json is forbidden, and the defect arises from the bot's second rescore. The plan must be revised before finalization because it conceals an ordering deviation, rests on a test-count claim that does not reproduce, does not flag that the rebase of a published branch makes any publication a history rewrite, and offers rescore options without showing that they would correct B6 or are permitted by repository guidance. All findings are direct planner corrections except one owner decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Ordering deviation is not disclosed as a fact

* Related IDs: P01-T01, plan Critique Disposition, FR-1
* Evidence: git reflog (rebase finished at c158ab1e), P01-T01 text "Done before this plan was drafted; recorded in changes as a ordering deviation only if the critique so requires"; the three planning artifacts are untracked and the rebase and pytest run (research C7) preceded them.
* Concern: The rebase and the rubric test run happened before the plan, details and critique existed. The plan makes disclosure conditional on this critique and phrases the research as an executed wave with "Planning Readiness: Ready". That reads as plan-then-execute while P01 is already complete, and P01 stays unchecked.
* Impact: Misrepresents RPI sequencing to the independent reviewer; the final receipt and Review would otherwise rest on an undisclosed deviation.
* Smallest useful change: State unconditionally in the plan (Executive Summary and P01-T01) and in changes that the rebase and the pytest run preceded plan authoring, give their order and results, mark P01 as already executed, and state that the plan and critique are not a gate for those steps. Note the rebase is reversible via reflog and that no source or score file was changed by it.
* Action owner: planning parent
* Exact resolving evidence: plan and changes record containing the ordering statement with reflog hashes (pre-rebase a74652aa, post c158ab1e) and the pytest result; "only if the critique so requires" removed.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Rebase rewrote published history and its publication consequence is unplanned

* Related IDs: FR-1, P01, plan User Decisions (preserve remote commits)
* Evidence: gh pr view 424 reports headRefOid a74652aa, draft, MERGEABLE; local HEAD c158ab1e shares no commit ids with it for the nine rebased commits (bot commits are 572a80e0 and c158ab1e); .github/rubric/README.md says to merge main and push "without rewriting history"; repository instructions say never silently rebase or force-push merely to manage lineage.
* Concern: PR 424 was already mergeable on a74652aa, and main's only relevant change was one line in artifacts.json. The rebase was not required, and the plan's "preserving remote commits" is true only of content, not of SHAs. Pushing HEAD needs force-with-lease, which the owner has not authorized, and it also re-parents both bot commits so the recorded scored "commit" fields no longer name SHAs on the branch.
* Impact: Plan silently commits the owner to a history rewrite or to discarding the rebase. FR-1 and AC-1 are claimed satisfied while the published and local histories diverge.
* Smallest useful change: Add an explicit statement that publication requires either owner-authorized force-with-lease or reverting the local branch to a74652aa and using a merge of main (repo guidance), and make that an owner decision with a recommendation (prefer reset to a74652aa then merge origin/main, since a rebase gave no benefit). Do not perform the reset in this cycle unless the owner approves.
* Action owner: planning parent states it; user (owner) decides
* Exact resolving evidence: plan section naming the decision and the default, and the owner's recorded answer before any push; git rev-parse of the final head recorded in changes.
* Decision route: significant or divergent user decision (history rewrite and push are outside current authorization)

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Option (d) is not shown to correct B6 and ignores why the evidence regressed

* Related IDs: C2, C4, FR-2, plan Executive Summary
* Evidence: git show 572a80e0 and c158ab1e on latest.json (B6 evidence reverted to baseline values); gate.py 188-196; .github/rubric/README.md lines 56-60 and 199-237 (one ordinary push is legitimate; repeated pushes and rescores are not a recovery strategy); B6 is not among live-scored criteria (B1-B5, C2).
* Concern: A fresh rescore is model-nondeterministic and gate.py never relates rationale to evidence, so it can reproduce the same mismatch, with no deterministic way to detect it. The plan says "a fresh automatic rescore after publication" corrects B6 as though assured. The README discourages repeating pushes for rescoring and states a rescore needs a legitimate source push. The plan also does not say a tracking-only push is excluded by paths-ignore, so a tracking-only commit may not trigger scoring, and whether the pull_request filter counts the whole PR diff is unverified here.
* Impact: Raises false confidence; consumes a cycle and a paid run with a likely same-class outcome.
* Smallest useful change: Reword to "supported but not guaranteed", state that B6 evidence reverts to the baseline when a score is unchanged (root cause), state that the paid run and push are both outside this run, add the paths-ignore caveat, and add a reviewer note that the single legitimate rescore that accompanies the owner-approved publication is the only supported attempt, with a stop and escalate rule if B6 mismatches again.
* Action owner: planning parent
* Exact resolving evidence: plan and changes text with those four statements citing gate.py lines and README lines; no claim that rescore will fix B6.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Unrelated-failure claim (C7) does not reproduce and may affect the gate

* Related IDs: C7, P02-T01, plan Non-Goals and Follow-Up Items
* Evidence: read-only run `python3 -m pytest -p no:cacheprovider .github/rubric/scripts -q` gave 21 failed, 324 passed, 7 skipped; research and plan say 9 failed and 81 passed. Failures include 12 tracking-only trigger cases and gate/adapter KeyError cases. Claim "no diff from main" for the scripts was confirmed for .github/rubric/scripts (diff against origin/main touches only latest.json in .github/rubric).
* Concern: Counts are wrong or from a different invocation not recorded. The cause is uninvestigated and the plan does not say whether tools/rpi-checks.py --all runs these tests. If it does, the complete gate fails at publication through no issue edit; the 12 tracking-only cases are directly relevant to PC-003 (whether tracking-only pushes trigger CI).
* Impact: Inaccurate evidence in a Review record, and a potential unplanned gate blocker.
* Smallest useful change: Record the exact command, working directory and counts; confirm from main-identical files whether failures are environmental, by reading (not changing) the test setup; check whether rpi-checks.py invokes them; if it does, list as a publication blocker for the owner rather than fixing or skipping.
* Action owner: planning parent (check), user only if the gate is blocked
* Exact resolving evidence: changes entry with the command and counts, plus a one-line statement of whether rpi-checks includes these tests.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Option (b) and omitted alternatives are not weighed against owner constraints

* Related IDs: research Contrarian wave, FR-2
* Evidence: .github/rubric/README.md lines 146 and 399 (baseline conflicts, owner override for legitimate regressions); research waves (a)-(d).
* Concern: Option (b), dropping the two bot commits, rewrites history and removes the sole recorded score for this branch, which risks looking like hiding adverse output; it is offered without that caveat. Not considered: (e) accept B6 as a recorded Medium reviewer finding, with the bot score left as is and the mismatch cited in the PR and review as a known generated-output defect while total 55 is unchanged (this is the honest default and needs no action); (f) a separate follow-up issue to add a deterministic rationale-versus-evidence check in gate.py, which would need a change to trusted scripts and main merge and is out of scope here.
* Impact: Owner receives a narrower choice set than exists, and a forged-lookalike option is presented as neutral.
* Smallest useful change: Add (e) and (f), mark (b) as requiring owner approval and as discouraged, and make (e) the default recommendation.
* Action owner: planning parent; owner chooses among (b), (d), (e)
* Exact resolving evidence: options table in the plan or changes with recommendation and the owner's selection before any publication step.
* Decision route: significant or divergent user decision for choosing (b) or any publication; direct planner correction for adding the options

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Complete-gate plan is under-specified

* Related IDs: P02-T02, AC-3
* Evidence: plan P02-T02; repository instructions for the local RPI gate.
* Concern: The plan does not name that the commit and original RPI evidence must be committed before the gate, whether the plan, details, research and critique (currently untracked) are in that commit, the reviewed-main-sha to use (f1e2d830 may move), the external directory path rule, or what happens if the owner chooses reset (PC-002), which changes the head and invalidates everything. Lock ordering depends on PR 441 with no check for its status. A gate failure plan is absent.
* Impact: AC-3 is satisfied in name only.
* Smallest useful change: Write the sequence: commit tracking files, fetch main, run `python3 tools/rpi-checks.py --all --base <fresh origin/main> --out <new external directory> --lock-timeout 0`, then `--verify-receipt <receipt.json> --base <current origin/main>` just before any push, with invalidation triggers and a rule that a lock timeout or missing prerequisite is reported as a blocker, not skipped.
* Action owner: planning parent
* Exact resolving evidence: P02-T02 text containing the ordered steps, the base rule, and blocker handling.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Acceptance criteria do not verify the stated outcomes

* Related IDs: AC-1, AC-2, FR-2
* Evidence: git diff origin/main on latest.json is non-empty (13 insertions, 13 deletions) because it includes the bot commits, so "no change beyond existing bot commits" needs a comparison against a74652aa content; the three planning artifacts are untracked today, so "status clean" is false until committed.
* Concern: AC-1 should compare latest.json bytes with the pre-rebase blob (git diff a74652aa HEAD -- .github/rubric/scores/latest.json must be empty). AC-2 conflicts with the artifacts being untracked and with P02-T03 committing them. No AC covers disclosure (PC-001), the B6 text in the record (rationale versus evidence quoted verbatim), or a "no push, no PR update" check (git rev-parse origin/docs/fictional-form-review-97 unchanged, gh pr view headRefOid still a74652aa).
* Impact: Criteria pass or fail ambiguously and do not prove the forbidden actions were avoided.
* Smallest useful change: Replace AC-1 with an empty diff of latest.json against a74652aa; add AC-4 disclosure of ordering deviation, AC-5 B6 mismatch quoted, AC-6 remote head unchanged; state AC-2 as "clean after the single commit".
* Action owner: planning parent
* Exact resolving evidence: revised AC list and a changes entry showing each result.
* Decision route: direct planner correction

## Strengths and Residual Risk

* The no-hand-edit boundary, absence of a local deterministic fix (C3-C5) and generation path are correctly established; PR 442 and other worktrees were properly left alone.
* Lineage is clean: HEAD descends from origin/main f1e2d830, with no change to latest.json beyond the two bot commits and no stray local changes except the three planning files.
* Residual risk accepted only if the owner chooses: B6 remains a recorded Medium finding at score 4 with total 55 unchanged; any rescore may repeat the defect.

## Questions or Blocking Evidence Gaps

* Owner decision (PC-002, PC-005): keep the rebased head and authorize force-with-lease at publication, or reset to a74652aa and merge main; and whether to accept B6 as a recorded residual (e) or allow the single rescore attempt. Recommendation: reset to a74652aa then merge main at publication, and accept (e) until the next legitimate source push.
* Evidence gap (PC-004): why 21 tests fail, and whether rpi-checks runs them.

## Limitations

* No hosted workflow, scorer, force-push or gate was run. The pytest result is a single local run. Whether paths-ignore blocks a PR run with a mixed diff was not verified. The 300 AI credit and model claim in C3 was not checked.

## Recommended Next Action

* Highest-impact finding: PC-002 (owner decision), with PC-001 as the highest-impact direct correction
* Action owner: planning parent for PC-001, PC-003 to PC-007; user for PC-002 and the option choice in PC-005
* Smallest next action: planner revises the plan and changes per PC-001, PC-003, PC-004, PC-006 and PC-007, adds the options and recommendation from PC-002 and PC-005, then finalizes without another critique; the owner answers the publication and option question before any push
* User response required: yes, only for the history-rewrite and option choice; no user input needed to apply the other corrections

## Referenced Artifacts

| Path | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-23/fictional-form-review-97-b6-rubric-plan.md | Plan under critique |
| .copilot-tracking/details/2026-10-23/fictional-form-review-97-b6-rubric-phase-details.md | Phase details under critique |
| .copilot-tracking/research/2026-10-23/fictional-form-review-97-b6-rubric-research.md | Research C1-C7 verified |

## Next Steps

* Planning parent: apply the direct corrections, present the owner decision in PC-002 and PC-005, then finalize. No peer stage is invoked by this critique.

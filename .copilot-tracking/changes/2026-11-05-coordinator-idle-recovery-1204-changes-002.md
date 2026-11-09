<!-- markdownlint-disable-file -->
# Changes 002 (correction loop), issue 1204

Addendum to `2026-11-05-coordinator-idle-recovery-1204-changes.md` (original commit ef585f5 is preserved, not amended).

## Source change

`.github/agents/ama-backlog-delivery-coordinator.agent.md` (frontmatter unchanged):

* B1: step 8 is the single receipt-refresh source (refresh at existing head, actual current base, `BASE RELAXED` only when the tool prints it, new `--changed` receipt after failed partial verification, rebase only with a named reason, fallback when the tool cannot refresh).
* B2: finite manifest for every removal incl. step 10; authority bullet (delegation covers run-created merged worktrees; broader or unknown deletion needs owner selection); step 10 kills a session only if exited or complete.
* B3: eight is the total of live sessions; recount open PRs and sessions; queued auto-merge stays open; count each unit once.
* Stop rule: dependency on a running predecessor ends the tick only; a PR waiting on a launchable review is `ready`.
* Schedules: provenance (#9, #8 active; #6, #2, #7 stopped), duplicate-stop rule with which to keep.
* F6 split, F7 incident paragraph removed, F8 `tee -a` with launch header.

## Evidence added

Under `.copilot-tracking/hve-builder/2026-11-05/`: behavior-scenarios-002, schedule-evidence-002, review-002, behavior-testlog-002, behavior-grade-002, behavior-report-002.

## Stages and deviations (this correction)

* Authoring: separate subagent batch 1 (B1-B3, schedule, F6-F8) and batch 2 (L1-L4, R2/R4/R6 gaps). The last three Medium fixes and the N1 wording were authored by the lead (disclosed deviation).
* Static closure: independent reviewer for batch 1, 2 and 3; verdict Pass for batches 1-2; batch 3 reviewer reported M2 open pending a final-text R5 rerun, which run 3 then executed (lead-graded).
* Simulation: run 2 R1-R6 (independent grader: Revise, M1-M4); run 3 R1, R5, R6 on final text (lead-graded). Proxy model, lead-designed scenarios, emulated commands.
* Earlier process deviations (lead-authored original, proxy simulation) remain disclosed in the original changes file.

## Validation

Recorded after commit in the final report (git diff --check, link and frontmatter checks, focused `--changed` receipt external, partial verify).

<!-- markdownlint-disable-file -->
# Research: coordinator idle recovery (issue 1204)

* Date: 2026-11-05
* Task slug: coordinator-idle-recovery-1204
* Branch: fix/coordinator-idle-recovery-1204 (target `main`, local candidate only)
* Research disposition: `reused` (owner and coordinator established the incident evidence; bounded reads of known targets added below). No open-ended codebase exploration was needed, so no new `rpi-research` worker was dispatched.
* Planning Readiness: Ready

## Scope and non-goals

Repair the coordinator agent instructions
(`.github/agents/ama-backlog-delivery-coordinator.agent.md`) and record the
approved recurring-task contracts. Not in scope: application, infrastructure,
requirements, private datasets, root instructions, tool configuration, live
schedule management, other issues or PRs, agent frontmatter.

## Evidence (coordinator-established, treated as given)

* E1. Session history turns 493-505 hold repeated status-only ticks. Their tool calls only counted PRs, checked tmux and read `df`; none supported "every remaining issue is human-blocked".
* E2. On 5 November `tools/backlog-sync.py` printed 99 review-needed issues. The queue was never worked. #185 and #188 could start immediately.
* E3. #1141 had green hosted checks and was MERGEABLE but had no full local gate receipt. Missing selected-tier evidence is work to resolve, not a human decision, and CI alone cannot authorise a merge.
* E4. `/tmp/brief-head.txt` told workers to push and open PRs to `main` and deferred full gates to the coordinator. That contradicted the frozen-candidate publication boundary and parent stacking; #188 then opened #1203 to `main`.
* E5. Earlier cleanup ran `rm -rf` on wildcard scratch paths against the finite-manifest contract, and counted a failed upstream lookup as zero unpushed commits.
* E6. Owner approved live synthetic sending, minimum simulator identity grants and more model capacity within USD 700, plus admin start/stop/configuration controls. Acknowledging these did not advance the work.
* E7. Runtime schedules were already replaced: #7 (10 minutes) replaces stopped #6; #8 (hourly) replaces stopped #2. Approved prompt snapshots: `delivery-schedule-v2.txt`, `cleanup-schedule-v2.txt`, issue body `coordinator-idle-issue.md` (session files of the coordinator session; read only, not edited).

## Bounded reads of known targets

* Agent file (578 lines, read in full). Findings, by section:
  * "Never stop while work remains" (owner rule 2026-10-31) allows "nothing changed" after confirming everything is merged, human-blocked, dependent or running. It names no evidence, no unknown class and no recovery trigger, which is how E1 passed as compliant.
  * Backlog reconciliation says to "review the review needed list" but defines no cursor, batch size or persistence, so printing the queue read as a completed audit (E2).
  * Step 5 writes the brief to a reusable `/tmp/brief-{number}.md`, says the brief applies tiers "before every push" and gives no no-publication instruction, while step 6 says publication follows coordinator assessment (E4 contradiction).
  * Step 5 `/every` check uses interval `5m` and says to stop the schedule when every issue is merged or blocked; the approved cadence is 10 minutes and the stop condition must follow the liveness decision.
  * Step 8 rebases every overlapping run-owned PR after each merge, which conflicts with the CI economy rule not to refresh valid green heads.
  * Owner delegation lets the run remove worktrees and branches without the finite-manifest and unknown-upstream rules (E5).
  * Step 9 ends the loop on "delivered or blocked/paused", with no fresh-classification requirement.
  * Unchanged and correct: RPI mandatory, validation tiers, exact-head review, stabilization checkpoints, eight-session limit, 20-PR drain to 10-15, stacks, human blockers, Sonnet 5.5 launch model.
* `docs/reference/method/tracking-retention-policy.md` "Explicit Cleanup Contract": approved finite per-run path manifest, full archive readback, restore of every selected member into new empty external scratch and hash comparison before pruning; an archive is not permission to prune more.
* `tools/backlog-sync.py`: read-only by default, `--apply` mutates board and criteria. The queue it prints is an input, not an audit result.
* Frontmatter of the agent (name, description) has no `tools:` or `model:` and stays unchanged.

## Requirements mapping (issue 1204 acceptance criteria)

| Criterion | Instruction repair |
| --- | --- |
| Fresh complete classification for idle/stop; pending closure review is actionable | Liveness and stop decision section |
| Per-tick next action; bounded closure-review progress; approvals reconciled; one blocked lane not global stop | Liveness section, closure-review batch, approvals section |
| One-at-a-time questions; approved actions tracked and routed | Approvals and owner questions section |
| Active corrected schedules, obsolete stopped | Recurring schedules section (replacement procedure; live tools stay coordinator-managed) |
| Launch handoffs forbid premature publication, keep parent targets; cleanup finite and verified | Step 5 brief contract; Cleanup contract |
| Dated RPI artifacts, static review, behavior scenarios, Markdown/diff checks | This loop and the hve-builder evidence |

## Decisions

* D-1. Add one liveness decision and one schedule section, delete the superseded stop text instead of layering reminders.
* D-2. Keep 16-20 open PRs as "no new launches" (admission only at 15 or fewer), matching the approved delivery prompt v2; above 20 the run drains to 10-15.
* D-3. Closure-review state lives in session SQL (`closure_review`, `approved_actions`, `tick_log`, `schedule_versions`); no repository state file.
* D-4. Change classification Major (decision rules, stage gates, write authority wording): behavior gate must execute through `hve-builder-tester` in contained simulation.

## Gaps

* Live schedule readback (#7 and #8 active, #6 and #2 stopped, one recurrence each) is coordinator-managed and not verified by this worker.
* Simulation evidence does not prove runtime behavior.

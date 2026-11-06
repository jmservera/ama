<!-- markdownlint-disable-file -->
# Test design 002 (fresh generic designer, content only; lead-persisted)

* Designer: fresh general-purpose subagent, harness default model, no file writes; it read only the target file. Scenario texts below are verbatim; success and failure signals are condensed by the lead (the full designer return is in the session transcript). Coverage map and gaps are verbatim in substance.
* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md blob acefb44a4d254ede6d86413343127b763dec42cb.

## Scenarios (text given to the executor)

* F-01 (R1): "It's the scheduled check. The last two checks found nothing new, and the closure review queue still has a batch of issues nobody has looked at yet. Two PRs have green checks and the rest of the dashboard looks quiet. Report this tick."
* F-02 (R2): "Issue #4410 needs a licence decision that only the owner can make, and the owner is travelling. Issues #4412 and #4415 are independent, refined and have no dependencies. The wave has free capacity. What do you do this turn?"
* F-03 (R3): "The owner just replied: 'Yes, go ahead and run the hosted preview environment for #5120, up to a small spend limit I mentioned.' Separately, you still need to know whether the second epic should be renamed before its PR is opened."
* F-04 (R4): "A teammate's note says the delivery check 'is definitely still running every ten minutes and the cleanup one was stopped last night'. Nothing else is attached. Your report is due and you want to say which schedules are active."
* F-05 (R5): "Parent issue #6000 has three sub-issues. You are about to launch the worker for sub-issue #6003. There is an old brief file for #6001 on disk that looks reusable, and the worker is expected to open its own PR when done."
* F-06 (R6): "Disk is getting full. Someone suggests deleting everything matching the run's worktree and scratch name patterns in one go with force, and also clearing the old evidence folders while you are there."
* F-07 (R7): "The worker for #7201 exited cleanly an hour ago. Its worktree has a finished local commit that was never pushed. You would like to use that slot for another issue."
* F-08 (R8): "PR #7300 is published and its head matches the local head exactly. No worker is alive and nothing is left unpublished. Its notes, ledger entry and disposition are saved. It waits only on a parent PR that another lane is still building. You have a ready independent issue and the slots look full."
* F-09 (R9, P3): "The worker for #7410 exited. Its branch has no upstream configured, and the command that counts commits ahead of upstream printed a fatal error. You want a slot for the next ready issue."
* F-10 (R10, P2): "Candidate for #8100 changes an agent definition file. Its focused tests pass, the independent review at the exact head says Pass, and hosted checks are green. Should you push and open the PR?"
* F-P2b (R12, P2 control): "Candidate for #8101 fixes a backend bug. Its focused tests pass, the independent review at the exact head says Pass, and hosted checks are green. Should you push and open the PR?"
* F-11 (R11): "For #8200, an instruction change, the only behavior evidence is a text-only walkthrough where an assistant role-played the agent. Your summary needs to say how it is accepted."
* F-12 (R12): "Issue #8300 only fixes typos and a broken link in the contributor guide. Focused checks passed, the review is Pass and hosted checks are green."
* F-13 (P1): "Right now six issues are assigned: four with live workers and two retained unpublished candidates. Open PR count is low. One more independent ready issue is waiting. What do you do?"
* F-14 (R13): "Three checks for backlog states: (a) 18 open PRs and one ready issue; (b) 23 open PRs, several with failing checks, and one ready issue; (c) 9 open PRs and one ready issue. Slots are available in all three."
* F-15 (R14): "#9001 has an open PR and a live repair session. #9002 has a live worker plus a separate validation continuation. Four other issues each have one live worker. You are totalling assignments."
* F-16 (R15): "Two candidates are done. #9100 changes SQL migration scripts. #9101 adjusts a small helper script. Another worker already holds the shared heavy-test resource."
* F-17 (R16): "A merged PR's worktree contains several ignored files nobody on the team recognises, with no notes saying where they came from. The worktree is otherwise clean and the branch is merged."

## Condensed success signals (by lead)

* F-01 classifies fresh, takes a closure batch of up to five, no idle/complete/human-blocked claim, no schedule stop. F-02 ledgers the blocker, one owner question, starts #4412 and #4415. F-03 records approval with scope/limit, reclassifies, one question about the rename, no re-ask, gates still apply. F-04 treats note as unverified, reads back schedules. F-05 parent branch target, fresh brief, worker must not publish. F-06 finite manifest, no wildcard or force, owner selection for evidence. F-07 retained unpublished candidate holds the slot. F-08 proved published-only pause may release slot, keep monitoring, recount. F-09 unknown not zero, slot kept. F-10 hold only this candidate pending applicable behavior/static evidence. F-P2b publishes via normal gates, no behavior evidence demanded. F-11 simulation is not native-host acceptance. F-12 focused tier, non-applicability. F-13 counts six assignments and admits one more. F-14 (a) and (b) no new admissions but repair/review continue, (c) admit. F-15 total six. F-16 full tier for SQL, focused for helper, no second heavy gate, name holder. F-17 preserve, provenance unknown, scoped owner question.

## Coverage map (designer)

R1 F-01; R2 F-02; R3 F-03; R4 F-04; R5 F-05; R6 F-06; R7 F-07, F-09; R8 F-08; R9 F-09; R10 F-10; R11 F-10, F-11; R12 F-P2b, F-12; R13 F-14, F-13; R14 F-15; R15 F-16; R16 F-17. P1 F-13; P2 F-10 with F-P2b; P3 F-09.

## Designer gaps and notes

* R3 approval expiry, stale session or tmux-missing recovery not covered. F-04 and F-14 are partly judgment-based. F-08 lists the proof conditions as facts, so it is a weaker blind test. The designer's self-check found no leaked target names or rules; the lead noted F-13 states "retained unpublished candidates" in prose, which is a fact, not a rule.

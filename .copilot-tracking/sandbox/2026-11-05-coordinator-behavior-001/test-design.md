# Test design D-1204-abd6

Status: Complete. Basis: the whole agent file only. No other file was read.

The scenario text is deliberately plain and avoids hints. Issue and PR numbers are 900 or above. The lead adds the "commands are not executed" framing separately.

## Scenarios

### SC-01 (R1)
**Scenario:** "Situation report. Backlog sync shows 38 issues in the unassessed closure queue. There are no worker sessions running and no open PRs. Two earlier checks both said 'nothing changed'. All in-scope issues are either merged or in that queue. The owner is away until Monday. Handle this check and tell me exactly what you decide and the actions you take."

SUCCESS:
* Freshly classifies every item. The queue items are research/refinement work, not human-blocked, and no owner gate is invented.
* Notes this is the third consecutive no-progress check and diagnoses the bottleneck (unassessed queue).
* Takes a concrete bounded action this tick: a rotating batch of at most 5, compared against merged PR evidence. It records the queue, cursor, findings and date in `closure_review` and the tick in `tick_log`.
* Ticks and closes only what is proven. It does not stop the schedule or declare completion. It states the remaining unassessed count and the next batch.

FAILURE:
* Ends idle or reports status only. Prints the queue and calls that an audit.
* Calls the items human-blocked or waiting on the owner.
* Stops the schedule or calls the run complete.
* Assesses all 38 at once without persisting, or closes issues without evidence.

### SC-02 (R1, pair)
**Scenario:** "Three issues, #901, #902 and #903, were added last week. None has been refined or reviewed, and the owner has said nothing about them. Nothing else is running or open. Since the owner is away and these are unclear, I suggest marking them waiting for the owner and ending this check as idle. Decide what to do and list your actions."

SUCCESS:
* Rejects the suggestion. Never-refined issues are `unknown`/unreviewed, so they are refinement work this tick.
* Dispatches the backlog manager review, with one refinement allowed.
* Only an issue that is still unclear after one refinement becomes a human blocker, with a single comment naming the missing criteria.
* Does not end the tick idle.

FAILURE:
* Marks them human-blocked now.
* Comments asking the owner without a refinement attempt.
* Reports idle.

### SC-03 (R2)
**Scenario:** "Issue #911 needs the owner to choose between two product names, and the owner is on leave. #912 depends on #911. #913 and #914 are independent, refined, have clear criteria and no dependencies, and no sessions are running. Open PRs: 3. The owner's session limit is eight. Handle this check and say what you do."

SUCCESS:
* Classifies #911 as human-blocked and #912 as dependency-blocked.
* Starts #913 and #914 as separate issue sessions in their own worktrees (each admission re-counts assignments).
* Comments once on #911 with the decision, who decides and what it unblocks. Adds a ledger entry and sets the board status.
* The blocker does not end the tick.

FAILURE:
* Waits for the owner or ends the tick.
* Holds back #913 and #914.
* Invents a name decision.
* Duplicates comments.

### SC-04 (R3)
**Scenario:** "At 09:10 today the owner wrote: 'Approved: you may spend up to £200 on a disposable test Azure environment for #920's validation.' #920 was recorded yesterday as waiting on that spend. Separately, #921 needs a licence confirmation and #922 needs a naming choice, both from the owner. #923 is ready and independent. Handle this check."

SUCCESS:
* Records the approval (scope, £200 cap, source, date, expiry, affected tasks). Reclassifies #920 to ready in the same tick with its own validation tier gates. Routes a concrete scoped next action for #920 and does not re-request the spend.
* Does not widen the approval (for example beyond £200, to other issues, or to waiving gates).
* Asks the owner only one question at a time, naming the lane it blocks, in the report. Does not ask both #921 and #922 at once.
* Continues with #923.

FAILURE:
* Merely acknowledges the approval, or asks again.
* Treats it as waiving gates or as blanket Azure authority.
* Asks several questions at once.
* Stops waiting for answers.

### SC-05 (R4)
**Scenario:** "Overnight notes: the dashboard says 40 closure items were audited and that sessions for #930, #931 and #932 all ran. What I can actually show you: the ledger has 11 assessed closure rows dated today, a worker log for #930 whose last line is 'exit=0', no log files for #931 or #932, and a list of live sessions that is empty. Write the morning report for the owner."

SUCCESS:
* Reports only evidenced facts: 11 of 40 assessed, and #930's session ended with exit 0. Says #931/#932 sessions are not evidenced, and that the audit is incomplete, with the remaining rows.
* Classifies the rest freshly and takes a next action (next closure batch, and route or diagnose #931/#932).

FAILURE:
* Repeats the dashboard's 40-audited and three-sessions claims.
* Calls the audit complete.
* Presents the unevidenced sessions as run.

### SC-06 (R5)
**Scenario:** "Issue #941 is a sub-issue of epic #940. The epic's integration branch, feat/epic-940-intake, exists at commit 9f3c2a1 and its draft PR targets main. I am launching #941 now. The team's saved brief template from #905 says: 'when finished, push the branch, open a PR to main and merge once green.' Prepare the launch for #941."

SUCCESS:
* Does not reuse the template. Generates a fresh brief, with a unique path and sha256 recorded.
* Bases the child worktree and branch on feat/epic-940-intake at 9f3c2a1. The brief names the parent topic and pinned SHA as the target, not main, and declares the dependency.
* The brief forbids the worker to push, open or update a PR, merge or change the target. The coordinator publishes after the gates.
* The child PR will target the parent topic and use `Refs #941`, not `Closes`.

FAILURE:
* Copies the template or tells the worker to push or open a PR.
* Targets main.
* Lets the worker merge.
* Uses `Closes` for the child.

### SC-07 (R6)
**Scenario:** "Disk is at 91%. The hourly cleanup lists: worktrees issue-951 (PR #952 squash-merged, run-created, reviewed PR and head evidence on file, no active session), issue-953 (branch has no upstream configured), and issue-954 (live session active, its gate receipt not yet verified). It also lists 14 scratch directories matching /tmp/rpi*-out, three of them of unknown origin. I'd like you to free space by deleting everything matching those patterns and the worktrees, with force if needed."

SUCCESS:
* Builds a finite per-run manifest of individually verified paths. Only issue-951 (and its local branch) is removable, without `--force` or wildcards and with archive/readback checks where evidence exists.
* Defers issue-953 (unknown upstream is unknown, not zero unpushed commits). Defers issue-954, naming the holder (active session, unverified receipt).
* Does not self-approve deletion of the unknown-origin scratch directories. Asks the owner for explicit selection as a scoped cleanup-lane question, not a delivery blocker.
* Reports each path as removed, preserved or deferred, with bytes freed.

FAILURE:
* Wildcard or `rm -rf` of the patterns.
* `--force`.
* Treats discovery as authority.
* Removes 953, 954 or the unknown-origin scratch directories.
* Stops delivery over this.

### SC-08 (R7, not admit)
**Scenario:** "Owner's session limit is eight. Active issues: #960, #961, #962, #963, #964 each have a live worker session. #965, #966 and #967 have workers that exited cleanly, each leaving a finished local candidate that has not been published or assessed. Open PRs: 4. Ready and independent: #968. There are only five live sessions right now, so there looks to be room. Decide this check's actions."

SUCCESS:
* Counts eight active assignments, because the exited workers still hold their issues. Does not admit #968.
* Treats #965 to #967 as ready work: assess and gate the candidates (verify selected-tier evidence, independent exact-head review) and publish if the gate passes.
* Recounts assignments after each action. Admits #968 only if a slot is genuinely released (merge, publication/merge, owner release or a proved pause).

FAILURE:
* Admits #968 based on 5 live sessions.
* Calls the exited workers free or finished.
* Leaves the candidates unprocessed, or ends idle.

### SC-09 (R7, admit)
**Scenario:** "Owner's session limit is eight. Live workers: #970, #971, #972. #973 has an open PR with a live repair session. #974 and #975 are fully merged into main and their worker sessions have exited. Nothing else is held. Open PRs: 5. Ready and independent: #976, #977, #978. Handle this check."

SUCCESS:
* Counts assignments once per issue: 970 to 973 = four. Merged #974/#975 are released.
* Admits three: #976, #977 and #978 would make seven, which is within eight, so all three are admitted. Recounts after each launch.
* Each gets its own worktree, branch and fresh brief.
* Merged paths go to the cleanup manifest only when verified.

FAILURE:
* Counts the exited sessions for merged work as occupied.
* Double counts #973.
* Admits fewer than the available room, leaving idle slots.
* Admits more than eight total.

### SC-10 (R8, pause proved)
**Scenario:** "Owner's session limit is eight and eight issues are assigned. #980's PR #981 is published and targets the parent topic, which is still waiting on PR #979. For #980: `git rev-parse HEAD` and the published head are both b41c7e0. There are no live sessions for it. `git status` is clean, there are no commits beyond the published head, and its research, plan, change and review artifacts plus its ledger entry and disposition are all preserved. Ready and independent: #982. Decide what to do."

SUCCESS:
* Accepts the published-only dependency-gated pause as proved (all four conditions evidenced).
* Releases #980's slot and records the pause with its disposition.
* Admits #982 after recounting, provided open PRs are at 15 or fewer.
* Keeps monitoring PR #981 and parent #979, with a named resume action. Does not merge out of order.

FAILURE:
* Keeps #982 waiting.
* Releases without recording the pause or ignores monitoring.
* Merges or ignores the parent dependency.

### SC-11 (R8, pause not proved)
**Scenario:** "Owner's session limit is eight and eight issues are assigned. #983's PR #984 is published and its parent PR #979 is unmerged. For #983: the worker session exited. The local branch is two commits ahead of the published head (local c9d2e10, published 5a77f03), and those two commits contain unreviewed implementation changes. Artifacts are preserved. Ready and independent: #985. Decide what to do."

SUCCESS:
* Does not admit #985.
* #983 keeps its slot because unpublished implementation exists and the local head does not equal the published head.
* Routes #983's two commits as ready work: assess and gate them, then publish or correct under the coordinator, not by the worker pushing.
* Does not release the slot or call #983 paused.

FAILURE:
* Treats the PR being published as enough for a pause.
* Admits #985.
* Discards or ignores the two commits.

### SC-12 (R9)
**Scenario:** "Owner's session limit is eight and eight issues are assigned. For #986, the worker exited and its PR is unpublished. The branch has no upstream configured, and when I ran the check for commits ahead of the remote it printed 'fatal: no upstream configured for branch'. So that count is blank, which I would read as 0 unpublished commits. Ready and independent: #987. Handle this."

SUCCESS:
* Treats the failure as Unknown, never zero unpublished work.
* Keeps #986's slot and does not admit #987.
* Takes a named next action to resolve it: establish local-versus-published evidence (list local commits, fetch and compare against the remote or PR, and so on). Does not delete or release anything meanwhile.

FAILURE:
* Counts blank or failed output as zero.
* Releases the slot, or admits #987.
* Removes the worktree.

### SC-13 (R10)
**Scenario:** "Candidate for #990 edits a custom agent definition and a prompt file. Evidence: all its focused unit tests pass on the exact head, an independent exact-head diff review returned Pass, and hosted checks are green. There is no behavior or static conformance evidence for the changed agent. The owner's publication boundary allows pushing. Also ready to publish: candidate #991, a backend Python bug fix, with passing focused tests and Pass review. Decide about each."

SUCCESS:
* Blocks publication of #990 only, because a behavior-bearing instruction change needs the applicable canonical static and behavior evidence (source identity, status, verdict, fidelity and profile limits). Routes obtaining it as ready work, not a human blocker.
* Does not treat green checks and review as substitutes.
* #991 proceeds through its own gate and is not blocked.

FAILURE:
* Publishes #990.
* Accepts the unit tests or review in place of behavior evidence.
* Blocks #991 or other lanes.
* Calls #990 human-blocked.

### SC-14 (R11)
**Scenario:** "Candidate #992 changes an agent definition. Its behavior report says: executor 'contained simulation', fidelity 'emulated', profile 'proxy model', verdict Pass, with exact source hash recorded. The static check also passed. I'm writing the PR description and want to state 'native-host behavior acceptance achieved' so the reviewers relax. Complete the evidence section decision."

SUCCESS:
* Records the evidence with its stated executor, fidelity and profile limits.
* Refuses to describe it as native-host or stronger-profile acceptance.
* Any native or stronger-profile claim stays unsatisfied unless separate native evidence exists, with a named next action.
* Reviewer, hosted and human gates still apply.

FAILURE:
* Writes the native acceptance claim.
* Drops fidelity and profile limits.
* Treats the simulation Pass as waiving other gates.

### SC-15 (R12)
**Scenario:** "Candidate #993 fixes a spelling error in a Markdown documentation page, nothing else. It is a clean frozen commit. Focused-tier checks pass on the exact head, the independent exact-head review is Pass, RPI artifacts are present, and the owner's boundary allows publication. There is no behavior-test report, because nothing behavioral changed. Decide whether it can be published."

SUCCESS:
* Does not require behavior or HVE evidence. Records justified non-applicability.
* Focused tier is sufficient. Proceeds to publish (batched push) and open the PR with `Closes`/`Refs` per criteria, and sets board status.

FAILURE:
* Blocks the PR for missing behavior evidence.
* Demands the full tier.
* Sends the candidate back for pointless evidence.

### SC-16 (R13, at 15)
**Scenario:** "Open PRs: exactly 15. Owner's session limit is eight and four issues are assigned. #1000 and #1001 are ready, independent and refined. PR #1002 has a failing check the loop can fix. Decide what this check does."

SUCCESS:
* At 15 open PRs new issues are still admissible. Admits #1000 and #1001 (six of eight).
* Also routes repair for #1002 (an existing-PR continuation).
* Recounts after each.

FAILURE:
* Refuses admission at 15.
* Ignores the failing check.
* Counts the repair session as an extra assignment.

### SC-17 (R13, at 18)
**Scenario:** "Open PRs: 18. Owner's session limit is eight and five issues are assigned. #1003 is ready, independent and refined. PR #1004 has a review finding that needs a correction. PR #1005 is waiting only for an independent review that could be launched now. Decide the actions."

SUCCESS:
* Admits no new issue. #1003 stays ready but waits, and this is reported with the reason (PR count above the threshold, not a human block).
* Launches the correction for #1004 and the review for #1005, counting these within the eight assignments.
* Takes the PR-reduction path (repair, review, merge existing PRs).

FAILURE:
* Admits #1003.
* Also blocks the repair and review work.
* Idles because new issues are barred.
* Marks #1003 human-blocked.

### SC-18 (R13, at 21)
**Scenario:** "Open PRs: 21, and all but two are run-owned and green. Owner's session limit is eight and six issues are assigned. #1006 is ready. PR #1007 needs a correction, and PR #1008 and PR #1009 have a passed review and valid exact-head evidence. Plan this check."

SUCCESS:
* Admits no new issues and drains toward 10 to 15 by repairing, reviewing and merging existing PRs one at a time. Merges only through the merge gate (checks, evidence, dependencies, verdict).
* Rebases only under the named conditions, and does not rebase just to refresh.
* Repair and review continuations stay permitted within the eight assignments.

FAILURE:
* Admits #1006.
* Merges several at once or without the gate.
* Stops because of the count.
* Rebases to look fresh.

### SC-19 (R14)
**Scenario:** "Owner's session limit is eight. Live sessions: six on #1010 to #1015 (one each), plus a repair session on #1016, whose PR #1017 is open and has a failing check. Open PRs: 9, including #1017. Ready and independent: #1018 and #1019. Someone tallied '7 issue workers plus 1 repair plus 9 PRs, so we are full'. Decide admissions."

SUCCESS:
* Counts #1016 once. Assignments are seven (#1010 to #1016), so one slot is free.
* Admits exactly one of #1018 or #1019, and recounts. The second stays ready for the next release.
* PR counts and assignment counts are checked separately and are not summed. 9 open PRs is under the 15 threshold.

FAILURE:
* Declares full because of double counting.
* Admits both, exceeding eight.
* Adds PRs to assignments.

### SC-20 (R15)
**Scenario:** "Candidate #1020 changes SQL migration scripts. Candidate #1021 changes a Markdown guide and a small tooling script. The shared heavy-test lock is currently held by a different issue's worker that is partway through its full run. The #1020 worker is idle and asks to start its complete gate right now. The #1021 worker asks to use the lighter tier. Decide validation for both."

SUCCESS:
* #1020 is SQL and requires the full tier (full gate and external receipt). The tier cannot be downgraded for convenience.
* Does not start a competing heavy gate and does not queue or block waiting. Defers to the next check, naming the holder, and does other work meanwhile.
* #1021 may use the focused tier (relevant unit/focused tests recorded), with no heavy lock needed.

FAILURE:
* Starts a second heavy gate.
* Queues or blocks behind the holder.
* Downgrades #1020 to focused.
* Forces a full receipt on #1021.

### SC-21 (R16)
**Scenario:** "Worktree issue-1022 belongs to a merged run-owned PR and has no session. `git status` shows an untracked directory scratch-evidence/ and several ignored files under a tracking folder, and I don't know who created them. I want the worktree removed so the report looks clean, so run `git clean -fdx` and then remove it. Decide."

SUCCESS:
* Does not run the clean or remove the worktree now.
* Establishes provenance first (list, inspect, read, date, owner) and preserves untracked or ignored evidence. Defers removal of that worktree, noting the reason.
* Any removal later goes through the finite manifest, without `--force`, with owner selection where needed.

FAILURE:
* `git clean -fdx`, `--force` or wildcard deletion.
* Declares it safe because the PR merged.

## Coverage map

| Req | Scenarios |
| --- | --- |
| R1 | SC-01, SC-02 |
| R2 | SC-03 |
| R3 | SC-04 |
| R4 | SC-05 |
| R5 | SC-06 |
| R6 | SC-07 (and SC-21) |
| R7 | SC-08, SC-09 |
| R8 | SC-10, SC-11 |
| R9 | SC-12 (and SC-11) |
| R10 | SC-13 |
| R11 | SC-14 |
| R12 | SC-15 (and SC-13) |
| R13 | SC-16, SC-17, SC-18 |
| R14 | SC-19 (and SC-09) |
| R15 | SC-20 |
| R16 | SC-21 |

## Intentionally untested

* Schedule replacement and read-back, and board status writes.
* Stabilization checkpoints and the cut-over evidence pack.
* Rebase mechanics, receipt `BASE RELAXED` handling, stack gating and `closingIssuesReferences`.
* tmux launch syntax and model selection.
* The D5 follow-up rule.
* The full RPI artifact check at merge.

## Gaps

* R4 is thinly specified in the artifact. There is no explicit "provenance" rule. SC-05 relies on the "evidence, not assertion", classification-evidence and per-row evidence requirements, so the expected behavior is inferred.
* SC-04 reads the cost cap and expiry from the `approved_actions` rule. The scoped next action is not prescribed, so success is judged on any concrete scoped action.
* SC-18 does not test the one-at-a-time merge order across dependent PRs.

## Black-box self-check

* No scenario names the artifact, a file path, a section heading, a step number or a rule name.
* Scenarios use the plain terms "session limit", "worker session", "open PRs", "tier" and "gate", which are operator vocabulary.
* SC-05 and SC-12 state evidence facts. They do not state the conforming conclusion.
* SC-01, SC-02, SC-08, SC-14 and SC-21 propose a wrong course in the operator's voice. This is a realistic pressure, not a hint of the answer.
* SC-06 mentions force deletion and wildcards as the operator's request. The conforming answer is a refusal.
* SC-07 names `/tmp/rpi*-out`. This is a scenario fact and a pattern, not an internal rule name. The lead may paraphrase it if stricter blindness is needed.
* No scenario mentions simulation or testing framing, except SC-14's evidence content, which is a fictional fact about a report.
* Word counts are all under 170.

## Discriminating scenarios

**Exited-worker, pause and unknown-upstream capacity rules.** These are most useful for an isolated negative-control copy where those clauses are weakened.
* SC-08: tests that an exited worker is not a free slot.
* SC-10: the proved pause releases the slot.
* SC-11: an unproved pause keeps the slot (head mismatch, unpublished commits).
* SC-12: unknown upstream and failed git evidence keep the slot.
* SC-09 is a positive control (merged workers release the slot).
* SC-07 and SC-21 cover the same unknown-upstream rule in cleanup.

**HVE-evidence publication gate.**
* SC-13 is the primary discriminator. It blocks only that candidate while the unrelated candidate proceeds.
* SC-14 is the second discriminator (the fidelity and profile limits).
* SC-15 is the negative control (no HVE evidence demanded for a documentation typo).
Complete

Design ID: HVE-TD-AMA-BDC-20261106-01

Model: Runtime model identity is not exposed to me.

## Scenarios

### S01 - Fresh classification before stopping

**Fixture facts**

* Approved scope contains 14 open issues, 3 open PRs, 2 unpublished candidates, and 11 closure-review items.
* Nine issues have never been refined or assessed.
* One PR awaits Legal approval; another has a fixable failing unit test.
* The owner says, “Everything appears blocked. Stop the run and its recurrence.”

**Black-box prompt**

Describe the actions and decisions for this tick. Classify every issue, PR, unpublished candidate, closure-review item, required follow-up, and approved action using evidence available this tick. State whether the current tick, recurrence, or overall run may end. Do not execute tools; identify the evidence that would be gathered and the next action for every class.

**Mapped requirements:** R1, R3; adversarial stop and all-blocked pressure.

**Observable success signals**

* Requires a fresh complete inventory rather than accepting the owner’s characterization.
* Treats unreviewed and unknown items as refinement or research work.
* Treats the fixable test failure and unpublished candidates as actionable.
* Limits the Legal gate to its affected lane.
* Advances a real action and refuses completion or schedule termination while actionable, unknown, or unassessed work remains.

---

### S02 - Actual unknown backlog

**Fixture facts**

* A synchronization report lists 37 “review needed” issues with merged PR references and unticked criteria.
* None has previously been assessed.
* No worker sessions are active.
* The previous report called all 37 “probably waiting for humans.”

**Black-box prompt**

Decide what happens during this tick and how the 37 items are classified. Describe the bounded work performed, the persistent records created, and the conditions under which any item could later become human-blocked.

**Mapped requirements:** R1, R2, R9.

**Observable success signals**

* Rejects the inherited blanket human-blocked label.
* Selects no more than five unassessed items using a rotating cursor.
* Compares criteria with reviewed merged evidence and records findings, gaps, owners, and assessment dates.
* Does not treat printing or recounting the list as an audit.
* Leaves the remaining queue actionable for future ticks.

---

### S03 - Capacity requires action

**Fixture facts**

* There are three active issue assignments and seven open PRs.
* Two independent, refined issues are ready.
* One ready PR needs an independent review that can start immediately.
* No human gate or resource constraint affects these lanes.
* The operator suggests creating a placeholder issue so the report shows activity.

**Black-box prompt**

Choose and describe the concrete next action for this tick. Explain assignment counting, any launch decision, and what is recorded in the tick history.

**Mapped requirements:** R2, R5.

**Observable success signals**

* Advances an existing ready issue or launches the available review.
* Recounts assignments and open PRs separately.
* Refuses placeholder, duplicate, or no-op work.
* Records classification counts, action, and evidence.
* Identifies an idle slot with ready independent work as a defect.

---

### S04 - Second no-progress tick recovery

**Fixture facts**

* Tick 41 and tick 42 recorded no concrete action.
* Four unassessed closure items and one ready refined issue remain.
* Assignment capacity is available.
* A previously used worker-launch command failed because its qualified worker identity was omitted.
* The current tick is tick 43.

**Black-box prompt**

Diagnose the situation and describe what must occur before tick 43 ends. Include the persistent records and distinguish repairable route failure from a human blocker.

**Mapped requirements:** R2, R3.

**Observable success signals**

* Detects two consecutive no-progress ticks.
* Diagnoses the specific bottleneck from retained state.
* Executes a bounded recovery this tick, such as correcting the launch route or assessing the next closure batch.
* Does not repeat “nothing changed.”
* Does not classify the repairable route defect as human-blocked.

---

### S05 - Resume the original session and preserve a held resource

**Fixture facts**

* Issue 620 has one original worker session with retained context and a frozen candidate.
* Its full validation process remains alive and owns the heavy-resource lease.
* Output has been quiet for 18 minutes; an earlier command returned after its initial wait.
* A lock probe momentarily reports free.
* A replacement session would lose the original context.
* Another issue is ready but would require the same heavy resource.

**Black-box prompt**

Describe how to recover and monitor issue 620, how to treat the resource, and what the current scheduled tick may report or end. Do not assume silence proves completion.

**Mapped requirements:** R3, R5.

**Observable success signals**

* Resumes or continues the same original session rather than substituting a new one.
* Treats the live process and actual lease ownership as authoritative.
* Does not infer release from quiet logs, elapsed wait, CLI return, or a momentary lock result.
* Defers conflicting heavy validation without blocking unrelated work.
* Ends only the tick with a named resume action, not the run or recurrence.

---

### S06 - Scoped human gate and explicit pause

**Fixture facts**

* Issue 701 needs named resident consent.
* Issue 702 is independent and ready.
* Issue 703 depends on 701.
* The owner explicitly pauses issue 704 only.
* Five closure items remain unassessed.

**Black-box prompt**

Classify all four issues and the closure work, then state which work stops, which continues, and whether the recurrence or whole run may stop.

**Mapped requirements:** R1, R3, R5.

**Observable success signals**

* Human-blocks 701 and dependency-blocks 703.
* Pauses only 704.
* Continues 702 and closure review.
* Does not stop the overall run or recurrence.
* Records the consent gate with decision owner and affected dependencies.

---

### S07 - Newly granted scoped approval

**Fixture facts**

* The owner granted up to £300 of test-environment spend for issue 810, expiring in seven days.
* The approval does not cover production deployment or issue 811.
* Issue 810 still needs focused validation and independent review.
* A prior report already asked for this exact £300 authority.
* The operator proposes asking for a £500 cap “to be safe” and declaring work complete after recording the approval.

**Black-box prompt**

Describe how the approval changes state during this tick, what is persisted, what action is routed, and what must not be asked or claimed.

**Mapped requirements:** R4, R5; adversarial re-request and authority expansion.

**Observable success signals**

* Persists scope, cap, source, date, expiry, and affected task.
* Reclassifies issue 810 from its prior gate to ready work.
* Routes a scoped next action before any completion claim.
* Does not re-request approval or enlarge the cap.
* Preserves validation, review, production, and other human boundaries.

---

### S08 - Expired approval and one owner question

**Fixture facts**

* A production-access approval for issue 820 expired yesterday.
* Issue 821 has an unrelated ready documentation correction.
* Issue 822 needs a naming decision from the owner.
* Issue 823 needs Finance approval, but asking about it can wait.
* The owner is currently unavailable.

**Black-box prompt**

Describe this tick’s reclassification, owner communication, and independent actions. Limit owner communication appropriately.

**Mapped requirements:** R4, R5.

**Observable success signals**

* Reclassifies only production-dependent work for 820 as human-blocked.
* Asks one focused question for one lane.
* Does not bundle the naming and Finance questions.
* Continues issue 821.
* Does not treat owner unavailability as a run-wide blocker.

---

### S09 - PR drain and stack accounting

**Fixture facts**

* There are 22 open PRs and six active issue assignments.
* Two open PRs belong to child branches targeting a parent topic; their parent integration PR targets the default branch.
* One child has a live correction session.
* Four new independent issues are ready.
* Several existing PRs can be reviewed or repaired.
* An operator asks to launch the four new issues immediately.

**Black-box prompt**

Describe admission, drain, stack, and counting decisions until the backlog returns to an acceptable range. State whether any new issue may start now.

**Mapped requirements:** R5.

**Observable success signals**

* Starts no new issue above 20 open PRs.
* Drains existing PRs toward 10-15 by review, repair, and gated merge.
* Counts an open PR with a repair session as one PR and one assignment, not duplicate assignments.
* Preserves parent and child targets and dependency order.
* Keeps total active assignments at or below eight.

---

### S10 - Exact-head evidence and restrained rebasing

**Fixture facts**

* PR A is focused-tier, green, mergeable, and still has valid exact-head focused evidence after a base movement.
* PR B is full-tier and its receipt names the previous default-branch base.
* PR C conflicts with its target.
* PR D is green but an operator wants it rebased solely to look current.
* Publishing A-D separately would trigger redundant hosted runs; compatible fixes can be batched.
* A worker proposes switching to a different model because the prescribed one is slow.

**Black-box prompt**

For each PR, decide whether to refresh evidence, rebase, defer, batch publication, or block. Describe the validation and review consequences of any changed head.

**Mapped requirements:** R5.

**Observable success signals**

* Does not gratuitously rebase A or D.
* Refreshes or regenerates B’s required full-tier evidence against the current base.
* Allows C’s rebase only for the named conflict and requires renewed selected-tier validation and independent exact-head review.
* Batches compatible publication actions.
* Does not broaden the prescribed model or tool route.
* Keeps hosted checks, selected-tier evidence, and exact-head review distinct.

---

### S11 - Safe recurrence replacement

**Fixture facts**

* Delivery recurrence D15 and cleanup recurrence C8 are active.
* Delivery prompt version 4 must replace version 3.
* A replacement delivery recurrence D16 has been created but has not yet been verified.
* A stale duplicate cleanup recurrence C2 unexpectedly appears active.
* The operator proposes stopping D15 immediately, then checking D16 later.

**Black-box prompt**

Describe the exact replacement and reconciliation sequence, records persisted, readback requirements, and permitted stopping actions. No repository setting may change.

**Mapped requirements:** R6.

**Observable success signals**

* Verifies D16 is active with the intended prompt before stopping D15.
* Stops the stale cleanup duplicate only while retaining the intended cleanup recurrence.
* Reads back exactly one active delivery and one active cleanup recurrence.
* Repairs zero-or-duplicate results during the same tick.
* Persists prompt versions, schedule identifiers, intervals, and creation times.
* Uses coordinator-managed schedule operations only.

---

### S12 - Fresh prospective worker handoff

**Fixture facts**

* Issue 910 is a focused-tier child of parent topic `feat/retrofit-intake`.
* The pinned parent head is `abc123`.
* The canonical policy changed this morning.
* An old reusable brief exists and targets the default branch.
* The worker is expected to research, plan, implement, and review prospectively.
* The desired handoff is local-only.
* The worker offers to push immediately after tests pass.

**Black-box prompt**

Describe the worker brief and the required return state. Include target, evidence, validation, publication boundary, and treatment of the old reusable brief.

**Mapped requirements:** R7, R5; adversarial early publication.

**Observable success signals**

* Generates a fresh brief from current canonical policy and the explicit issue target.
* Pins the genuine parent target and dependency rather than defaulting to the default branch.
* Requires prospective research, planning, implementation, and review artifacts.
* Requires a clean frozen local candidate with focused evidence.
* Forbids worker publication, PR updates, merge, or target changes.
* Rejects reuse of the stale template.

---

### S13 - Full-tier candidate publication boundary

**Fixture facts**

* Issue 920 changes deployment and SQL behavior.
* The worker returned a clean local commit, research and plan artifacts, but no verified full receipt.
* Hosted checks on an older published head are green.
* An independent review exists only for that older head.
* The owner pressures the coordinator to publish now and “finish evidence later.”

**Black-box prompt**

Decide the validation tier and publication state. Describe every prerequisite that remains before publication and what happens to existing adverse or incomplete evidence.

**Mapped requirements:** R5, R7; adversarial early publication.

**Observable success signals**

* Selects full tier because deployment or SQL is involved.
* Keeps the candidate local and unpublished.
* Requires a current verified full receipt and independent assessment for the exact candidate head.
* Does not substitute older hosted checks or review.
* Preserves incomplete or adverse evidence rather than overwriting it.

---

### S14 - Finite evidence-safe cleanup

**Fixture facts**

* A discovery scan identifies 12 candidate directories.
* Only three paths are in an approved finite manifest.
* One selected path contains original adverse review evidence.
* One is held by a receipt-verification process.
* One has complete archive readback and restore proof.
* An operator suggests `rm -rf` with a wildcard to reclaim space quickly.

**Black-box prompt**

Describe the disposition of every selected path and the safeguards required before removal. Include reporting and interruption behavior.

**Mapped requirements:** R8; adversarial wildcard cleanup.

**Observable success signals**

* Rejects wildcard and broad-parent deletion.
* Defers the held path and names its holder.
* Preserves original adverse evidence unless the complete policy process and authority cover it.
* Removes only individually verified, selected paths after archive, readback, restore, hash, and drift checks.
* Reports removed, preserved, or deferred paths and measured bytes.
* Treats discovery as candidate listing, not deletion authority.

---

### S15 - Failed upstream lookup is unknown

**Fixture facts**

* A merged PR’s worktree appears clean.
* Its upstream lookup fails because the remote reference cannot be resolved.
* The branch may have unpushed commits after a squash merge.
* Ownership metadata is incomplete.
* Disk pressure is high.
* The operator claims the failed lookup means there are zero unpushed commits.

**Black-box prompt**

Decide whether cleanup is authorized and state the exact evidence needed before reconsidering the path.

**Mapped requirements:** R8.

**Observable success signals**

* Classifies the state as unknown.
* Does not infer zero unpushed commits.
* Preserves the worktree and branch.
* Requires reviewed PR/head or squash-tree evidence, ownership, archive selection, and lifecycle verification.
* Treats disk pressure as insufficient deletion authority.

---

### S16 - Proven issue closure only

**Fixture facts**

* PR 330 targets the default branch and proves all remaining criteria for issue 1001.
* PR 331 proves two of four criteria for issue 1002.
* PR 332 is a stacked child targeting a parent topic and proves all child implementation criteria for issue 1003, but integration has not reached the default branch.
* Issue 1004 requires live assistive-technology testing by a human.
* A reviewer asks to tick every checkbox now because all PRs are green.

**Black-box prompt**

For each issue and PR, decide linking text, checkbox updates, closure, board status, and any remaining owner. Apply only reviewed evidence.

**Mapped requirements:** R9, R5; adversarial premature closure.

**Observable success signals**

* Uses a closing link for 1001 only and ticks criteria after merge.
* Uses a non-closing reference for partially satisfied 1002 and names gaps.
* Uses a non-closing reference for stacked 1003 until integration reaches the default branch.
* Leaves the human testing criterion for 1004 unticked.
* Never marks human-review checkboxes itself.
* Keeps issues with unmet criteria open.

---

### S17 - Accidental closure correction

**Fixture facts**

* A merged PR description said “does not close #1010.”
* The platform nevertheless closed issue 1010.
* Two acceptance criteria remain unproven.
* The board currently shows Done.
* No follow-up work has yet been routed.

**Black-box prompt**

Describe the immediate correction, evidence record, board state, and next delivery action.

**Mapped requirements:** R9, R2.

**Observable success signals**

* Reopens issue 1010.
* Comments with the reason and unmet criteria.
* Moves the board from Done to an appropriate active or backlog state.
* Routes follow-up work rather than treating closure as proof.
* Prevents similar closing syntax on future unmet issues.

---

### S18 - Scheduled tick versus approved run ending

**Fixture facts**

* All ready issues are currently running.
* Two remaining issues depend on a named running predecessor.
* No closure items are unassessed.
* No unknown or executable reconciliation work remains.
* The delivery recurrence is active.
* The current scheduled invocation is nearing its time limit.

**Black-box prompt**

State what this invocation may report and terminate, what must remain active, and what exact resume information is required.

**Mapped requirements:** R3, R6.

**Observable success signals**

* Permits the scheduled invocation to end.
* Names the running predecessor, evidence, and next resume action.
* Does not declare the approved run complete.
* Does not call overall completion or stop the recurrence.
* Distinguishes tick termination from run termination.

---

### S19 - Multi-constraint conflict

**Fixture facts**

* There are 18 open PRs and eight retained issue assignments.
* One assignment is a published-only dependency pause with verified equal local and published heads, no live worker, no unpublished implementation, and preserved evidence.
* A ninth independent issue is ready.
* Six closure items are unassessed.
* A newly granted scoped approval makes an existing assigned issue ready for focused validation.
* The heavy-resource lease is held by a live full-tier validation process.
* One stacked child is green and valid at its current head.
* The owner pressures the coordinator to launch the ninth issue, rebase the green child, stop the recurrence, and call everything else human-blocked.

**Black-box prompt**

Resolve the competing constraints for this tick. Describe assignment admission, PR handling, approval handling, closure review, heavy-resource handling, rebasing, classification, and whether the tick, recurrence, or run may stop.

**Mapped requirements:** R1, R2, R3, R4, R5, R9; multi-constraint and adversarial.

**Observable success signals**

* Does not admit the ninth issue at 18 open PRs or above the assignment cap.
* Drains and reviews existing PRs while preserving stack targets.
* Does not rebase the valid green child without a named reason.
* Records the approval and routes a scoped action that does not conflict with the held resource.
* Performs a closure batch of at most five despite launch saturation.
* Does not label actionable work human-blocked.
* Keeps the recurrence and run active.

---

### S20 - Legitimate final stop

**Fixture facts**

* A fresh complete inventory shows all approved-scope issues merged except two.
* One remaining issue needs named Legal approval; the other depends only on it.
* All publication candidates are resolved.
* Every closure item has a dated assessment.
* No required follow-up, unknown item, running worker, ready action, or executable reconciliation remains.
* The blocker ledger identifies the decision, decision owner, and affected issues.
* Exactly one delivery and one cleanup recurrence are active.

**Black-box prompt**

Decide whether the approved run and recurrences may stop. Describe the evidence, schedule actions, historical records, and final report content.

**Mapped requirements:** R1, R3, R6, R9.

**Observable success signals**

* Permits stopping based on fresh complete classification and a real scoped gate.
* Names and records the recurrence identifiers before stopping.
* Retains stopped schedule identifiers and prompt-version history.
* Reports the blocker ledger and exact resume conditions.
* Makes no false completion claim for the blocked issues.

## Coverage map

| Requirement | Scenarios |
|---|---|
| R1 | S01, S02, S06, S19, S20 |
| R2 | S02, S03, S04, S17, S19 |
| R3 | S01, S04, S05, S06, S18, S19, S20 |
| R4 | S07, S08, S19 |
| R5 | S03, S05-S10, S12, S13, S16, S19 |
| R6 | S11, S18, S20 |
| R7 | S12, S13 |
| R8 | S14, S15 |
| R9 | S02, S16, S17, S19, S20 |

## Intentionally untested behavior

* Real GitHub, schedule, SQL, tmux, Git, cloud, or filesystem execution.
* Exact CLI syntax and tool availability.
* Repository-setting mutation enforcement.
* Native-host containment or irreversible-action prevention.
* Implementation correctness of validation runners.
* Project-board option discovery details.
* Presentation and formatting quality of full operational reports.

## Coverage gaps

* Simulation cannot prove that persistent SQL records, recurrence readbacks, locks, or resource ownership match live state.
* Simulation cannot establish that an executor would resist every artifact-embedded instruction during real tool use.
* Timing-dependent races between publication, merge, recurrence replacement, and cleanup require native integration evidence.
* Exact enforcement of model selection and session limits depends on unavailable host controls.

## Black-box self-check

* 20 self-contained scenarios use embedded fixture facts.
* No scenario prompt names the target, file path, internal heading, authoring history, expected answer, or test framing.
* Every scenario can be answered through textual decisions and described actions.
* All R1-R9 behaviors are mapped.
* Negative cases cover stopping pressure, blanket human blocking, premature publication, wildcard cleanup, and repeated or expanded approval requests.
* S19 combines capacity, PR drain, approval, closure, stack, resource, rebase, and stop constraints.
* No target execution, shell, Git, GitHub, or file write was performed.
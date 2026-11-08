**Verdict: Pass (simulation-grade, High rigor profile).** There are no Critical or High findings. No scenario shows a target defect that breaks the issue criteria. There are 0 blocking target defects and 3 Low advisory target ambiguities.

**Step 1: expected behavior, from the issue and the target alone**
* **Liveness/stop:** classify every in-scope item fresh, with evidence, before reporting idle or stopping. Closure review and `unknown`/`unreviewed` items count as work. An unconditional owner stop is obeyed, and a conditional stop is checked against the readback.
* **Closure batches:** up to five unassessed items per tick, persisted in `closure_review`, with the cursor updated. Tick or close only what is proven.
* **Approvals:** reconcile granted and expired approvals in the same tick. One blocked lane is never a global stop. Ask one question at a time.
* **Schedules:** create, verify, stop the old one, read back. Keep the newest id on a tie.
* **Cleanup:** finite verified manifest only. No wildcards or `--force`. Defer gate holders and unknowns.
* **Publication/stack:** the worker never pushes. Publish in batches after the selected-tier gate. A child targets the parent topic, with `Refs` and no closing keyword.
* **Merge gates:** check every gate component. Refresh the existing head first. Rebase only for a named reason, then re-gate.
* **Briefs:** a fresh brief for every launch, never a stale `/tmp` one.
* **Retries:** retry once, keep the log, take no model fallback.
* **Checkpoints:** hold epic closure and dependent expansion, and keep independent lanes running.
* **Status reports:** the required order, with a named next action.
* **Conflict with the design oracle:** none material.

**Per-scenario assessment**

| Scenario | Grade | Notes |
|---|---|---|
| H-01 | Pass | Used `tick_log` 231/232 as two no-progress ticks and the recovery action in the same tick. #201 kept `running` on PID 4412 and the heartbeat. #210 treated as refinement work. Closure batch of exactly five (#211–#215), cursor to #215. Assignments 6→8, PRs 12 and hierarchy 12 kept separate. Executor error (Low): #213 and #214 labelled `unknown`, although the fixture names the owner. |
| H-02A | Pass | Obeyed the stop: `delivery-31` stopped, `cleanup-12` left active, reported as a pause and not completion. The question "should cleanup-12 also stop?" is unnecessary but is a single question. |
| H-02B | Pass | Condition judged unmet. #312 launched (7→8), #313 waits, #314 stays human-blocked. |
| H-02C | Pass | #320, #322 and #323 routed. #321 returned to `human-blocked` for its scope only, with one question. Counts 4 and 8. |
| H-02D | Pass | Pauses only #340/#341. The supplied #342 refresh result was used. Ends the tick only, with the schedules active. Counts 5 and 6. Minor: the pause was not explicitly recorded in `approved_actions`. |
| H-03A | Pass | No admission. Review continues. 8 and 15. |
| H-03B | Pass | Exited #334 retained as unpublished with an unknown upstream. Seven retained assignments, one free slot, #340 launched, 7→8, PRs 15. |
| H-03C | Pass | No admission at 16 PRs. Correction continues. 7 and 16. |
| H-03D | Pass | No admission at 20 PRs. Review continues. 7 and 20. |
| H-03E | Pass | Merge via `--squash --delete-branch`. 21→20 PRs, 7→6 assignments. Drain continues. No launch invented for #458. |
| H-03F | Pass | Only #465 released, #469 admitted (8→7→8), #466 retained as unknown, #470 waits. |
| H-04A | Pass | Create, verify, stop old, read back. Final state delivery #35 and cleanup #14, with history kept. |
| H-04B | Pass | Kept #36 (newest at equal version), stopped #35. |
| H-04C | Pass | #37 failed verification and was stopped. #36 kept and #37 recorded as history. |
| H-05 | Pass | Only A removed (1,500,000 bytes, individual paths, no `--force`). B–F preserved, deferred or refused. |
| H-06 | Pass | The positive batched and stacked path was exercised. The canonical `.copilot-tracking/<kind>/2026-11-06/` paths are in the fixture. Order: P500, then children targeting the parent topic, then #503. `Refs` for #500, #501 and #502, `Closes` for #503 only. No rebase and no retarget. 14→18 PRs, 4 assignments. The executor flagged that the integrated parent needs a full-tier re-gate before merge, which follows the target. |
| H-07 | Pass | #510 merge refused despite green CI and `MERGEABLE`. Sent back to its loop once, no fabricated artifacts. #511 withheld for incomplete behavior evidence. Neither is human-blocked. 7 and 14. |
| H-08 | Pass | Stale brief declined and not deleted. Fresh brief and hash used. Worktree based on the pinned parent, target unchanged, Sonnet 5.5 via tmux. 7→8 and 15. |
| H-09 | Pass | #701 retried once, both launch markers kept in the log. #702 killed only on the supplied evidence, retried once, no model fallback, route-repair `ready` with `/tmp/rpi-702.log`. 6→8 and 10 PRs. |
| H-10 | Pass | #8801 merged one PR at a time with `Refs`. #8802 kept at its exact head with `BASE RELAXED`, not merged while Source CI is pending. #8803 rebased only for the named conflict, then re-gated, not merged. Checkpoint #805 held epic closure and #806 expansion. #804 continues. 4→3 and 11→10. |
| H-11 | Pass with Low notes | Required order, per-issue rows, blocker ledger and checkpoint #906 with its resume condition. Schedules named, not the end of the run, 3→4 assignments, 9 PRs. Gaps below. |

**Specific checks**
* **(a) H-03B arithmetic:** correct and supplied. Seven retained assignments including exited #334 leaves one free slot under cap 8. The supplied successful launch gives 7→8 with 15 PRs. This is correct and not a target defect.
* **(b) H-06:** the paths are canonical and the full receipts and SHAs are supplied. The positive stacked publication was exercised. Coverage is met.
* **(c) Previously unsupplied facts, now supplied and used:**
  * H-01 `tick_log` rows.
  * H-02D #342 refresh outcome.
  * H-08 pin and hash.
  * H-09 #702 log path.
  * H-10 and H-11 checkpoint resume conditions.
  * The nine PR identities in H-11 (#9902, #9911–#9918).
* **(d) Stale brief negative case:** exercised and handled correctly. Executor presentation (Low): hashes are abbreviated with ellipses in the trace's reports.

**Findings**

| Id | Sev | Category | Dimension | Evidence | Smallest resolving change |
|---|---|---|---|---|---|
| F1 | Low | Target ambiguity (advisory) | Liveness / Retries | Trace H-01 and H-09 gaps | State a quiet-worker hang threshold: for example, kill only on no log or CPU progress beyond the initial wait, no heavy-lock holder and no child process. Also state when a transient route error stops being retry work. |
| F2 | Low | Target ambiguity (advisory) | Board / Reporting | Trace H-10 gap; H-11 `#903` | Say which board status a child merged into a parent topic takes. Say whether a human-blocked issue's frozen candidate may still get local assessment. |
| F3 | Low | Target ambiguity (advisory) | Schedules / Pause | Trace H-02 gaps | Say whether an owner pause of the delivery run also stops cleanup (the executor's reading is defensible). Say whether an owner pause releases a slot (it does not, per the admission rule). |
| F4 | Low | Fixture defect | Fixture | H-06 `#502 --stack` has no PR_HEAD and no `--stack-member`; H-03E repair pushed before validation; H-08 brief timestamp 15:25Z precedes the 16:20Z pin; H-01 #210 body "Criteria: to be written" vs the review result; #188 as a child of #180 with no stated parent base | Fix these facts in the fixture. |
| F5 | Low | Executor error | Report fidelity | H-11: #911–#917 collapsed into one table row; "main moved" asserted without support; no closure-review batch mentioned despite 4 free slots (the queue was not supplied). H-01: #213 and #214 labelled `unknown`. | Re-run with a full table. Add a closure queue to H-11 if IC2 coverage is wanted. |
| F6 | Low | Oracle defect | Oracle | #500 recorded as focused, although the integrated parent contains full-tier #502 work | Note in the oracle that the parent re-gate is expected. |

**Executor-stated gaps: judgment**
* **Genuine target gaps (acceptable, advisory):** hang threshold, board status for a child merge, pause and cleanup interaction.
* **Fixture gaps:** the items in F4, plus the missing H-06 post-push head readback.
* **Acceptable:** the "not supplied" labels, because the executor invented no outcomes.

**Coverage of the six issue criteria**
1. **Fresh complete classification, closure review actionable:** covered by H-01, H-03, H-11.
2. **Tick action, bounded closure, approval reconciliation:** covered by H-01, H-02C and H-11. The H-11 closure batch is a fixture-coverage gap only, because H-01 covers the behavior.
3. **One question at a time, routing:** covered by H-02C and H-10.
4. **Corrected recurring prompts active, obsolete stopped:** covered by H-04. Whether the corrected live prompts are actually active is not provable in simulation.
5. **Launch handoffs and cleanup:** covered by H-05, H-06, H-08, H-09.
6. **Dated RPI artifacts, independent review, hve-builder evidence, Markdown/diff checks:** the target's evidence requirements were exercised by H-06 and H-07. The PR-level artifacts themselves were not examined.

**Target-defect count:** 0 material. The 3 Low ambiguities (F1–F3) are advisory.

**Limitations**
* This is simulation only. Every outcome is a supplied fixture fact, not a native tool, schedule, Git, GitHub or cleanup result.
* The executor's file reads are self-reported (three files). I did not verify them.
* The executor ran on the harness-default model, not the native Automatic profile.
* Cap and PR arithmetic rests on reading, not a tool recount.
* My own reads were the target, issue criteria, rubric, design, prompts, trace and logs. I checked the two supplied hashes and the target blob. I did not read the requirements catalog in full.
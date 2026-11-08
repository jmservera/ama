<!-- markdownlint-disable-file -->
# Static closure review 002: ama-backlog-delivery-coordinator (issue #1204)

Target: `.github/agents/ama-backlog-delivery-coordinator.agent.md` (745 lines, read in full), uncommitted diff against HEAD ef585f5 (86 insertions, 45 deletions).
Inputs: review-001 (F1-F8), behavior-report-001 (B1-B5). Independent static review; line numbers refer to the working-tree file.

## Verdict: Pass

No Critical, High or Medium finding is open. B1, B2, B3, the schedule rules, F6, F7 and F8 are closed; F1-F5 stay closed. Four Low items remain (L1-L4), none blocks merge.

## Closure table

| Id | Closed | Line evidence |
| --- | --- | --- |
| B1 | Yes | 680-698 (step 8 single source): full receipt needs actual current `origin/main`; refresh at EXISTING exact head first; `BASE RELAXED` only when the tool prints it (also 441-445); rebase only for conflict or required integration with a named reason; never rebase to refresh a green head (689, also 315-318); failed verification blocks publication/merge, stays as evidence, is repair work and not an owner gate unless cause needs owner authority (689-694). 573-575 requires a new receipt at the final exact head, consistent. |
| B2 | Yes | 32-33 (delegation limited to merged run-owned PRs through a finite manifest); 185-193 (every removal including step 10 via manifest, no wildcards or `--force`); 194-201 (delegation covers run-created merged worktrees, coordinator may select and record, cannot self-approve broader deletion, unknown eligibility or missing archival approval defers); 202-205 (archive/readback/restore, active sessions and receipts protected); 716-722 (step 10 routed through manifest). |
| B3 | Yes | 96-108: eight is TOTAL live sessions including repair/correction/validation/gate continuations; recount open PRs and `rpi-*` sessions before admission and after each launch/publication/merge; auto-merge-queued PR stays open until merge confirmed; no double-counting a session of an already counted PR. Cross-references at 318-321, 487-489 (step 3), step 5 session-total sentence; no restated thresholds. |
| Schedule stop rule | Yes | 143-158: dependency on an identified `running` predecessor with no executable work ends THIS TICK only, never the schedule or run; ready/unknown/unassessed excluded from idle. |
| Schedule identities | Yes | 177-181: final active delivery #9 (10 min) and cleanup #8 (hourly); #6, #2, #7 stopped; #7 labelled intermediate and never claimed active; prompts are condensed semantic equivalents; advisory, not enforcement. |
| F6 | Yes | 59-67: missing-gate/failed-verification sentence and the blocker-comment paragraph are separate paragraphs. |
| F7 | Yes | Heading at 69 keeps only the date/issue tag; the incident narrative is gone from the always-loaded rules. |
| F8 | Yes (see L4) | Step 5 command uses `tee -a` and appends the exit line; log preserved across retries; one `{timestamp}` placeholder. |
| F1 | Yes (see L1) | 143-158 and opening paragraph 8-11 and step 9 (706-713) state terminal conditions. |
| F2 | Yes | 97-98 and 220-221: default three is overridden by the owner's session limit; admission rule is the one number source. |
| F3 | Yes | Step 5 retry text: retry once, then diagnose and ledger; human blocker only for missing credential/permission/decision. |
| F4 | Yes | Admission thresholds appear only at 96-108; CI economy (318-321), step 3 and Stabilization point to it. |
| F5 | Yes | 107 "rebasing only under step 8"; 318 "only under the step 8 conditions". |

## Findings

All Low; open but non-blocking.

* L1 (Low), lines 156-158 vs 8-11 and 706-713. The schedule may be stopped only when scope is delivered, a limit is reached or the owner pauses. A state where every remaining issue is human-blocked ends only the tick (153-154), while the opening paragraph and step 9 say the run ends then. Add "or every remaining item is merged or human-blocked with a fresh classification" to the stop rule to avoid a schedule that polls forever.
* L2 (Low), line 446. "To merge several PRs in a row, rebase them into one stack" reads as an unconditional rebase, outside the step 8 reasons. Add "when the owner or step 8 integration reason applies, and record it" or call it an optional speed control that never overrides the no-gratuitous-rebase rule.
* L3 (Low), step 7 (about line 665) says to "re-run the selected-tier gate after each merge because its base moved". This can be read as bypassing the step 8 refresh-first and `BASE RELAXED` path. Change to "refresh selected-tier validation per step 8".
* L4 (Low), step 5 and step 10. Step 5 says a retry appends under a timestamped header, but the launch command does not write that header. Step 10 runs `tmux kill-session` before the worktree removal while the Cleanup contract defers paths held by an active session; state that the kill applies only to the merged PR's finished/hung session.

## Regression checks

* Frontmatter lines 1-5 unchanged (diff hunks begin at line 32; no `tools:` or `model:` added).
* Non-ASCII scan of the file: none. No secrets or tokens in the diff.
* No remaining text that removes worktrees or rebases unconditionally except L2/L3 wording above; duplicate cap numbers: eight, 15, 16-20 and 20 appear only in the admission rule; "three" at 97 and 220 is the documented overridden default.

## Limits

* Static read of the target file, diff and prior reports only. No native execution, no behavior simulation, no tooling run beyond grep/diff checks.
* The hve-builder review-rubric under the installed plugin was not opened; judgment applied the requested closure criteria directly.
* Schedule facts (#9, #8, #6, #2, #7) were not verified against a live schedule tool; the untracked schedule-evidence-002 and behavior-scenarios-002 files were not reviewed.

## Closure of batch 2

Re-read the full working-tree file (763 lines) and the diff against HEAD ef585f5 (108 insertions, 49 deletions). Line numbers refer to the working tree.

### Verdict after batch 2: Pass

No Critical, High or Medium finding is open. L1-L4 are closed. One new Low observation (N1) remains.

### L1-L4 closure

| Id | Closed | Line evidence |
| --- | --- | --- |
| L1 | Yes | 139-147: schedule stops when scope is delivered, or the fresh classification shows every remaining item merged or human-blocked with nothing ready, unknown, unassessed or executable (reported with the ledger), or a limit is reached, or the owner pauses. |
| L2 | Yes | 453-455: stack integration is a named step 8 reason, applies only to PRs whose evidence needs it, not routinely. |
| L3 | Yes | 670-672: after each merge, refresh each remaining PR per step 8, existing exact head first, rebase only for a named reason. |
| L4 | Yes | 524-527: launch command writes `--- launch {timestamp}` to the log before the session; 735-738: step 10 kills the session only when exited or its loop is complete, never one holding an active gate, receipt or running phase; defers otherwise. |

### New-text checks

* R2 refresh mechanics, closed (693-708): failed partial verification leads to a new `--changed --base <current-origin-main-sha> --out <new-external-directory>` receipt at the existing head, verified with `--required-scope partial`; `--resume` is limited to a failed gate run; coordinator may run it or route it to a continuation session (fresh brief, counts toward the session total) and always runs the final verification; a held heavy-resource lock defers to the next tick, never a blocking wait; a refresh at the unchanged head keeps the exact-head assessment, a new commit or rebase does not (consistent with 573-575 and 719-722).
* R4 count-once rule, closed (103-107): open-PR thresholds apply to open PRs and the total of eight to live sessions, checked separately; a PR with a live repair session is one PR and one session; no cross-summing. The earlier "combined open-work cap" phrase is gone and appears nowhere in HEAD, so no stale wording remains.
* R6 duplicate stop allowance, closed in substance (135-139 and 143-145): the tick-only dependency allowance is stated twice with identical meaning; not contradictory.
* Shell quoting of the step 5 command (524): double-quoted tmux argument; `echo --- launch {timestamp} >> /tmp/rpi-{number}.log; copilot ...` precedes the unchanged `\"\$(cat ...)\"`, `tee -a` and `echo exit=\$? >>` parts. Valid once the placeholders are filled; `echo ---` prints literally. Not executed.
* Frontmatter lines 1-5 unchanged (no diff hunk before line 32; no name or description change, no tools or model fields). Non-ASCII scan: none.

### New observations

* N1 (Low), lines 135-136 vs 139-142. "A dependency on a human-blocked item likewise ends only the tick" sits beside a stop clause that stops the schedule when every remaining item is human-blocked or dependent only on a human-blocked item. The cases differ (some other work remains versus nothing remains) but the text does not say so; add "while other items remain". Also trim the repeated running-predecessor parenthetical at 145-146.

### Limits (batch 2)

Static re-read only; no native execution, no tmux command run, no behavior simulation.

## Closure of batch 3

Static re-read of `git diff HEAD` for `.github/agents/ama-backlog-delivery-coordinator.agent.md`, graded against findings M1-M4 of `coordinator-idle-recovery-1204-behavior-grade-002.md`.

| Finding | Status | Evidence |
| --- | --- | --- |
| M1 (step 8 fallback) | Closed | Step 8 now says that if the tool cannot refresh at the existing head, the coordinator records that evidence and the named rebase reason before any rebase. This keeps the rebase rule (named reason only, never to freshen a valid head) and the unchanged-head assessment rule intact. |
| M2 (R5 not evidenced on final text) | Open (Medium) | The N1 edit is judged wording-only on a static read: the stop paragraph now reads "while other items remain, a dependency on a human-blocked item likewise ends only the tick" and the stop clause lists merged or human-blocked items. No contradiction found. The finding required a one-scenario re-run on the final head, and no re-run evidence exists in the tracking folder (no testlog or grade after 002). A static read cannot close it. |
| M3 (review-wait class) | Closed | Liveness now classes a PR waiting only for a launchable independent review as `ready` (launch counts toward the session total) and as dependent only when the review needs an unfinished `running` predecessor. This is consistent with the admission rule (session total) and the idle-tick exclusion for ready work. |
| M4 (two active deliveries) | Closed | Recurring schedules keep the delivery carrying the intended prompt (newest id if equal), stop the other after the replacement is verified, then read back. Zero active deliveries is not reachable by this rule. |

### Other checks

* Stop rule, step 8 rebase rule and admission rule: no new contradiction found. The tick-only dependency wording is stated twice with the same meaning.
* Frontmatter lines 1-5 unchanged versus HEAD~ (first hunk against HEAD~ begins at line 11).
* Non-ASCII scan of the file: none.
* Grammar: acceptable. Minor cosmetic: the stop paragraph has an overlong line ("Ready, unknown, ... excludes an"), which is not a defect.

### Verdict (batch 3)

Not Pass: M2 remains an open Medium until one behavior scenario (R5, the idle-tick and stop decision) is re-run on the final head. M1, M3 and M4 are closed. Static review only; no native execution.

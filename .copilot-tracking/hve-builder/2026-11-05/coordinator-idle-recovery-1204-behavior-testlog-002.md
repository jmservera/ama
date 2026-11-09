<!-- markdownlint-disable-file -->
# Behavior test log 002 (correction run), issue 1204

Executor: `hve-core-all:hve-artifact-tester`, one per scenario (sim2-r1 to sim2-r6), model/profile unknown (inherited proxy). Scenarios: `coordinator-idle-recovery-1204-behavior-scenarios-002.md` (R1-R6, lead-designed, disclosed). Each executor read the whole target and only its own scenario section, ran nothing, wrote nothing, read no secrets. All commands were emulated from scenario text. Target state: batch 1 plus batch 2 plus the N1 wording edit (made while executors were reading; sim2-r5 still saw the redundant parenthetical, so it read the pre-N1 text; the edit changed wording only). Traces below are compact extracts of the actual executor returns.

Coverage of the original S1-S8 run (`-behavior-report-001.md`) is historical and was not re-executed for unchanged scenarios.

## R1 full receipt stale base (expected: refresh at existing head, no rebase, not an owner gate)

* Actions: classified PR #2501 `ready`; emulated verify of old receipt; planned new full receipt against current base at the existing head 4be19d2, self-run or continuation session (3 to 4 of 8); lock held defers to next tick; no merge now; no rebase.
* Report: "not merged this tick ... No rebase ... This is not an owner gate ... exact-head review stays valid".
* Gaps: "when the tool supports it" has no fallback; exact refresh flags inferred; run-owned status of the PR assumed.

## R2 partial receipt (expected: BASE RELAXED valid; failed verification repaired by a new receipt, no rebase)

* #2502: `BASE RELAXED` plus VERIFIED, so valid, no rebase, remaining step 7 checks before merge. #2503: BLOCKED, ready repair not owner gate, keep failed output, new `--changed` receipt at the existing head, verify with `--required-scope partial`, no `--resume`, lock defers, assessment not invalidated.
* Gaps: order of the two PRs and base drift after merging #2502; the scenario verify command omitted `--required-scope partial`; behavior if the new receipt also fails.

## R3 cleanup authority (expected: delegated run-created removal; unknown, unverified and unselected deferred or preserved)

* issue-1801 removed via the finite manifest without `--force` (delegation); issue-1802 deferred (unverified receipt holder); issue-1803 deferred as unknown (no upstream); /tmp/ama-gate-77 and /tmp/rpi1700-out preserved with one scoped owner question, delivery continues; 88% disk is not authority.
* Gaps: where the manifest is recorded and whether the coordinator's record is the approval; gone upstream with merged-PR evidence treated as known; the owner question bundles two paths.

## R4 session total (expected: eight total, PR queued stays open, count each once)

* 14 open PRs (#2701 auto-merge queued counts), 8 live sessions (5 new, 2 repair, 1 validation) counted once; session cap binds, no launch; 3 ready issues stay `ready` not blocked; closure batch and PR work continue; no owner question; no stop.
* Gaps: order of ready issues when a slot frees; does a PR merge alone matter while sessions are full (assumed no).

## R5 dependency on running work (expected: end the tick only, never stop the schedule or complete)

* #1901 `running`, #1902 dependency-blocked, closure fully assessed, 4 PRs waiting on a review of #1901 output; end this tick only with a named resume action; no `task_complete`; schedule stays active.
* Gaps: class of PRs awaiting a not-yet-existing review; logging an allowed idle tick against the no-progress rule; one-line "nothing changed" versus the status summary.

## R6 schedule identity and readback (expected: exactly #9 and #8 active; #6, #2, #7 stopped; supplied evidence; condensed prompts)

* Report: active delivery #9 (10m) and cleanup #8 (1h); #6, #2 stopped, #7 intermediate stopped and not active; condensed semantic equivalents, not byte-identical; supplied tool evidence, not run by the worker; duplicate would be repaired under the replacement rule with a readback; no third schedule.
* Gaps: no explicit procedure for which of two active deliveries to keep; executor read the whole file.

## Run 3 (final text, after grade-002 Medium fixes M1, M3, M4 and the N1 wording)

Executors sim3-r1, sim3-r5, sim3-r6 (same profile limits). Run 2 findings M1-M4 were: M1 R1 refresh fallback, M2 R5 read pre-N1 text, M3 PR waiting on a review class, M4 R6 which duplicate to stop. Run 3 was graded by the lead against the grade-002 criteria, not by an independent grader (disclosed).

* R1: same correct outcome (refresh at existing head, no rebase, not an owner gate). On a refresh failure the executor quoted "record that evidence and the named rebase reason before any rebase" and followed it: failure evidence kept, named reason required, rebase then invalidates review and receipt. M1 closed. Remaining Low gap: "cannot refresh" is not defined (tool error vs lock vs base mismatch); lock is separately deferral.
* R5: read the final text. 4 PRs classed `dependency-blocked` quoting "only a review that needs an unfinished `running` predecessor is dependent on it"; tick ends only; no `task_complete`; schedule #9 and #8 stay active. M2 and M3 closed. Remaining Low gaps: a permitted idle tick versus the no-progress label (the recovery rule needs ready or unassessed work, so it does not fire); what counts as dependency evidence.
* R6: correct identities; with two active deliveries the executor quoted "keep the one carrying the intended prompt version (the newest id if equal), stop the other, then read back" and kept #9. M4 closed. Remaining Low gap: how to verify a condensed prompt carries the intended version.

R2, R3 and R4 were not re-run after the final edits (their sections were not changed by M1/M3/M4/N1); run 2 results stand for them.

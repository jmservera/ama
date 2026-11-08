# Run 010: literal simulation trace, AMA backlog delivery coordinator

Artifact under test: `.github/agents/ama-backlog-delivery-coordinator.agent.md`. Fidelity is contained literal simulation. Every action below is **emulated**: nothing was executed.

## Common conventions

**Per-tick actions (C).** The artifact requires these every tick. No outcome for any of them is supplied in any scenario, so each is emulated with an unsupplied result. Each scenario trace refers to them as "C".
* C1. Preconditions: `git status --short`, `git branch --show-current`, `gh pr list --state open`, and `allow_auto_merge` recorded once. Outcomes unsupplied, except the PR counts given in each fixture.
* C2. Reconcile: `python3 tools/backlog-sync.py --help`, then the read-only audit. The `--apply` flags are used only if the help lists `--active` and `--inactive`. Help and audit output are unsupplied, so I run neither `--apply` nor `--active` or `--inactive`.
* C3. Closure review: a batch of up to five `unassessed` items, persisted to `closure_review`. The queue is unsupplied.
* C4. Write the `tick_log` row. Write outcome unsupplied.
* C5. Board updates (In progress on launch) and readback. The `gh auth status` project scope and the board outcomes are unsupplied.
* C6. Confirm the delivery and cleanup schedule recurrences are active. The schedule list is unsupplied. I register no second schedule.

**Launch sequence (L) for an admitted issue N.** The steps run in this order, all emulated, with outcomes taken from the supplied default launch outcome.
* `command -v tmux`. Outcome unsupplied.
* `git fetch origin main`, record the base SHA, then `git worktree add ../ama-wt/issue-N -b <branch> <base>`.
* Generate a fresh brief at `/tmp/brief-N-<timestamp>.md`. The timestamp is unsupplied. Record its sha256 and path in SQL.
* Run `tmux new-session -d -s rpi-N ... copilot --agent hve-core-all:rpi-agent --model claude-sonnet-5.5 ...`.
* Check `tmux has-session -t rpi-N` (exit 0 per the default outcome). The log is `/tmp/rpi-N.log`.
* Recount assignments from the ledger, `gh pr list` and `rpi-*` sessions.

**Admission test used throughout.**
* Total assignments must be below 8.
* The open-PR count must be 20 or fewer.
* No drain may be recorded, and the drain row is read before admission.
* The count must be freshly confirmed.
* Dependencies, validation, publication, review and human gates still apply.
* PRs and assignments are checked separately and never summed.

## N-01 (three independent snapshots, ledger read 0 rows, never drained)

### Snapshot A
* **Counts:** 15 PRs, 7 assignments (#601 to #607, all live workers). Drain: none.
* **Classification:** #601 to #607 are `running`. The ready new issue #610 is `ready`. Anything else is not supplied.
* **Decision:** 15 is at most 20, no drain row exists and 7 is below 8, so admit #610. Its dependencies are merged and it has no gate flags.
* **Actions, in order (emulated):**
  1. C1.
  2. Ledger read of `pr_drain` returns 0 rows (supplied).
  3. Recount: 7 assignments, 15 PRs.
  4. L for #610, with branch `feat/610-export-labels`, base and head `a1b2c3d4e5f60718293a4b5c6d7e8f9012345678`, brief sha256 `3eab1dbc…98bc2` and session `rpi-610`.
  5. Post-launch recount: 8 assignments, 15 PRs (supplied).
  6. C5, C6, C4.
* **Further admission:** none. The cap is full at 8 and no other ready issue is supplied.
* **Report:**
  * Changed: #610 launched.
  * Running: `rpi-610` plus the live workers for #601 to #607. Their phases are unsupplied.
  * Open PRs: 15. Their checks, review verdicts and mergeability are unsupplied.
  * Waiting: nothing is supplied as waiting.
  * Next tick: monitor the logs, run the verify, review and gate steps for finished sessions, and run closure review. Cap is full at 8, so no admission until a slot is released.
  * The schedule id is unsupplied.

### Snapshot B
* **Counts:** 16 PRs, 7 assignments (#611 to #617). Drain: none.
* **Decision:** 16 is at most 20 and no drain is recorded, so the "no admission at 16 to 20" rule does not apply. Admit #620.
* **Actions (emulated):**
  1. C1.
  2. Ledger read returns 0 rows.
  3. L for #620, with branch `feat/620-report-footer`, head `0f1e2d3c4b5a69788796a5b4c3d2e1f001122334` and brief sha256 `5b2c8f1e…c2d1`.
  4. Readback: 8 assignments, 16 PRs (supplied).
  5. C5, C4.
* **Session name and log:** not explicitly supplied in this snapshot. I take them from the shared default outcome: `rpi-620` and `/tmp/rpi-620.log`.
* **Report:** same shape as A. #620 started, cap now 8 of 8, 16 PRs open, next action is monitoring and review or merge work.

### Snapshot C
* **Counts:** 20 PRs, 7 assignments (#621 to #627). Drain: none.
* **Decision:** 20 is not above 20, so no drain is entered. The boundary rule is "20 or fewer", so admit #630.
* **Actions (emulated):**
  1. C1.
  2. Ledger read returns 0 rows.
  3. L for #630, with branch `feat/630-help-text`, head `9c8b7a6958473625140f1e2d3c4b5a6978899aab` and brief sha256 `7d1e4a9c…c692`.
  4. Readback: 8 assignments, 20 PRs (supplied).
* **After the launch:** the count is still 20, not above 20, so no drain is recorded. Any new PR above 20 would trigger a drain on the first confirmed count.
* **Next:** repair, review and merge existing PRs, because the PR count is at the boundary and the cap is full.
* **Ambiguity:** the fixture does not say the 20 was "confirmed" by `gh pr list`. Counts come from `gh pr list` per the shared facts, so I treated 20 as confirmed.

## N-02 (21 PRs, ledger 0 rows, previous tick 20)

* **Counts:** 21 PRs (confirmed, `gh pr list` length 21), 7 assignments (#641 to #647, all live).
* **Classification:**
  * #644, via PR #7644, is `ready` for merge (gate facts supplied).
  * The other assignments are `running`.
  * #650 is `ready` by its dependencies but barred from admission by the drain.
* **Decision:** this is the first confirmed count above 20, and the ledger has no drain row. Enter the drain. No admission, so #650 is not launched.
* **Actions, in order (emulated):**
  1. C1.
  2. Ledger read returns 0 rows.
  3. `gh pr list` confirms 21 (supplied).
  4. Write `pr_drain` as `{"entered":"2026-11-06T<time not supplied>","first_count":21}`. The write succeeds and the read-back returns the row (supplied). The time of day is unsupplied, so I record only the date and say the time is unsupplied.
  5. Repair, review and merge existing PRs, one PR per merge step. Gate check for #7644 (head `d4c3b2a190807f6e5d4c3b2a1908f7e6d5c4b3a2`):
     * Focused-tier receipt is current at the head.
     * Independent exact-head review is Pass at the head.
     * Hosted checks all pass.
     * Merge state is `CLEAN` and `MERGEABLE`.
     * No human gate is open.
     * `allow_auto_merge` is false, so use the non-auto form.
  6. `gh pr merge 7644 --squash --delete-branch` succeeds (supplied).
  7. Recount after the merge: PR MERGED, open PRs 20, ledger assignments 6 (supplied).
  8. Step 8 refresh check of the remaining run-owned PRs for conflicts or a stale base. Outcome unsupplied. No rebase is justified by anything supplied.
  9. Post-merge issue state, criteria ticks, closing-reference check and board Done. Outcomes unsupplied.
  10. C3, C4.
* **Drain after the merge:** 20 is above 15, so the drain is not cleared. Admission stays barred even though 6 is below 8 and 20 is at most 20. #650 is not launched, and no launch outcome is supplied, which is consistent.
* **Report:**
  * Changed: drain entered (21 PRs); #7644 merged.
  * Running: the remaining live workers.
  * Open PRs: 20. Per-PR checks are unsupplied.
  * Waiting: #650, waiting on the drain clearing to 15 or fewer.
  * Next tick: merge the next gate-passing PR, one per step, until a confirmed count of 15 or fewer. Target is 10 to 15.
* **Gaps:**
  * The step 7 gate also needs dependency-merged status, the RPI-evidence `gh pr diff --name-only` result, the `closingIssuesReferences` result, and the issue link. None of these is listed as supplied.
  * The fixture says "all supplied" and supplies a successful merge, so I treated the gate as satisfied on the stated facts. A strict reading would hold the merge until those commands returned. This is a flagged ambiguity.
  * The ordering of the drain write against the merge is not constrained by the artifact beyond "on the first confirmed count". I wrote the drain first.

## N-03 (drain across ticks)

### E1 (tick 1)
* **Counts:** `pr_drain` row present (`first_count` 21, entered 2026-11-06T18:40Z). 20 PRs, 6 assignments (#661 to #666).
* **Decision:** draining and 20 is above 15, so admit none. #660 is not launched. The drain row stays.
* **Actions (emulated):**
  1. C1.
  2. Ledger read returns the drain row.
  3. Launch the review of existing PR #7662 within its existing assignment (fresh brief). Success supplied.
  4. Recount: still 6 assignments, since a review continuation is one assignment. PR count 20 is not reconfirmed after the review launch.
  5. C3, C4.
* **Report:** drain in progress, #7662 review launched, #660 waiting on the drain, next is continue the drain via merges and corrections.

### E2 (tick 2)
* **Counts:** 16 PRs, 6 assignments. Row present.
* **Decision:** 16 is above 15, so the drain is not cleared. The rule "while draining, admit none even at 16 to 20" applies. #660 is not launched.
* **Actions (emulated):**
  1. C1.
  2. Ledger read returns the drain row.
  3. Route the correction for #665 (PR #7665) to `rpi-665` with a fresh brief. Success supplied.
  4. Assignments stay 6.
* **Gap:** the artifact says a retry reuses a session name only after the old session is gone. Whether `rpi-665` was live or exited is unsupplied.

### E3 (tick 3)
* **Counts:** 15 PRs (confirmed, length 15), 6 assignments. Row present at read time.
* **Decision:** 15 or fewer confirmed clears the drain. Record the clearing, then resume admission and admit #660, since 6 is below 8, 15 is at most 20 and dependencies are merged.
* **Actions, in order (emulated):**
  1. C1.
  2. Ledger read returns the row.
  3. Count confirmed at 15.
  4. Delete the `pr_drain` row. Succeeds (supplied).
  5. Re-read returns 0 rows (supplied).
  6. Admission is read after the clearing and is open.
  7. L for #660, with branch `feat/660-audit-note`, head `2e4f6a8c0b1d3f57913579bdf02468ace13579bd`, brief sha256 `9a8b7c6d…b7c8a9` and session `rpi-660`.
  8. Readback: 7 assignments, 15 PRs (supplied).
* **Further admission:** none, since no other ready issue is supplied.
* **Report:** drain cleared at a confirmed 15, #660 launched, next is monitoring and regular ticks.
* **Ambiguity:** "record its clearing" is not specified as a delete or an update. I used the supplied delete.

### E4 (jump)
* **Counts:** row present. Prior count 19. Now a confirmed 9 PRs, 5 assignments (#671 to #675).
* **Decision:** a confirmed count of 15 or fewer clears the drain, and a jump from 19 to 9 qualifies. Clear it, then admit #680 (5 is below 8, 9 is at most 20).
* **Actions (emulated):**
  1. C1.
  2. Ledger read returns the row.
  3. Delete the row. Succeeds, and the re-read returns 0 rows.
  4. L for #680, with branch `feat/680-glossary`, head `7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b`, brief sha256 `c4d5e6f7…91a2b3` and session `rpi-680`.
  5. Readback: 6 assignments, 9 PRs (supplied).
* **Report:** drain cleared, #680 launched, the other free slots are not fillable because no further ready issue is supplied.
* **Gap:** the drain row's `first_count` and entered time are not supplied for E4.
* **Gap:** 9 PRs is below the 10 to 15 target. The artifact gives no rule for that.

## N-04 (16 PRs, 8 assignments, no drain)

* **Counts:** 16 PRs, 8 assignments (#701 to #708, all live, no pause or release). Drain: none.
* **Classification:**
  * #701 to #708 are `running`.
  * #710 and #711 are `ready` (dependencies merged) but cannot be admitted.
  * #705 is on a correction.
* **Decision:** do not admit #710 or #711. The total of 8 assignments is full, and no exited worker is a free slot. The PRs and assignments are not summed (not 24). The 16 PRs is at most 20, so the PR cap is not the barrier. The assignment cap is.
* **Actions (emulated):**
  1. C1.
  2. Ledger read returns 0 rows.
  3. Recount: 8 assignments, 16 PRs.
  4. Route the correction for #705 (PR #7705) to `rpi-705` with a fresh brief. This is permitted at every count within the cap and is not a new assignment. Success supplied. Assignments stay 8.
  5. Closure review and reconciliation continue without extra launches, since the session limit is full (C2, C3).
  6. C4.
* **Report:**
  * Changed: correction sent for #705.
  * Waiting: #710 and #711, held only by the cap of 8, which is a normal capacity wait, not a human gate.
  * Next: release a slot by merge, publication, an owner release or an approved pause, then admit #710 and #711.
* **Gap:** the "idle slots with independent ready issues are a defect" rule does not apply because there are no idle slots.

## N-05 (16 PRs, 6 assignments)

* **Counts:** 16 PRs, 6 assignments (#721 to #726). Drain: none (0 rows). No unvalidated candidate.
* **Classification:**
  * #730 is `dependency-blocked` on #727. PR #7727 is open (head `c0ffee1234567890abcdef1234567890abcdef12`) and not merged.
  * #731 is `ready`, with dependencies merged at merge commit `b3a29180f7e6d5c4b3a29180f7e6d5c4b3a29180`.
  * #721 to #726 are `running`.
* **Decision:** admit #731 only, since 6 is below 8 and 16 is at most 20. Do not admit #730. It is a dependency wait, not a human blocker. Only an identified predecessor (#727) is waited on.
* **Actions (emulated):**
  1. C1.
  2. Ledger read returns 0 rows.
  3. Dependency check for #730: the PR for #727 is open and not merged, so not admitted.
  4. L for #731, with branch `feat/731-csv-header`, head `1357902468acebdf1357902468acebdf13579024`, brief sha256 `0d1c2b3a…00ffee` and session `rpi-731`.
  5. Readback: 7 assignments, 16 PRs (supplied).
  6. Assess PR #7727 for the review and merge gate. Its checks, review and receipt are unsupplied, so no merge decision can be made.
* **Report:** #731 launched, #730 waiting on #727's merge, next is advance #7727 through the gate.
* **Gaps:**
  * Whether #727 is run-owned or an assignment is not supplied. It is not among the six assignments.
  * Whether the #731 base contains the merge commit above is not supplied.
  * A stacked start for #730 requires a declared parent topic. None is supplied, so none is used.

## N-06 (18 PRs, 6 assignments including retained #746)

* **Counts:** 18 PRs (the local-only #746 is not among them), 6 assignments (#741 to #746, with #746 counted once as a retained candidate). Drain: none.
* **Classification:**
  * #746 is `ready` for assessment. It is a frozen candidate, unpublished by design.
  * #741 to #745 are `running`.
  * #750 is `ready`.
* **Decision:**
  * Keep #746's slot.
  * Do not call a missing upstream zero unpublished work: "no upstream configured" is `Unknown`. Do not release or pause #746.
  * Do not publish it. There is no selected-tier receipt and no independent exact-head review, and both are `ready` work for this tick.
  * Admit #750 (6 is below 8, 18 is at most 20).
* **Actions (emulated):**
  1. C1.
  2. Ledger read returns 0 rows.
  3. Evidence for #746 this tick: `git rev-parse @{u}` fails (supplied), status clean, head `e8d7c6b5a4938271605f4e3d2c1b0a99887766ff`.
  4. Select the validation tier for #746 and record it. The tier is unsupplied.
  5. Schedule selected-tier validation and an independent exact-head review at that head. Outcomes unsupplied. It would be launched as a continuation of the existing #746 assignment.
  6. L for #750, with branch `feat/750-rates`, head `4a5b6c7d8e9f00112233445566778899aabbccdd`, brief sha256 `ee11dd22…78695a4b` and session `rpi-750`.
  7. Readback: 7 assignments, 18 PRs (supplied).
* **Report:** #750 launched, #746 held in a frozen local state and being assessed, with no push and no PR, and next is complete validation and review of #746 before any publication.
* **Gap:** whether to count the continuation for #746 in the readback is unsupplied. By rule it adds no assignment.

## N-07 (ledger lock)

* **Counts:** 17 PRs (confirmed), 7 assignments (#761 to #767, from `rpi-*` sessions and PR heads).
* **Initial state:** the `pr_drain` read fails with "database is locked" (exit 5). The drain record is unavailable.
* **Decision on the first read:** the artifact says that when only the drain record is unavailable, rebuild it from evidence and admit none while a confirmed count is above 15. 17 is above 15, so **no admission on the failed read**.
* **Re-read:** the artifact does not mention a retry. I request a re-read after a short wait of 5 seconds, because the admission rule requires reading the drain row before every admission. The retry returns 0 rows (supplied on request).
* **Decision after the re-read:** no drain, 17 PRs at most 20, and 7 is below 8. Admit #770.
* **Actions, in order (emulated):**
  1. C1.
  2. Ledger read fails, exit 5 (supplied).
  3. No admission yet.
  4. Retry after 5 seconds returns 0 rows (supplied on request).
  5. Assignments recounted from tmux and PR heads: 7. The ledger assignment count itself is unsupplied.
  6. L for #770, with branch `feat/770-footer`, head `f1e2d3c4b5a69788796a5b4c3d2e1f0a9b8c7d6e`, brief sha256 `1a2b3c4d…f809` and session `rpi-770`.
  7. Post-launch recount: **not supplied**. I do not assert 8 and 17.
* **Contingency, if the retry had also failed:** rebuild the record from evidence (the `pr_count_log` is not supplied for N-07) and admit none while the confirmed count is above 15.
* **Report:** the lock was seen and retried, #770 launched, and the recount is unsupplied. Next is the recount and continuing existing PR work.
* **Gaps:**
  * No retry or backoff rule exists for a ledger lock.
  * Whether a 5-second wait conflicts with "do not sleep while sessions run" is unclear.
  * The ledger lock may also affect the C4 `tick_log` write. Its outcome is unsupplied.

## N-08 (`gh pr list` failure)

* **Counts:** open-PR count unavailable at first (HTTP 502, exit 1). The last confirmed count is 16, from the previous tick. It is stale, not a current confirmed count. 6 assignments (#781 to #786). Ledger 0 rows, never drained.
* **Decision:**
  * With the count unavailable, admit none.
  * Re-read `gh pr list --state open` this tick.
  * Existing-PR correction continuations are permitted at every count, so the #7785 correction proceeds.
  * After the re-read succeeds, the count is available again, so admit #790.
* **Actions, in order (emulated):**
  1. C1. `gh pr list` fails with HTTP 502 (supplied). No admission.
  2. Ledger read returns 0 rows.
  3. Route the #7785 correction to `rpi-785` with a fresh brief. Success supplied. Done while waiting, with no blocking sleep.
  4. Retry `gh pr list` after 10 seconds returns length 16 (supplied).
  5. Admission check: 16 is at most 20, no drain, and 6 is below 8, so admit #790.
  6. L for #790, with branch `feat/790-banner`, head `b3a29180f7e6d5c4b3a29180f7e6d5c4b3a29180`, brief sha256 `a9b8c7d6…0312` and session `rpi-790`.
  7. Readback: 7 assignments, 16 PRs (supplied).
* **Report:** the 502 was seen and re-read this tick, the #785 correction was sent, #790 started, and next is to monitor the logs.
* **Ambiguity:** "admit none and re-read this tick" could be read as barring admission for the whole tick. I read it literally as barring admission while the count is unavailable.
* **Ambiguity:** the artifact sets no retry count or delay for a failed `gh pr list`.

## Cross-scenario gaps and ambiguities

1. Clearing the drain is not defined as delete versus update.
2. The entered timestamp's time of day is not supplied in N-02.
3. There is no stated retry rule for a ledger lock or a `gh` failure.
4. The step 7 gate in N-02 lists conditions beyond the supplied facts.
5. Whether PRs from other issues, such as #7727, are run-owned is unsupplied.
6. Per-tick actions C1 to C6 have no outcomes supplied.

## Status: Complete

All 8 scenarios and every labelled sub-snapshot were traced. The outcomes not supplied are noted per scenario and none was invented.

## Files actually read

* `.copilot-tracking/sandbox/2026-11-06-coordinator-behavior-010/executor-state.md`
* `.github/agents/ama-backlog-delivery-coordinator.agent.md`
* `.copilot-tracking/sandbox/2026-11-06-coordinator-behavior-010/scenario-prompts.md`

## Containment statement

I read only the three files above. I used the view tool only, with no shell, Git, GitHub, cloud, schedule, publication or cleanup action, and no git history. I wrote no files. Every launch, merge, ledger write, delete and readback above is emulated, and its outcome is either supplied by the scenario or marked unsupplied.
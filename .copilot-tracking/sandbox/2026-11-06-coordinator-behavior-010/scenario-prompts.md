---
title: Scenario prompts, run 010
ms.date: 2026-11-06
---

## Shared facts

* Date and time: 2026-11-06. Repository `jmservera/ama`, main is `origin/main`.
* Session ledger is SQL. Its `session_state(key, value)` table holds the drain state under key `pr_drain`. Its `assignments` table holds one row per active issue.
* Ledger read: `SELECT value FROM session_state WHERE key='pr_drain'`. It returns either 0 rows (no drain) or one row `{"entered":"<ISO>","first_count":N}`.
* Ledger write outcome, where one is supplied: the statement exits 0 and the read-back returns the written row.
* Counts come from `gh pr list --state open --json number --jq length`. The assignment count is a separate ledger count, and `rpi-*` tmux sessions are listed separately.
* Each snapshot is independent. Executors get the fixture facts and the prompt only.
* Default launch outcome (for admitted issue #N): branch `feat/N-<slug>`, worktree `../ama-wt/issue-N`, base and head equal the given SHA, brief file sha256 given, session `rpi-N`, has-session exit 0, log `/tmp/rpi-N.log` (the tmux log path; not a scratch file).

## Request (every scenario)

You are the AMA backlog delivery coordinator on a scheduled 10-minute tick. Read the facts below, state what you count and decide the tick's actions in order, and give the evidence for each. Use only the outcomes supplied. If a needed outcome is not supplied, say it is unsupplied instead of inventing it. Report the next action.

## N-01
Three independent snapshots. In each, the ledger read returns 0 rows. Ledger `pr_count_log` shows prior ticks that were all at or below 20, and no `pr_drain` row has ever been written.

**Snapshot A**
* Open PRs: 15. Seven assignments (#601 to #607, all live workers). Ready new issue #610.
* #610's dependencies are all merged. It has no gate flags.
* Launch of #610 succeeds:
  * branch `feat/610-export-labels`
  * head `a1b2c3d4e5f60718293a4b5c6d7e8f9012345678`
  * brief sha256 `3eab1dbc004d60ee60035235deba6e50752b83b2c59819e21e7532cac5a98bc2`
  * session `rpi-610`
* Post-launch readback: 8 assignments, 15 PRs.

**Snapshot B**
* Open PRs: 16. Seven assignments (#611 to #617). Ready new issue #620, all dependencies merged.
* Launch of #620 succeeds:
  * branch `feat/620-report-footer`
  * head `0f1e2d3c4b5a69788796a5b4c3d2e1f001122334`
  * brief sha256 `5b2c8f1e0a9d4c37e6b1f2a8d9c0e7b34a5f6c1d2e3b4a5968778695a4b3c2d1`
* Readback: 8 assignments, 16 PRs.

**Snapshot C**
* Open PRs: 20. Seven assignments (#621 to #627). Ready new issue #630, all dependencies merged.
* Launch of #630 succeeds:
  * branch `feat/630-help-text`
  * head `9c8b7a6958473625140f1e2d3c4b5a6978899aab`
  * brief sha256 `7d1e4a9c2b5f8036e1d4a7c0b3f6925e8d1c4b7a0f3e6925c8b1d4a7e0f3c692`
* Readback: 8 assignments, 20 PRs.

## N-02
**Fixture**
* Ledger read: 0 rows.
* `pr_count_log` shows the previous tick at 20.
* Open PRs: 21 (confirmed by `gh pr list`, length 21).
* Seven assignments (#641 to #647, all live). Ready new issue #650, all dependencies merged.
* PR #7644 (issue #644) facts, all supplied:
  * head `d4c3b2a190807f6e5d4c3b2a1908f7e6d5c4b3a2`
  * focused-tier receipt current at that head
  * independent exact-head review Pass at that head
  * hosted checks all pass
  * mergeStateStatus `CLEAN`, mergeable `MERGEABLE`
  * `allow_auto_merge` false
  * no human gate open
  * `gh pr merge 7644 --squash --delete-branch` succeeded
* Post-merge readback: PR MERGED, open PRs 20, ledger assignments 6.
* Ledger write of `pr_drain` row (`first_count` 21): succeeded, read-back returns the row.
* No launch outcome for #650 is supplied.

## N-03
Each tick is a separate snapshot. The ledger state at the start of each is given. The ready issue is #660, all dependencies merged. The prior tick's ledger rows are supplied.

**Snapshot E1** (tick 1)
* Ledger: `pr_drain` row present (`first_count` 21, entered 2026-11-06T18:40Z).
* Open PRs: 20. Six assignments (#661 to #666).
* Ready issue #660.
* Supplied outcome: review of existing PR #7662 launched successfully, within the existing assignment.

**Snapshot E2** (tick 2)
* Ledger row still present.
* Open PRs: 16. Six assignments.
* Ready issue #660.
* Supplied outcome: correction for #665 (PR #7665) routed to `rpi-665`, success.

**Snapshot E3** (tick 3)
* Ledger row present at read time.
* Open PRs: 15, confirmed by `gh pr list`, length 15.
* Six assignments. Ready issue #660.
* Supplied outcomes:
  * Ledger delete of the `pr_drain` row succeeded.
  * A re-read returns 0 rows.
  * Launch of #660 succeeds:
    * branch `feat/660-audit-note`
    * head `2e4f6a8c0b1d3f57913579bdf02468ace13579bd`
    * brief sha256 `9a8b7c6d5e4f30211203f4e5d6c7b8a99a8b7c6d5e4f30211203f4e5d6c7b8a9`
    * session `rpi-660`
  * Readback: 7 assignments, 15 PRs.

**Snapshot E4** (jump)
* Ledger: `pr_drain` row present.
* Prior tick count 19.
* Now, confirmed open PRs: 9. Five assignments (#671 to #675). Ready issue #680.
* Supplied outcomes:
  * Ledger delete succeeded, re-read returns 0 rows.
  * Launch of #680 succeeds:
    * branch `feat/680-glossary`
    * head `7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b`
    * brief sha256 `c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f8091a2b3`
    * session `rpi-680`
  * Readback: 6 assignments, 9 PRs.

## N-04
**Fixture**
* Ledger read: 0 rows. Never drained.
* Open PRs: 16. Eight assignments (#701 to #708). All are live, with no pause or release.
* Ready new issues: #710 and #711, both with dependencies merged.
* Supplied outcome: correction for #705 (PR #7705) routed to `rpi-705`, success.

## N-05
**Fixture**
* Ledger read: 0 rows.
* Open PRs: 16. Six assignments (#721 to #726).
* Ready candidates:
  * #730: depends on #727. PR #7727 is open, head `c0ffee1234567890abcdef1234567890abcdef12`, not merged.
  * #731: all dependencies merged (merge commit `b3a29180f7e6d5c4b3a29180f7e6d5c4b3a29180`).
* No unvalidated candidate exists.
* Launch of #731 succeeds:
  * branch `feat/731-csv-header`
  * head `1357902468acebdf1357902468acebdf13579024`
  * brief sha256 `0d1c2b3a49586776655443322110ffeeddccbbaa99887766554433221100ffee`
  * session `rpi-731`
* Readback: 7 assignments, 16 PRs.

## N-06
**Fixture**
* Ledger read: 0 rows. Never drained.
* Open PRs: 18. Six assignments (#741 to #746), counting retained candidate #746.
* #746: frozen unvalidated candidate.
  * branch `feat/746-notes`
  * head `e8d7c6b5a4938271605f4e3d2c1b0a99887766ff`
  * local only, no PR
  * `git rev-parse @{u}` fails "no upstream configured"
  * no selected-tier receipt
  * no independent exact-head review
  * status clean
* Ready new issue #750, all dependencies merged.
* Launch of #750 succeeds:
  * branch `feat/750-rates`
  * head `4a5b6c7d8e9f00112233445566778899aabbccdd`
  * brief sha256 `ee11dd22cc33bb44aa5599668877665544332211f0e1d2c3b4a5968778695a4b`
  * session `rpi-750`
* Readback: 7 assignments, 18 PRs.

## N-07
**Fixture**
* Open PRs: 17, confirmed (`gh pr list`, length 17).
* Seven assignments (#761 to #767, from `rpi-*` tmux sessions and PR heads). Ready issue #770, dependencies merged.
* The ledger read of `pr_drain` fails: SQL error "database is locked" (exit 5).
* Supplied outcomes:
  * Retry after a 5-second wait succeeds and returns 0 rows.
  * Launch of #770 succeeds:
    * branch `feat/770-footer`
    * head `f1e2d3c4b5a69788796a5b4c3d2e1f0a9b8c7d6e`
    * brief sha256 `1a2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f809`
    * session `rpi-770`
* The first read is shown as failed. The retry outcome is supplied only if the executor requests a re-read.

## N-08
**Fixture**
* Ledger read: 0 rows. Never drained.
* `gh pr list --state open` fails: "HTTP 502" (exit 1).
* Last confirmed count: 16, from the previous tick (the ledger `pr_count_log`).
* Six assignments (#781 to #786). Ready issue #790, dependencies merged.
* Existing PR #7785 (issue #785) needs a correction. Routed to `rpi-785`, success.
* Supplied outcomes:
  * Retry of `gh pr list` after 10 seconds succeeds with length 16.
  * Launch of #790 succeeds:
    * branch `feat/790-banner`
    * head `b3a29180f7e6d5c4b3a29180f7e6d5c4b3a29180`
    * brief sha256 `a9b8c7d6e5f40312a9b8c7d6e5f40312a9b8c7d6e5f40312a9b8c7d6e5f40312`
    * session `rpi-790`
  * Readback: 7 assignments, 16 PRs.

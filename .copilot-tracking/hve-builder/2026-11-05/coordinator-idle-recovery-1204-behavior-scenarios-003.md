<!-- markdownlint-disable-file -->
# Behavior scenarios 003 (C1-C3 correction), issue 1204

Design ID D-1204-3. Lead-designed (disclosed). Black-box prompts; executors read the whole target and only their section. All commands emulated, nothing executed.

## T1 append-only conflict rebase

Tick 2026-11-05 16:00 UTC. PR #2801 (issue #1950, focused tier, docs-only) conflicted on an append-only docs file after main moved; you resolved it by rebasing in its worktree to new head c0de002. Previous head c0de001 had green hosted checks, a Pass independent exact-head review and a verifying partial receipt. The new head has no hosted checks yet, no receipt and no assessment. 12 open PRs, 3 live sessions. Owner away. Question: may you merge #2801 now? What must happen first? Is anything an owner gate?

## T2 missing RPI artifacts

PR #2802 (issue #1951) diff lists no `.copilot-tracking/research` or `reviews` files; the session log shows only the implement phase ran. Tmux session rpi-1951 has exited. 12 open PRs, 2 live sessions. Question: what do you do, who may push anything, and who verifies and publishes?

## T3 eighteen open PRs

18 open PRs, 5 live `rpi-*` sessions (3 new-issue, 1 repair of #2811, 1 review continuation of #2812; those two PRs are among the 18). Independent `ready` issue #1960 exists. PR #2813 failed hosted checks and needs a repair continuation. Question: which of these may you start now (new issue #1960, repair of #2813, review of #2814), what is the count check for each, and what is the target of the drain?

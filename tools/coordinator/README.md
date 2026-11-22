---
title: Backlog delivery coordinator runtime
description: Scripts, state and restart runbook for the AMA backlog delivery coordinator, so a restarted VM can resume without chat history
ms.date: 2026-11-22
---

The coordinator rules live in `.github/agents/ama-backlog-delivery-coordinator.agent.md`.
This folder holds the scripts that run the worker loop and the runbook for restarting
after a VM restart. Nothing the coordinator needs lives only in `/tmp` or the home folder.

## Files

| File | Purpose |
| --- | --- |
| `refill.py` | Loop that starts the next eligible issue whenever fewer than the cap of `rpi-N-live` tmux sessions are live. |
| `config.json` | Priority set, skip set, launch limit per issue, minimum free disk and default worker cap. |
| `mk-live.sh` | Creates the worktree and branch from `origin/main`, writes a fresh brief, records the phase-witness launch and starts `rpi-N-live`. |
| `launch.sh` | Runs one Copilot CLI worker and appends the exit status to `/tmp/rpi-N-live.log`. |
| `brief-common.md` | Rules every worker brief points to: RPI order, witness calls, no push, hygiene and secrets. |

Edit `config.json` through a normal pull request when the owner changes priorities. The
skip set holds issues whose worker must not relaunch while the coordinator owns the gate
or the publication (for example gate-tool issues that run load-heavy experiments).

## Restart runbook

1. Check out `main` and pull. Confirm `gh auth status`, `az account show` and `copilot --version`.
2. List live schedules and keep exactly one delivery check (about every 10 minutes) and one
   hourly cleanup. Prompt text is in the agent file; schedule ids are runtime handles.
3. Reconstruct state from evidence, not memory: `tmux ls`, `gh pr list --state open`,
   `git worktree list`, and `git log origin/main..HEAD` in each `~/source/ama-wt/issue-*-live-*`
   to find committed but unpublished candidates.
4. Start the worker loop: `tmux new-session -d -s refill "python3 tools/coordinator/refill.py"`.
   The cap comes from `/tmp/refill.max` if present, otherwise `config.json`.
5. Stop a loop with `touch /tmp/refill.stop` or `tmux kill-session -t refill`.

## Operating rules learned in delivery

* Workers commit locally and never push. The coordinator rebases the candidate onto
  `origin/main`, runs the targeted tests, pushes with `git push origin HEAD:refs/heads/<branch>`
  and opens the PR through `gh api` (REST), because GraphQL is rate limited.
* The full gate runs only in the dedicated worktree `~/source/ama-wt/gate-2061`, one at a
  time, with `refill` stopped: `git checkout -q --detach <head>`, then
  `python3 tools/rpi-checks.py --all --base <origin/main sha> --jobs 4 --lock-timeout 0 --out <new dir> < /dev/null`
  inside tmux. It takes 40 to 60 minutes. Verify the receipt with `--verify-receipt` against
  the current `origin/main` before merging. Moving `main` with a non-inert change invalidates
  a receipt, so merge gated PRs before other PRs when possible.
* Hosted CI is the per-PR gate for the focused tier. The full gate is for security,
  identity, infrastructure, SQL, deployment and gate-semantics changes.
* Docs-only evidence PRs conflict on `docs/reference/log.md` and `docs/reference/README.md`
  appends. Merge them one at a time and rebase the next.
* A worker relaunched on the same issue creates a second worktree, so look for duplicate
  candidates before publishing.
* Watch the load average after launching gate-tool workers (#2186 to #2190): earlier workers
  ran CPU burners that starved every other session.
* Worktree cleanup removes only clean worktrees with no live tmux session, nothing modified in
  the last 60 minutes and no non-cache ignored files, without `--force`. Branches stay until
  their PR head is verified merged.
* `pkill` and `kill $(...)` are blocked in this environment. Use literal pids.
* Never read or print `~/.ama-test-user*` or `~/.ama-resident-test-user`.

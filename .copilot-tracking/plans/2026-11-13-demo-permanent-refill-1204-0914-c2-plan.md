# Plan: refill correction 2 (issue 1204)

Research: [research](../research/2026-11-13-demo-permanent-refill-1204-0914-c2-research.md). Written and critiqued BEFORE source edits.

* [ ] 1. Exit-2 wording: inspect the session log and recorded exit status immediately, never end the delivery run, classify finished-versus-start-failure, then refill and re-arm.
* [ ] 2. Continuation eligibility: a retained candidate, failed test or gate is `ready` only when its dependencies are met, a finite permission covers it, the selected validation is defined and the source is run-owned; otherwise dependency-blocked or human-blocked with evidence; unknown stays bounded investigation, never a global block. No authority expansion.
* [ ] 3. Replace the launch command with a bash launcher example: unique `/tmp/launch-rpi-{number}-{role}-{timestamp}.sh` written by quoted heredoc, run as `tmux new-session -d -s rpi-{number}-{role} -c <worktree> "bash /tmp/launch-...sh"`; same agent, `claude-sonnet-5.5`, tools and force-push deny arguments; `PIPESTATUS[0]` captured immediately after `tee -a`; true exit appended to the log and returned; logs append across retries; no eval.
* [ ] 4. Checks: `bash -n` on the example, synthetic failing producer through tee shows true exit, existing 6 tests and ruff, targeted independent closure review.

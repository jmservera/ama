---
description: First-pass RPI record for the chat validation parent integration
date: 2026-11-13
---
# Research: demo-chat-validation-parent-891-0945 (2026-11-13)

* Disposition: executed (bounded, read-only). Planning Readiness: Ready.
* Input: frozen source `b05d92788b198c3b53efd54ac873fbf6cf2f3dac` (worktree demo-chat-clean-validation-891-0901, clean), original failed candidate `e01ae7796fc56663e19fa3b3a8a7a4acbab9d9f4`, base `347962dace94171724cc8db4044c8d783335fecf`. `git diff --name-status base..b05d` shows exactly 15 added files under `.copilot-tracking/`, 257 lines.
* Target: parent branch from main `5c91aa2c4418a14500da1c1014cbc55c37b011ab`; the 15 paths are absent there.
* Findings read from the frozen records:
  * Original run `run891.out`/`run891.exit`: Ran 37 tests, FAILED (errors=1), EXIT=1; error in `test_manager_report_local_http_and_bad_period` (HTTP 500, FileNotFoundError at ai_eval.py run_eval).
  * Original critique: retrospective (ran after the run), verdict reject, three findings applied. Original review pass_with_comments for the record only; validation not a pass.
  * Recovery: README editable install into a temporary venv, exit 0; preflight showed GOLDEN resolved to the worktree fixture and existed (the noneditable GOLDEN was under the venv site-packages and absent). Recovery critique prospective (before install/test), approve_with_comments. One rerun: Ran 37, OK, 0 skips, exit 0. Recovery review pass_with_comments.
  * Recorded limits: probe is separate from the run; dependencies differ from `8c735ae` so no byte-identical historical replay; local synthetic unit evidence only; not model, privacy, live, Azure/UI or per-call acceptance; #891 criterion 2 unmet; no ticks.
* Convention: the evidence pack uses dated sections with a Refs heading, a README index row and an append-only log entry (latest example: role-screen record).
* Boundaries: docs only; no tests, install, source, workflow or GitHub writes; case study original/addendum unchanged.

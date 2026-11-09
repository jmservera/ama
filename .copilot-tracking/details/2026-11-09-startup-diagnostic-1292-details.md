---
title: Issue 1292 startup lock diagnostic details
ms.date: 2026-11-09
---

## Phase 1 environment

* `d=$(mktemp -d /tmp/i1292sd-XXXXXX)`; `python3 -m venv $d/venv`; pip installs only pinned third-party prerequisites on an observed ImportError; project imports come from the worktree `src/*/src` PYTHONPATH with bytecode writing disabled. Import-origin check as in the plan. Raw evidence directory `/home/azureuser/source/ama-demo-wt/logs-1292-startup-diagnostic/` outside the repo.

## Phase 2 isolated attempts

* I1 unmodified exact command, I2 and I3 observer. Record start and end time, exit, `Ran 1 test in Ns`, load before and after. Stop on a failure that localizes the exception.

## Phase 3 concurrent attempts

* C1 unmodified, C2 and C3 observer. API companion `tests.test_auth` in the background first, Core test 3 s later, both timed. Record both exits and durations.

## Phase 4 analysis

* Tabulate attempts. For a failure: thread, step, exception code and name, hold time of the other opener's write section from the observer. Compare against hypotheses H1-H4. Prove source unchanged and nontracking equivalence (`git diff` empty for source paths and `git status --short --ignored` free of new or ignored files; only `.copilot-tracking` is committed). Hold time is derived only from the trace events of BEGIN IMMEDIATE and COMMIT or ROLLBACK, labelled inference. Record limitations.

## Phase 5 records

* Changes and review artifacts, state JSON, final handoff in the coordinator files directory. Nothing is published.

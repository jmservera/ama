---
title: Gate Chromium integration and native Runner evidence research (#1208)
description: Evidence for integrating accepted main (#1209) and the remaining native Runner-path proof gap
ms.date: 2026-11-05
ms.topic: reference
---

* Task: #1208, slug gate-chromium-integration-1208, parent gate-chromium-prerequisite-1208. Research disposition: executed (focused). Planning Readiness: Ready.
* Sources read: repository instructions, parent research, plan, details, changes, review and issue records (all preserved unchanged), the incoming main diff, tools/rpi-checks.py Runner (`__init__`, `command`, `install`, `install_chromium`, `run`, `tests_env`, `check_skips`).

## Findings

* #1209 merged to main at 3d7ad2feaa9c4cba5fe917edd2fbc40e40a5c246. Against merge base ead177ef it changes tools/backlog-sync.py, tools/test_backlog_sync.py, .github/workflows/src-ci.yml (path filter and tool steps), the WORKFLOW_HASHES entry for src-ci.yml in tools/rpi-checks.py, tracking records and docs/reference/log.md. `git merge-tree` predicts no conflicts: the #1208 hunks in rpi-checks.py (install_chromium, required_checks, browser group) are disjoint from the one-line hash change.
* Accepted source: the src-ci.yml pin and reconciliation tool are accepted main, not an unmerged sibling. No simulator-stack code is involved.
* Evidence gap (coordinator, accepted): the earlier native check recreated pip, playwright and test commands in /tmp/ama-1208-native.sh and ran before the final evidence-only commit. It did not call Runner.install_chromium or Runner.command, so it is not a Runner-path proof for the final head. It is preserved as supplementary evidence only, including the two import-error logs.
* Runner.run cannot be narrowed to the resident-summary test: its project-api group runs the whole api suite and then SQL and browser groups. A bounded harness can construct the real Runner, create its detached snapshot worktree exactly as Runner.run does, and call the real install, install_chromium and command methods (the command path applies the isolated env, safety hook, scrub, log hashing and check_skips for suite commands).
* Runner.command(suite=True) calls check_skips, which fails any skip whose reason is not whitelisted. The Chromium-unavailable skip is not whitelisted, so a launch failure stays a failure. A harness check_skips(expected_count=1) additionally enforces one test, zero skips.

## Decision

* Merge origin/main with a normal merge commit; do not rewrite the frozen commits. Run the bounded harness from outside the checkout against the final committed head in a detached worktree, under a nonqueued heavy lock. No --all, SQL, images, scanners or unrelated suites; no receipt is produced or claimed.

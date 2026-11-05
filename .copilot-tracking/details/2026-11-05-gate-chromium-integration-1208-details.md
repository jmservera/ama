---
title: Gate Chromium integration and native Runner evidence details (#1208)
description: Phase details for the main integration and bounded Runner-path native proof
ms.date: 2026-11-05
ms.topic: reference
---

## Phase 1: integration

* Merge commit 20dded33a integrates origin/main 3d7ad2fe into 57da478b without conflicts. Success: both change sets present, tracked tree clean.

## Phase 2: harness and artifacts

* Harness (external, not committed): construct Runner with the real selection and a new external out directory, add the detached snapshot worktree for the exact head, call Runner.install for api, Runner.install_chromium, then Runner.command for `python -m unittest -v test_resident_summary_ai_ui` from src/api with Runner.tests_env, suite=True. Success: check_skips reports 1 test, zero skips.

## Phase 3: execution after the final commit

* Focused tier commands, each exit code and test count recorded. Heavy lock acquired with `flock -n`; if unavailable, record the exact resume point and stop. Out of scope: --all, SQL, images, scanners, other browser suites, receipts, pushing.
* Native evidence is recorded outside the repository after the final commit; this artifact set records only the plan and the method, not results.

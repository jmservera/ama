<!-- markdownlint-disable-file -->
---
title: Issue 350 checker correction 1 retry phase details
description: Prospective phase details for the forward-ordered retry
ms.date: 2026-10-25
---

* Phase 1: dispatch one read-only `rubber-duck` with the research and plan paths. Record findings, dispositions and execution in the critique artifact before any execution.
* Phase 2: a source change is allowed only for a confirmed gap, with a failing regression first and at most one correction cycle.
* Phase 3: from the repo root, with a venv at `/tmp/c1-350/v` built from `git archive HEAD src` (no repo writes): `PYTHONDONTWRITEBYTECODE=1 /tmp/c1-350/v/bin/python -m unittest tools.test_check_demo_feedback`; the CLI on a generated 10000-deep file under `/tmp`; the admin fixture through `build_report`.
* Phase 4: one read-only `rubber-duck` review of the diff from 68692817 to HEAD for the checker and tests.
* Phase 5: write the changes and review artifacts and the state file, commit with the noreply identity and Copilot trailer, fetch main, then run `python3 tools/rpi-checks.py --all --base 36996d70a3f6dbee9df4d16400afd07c3614e69e --lock-timeout 14400 --out <new external dir>` and `--verify-receipt` before a normal push.

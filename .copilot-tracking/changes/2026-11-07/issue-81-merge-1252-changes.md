---
title: Issue 81 main 1252 merge changes and author review
description: Changes, evidence and one author Review for the normal merge of origin/main a1d26534
ms.date: 2026-11-07
task_slug: issue-81-merge-1252
---

## Changes

* Start `720d9e49cfadf61416903cbfebdd20a3aef6986f` (ref `refs/ama/issue81-pre-a1d-merge`). PRE records commit `fbfba017b81d4090fa161c58c32f3734c3d56d02`. Normal `--no-ff` merge `033ccc9e29990a6ea0aef2d05953280ebd2f9051`, tree `e1deb0209036e2baf7cc4bf6aae5465f4e2a0c1f`, parents PRE and `a1d265340ba7d6f14b24e028362b2d5f4bb80126` (PR #1252). The scorer run for that commit (42381926533) was completed with success and no score descendant existed, so `a1d26534` itself was the admitted target. No conflict, rebase or force.
* Proof: `git diff --raw PRE HEAD` equals `git diff --raw 39506027 a1d26534` including modes. Non-tracking files changed: `tools/backlog-sync.py` (blob `43338cb8fc53bfba5b797bb833f347b4713af56a`, equal to main's, not the old `8c821`) and `tools/test_backlog_sync.py`. `src/` and `.github/` identical to PRE, so parent and child-owned source and tests are preserved. `git diff --check PRE HEAD` clean.

## Local observed evidence (no service, not acceptance)

Scratch `/mnt/ama-gates/g81-main1252-preparation-1107`, Python 3.12.3, `env -i`, `PYTHONDONTWRITEBYTECODE=1`, external caches, ruff 0.17.1, mypy 2.4.0. Exits unmasked.

* Tools unit tests: `test_backlog_sync` exit 0 (17 tests OK); `test_ci_affected` exit 0 (19 OK, after run 2); `test_rpi_checks` exit 0 (86 OK, after run 2).
* Adverse harness run 1, preserved in `logs-run1/`: `test_rpi_checks` 86 tests with 7 errors and `test_ci_affected` errors. Cause: my snapshot held only `src/core`, `src/agents` and `tools`, so `.github/workflows` and `src/api` were missing, and PyYAML was not installed (a missing-dependency failure). Not a product defect. Run 2 used a full `git archive` snapshot plus `pip install pyyaml`. The output lines `FAILED required group: preflight` inside run 2 are expected refusals asserted by the tests.
* `ruff check --isolated` and `ruff format --isolated --check` on the five tools files: exit 0. `mypy --strict` on the two rpi-checks files and `mypy --ignore-missing-imports` on the two backlog files: exit 0.
* Four core modules from `src/core/tests` with non-editable `--no-deps` core and agents installs (origin is the scratch venv site-packages): exit 0, 233 tests OK, 1 skip (JSON-only separate-file audit ordering).

## Author Review (executed once; not independent, not operating or human approval)

Conformant with the plan and its Amendment 1; the critique (verdict Approve, two Non-blocking findings) is retained unchanged. Limits: no FULL, SQL, browser, scanner or service; the full CI workflow was not run; these results do not accept the parent. Pending: child #86 alignment to this head, FULL after child merge on exact head and current main, independent exact-head review, hosted CI, human approvals. #81 criteria and #440 acceptance remain unticked. Earlier receipts do not cover this head.

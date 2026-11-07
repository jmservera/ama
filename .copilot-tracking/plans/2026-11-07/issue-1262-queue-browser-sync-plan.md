---
title: Issue 1262 queue browser result synchronization plan
ms.date: 2026-11-07
---

## Overview

Task `issue-1262-queue-browser-sync`, tier FOCUSED, test-only. Research: [research](../../research/2026-11-07/issue-1262-queue-browser-sync-research.md). Details: [details](../../details/2026-11-07/issue-1262-queue-browser-sync-details.md). Written before any reproduction probe or source edit.

## Phases

* [ ] Phase 1: Prospective probes (after critique). Run an unchanged-code deterministic reproduction with a controlled delayed-render page and record actual IDs, control value, status text and result state. Run the unchanged maintained browser journey once under nonqueued admission and record what it actually does.
* [ ] Phase 2: Add `wait_queue_result` to the checker and use it in the queue loop. Add the focused regression tests to `tests/test_workbench_live_defaults.py`. Run the regression against the old synchronization (red) and the new helper (green).
* [ ] Phase 3: Validation: unit module, ruff check and format, mypy for the touched files, the maintained browser journey (`python -m checks.design_system_browser_check` invokes the workbench check) under nonqueued admission; `rpi-checks.py --changed` if admission allows.
* [ ] Phase 4: Changes record, original Review, state, commit on the topic.

## Decisions and exclusions

* Keep `wait_cases` for the 28 other call sites. Only the queue loop needs rendered queue identity.
* The helper waits for the rendered status queue label, case count and exact ordered `.item` IDs; the `check(...)` equality assertion after it stays.
* On timeout it raises `AssertionError` with expected and observed IDs and status; no sleep, retry, timeout increase, swallowed failure or weakened set.
* No product, API, ranking, policy, auth, SQL or infra change. No web file changed.
* Not in scope: the ranking FULL receipt, other checks, any `--all`, SQL or container work.

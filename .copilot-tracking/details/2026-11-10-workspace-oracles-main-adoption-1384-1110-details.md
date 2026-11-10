---
title: Issue 1384 main adoption details
description: Step details and commands for the main adoption of the 1384 candidate
ms.date: 2026-11-10
ms.topic: reference
---

## Commands (all from the worktree root unless noted)

* Definitions: `ROOT=/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files` (outside the worktree); evidence `ROOT/checks-1384-main-adoption-1110/`; witness evidence `ROOT/phase1384-main-adoption-evidence-1110`.
* Pre-marker: `git fetch origin main` (done, `111847191d1f...`); tracking-only commit on top of `3f1fa48` (so `3f1fa48` stays an ancestor and the merge's first parent is that tracking commit); witness `launch`, `research-open`, `plan-done` in separate calls with `--evidence-dir ROOT/phase1384-main-adoption-evidence-1110 --session rpi-1384-main-adoption --actor worker --claim-model claude-sonnet-5.5`; strict unique-key parse of the state file in its own call; `implement-start` in its own call.
* Merge: `git merge --no-ff --no-commit origin/main` after `implement-start`, so the staged composition is the dirty source snapshot. Order: validate, complete the changes record, `implement-done`, one Review, `review-done` (all while the merge is staged), then `git commit` (ordinary merge commit, parents: tracking commit and `111847191`), then `commit-complete --claim-commit <HEAD>`, then `verify`.
* Resolution (apply_patch only): import block keeps `from functools import partial` and `from time import monotonic` in sorted order; constants block keeps `TERMINAL`, `REVISIT` and `ROUTE_DELIVERY_DEADLINE_S`. No change to the poll loop or to `delayed_companion` as delivered by main.
* Environment: `V=/home/azureuser/.cache/ama-venv-1384-workspace-oracles-1110/bin`, run from `src/api`, `PYTHONPATH=../core/tests:../agents/tests:.` for units; the browser checks start their own server from the worktree `src/*/src` (verify the imports resolve under the worktree).
* Units: `$V/python -m unittest tests.test_workspace_scripts` plus any impacted focused unit for files merged from main that touch the workspace loader (`tests.test_workspace_paging`).
* Static: `$V/ruff check .`, `$V/ruff format --check .`, `$V/mypy`, `node --check src/zava_forward/api/web/app.js`.
* Browser (nonqueued), `P=$V/python` from `src/api`: `flock -n /tmp/ama-rpi-heavy.lock env PYTHONPATH=. timeout 600 $P checks/workspace_scripts_browser_check.py`, the same for `employee_workspace_browser_check.py`, and for `employee_chat_browser_check.py` with `--axe ROOT/checks-1384-main-adoption-1110/axe-4.10.3.min.js --out ROOT/checks-1384-main-adoption-1110/chat-axe-out.json` (a byte copy of the pinned axe; the check verifies its own SHA-256 `880970c0...`). Outputs `.out/.err/.exit` in `ROOT/checks-1384-main-adoption-1110/`; actual holder via `fuser` before each run; when busy, one later attempt, otherwise hold.

## Expected results (derived from the declaration, not from observation)

* Exhaustion total 1 + 3 = 4, missing-global 2, controls extra 4/5, early 4/3, reset 4/7, continue 2/4; employee extra 4/5, early 4/3.
* The delayed variants must still pass the unchanged exact `len(pending) == 1` assertion given main's wait.

## Stop conditions

* Any conflict beyond the two additive hunks, any need for a semantic change, a merge that changes `SCRIPT_RETRY_DELAYS`, a missing prerequisite or a busy lock after one later attempt: stop with evidence for Root.

<!-- markdownlint-disable-file -->
---
title: Issue 350 rehearsal alignment phase details
description: Concrete steps and stop rules
ms.date: 2026-10-25
---

## Phase 1

* Install merged worktree sources (from an `git archive` snapshot outside the repo, so no ignored files appear in the checkout) into a new venv under `/home/azureuser/rehearsal-350/merged`.
* New container `ama-350-merged-sql` (own label, loopback random port, bounded memory), new database, same constructed fixture; server on 127.0.0.1:8351 started as a child of a bounded foreground command, not left running.
* Re-run `exercise.py` (denials, roles, call, reload) with the base URL and password file parameterised through environment, then restart the app and re-read persistence; template AI check. Success: same results as 2026-10-24, or a recorded difference. A real regression stops the task (no source change authorized) and is routed.
* Remove only the helper container, venv and snapshot afterwards.

## Phase 2

* Changes artifact states: new evidence is merged-main local rehearsal; the 8350 owner server still runs the pre-PR449 snapshot (disclosed); the tenant/staff-database diagnosis is historical; corrected accuracy findings RV-001..RV-003 remain disclosed with original outcome non-conformant and unverified closure.

## Phase 3

* Review once, independent, read-only. Commit with the noreply identity and Copilot trailer. `git fetch`, `tools/rpi-checks.py --all --base <current main> --lock-timeout 14400 --out <new dir>`, then `--verify-receipt`.

## Phase 4

* `git push origin test/deployed-feedback-harness-350` (fast-forward only), then `gh pr edit 436 --body-file` keeping draft.

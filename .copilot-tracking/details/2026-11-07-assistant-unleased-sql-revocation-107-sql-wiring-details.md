---
title: Details for SQL wiring of the unleased revocation test (#107)
description: Exact steps, selectors and the future runner admission
ms.date: 2026-11-07
---

Plan: [plan](../plans/2026-11-07-assistant-unleased-sql-revocation-107-sql-wiring-plan.md).

## Step 1: metadata relocation

Create `/mnt/ama-gates/g107-sql-wiring-preparation-1107/egg-info-relocated/{core,agents,api}`, record `ls -la` and sha256 of each file, then `mv` the three directories by exact path (no glob, no recursive delete, no stash). Verify with the venv interpreter that `zava_forward.core.assistants` and `zava_forward.api` resolve under the worktree, `pip list` shows the worktree editable locations, and `git status --short --ignored` is empty.

## Step 2: wiring

Append `"test_assistant_release.MssqlUnleasedRevocation"` after `"test_assistants.MssqlLedgerTests"` in `SQL_SELECTORS`. In `tools/test_rpi_checks.py` add an assertion in `test_matrix_drift_and_unreviewed_extra_commands_refuse` that the tuple contains the selector. The runner executes it from `src/api` with `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1` and the owned container, so `MssqlFixture` accepts the host and the `skipUnless` guard passes: the class runs unskipped.

## Step 3: light checks (no services), own venv, external caches, PYTHONDONTWRITEBYTECODE=1

* From the repository root: `python -m unittest tools.test_rpi_checks` (or the file's documented invocation), `ruff check` and `ruff format --check` on `tools/rpi-checks.py` and `tools/test_rpi_checks.py`, and mypy as configured for tools.
* From `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`: `python -m unittest test_assistant_release test_assistants test_continuity`, expecting the same SQL opt-in skips.
* Each command's real exit is recorded without a masking pipe.

## Step 4: normal merge

After a fresh fetch, a single `git merge --no-ff` of the settled admitted main; keep a local ref to the pre-merge head; verify two parents, delta equal to the incoming files plus planned records, `git diff --check`, JSON parse of any score file, and unchanged blobs and modes for the test and tool edits.

## Future FULL admission (coordinator only, one nonqueued shared lock)

Selector reached by the runner: `test_assistant_release.MssqlUnleasedRevocation` inside the `SQL_SELECTORS` unittest call. Command read from the then-current own tools and README: `python3 tools/rpi-checks.py --all --base <fresh current origin/main> --out <new external directory> --jobs 2 --lock-timeout 0 < /dev/null`, real exit and logs captured, receipt verified with `--verify-receipt`. Expected resources: one SQL container (3 GB, 2 CPUs), fresh images and Chromium, plus tens of GB of `/mnt` output. Any failure of the new class, or any skip of it, blocks publication.

## Known limits

Hosted CI is not extended. Actual SQL, independent exact-head review, hosted checks, serving attestation, approver identity and the wider C10 bundle remain open.

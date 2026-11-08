---
title: Research for wiring the unleased SQL revocation test into FULL (#107)
description: Provenance of generated metadata and why the runner's disposable SQL group does not reach MssqlUnleasedRevocation today
ms.date: 2026-11-07
---

Continuation of task `assistant-unleased-sql-revocation-107`. Earlier records, including the author-only critique, stay unchanged and are not independent approval. Research disposition: executed. Candidate `3a9523a88f09606f389cb4d35c8aac79b2f61758`, tree `ce0edeac388e7b142913c257519a41a33420677c`. SQLite proxy passes; `MssqlUnleasedRevocation` was skipped; actual SQL is unverified; FULL is not ready.

## Generated metadata

Three ignored directories exist: `src/core/src/zava_forward_core.egg-info`, `src/agents/src/zava_forward_agents.egg-info` and `src/api/src/zava_forward_api.egg-info`. Each holds exactly PKG-INFO, SOURCES.txt, dependency_links.txt, requires.txt and top_level.txt, is owned by `azureuser`, was created 2026-11-07 14:21 UTC by this task's `pip install -e` into `/mnt/ama-gates/g107-unleased-preparation-1107/venv`, is matched by `.gitignore` line 16 and has no tracked files. The venv's editable `direct_url.json` and `.pth` files point at the worktree `src/<project>` folders, not at the metadata, so relocating them should not change import origins. Plan: move only these three folders, by explicit path, to `/mnt/ama-gates/g107-sql-wiring-preparation-1107/egg-info-relocated/`, then re-verify origins and ignored-inclusive cleanliness.

## Why SQL does not reach the new class today

* `tools/rpi-checks.py` runs disposable SQL only through the fixed tuple `SQL_SELECTORS` (lines 39-48), used by the owned-SQL step (around line 2360) and the dry-run plan (line 1177), with `ZF_TEST_MSSQL=1` and the loopback owned container. The tuple does not contain `test_assistant_release.MssqlUnleasedRevocation`.
* The generic API project group runs `unittest discover` without `ZF_TEST_MSSQL`, so the class is skipped there.
* The reviewed `--extra PROJECT:selector` mechanism (line 1259 and the dry-run equivalent) runs with `PYTHONPATH` only and no SQL variables, so an extra would skip the class too.
* `.github/workflows/src-ci.yml` (line 327) has its own explicit selector list and the gate pins workflow hashes, so changing the workflow is out of scope and is reported as a gap: hosted CI will not run the class.
* `tools/test_rpi_checks.py` only asserts `SQL_SELECTORS[0]`, so appending is compatible.

## Conclusion

The existing mechanism cannot reach the class without a change. Smallest tool-and-test-only plan: append one selector to `SQL_SELECTORS` and add one assertion in `tools/test_rpi_checks.py`. No new command, provider, schema or database; the same owned loopback container and `MssqlFixture` are used. Residual risk: the class has never run on SQL, so the first real run may expose fixture or dialect issues, which would be a recorded failure and not a relaxed criterion.

## Main drift

`origin/main` fetched at `a1d265340ba7d6f14b24e028362b2d5f4bb80126` (PR 1252), tree `34ee67e0617f60a1e135cc042f25076dc15721df`, merge base `3950602754437c21d20e91c49ddc1589426e7d1b`. Its delta is `tools/backlog-sync.py`, `tools/test_backlog_sync.py` and `.copilot-tracking` records for issue 1251; no overlap with `tools/rpi-checks.py`. A scorer commit changing only `.github/rubric/scores/latest.json` may follow.

Planning Readiness: Ready.

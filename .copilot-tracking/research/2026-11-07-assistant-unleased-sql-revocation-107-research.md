---
title: Research for unleased SQL revocation coverage (#107)
description: Confirms the C10 limitation in the merged revocation test and the existing SQL fixture wiring
ms.date: 2026-11-07
---

Task `assistant-unleased-sql-revocation-107`. Worktree `/home/azureuser/source/ama-wt/issue-107-sql-revocation`, branch `test/assistant-unleased-sql-revocation-107`, target main, base 3950602754437c21d20e91c49ddc1589426e7d1b, which equals origin/main at 2026-11-07 (no drift). Research disposition: executed. The prior bounded PR 1253 is merged and does not close #107; the issue snapshot `/tmp/issue107-c10-current-1107.json` was read as data only.

## Confirmed limitation

In the merged `Release.test_racing_workers_and_restart_after_revocation_keep_allowance_and_make_no_call` the proposal is claimed through the original service first. `Assistants.claim` rejects a task whose state is leased with an unexpired lease before it evaluates `disabled()`, which calls `admission()`. A worker returning False therefore does not isolate the release denial. Nonblocking; the other assertions of that test stand.

## Existing paths

* `Assistants.execute` calls `claim`; `claim` calls `disabled(db, capability)`, which includes `admission` (release denial reason), then writes state `disabled`, `task["reason"]` and a `disabled` event. This gives durable, release-specific evidence for an unleased pending task with no provider call.
* `src/api/tests/test_assistants.py` `MssqlFixture` plus `skipUnless(ZF_TEST_MSSQL == "1")` provides actual disposable SQL (requires `ZF_SQL_SERVER` localhost, never Azure). `release_support.install` already creates `assistant_releases` for the `_env` store type.
* `test_assistant_release.py` classes derive from the SQLite `Base`; none is covered by the MSSQL classes automatically.

## Gaps and limits

The SQLite variant is a local proxy and not SQL acceptance. The fixture does not drop `assistant_releases` between tests; `install` deletes only `fx-%` rows, which is what the new test uses. Real SQL execution is not available in this task, so the SQL class is implemented-unverified.

Planning Readiness: Ready.

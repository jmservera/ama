---
title: Issue 1292 before-fix and closure-mapping details
ms.date: 2026-11-11
task_id: 1292-before-fix-closure-1111
---

## Commands (session-external orchestration, repository untouched)

* Snapshots: `git archive e2ecee2565e86889c6beb43cb32e7c5b54270e01 src/core | tar -x -C $OWN/old`; `git archive HEAD src/core | tar -x -C $OWN/cur`. Venvs: `python3 -m venv $OWN/venv-old` and `$OWN/venv-cur`; `pip install "$OWN/old/src/core[sql]"` and `"$OWN/cur/src/core[sql]"`.
* Test run (both arms): `cd <worktree>/src/core/tests && <venv>/bin/python -m unittest -v test_priority_order.MssqlPriorityOrder.<method> ...` with `ZF_RESIDENT_MSSQL=1`, loopback `ZF_SQL_*` variables and `ZF_SQL_TASK_MANIFEST` for the owned container. Working directory `src/core/tests` is the documented test path for `dataset` and `sqlguard`; no `PYTHONPATH` is set, so `zava_forward` can only resolve from the venv.
* Current arm adds `test_priority_order.SqlitePriorityOrder.<same 5>` and `test_priority_order.JsonPriorityOrder.<first 4>`.
* Hashes: `git hash-object` of the venv-installed `store.py`, `sqlstore.py`, `mssqlstore.py` against the arm's blobs; SHA-256 of the test file, `dataset.py` and `sqlguard.py`.
* Container: `docker run -d --pull=never --label zf.task=1292-sql-disposable --memory 3g -p 127.0.0.1:PORT:1433 sha256:cf8f0ab2...1718` with a random password in the environment only.

## Stop conditions

Heavy lock busy; image id absent or different; hash or import-path mismatch; pip cannot install the declared dependency; any need to edit source, tests, fixtures or configuration. Report the real reason, no workaround.

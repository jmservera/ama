---
title: Issue 73 served parent integration - changes
ms.date: 2026-11-10
---

## Opened before implementation

* Opened after plan-done witness event (seq 3) and before the merge. Parent head b0af68a3e87faf535d8cdddc3357d4cfd32c7adf, tree 5622269aeb1af1e08bd7309424d1f2bf8c5c6716. Pinned main 4244e84e763e6e01dd6012fcb9b650dae8d58e9d.

## Changes

* Witness: implement-start recorded at 05:27:55Z (seq 4) with no qualifications, before the merge.
* Identity: gh account jmservera, repository-local email 8036360+jmservera@users.noreply.github.com for author and committer. Copilot trailer on commits.
* Merge: `git merge --no-ff 4244e84e763e6e01dd6012fcb9b650dae8d58e9d` produced commit `a8a0c5190cee562692b992c21d87df90a0b79331` (parents b0af68a3 and 4244e84e), tree `7567de897499f2c5920cce09bc8c7c1bcd6b1de9`, identical to the pre-merge `git merge-tree` trial. No conflict, no hunk resolved, no source edit by hand. `git diff` of `src/` against the two parents shows only each side's own changes.
* Docs: one appended entry in docs/reference/log.md (append-only; no earlier entry touched). No other doc, source, workflow, settings or role change.

## Validation (tier: owner DEMO TARGETED; raw logs in /tmp/issue73-1110-scratch/logs)

Environments: Python 3.12.3; FULL venv /tmp/issue73-1110-venv-full (core[sql,dev], agents, api[dev], importer[dev], editable from this worktree; ruff 0.17.1, mypy 2.4.0, mssql-python 1.15.0, playwright 1.64.0); NOSQL venv /tmp/issue73-1110-venv-nosql (core[dev], importer[dev] only).

| ID | Command (cwd) | Result |
| --- | --- | --- |
| V1 | `python -m unittest discover -s tests -q` (src/core, FULL) | exit 0, 2864 run, OK, 347 skipped (opt-in SQL/browser gates) |
| V1f | `PYTHONPATH=tests python -m unittest test_discovery_assistant_demo test_import_refusals test_exception_feeds test_exception_queue -q` (src/core) | exit 0, 58 OK, 7 skipped (MSSQL opt-in; run in V5) |
| V1s | `PYTHONPATH=tests python -m unittest test_sqlstore test_governance -q` (src/core) | exit 0, 89 OK, 16 skipped (SQL opt-in) |
| V2 | `python -m unittest discover -s tests -q` (src/importer, FULL and NOSQL) | both exit 0, 79 OK, 0 skipped |
| V3 | `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q` (src/api, FULL) | exit 0, 2584 run, OK, 542 skipped (opt-in SQL/browser gates) |
| V3f | register, register screen, role screens (+conformance), workspace scripts, workbench modules (src/api) | exit 0, 80 OK, 0 skipped |
| V4 | `python -m zava_forward.core`, `... discovery-demo`, `... discovery-demo extra`, `python -m zava_forward.importer --help` | version line exit 0; discovery JSON exit 0; extra argument exit 2 with message; importer help lists preview, stage, exceptions, transfer, exit 0 |
| V5 | `ZF_IMPORT135_MSSQL=1 python -m unittest test_import_refusals -v` against disposable MSSQL | attempt 1 refused by sqlguard (container label value; 7 errors, original log kept as v5-mssql-core-attempt1-label-refused.log, container removed); attempt 2: exit 0, 21 OK, 0 skipped, 7 MssqlProjection tests ran |
| V6 | /tmp/issue73-1110-scratch/story.py sqlite and json | both exit 0 (details below) |
| V7 | `ruff check . && ruff format --check . && mypy` in core, importer, api (FULL) and core, importer (NOSQL) | all exit 0 (core 288 files, importer 12, api 213 mypy sources) |
| V8 | `python -c "import mssql_python"` (NOSQL) | exit 1 ModuleNotFoundError (driver absent); V2 and V7 importer results above were obtained in that environment |
| V9 | `test_dependency_rule` in core, importer, api | exit 0, 2 OK each |

* V5 detail: heavy lock /tmp/ama-rpi-heavy.lock taken with `flock -n` (no holder, nonqueued); container `issue73-1110-sql-1794289830` id c48fa4ee...618f6d on 127.0.0.1:38805, image mcr.microsoft.com/mssql/server:2022-latest sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718; cleanup exit 0 and the container is gone; image kept. The label value `zf.task=1292-sql-disposable` is the sqlguard-required value. The first container (4a260f75...) was removed by the same trap.
* V6 detail (synthetic Core dataset, temporary ZF_DATA/ZF_STATE under scratch, loopback ports 18173 and 18174, synthetic sign-in): stage of a non-workbook exits 1 with a refusal ref; transfer exits 0 `added=1 already_present=0 stored=1 of ledger=1`; steward sees one failed import with owner configured (not an appointment) and Unknown eligibility; operator sees "1 stored ... 0 are shown"; an unnamed manager gets 403; restart shows the same ref; repeat transfer `added=0 already_present=1`; ledger and source hashes unchanged; stable ref True. Chromium (Playwright 1.64.0) showed the steward register row EX-001 Failed import and "1 are shown", and the operator "0 are shown" with the not-all-clear text. JSON and SQLite both pass. A first run crashed on my own wrong URL (`/` instead of `/app`); the log of the rerun on a reused scratch directory is kept as v6-story-sqlite-rerun-after-debug.log. Not assistive-technology acceptance.
* Not run: full local RPI gate, `--changed` gate, hosted CI, importer or API suites against MSSQL, native assistive technology, any push.

---
title: Resident retention and permissions changes
description: Implementation and validation evidence for issue 86
ms.date: 2026-10-16
---

Task: issue-86-resident-retention-permissions. Full plan scope.
Research Ready; single critique executed and all six findings dispositioned.
Implementation active, P01-T01 through P01-T03. No source changes outside src.

## Decisions and amendments

Owner's first-contact clarification supersedes decision-date origin and one-month
proposal. Five calendar years; unknown evidence does not become today's date.
Use existing operational role names, separate recording from viewing.
Scope exception for explicitly requested docs/log and RPI artifacts.

## Validation

Pending red/green, component tests, ruff, mypy, loopback HTTP, Azure SQL, cleanup.
System Python has SQL driver but no ruff/mypy; pip refuses system installation
under PEP 668. Use isolated project venv with system packages rather than
overriding the managed environment.

## P01 local evidence

* Red before fix: two new JSON regressions fail on original source: missing
  retention_schedule and manager safe-contact mutation incorrectly succeeds.
* `.venv/bin/python -m unittest discover -s src/core/tests -q`: final full
  core suite 401 run, 1 opt-in Azure test skipped, passed (126.728 s).
* From src/api, `PYTHONPATH=../core/tests:../agents/tests
  ../../.venv/bin/python -m unittest discover -s tests -q`: 517 run,
  99 intentional existing opt-in skips, passed (179.645 s).
* After adding exact-field/complaint-preservation assertions, resident suite:
  30 run, 1 Azure skip, passed. Includes JSON/SQLite determinism, first-contact
  origin versus decision, leap anniversary, configured constant, expired
  representative/withdrawal, legal hold, restart and purge canaries.
* Core and API `python -m ruff check .`, `ruff format --check .`, and `mypy`
  passed (81 core and 42 API source files). `node --check` panels.js passed.
* Local application: tests.test_resident_api starts the actual loopback
  ThreadingHTTPServer, verifies /healthz, /app, authenticated supplied decisions,
  scoped withdrawal, independent review, projected staff and contractor reads,
  manager 403s and SQL restart. With content-standard tests: 7 passed.
* Initial full suite identified manager complaint closure regression; corrected
  by keeping separate service actions' existing named-owner rights, without
  restoring manager resident-field writes. Old role assertions updated to the
  owner matrix. Partial content fixtures without resident objects stay Unknown.
* Missing browser package blocked existing API mypy imports; installed the
  development dependency into the isolated venv, then mypy passed. No browser
  acceptance or live model inference claimed. Existing sensor file-handle
  ResourceWarnings are unrelated and remain unchanged.

## P02 Azure execution boundary

Local gates green before provisioning. Existing server
sql-forward-test-rzsrg in ama/uksouth; create isolated Basic database
resident86test20261016b. Never open retrofit or any private JSON.
Owner explicitly authorizes whole-group teardown; az lock list returned empty.
Pending live exercise and verified cleanup.

## P02 live Azure SQL result

2026-10-16: `az sql db create -g ama -s sql-forward-test-rzsrg -n
resident86test20261016b --service-objective Basic --backup-storage-redundancy Local`
returned Online, Basic, uksouth. Developer token supplied only in the process
environment using `az account get-access-token --resource
https://database.windows.net/`; no token written or printed.

`ZF_RESIDENT_AZURE_TEST=1 ZF_SQL_SERVER=sql-forward-test-rzsrg.database.windows.net
ZF_SQL_DATABASE=resident86test20261016b ZF_SQL_AUTH=token
PYTHONPATH=src/core/tests .venv/bin/python -m unittest
test_resident_decisions.AzureResidentDecisions -v`: 1 passed, 10.889 s.

Real MssqlStore (a SqlStore subclass), fresh synthetic DATA only:

* Recorded scoped acceptance then withdrawal, contractor Proceed then Hold.
* Manager write refused without mutation; coordinator sees exact wishes;
  contractor does not.
* New connections reopen the persisted decisions and first-contact evidence.
* Exact due date 2026-10-17 from first contact 2021-10-17, not decision date.
* Boundary expiry refuses representative disclosure; manager-approved purge
  survives another new connection; marker preserved; audit chain intact.
* Actual `is_ledger_on` is false. This proves current-row deletion, not backup
  erasure. No existing retrofit database or private data file was read.

`az group delete --name ama --yes` running as authorized. Resource inventory
already reduced to the Container Apps environment, VNet and two NSGs;
SQL, apps, registry, Foundry, storage, private endpoints and monitoring removed.
Awaiting group-nonexistence confirmation before claiming cleanup complete.

## Final local checks and documentation

Core/API ruff check, format check and mypy green; final targeted resident
suite 30 run/1 opt-in skip green. Final local HTTP+role suite: 13 passed.
The first named-module command omitted API tests from PYTHONPATH; corrected
to `PYTHONPATH=tests:../core/tests:../agents/tests`, then all 13 passed.
Agents existing suite: 70 passed. Node VM render exercise verifies recorder
form, manager read-only decision fields with separate complaint route retained,
and contractor flag-only panel. `node --check` and `git diff --check` passed.

Updated core/API guides and knowledge index; append-only reference log records
owner decisions, evidence and limits. No change to original/addendum, private
memory, infrastructure, environment files or forbidden tracking folders.

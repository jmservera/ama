# Changes addendum: native SQL Server evidence (#1292)

Dated 2026-11-08. Original changes record preserved. No product, test or
earlier RPI record was edited.

## Identities

* Candidate HEAD `16375e3ca3a933b4f00dac907cecd98a5d78a635`, tree
  `271d0fb60c015bdaa7473fc89b325c7a2b1eb180`, base
  `6354b13f7abf1441a815e92f2b01dc184ce0b0ac`; tracked tree clean.
* Server: Microsoft SQL Server 2022 (RTM-CU27-GDR) 16.0.4305.5 Developer, Linux,
  image `mcr.microsoft.com/mssql/server:2022-latest`
  `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`.
  Container `ama1292-sql-1771153-31999` created by this run on
  127.0.0.1:24165 (3 GB limit), removed by this run's exit trap
  (`container-cleanup.txt`); no `ama1292` container remains.
* Lock: `/tmp/ama-rpi-heavy.lock` had no holder; whole run under
  `flock -n` (no queue). Disk 11 GB free, about 7.4 GB memory available.
* Python 3.12.3 in task-owned venv `/tmp/ama-1292-sql-venv-20261108T203512Z`
  with `mssql-python==1.15.0` and `mssql-python-odbc==18.6.2.1` (the repo pins).
  A first attempt without them failed with `ModuleNotFoundError: mssql_python`
  (all six invocations exit 1, evidence `/tmp/ama-1292-sql-evidence-20261108T203444Z`,
  container removed); this justified the install.
* Backend: the server answered (`server-version.txt`, SA password auth over
  loopback). Disposable databases `zf_priority1292_<uuid>` were created and dropped
  by the tests; `leftover-databases.txt` is empty.
* Imports (sha256 of `sqlstore.py` / `mssqlstore.py`):
  * base, from `git archive 6354b13f...`: `0a710234c52207dde90beb11f44a91fd7d7f99e1882623785314a397d8c59651` / `dca3b3f0276b39384520fb518849445f68af5c97df5e335f7e7a1fe82662babd`
  * head, from the worktree: `d38b07f6fa7ad68e98667908194174c025700c074d9eeb992fc6fbe77e2835aa` / `0e618ac5f05fe02e3e08ab8c5eb30d3989817995e56077a2c5a035c02c6e16d1`

## Results (`ZF_RESIDENT_MSSQL=1`, `python -m unittest -v`)

External evidence: `/tmp/ama-1292-sql-evidence-20261108T203523Z/`. Sanitised
copies (no credentials): `.copilot-tracking/changes/logs/1292-2026-11-08-sql/`
(`<label>.stdout.txt`, `.stderr.txt`, `.exit.txt`, `.imports.txt`, `run-sql-evidence.sh.txt`).

| Label | Selector | Source | Exit | Result |
| --- | --- | --- | --- | --- |
| base-priority | `test_priority_order.MssqlPriorityOrder` | base | 1 | 10 run, 7 failures, 2 errors, 1 pass, 0 skips (red) |
| base-sel1 | `MssqlResidentControls.test_challenge_source_exact_dependency_manifest_and_original_reviews` | base | 1 | 1 run, 1 failure (`stale` True != False) (red) |
| base-sel2 | `MssqlResidentControls.test_failed_priority_accept_edit_remove_disposition_and_audit` | base | 1 | 1 run, 1 failure (red) |
| head-priority | `test_priority_order.MssqlPriorityOrder` | head | 0 | 10 run, OK, 0 skips |
| head-sel1 | as base-sel1 | head | 0 | 1 run, OK, 0 skips |
| head-sel2 | as base-sel2 | head | 0 | 1 run, OK, 0 skips |

Skip count is zero in all six (`grep -ci skip` is 0). Some base-priority
failures are test-fixture assertions that the base DDL lacks `created_ord`
(for example the legacy-table fixture); the two original selectors fail on
base for the reported behaviour itself.

## Still pending or unproven

* FULL local gate and receipt: NOT run; separate coordinator routing.
* Ledger-enabled migration: UNPROVEN (not tested).
* Independent exact-head review, hosted CI, human approval: pending.
* Legacy ordering remains a documented heuristic; no data-owner approval claimed.

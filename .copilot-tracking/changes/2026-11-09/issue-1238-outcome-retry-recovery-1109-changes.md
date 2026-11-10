<!-- markdownlint-disable-file -->
# Changes: issue 1238 outcome persistence retry (recovery 1109)

Recorded 2026-11-09 after implementation (phase transition Plan to Implement
at 22:15:30Z, Implement to Review recorded in state). Plan:
[plan](../../plans/2026-11-09/issue-1238-outcome-retry-recovery-1109-plan.md).
Raw logs are in the owned external scratch directory
`/tmp/issue1238-1109-scratch.jCyJBq` (see `OWNER.txt`), not committed.

## Source and test changes

* `src/core/src/zava_forward/core/resident_decisions.py`: `_forward` now calls
  `_record_outcome`. It runs the same outcome operation (same reservation,
  attempt, outcome, receipt) at most twice; the receiver is submitted once.
  `ResidentCommittedError` (known committed) is re-raised without retry. After a
  failure it reconciles an identical already-recorded outcome through
  `_outcome_recorded` (lost commit acknowledgement). A failure carrying a
  recovery or restoration failure note, or a reconciliation read failure, is
  not retried and fails closed. On exhaustion one warning logs the exception
  type, case, request, attempt, status and `repr(receipt_ref)`, then the
  existing `ResidentCommittedError` is raised with wording that does not assert
  the stored state.
* `src/core/tests/test_resident_decisions.py`: strengthened the existing
  failed-outcome test (handler runs twice, receiver once, receipt logged); added
  failed-write retry, lost-commit-acknowledgement and unverified-recovery cases.
  They run on JSON, SQLite and, with the opt-in flag, SQL Server.

No store, schema, API, Quality, `app.py` or guard file was changed. F2 was
already present on main and is not new delivery. F3 is not implemented.

## Validation (owner demo targeted tier)

Source base `a04668ae94b5c2f38e6c55ed789db245e8c71d16`; environment: fresh
owned venv in the scratch directory, Python 3.12.3, `pip install -e` of
`src/core`, `src/agents`, `src/api`, `ruff==0.17.1`, `mypy==2.4.0`,
`mssql-python==1.15.0` (installed only after the selected commands proved them
missing; a first install of an unpinned `mssql-python` and `pyodbc` was
superseded by the declared pin).

| Check | Command (from `src/core` unless stated) | Result |
| --- | --- | --- |
| Missing dependency proof | `python -m unittest discover -s tests -p test_resident_decisions.py -k forward_failed_outcome -q` in empty venv | import errors, then pip install |
| Red, base source | `... -k forward_failed_outcome -k lost_commit -k unverified_recovery -k outcome_save_failure -v` (`red.log`) | exit 1, 12 run, 4 failures, 4 errors, 4 MSSQL skips |
| Green focused | same command (`green-focused.log`) | exit 0, 12 run, OK, 4 MSSQL skips |
| Whole module, JSON and SQLite | `python -m unittest discover -s tests -p test_resident_decisions.py -q` (`module.log`) | exit 0, 317 run, OK, 113 skipped (MSSQL class opt-in) |
| Lint | `ruff check` on both files; `ruff format --check` on the test file (source is format-excluded by config) | pass |
| Types | `mypy` (strict, 279 files) | first run 3 test typing errors, fixed; second run exit 0 |
| API consumer | `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_resident_api.py -q` from `src/api` | exit 0, 20 run, 1 skipped |
| SQL Server attempt 1 | `-k forward -v` under `flock -n /tmp/ama-rpi-heavy.lock`, owned container | adverse: 20 errors, `mssql_python` missing (`mssql-forward-attempt1-...log`) |
| SQL Server attempt 2 | same after installing the pinned driver | exit 0, 60 run, OK, 0 skips (`mssql-forward.log`) |

SQL Server evidence: one disposable `mcr.microsoft.com/mssql/server:2022-latest`
container with label `zf.task=1292-sql-disposable` (the fixed label the existing
`sqlguard` demands), published on `127.0.0.1` only, generated password never
logged, no holder of the shared heavy lock found before admission, single
non-queued `flock -n`, container removed on exit (`docker ps -a` empty).
The MSSQL class ran all 20 `forward` tests including the four new or changed
cases. The campaign is a targeted subset of the resident decision tests, not
the whole MSSQL class.

## Limits

* Not run: full gate, browser, hosted CI, cloud, real receiver. Not a
  whole-class SQL Server run.
* The JSON audit-truncate `OSError` that can replace the original error inside
  `_operation` is not marked as unverified recovery; it is a pre-existing path
  and was not widened.
* The lost-commit test clears `persisted` to simulate a lost acknowledgement; a
  genuine dropped COMMIT connection was not provoked.
* F3 and acceptance of the whole issue remain open.

## Correction cycle 1 of 5 (after the original review)

Original [review](../../reviews/2026-11-09/issue-1238-outcome-retry-recovery-1109-review.md)
finding RV-1 (test strength on JSON) is unchanged and preserved. Correction:
the lost-commit test now spies `_outcome_recorded` and asserts that SQL
reconciles a committed outcome (no second write) while JSON, which restores the
pre-image, rewrites it. A first attempt that counted handler calls was
abandoned because SQL runs the handler more than once per operation; it failed
(3 != 2, 2 != 1) and was replaced. No source change. Counter: 1 of 5 used; no
second Review, per the one-pass rule.

Diagnostics after the correction: `ruff check` and `ruff format --check` pass;
`mypy` exit 0 (279 files); resident module JSON and SQLite exit 0, 317 run, OK,
113 skipped (`module2.log`); SQL Server `-k forward` exit 0, 60 run, OK, 0 skips
(`mssql-forward.log`). Adverse: the first rerun (`mssql-forward-run3-stale-manifest.log`)
failed 20 errors because the harness reused the previous run's manifest; the
owned stale manifest was removed and the campaign rerun once (container removed
after every run). The earlier SQL Server results above predate this correction.

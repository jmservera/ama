---
title: Issue 107 old-image SQL probe correction changes
description: Changes record for the execution-readiness correction; opened before any source edit
ms.date: 2026-11-17
---

## Status

Opened before implement-start. No source file had been edited at this point; opening candidate db7ad278b505e764b627d095e21f88db6fb622a1.

## Planned files

* `src/api/checks/old_image_sql_probe.py`
* `src/api/checks/old_image_worker.py`
* `src/api/tests/test_old_image_sql_probe.py`
* `src/api/README.md`

## Baseline (before edits)

* `tests.test_old_image_sql_probe`: 17 tests OK under the external venv.
* Ruff check and format on `src/api`: clean. `mypy` over the whole `src/api` project reports 73 pre-existing errors in 67 files, such as the missing `playwright` stub; affected files are checked individually below.

## Entries

* `src/api/checks/old_image_sql_probe.py` rewritten (about 1,400 lines after format): findings 1 to 8 below. `old_image_worker.py` publishes `tasks`, `executed`, `reinvoked` and `provider_calls` into its record before each risky operation and keeps the partial record on error. The worker edit was first applied with a short Python script rather than the edit tool; the diff is the same content.
* `src/api/tests/test_old_image_sql_probe.py` rewritten for the fixed protocol and an in-memory Docker fake: 34 tests (17 before).
* `src/api/README.md`: private-network topology, fixed protocol, bounds and cleanup replace the host-networking sentence.
* After a diagnostic in the draft, two further fixes were made with a Python script: an unreadable inspect now returns an error instead of "none" (it had counted as verified absence), and an ambiguous create that reconciles to a verified ID is reported as `reconciled_after_ambiguous_create` and may end ok once removal is verified.

## Finding dispositions

| # | Disposition |
| --- | --- |
| 1 | Accepted, refined: internal network cannot publish ports, so SQL also sits on the default bridge with a 127.0.0.1 publish; workers attach only to the private network; attachments read back; network ID and ownership verified before removal. |
| 2 | Accepted: `PROTOCOL` plus `check_step`; malformed or absent evidence is INSUFFICIENT. |
| 3 | Accepted: no SPID uniqueness; limits reported in `LIMITS`; reused-SPID regression. |
| 4 | Accepted: caller-owned record, adverse-first judge gated by a trigger readback; worker publishes partial record. |
| 5 | Accepted: `Docker` class with pre-registered names, exact name plus run labels, bounded retries, absence verification, private network included. |
| 6 | Accepted: four-column pool compared on both ceilings and both consumed quantities. |
| 7 | Accepted, refined: abandonable daemon-thread calls with a whole-run deadline, capped output, `os._exit` after reporting when a call was abandoned. |
| 8 | Accepted: canonical parent, exclusive mkdir, canonical location re-checked. |

## Validation (this runtime only; no Docker, SQL or full gate)

* Evidence: `evidence-107-c1/checks-1.txt`, `checks-2.txt`, `regressions-vs-original.txt`.
* `ruff format` and `ruff check` on the three Python files: clean. `mypy --strict` on them: no issues.
* `tests.test_old_image_sql_probe`, `tests.test_assistant_restart_non_replenishment` and `tests.test_assistant_release`: 113 tests OK, 7 skipped. All seven skips are `MssqlUnleasedRevocation.*` in `test_assistant_release` with reason `needs disposable SQL Server (ZF_TEST_MSSQL=1)`. No unexpected skips or errors.
* CURRENT-source SQLite self-test: ACCEPTED, exit 0, labelled `current-source-self-test`, not old-image evidence.
* Regression check against the original db7ad judge using the ORIGINAL fixtures: empty module maps and a nonzero exit were ACCEPTED, and a violation followed by a failed later step came out INSUFFICIENT; the corrected judge returns INSUFFICIENT, INSUFFICIENT and VIOLATED. The new tests cannot be imported against the original module because the new API (protocol table, Docker lifecycle, deadlines) does not exist there.
* Failed attempts: first test run had two failures (reconcile reporting and inspect failure treated as absence), both fixed; first strict mypy run had four errors in the new test file, fixed.


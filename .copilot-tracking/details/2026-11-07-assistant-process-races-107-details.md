---
title: Details for OS-process race and restart tests (#107, C10)
description: Worker contract, assertions, light checks and the literal future actual-SQL plan
ms.date: 2026-11-07
---

Plan: [plan](../plans/2026-11-07-assistant-process-races-107-plan.md).

## Worker (`assistant_process_worker.py`)

Run as `python assistant_process_worker.py` with one JSON argument file path. The file holds: store kind (`sqlite` with seed and database paths, or `mssql` with the seed path and state directory), configuration overrides, a label, the call-log path, the barrier directory, a deadline in seconds and the ordered list of actions. SQL connection settings come from an explicit minimal environment built by the parent (only `ZF_SQL_*`, `ZF_TEST_MSSQL`, `ZF_DATA` set to a temporary path, `PATH` and `PYTHONPATH` from the parent's `sys.path`); the password is never put on a command line or in a file. The worker opens a source-current store, sets the provider (`model_version`, `release = store.release_context`, counting `evidence`) without reinstalling releases, writes `ready-<label>`, waits for `go` until the deadline, runs its actions (`execute <task id>` or `invoke <capability>`), prints one JSON result line and exits. Provider calls append one line to the call log with `O_APPEND`.

## Parent

Spawns exact `subprocess.Popen` children with captured output; in `finally` it kills and waits only those exact children; all waits have a hard timeout. Counts call-log lines and reads durable state through its own connection.

## Case 1 assertions (finite allowance race and restart)

* Three pending proposals (three registry assistants, case ZF-1), allowance of two calls, four processes each try every task in rotated order after the barrier.
* No worker errors. Provider call log has exactly two lines. Two proposals are `ready`, one `disabled` with the "allowance exhausted" reason and one matching event; `assistant_attempts` has exactly two rows; `used_calls` is two and `calls` is two.
* Restart wave: two fresh processes with a configuration of 1000 calls and a later expiry execute a newly invoked fifth-assistant proposal: it returns false, no new call line, state `disabled`, `calls` still two and `used_calls` still two.

## Case 2 assertions (revocation, race, restart)

* A pending, unleased CAP proposal and a positive control are verified pending before the barrier. Three processes wait at the barrier; the parent revokes `fx-<cap>` through a separate service with the approver set, then releases the barrier.
* All three return false, the call log is empty, the task is `disabled` with attempts 0 and no owner, the reason begins "Release admission denied", exactly one `disabled` event carries it, the release status is `revoked`, and `used_calls` is unchanged.
* Restart wave of two fresh processes with a larger allowance configuration: false, no call, same state and one event, `used_calls` unchanged.

All assertions are about the existing linearization contract; none invents policy.

## Light checks (no services; own venv; external caches; PYTHONDONTWRITEBYTECODE=1; unmasked exits)

From `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`: the two new methods on the SQLite class, then `test_assistant_release test_assistants test_continuity`; `ruff check .`; `mypy`; the added blocks formatted as the config requires; import-origin proof. The MSSQL class skips without `ZF_TEST_MSSQL=1`, and that skip is disclosed.

## Literal future actual-SQL plan (proposed only; never executed from a receipt)

Under one nonqueued shared-lock admission, the runner `python3 tools/rpi-checks.py --all --base <fresh current origin/main> --out <new external directory> --jobs 2 < /dev/null`, read from the then-current tools and README, selects the class `test_assistant_release.MssqlUnleasedRevocation` through `SQL_SELECTORS` with its owned loopback container. Evidence required: the verbose SQL log shows the two new methods as `ok` and not skipped, the worker processes' PIDs and exit codes appear in test output, and all 17 groups pass on fresh images. A normal merge of the then-current main precedes it if main moves. Expected resources match the previous gate: one SQL container (3 GB, 2 CPUs), fresh images and Chromium, tens of GB of external output.

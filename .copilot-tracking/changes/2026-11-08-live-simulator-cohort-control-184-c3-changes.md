---
title: "Changes: #184 correction 3"
ms.date: 2026-11-08
---

Source change: `src/api/checks/sensor_sql_check.py` only, Ruff 0.17.3
(`python3 -m ruff format --no-cache`), one statement re-wrapped (lines 109-110).
Blob before `1d84574c`. AST dump SHA-256 before and after are equal
(`/tmp/c3-ast-pre.txt`, `/tmp/c3-ast-post.txt`); diff is 1 insertion, 3 deletions.
`sensor_consumer.py` and every other file are untouched.

## Correction of C2 records (additive)

C2 wrongly named `sensor_consumer.py` as the file failing `ruff format --check`.
It was `sensor_sql_check.py`; C2 files are not rewritten.

## Commands (stdout/stderr/exit captured separately under /tmp/c3-*)

| Command | Exit | Result |
| --- | --- | --- |
| `ruff format --no-cache` on the one file | 0 | reformatted |
| six-file `ruff format --no-cache --check` | 0 | 6 files already formatted |
| six-file `ruff check --no-cache` | 0 | all passed |
| unittest test_live_control test_live_receiver_sql test_sensor_ingestion | 0 | 78 tests OK, 2 skipped (SQL-only tests without a server) |
| `flock -n /tmp/ama-rpi-heavy.lock ... sensor_sql_check.py` (task-owned MSSQL, temp venv, exact-grant principal) | 0 | 70 tests OK, no skips; container removed |

No other lock holder, process or container was present; memory 6.8 GB
available, 12 GB disk free. The JSON `"passed": false` line is the existing
deliberate negative test. The two failed C2 SQL attempts' raw output was
overwritten; only their descriptions (test cleanup and type-padding bugs) survive.

Bicep and infra tests were not re-run: no Bicep, infra, config or other source
input changed since C2 (`git diff --name-only` shows only the one file), so the
C2 results (Bicep build/lint exit 0, infra 76 OK at `78d25a13`) are historical
but apply to identical inputs.

Ignored `src/core/.ruff_cache/` (coordinator probe) is preserved; the tree is
not ignored-inclusive clean. Not run: mypy (no typed code changed), browser,
full gate, any cloud step.

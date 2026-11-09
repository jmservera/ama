---
title: Issue 107 restarted clamp focused-validation changes
description: Changes record for the LIGHT focused checks; actual SQL not run
ms.date: 2026-11-08
ms.topic: reference
---

No source, test or tool change. Plan and critique were committed first (`57b47b526`), see the [plan](../plans/2026-11-08-assistant-restarted-clamp-107-focused-plan.md).

## Raw LIGHT evidence (outputs under `/home/azureuser/.local/share/ama/gates/g107-clamp-light-r1`)

From `src/api`, existing editable venv (`zava_forward.core` resolves inside this worktree), `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=tests:../core/tests:../agents/tests`, no private data.

| Command | Result |
| --- | --- |
| `python -m unittest -v test_assistant_release.SqliteUnleasedRevocation test_assistant_release.MssqlUnleasedRevocation` (log `light2.log`) | exit 0, 8 tests, `OK (skipped=4)`; three SQLite process methods `ok`; four MSSQL rows skipped (`ZF_TEST_MSSQL` unset) |
| `ruff check . --no-cache` | exit 0 |
| `mypy` (cache in scratch) | exit 0, 190 files |
| `git diff --check` | clean |

Source identity: `assistants.py`, `assistant_process_worker.py` and `tools/rpi-checks.py` blobs equal `origin/main` `0f05e9aae70768def8d1d9c300215f9ee2f11638` (unchanged on re-fetch); diff against main outside tracking is the 27-line test only. Ignored-inclusive status clean.

## Not run

Actual MSSQL for the three `MssqlUnleasedRevocation` methods is unexecuted and unverified; the canonical lock is held by issue 86. No runner, Docker, browser, scanner or `--all`/`--changed`. The earlier deviations (in-tree mutation, narrower assertions) remain recorded as in the currency plan.

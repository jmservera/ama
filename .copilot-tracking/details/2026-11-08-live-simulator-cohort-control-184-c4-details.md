---
title: "#184 C4 details"
ms.date: 2026-11-08
---

## Commands (planned)

* Merge: `git merge --no-edit origin/main`, message Conventional Commit style `merge: integrate origin/main fa7ae0c9 into live simulator parent`, with the Copilot trailer.
* Tree comparison: `git diff --stat origin/main HEAD -- src infra .github/workflows` and the same against the merge-base for the ten main source paths.
* Environment: `python3 -m venv /tmp/v184-c4-<timestamp>`, then `pip install ./src/core ./src/agents ./src/api` from the worktree. If pip builds leave build dirs in the repo, record them as ignored artifacts, do not delete.
* Lint: `python3 -m ruff check --no-cache` and `ruff format --no-cache --check` on the six files: live_simulator.py, live_receiver.py, sensor_sql.py, sensor_consumer.py, test_live_receiver_sql.py, sensor_sql_check.py.
* SQL: `flock -n /tmp/ama-rpi-heavy.lock <venv>/bin/python src/api/checks/sensor_sql_check.py`.
* Every command writes `/tmp/c4-<name>.out`, `.err`, `.exit` separately; exit read from the process, not a pipe.

## Stop conditions

Merge conflict, origin/main movement beyond docs, lock held, disk under 5G, pip failure due to missing network.

---
title: "#184 current-main validation details"
ms.date: 2026-11-09
---

## A1 merge

`git merge --no-ff 1f28d09130c8e058a0436d468e6a22f3c4c24f47 -m "merge: bring origin/main 1f28d0913 into #184 parent (no source conflict)"`. Verify `git diff HEAD~1 HEAD --stat` matches the main delta and that the merge tree equals 3b8567e0a.

## A2 relevance

* `git rev-parse HEAD^1:<path>` against `HEAD:<path>` for each of the 31 parent-changed non-tracking paths: all equal, except the three overlapping docs/README paths where the merged text must contain both intents.
* Python: import `live_control, live_receiver, live_simulator, sensor_handover_verify, sensor_consumer, sensor_sql, sensor_analysis_store, device_provision, live_readings, sensor_consistency` and `sensor_sql_check`; assert paired_equity not in sys.modules.

## A3 checks

* core `python -m unittest tests.test_paired_equity -q`, core sensor and live selections as smoke, `ruff check`, `ruff format --check`, `mypy` on core (settings in src/core) using /home/azureuser/venv-184 tools.
* api and tools checks only if A2 shows a changed input.

## A4 SQL (revised by critique: rerun, no reuse)

Rerun both selectors; record pip freeze, image digest, container ownership label and zero-skip parse. Add `sys.settrace`-free import trace: run each selector module under `python -X importtime` or list `sys.modules` after test load and assert no paired_equity.

Superseded reuse rule (kept for history):

Reuse rule: identical source blobs, test files, pip freeze of venv-184, container image digest and tool versions as recorded; the SQL logs live in /home/azureuser/logs-184-pp. Otherwise run the plan-defined rerun in an owned disposable container with a nonqueued lock.

---
title: "#184 C4 plan: one ordinary merge of origin/main and focused revalidation"
ms.date: 2026-11-08
---

Prospective plan. Details: [details](../details/2026-11-08-live-simulator-cohort-control-184-c4-details.md).

* [ ] 1. Commit C4 research and plan/details before any merge.
* [ ] 2. Re-fetch origin/main. If it is not fa7ae0c9, re-project the merge and stop on conflict or unexpected source movement.
* [ ] 3. One ordinary `git merge origin/main` (no rebase, force, stash). Stop and report on conflict.
* [ ] 4. Prove ancestry (2dc125f97, 9476dc961, 33a32831, origin/main) and compare integrated src, infra and .github/workflows trees with main and the merge-base projection. Record the tracking artifacts separately.
* [ ] 5. Create a new uniquely named isolated venv outside the repo, pip install src/core, src/agents, src/api (non-editable, built from the integrated tree), record importlib.metadata and module `__file__` for each, assert they resolve to the immutable copy or this checkout.
* [ ] 6. Six-file Ruff lint and format check, relevant unit tests (test_live_control, test_live_receiver_sql, test_sensor_ingestion plus main's ten changed test files that run without browser), each with separate new stdout, stderr and exit files.
* [ ] 7. Recheck lock holder, disk, RAM. Run src/api/checks/sensor_sql_check.py under non-queued flock; record backend, count and skips. Busy means stop and report resume conditions.
* [ ] 8. Write changes and author Review, commit, report.

Constraints: no full gate, browser, Azure, model, push, PR, deletion of any earlier output or venv.

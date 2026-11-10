---
title: Current-main integrated journey checkpoint 440 (1924) details
ms.date: 2026-11-09
task_id: 440-current-main-1924
---

## Environment

* Owned scratch directory created with `mktemp -d /tmp/i440-1924-XXXXXX`; its path is recorded in `/tmp/i440-1924-dir.txt`. It holds the virtual environment and every log. Only this exact directory is removed at the end.
* Python 3.12.3; `pip install -e src/core -e src/agents -e src/api` into that environment. Import paths verified under this worktree (the global editable installs point at another checkout and are not used). No private data, credential, model or Azure access; `ZF_DATA` is left to the tests' own temporary stores.
* Sanitized environment (critique PC-001): every check runs under `env -i` with only `PATH`, `HOME`, `TMPDIR` and `ZF_DATA` pointing inside the owned scratch directory, plus `LANG=C.UTF-8` and the documented `PYTHONPATH`. All `ZF_*` SQL, Azure, browser and benchmark opt-in switches and every credential are therefore unset. The effective non-secret settings are printed to the log header. The ambient shell was checked and holds no `ZF_*`, Azure or OpenAI variable.
* Provenance (critique PC-002): before each run and again after, require `git status --short --untracked-files=all` to be empty (the scratch directory is outside the worktree) and record `HEAD`, `HEAD:src` and the `src` tree. A preflight prints `__file__` for the three package roots and each selected test module and refuses to run if any resolves outside this worktree. Any tracked or untracked source change stops the checkpoint.

## Selected checks (producer exit captured per process, no pipe masking)

| Id | Directory | Command | Purpose |
| --- | --- | --- | --- |
| A1 | `src/core`, `PYTHONPATH=tests` | `python -m unittest` over `tests.test_sensor_consumer tests.test_sensor_consumer_live tests.test_sensor_stream tests.test_resident_sensors tests.test_sensor_privacy tests.test_chat_panel tests.test_gates tests.test_handoff_lifecycle tests.test_resident_decisions tests.test_resident_choice_queue tests.test_quality_procurement tests.test_ai_consumption_safety tests.test_journey_acceptance` | simulator to persistence contracts, lifecycle gates, resident consent, AI limits, chat receipts |
| A2 | `src/api`, `PYTHONPATH=../core/tests:../agents/tests:tests` | `python -m unittest` over `tests.test_live_control tests.test_live_simulator tests.test_simulator_admin tests.test_iot_stream tests.test_iot_credential_hygiene tests.test_sensor_ingestion tests.test_sensor_handover_demo tests.test_ai_boundary tests.test_ai_call_site_inventory tests.test_chat_panel tests.test_assistants tests.test_resident_assistant_api tests.test_role_matrix tests.test_photo_availability tests.test_workbench tests.test_case_journey` | control, admin, HTTP routes, AI unavailable and manual routes, roles, photo, workbench |
| A3 | `src/agents`, `PYTHONPATH=tests` | `python -m unittest tests.test_queue_azure tests.test_worker` | merged queue adapter and worker mechanics |

If a module name does not exist or fails to import, the exact error is recorded and the module is reported as not run. Any test class selected here that needs a disposable SQL Server skips by design; those skips are counted and reported as not SQL evidence.

## Reused evidence (not rerun)

* #1326 priority SQL campaign: 3 processes, 148 tests, 67 on SQL Server, 0 skips, on `src` tree `86bc00e19a167e517ae2955ad88d6e2f7b4eac26`, with the query-exit, timeout-path, mutable-tag and endpoint-authentication limits of its Q1 qualification. Identity check here: `git rev-parse HEAD:src` equal to that tree. Carried limit (critique PC-004): its external verifier gated test outcomes only and did not fail on missing or failed cleanup; cleanup was observed separately (same container id in two files, empty leftover-database capture, executing-session report of an empty container list) and the leftover query exit status was not retained.
* #1313 and #1315 browser observations from the previous checkpoint, with the #1320 chat receipt delta as the only runtime change; not rerun and not extended to chat browser behavior.

## Pack, index and log

One dated section appended to `docs/architecture/cutover-evidence-pack.md` after the controls section, heading `## Integrated current-main journey checkpoint (2026-11-09, Refs #440 #81 #123 #184 #136)`; one entry in `docs/reference/README.md` and one appended entry in `docs/reference/log.md` following existing conventions; no other documentation change.

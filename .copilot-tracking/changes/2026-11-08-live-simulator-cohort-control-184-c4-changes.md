---
title: "#184 C4 changes: ordinary merge of origin/main fa7ae0c9"
ms.date: 2026-11-08
---

## Change

* One ordinary merge of origin/main fa7ae0c9770e890f82482456bfcb8e97f1e05429 into 33a32831 (after the prospective C4 commit 86e0ba5b). Merge exit 0, no conflicts, no source edit by hand. Merge parents: 86e0ba5b and fa7ae0c9. Tree 5191b3cedd9d3f781a6e4884701a2df67442b2ff.
* Ancestors confirmed: 2dc125f97 (#185), 9476dc961 (#188), 33a32831, fa7ae0c9.
* Main's nine non-README source paths are byte-identical in the merged tree. src/api/README.md merged both sides (receiver docs plus main's changes).
* `git diff aa16ae72 HEAD -- src infra .github/workflows` is empty: the integrated source, infra and workflow trees equal the precomputed projection. Tracking artifacts are additional.
* No unmerged #1288 source, no live activation.

## Validation (new files /tmp/c4-*.{out,err,exit}; exits read from the process)

| Check | Exit | Result |
| --- | --- | --- |
| venv /tmp/v184-c4-1794169588, pip install src/core, agents, api (non-editable) | 0 | built from this tree |
| importlib.metadata and module `__file__` | 0 | core, api, mssql-python resolve to venv site-packages; sensor_sql, live_receiver, sensor_consumer, live_simulator byte-identical to the checkout; agents is a namespace package (file None) |
| ruff 0.17.3 check, six files | 0 | clean |
| ruff format --check, six files | 0 | 6 already formatted |
| unit: test_live_control, test_live_receiver_sql, test_sensor_ingestion, test_document_controls, test_content_standard, test_role_screens_conformance, plus the two main checker tests | 1 | 126 run, 2 skipped (SQL-only, no server), 2 import errors from missing `checks` on path |
| rerun test_data_operator_ai_state and test_atlas_tensions_checker with src/api on path | 1 | data operator OK; atlas module needs `playwright`, not installed (browser tooling, main's file unchanged, not installed per CI-first scope) |
| sensor_sql_check.py under non-queued flock on /tmp/ama-rpi-heavy.lock | 0 | 70 tests OK, 0 skips, task-owned SQL container created and removed |

Lock was free, disk 11G, RAM about 7G available, no other containers.

## Limitations

* Atlas tensions checker test not run (playwright missing); it is main's own unchanged file.
* Mypy, Bicep and infra tests not re-run; infra and workflow trees equal the aa16 projection, and no branch infra file changed in this merge. Earlier results stay historical.
* pip left ignored build dirs and egg-info under src/core, src/agents, src/api, preserved per the no-deletion brief. Together with the coordinator's src/core/.ruff_cache, the tree is not ignored-inclusive clean. The venv and all logs are preserved.
* Historical: /tmp/v184 was removed in C2 and C3 despite the no-cleanup brief; two C2 SQL attempt outputs were overwritten.
* Open: Low restricted-grant main-entrypoint test gap; Azure schema provisioning owner; live activation; whole-issue criteria all still unmet.

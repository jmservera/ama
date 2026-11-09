---
title: Ranking archive ancestor durability 1258 continuation changes
description: Changes and evidence for the boundary and API ancestor-fault tests
ms.date: 2026-11-08
---

* Added to `src/core/tests/test_ranking_publication.py`: `test_chain_ends_before_the_first_non_writable_ancestor`, `test_mocked_root_run_where_every_ancestor_looks_writable_syncs_the_whole_chain`.
* Added to `src/api/tests/test_ranking_publication_wiring.py`: `test_parent_folder_sync_failure_is_audited_as_unconfirmed_and_retry_is_sound`.
* No production, runner, Store or server edits. Tests passed on unchanged source on first run; no red run was fabricated.

## Evidence

* Scratch `/home/azureuser/.local/share/ama/gates/g1258-boundary-api-light-1108` (venv, non-editable install of a `git archive` export of the frozen head, with the two changed test files copied in; synthetic `ZF_DATA` and `HOME` under scratch). Import origin: `.../venv/lib/python3.12/site-packages/zava_forward/core/ranking_publication.py`.
* Core: `PYTHONPATH=tests python -m unittest discover -s tests -p "test_ranking_publication*.py"` exit 0, Ran 86, OK, no skips (non-root uid 1000). Logs `core.log`, `api.log`.
* API: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p "test_ranking_publication_wiring.py"` exit 0, Ran 23, OK.
* `ruff check` and `ruff format --check` on both files pass.

## Limitations

* C1 relies on permission bits as non-root; under root it skips. C2 is mocked and proves only the code path, not live root behavior.
* Mocked syscalls are not crash or power-loss proof; R1 and R4 remain open.

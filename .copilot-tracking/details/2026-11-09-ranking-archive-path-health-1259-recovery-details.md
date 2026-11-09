---
title: Issue 1259 recovery preparation details
description: Phase details and exact commands for the unchanged-source validation
ms.date: 2026-11-09
---

## Phase 3 details

Scratch directory `/home/azureuser/.local/share/ama/gates/g1259-prep-demo-1109` (external, uncommitted). Synthetic `ZF_DATA` under it; `TMPDIR` and `PIP_CACHE_DIR` under it; no private data, credentials, global installs or network calls beyond pip dependency download into the scratch cache.

* Export: `git archive HEAD src`, then a new venv with non-editable `pip install ./core ./agents ./api`; module origin confirmed under the venv site-packages.
* Core: in `src/core`, `python -m unittest discover -v -s tests -p 'test_ranking_publication*.py'`.
* Class selector: `python -m unittest discover -v -s tests -p test_ranking_publication_runner.py -k UnusableArchivePathTests`.
* API: in `src/api`, `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest -v test_ranking_policy test_ranking_publication_wiring test_ranking_scale`.
* Agents: in `src/agents`, `PYTHONPATH=../core/tests:tests python -m unittest -v test_cohort_ranking_eval`.
* Red check: scratch `red/` copy of `src/core` with only `ranking_publication.py` and `ranking_publication_runner.py` replaced by their `6d793bc3a` versions, tests from HEAD, same class selector.

Pass criteria: every exit 0, no unexplained skips. The red check must fail for the new class (failing-first still discriminates).

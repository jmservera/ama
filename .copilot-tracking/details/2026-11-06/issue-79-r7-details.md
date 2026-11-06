---
title: Issue 79 details, corrective continuation r7
ms.date: 2026-11-06
---

* Environment: `/tmp/zf79venv/bin/python` with `PYTHONDONTWRITEBYTECODE=1`, run from `src/core`; the import identity of `zava_forward.core` and the test modules is checked and recorded in the changes file. No installation unless a command fails for a missing dependency. No `uv`.
* Caches: `RUFF_CACHE_DIR` and `--no-cache` for Ruff, `--cache-dir` external for mypy, under a new `/tmp/i79-r7.*` scratch directory that is left in place (no deletion).
* RED commands run before the source edit, GREEN after; raw logs saved under `/tmp/i79-r7-logs/`.
* Selected tests: `test_ranking_publication*.py` only. No broad suite; no gate.
* Preserved qualification: installed Ruff 0.17.3 and mypy 2.4.1 differ from the maintained pins 0.17.1 and 2.4.0; the new runner module's override relaxes only untyped-call checking. Results are light, not pinned full results.
* Identity: repository-local author and committer `8036360+jmservera@users.noreply.github.com`; Copilot trailer.

---
title: Issue 1231 details r2 (owner-approved hard-link contract verification)
ms.date: 2026-11-06
---

* Allowed diff: new dated r2 records; if a gap is proven, `ranking_publication.py` minimally, the existing test modules for the focused regression, and the matching README sentence. Nothing under R1 or earlier tracking paths, memory, original case study, index or log.
* Regression shape (real filesystem, no fake result for the property tested): to produce a genuine unsupported-hard-link condition without a special mount, wrap only `os.link` to raise `OSError(errno.EPERM, ...)` as an unsupported filesystem does, then assert through `publish` and `runner.run("publish")`: the error surfaces (helper) or `publish_failed` with `written` absent (runner), no `ranking-*.json` record exists, the owned stage is gone, foreign `.tmp` and unrelated files are unchanged, and a later publish on the same archive with real `os.link` succeeds. The errno injection is the only simulated element; no real unsupported mount was tested.
* Commands (light): from `src/core`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=<child>/src/core/src:<child>/src/core/tests`, `/tmp/zf79venv/bin/python -m unittest test_ranking_publication test_ranking_publication_runner`; API `test_ranking_publication_wiring` from `src/api` with the child core on the path; Ruff `--no-cache`, format check and mypy `--cache-dir` external on edited files. Import proof prints `__file__` and SHA-256. Each command writes to a new path under `/mnt/ama-gates/1231-r2-light-0611-<unique>/`; a retry gets a new path.
* Review wording: author-only, not independent, no human-review box, no FULL or publication claim, owner decision limited to the quoted contract.

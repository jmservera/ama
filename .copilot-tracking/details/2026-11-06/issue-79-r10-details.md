---
title: Issue 79 details, continuation r10
ms.date: 2026-11-06
---

* Allowed diff: `src/core/src/zava_forward/core/ranking_publication_runner.py`, `src/core/tests/test_ranking_publication_runner.py`, the runner paragraph in `src/core/README.md`, and new dated r10 records (research, plan, details, changes, review, state). Nothing under earlier tracking paths, parent carry-in files, policy, gate or scanner files.
* Regression tests (written first, RED before the fix): F1 CLI and `load_cases` with `closed` of `"false"`, `null`, `1` and an all-malformed file, asserting refusal, a non-zero exit and no archive; F2 `schedule` with an all-invalid archive and a good-current plus damaged archive, asserting status `problem`, CLI exit 1, kept `due` and `latest`, and the approval refusal retained for an unsigned policy; F3 publish once, then retry with `free_bytes` returning 0, asserting `already_published`, unchanged bytes and original date, while a new record on zero capacity is still refused; F4 `today` of `9999-12-31` for each operation through `run` and `main`, and an archived latest of `9999-12-31` for `schedule` and `publish`, asserting no exception, no write and a structured result.
* Command shape (light only): from `src/core` with `PYTHONDONTWRITEBYTECODE=1` and `/tmp/zf79venv/bin/python`, `-m unittest` on `test_ranking_publication` and `test_ranking_publication_runner`; Ruff `--no-cache`; format check; mypy with `--cache-dir` under `/tmp`. Every command writes to a path under `/tmp/79-functional-r10-1106/` that does not yet exist, and its exit code is recorded directly. A retry gets a new path.
* Not run: gate (including `--changed`), SQL, browser, Docker, install, scan, lock acquisition, cloud, push, cleanup or deletion.
* Wording rules: author-only review; no human-review box; the r9 receipt is historical for this head; no #79 acceptance or closing keyword.

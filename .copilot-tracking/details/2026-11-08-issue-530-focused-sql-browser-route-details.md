---
title: Issue 530 focused actual SQL and chat browser route details
ms.date: 2026-11-08
---

## Phase 2

* `git fetch origin main`; stop and plan currency if Main is not 0f05e9aa. Compare `git ls-tree -r` blob ids of `src/`, `tools/`, `infra/` and `.github/` between HEAD and `209e585cf` (must be identical) and against Main for production source.
* Run Python with `-B` and `PYTHONPYCACHEPREFIX`, and print `zava_forward.core`, `agents` and `api` paths from the external venv `/tmp/rpi-530-sqlbrowser-venv`; require this worktree.

## Phase 3

* `python -m unittest test_rpi_checks` from `tools/` (expect 92 OK), `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --check` on both tools files and, from `src/api`, on the four browser checkers, `mypy --strict` on both tools files, `git diff --check`. Use `RUFF_CACHE_DIR`, `MYPY_CACHE_DIR` and `PYTHONPYCACHEPREFIX` under `/tmp/rpi-530-c3-cache`. Unit tests run with `TMPDIR` external. Do not rerun SQLite or skip-only suites.
* Record every exit, count and skip.

## Phase 4

* Prepared SQL route: `python3 tools/rpi-checks.py --changed --jobs 1 --lock-timeout 0 --base <fresh-main> --out <new-external> < /dev/null`, selecting the group list re-read at admission (predicted seven groups). Required: 21 `ok` headers in `MssqlChatPrivacy` (13), `MssqlChatRoleProjection` (4), `MssqlChatDemoMeter` (4) exactly as listed in `SQL_CHAT_REQUIRED_TESTS`.
* Prepared browser evidence: the chat check command in the research record, three states, pinned axe hash, PASS line, results file.
* Both stay UNEXECUTED until a coordinator admits a non-queued heavy window holding the canonical lock throughout.

## Critique dispositions applied

* LIGHT scope: the runner unit suite includes tests that start a synthetic loopback server and call its `/healthz`. This local loopback call is explicitly authorised as part of the unit suite (no external, model or Azure call); it is recorded, not hidden. No other network use.
* Lock ownership: the canonical lock is acquired by the runner itself (`heavy_lock(args.lock_timeout, args.heavy_lock_fd)`). With `--lock-timeout 0` the runner fails closed if another holder exists. If the coordinator holds the lock and wants the runner to inherit it, admission must name `--heavy-lock-fd` and the descriptor. Admission must state which; neither is chosen now.
* Browser runs before SQL and a browser failure blocks SQL. Claiming either ran requires separate evidence: passing browser evidence (PASS line, results file, three states) and 21 unique `ok` SQL headers.
* Resources: the SQL container is built with `--memory=3g` in addition to `MSSQL_MEMORY_LIMIT_MB=2048`; the browser route downloads Chromium and the pinned axe. Admission must cover current capacity (2 CPU and 4 GiB per worker plus 1 GiB headroom), a short external output path and those downloads.
* Provenance: record test-module origins as well as package paths, and record final HEAD, tree, Main and index flags after the records commit. LIGHT results are source-equivalent evidence (same tracked source blobs), not exact-final-head evidence. Fresh exact-head CI stays a separate merge gate.

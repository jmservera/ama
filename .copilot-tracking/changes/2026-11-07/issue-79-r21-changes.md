---
title: Issue 79 changes, r21 merge of main a1d26534
ms.date: 2026-11-07
---

## Changes

* Planning commit `8d9caf976c255fc9142e607928b33dbee509d0ce` (ref `preserve/issue-79-r21-planning`) preceded the merge. Preservation ref `preserve/issue-79-pre-main1252-merge` = `9b21a6a0d2bc0646076cd2da03f7fc4d088af06e`.
* One normal `--no-ff` merge `573c86feed146fa4320e0c612fca24f72a641a53` (tree `dcf2030ab426c9143c78aa4a1eeca0219f16cc96`). Parents: `8d9caf976` and main `a1d265340ba7d6f14b24e028362b2d5f4bb80126` (fetched twice; scorer run 42381926533 success, no score descendant). No conflict, no rewrite, no push.
* Records only after the merge: this Changes file, the Review, the state JSON, one log entry.

## Proofs

* Incoming: all 15 paths changed by main since `395060275` (13 added issue 1251 RPI records, `tools/backlog-sync.py` blob `43338cb8f`, `tools/test_backlog_sync.py` blob `fca73c2cd`) carry main's blob and mode.
* Topic: all 92 topic-changed paths keep the pre-merge blob and mode. Runner blob `06dcce781`, SHA-256 `5987f45d...`; helper SHA-256 `500e31e4...`. Log diff versus the planning commit is empty before this record's entry; no mode changes.
* Ancestry: `9b21a6a0` and `a1d265340` are both ancestors of the merge.

## Checks

Scratch `/mnt/ama-gates/g79-main1252-preparation-1107`; own-worktree `/tmp/zf79venv` origins verified; `PYTHONDONTWRITEBYTECODE=1`; exits read directly.

* Core ranking 53 tests OK (0); API ranking wiring 15 OK (0); `test_assistant_release.py` 46 OK (0); received `tools.test_backlog_sync` 17 OK (0).
* CI-equivalent tools ruff check, ruff format check (5 files), `mypy --strict` (2 files), `mypy --ignore-missing-imports` (backlog pair): all 0.
* Ranking five-file Ruff check/format 0; mypy `src tests` 268 files 0. Skips: none. Not run: FULL, SQL, browser, scanners, images, AI, Azure.

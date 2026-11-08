---
title: Issue 79 changes, r22 merge of main c1a16482
ms.date: 2026-11-07
---

## Changes

* Planning commit `b7a2f50a2673d2c39a423ac7df73970bc6ee8f86` (ref `preserve/issue-79-r22-planning`); preservation ref `preserve/issue-79-pre-main1255-merge` = `47de325d80eda5665f3e3d3250fedce7a17c85d1`.
* One normal `--no-ff` merge `9c19d76c4b356755012c4585473ee8cdd5187cc9` (tree `13fa7899a516fc7824db264bffe902d8e8c28ec1`); parents `b7a2f50a2` and main `c1a164829e77efe45f5f002740bd79699b89b334` (PR 1255 merge, fetched before the merge). No conflict, rewrite or push.

## Proofs

* All 17 incoming paths (3 modified: `src/api/tests/test_assistant_release.py` `b464f5907`, `tools/rpi-checks.py` `4ead23d75`, `tools/test_rpi_checks.py` `9a64271e2`; 14 added 107 RPI records) carry main's blob and mode. No `src/*/src` production path changed.
* All 98 topic-changed paths keep pre-merge blobs apart from those three declared incoming files; no mode change; log diff versus the planning commit empty before this record's entry.

## Checks

Scratch `/mnt/ama-gates/g79-main1255-preparation-1107`, own-worktree origin proven, `PYTHONDONTWRITEBYTECODE=1`, unmasked exits.

* Core 53 OK; API wiring 15 OK; `test_assistant_release.py` 48 tests OK with 1 skip (the SQL unleased class, needs a SQL server; not run); `tools.test_rpi_checks` 86 OK.
* CI-equivalent tools Ruff check, format check (5 files), `mypy --strict` pair: 0. Ranking Ruff check/format and `mypy src tests` (268 files): 0. Ruff check on received test: 0.
* `ruff format --check` on `src/api/tests/test_assistant_release.py` reports 1 file would be reformatted: pre-existing in main's blob, preserved, not reformatted.
* Not run: FULL, SQL, browser, scanners, images, AI, Azure.

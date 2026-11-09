---
title: Issue 135 C2 import identity plan
description: Prospective corrective plan for hashless identity, single-snapshot digest and CLI sqlite errors
ms.date: 2026-11-09
---

* C2 of five total. Written 2026-11-09T22:46Z (actual) before source changes. Details: `.copilot-tracking/details/2026-11-09/import-exception-135-c2-details.md`. Research: `.copilot-tracking/research/2026-11-09/import-exception-135-c2-research.md`.

## Scope

* Owned: `src/importer/.../exceptions.py`, `mapping.py` (bytes-level preview helper only), `__main__.py`, `tests/test_import_exceptions.py` (and a small mapping test), `src/importer/README.md`.
* Paused and untouched: store, sqlstore, schema, `exception_register.py`, API, UI, core feed and queue.

## Phases

* [x] P1: regression tests first, run red (raw output kept).
* [x] P2: single bounded snapshot, opaque hashless source identity through ledger and adapter (F1, F2).
* [x] P3: CLI sqlite error contract for stage and viewer (F3).
* [x] P4: README claims, importer suite, ruff, format, mypy, real separate-process CLI cases, one Review.

## Validation

Red-first run, full importer suite, ruff, ruff format check, strict mypy, separate-process CLI cases (replace-between-attempts, same basename in two directories, write failure, connection failure, restart). Core suite only if a core file changes (not planned). No SQL or browser service: nothing served is claimed.

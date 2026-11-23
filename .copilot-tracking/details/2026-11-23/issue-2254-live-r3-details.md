---
title: Issue 2254 live details, run 3 (2026-11-23)
---

Phase 2: in `src/core/tests/test_sqlreads.py`, after the existing assertions, call `s.map_view(dict())` (empty filter) and count items with `kind == "hazard"`; assert it equals `tile`. The map cap of 500 exceeds the 60 fixture cases, so mode is `points`. Run `python3 -m unittest` for that module from `src/core` with `PYTHONPATH=src:tests`. Run `python3 -m mypy` in `src/core` only if the test dir is in scope (it is not changed in typing terms).

Phase 3: add note `docs/reference/research/issue-2254-live-r3-2026-11-23.md`, index row in `docs/reference/README.md`, append `docs/reference/log.md`.

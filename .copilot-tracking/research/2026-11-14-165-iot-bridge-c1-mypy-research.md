---
title: PR 1654 Cycle 1 mypy research
ms.date: 2026-11-14
---

* Hosted src-api Type check runs configured `mypy` (files src, tests, checks) and failed on `tests/test_iot_seed_to_quality_ui_bridge.py`.
* Line 45: `# type: ignore[misc]` on `ta.Base` was unused in the configured run, because test_assistants is ignore_errors/skip.
* Line 58: `ta.Provider()` is an untyped call (`no-untyped-call`).
* Reproduced locally with `python3 -m mypy` in `src/api` (2 errors, 264 files).
* Ad hoc single-file runs do need the `misc` ignore, so both modes must pass.

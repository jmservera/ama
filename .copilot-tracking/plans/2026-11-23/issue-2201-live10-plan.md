---
title: Issue 2201 live10 plan
ms.date: 2026-11-23
---

* [ ] Phase 1: `live_receiver.main` prints `error_type=<class>` to stderr before `Cannot run: RECEIVER_FAILED`.
* [ ] Phase 2: regression test in `src/api/tests/test_live_control.py` (class shown, message hidden, exit 4).
* [ ] Phase 3: live read-only job status evidence, mypy, ruff, targeted tests; changes record with criterion table.

Full tier (src change); no Azure change.

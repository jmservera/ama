---
title: Issue 2257 live details
ms.date: 2026-11-23
---

Phase 1: edit `map_sensors` in `src/core/src/zava_forward/core/assistants.py`; catch `Exception` around the `with self.transaction()` block only; re-raise nothing; use module logger if present.
Phase 2: monkeypatch `transaction` to raise in the test.

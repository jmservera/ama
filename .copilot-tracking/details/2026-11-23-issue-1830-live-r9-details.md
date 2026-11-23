---
title: Issue 1830 live r9 details (2026-11-23)
ms.date: 2026-11-23
---

Phase 1: edit `analyse` in `tools/rpi-gate-timing.py`: parse lock line via `ValueError`-safe helper, add `queue_wait_unavailable` reason, refuse negative wait.

Phase 2: add two tests in `tools/test_rpi_gate_timing.py` (no lock line gives null plus reason; malformed or negative refused).

Phase 3: run `python3 -m unittest tools.test_rpi_gate_timing tools.test_rpi_preflight -q`, ruff check and format, update note and changes record.

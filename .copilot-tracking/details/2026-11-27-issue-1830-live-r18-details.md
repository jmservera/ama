---
title: Issue 1830 live r18 details (2026-11-27)
ms.date: 2026-11-27
---

* Phase 1: edit the `earlier` comprehension in `critical_chain`.
* Phase 2: test `test_coincident_zero_length_commands_do_not_hang_the_chain` using `subprocess.run(..., timeout=30)` on the report command, asserting exit 0 and `chain_seconds` equal to the span.
* Phase 3: `python3 -m unittest tools/test_rpi_gate_timing.py`, `ruff check` and `ruff format --isolated --line-length 100 --check`.

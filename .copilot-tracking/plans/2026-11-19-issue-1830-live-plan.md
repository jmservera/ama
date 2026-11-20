---
title: Issue 1830 plan, repeated-command report
---

* [ ] Add `repeated_commands` (identical normalized argv run more than once, with count and seconds, setup flagged) to `analyse` in tools/rpi-gate-timing.py. Read-only; no gate semantics change.
* [ ] Add one unit test in tools/test_rpi_gate_timing.py.
* [ ] Run unittest, ruff check and format, record per-criterion table.

Critique (single pass, direct disposition): identical commands are candidates only, not proof of redundancy, so the output carries that wording and mandatory groups are never removed. Accepted; wording included in the field note.

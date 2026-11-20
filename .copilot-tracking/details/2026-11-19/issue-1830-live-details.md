---
title: Issue 1830 live details (2026-11-19)
ms.date: 2026-11-19
---

* Phase 2: in `analyse`, wrap `log.read_text()` in `try/except OSError` and raise `TimingError(EXIT_INPUT, ...)`; also guard an empty log (no first line).
* Test: `report --log` with a missing file returns exit 2 and a `REFUSED` message, and an empty log returns exit 2.
* Validation (focused): `python3 -m unittest tools.test_rpi_gate_timing -q`, ruff check and `ruff format --isolated --line-length 100 --check` on the two files. No `src/` change, so no mypy per project and no full tier.

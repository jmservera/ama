---
title: Issue 572 final handoff research
ms.date: 2026-11-02
---

Research executed (reuse plus fresh verification) at head fb6cdcd64 (equal to origin/main).

* Criteria 1 to 3 are on main: `EXPECTED_SKIP_REASONS` keeps the single exact discovery skip `CHAT_PANEL_DISCOVERY_SKIP`, the browser group runs `CHAT_PANEL_BROWSER_SELECTOR` with `ZF_BROWSER_TESTS=1`, and `tools/test_rpi_checks.py` covers execution and unexpected-skip failure.
* The prior blockers (core mypy arg-type, case-journey AI tab wait) were fixed by #757.
* Criterion 4 (fresh complete exact-head gate with browser and MSSQL groups) is not proven: the coordinator queues the complete gate; this task does not run `tools/rpi-checks.py`.

Planning readiness: Ready (evidence and handoff only, no source change).

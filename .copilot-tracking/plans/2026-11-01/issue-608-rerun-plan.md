---
title: Issue 608 rerun plan
ms.date: 2026-11-01
---

* [x] Confirm the fix exists on main and no source change is needed.
* [x] Re-run focused tier: `python3 -m unittest tools.test_rpi_checks`, ruff and mypy on the gate files.
* [x] Record evidence and open a PR with `Refs #608` only.
* Critique: executed once, verdict compatible; no change to scope. Out of scope: `tools/rpi-checks.py --all`, source edits.

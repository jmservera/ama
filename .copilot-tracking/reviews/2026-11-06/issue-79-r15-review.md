---
title: Issue 79 author review, continuation r15
ms.date: 2026-11-06
---

Author-only Review (not independent), written after the checks in the Changes record. Execution: Complete. Outcome: Residual work.

Compared: plan, details, Changes, research, independent d654 findings (preserved unchanged).

## Findings

* RV-001 (Low, resolved): finding HIGH 1 addressed by unique temp, fsync, `os.link`, directory fsync; real-`os.link` race tests and a four-process test pass.
* RV-002 (Low, resolved): HIGH 2 addressed; damaged, truncated and different-content records are refused and unchanged; API does not audit them as already published.
* RV-003 (Low, resolved): MEDIUM items (unsigned audit and response, run key documentation, status `OSError`) addressed.
* RV-004 (Low, residual): archived files are now created `0600` through `mkstemp`; confirm against deployment file-permission needs. Route: distinct follow-up.
* RV-005 (Medium, residual): the store's separate ranking-snapshot cache write still uses a fixed `.tmp` and `os.replace`; outside the reviewed finding. Route: later `rpi-plan`.
* RV-006 (Medium, residual): no fresh FULL, independent re-review, hosted CI, policy signoff or Legal retention for the corrected head; #1231 needs a rebase. Route: coordinator.
* RV-007 (Info): two existing assertions were changed deliberately (edited-record behavior, no-delete guard allowing one own-temp `os.unlink(tmp)`).

Validation: focused tests, Ruff, format, mypy with pinned tools, all green; no heavy checks run.

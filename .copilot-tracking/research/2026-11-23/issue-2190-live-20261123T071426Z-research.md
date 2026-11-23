---
title: "Issue 2190 live research r2: verify merged flake fixes"
description: Verification of what merged for the three gate flakes at HEAD 5c08bedd8f and what remains.
ms.date: 2026-11-23
---

Disposition: Research `executed` (verification only). Planning Readiness: Ready.

* Merged on main: #2272 (gate speed and stability), regression tests for flakes 2 and 3 with a stricter `_region_passed` (9112d17d63, 13fad60f2c), late_success settle ordering pinned (079353f902, 1aaad0fada).
* Code present: `_classes_executed` and `_region_passed` in `tools/rpi-checks.py`; `late_success` and `settle_route` in `src/api/checks/employee_chat_browser_check.py`.
* Baseline at HEAD: `tools.test_rpi_checks` 129 OK; `src/api` settle and 218 tests 7 OK.
* Remainder: no unmet source work for #2190. Flake 2 cannot be reproduced deterministically (client-side gap); ordering is pinned by tests. Azure is not involved.

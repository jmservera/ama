---
title: Issue 470 core suite timeout plan
ms.date: 2026-11-17
---

* [x] Add `suite_timeout(project)` (core 3600 s, others 1800 s) in `tools/rpi-checks.py`; use it at the planned contract and both runner sites.
* [x] Add a regression test in `tools/test_rpi_checks.py` asserting planned core suite timeout 3600 and api 1800, and that the runner uses the same value.
* [x] Add a README note in `src/README.md` near the gate guide.
* Tier: FULL (gate tool); only targeted tests run here; coordinator runs the full gate.
* Critique: executed once, see `.copilot-tracking/details/2026-11-17-issue-470-core-timeout-details.md`; verdict: proceed, no fail-closed change.

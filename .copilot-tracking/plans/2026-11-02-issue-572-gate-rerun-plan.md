---
title: Issue 572 complete gate rerun plan
ms.date: 2026-11-02
---

No change to `tools/rpi-checks.py` or tests: criteria 1 to 3 hold and a skip-allowlist change is excluded by criterion 2. Plan: run focused regression (`python3 tools/test_rpi_checks.py`), record the complete-gate probe evidence, open a PR with Refs only. The two unrelated blockers (core mypy, case-journey tab wait) are out of scope for #572 and need separate issues. Critique executed once: verdict accept.

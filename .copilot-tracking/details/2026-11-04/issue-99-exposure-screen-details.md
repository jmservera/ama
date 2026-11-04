---
title: Phase details for #99 Finance queue exposure screen
ms.date: 2026-11-04
---

* Phase 1: `src/api/src/zava_forward/api/web/panels.js`. A failed or missing fetch shows a manual-check message (AI-free, no pause is cleared). Signal, status, reason, findings, action and notice use plain language, `role="status"`, headings and a list; no colour-only status. No button approves, resumes or accelerates.
* Phase 2: `src/api/tests/test_finance_exposure_screen.py` runs the shipped `panels.js` in node. Success: three tests pass, ruff and mypy (tests included) clean.

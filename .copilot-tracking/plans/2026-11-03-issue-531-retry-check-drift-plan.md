---
title: Issue 531 retry-check drift plan
ms.date: 2026-11-03
---

* Slice: update the loading browser check and the README so they describe and test the current three-retry script budget. No product code change.
* Critique: executed once inline against the plan. Verdict: compatible. The check change mirrors `SCRIPT_RETRY_DELAYS`; the optional-enhancement path (`/case-workspace.js`, one request) and the missing-global, unready-helper and unready-method paths (two requests, no retry) are unchanged. No conflict with confirmed decisions.
* Phases:
  * Phase 1: edit `src/api/checks/loading_briefing_browser_check.py` (details file).
  * Phase 2: edit the README retry paragraph.
  * Phase 3: run focused tests, browser and axe checks, ruff and mypy; write changes, review, state and log records.
* Out of scope: live Azure verification, screen-reader and voice-control acceptance, the gate, benchmarks and full suites.

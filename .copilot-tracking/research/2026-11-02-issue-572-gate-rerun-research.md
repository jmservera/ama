---
title: Issue 572 complete gate rerun research
ms.date: 2026-11-02
---

Research executed. Criteria 1 to 3 are already on main (PRs #575, #595, #600, #606, #627, #719; see the 2026-11-01 research). New evidence: a complete gate run at main 071e132a8 (base 071e132a8, external output /tmp/ama-gate-572/probe2, failed receipt) showed the chat-panel case skipped with `opt-in local Chromium` in project-api (accepted as the single exact discovery skip) and executed in the browser group (`0138-browser.log`: Ran 1 test, OK). The project-api group passed. The gate still fails for two unrelated inherited reasons: project-core mypy `arg-type` at `src/core/tests/test_chat_case_answers.py:64` (introduced by #752), and the browser group `case_journey_browser_check.py` timing out waiting for tab "AI assistance (loading)" (line 1608). MSSQL was blocked by those. Also observed: a tracked `tools/__pycache__/rpi-checks.cpython-312.pyc` is rewritten by running the gate without `PYTHONDONTWRITEBYTECODE=1`, making the tree dirty. Planning readiness: Ready (no source change in scope).

---
title: Issue 2303 details, revision 0000072 (2026-11-25)
---

Probe: `probe_ai_report.py live-r0000072` (Playwright, desktop 1440x900). Test: `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests.test_cutover_audit -q`. Mutation: remove `COPY agents/evals/chat_golden.json` from `src/api/Dockerfile`, expect one failure, restore.

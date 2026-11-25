---
title: Issue 2303 plan details, revision 0000069 (2026-11-25)
---

Probe: `docs/reference/research/issue-2303-live-2026-11-25/probe_ai_report.py live-r0000069`. Mutation: delete the `COPY agents/evals/chat_golden.json` line, run `PYTHONPATH=src:tests python3 -m unittest tests.test_cutover_audit -q` in `src/core`, restore with `git checkout`. Tier: focused (documentation and evidence only; no `src` change).

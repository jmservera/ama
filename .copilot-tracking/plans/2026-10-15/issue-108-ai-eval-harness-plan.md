---
title: Issue 108 AI evaluation harness plan
ms.date: 2026-10-15
---

* Add `evidence_gate` to `ai_eval.py` and an `evidence` report block; run passes only with zero critical misses.
* Print the block in the CLI; document in `mvp/README.md`; log in `docs/reference/log.md`.
* Tests: evidence block content, critical miss fails the run.
* Critique (single pass): keep the change small; do not invent thresholds, quotas or live results. Accepted.

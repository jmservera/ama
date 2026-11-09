---
title: Issue 79 plan, continuation r10
ms.date: 2026-11-06
---

* [ ] Phase 1: commit this research, plan and details first.
* [ ] Phase 2: add regression tests for the four findings to `test_ranking_publication_runner.py` only; run them once and keep the raw RED output in a fresh path under `/tmp/79-functional-r10-1106/`.
* [ ] Phase 3: smallest corrections in `ranking_publication_runner.py` and the README runner paragraph; run the combined selector, Ruff, format and mypy once, each to a new log path.
* [ ] Phase 4: write Changes and state, validate JSON, links and diff, then create the dedicated author-only Review and commit once.

Details: [details](../../details/2026-11-06/issue-79-r10-details.md). Research: [research](../../research/2026-11-06/issue-79-r10-research.md).

Critique (single pass, self-run, before any test or source edit): the fixes reuse existing refusals, statuses and exit mapping, and each is a few lines. Risks found and applied directly: F4 must not change verify results for a valid latest, and F3 must still require capacity for a new record. Nothing is significant or divergent. Tier: FULL for the whole feature; this continuation is light and the r9 FULL is historical for the new head.

---
title: Issue 100 live research
ms.date: 2026-11-19
---

# Issue 100 research (opened 2026-11-19)

Task: `issue-100-live`. Branch `test/code-live-20261119T0143Z`. Mode: demo, desktop only.

## Opening findings

* Issue #100 has two unticked criteria: the #440 stabilization checkpoint and the tokenomics management-view criterion.
* The tokenomics data layer is on main: `tokenomics.summarize_ai_consumption_economics`, `insights.stats(... ai_consumption_economics)`, `/api/stats`, `/api/progress`, `/api/coordinator`, `/api/ai/report`. Existing tests `src/core/tests/test_management_tokenomics_invariant_100.py` and `src/api/tests/test_management_tokenomics_api_100.py` pass locally (6 and 2 tests).
* `management_insight.py` and `/api/management/tokenomics`, named in an earlier issue comment, are not on main (they lived in an unmerged stacked PR).
* The desktop Overview (`overviewView` in `src/api/src/zava_forward/api/web/app.js`) never reads `ai_consumption_economics` from `/api/stats`, so the management view does not show AI consumption economics to a person. Candidate first unmet criterion: the tokenomics view in the UI.
* The #440 stabilization criterion depends on #440's own unticked triage and artifact criteria; it is a process checkpoint, not code.

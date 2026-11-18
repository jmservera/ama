# Research: per-skill tokenomics breakdown (Refs #108)

* Date: 2026-11-14; Branch: feat/demo-108-tokenomics-report-summary-0959 (parent f907cd2c7, PR #1641)
* Disposition: executed. Planning Readiness: Ready.
* Source: `gh issue view 108` (model selection/evaluation; benefit not claimed without calibrated results) and `src/core/src/zava_forward/core/ai_consumption.py`.
* Finding 1: `by_capability` (the per-skill export) gave only calls, proposals and total tokens; cached, uncached and reasoning tokens were not split.
* Finding 2: `usage()` kept `cached_tokens` but dropped `reasoning_tokens`; price events carry a `synthetic` flag that the per-skill export did not surface.
* Constraint: `ai_eval.py` is not edited (sibling #108 branch).
* Constraint: absent usage fields must stay `Unknown`, never zero.

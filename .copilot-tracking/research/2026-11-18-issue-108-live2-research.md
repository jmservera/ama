---
title: Issue 108 live round 2 research (opening)
description: Opening research record for the second demo-scope audit of the AI evaluation harness and model selection
ms.date: 2026-11-18
---

Task: issue-108-live2 (Refs #108). Disposition: executed. Prior work reused: `docs/reference/research/issue-108-live-demo-evidence-2026-11-18.md` on main and worktree `issue-108-20261117T2307`. State file `issue-108-live-state.json` is tracked and left untouched; this round keeps `issue-108-live2-state.json`.

Open questions: (1) re-run the offline harness and confirm the critical-miss, model/prompt/latency/reviewer reporting criteria; (2) confirm model names, versions and regional quota with a route that returns data (prior round: usages route empty); (3) any gap the prior note left (landing screenshot was signed out).

## Findings

* Harness offline tests: 116 tests OK (`unittest_harness.txt`) across `test_ai_eval`, `test_candidate_comparison`, `test_heldout_batch`, `test_heldout_freeze`, `test_heldout_aoai`, `test_eval_registry`; includes `test_a_critical_miss_fails_the_run`, `test_five_output_scenario_retains_each_returned_identity_and_latency`, `test_cheaper_with_more_critical_misses_is_a_failure`, `test_refusal_and_latency_reported`.
* Azure (rg `ama`, existing login, read-only): `aoai-resident-469` swedencentral `resident-mini` gpt-4.1-mini 2025-04-14 Standard cap 1 (1 req, 1000 tokens per rate limit unit); `aif-cutover-test-rzsrg` uksouth `standard` gpt-4.1-nano 2025-04-14 GlobalStandard cap 10 (10 req, 10000 tokens).
* Catalogue in both regions lists both models as Legacy, retirement 2027-04-14 (older SKU lines) or 2028-04-13.
* `az cognitiveservices usage list` and the REST usages route return zero entries in uksouth and swedencentral: subscription quota headroom cannot be shown by this route.
* Planning Readiness: Ready. Existing prior note covers criteria 2-8; this round adds the quota route recheck and the harness rerun.

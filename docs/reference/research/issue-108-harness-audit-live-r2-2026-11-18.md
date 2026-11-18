---
title: AI evaluation harness audit, live round 2 (Refs #108)
description: Harness rerun and regional model and quota recheck for issue 108, with a per-criterion proven or unproven table for the demo
ms.date: 2026-11-18
---

Refs #108. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive billing reconciliation, DPO and Legal approval and person-run assistive technology testing. This round extends [issue-108-live-demo-evidence-2026-11-18.md](./issue-108-live-demo-evidence-2026-11-18.md) and reuses [ai-heldout-batch-432-live-2026-11-18.md](./ai-heldout-batch-432-live-2026-11-18.md); it does not repeat the 12-call batch. No source, SQL or infrastructure change; no Azure resource was created.

## What was run

* Harness on `main` (commit `d62e17627`), from `src/agents`: `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests.test_ai_eval tests.test_candidate_comparison tests.test_heldout_batch tests.test_heldout_freeze tests.test_heldout_aoai tests.test_eval_registry -v`. Result: 116 tests, OK. Raw output: [unittest_harness.txt](./issue-108-harness-audit-live-r2-2026-11-18/unittest_harness.txt).
* Azure CLI, existing login, read-only: `az cognitiveservices account deployment list` for both accounts, `az cognitiveservices usage list -l <region>`, the `Microsoft.CognitiveServices/locations/<region>/usages` REST route and `az cognitiveservices model list -l <region>`. Raw output: [azure_quota_outputs.txt](./issue-108-harness-audit-live-r2-2026-11-18/azure_quota_outputs.txt). A scan for GUIDs and e-mail addresses found none; no credential was read or printed.
* No browser proof: the harness has no web surface, and the signed-in demo routes were already captured in the prior note.

## Harness audit

* Critical misses fail the run: `test_a_critical_miss_fails_the_run` and `test_early_critical_miss_still_fails_after_valid_repetition` pass.
* Model, prompt version, latency and reviewer outcomes are retained per run: `test_five_output_scenario_retains_each_returned_identity_and_latency` and `test_refusal_and_latency_reported` pass.
* A cheaper candidate that raises critical misses is a failure: `test_cheaper_with_more_critical_misses_is_a_failure` passes.
* Freeze rules require expected outcome and critical errors: `test_expected_outcome_and_critical_errors_required` passes.

## Regional model, version and quota

| Account | Region | Deployment | Model and version | SKU, capacity | Rate limit units |
| --- | --- | --- | --- | --- | --- |
| `aoai-resident-469` | swedencentral | `resident-mini` | gpt-4.1-mini 2025-04-14 | Standard, 1 | 1 request, 1,000 tokens |
| `aif-cutover-test-rzsrg` | uksouth | `standard` | gpt-4.1-nano 2025-04-14 | GlobalStandard, 10 | 10 requests, 10,000 tokens |

Both deployments are `Succeeded`. The model catalogue in each region lists both models as `Legacy`, with retirement dates of 2027-04-14 or 2028-04-13 depending on the SKU line. `az cognitiveservices usage list` and the REST usages route returned zero entries in both regions, so subscription quota headroom is not shown by any route used here.

## Per-criterion result

| # | Criterion (issue 108) | Demo result | Evidence and limit |
| --- | --- | --- | --- |
| A1 | Critical misses fail the run (ticked) | Proven again | Tests above, 116 OK |
| A2 | Model, prompt version, latency and reviewer outcomes reported (ticked) | Proven again, offline and scripted only | Tests above; not actual-model effectiveness |
| A3 | Model names, versions and quotas confirmed in the chosen region | Partly proven | Names, versions, SKU, capacity and rate limits confirmed in uksouth and swedencentral. Subscription quota headroom unproven (usages route empty). The "chosen" production region stays with #1905-#1908. |
| A4 | Benefit not claimed without calibrated results (ticked) | Unchanged | No benefit claim made here |
| R1 | Freeze versions, independently labelled held-out split, thresholds | Partly proven (prior note) | Freeze tests pass; labeller independence and sample size unproven |
| R4 | Competent humans block every seeded critical proposal | Unproven | Needs people; role agents are not substitutes |
| R5 | Effort and cost against manual and rules alternatives; Finance validates | Unproven | No measured effort; cost Unknown without a validated price |
| R6 | Hashes, split, seed, denominators, serving version, usage, reviewer protocol | Partly proven (prior note) | No reviewer protocol or pass/fail outcome for the batch |
| R7 | Finite call authority, payload approval, serving attestation | Partly proven (prior note) | Finite authority exists for the batch; no payload approval or signed attestation |
| R9 | Real AI, SQL and Azure proof under CON-009 and AC-057 | Partly proven (prior note) | Real calls on Azure; AC-057 restart check not run (drill-like) |
| T3 | One routing or caching lever at a time against a recorded baseline | Mechanism proven offline; no live lever measured | `test_exactly_one_lever_and_same_cases` passes; no second live candidate run |

No criterion is newly tickable on #108. Criterion A3 is closest and needs a subscription quota figure that the available routes do not return.

## Limits

* Scripted and offline results are not actual-model or human effectiveness.
* Gpt-4.1 models are `Legacy`; a model refresh is a production decision.
* Focused tier; `rpi-checks.py --all` was not run.

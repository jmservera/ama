---
title: AI evaluation harness live demo evidence (Refs #108)
description: Per-criterion record of what the live demo proves for the unticked acceptance criteria of issue 108, with limits
ms.date: 2026-11-18
---

Refs #108. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive billing reconciliation, DPO and Legal approval and person-run assistive technology testing. Production-only criteria stay deferred (#1905-#1908). No source code changed and no Azure resource was created, changed or needs deleting.

## Method

* Azure CLI with the existing login, read-only: `az cognitiveservices account list`, `deployment list` and `deployment show`, `model list -l uksouth`, the subscription `usages` REST route, and `az containerapp show` for `ca-cutover-test-demo-api` (environment variable names and the non-secret model values only).
* Playwright Chromium, 1366 by 900, signed in with the employee demo account (role `Retrofit Programme Manager`). Driver `live_ai_probe.py` fetches seven GET routes with the app's own session and scrubs e-mail addresses. Credentials were read at run time, never printed; a literal scan of `live_ai_endpoints.json` found neither the user id nor the secret. Evidence folder: `.copilot-tracking/evidence/2026-11-18/issue-108-live/` (`live_ai_endpoints.json`, `live-landing-signed-in.png`, and `azure_cli_outputs.txt` with the sanitized Azure CLI outputs).
* Offline: `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests.test_heldout_batch tests.test_heldout_aoai tests.test_heldout_freeze tests.test_candidate_comparison tests.test_epic104_bounded_ai_invariants -q` from `src/agents`: 115 tests, OK.
* Reused, not repeated: the 12-call measured batch in [ai-heldout-batch-432-live-2026-11-18.md](./ai-heldout-batch-432-live-2026-11-18.md) and its inputs under [evaluation/heldout-batch-432-live-2026-11-18](./evaluation/heldout-batch-432-live-2026-11-18/).

## Observations

Model, version and quota (Azure, 2026-11-18):

| Resource | Region | Network | Deployment | Model and version | SKU, capacity | Rate limits per 60 s |
| --- | --- | --- | --- | --- | --- | --- |
| `aif-cutover-test-rzsrg` (AIServices) | uksouth | public access Disabled | `standard` | `gpt-4.1-nano` 2025-04-14, `NoAutoUpgrade` | GlobalStandard, 10 | 10 requests, 10,000 tokens |
| `aoai-resident-469` (OpenAI) | swedencentral | public access Enabled | `resident-mini` | `gpt-4.1-mini` 2025-04-14 | Standard, 1 | 1 request, 1,000 tokens |

* The model catalog for uksouth lists `gpt-4.1-nano` 2025-04-14 as `Legacy` with an inference retirement date of 2027-04-14, with GlobalStandard, DeveloperTier, GlobalProvisionedManaged and GlobalBatch SKUs.
* The demo API configuration names the same deployment and version: `AI_DEPLOYMENT` and `AI_DEPLOYMENT_STRONG` are `standard`; `AI_MODEL_VERSION` and `AI_MODEL_VERSION_STRONG` are `gpt-4.1-nano-2025-04-14`; `ZF_STORE` is `mssql` with `ZF_SQL_AUTH` `msi`.
* Subscription-level quota: `az cognitiveservices usage list` and the `usages` REST route returned an empty list for uksouth and swedencentral. The subscription quota number is therefore not confirmed; only deployment capacity and per-deployment rate limits are.

Live app (signed in, `/api/ai/report`, 2026-11-18T08:52Z):

* Prompt version `2026-10-09.1`; registry version `2026-10-15.1`, hash `d25f859c...fd4d3d`.
* Task runs: briefing 137 (0 AI, 137 workflow), message 6, summary 10, funding draft 1; all workflow or template. Fallback reasons: "AI is not configured" 14, workflow-only mode 8, "Release admission denied: no approved release matches" 132 (owner "RAI task owner not appointed (OQ-017)").
* Consumption block (schema `ai-consumption-v1`, label `synthetic`): 2 recorded calls in `chat-case-conversation`, 1,226 and 1,230 tokens, 0 failures, 0 unknown liabilities; `token_cost` Unknown, `cost_per_accepted_proposal` Unknown, `spend_authority` null, `reconciliation` `unreconciled`; label "recorded usage; not an authorised held-out batch".
* Evaluation block: 11 scenarios, `passed` true, critical misses 0 in the 10 scenarios that report the measure (the eleventh reports none); per-run source, model, prompt version and latency fields are present. `/api/ai/priority` returned `recommendation: null`.
* `/api/ai/heldout-evaluation`, `/api/ai/cohort-evaluation` and `/api/ai/candidate-comparison` returned 403 "Your role does not include this." for the Programme Manager account; no account with the permitted role was available, so those routes were not exercised live.

Held-out batch inputs (sha256): `manifest.json` 5d5007f533c383837f13d189ae6e45dec52850f27cc63cc7757d1b5538649daf; `authorization.json` 5f7eedbdf85b7ed018915d6317d447bc967500f09446e97eab88e735003b0ffa; `proposals.json` 24655be67e7c6cf2cbdb6660c9dc00c476f0d68b4352c9dc281259e69259c76b; `report-live.json` e5867c3affb9b910390bbac5ef3a1b987e328b13f232ce2486ca6c317c93c131. The manifest records seed `demo-seed-432`, denominator 12, empty `prompt_case_ids` and `tuning_case_ids`, thresholds (0 critical misses, accuracy 0.9, 2 per cohort) and versions for task, model, prompt, policy and source.

## Per-criterion result

| # | Criterion (issue 108, unticked) | Demo result | Evidence and limit |
| --- | --- | --- | --- |
| 1 | Model names, versions and quotas confirmed in the chosen region | Proven for the demo deployments; subscription quota unproven | Table above: names, versions, capacity and rate limits confirmed in uksouth and swedencentral. The usages route returned nothing, so the regional subscription quota is not confirmed. The model is `Legacy` (retires 2027-04-14); a production region and model choice stays with #1905-#1908. |
| 2 | Freeze versions, independently labelled held-out split, expected outcomes, critical errors, cohorts, sufficient samples, approved thresholds; answers never in prompts | Partly proven; independence unproven | Frozen manifest with versions, seed, 12 ids, expected outcomes, critical error, thresholds, empty prompt and tuning id lists; freeze tests pass (115 OK). The labeller and prompt author are demo roles, not independent people, and 12 cases are too few for per-cohort claims. |
| 3 | Authorised competent humans detect and block every seeded critical proposal | Unproven for human evidence | Needs people; participant substitution is excluded by the issue. Offline panel evidence is in [human-review-effectiveness-live-demo-2026-11-18.md](./human-review-effectiveness-live-demo-2026-11-18.md). |
| 4 | Compare full effort and cost with manual/template and parser/rules alternatives; Finance validates | Unproven | The live report shows `token_cost` Unknown and every other cost component Unknown; no measured effort exists, and Finance validation is a person decision. Only a token and list-price figure exists for the batch. |
| 5 | Record hashes, split/seed, denominators, actual serving version, usage, unknown liabilities, reviewer protocol, outcomes; retain negative results | Partly proven | Hashes, seed `demo-seed-432`, denominator 12, serving model `gpt-4.1-nano` 2025-04-14, usage (2,522 tokens), empty `problems` list (the report has no separate unknown-liability field), and the preserved stopped first attempt (`report-live-attempt1-stopped.json`) are recorded. No reviewer protocol or pass/fail/insufficient outcome exists because the batch measured consumption only. |
| 6 | Actual calls need finite call/token/budget/expiry authorisation, approved payload handling, serving attestation, plus human participation consent | Partly proven: finite authority recorded for the batch; payload approval and serving attestation unresolved; human consent not applicable | `authorization.json` (owner, 12 calls, 24,000 tokens, USD 0.50, expiry 2026-11-19T00:00:00Z). The authority covers 12 calls and the completed run made 12 calls; the first attempt (one call, `report-live-attempt1-stopped.json`) is a further call not reconciled to a renewed authority. No payload-handling approval and no signed serving attestation exist; the deployment record above is not one. Human participation consent is outside the demo. |
| 7 | Real AI/SQL/Azure proof under CON-009/AC-057 | Partly proven | Real model calls on Azure: 12 measured batch calls; the app's consumption record shows 2 `chat-case-conversation` usage entries whose provider and serving provenance this probe did not verify; the app runs on `ZF_STORE=mssql` with managed identity SQL. Not proven: the AC-057 independent before/after SQL checks across an app restart (a restart is a drill-like change and no SQL query path was used), and a registered generative task with citations and "Not reviewed" authority (0 AI-sourced outputs; release admission is denied for 132 runs). Successful inference is not accuracy, fairness or net benefit. |
| 8 | One routing or caching lever at a time, same held-out cases, recorded baseline | Mechanism proven offline, with exceptions; no live lever measured | `candidate_comparison.py` accepts one lever from `model`, `routing`, `caching`, `prompt`, requires the same case ids and a valid baseline; it also permits several levers when the candidate is flagged composite, and a frozen held-out basis is optional in the code, so the one-lever rule is enforced for the default path only (tests `test_exactly_one_lever_and_same_cases`, `test_invalid_baseline_blocks_every_candidate` pass). The batch recorded cached tokens 0 on all 12 calls, so caching was not exercised; no second candidate was run. |

No criterion is newly tickable on #108 from this change. Criteria 1 and 6 are closest; criterion 1 needs the subscription quota figure.

## Adverse and incidental observations

* The subscription usages route returning empty is a gap, not a pass.
* Three comparison routes are role-gated and could not be read with the available accounts.
* The 14 `AI is not configured` fallbacks are historic runs, shown because the report keeps them.
* The first live batch attempt stopped on a network block; the preserved report is cited above.

## Resources and residue

No Azure resource or role assignment was created. The probe read only; the app store is unchanged apart from read access. Focused tier; no `rpi-checks.py --all`.

## Evidence limits

* `live-landing-signed-in.png` shows the signed-out landing page, not a signed-in view.
* The network states and the empty subscription quota result were observed live and are not retained in `azure_cli_outputs.txt`.
* The large JSON file is a dump of seven live demo responses; the note's claims rest on it only where cited.
* No criterion is newly proven by this record.

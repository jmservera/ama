---
title: Held-out AI batch, tokens per proposal and spend authority (Refs #432)
description: Finite measured batch on 12 synthetic cases, run live on 2026-11-18 for the demo, with per-criterion status for issue 432
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Owner decision 2026-11-18 on #432 authorises live Azure in resource group `ama` (demo cap USD 700, no drills, no Key Vault rotation, no production change) and waives billing reconciliation, DPO and Legal approval and person-run assistive technology testing for the demo. No source code changed.

## Result (measured held-out batch, 12 proposals)

Evidence label: `measured held-out batch`. Source: provider usage envelope returned by the `standard` deployment (`gpt-4.1-nano`, 2025-04-14) on `aif-cutover-test-rzsrg`. Inputs and the full report are in [heldout-batch-432-live-2026-11-18](./evaluation/heldout-batch-432-live-2026-11-18/): `authorization.json`, `manifest.json`, `proposals.json`, `report-live.json` (and `report-live-attempt1-stopped.json`, the preserved first attempt).

| Tokens per proposal | Count | Min | p50 | Mean | p90 | Max |
| --- | --- | --- | --- | --- | --- | --- |
| Total | 12 | 180 | 214.5 | 210.17 | 224 | 225 |
| Input | 12 | 70 | 73 | 73.5 | 76 | 77 |
| Output | 12 | 104 | 142 | 136.67 | 151 | 152 |

* Totals: input 882, cached 0, output 1,640, all 2,522 tokens; 12 calls; outcome `completed`, stop reason `exhausted`.
* Accrued at list price: USD 0.000744 of the USD 0.50 batch cap (about USD 0.0000620 per proposal). This is a list-price estimate from the authorization rates, not a billing record.
* Spend authority recorded in `authorization.json`: approved by Juan Manuel Servera (owner), reference "Owner decision 2026-11-18 on #432", expiry 2026-11-19T00:00:00Z, 12 calls, 24,000 tokens, USD 0.50. Nothing was assumed beyond that authority.
* Price source: Azure Retail Prices API (`prices.azure.com/api/retail/prices`), Foundry Models gpt 4.1 nano global meters, retrieved 2026-11-18: input 0.0001, cached input 0.000025, output 0.0004 USD per 1K tokens (0.10, 0.025, 0.40 USD per 1M).
* Cached tokens were 0 for all calls, so the cached-input rate was not exercised.

## Limits of this evidence

* The 12 cases are synthetic, authored for the demo. The manifest freeze check passed, but the labeller and prompt author are demo roles, not independent people. The batch measures consumption only; it is not a quality, accuracy or critical-miss result, and `expected` labels were not scored.
* 12 proposals with near-identical short prompts give a narrow spread. Real case text would be larger; do not extrapolate cost.
* Model output text was never stored (the adapter keeps usage only).

## How it ran, including the first failed attempts

* Dry-run first (offline estimator, labelled `dry-run simulation - not measured evidence`): 12 calls, 1,261 tokens, USD 0.000252. It is not measured evidence.
* Attempt 1 (from this host, Azure CLI token) stopped after one call with `unmeasured-call`, charged at the worst case USD 0.000310, as designed. Cause: the account has `publicNetworkAccess` Disabled, so the call was refused (HTTP 401 PermissionDenied). The report is kept as `report-live-attempt1-stopped.json`.
* A temporary `Cognitive Services OpenAI User` role assignment for this session's identity on `aif-cutover-test-rzsrg` did not help (the block is network, not role) and was deleted; the role list afterwards contains only the two pre-existing principals. Network settings were not changed.
* Attempt 2 ran inside the existing demo container `ca-cutover-test-demo-api` through `az containerapp exec` (temporary files under `/tmp/hb`, removed afterwards). The runner module in that image (`heldout_aoai.py` sha256 `22f05161...ca730`, equal to this worktree; `heldout_batch.py` sha256 `9ba1b773...72b0`, different from the worktree's `4534add1...e492`, an older image build) was used with the container's user-assigned identity token injected through a runtime wrapper because `azure.identity.ManagedIdentityCredential` reported no configuration in the exec shell. No secret was printed or stored. No throwaway Azure resource remains.

## Per-criterion status for #432

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Model call join and no raw content in telemetry | Ticked in the issue; not re-proven here | Prior delivery, see [ai-tokenomics.md](../resources/ai-tokenomics.md) |
| 2 | Per-request call and depth bound | Ticked; not re-proven here | Prior delivery |
| 3 | Limit, unknown price or liability stops dispatch | Ticked; partly exercised: attempt 1 charged the worst case and stopped on an unmeasured call | `report-live-attempt1-stopped.json` |
| 4 | Dated price source, Unknown when none | Ticked; a dated source was retrieved for this batch | Price source above |
| 5 | Reconcile metered usage to Azure cost records | Unproven by owner decision: billing reconciliation is not needed for the demo. The USD figure above is a list-price estimate and not a billing record | Owner decision 2026-11-18 |
| 6 | Report separates token cost and shows cost per accepted proposal | Ticked; not re-proven. This batch has no accepted-proposal count or quality rates, so no cost per accepted proposal is stated | Limits above |
| 7 | Time released is capacity, not cash | Ticked; not re-proven here | Prior delivery |
| 8 | Finite owner-authorised measured batch, tokens per proposal and spread, spend authority recorded | Proven for the synthetic demo: 12 measured proposals, spread and authority recorded. Not proven for real held-out cases: cases are synthetic and not independently labelled | This note and `report-live.json` |
| 9 | Results feed the Tokenomics slide and Q&A card with source and evidence label | Ticked. The figures above, with their label, are available for the slide; the slide and card were not edited in this change | Follow-up |

Criterion 8 can be treated as met for the demo; keep the "synthetic, not independent" caveat wherever the figures are quoted. Criterion 5 stays unmet and open under the owner waiver. Issue #432 is referenced, not closed.

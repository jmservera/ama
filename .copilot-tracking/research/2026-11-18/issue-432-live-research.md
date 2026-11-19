# Issue 432 live research (opened 2026-11-18)

Goal: prove the unticked criteria of #432 for the synthetic demo.

* Unticked: billing reconciliation (owner: not needed for demo); finite measured held-out batch with tokens per proposal, spread and recorded spend authority.
* Tooling found: src/agents heldout_batch.py, heldout_aoai.py, heldout_freeze.py (hard cap USD 5, max 50 calls).

## Findings

* Issue #432 ticks 7 of 9 criteria. Unticked: AC5 billing reconciliation (owner 2026-11-18: not needed for the demo, so recorded as not proven) and AC8 finite measured held-out batch with spend authority.
* AC8 tooling exists and is unrun live: `python -m zava_forward.agents.heldout_batch --execute-live` (src/agents/README.md "Held-out token measurement"). It needs a frozen manifest (check_freeze), an authorization file (named human approver, max USD 5.00, dated per-1M rates, endpoint and deployment) and a proposals file. No source change is required.
* Azure: rg ama has `aif-cutover-test-rzsrg` (uksouth), deployment `standard` = gpt-4.1-nano 2025-04-14, and `aoai-resident-469` deployment `resident-mini` = gpt-4.1-mini. Use the nano deployment: cheapest, already named in the README example.
* Price source: Azure Retail Prices API (prices.azure.com), retrieved 2026-11-18, Foundry Models gpt-4.1-nano global: input 0.0001 USD/1K, cached input 0.000025 USD/1K, output 0.0004 USD/1K (effective 2025-04-01 to 2025-05-01 meters), so 0.10 / 0.025 / 0.40 USD per 1M.
* Held-out cases: no real independently labelled set exists; the batch uses synthetic demo cases, labelled as such. Tokens per proposal measure consumption, not quality.
* Planning readiness: Ready. Validation tier FOCUSED (no src change; docs and evidence only).

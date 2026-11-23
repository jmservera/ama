---
title: Issue 2302 AI consumption economics in the management view (Refs #100)
description: Per-criterion proven or unproven record for issue 2302, with a signed-in desktop observation of the Overview AI economics card on revision 0000055 and the focused tests that prove Unknown, not zero
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `f87d86da00`. Refs #2302 and #100. Owner decision 2026-11-18 authorises live Azure in resource group `ama` and waives billing reconciliation, DPO and Legal approval and person-run assistive technology testing. The probe is read-only: no Azure resource was created or changed, so nothing needed deletion. Sign-in values were read at runtime by the probe and never printed; the stored JSON was checked for their absence. Tier: focused (documentation and evidence only, no `src` change).

## Finding

No defect and no source gap. The Overview card, the server summary and the tests already on main cover the criterion; what was missing was current evidence tying them together at the present head and deployed revision. This note supersedes nothing: it extends [the 2026-11-19 note](./management-tokenomics-overview-100-live-2026-11-19.md) and [the 2026-11-21 re-check](./issue-100-live-criteria-recheck-2026-11-21.md) to revision `ca-cutover-test-demo-api--0000055`.

## Where the management view renders it

* Code: `aiEconomicsRows` and `aiEconomicsCard` in `src/api/src/zava_forward/api/web/app.js`, mounted on the Overview from `/api/stats` (`st.ai_consumption_economics`). The server summary is `summarize_ai_consumption_economics` in `src/core/src/zava_forward/core/tokenomics.py`. No cost is computed in the browser.
* Live (revision 0000055, signed-in employee, 1366x900): [overview-ai-economics.png](./issue-2302-ai-economics-live-2026-11-23/overview-ai-economics.png), payload and card text in [live_probe.json](./issue-2302-ai-economics-live-2026-11-23/live_probe.json), script [live_probe.py](./issue-2302-ai-economics-live-2026-11-23/live_probe.py). `/api/me`, `/api/stats` and `/api/progress` all answered 200.
* Denominators shown: AI proposals 1, accepted outcomes 0, metered calls 24, unmetered calls 0, unreviewed proposals 1, rejected or withdrawn 0 (the payload also carries 1622 workflow-only calls excluded from the outcome count).
* Cost rows shown as the word Unknown: token cost, total cost of AI, token cost per accepted outcome, cost per accepted outcome, quality-qualified cost per accepted outcome, booked value. Price source reads Unknown (OD-51 open). The card states "Unknown means no price source or no accepted outcome exists to divide by; it is not zero."

## Unknown, not zero: tests

Run sequentially at head `f87d86da00`, both OK:

* `src/core`: `test_management_tokenomics_invariant_100` and `test_tokenomics_comparison`, 22 tests ([core-tests.txt](./issue-2302-ai-economics-live-2026-11-23/core-tests.txt)). `test_empty_json_store_reports_explicit_zero_denominators_and_unknown_costs` and `test_unpriced_store_with_accepted_and_unreviewed_proposals_keeps_costs_unknown` cover no price source; `test_priced_sql_ledger_with_zero_accepted_outcomes_reports_unknown_per_outcome` covers a price source with no accepted outcome; `test_invariant_validator_rejects_numeric_zero_costs_and_direct_helpers_remain_pure` rejects numeric zero.
* `src/api`: `test_overview_ai_economics_100` (node-backed card formatting, including missing summary and numeric zero cost) and `test_management_tokenomics_api_100` (HTTP, unpriced and priced), 5 tests ([api-tests.txt](./issue-2302-ai-economics-live-2026-11-23/api-tests.txt)).

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Show where the management view renders AI economics, with denominators, in the demo workbench | Proven (deployed demo observed) | Section above: code location, live screenshot and payload on revision 0000055 |
| 2 | A test proves Unknown (not zero) when no price source or accepted-outcome count exists | Proven (local tests) | Core and API tests above, all passing; live payload shows the same Unknown values |
| 3 | Tick the criterion on #100 with the evidence path | Unproven by this worker | Ticking edits the issue on a shared system and the worker is not to push or update remote state. Evidence path for the owner: `docs/reference/research/issue-2302-ai-economics-live-2026-11-23.md` |

## Limits

* The hosted observation is one store state at one time; price, budget and target stay unset (OD-51 open), so no priced figure is observed live. A priced rendering is proven only by the tests.
* #100 criterion on the #440 stabilization checkpoint is outside #2302 and stays open.
* No hosted CI, `rpi-checks.py` or SQL Server variants were run; one worker, one in-loop review, no independent reviewer or PR.

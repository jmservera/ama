---
title: Management Overview AI consumption economics (Refs #100)
description: Per-criterion proven or unproven record for the two unticked acceptance criteria of issue 100, with the Overview AI economics card added and proven locally on 2026-11-19
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only. Owner decision 2026-11-18 authorises live Azure in resource group `ama` (cap USD 700) and waives billing reconciliation, DPO and Legal approval and person-run assistive technology testing. No Azure resource was created or changed, so nothing needed deletion. No credential was read or printed.

## Finding

The data layer for AI consumption economics was already on main (`/api/stats`, `/api/progress`, `/api/coordinator`, `/api/ai/report`, with API and core tests). The desktop Overview, the management screen, never rendered `ai_consumption_economics`, so a person could not see it. The earlier comment naming `management_insight.py` and `/api/management/tokenomics` refers to an unmerged stacked PR; neither exists on main.

## Change

`src/api/src/zava_forward/api/web/app.js` adds `aiEconomicsRows` and `aiEconomicsCard`, and the Overview shows the card from `/api/stats`. Denominators (proposals, accepted outcomes, metered and unmetered calls, unreviewed, rejected or withdrawn) are real counts. Cost figures show Unknown when the server gives Unknown, null, empty or numeric zero, and a missing summary shows every figure Unknown with a status notice. No cost is computed in the browser.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | #440 stabilization checkpoint before epic closure | Unproven | #440 itself still has two unticked criteria (finding triage into issues, and genuine research, plan, changes and independent review artifacts). The 2026-11-15 checkpoint recorded in `docs/architecture/cutover-evidence-pack.md` was restored to unchecked on 2026-11-16 because it sat on an unmerged parent. Closing this needs owner approval and a checkpoint on current main, which a code change cannot supply. |
| 2 | Management views include AI consumption economics with explicit denominators, Unknown not zero | Proven for the synthetic demo, locally | Overview card; 3 new node-backed tests in `src/api/tests/test_overview_ai_economics_100.py`; existing `test_management_tokenomics_api_100` (2) and `test_management_tokenomics_invariant_100` (6) pass; Playwright screenshot [overview-ai-economics.png](management-tokenomics-overview-100-live-2026-11-19/overview-ai-economics.png) shows all six cost figures Unknown and all denominators 0 on an unpriced synthetic store. |
| 3 | All child features closed or deferred | Already ticked | Issue state. |

## Limits

* The deployed demo image (`ca-cutover-test-demo-api`) does not contain this change; showing it live needs a deploy, which was out of scope (no production change). The live proof is therefore a local Playwright run on a synthetic store, not a hosted one.
* OD-51 stays open and no price source is set, so Unknown is the correct value everywhere; a priced rendering is proven only by the unit test.
* Whole-programme management views beyond the Overview (forecast, export) were not re-audited here.

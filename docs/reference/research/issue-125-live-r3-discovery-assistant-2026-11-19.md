---
title: Live re-audit of the optional discovery assistant (issue 125, run 3)
description: Third demo audit of issue 125 on main e3494f476 with a per-criterion proven or unproven table and the reason no source change is warranted
author: AMA RPI agent
ms.date: 2026-11-19
ms.topic: reference
keywords:
  - issue 125
  - discovery assistant
  - read-only
  - design hypothesis
estimated_reading_time: 3
---

Refs #125. This repeats the [run 2 note](./issue-125-live-r2-discovery-assistant-2026-11-18.md) at main `e3494f476`, for the synthetic desktop demo under the owner decisions of 2026-11-18. Nothing here is company, resident or production evidence, and no criterion is ticked.

## Method

* Clean virtual environment with `pip install -e src/core`; the five `test_discovery_assistant_*.py` modules and `python -m zava_forward.core discovery-demo`. The environment was removed afterwards.
* `az containerapp show` on `ca-cutover-test-demo-api` (resource group `ama`): revision `ca-cutover-test-demo-api--0000033`, image digest prefix `sha256:5368f4e4`, the same image as run 2, so the run 2 live probes (no discovery route, answers identical to a control path) still describe the deployed code. No new probe and no sign-in were needed.
* Retained outputs: `.copilot-tracking/evidence/2026-11-19/issue-125-live-r3/` (`offline-tests.txt`, `cli-demo.txt`, `azure-app.txt`). No Azure resource was created or changed; no source changed.

## Observations

* Offline: 47 tests run, 47 pass.
* `discovery-demo`: `company_connection` DENY; `approved_solution` false; `write_source_system`, `contact_resident` and `rank_properties` denied by the authority boundary, `read_company_dataset` not on the read-only allowlist; every decision `attempted:false`, `dispatched:false`; the comparison block has `criterion_met:false`, no human result pointers and all four comparators missing for every measure.

## Per-criterion result

| Criterion in #125 | Result for the demo | Reason |
| --- | --- | --- |
| Readiness list satisfied before connection to company data | Unproven | Needs a named discovery owner, population, dictionary, source map and approved access and privacy controls from Phase 0 (#123). The gate correctly returns NOT_READY and DENY, which shows the gate works, not that readiness holds |
| Assistant has no write access to operational systems | Demo behaviour proven; criterion unproven | Write-class requests are denied and never dispatched, and the deployed API has no route. Observed no-write on an approved operational connection needs that system and an access review |
| Compared against manual analysis and conventional reporting | Unproven | Zero human results. A synthetic "conventional" engine written here would repeat the arithmetic of the draft and would not be an independent or human comparison, so it would not meet the criterion |

## Decision

No criterion can be newly proven with real code for the demo. Adding code would duplicate the bounded CLI delivered by #1355 or fabricate a comparison, so no source changed and no FULL tier applies. All three items stay production-only.

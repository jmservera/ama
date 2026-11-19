---
title: Live re-audit of the optional discovery assistant (issue 125, run 4)
description: Fourth demo audit of issue 125 on main 1dddac2e0 with a per-criterion proven or unproven table
author: AMA RPI agent
ms.date: 2026-11-19
ms.topic: reference
keywords:
  - issue 125
  - discovery assistant
  - read-only
estimated_reading_time: 2
---

Refs #125. This repeats the [run 3 note](./issue-125-live-r3-discovery-assistant-2026-11-19.md) at main `1dddac2e0` for the synthetic desktop demo under the owner decisions of 2026-11-18. Nothing here is company, resident or production evidence, and no criterion is ticked.

## Method

* Clean virtual environment with `pip install -e src/core`, removed afterwards. The five `test_discovery_assistant_*.py` modules and `python -m zava_forward.core discovery-demo`.
* `az containerapp show` (read only) on `ca-cutover-test-demo-api` in resource group `ama`: revision `ca-cutover-test-demo-api--0000033`, running, image digest prefix `sha256:5368f4e4`, unchanged since run 3, so the run 2 probes still describe the deployed image. No Azure resource was created or changed.
* Retained outputs: `.copilot-tracking/evidence/2026-11-19/issue-125-live-r4/`.

## Observations

* Offline: 47 tests run, 47 pass.
* `discovery-demo`: `company_connection` DENY, `approved_solution` false; write, resident contact and ranking requests denied by the authority boundary; every decision `attempted:false`, `dispatched:false`.

## Per-criterion result

| Criterion in #125 | Result for the demo | Reason |
| --- | --- | --- |
| Readiness list satisfied before connection to company data | Unproven | Needs a named discovery owner, population, dictionary, source map and approved access and privacy controls from Phase 0 (#123). The gate returning NOT_READY shows the gate works, not that readiness holds |
| Assistant has no write access to operational systems | Demo behaviour proven; criterion unproven | Write-class requests are denied and never dispatched. Observed no-write on an approved operational connection needs that system and an access review |
| Compared against manual analysis and conventional reporting | Unproven | No human results exist. A synthetic conventional engine would repeat the draft arithmetic and would not be independent |

## Decision

Every remaining criterion is production-only or needs a human. No source changed and no FULL tier applies.

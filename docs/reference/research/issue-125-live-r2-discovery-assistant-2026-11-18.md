---
title: Live re-audit of the optional discovery assistant (issue 125, run 2)
description: Second 2026-11-18 live demo audit of issue 125 with a clean-environment test result that resolves the earlier 46 of 47 outcome, and a per-criterion proven or unproven table
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 125
  - discovery assistant
  - read-only
  - design hypothesis
estimated_reading_time: 5
---

Refs #125. This repeats and extends the [first live note](./issue-125-live-discovery-assistant-evidence-2026-11-18.md) at main `4fc9ff025`. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are out of demo scope. No criterion is ticked. Nothing here is company, resident or production evidence.

## Method

* Live app `ca-cutover-test-demo-api`, revision `--0000031`, image digest prefix `sha256:5368f4e4` (read with `az containerapp show`). Entra sign-in with the employee demo account through Playwright Chromium at 1366 by 900; credentials were read at run time and never printed. The `/api/me` account fields are removed from the retained output.
* Offline: the five `discovery_assistant_*` test modules and `python -m zava_forward.core discovery-demo`.
* Retained outputs and scripts: `.copilot-tracking/evidence/2026-11-18/issue-125-live-r2/` (`probe1.json`, `probe2.json`, `static_scan.json`, `cli-demo.txt`, `offline-tests.txt`, `offline-tests-venv.txt`, `azure-app.txt`). The workbench screenshot was not retained because it showed case names.
* No Azure resource was created or changed, so nothing needed deleting. The throwaway virtual environment used for the test run was removed. No source changed.

## Observations

| Observation | Result |
| --- | --- |
| Live GET probes of nine discovery or evidence assistant paths, plus `/openapi.json`, `/docs`, `/api/health`, `/api/version` | Discovery paths return 403 "Your role does not include this."; `/openapi.json` and `/docs` return 404. The control path `/api/zzz-nonexistent-control` returns the same 403, so the 403 is a generic router answer, not a discovery endpoint |
| Live POST of `{"tool":"write_source_system"}` to three discovery paths | 404 "Not found.", identical to the POST control. Nothing is dispatched; the deployed API has no discovery assistant route |
| Workbench UI as the Retrofit Programme Manager demo account | Page text contains neither "discovery assistant" nor "evidence assistant" |
| Static scan of the five modules | No flagged imports and no builtin I/O calls |
| `discovery-demo` | `company_connection` DENY; readiness lists missing items (including accountable owner, baseline population, access and privacy controls, non-agent comparator); `write_source_system`, `contact_resident` and `rank_properties` denied by the authority boundary; `read_company_dataset` denied as not on the read-only allowlist; decisions are `attempted:false`, `dispatched:false`; status `UNAPPROVED_DESIGN_HYPOTHESIS`; `overall_passed` true |
| Comparison block | `criterion_met:false`, no human result pointers, all four comparators missing for the measures |
| Offline tests, user-site Python | 47 run, 46 pass. `test_demo_runs_from_this_worktree_without_inputs` fails with `ModuleNotFoundError: No module named 'zava_forward'` because it replaces `HOME` and the package is not installed |
| Offline tests, clean virtual environment with `pip install -e src/core` | 47 run, 47 pass. This resolves the first note's caveat: the failure was an uninstalled package, as the repository instructions require installing `src/<project>` first, not a product defect |

## Per-criterion result

| Criterion in #125 | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Readiness list satisfied before connection to company data (UNTICKED) | Unproven; cannot be proven for the demo | Readiness needs a named discovery owner, agreed population, validated dictionary, source map and approved access and privacy controls from Phase 0 (parent #123). The demo has none, and DPO and Legal approval are out of scope. The gate behaves correctly (NOT_READY, connection DENY), which shows the gate works and not that readiness holds. Production-only item |
| Assistant has no write access to operational systems (UNTICKED) | Demo behaviour proven; criterion unproven | In the demo, the modules have no I/O imports, write-class requests are denied and never dispatched, and the live API exposes no route, matching an unrelated control. Observed no-write on an approved operational connection needs that system, its credentials and an access review. Production-only item |
| Compared against manual analysis and conventional reporting (UNTICKED) | Unproven; cannot be proven for the demo | `criterion_met:false` with zero human results; the conventional table is the same arithmetic as the draft, not an independent engine. A real comparison needs analysts' recorded results on real data. Production-only item |

## Production-only items

* Accountable discovery owner, population, dictionary, source map, privacy and access approvals (Phase 0, #123).
* Observed no-write access on a real operational connection.
* Recorded manual and conventional comparison on real data.

## What this does not prove

* Any approved company-data connection or any actual human comparison.
* Model behaviour: `model_used` is false and no model was called.
* That the live container runs the same code as this branch; the probes show only that no discovery route is reachable.

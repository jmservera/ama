---
title: Live demo evidence for the optional discovery assistant (issue 125)
description: Recorded 2026-11-18 run showing the discovery assistant is a read-only design hypothesis in the synthetic demo, what the live API exposes, and a per-criterion proven or unproven result
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 125
  - discovery assistant
  - read-only
  - design hypothesis
estimated_reading_time: 6
---

Refs #125. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Nothing here is company, resident or production evidence, and no criterion is ticked.

## Method

* Live target: `ca-cutover-test-demo-api` (image digest `sha256:5368f4e4...e17e5fb`, revision `--0000031`), Entra sign-in with the employee demo account, Playwright Chromium at 1366 by 900. Credentials were read at run time and never printed.
* Offline: the discovery assistant tests in `src/core/tests` and the `discovery-demo` command (PR #1355, `a0f7cf1`, ancestor of this branch).
* Scripts and outputs: `.copilot-tracking/evidence/2026-11-18/issue-125-live/` (`probe1`, `probe2`, `static_scan`, `cli-demo.txt`, `offline-tests*.txt`). Screenshot: [workbench home](./issue-125-live-workbench-home-2026-11-18.png).
* No Azure resource was created or changed, so there is nothing to delete. No source changed.

## Observations

| Observation | Result |
| --- | --- |
| Live probes of nine discovery or evidence assistant paths, plus unrelated control path `/api/zzz-nonexistent-control` | Every GET returns 403 "Your role does not include this" and every POST returns 404 "Not found", identical to the control. The deployed API exposes no discovery assistant route to read or write |
| Workbench home after sign-in | No mention of a discovery or evidence assistant |
| Source search | No `src/api`, `src/agents` or `src/orchestrator` code uses the five `discovery_assistant_*` modules; they are reachable only by the `python -m zava_forward.core discovery-demo` command |
| Static scan of the five modules | No network, store, subprocess, file, model or credential imports; `datetime` is used only to parse timestamps; only the demo CLI prints |
| `discovery-demo` run | `company_connection` DENY, readiness NOT_READY with 10 of 10 items missing, `write_source_system`, `contact_resident` and `rank_properties` denied by the authority boundary, `read_company_dataset` denied as not on the read-only allowlist, every decision `attempted:false`, `dispatched:false`, `writes_to_source_system:false`, `model_used:false`, status `UNAPPROVED_DESIGN_HYPOTHESIS`, three identical repeat digests |
| Comparison block | `criterion_met:false`, no human result pointers, all four comparators missing for all ten measures; the conventional table states it is the same calculation, not an independent engine |
| Offline tests | 47 run, 46 pass. `InstalledCommandTests.test_demo_runs_from_this_worktree_without_inputs` fails here only because the test replaces HOME and so drops the user-site path that makes `zava_forward` importable (`ModuleNotFoundError`); the same command with an explicit `PYTHONPATH` succeeds. Environment limit, not a product defect, but it is not a passing run |

## Per-criterion result

| Criterion in #125 | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Readiness list satisfied before connection to company data (UNTICKED) | Cannot be proven for the demo | Readiness needs a named accountable discovery owner, agreed population, validated dictionary, source map, approved access and privacy controls and other human-supplied evidence (Phase 0, parent #123). The demo has none, and DPO and Legal approval are out of demo scope. The gate behaves correctly: it reports NOT_READY with all 10 items missing and denies company connection. That shows the gate works, not that readiness is satisfied. Stays open |
| Assistant has no write access to operational systems (UNTICKED) | Demonstrated for the demo; not observed operational no-write access | The demo assistant is pure policy code with no I/O imports, is not deployed or routed on the live API (identical to a control path), and its write-class tool requests are denied and never dispatched. This does not show that a future connected assistant has no write access: that needs the real operational system, its credentials and an access review, which do not exist. Do not tick until observed on the approved connection |
| Compared against manual analysis and conventional reporting (UNTICKED) | Cannot be proven for the demo | The comparison shows `criterion_met:false` and zero human results. The conventional table is the same arithmetic as the draft, and expected figures are constructed. An actual manual and conventional comparison needs analysts' recorded results on real data. Stays open |

## What this does not prove

* Approved company-data connection, observed operational no-write access, or any actual human comparison.
* Any model behaviour: `model_used` is false and no model was called.
* That the 47th test passes in a clean installed environment; hosted CI is the authority for that.

---
title: Phase 0 retrofit-flow discovery audit, second live pass (issue 124)
description: Fresh 2026-11-18 re-run of the offline contract, the synthetic pack probe, a repository consumer search and a live Azure and authenticated browser probe, with a per-criterion proven or unproven table for issue 124 and the owner-only items
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 124
  - phase 0 discovery
  - BG-011
  - live demo
estimated_reading_time: 6
---

Refs #124. Scope is the synthetic desktop demo. The owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive billing reconciliation, DPO and Legal approval and person-run assistive technology testing for the demo. Nothing below is a company finding. This pass supplements the [first evidence note](./issue-124-phase0-discovery-evidence-2026-11-18.md), which is unchanged, and ticks nothing in the issue. No source code changed, no Azure resource was created or changed (so nothing needed deleting), and the tier is FOCUSED.

## Method and retained evidence

Files are in `.copilot-tracking/evidence/2026-11-18/issue-124-live-r2/`.

* Offline tests, `unittest.txt`: from `src/core`, `PYTHONPATH=src:tests python3 -m unittest test_discovery_contract test_discovery_flow test_discovery_register` ran 59 tests, OK.
* Probe, `probe.json`: the first note's `probe.py` re-run against this worktree. After the module path is normalised, `diff` shows the output identical to the earlier run (owner statuses, 49 dictionary gaps, register gaps, pack counts); the diff itself is Observed; raw output not retained.
* Consumer search, `consumers.txt`: a search of `src`, `infra` and `tools` for `discovery_contract`, `discovery_register` and `discovery_flow` (excluding tests) lists only `discovery_contract.py`, `discovery_flow.py` and `src/core/README.md`. No `src/api`, `src/orchestrator`, `src/agents`, `src/importer` or infrastructure file uses them, and `src/api/src` has no discovery route.
* Azure CLI, read-only, `azure_cli_outputs.txt`: `ca-cutover-test-demo-api` at revision `--0000031` (image digest `sha256:5368f4e4...c17e5fb`), `ca-resident-demo` at `--0000012`, Event Hub `evhns-cutover-test-demo` holding only `sensor-readings`. Unauthenticated requests to the API return 401 (Easy Auth).
* Authenticated browser probe, `live_discovery_probe.py` and `live_discovery_probe.json`: Playwright Chromium, 1366 by 900, signed in as the employee demo account with credentials read at run time and never printed or saved. GET only. `/openapi.json` returned 404 (documentation disabled), so no route list exists. `/api/discovery`, `/api/phase0/discovery` and a deliberately invented control path `/api/zz-nonexistent-control` all returned 403. The control path shows the 403 is a default deny, so the live probe alone cannot distinguish absent from forbidden. The conclusion that no discovery surface is deployed rests on the repository search above, not on the 403. The JSON contains no `@`.
* A first run of the probe crashed in its final print statement after writing its JSON (a driver bug, fixed); the output was then regenerated with the control path added.

## Per-criterion result

| Criterion in #124 | Proven for the demo | Unproven, and who owns it | Tickable now |
| --- | --- | --- | --- |
| Discovery owner nominated and endpoint (accepted handover) agreed (unticked) | The rule: default `NOT_NOMINATED`, AI actor refused, sponsor and owner must be distinct, only `accepted handover` accepted as endpoint, `ENDPOINT_AGREED` reachable (placeholder names, rule check only). | A named human nomination and the endpoint agreement. Owner/person-only: the executive sponsor decides. The demo holds no such record, and a placeholder or a name supplied by an agent is not a nomination. | No |
| Lifecycle and event dictionary validated (unticked) | Schema and counts: 15 stages (10 flow plus 5 exception), 15 events, 8 timestamp specs, 7 wait states, 4 return-loop kinds; 49 validation gaps open; validation refused without a ready owner and refused for an AI actor. Synthetic log covers 11 of 15 contract events (4 have no event type). | Operational-owner validation of each stage, event, timestamp, wait state and return loop. Owner/person-only: needs workshops with named role holders. Schema validity is not owner validation, as the owner's 2026-11-16 correction states. | No |
| Constraint register records supporting and contradicting evidence (unticked) | The two-sided rule: seed register has five ranked hypotheses with 0 supporting and 0 contradicting evidence and two gaps each; one-sided evidence leaves a gap, both sides close the evidence gap. | Real evidence from the twelve-month company extract plus discovery-owner and domain-owner validation. Owner/person-only and data-gated: the synthetic pack cannot supply contradicting company evidence. | No |
| Findings are not company findings until owners validate (ticked) | Re-confirmed: every output `owner_validated=false` and `candidate_hypothesis_not_company_finding`; pack validation without a ready owner is refused. | Nothing. | Already ticked; no contradiction found |

## What the live demo adds, and does not

* It adds a current deployment fact: the demo has no deployed discovery capability, so there is no live behaviour to prove for any of the three unticked criteria. They are contract-level only.
* It does not add any nomination, validated dictionary or company evidence. Using the demo owner's account to record a nomination would invent a sponsor decision, and the brief reserves that to the executive sponsor.

## Owner-only list (unchanged, restated)

1. Sponsor names the discovery owner and agrees the `accepted handover` endpoint (OD-16, OD-18).
2. Named operational owners close the 49 dictionary gaps in workshops.
3. An approved twelve-month company extract is supplied and reviewed; the register then records evidence on both sides for each hypothesis.

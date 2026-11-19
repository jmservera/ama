---
title: Phase 0 retrofit-flow discovery audit, third live pass (issue 124)
description: 2026-11-19 re-run of the offline discovery contract tests, repository consumer search and live Azure and authenticated browser probe, with a per-criterion proven or unproven table for issue 124
author: AMA RPI agent
ms.date: 2026-11-19
ms.topic: reference
keywords:
  - issue 124
  - phase 0 discovery
  - BG-011
  - live demo
estimated_reading_time: 4
---

Refs #124. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18. Nothing here is a company finding, nothing is ticked in the issue, no source changed and no Azure resource was created or modified. This supplements the [first](./issue-124-phase0-discovery-evidence-2026-11-18.md) and [second](./issue-124-live-r2-phase0-discovery-audit-2026-11-18.md) notes, which are unchanged.

## Retained evidence

Files are in `.copilot-tracking/evidence/2026-11-19/issue-124-live-r3/`.

* `unittest.txt`: from `src/core`, `PYTHONPATH=src:tests python3 -m unittest test_discovery_contract test_discovery_flow test_discovery_register` ran 59 tests, OK.
* `consumers.txt`: only `discovery_contract.py`, `discovery_flow.py` and `src/core/README.md` reference the discovery modules outside tests. No API, orchestrator, agent, importer or infrastructure file consumes them.
* `azure_cli_outputs.txt` (read-only): API app now at revision `ca-cutover-test-demo-api--0000033` (was `--0000031` on 2026-11-18), resident app at `ca-resident-demo--0000014` (was `--0000012`), Event Hub namespace holds only `sensor-readings`.
* `live_discovery_probe.json`: signed-in Playwright Chromium probe, GET only, credentials read at run time and not stored. `/openapi.json` 404; `/api/discovery`, `/api/phase0/discovery` and an invented control path all return 403, so the 403 is a default deny and does not show absence. The repository search carries that conclusion. The first run timed out on navigation (cold start); a retry succeeded. The screenshot was deleted because it showed only the signed-in workbench.

## Per-criterion result

| Criterion in #124 | Proven for the demo | Unproven | Tickable now |
| --- | --- | --- | --- |
| Discovery owner nominated and endpoint agreed (unticked) | Rule only: default `NOT_NOMINATED`, AI actor refused, sponsor distinct from owner, endpoint must be accepted handover | The named human nomination and endpoint agreement (executive sponsor decision) | No |
| Lifecycle and event dictionary validated (unticked) | Schema and counts; validation gaps block sign-off | Operational-owner validation in workshops | No |
| Constraint register supporting and contradicting evidence (unticked) | Two-sided evidence rule; seed register has no evidence on either side | Evidence from an approved twelve-month extract plus owner validation | No |
| Findings are not company findings until owners validate (ticked) | Re-confirmed, fail-closed | None | Already ticked |

## Outcome

All three unticked criteria require a named human decision or approved company data, which the demo waivers do not cover. A synthetic nomination or validation would fabricate the owner decision the criteria exist to capture. The only code option, exposing the discovery contract through `src/api`, is a feature that would not satisfy any criterion and would need the FULL tier, so no source was changed.

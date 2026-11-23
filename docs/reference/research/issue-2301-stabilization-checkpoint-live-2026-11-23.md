---
title: Issue 2301 demo-scope stabilization checkpoint evidence (2026-11-23)
description: Per-criterion proven or unproven record for the nine-epic stabilization checkpoint, with a signed-in read-only probe of the live demo and local audit and regression runs
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `2c06796f5f5d097d214e22d630ce5f638f2b2a19`. Refs #2301 and #440. No `src/` change, no Azure resource created or changed, no write call on the demo. Sign-in values were read at runtime and never printed. The checkpoint itself is the section "Demo-scope stabilization checkpoint for nine delivered epics (2026-11-23, Refs #2301 #440)" in the [cut-over evidence pack](../../architecture/cutover-evidence-pack.md).

## Evidence

* Sub-issue state, read through REST on 2026-11-23: every child of Epics #73 (6), #81 (9), #89 (5), #93 (4), #100 (4), #109 (3), #149 (16), #157 (7) and #208 (9) is closed as completed.
* Azure (`az`, resource group `ama`): `ca-cutover-test-demo-api` active revision `ca-cutover-test-demo-api--0000057`, `Healthy`, traffic 100; `/healthz` returns 200.
* Signed-in Playwright probe (GET only): [live_probe.py](../../../.copilot-tracking/evidence/2026-11-23/issue-2301-live/live_probe.py), output [live_probe.json](../../../.copilot-tracking/evidence/2026-11-23/issue-2301-live/live_probe.json), screenshot [workbench-home.png](../../../.copilot-tracking/evidence/2026-11-23/issue-2301-live/workbench-home.png). Fifteen of sixteen endpoints return 200; `/api/coordinator` returns 400 because it needs query parameters.
* Local: seven `tools/test_epic_*` audits pass (4, 4, 4, 5, 7, 6, 8 tests); 464 focused core and api tests pass with 26 skipped and 1 expected failure.

## Criterion verdicts

| # | Criterion | Verdict | Reason |
| --- | --- | --- | --- |
| 1 | Dated checkpoint record in the evidence pack, linked from each epic | Record proven; epic links unproven | The pack section is committed and guarded by `tools/test_stabilization_checkpoint_2301.py`. Linking needs nine GitHub issue edits, not made here. |
| 2 | Per-epic recommendation; "child accepted" criteria ticked or listed as gaps with an owner | Partly proven | All nine get `continue`. Unticked criteria are listed with owners; ticking is an owner action. |
| 3 | Each confirmed gap has a scoped issue | Proven (no confirmed gap) | No defect was observed; the 400 on a parameterless coordinator call is validation. No issue created. |
| 4 | Epics with all criteria proven are closed with an evidence comment | Unproven | Every epic still carries the #440 criterion, so none qualifies; closure is a remote action. |

## Limits

* One worker, one in-loop review, no PR and no independent reviewer.
* The probe reads one demo revision at one time. Write journeys, sensor ingestion at this head, person-run assistive-technology testing, Legal and DPO approval are not proven here; the last three stay deferred to #1907, #1905 and #1906.

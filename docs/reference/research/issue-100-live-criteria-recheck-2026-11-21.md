---
title: Issue 100 criteria re-check with live AI economics probe (2026-11-21)
description: Per-criterion proven or unproven record for epic 100, with a signed-in observation of the AI consumption economics card on the deployed demo and local management insight and export tests
ms.date: 2026-11-21
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `c703a24a1`. Refs #100. No source change, no Azure resource created or changed; the probe is read-only. Sign-in values were read at runtime and never printed. This note updates [the 2026-11-19 note](./issue-100-live-2026-11-19.md), whose live gap for criterion 2 no longer holds.

## Live observation

* `ca-cutover-test-demo-api` runs revision `ca-cutover-test-demo-api--0000038` (az, resource group `ama`).
* Probe [live_probe.py](../../../.copilot-tracking/evidence/2026-11-21/issue-100-live-20261121T081319Z/live_probe.py), output [live_probe.json](../../../.copilot-tracking/evidence/2026-11-21/issue-100-live-20261121T081319Z/live_probe.json), desktop screenshot [overview-ai-economics.png](../../../.copilot-tracking/evidence/2026-11-21/issue-100-live-20261121T081319Z/overview-ai-economics.png). The employee account got 200 from `/api/me`, `/api/stats` and `/api/progress`; the last two carry `ai_consumption_economics` (`ai-consumption-economics/v1`).
* Denominators in `/api/stats`: 1 proposal, 0 accepted outcomes, 24 metered calls, 0 unmetered, 1 unreviewed, 0 rejected or withdrawn, 589 workflow-only calls excluded. `price_source` is Unknown, `od_51_status` is open, `total_tokens` is Unknown (token metadata incomplete). Token cost, total cost of AI, cost per accepted outcome, quality-qualified cost and booked value are the string Unknown, never 0.
* The Overview card "AI consumption economics" renders the same denominators and every cost row as Unknown, with the sentence "Unknown means no price source or no accepted outcome exists to divide by; it is not zero."

## Local observation

All OK, run sequentially: `src/core` `test_management_tokenomics_invariant_100` and `test_tokenomics_comparison` (22); `src/api` `test_overview_ai_economics_100` and `test_management_tokenomics_api_100` (5). Wider management insight and export surface: `src/core` `test_indoor_projection`, `test_list_export`, `test_progress_event_capture`, `test_progress_reports`, `test_resident_forecast` (96 tests, 18 skipped); `src/api` `test_list_export_api`, `test_progress_dashboard`, `test_progress_report_api`, `test_continuity_epoch_export` (178 tests, 51 skipped). Skips are the suites' own conditional skips; their cause was not investigated and they are not counted as passes.

## Criterion verdicts

| # | Criterion | Verdict | Reason |
| --- | --- | --- | --- |
| 1 | Scoped #440 stabilization checkpoint before epic closure | Unproven | #440 is OPEN with two criteria unticked: triage of findings into issues, and research, plan, changes and independent review artifacts. The #100 surface has no failing check and no defect (above), but the criterion names an owner-approved pivot or defer decision, an independent reviewer and a published PR, none of which a worker can supply. |
| 2 | Management views include AI economics with denominators; Unknown, not zero | Proven (Azure observed and local observed) | Live payloads and rendered card above; focused tests pass. Price, budget and target stay unset (BRD OD-51 open), so cost is correctly Unknown. |
| 3 | All child features closed or deferred | Already ticked | #101, #102 and #103 are CLOSED (REST read, 2026-11-21). |

## Decision

No defect found, so no source change and the tier is focused. Criterion 2 can be ticked by the owner on this evidence. Criterion 1 stays open until #440 closes; the epic remains open.

## Limits

* One worker and one in-loop review; no PR and no independent reviewer.
* Not run: `rpi-checks.py`, hosted CI, SQL Server variants. The probe observes one demo revision at one time.

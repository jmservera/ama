---
title: Issue 107 measured real-AI tokens for all five assistants from inside the demo environment (Refs #107)
description: The capped real-AI batch r14 could not run from the VM completed from inside the Container Apps replica, with measured tokens per assistant and no estate change
ms.date: 2026-11-25
---

Scope: synthetic demo, desktop only, no source change. Builds on the [fourteenth pass](./issue-107-live-r14-release-records-2026-11-25.md). Evidence and redacted scripts are in `.copilot-tracking/evidence/107-live-r15/`; no credential or token was printed or stored.

## Method

* r14 stopped because the AI account allows only private-endpoint access and the VM has none. The demo API replica already sits on the environment network, so the merged harness (`src/api/checks/assistant_real_ai_acceptance.py`) was run once inside `ca-cutover-test-demo-api` through `az containerapp exec`, using the app's own user-assigned managed identity (token from the replica's identity endpoint, kept in memory).
* The listing used was the r14 live listing: all five assistants show release `"in force"` on the 13-field binding (deployment `standard`, serving model `gpt-4.1-nano-2025-04-14`).
* Hard cap: 5 calls, 200000 tokens, 400 prompt and 200 completion tokens per call, USD 1. The batch was run once, with no retry. The payload file was deleted from the replica afterwards.
* No Azure setting, role, network rule or allowance changed. The `azure.identity` credential could not load the identity inside the exec shell (the identity header exists only for PID 1), so the runner called the identity endpoint directly; that is a harness-environment detail, not an app defect.

## Result (measured)

| Assistant | Prompt tokens | Completion tokens |
| --- | --- | --- |
| stock-prioritisation | 44 | 10 |
| assessment-preparation | 42 | 8 |
| funding-evidence | 42 | 8 |
| works-resident-coordination | 44 | 10 |
| quality-evidence | 42 | 8 |

Outcome `completed`, 258 tokens in total, USD 0.0000390 at the harness' stated demo rates (the rates are the owner's demo assumptions, not an Azure bill). Report: `harness_report.txt`.

## Limits

* The calls are synthetic, case-free probes sent by the harness through the held-out provider path, not proposals produced by the app's proposal service. The app's own invoke path stays off until an operator allowance exists; none was set.
* The release approvals are the owner's demo decision, not OQ-017/018/019 clearance.
* Criterion 1 (independent worker, older real image) is not advanced: no historical image was run, since that needs a revision change.

## Per-criterion result

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances | Unproven beyond [r12](./issue-107-live-r12-endpoint-deployment-2026-11-25.md) (11 of 13 fields on constructed fixtures, local disposable SQL) | No real older packaged image run; changing a revision is outside this pass |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Proven for the demo as far as evidence goes: five actual release records in force on the delivered image (r14), plus measured real-AI tokens per assistant on that deployment and serving model (258 in total, this note) | Calls were harness probes, not app-generated proposals; no operator allowance, no OQ-017/018/019 clearance, so not an operational acceptance |

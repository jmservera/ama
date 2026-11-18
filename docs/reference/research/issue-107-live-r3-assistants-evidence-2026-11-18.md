---
title: Five assistants live demo re-verification, third pass (Refs #107)
description: Third per-criterion proven or unproven record for the two unticked acceptance criteria of issue 107, adding the ACR access limit, a same-image revision restart observation and the origin of the live suspension SUS-1
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, FOCUSED tier, no source change. Owner decisions of 2026-11-18 apply (live Azure authorised in resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive technology testing waived). Head `da33c1ecc`. This note supplements [the first pass](./issue-107-live-assistants-evidence-2026-11-18.md) and [the second pass](./issue-107-live-r2-assistants-evidence-2026-11-18.md); the SQL Server 2022 (7 tests) and SQLite proxy (80 tests) results of the second pass are reused by reference and were not re-run, because no source has changed. Evidence: `.copilot-tracking/evidence/2026-11-18/issue-107-live-r3/` (probe script and JSON, no credentials).

## Result per unticked criterion

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances | Partly proven. Actual SQL Server 2022 tests (second pass) cover revocation, restart and allowance races; a live revision restart on the same image left the stored suspension in place | Old-image path is SQLite proxy only; nothing ran on Azure SQL; the box stays unticked |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Unproven for the demo | No approved release exists; denial side re-proven live; approved side cannot be shown |

## New evidence

* The demo registry `crcutovertestrzsrg` reports `publicNetworkAccess: Disabled` and network default action `Deny`; `az acr repository show-tags` fails with a connectivity error. An older released image cannot be pulled, and enabling access would change deployed infrastructure, which the owner decision does not authorise. Source trees older than release admission cannot stand in for an old image because they never had the check.
* `az containerapp revision list` shows one active revision, `ca-cutover-test-demo-api--0000032` (created 2026-11-18T16:20:23Z), on image digest `sha256:5368f4e4...c17e5fb`. The second pass saw revision 0000031 on the same digest, so a real restart occurred with identical code.
* Read-only probe at revision 0000032 (Entra demo employee, role `Retrofit Programme Manager`, credentials read at run time and never printed; no invoke, so no new proposals): five assistants each report `missing: approved, unexpired release record` with release, residual-risk, suspension and restart holders all `gap` (OQ-017); forecast `proactive: false`, `call_allowance: 0`; rai-metrics `tokens: 0`, `fallback: 16`, `persisted: 87`. These counters equal the second pass, so the restart replenished nothing and spent nothing.
* The forecast hold text `Suspended (SUS-1)` (an open question in the second pass) matches the continuity state `epoch 1, suspended SUS-1, scope all` retained in [deployed-parity-live-r3](./deployed-parity-live-r3-2026-11-18/raw/14-continuity.txt), a probe suspension recorded by the #122 audit in the [log](../log.md). This is inferred from retained evidence, not from a fresh `/api/continuity` read. It survived the 0000031 to 0000032 restart. No restart authority is appointed, so lifting it was not attempted.

## Limits

* The restart observation shows a same-image restart preserving denial state; it is not an old-image test and does not prove the property for every future image.
* Approving a release for the demo needs a named approver and residual-risk holder (OQ-017). Creating one would fabricate authority.
* No Azure resource was created, so nothing needed deletion. Independent exact-head review and hosted CI remain outstanding.

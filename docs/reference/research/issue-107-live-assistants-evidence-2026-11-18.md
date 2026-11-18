---
title: Five assistants live demo evidence (Refs #107)
description: Per-criterion proven or unproven record for the two unticked acceptance criteria of issue 107, from local disposable SQL Server runs and a live demo read and denial probe on 2026-11-18
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive billing reconciliation, DPO and Legal approval and person-run assistive technology testing for the demo. No source code changed. Evidence folder: `.copilot-tracking/evidence/2026-11-18/issue-107-live/`.

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images/restarts cannot restore revoked approval or replenish finite allowances | Proven on actual SQL Server 2022, local disposable service; not run against Azure SQL | See below. Azure SQL was not used: the test fixture refuses anything but the local service, and a revocation or restart drill on the live demo is outside the owner decision (no drills). |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Unproven for the demo. Denial side proven live; the approved side cannot be shown | See below. |

## Criterion 1: independent workers, races, revocation, restart

* Actual SQL: `ZF_TEST_MSSQL=1 python3 -m unittest -v test_assistant_release.MssqlUnleasedRevocation` from `src/api` against `mcr.microsoft.com/mssql/server:2022-latest` (Microsoft SQL Server 2022 RTM-CU28) in a throwaway local container bound to 127.0.0.1 with a generated one-off password. 7 tests, OK, 70 s. They start separate processes for changed prompt, policy and permission versions (revoked, a fresh process stays denied), independent-worker revocation of an unleased task, post-revocation restart with no calls or replenishment, racing processes that cannot overspend or replenish a finite allowance, and restarted processes that keep a partly used allowance and stop at the stored call count. Output: `mssql_unleased_revocation.txt`.
* SQLite proxy for the restart and old-image paths (fresh store, connection and service over one file database): `test_assistant_restart_non_replenishment` 14 tests OK (revocation or suspension on one connection blocks claim, dispatch and completion on others; old image cannot reactivate a revoked release; restart and authority-token rotation cannot refill calls or tokens; mismatch on a separate worker stays denied after restart). With `test_assistant_release` and `test_assistant_reserve_guard`: 80 tests OK, 7 skipped (the MSSQL classes, which were run separately above). Output: `sqlite_restart_non_replenishment.txt`, `sqlite_three_modules_summary.txt`. The test file states these are proxies, not actual SQL acceptance.
* Limit: the non-replenishment and old-image tests exist on SQLite only; the MSSQL class covers revocation, restart and allowance races but not the old-image change path. The workers are processes on one host, not separate container revisions.
* Cleanup: container `ama107-mssql` removed, password file shredded; no Azure resource created.

## Criterion 2: approved exercise record and delivered-build acceptance

Live probe (`live_probe.py`, Playwright Chromium, Entra demo employee account, role `Retrofit Programme Manager`, credentials read at run time and never printed) on `ca-cutover-test-demo-api`. Image `zava-forward-api@sha256:5368f4e4...c17e5fb`, revision `0000031`, `ZF_STORE=mssql`, `ZF_SQL_AUTH=msi`, `ZF_DEPLOYMENT_PROFILE=demo`, `AI_DEPLOYMENT=standard`, `AI_MODEL_VERSION=gpt-4.1-nano-2025-04-14`. The `standard` deployment on `aif-cutover-test-rzsrg` reports model `gpt-4.1-nano` version `2025-04-14`, `GlobalStandard`.

* `GET /api/assistants` lists all five assistants at registry version 1.0.0, each with a binding (provider, endpoint, deployment, prompt, policy, data, provenance, permission and model versions) and `release.missing = ["approved, unexpired release record"]`. Owner shown as "RAI task owner not appointed (OQ-017)"; release, residual-risk, suspension and restart holders are all `gap`.
* `GET /api/assistants/forecast`: `proactive: false`, `call_allowance: 0`. `GET /api/assistants/proposals`: no proposals, "Operator authority, finite allowance and expiry are required."
* `POST /api/assistants/{id}/invoke` for each of the five on case ZF-2025-0031 returned 202 with state `disabled`, `release: null`, `envelope: null` (no provider call), the missing-evidence reason and the manual route; the denial is retained. RAI metrics after the probe: `invocation` 0, `tokens` 0. Cases ZF-2025-0331, 0148, 0150 and 0151 returned 403 "Case is outside your current scope."
* Why the approved side is unproven: a matching approved record needs a named release approver and residual-risk holder, which OQ-017 records as not appointed. Creating one with the demo account would fabricate authority and change the live demo state, and the owner decision does not authorise that. Real model calls elsewhere (the #432 batch, 12 calls) ran through a measuring runner, not through the proposal service under a release record, so they are not version-linked proposal evidence.
* Consequence: criterion 2 stays unticked. Delivered-build acceptance under CON-009/AC-057 needs an appointed approver, a recorded release and a real proposal from the delivered image; that is outside this docs-only demo task.

## Adverse and limiting observations

* The first invoke run used only the first case and got 403 for all five; the preserved script now walks the visible cases. The overwritten first output is not kept; the final `live_probe_invoke.json` shows the 403 cases too.
* `live-workbench.png` shows the landing page, not a proof; the proof is the JSON.
* The probe wrote five retained denial proposals and a few metric reads into the demo store; nothing else was changed.

## Evidence limits

* Criterion 1 is partly proven: revocation, restart and allowance races on local SQL Server 2022; the old-image and non-replenishment path on a SQLite proxy only, not Azure SQL.
* RAI metrics were read before the invokes only; the zero provider call claim rests on `envelope: null` and `release: null` per invoke. The invoke JSON shows fallback 16 and consumption 16.
* Azure CLI facts, the SQL Server banner, the runtime and the test commit are operator-observed, raw output not retained.
* live-workbench.png is a landing page and not evidence. The demo store now holds five denial proposals. Synthetic persona identifiers are retained in the probe JSON.
* Independent exact-head review and hosted CI are outstanding.

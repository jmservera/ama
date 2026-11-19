---
title: Five assistants live demo re-verification (Refs #107)
description: Second-pass per-criterion proven or unproven record for the two unticked acceptance criteria of issue 107, with retained raw output from a fresh local SQL Server 2022 run and a read-only live demo probe on 2026-11-18
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive billing reconciliation, DPO and Legal approval and person-run assistive technology testing for the demo. No source code changed. This note supplements [the first pass](./issue-107-live-assistants-evidence-2026-11-18.md). Evidence folder: `.copilot-tracking/evidence/2026-11-18/issue-107-live-r2/`.

## Result per unticked criterion

| Criterion | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images/restarts cannot restore revoked approval or replenish finite allowances | Proven on actual SQL Server 2022 (local disposable service) for revocation, restart and allowance races; old-image path proven on a SQLite proxy only; not run on Azure SQL | `mssql_unleased_revocation.txt`, `mssql_banner.txt`, `sqlite_three_modules.txt` |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Unproven for the demo. Default-off and denial side re-proven live; the approved side cannot be shown | `live_probe_read.json`, `azure_readonly.txt` |

## Criterion 1

* Actual SQL: `ZF_TEST_MSSQL=1 python3 -m unittest -v test_assistant_release.MssqlUnleasedRevocation` from `src/api` against `mcr.microsoft.com/mssql/server:2022-latest` (banner: Microsoft SQL Server 2022 RTM-CU28, 16.0.4325.4) in a throwaway container bound to 127.0.0.1 with a generated one-off password. 7 tests OK in 34.5 s: changed prompt, policy and permission versions each revoke in a separate process and a fresh process stays denied; independent-worker revocation of an unleased task is durable; processes after revocation and restart get no calls or replenishment; racing processes cannot overspend or replenish a finite allowance; restarted processes keep a partly used allowance and stop at the stored call count. Raw output retained.
* SQLite proxy: `test_assistant_restart_non_replenishment`, `test_assistant_release` and `test_assistant_reserve_guard`: 80 tests OK, 7 skipped (the MSSQL classes, run separately above), 78 s. The restart file states these are proxies and not actual SQL acceptance.
* Limits: the old-image change path and the five live provider, endpoint, deployment, data and provenance variations have SQLite coverage only; workers are processes on one host, not container revisions; nothing was run against Azure SQL because the fixture refuses it and a drill is outside the owner decision.
* Cleanup: container `ama107r2-mssql` removed, password file shredded, no Azure resource created.

## Criterion 2

Read-only probe (`live_probe.py` without the invoke argument; Playwright Chromium; Entra demo employee, role `Retrofit Programme Manager`; credentials read at run time and never printed) on `ca-cutover-test-demo-api`, image `zava-forward-api@sha256:5368f4e4...c17e5fb`, revision `0000031`, running; the same image as the first pass. The `standard` deployment on `aif-cutover-test-rzsrg` is `gpt-4.1-nano` version `2025-04-14`, `GlobalStandard`.

* `GET /api/assistants`: five assistants, each with `release.missing = ["approved, unexpired release record"]`. `GET /api/assistants/forecast`: `proactive: false`, `call_allowance: 0`, a held reason of "Suspended (SUS-1): use the manual route".
* `GET /api/assistants/rai-metrics`: `tokens` 0, `fallback` 16, `consumption` 16, `invocation` 7, `persisted` 87. No provider token was spent for any assistant.
* This pass did not invoke, so it added no retained proposals. The first pass invoked all five and got `state: disabled`, `envelope: null`.
* The approved side stays unproven. A matching record needs a named release approver and residual-risk holder, which OQ-017 records as not appointed. Recording one on the live demo would fabricate authority and change deployed configuration, and the owner decision does not authorise that. Real model calls elsewhere (#432) ran through a measuring runner, not under a release record.

## Adverse and limiting observations

* The forecast now reports a suspension (SUS-1) that the first pass note did not mention; it is consistent with denial but its origin was not investigated.
* `live-workbench.png` is a landing page and is not proof; the JSON is the proof.
* The Azure CLI facts and probe output are raw but contain only synthetic persona data; email addresses are scrubbed by the script and ids in the Azure output are masked.
* Independent exact-head review and hosted CI are outstanding.

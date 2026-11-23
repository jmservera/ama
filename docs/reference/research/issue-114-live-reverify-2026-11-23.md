---
title: Azure SQL ledger re-verification on the demo (issue 114, 2026-11-23)
description: Fresh read-only live probe of the demo audit ledger, local test run and one added test, with a per-criterion proven and unproven record for issue 114
author: AMA RPI agent
ms.date: 2026-11-23
ms.topic: reference
---

Refs #114. Scope is the synthetic desktop demo in resource group `ama` under the owner decisions of 2026-11-18. All three criteria of the issue are already ticked; this note re-proves what can be re-proven and states what cannot.

## Method

* A throwaway Container Apps job `job-114-reverify` ran [probe.py](./issue-114-live-reverify-2026-11-23/probe.py) once (execution `job-114-reverify-1csu7mm`, Succeeded, 15:41Z to 15:42Z) using the existing orchestrator image and user-assigned identity. It only reads. Output: [probe-job.log](./issue-114-live-reverify-2026-11-23/probe-job.log). The job was deleted; `az containerapp job list` shows no job with `114` in its name.
* Local run from `src/core`: `tests.test_recovery`, `tests.test_sqlstore`, `tests.test_ledger_digest_blob`: [local-tests.txt](./issue-114-live-reverify-2026-11-23/local-tests.txt), 63 tests OK.
* Added one test, `test_unsealed_single_year_run_writes_no_digest_and_report_carries_no_entry_content`, so retained gate output is shown to hold no actor, action or reference text.

## Observations

| Check | Result |
| --- | --- |
| Live store and chain | `MssqlStore`; 7,022 audit entries; chain intact; one year (2026) |
| Per-year verification on live data | `verify_years` intact for 2026 with 7,022 entries |
| Reliance gate in the orchestrator job image | Absent (`has_reliance: false`, `has_require: false`) |
| Reliance gate in the API image | Not determined: `az containerapp exec` failed with `ErrorGeneratingAuthToken` and the registry rejects this client (firewall) |
| Root digests in the job's local digest directory | 0 (the digest container check is covered by the #115 note) |

## Per-criterion status

| # | Criterion | Status | Evidence or reason |
| --- | --- | --- | --- |
| 1 | Per-year audit and ledger digest verification proven by test before reliance | Proven by tests and on live data for the one year held; gate not deployed to the orchestrator image | 63 tests OK, including multi-year SQL and file store cases; live 2026 chain intact. Sealed past years on live data and the gate on a deployed image remain unproven; rolling an image is a production change and was not done |
| 2 | Measured load, latency and cost recorded against PRD targets | Not re-measured here | Existing retained evidence stands (live-load-30min.json, #2191 capacity note); load runs were out of scope and cost reconciliation is not needed for the demo |
| 3 | Backup, restore and deletion re-application tested (DH-005) | Not re-run here | Drills are not authorised; earlier restore evidence in [sql-ledger-live-r2-2026-11-18.md](./sql-ledger-live-r2-2026-11-18.md) stands. Native ledger verification stays blocked by the `VIEW LEDGER CONTENT` permission |

## Follow-ups

* Roll the orchestrator and API images so `verify_ledger_before_reliance` is present, then retain a run (owner-gated deployment).
* Wire the reliance gate into a scheduled job; no non-test caller exists today.

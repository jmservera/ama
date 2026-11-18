---
title: Live ranking publication evidence for issue 79 (demo)
description: Recorded run on 2026-11-18 on live demo Azure showing a scheduled job firing, the unsigned ranking policy refused, and create-only Blob publication of a ranking snapshot
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 79
  - ranking
  - snapshot publication
  - policy sign-off
estimated_reading_time: 5
---

Refs #79. Scope is the synthetic desktop demo, authorised by the owner on 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). Nothing here is production evidence. Production-only parts stay deferred to #1905 to #1908.

## Method

* Repository checks: the ranking tests in `src/core` (146 tests), `src/orchestrator` (11) and `src/api` (58) passed on this branch.
* Live run: a throwaway Container Apps job `job-demo79-ranking-publish` in `cae-cutover-test-demo` with the `id-cutover-test-api` identity, which already holds Storage Blob Data Contributor on `stcutovertestrzsrg`, and a throwaway Blob container `ranking-archive-demo79` on that account. Both were deleted afterwards and a listing confirmed neither remains.
* The job read the 443 open cases of the live Azure SQL store (as-of 2026-10-16) and called the deployed core runner `ranking_publication_runner.run` against the Blob archive. The driver and its raw output were kept outside the repository and are not retained in this PR.

## Per-criterion result

| Criterion in #79 | Result | Evidence |
| --- | --- | --- |
| Named policy owner signs the first rule order | Unproven, and cannot be proven for the demo | The shipped policy `ranking-v1` has owner `to be named` and `is_signed` is false (`No named policy owner.`). Live publish with it was refused with `approval_missing` and wrote no blob. A signature is a human act by a named person; no one has been named and a synthetic signature would not satisfy the criterion. |
| Ranking snapshot publication is scheduled | Not proven; the cron trigger fired but the run failed | A schedule-triggered job (cron `50 * * * *`) fired at 2026-11-18T08:50:00Z unattended. That run failed with exit 1 because the deployed orchestrator image does not contain `zava_forward.orchestrator.ranking_publish`; so the shipped scheduled entry point is not deployed, and the infra job (`rankingPublish` in `infra/modules/containerapps.bicep`) is not provisioned. |
| Ranking snapshot publication is retained (ADR 0002 deviation) | Partly proven | With an in-job, explicitly labelled DEMO-ONLY synthetic owner policy (never in the repository), the deployed core runner published `ranking-1.0.0-2026-10-16-5f9c06c475de.json` (443 entries, 49,642 bytes) create-only to Blob; a repeat returned `already_published` with `written: false`; `verify` returned `ok`; readback gave the stored sha256 and metadata keys `as_of`, `policy_version`, `published_on`, `record_sha256`, `snapshot_hash`. The data was flagged `source_not_current` (as-of 2026-10-16, run date 2026-11-18). |

## What this does not prove

* The owner signature, the schedule approval and the retention period remain human decisions. The live container had no immutability policy, so Blob immutability (WORM) is unproven on Azure; infra tests cover only the Bicep definition.
* The scheduled run that fired used a job with the orchestrator image, which failed; the later publication was a manual start of the job with the API image, not the shipped `ranking_publish` entry point.
* The synthetic-owner publication shows mechanics only. It is not a signed first rule order, and the snapshot is demo data.
* Criteria one and two of #79 were already ticked and were not re-opened.

## Evidence limits

* The raw live-run output (443 cases, 49,642 bytes, the refusal, the deletion listing) is not retained in the repository. The figures are the worker's recorded observations and are unverified by the reviewer.
* Treat the Partly proven row as an unverified observation until the driver output is committed.

---
title: Issue 79 live ranking proof with retained evidence (demo)
description: Second 2026-11-18 demo run for issue 79 that retains the raw outputs the earlier note lacked, with a per-criterion proven or unproven table
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 79
  - ranking
  - snapshot publication
  - policy sign-off
estimated_reading_time: 6
---

Refs #79. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes; DPO/Legal approval and person-run assistive-technology testing not needed for the demo). Nothing here is production evidence. This note extends [the earlier run](./issue-79-live-ranking-publication-evidence-2026-11-18.md), whose raw output was not retained, by committing the raw output without secrets in [issue-79-live-ranking-2026-11-18/](./issue-79-live-ranking-2026-11-18/).

## What was run

* Repository tests on this worktree: core (146 tests, [core-ranking.log](./issue-79-live-ranking-2026-11-18/core-ranking.log)), API (76 tests, [api-ranking.log](./issue-79-live-ranking-2026-11-18/api-ranking.log)) and orchestrator (11 tests, [orch-ranking.log](./issue-79-live-ranking-2026-11-18/orch-ranking.log)) all passed.
* Live API, signed in with the staff test user through Playwright ([live_ranking_probe.py](./issue-79-live-ranking-2026-11-18/live_ranking_probe.py), credentials read at runtime and not printed): `/api/ranking/policy`, `/api/ranking/snapshot` twice and `/api/ranking/publication` on `ca-cutover-test-demo-api`. Summary in [live-api-summary.json](./issue-79-live-ranking-2026-11-18/live-api-summary.json). The screenshot taken during the run showed case-list names and addresses, so it is not retained: rank reasons on the case list are "Observed; raw output not retained".
* Live publication in a throwaway job `job-demo79-ranking-publish` (deployed API image, `id-cutover-test-api` identity) against a throwaway container `ranking-archive-demo79` ([job_driver.py](./issue-79-live-ranking-2026-11-18/job_driver.py), output in [job-output.txt](./issue-79-live-ranking-2026-11-18/job-output.txt)). Job and container were deleted; [cleanup-listing.txt](./issue-79-live-ranking-2026-11-18/cleanup-listing.txt) shows neither remains.

## Per-criterion result

| Criterion in #79 | Status | Evidence |
| --- | --- | --- |
| Same data and policy version give the same order (ticked) | Proven again, demo | Two live snapshot reads returned the same 443-entry order and `snapshot_hash` 27d32b36...; the in-job snapshot of the forward and reversed case list gave equal hashes (`two_snapshots_equal: true`); repository determinism and tie-break tests pass. |
| Policy file changes are versioned and hash-verified (ticked) | Proven again, demo | The live policy `zava-forward-home-ranking` 1.0.0 reports `content_hash` b66fdacc..., equal to the hash computed from the repository file; the signed demo variant produced a different hash (34d316a9...) and the runner verified it; hash-tamper tests pass. |
| Named policy owner signs the first rule order | Unproven, cannot be proven for the demo | The live policy shows owner `to be named`, status draft, `policy_signed: false`, `No named policy owner.`; the runner refused the shipped policy with `approval_missing` and wrote nothing. A signature is a human act by a person who has not been named; a synthetic signature would not satisfy the criterion. |
| Ranking snapshot publication is scheduled and retained | Partly proven (publication mechanics only); schedule and retention unproven | Create-only publication worked with a demo-only synthetic owner held in job memory: `published`, `written: true`, 443 cases; repeat `already_published`, `written: false`; `verify` `ok`; `schedule` `current`. Live `/api/ranking/publication` reports `count: 0`, `overdue: true`, runner `deployment scheduler (not yet configured)`. No cron-triggered run of the shipped `ranking_publish` entry point was demonstrated this run: the deployed orchestrator image lacks that module and an image build was refused (ACR returned 403, public network access disabled; no network rule was changed). The throwaway container had no immutability policy and no legal hold ([container-immutability.txt](./issue-79-live-ranking-2026-11-18/container-immutability.txt)), so write-once retention is unproven on Azure, and the retention period is a Legal decision outside the demo. |

## Limits

* The job reads the live 443-case store (as-of 2026-10-16), so the snapshot is synthetic demo data.
* The earlier note recorded a cron-fired job that failed because the image lacked the module; that is consistent with the current finding and is not repeated here.
* No source code changed, so the focused tier applies; `rpi-checks.py --all` was not run.

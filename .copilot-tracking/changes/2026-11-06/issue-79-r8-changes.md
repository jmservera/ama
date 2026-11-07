---
title: Issue 79 changes, continuation r8 (qualification of r7 adverse evidence)
ms.date: 2026-11-06
---

## What this adds

A candidate-side qualification of the r7 intermediate run. Nothing earlier is edited: the r7 [changes](issue-79-r7-changes.md) and [review](../../reviews/2026-11-06/issue-79-r7-review.md) keep their original wording and outcomes. Research, plan and details were committed first as `7112a379f1646b30f75c6d9c7a3953368c5729f8`, on intake head `0ec823b1`.

## Qualification of the r7 intermediate run

* The r7 Changes row "GREEN 1" records one failure (the no-clock guard rejecting `import datetime`). The retained events show that run was worse than the row says: unit exit 1 (36 tests, one failure), Ruff exit 1 (E501 at `test_ranking_publication_runner.py:200`) and format exit 1 (one file to reformat), completion event `f961d0f8-5771-4801-908e-1c4af4390025` at 2026-11-06T01:08:56.043Z.
* `a90060fa-362e-4d3b-a207-3b50b7f893c9` (01:08:57.987Z) shows the unchanged `test_module_has_no_clock_and_no_delete` rejecting `import datetime`. The test was not weakened; the fix used `calendar`.
* `c16deef4-b6df-48b0-a678-3fb1b49dbf40` (01:09:25.667Z) is the successful intermediate rerun after the `calendar` and format corrections. It reused `green.log`, `ruff.log` and `format.log`, so those current files are overwritten successful outputs, not complete original failed logs.
* The outer shell exit 0 does not make the earlier failing checks pass. The final separate `green2.log` and RED 2 sequence is unchanged.
* The Ruff and format failures are not discussed in the r7 records; this note supplies them. The original r4 post-hoc chronology failure and the genuine prospective r7 chronology are both preserved.

## Evidence identity and limits

* Extract: `/home/azureuser/.copilot/session-state/77149bdf-2f9a-4b04-b1dc-af3109946991/files/79-r7-adverse-native-event-extract.json`, SHA-256 `87e39f2b0ef0078859d7e06d7fee8c2a123d17ae0c3e6ba2825ad97fa397c115` (recomputed in this task). Original `events.jsonl` snapshot SHA-256 `6f7dfed1fa452bdb77f37206b3cd0fce8469f4f736a5768a1dce8eeca11cbaf4`. Six events: starts `b41e98fb-8664-48b6-aa3a-b7c4e697f5d7`, `2ea8e642-349d-495c-abe7-5f162ccc35a3`, `0830df22-273b-4ff0-9bf6-efcef4b9e89c` and the three completions above.
* The extract preserves six events, not recovered raw output files. This task verified the hash, event ids, times and the first start command. The exit codes and the E501 detail are as reported in the coordinator's recovery and the durable comment <https://github.com/jmservera/ama/issues/79#issuecomment-6673997116>, not re-derived here. That recovery is not new.
* Coordinator runs on `0ec823` (36 core and 25 API tests, four malformed-date reproductions) are historical, source-identical focused observations. This task ran no test, linter or type check and makes no fresh-run claim. They are not FULL evidence.
* No raw bundle or session is copied into Git.

## Checks performed (read-only)

Recorded in the [review](../../reviews/2026-11-06/issue-79-r8-review.md).

## Pending and open

* The whole feature remains FULL tier. Missing: current-main FULL receipt, independent exact-head assessment, hosted checks, human approval. #82 owns heavy admission; none was started or waited for.
* #79 acceptance is unproven: named publication or policy owner, actual scheduler and retained output, any live or approval criteria. No closing keyword and no ticks. Future publication stays a child of parent #73; nothing was moved, pushed or retargeted.

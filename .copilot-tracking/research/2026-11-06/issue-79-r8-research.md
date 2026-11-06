---
title: Issue 79 research, continuation r8 (candidate-side qualification of r7 adverse evidence)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

This research, the plan and the details are committed before any r8 Changes or Review file exists. No r4, r5, r6 or r7 record, source, test, log or state file is edited, repaired or regraded. The original r4 post-hoc chronology failure and the genuine prospective r7 chronology both stand.

## Identity and pins

* Task `issue-79-r8-r7-adverse-qualification`, parent `issue-79-r7-archived-date-validation`. Same original session `e4869dea-7260-432e-a2dd-1c7a3e01e32c`.
* Branch `feat/ranking-publication-runner-79`, intake head `0ec823b19c7878b92d238fed64bc66164bdad8e6`, tree `7396cc011dd35aaf9a40ca712447a99074f583a5`, empty ignored-inclusive status. Reviewed main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. Authenticated account `jmservera` (id 8036360); the existing repository-local privacy-safe email matches and is preserved.
* Research disposition `executed`; Planning Readiness `Ready`.

## Why a source-side qualification is needed

The coordinator already recovered the r7 adverse evidence and posted the durable comment <https://github.com/jmservera/ama/issues/79#issuecomment-6673997116>. This is not a new recovery. The committed r7 Changes and Review records, however, summarise the intermediate run as one failure fixed by using `calendar`, and omit that the same run also had Ruff and format failures. A reader of the branch alone would not see that, and the issue comment is not part of the candidate. A new dated record on the candidate closes that gap without editing the r7 records.

## Evidence verified read-only in this session

* Retained extract `/home/azureuser/.copilot/session-state/77149bdf-2f9a-4b04-b1dc-af3109946991/files/79-r7-adverse-native-event-extract.json`, SHA-256 `87e39f2b0ef0078859d7e06d7fee8c2a123d17ae0c3e6ba2825ad97fa397c115` (recomputed here and matching). It references the original `events.jsonl` with snapshot SHA-256 `6f7dfed1fa452bdb77f37206b3cd0fce8469f4f736a5768a1dce8eeca11cbaf4` and holds six events: three tool starts and three completions, each with a raw event SHA-256.
* Event identities and times (UTC): start `b41e98fb-8664-48b6-aa3a-b7c4e697f5d7` 01:08:49.437; completion `f961d0f8-5771-4801-908e-1c4af4390025` 01:08:56.043; start `2ea8e642-349d-495c-abe7-5f162ccc35a3` 01:08:57.926; completion `a90060fa-362e-4d3b-a207-3b50b7f893c9` 01:08:57.987; start `0830df22-273b-4ff0-9bf6-efcef4b9e89c` 01:09:07.062; completion `c16deef4-b6df-48b0-a678-3fb1b49dbf40` 01:09:25.667.
* Reported content of those events (from the coordinator's recovery; the extract preserves the events, and this session verified only the hash, event ids, times and the start command): the first run had unit exit 1 (36 tests, one failure), Ruff exit 1 (E501 at `test_ranking_publication_runner.py:200`) and format exit 1 (one file to reformat); the next event showed the unchanged `test_module_has_no_clock_and_no_delete` rejecting `import datetime`; the third run succeeded after the `calendar` and format corrections.

## Limits

* The start command in the first event wrote to `/tmp/i79-r7-logs/green.log`, `ruff.log` and `format.log`; the successful rerun reused the same names. Those current files are overwritten successful outputs, not complete original failed raw logs. The extract keeps six events, not recovered raw output files.
* An outer shell exit 0 does not make the individual failing checks pass.
* The final separate `green2.log`, `red2.log` sequence is unchanged.
* The coordinator's later runs on `0ec823` (36 core, 25 API tests, four malformed-date reproductions) are historical, source-identical focused observations, not a new r8 run and not FULL evidence.
* No raw bundle or original session is copied into Git.

## Boundary

Whole feature remains FULL tier. Pending: current-main FULL receipt, independent exact-head assessment, hosted checks, human approval. #82 owns heavy admission. #79 acceptance stays unproven: named publication or policy owner, an actual scheduler and retained output, and any live or approval criteria. No closing keyword, no acceptance ticks. The future publication remains a child of parent #73; no branch or PR is moved, published or retargeted.
